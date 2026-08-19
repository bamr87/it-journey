#!/usr/bin/env python3
"""
youtube_upload.py — publish quest walkthrough videos to YouTube (stdlib-only).

The UPLOAD arm of the quest-video lane: consumes the deterministic upload plan
(video_manifest.py build), pushes each video to YouTube via the Data API v3
resumable-upload protocol, and writes videos/uploads.json — the record that
`video_manifest.py apply` turns into quest frontmatter + the committed catalog.

Design constraints (mirroring the fleet's guardrails):
  * NO third-party deps — urllib only, so the workflow needs no google-api
    client install and the supply-chain surface stays flat.
  * Credentials come ONLY from the environment (CI secrets):
        YOUTUBE_CLIENT_ID, YOUTUBE_CLIENT_SECRET, YOUTUBE_REFRESH_TOKEN
    (a one-time OAuth "installed app" consent with scope
     https://www.googleapis.com/auth/youtube.upload — see
     docs/quests/VIDEO_FRAMEWORK.md for the 10-minute setup)
    plus optional YOUTUBE_PLAYLIST_ID to file uploads into a playlist
    (needs the broader youtube scope on the refresh token).
  * IDEMPOTENT against the committed catalog (.quests/videos.yml): a quest
    that already has a published video is skipped unless --force, so a re-run
    workflow can never spam the channel with duplicates.
  * Default privacy is whatever the plan says (the lane defaults to unlisted);
    --privacy overrides for every item this run.

Usage:
  python3 scripts/quest/youtube_upload.py \
      --plan videos/upload-plan.json --out videos/uploads.json \
      [--catalog .quests/videos.yml] [--privacy unlisted] \
      [--force] [--dry-run] [--verify-only]

Exit: 0 all uploads ok (or everything skipped / nothing to do), 1 any upload
failed, 2 configuration error (missing credentials/files).
"""

from __future__ import annotations

import argparse
import json
import mimetypes
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

TOKEN_URL = "https://oauth2.googleapis.com/token"
UPLOAD_URL = ("https://www.googleapis.com/upload/youtube/v3/videos"
              "?uploadType=resumable&part=snippet,status")
PLAYLIST_URL = "https://www.googleapis.com/youtube/v3/playlistItems?part=snippet"
CHANNELS_URL = "https://www.googleapis.com/youtube/v3/channels?part=id&mine=true"
CHUNK = 8 * 1024 * 1024  # resumable-upload chunk size (multiple of 256 KiB)
RETRIES = 4


def log(msg: str):
    print(msg, file=sys.stderr, flush=True)


def die(msg: str, code: int = 2):
    log(f"❌ {msg}")
    sys.exit(code)


# ─────────────────────────────────────────────────────────────────────────────
# HTTP plumbing (urllib, honors HTTPS_PROXY from the environment)
# ─────────────────────────────────────────────────────────────────────────────

def _request(url: str, data: bytes | None = None, headers: dict | None = None,
             method: str = "GET", timeout: int = 120):
    req = urllib.request.Request(url, data=data, headers=headers or {}, method=method)
    return urllib.request.urlopen(req, timeout=timeout)  # noqa: S310 — fixed https endpoints


def _json_or_die(resp, what: str) -> dict:
    body = resp.read().decode("utf-8", "replace")
    try:
        return json.loads(body) if body.strip() else {}
    except json.JSONDecodeError:
        die(f"{what}: non-JSON response: {body[:400]}")


class Auth:
    """OAuth refresh-token → short-lived access token, refreshed on demand."""

    def __init__(self):
        self.client_id = os.environ.get("YOUTUBE_CLIENT_ID", "")
        self.client_secret = os.environ.get("YOUTUBE_CLIENT_SECRET", "")
        self.refresh_token = os.environ.get("YOUTUBE_REFRESH_TOKEN", "")
        self._token = ""

    def configured(self) -> bool:
        return bool(self.client_id and self.client_secret and self.refresh_token)

    def token(self, force: bool = False) -> str:
        if self._token and not force:
            return self._token
        data = urllib.parse.urlencode({
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "refresh_token": self.refresh_token,
            "grant_type": "refresh_token",
        }).encode()
        try:
            with _request(TOKEN_URL, data=data, method="POST",
                          headers={"Content-Type": "application/x-www-form-urlencoded"}) as resp:
                payload = _json_or_die(resp, "token refresh")
        except urllib.error.HTTPError as e:
            die(f"token refresh failed (HTTP {e.code}): {e.read().decode('utf-8', 'replace')[:400]}")
        self._token = payload.get("access_token") or ""
        if not self._token:
            die(f"token refresh returned no access_token: {payload}")
        return self._token


