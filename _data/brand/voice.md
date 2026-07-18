# IT-Journey — Voice & Tone

> The narrative companion to [`voice.yml`](voice.yml). `voice.yml` is the
> machine-readable profile registry; this file is the prose a writer (human or
> the `brand-voice` skill) reads to internalize how IT-Journey sounds. Section
> guides point here — they never restate these pillars (DRY).

## Who is speaking

A practitioner who was a `n00b` not long ago and remembers exactly what was confusing. Knowledgeable but not superior; generous with context; honest about failure. The brand's whole promise is **zer0 → her0** — so the voice never gatekeeps and never makes the reader feel dumb for not knowing yet.

## Voice pillars

1. **Practical over theoretical.** Lead with the thing the reader can do. Theory
serves the task, not the other way around. Every claim earns its place with a command, a verify step, or first-hand experience.
2. **Honest about failure (DFF).** Show the dead ends, the error message, the fix.
   A chronicle that hides its struggles teaches less and reads as marketing.
3. **Plain over clever (KIS).** Short sentences. One idea each. If a sentence
   needs re-reading, cut it down. Explain jargon the first time it appears.
4. **Generous, not gatekeeping (COLAB).** "Here's how" not "obviously you just".
   Invite the reader in — issues, PRs, discussions — and credit others.
5. **Transparent about AI (AIPD).** When AI assisted the work, say so, and say
what it got right *and wrong*. Never imply blind trust; always show the human in the loop.

## The three profiles (see `voice.yml` for the machine view)

- **`practitioner-chronicle`** (default) — tutorials and AI-session chronicles.
Second person + imperative for steps, past tense for "what happened". Light emoji. This is the everyday IT-Journey voice.
- **`concept-essay`** — trends, ideas, business, culture, technology think-pieces.
More analytical and reflective; a clear argument backed by evidence; minimal emoji. Still lands on "so what does the reader do with this".
- **`muse-opinion`** — short-form opinion/news *muses* on the magazine landing.
First person, punchy, opinion stated early. Structure: **hook → take → one piece of evidence / one link out → zer0-to-her0 tie-back.** Moderate emoji, tight word budget.

## Tone by situation

| Situation | Tone |
|---|---|
| A beginner tutorial | Warm, patient, lots of "why". Assume nothing. |
| An advanced chronicle | Peer-to-peer, fast, assumes fluency; still shows verify steps. |
| Something broke | Matter-of-fact and specific. Name the error, the cause, the fix. |
| An opinion / muse | Confident and direct. Own the take; don't hedge it to death. |
| Crediting others | Specific and warm. Name people and link their work. |

## Do

- Open with the problem or the payoff, not throat-clearing.
- Write to one reader ("you"), not "users" or "one".
- Use real, tailored examples — never generic stock snippets.
- Prefer the open-source / free-tier path first (OSAP, PoLR).

## Don't

- No empty hype: cut **comprehensive, powerful, seamless, cutting-edge,
  revolutionary, game-changing, effortless** (see [`glossary.yml`](glossary.yml)).
- No "simply / just / obviously" — they shame the reader who's stuck.
- No unverified benchmark or "fastest/best" claims.
- Don't bury the lede; don't pad to hit a length.

## Example openings

- *practitioner-chronicle:* "The Azure deploy failed three times before the
  workflow turned green. Here's the one setting that fixed it."
- *concept-essay:* "Refactoring isn't a tech upgrade — it's a manufacturing
  decision. Here's why that framing changes the budget conversation."
- *muse-opinion:* "Hot take: most CI pipelines are slow because nobody owns the
  cache. I fixed ours in one line — and got 40 minutes a run back."
