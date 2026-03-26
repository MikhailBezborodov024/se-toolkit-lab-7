"""LLM client for intent classification and tool calling."""

import json

import httpx

from config import get_llm_api_base_url, get_llm_api_key, get_llm_api_model


class LLMClient:
    """Client for the LLM API (Qwen proxy)."""

    def __init__(self) -> None:
        self.base_url = get_llm_api_base_url()
        self.api_key = get_llm_api_key()
        self.model = get_llm_api_model()
        self._client: httpx.Client | None = None

    def _get_client(self) -> httpx.Client:
        """Get or create an HTTP client with auth headers."""
        if self._client is None:
            # Remove /v1 suffix if present since we add it in requests
            base_url = self.base_url.rstrip("/v1").rstrip("/")
            self._client = httpx.Client(
                base_url=base_url,
                headers={"Authorization": f"Bearer {self.api_key}"} if self.api_key else {},
                timeout=30.0,
            )
        return self._client

    def chat(self, messages: list[dict], tools: list[dict] | None = None) -> dict:
        """Send a chat request to the LLM.

        Args:
            messages: List of message dicts with 'role' and 'content'
            tools: Optional list of tool definitions for function calling

        Returns:
            LLM response dict with 'content' or 'tool_calls'
        """
        try:
            client = self._get_client()
            
            payload = {
                "model": self.model,
                "messages": messages,
            }
            
            if tools:
                payload["tools"] = tools
                payload["tool_choice"] = "auto"
            
            response = client.post("/v1/chat/completions", json=payload)
            
            if response.status_code != 200:
                return {"error": f"LLM API error: HTTP {response.status_code}"}
            
            data = response.json()
            choice = data.get("choices", [{}])[0]
            message = choice.get("message", {})
            
            # Check for tool calls
            tool_calls = message.get("tool_calls")
            if tool_calls:
                return {"tool_calls": tool_calls}
            
            # Return content
            content = message.get("content", "")
            return {"content": content}
            
        except httpx.RequestError as e:
            return {"error": f"LLM connection error: {str(e)}"}
        except Exception as e:
            return {"error": f"LLM error: {str(e)}"}


# Global client instance for reuse
_llm_client: LLMClient | None = None


def get_llm_client() -> LLMClient:
    """Get the global LLM client instance."""
    global _llm_client
    if _llm_client is None:
        _llm_client = LLMClient()
    return _llm_client