# ─────────────────────────────────────────────────────────────────────────────
# Resumable upload
# ─────────────────────────────────────────────────────────────────────────────

def start_session(auth: Auth, item: dict, size: int, ctype: str) -> str:
    body = json.dumps({"snippet": item["snippet"], "status": item["status"]},
                      ensure_ascii=False).encode()
    headers = {
        "Authorization": f"Bearer {auth.token()}",
        "Content-Type": "application/json; charset=UTF-8",
        "X-Upload-Content-Length": str(size),
        "X-Upload-Content-Type": ctype,
    }
    with _request(UPLOAD_URL, data=body, headers=headers, method="POST") as resp:
        loc = resp.headers.get("Location")
        if not loc:
            die("resumable-session init returned no Location header")
        return loc


def upload_file(auth: Auth, session_url: str, path: Path, ctype: str) -> dict:
    """PUT the file in chunks; resume on 308; retry transient errors."""
    size = path.stat().st_size
    sent = 0
    with path.open("rb") as fh:
        while sent < size:
            fh.seek(sent)
            chunk = fh.read(CHUNK)
            end = sent + len(chunk) - 1
            headers = {
                "Authorization": f"Bearer {auth.token()}",
                "Content-Type": ctype,
                "Content-Range": f"bytes {sent}-{end}/{size}",
            }
            for attempt in range(1, RETRIES + 1):
                try:
                    with _request(session_url, data=chunk, headers=headers,
                                  method="PUT", timeout=600) as resp:
                        if resp.status in (200, 201):
                            return _json_or_die(resp, "upload finalize")
                        sent = end + 1  # unexpected 2xx mid-file — advance
                    break
                except urllib.error.HTTPError as e:
                    if e.code == 308:  # resume-incomplete: server tells us what landed
                        rng = e.headers.get("Range", "")
                        sent = int(rng.rsplit("-", 1)[-1]) + 1 if "-" in rng else end + 1
                        break
                    if e.code == 401 and attempt < RETRIES:
                        auth.token(force=True)
                        headers["Authorization"] = f"Bearer {auth.token()}"
                        continue
                    if e.code in (500, 502, 503, 504) and attempt < RETRIES:
                        time.sleep(2 ** attempt)
                        continue
                    raise
                except (urllib.error.URLError, TimeoutError):
                    if attempt < RETRIES:
                        time.sleep(2 ** attempt)
                        continue
                    raise
    die("upload loop ended without a finalize response")  # pragma: no cover


def add_to_playlist(auth: Auth, playlist_id: str, video_id: str):
    body = json.dumps({"snippet": {
        "playlistId": playlist_id,
        "resourceId": {"kind": "youtube#video", "videoId": video_id},
    }}).encode()
    headers = {"Authorization": f"Bearer {auth.token()}",
               "Content-Type": "application/json; charset=UTF-8"}
    with _request(PLAYLIST_URL, data=body, headers=headers, method="POST") as resp:
        resp.read()


# ─────────────────────────────────────────────────────────────────────────────

