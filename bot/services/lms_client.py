"""LMS API client for communicating with the backend."""

import httpx

from config import get_lms_api_base_url, get_lms_api_key


class LMSClient:
    """Client for the LMS backend API."""

    def __init__(self) -> None:
        self.base_url = get_lms_api_base_url()
        self.api_key = get_lms_api_key()
        self._client: httpx.Client | None = None

    def _get_client(self) -> httpx.Client:
        """Get or create an HTTP client with auth headers."""
        if self._client is None:
            self._client = httpx.Client(
                base_url=self.base_url,
                headers={"Authorization": f"Bearer {self.api_key}"} if self.api_key else {},
                timeout=10.0,
            )
        return self._client

    def health_check(self) -> bool:
        """Check if the backend is reachable.
        
        Returns:
            True if backend is up, False otherwise
        """
        try:
            client = self._get_client()
            response = client.get("/health")
            return response.status_code == 200
        except Exception:
            return False

    def get_items(self) -> list[dict]:
        """Get all items (labs) from the backend.
        
        Returns:
            List of items, or empty list on error
        """
        try:
            client = self._get_client()
            response = client.get("/items/")
            if response.status_code == 200:
                return response.json()
            return []
        except Exception:
            return []

    def get_analytics(self, lab: str) -> dict:
        """Get analytics for a specific lab.

        Args:
            lab: Lab identifier (e.g., "lab-04")

        Returns:
            Analytics data, or empty dict on error
        """
        try:
            client = self._get_client()
            response = client.get(f"/analytics/{lab}")
            if response.status_code == 200:
                return response.json()
            return {}
        except Exception:
            return {}

    def get_pass_rates(self, lab: str) -> list[dict]:
        """Get per-task pass rates for a lab.

        Args:
            lab: Lab identifier (e.g., "lab-04")

        Returns:
            List of pass rate data, or empty list on error
        """
        try:
            client = self._get_client()
            response = client.get("/analytics/pass-rates", params={"lab": lab})
            if response.status_code == 200:
                return response.json()
            return []
        except Exception:
            return []


# Global client instance for reuse
_lms_client: LMSClient | None = None


def get_lms_client() -> LMSClient:
    """Get the global LMS client instance."""
    global _lms_client
    if _lms_client is None:
        _lms_client = LMSClient()
    return _lms_client
