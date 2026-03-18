#!/usr/bin/env python3
"""
Vendor-agnostic AI client for IT-Journey scripts.

Provides a unified interface for chat completions across multiple AI providers
(OpenAI, Anthropic). Centralizes authentication, error handling, and fallback
logic so that individual scripts do not duplicate provider-specific code.

Usage:
    from ai_client import AIClient

    client = AIClient(provider="openai", model="gpt-4o-mini")
    result = client.chat(
        prompt="Summarise these broken links...",
        system="You are a concise link-health advisor.",
        max_tokens=500,
        temperature=0.2,
    )
    if result.success:
        print(result.content)
    else:
        print(result.error)

Environment Variables:
    OPENAI_API_KEY      - Required when provider is 'openai'
    ANTHROPIC_API_KEY   - Required when provider is 'anthropic'
    AI_PROVIDER         - Optional default provider override
    AI_MODEL            - Optional default model override
"""

import os
from dataclasses import dataclass
from typing import Optional, List, Dict, Any

try:
    import requests as _requests
    HAS_REQUESTS = True
except ImportError:
    _requests = None  # type: ignore[assignment]
    HAS_REQUESTS = False


# -- Default models per provider -------------------------------------------

DEFAULT_MODELS: Dict[str, str] = {
    "openai": "gpt-4o-mini",
    "anthropic": "claude-sonnet-4-20250514",
}

# -- Provider API endpoints ------------------------------------------------

_PROVIDER_ENDPOINTS: Dict[str, str] = {
    "openai": "https://api.openai.com/v1/chat/completions",
    "anthropic": "https://api.anthropic.com/v1/messages",
}

# -- Provider env-var names for API keys -----------------------------------

_PROVIDER_KEY_ENV: Dict[str, str] = {
    "openai": "OPENAI_API_KEY",
    "anthropic": "ANTHROPIC_API_KEY",
}


@dataclass
class ChatResult:
    """Unified result of a chat completion request."""
    success: bool
    content: Optional[str] = None
    error: Optional[str] = None
    provider: Optional[str] = None
    model: Optional[str] = None
    raw_response: Optional[Dict[str, Any]] = None


class AIClient:
    """Vendor-agnostic AI chat client.

    Parameters
    ----------
    provider : str
        One of ``"openai"``, ``"anthropic"``, or ``"none"``.
        ``"none"`` disables all API calls and ``chat()`` always returns a
        ``ChatResult(success=False, error="AI disabled")``.
    model : str | None
        Model identifier.  When *None* the per-provider default is used.
    api_key : str | None
        Explicit API key.  When *None* the key is read from the
        provider-specific environment variable at call time.
    timeout : int
        HTTP request timeout in seconds.
    """

    def __init__(
        self,
        provider: str = "none",
        model: Optional[str] = None,
        api_key: Optional[str] = None,
        timeout: int = 30,
    ):
        # Allow env-var overrides for easy CI configuration
        self.provider = os.environ.get("AI_PROVIDER", provider).lower()
        self.model = os.environ.get("AI_MODEL", model) or DEFAULT_MODELS.get(self.provider)
        self._api_key = api_key
        self.timeout = timeout

    # -- public API --------------------------------------------------------

    def chat(
        self,
        prompt: str,
        system: Optional[str] = None,
        max_tokens: int = 500,
        temperature: float = 0.3,
    ) -> ChatResult:
        """Send a chat completion request and return a ``ChatResult``.

        Parameters
        ----------
        prompt : str
            The user message / prompt.
        system : str | None
            Optional system message.
        max_tokens : int
            Maximum tokens to generate.
        temperature : float
            Sampling temperature.

        Returns
        -------
        ChatResult
            Always returns a result — never raises.
        """
        if self.provider == "none":
            return ChatResult(success=False, error="AI disabled (provider='none')")

        if not HAS_REQUESTS:
            return ChatResult(
                success=False,
                error="requests library not installed — cannot call AI APIs",
            )

        api_key = self._resolve_api_key()
        if not api_key:
            env_var = _PROVIDER_KEY_ENV.get(self.provider, "UNKNOWN")
            return ChatResult(
                success=False,
                error=f"API key not found — set {env_var} or pass api_key=",
            )

        dispatch = {
            "openai": self._call_openai,
            "anthropic": self._call_anthropic,
        }
        handler = dispatch.get(self.provider)
        if handler is None:
            return ChatResult(
                success=False,
                error=f"Unknown AI provider: {self.provider!r}",
            )

        return handler(
            api_key=api_key,
            prompt=prompt,
            system=system,
            max_tokens=max_tokens,
            temperature=temperature,
        )

    # -- internal helpers --------------------------------------------------

    def _resolve_api_key(self) -> Optional[str]:
        if self._api_key:
            return self._api_key
        env_var = _PROVIDER_KEY_ENV.get(self.provider)
        return os.environ.get(env_var) if env_var else None

    def _call_openai(
        self,
        api_key: str,
        prompt: str,
        system: Optional[str],
        max_tokens: int,
        temperature: float,
    ) -> ChatResult:
        messages: List[Dict[str, str]] = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": self.model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
        }

        try:
            resp = _requests.post(
                _PROVIDER_ENDPOINTS["openai"],
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                },
                json=payload,
                timeout=self.timeout,
            )
            if resp.status_code == 200:
                data = resp.json()
                content = data["choices"][0]["message"]["content"]
                return ChatResult(
                    success=True,
                    content=content,
                    provider="openai",
                    model=self.model,
                    raw_response=data,
                )
            return ChatResult(
                success=False,
                error=f"OpenAI API error {resp.status_code}: {resp.text[:200]}",
                provider="openai",
                model=self.model,
            )
        except Exception as exc:
            return ChatResult(
                success=False,
                error=f"OpenAI request failed: {exc}",
                provider="openai",
                model=self.model,
            )

    def _call_anthropic(
        self,
        api_key: str,
        prompt: str,
        system: Optional[str],
        max_tokens: int,
        temperature: float,
    ) -> ChatResult:
        payload: Dict[str, Any] = {
            "model": self.model,
            "max_tokens": max_tokens,
            "messages": [{"role": "user", "content": prompt}],
        }
        if system:
            payload["system"] = system

        try:
            resp = _requests.post(
                _PROVIDER_ENDPOINTS["anthropic"],
                headers={
                    "x-api-key": api_key,
                    "anthropic-version": "2023-06-01",
                    "Content-Type": "application/json",
                },
                json=payload,
                timeout=self.timeout,
            )
            if resp.status_code == 200:
                data = resp.json()
                content = data["content"][0]["text"]
                return ChatResult(
                    success=True,
                    content=content,
                    provider="anthropic",
                    model=self.model,
                    raw_response=data,
                )
            return ChatResult(
                success=False,
                error=f"Anthropic API error {resp.status_code}: {resp.text[:200]}",
                provider="anthropic",
                model=self.model,
            )
        except Exception as exc:
            return ChatResult(
                success=False,
                error=f"Anthropic request failed: {exc}",
                provider="anthropic",
                model=self.model,
            )