def load_catalog_ids(path: Path) -> dict:
    """permalink → existing catalog entry (empty when no catalog / no pyyaml)."""
    if not path.exists():
        return {}
    try:
        import yaml  # noqa: PLC0415
    except ImportError:
        log("ℹ️  pyyaml not installed — catalog idempotency check skipped.")
        return {}
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    vids = data.get("videos") or {}
    return vids if isinstance(vids, dict) else {}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--plan", default="videos/upload-plan.json")
    ap.add_argument("--out", default="videos/uploads.json")
    ap.add_argument("--catalog", default=".quests/videos.yml")
    ap.add_argument("--privacy", choices=["public", "unlisted", "private"],
                    help="override the plan's privacy for every item this run")
    ap.add_argument("--force", action="store_true",
                    help="upload even when the catalog already has a video for the quest")
    ap.add_argument("--dry-run", action="store_true",
                    help="print what would upload; no network calls")
    ap.add_argument("--verify-only", action="store_true",
                    help="refresh the token + print the channel id, then exit")
    args = ap.parse_args()

    auth = Auth()
    if args.verify_only:
        if not auth.configured():
            die("YOUTUBE_CLIENT_ID / YOUTUBE_CLIENT_SECRET / YOUTUBE_REFRESH_TOKEN not set")
        with _request(CHANNELS_URL, headers={"Authorization": f"Bearer {auth.token()}"}) as resp:
            payload = _json_or_die(resp, "channels.list")
        ids = [i.get("id") for i in payload.get("items") or []]
        print(f"✅ credentials OK — channel id(s): {', '.join(ids) or '(none visible)'}")
        return 0

    plan_path = Path(args.plan)
    try:
        plan = json.loads(plan_path.read_text(encoding="utf-8"))
    except Exception as e:  # noqa: BLE001
        die(f"cannot read upload plan {plan_path}: {e}")
    items = plan.get("items") or []
    existing = load_catalog_ids(Path(args.catalog))

    result = {
        "schema_version": "1.0.0",
        "generated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "uploads": [], "skipped": [], "failures": [],
    }

    todo = []
    for item in items:
        permalink = item.get("permalink") or ""
        if not args.force and permalink in existing and existing[permalink].get("id"):
            result["skipped"].append({"permalink": permalink,
                                      "reason": f"already published as {existing[permalink]['id']} (use --force to replace)"})
            log(f"⏭️  {permalink} — already in the catalog; skipping.")
            continue
        f = Path(item.get("file") or "")
        if not f.exists():
            result["failures"].append({"permalink": permalink, "error": f"video file missing: {f}"})
            continue
        todo.append((item, f))

    if args.dry_run:
        for item, f in todo:
            privacy = args.privacy or item["status"].get("privacyStatus", "unlisted")
            log(f"DRY-RUN would upload {f} ({f.stat().st_size / 1e6:.1f} MB) as "
                f"“{item['snippet']['title']}” [{privacy}] → {item.get('permalink')}")
        Path(args.out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.out).write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n",
                                  encoding="utf-8")
        return 0

    if todo and not auth.configured():
        die("YOUTUBE_CLIENT_ID / YOUTUBE_CLIENT_SECRET / YOUTUBE_REFRESH_TOKEN not set "
            "(set the repo secrets, or run with --dry-run)")
    playlist = os.environ.get("YOUTUBE_PLAYLIST_ID", "")

    for item, f in todo:
        permalink = item.get("permalink") or ""
        if args.privacy:
            item["status"]["privacyStatus"] = args.privacy
        ctype = mimetypes.guess_type(str(f))[0] or "video/webm"
        size = f.stat().st_size
        log(f"⬆️  uploading {f.name} ({size / 1e6:.1f} MB) — “{item['snippet']['title']}” …")
        try:
            session = start_session(auth, item, size, ctype)
            payload = upload_file(auth, session, f, ctype)
            vid = payload.get("id") or ""
            if not vid:
                raise RuntimeError(f"upload finished but no video id in response: {payload}")
            if playlist:
                try:
                    add_to_playlist(auth, playlist, vid)
                except urllib.error.HTTPError as e:
                    log(f"⚠️  playlist add failed for {vid} (HTTP {e.code}) — video is still up.")
            result["uploads"].append({
                "slug": item.get("slug"), "name": item.get("name"),
                "permalink": permalink, "quest_path": item.get("quest_path"),
                "video_id": vid, "url": f"https://www.youtube.com/watch?v={vid}",
                "title": item["snippet"]["title"],
                "privacy": item["status"]["privacyStatus"],
                "recorded": item.get("recorded"), "run_url": item.get("run_url"),
                "slice": item.get("slice"), "duration_s": item.get("duration_s"),
                "verdict": item.get("verdict"), "score": item.get("score"),
            })
            log(f"✅ https://www.youtube.com/watch?v={vid}")
        except Exception as e:  # noqa: BLE001 — collect per-item, report at exit
            result["failures"].append({"permalink": permalink, "error": str(e)[:500]})
            log(f"⚠️  upload failed for {permalink}: {e}")

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    log(f"📄 {len(result['uploads'])} uploaded, {len(result['skipped'])} skipped, "
        f"{len(result['failures'])} failed → {out}")
    return 1 if result["failures"] else 0


if __name__ == "__main__":
    sys.exit(main())
