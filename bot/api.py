from typing import Optional

import aiohttp

from .constants import TMIAPI


class ResponseCodeError(ValueError):
    """Raised when a non-OK HTTP Response is received"""

    def __init__(
        self,
        response: aiohttp.ClientResponse,
        response_json: Optional[dict] = None,
        response_text: str = "",
    ):
        self.status = response.status
        self.response_json = response_json or {}
        self.response_text = response_text
        self.response = response

    def __str__(self):
        response = self.response_json if self.response_json else self.response_text
        return f"Status: {self.status} Response: {response}"


class APIClient:
    """TMI API Wrapper"""

    def __init__(self, **session_kwargs):
        self.session = aiohttp.ClientSession(**session_kwargs)

    @staticmethod
    def _url_for(endpoint: str) -> str:
        return f"{TMIAPI.tmiapi}{endpoint}"

    async def maybe_raise_for_status(
        selfe, response: aiohttp.ClientResponse, should_raise: bool
    ) -> None:
        """Raise ResponseCodeError for non-OK response if an exception should be raised"""
        if should_raise and response.status >= 400:
            try:
                response_json = await response.json()
                raise ResponseCodeError(response=response, response_json=response_json)
            except aiohttp.ContentTypeError:
                response_text = await response.text()
                raise ResponseCodeError(response=response, response_text=response_text)

    async def request(
        self, method: str, endpoint: str, *, raise_for_status: bool = True, **kwargs
    ) -> dict:
        """Send an HTTP request to the site API and return the JSON response."""
        async with self.session.request(
            method.upper(), self._url_for(endpoint), **kwargs
        ) as resp:
            await self.maybe_raise_for_status(resp, raise_for_status)
            return await resp.json()

    async def get(
        self, endpoint: str, *, raise_for_status: bool = True, **kwargs
    ) -> dict:
        """Site API GET."""
        return await self.request(
            "GET", endpoint, raise_for_status=raise_for_status, **kwargs
        )

    async def patch(
        self, endpoint: str, *, raise_for_status: bool = True, **kwargs
    ) -> dict:
        """Site API PATCH."""
        return await self.request(
            "PATCH", endpoint, raise_for_status=raise_for_status, **kwargs
        )

    async def post(
        self, endpoint: str, *, raise_for_status: bool = True, **kwargs
    ) -> dict:
        """Site API POST."""
        return await self.request(
            "POST", endpoint, raise_for_status=raise_for_status, **kwargs
        )

    async def put(
        self, endpoint: str, *, raise_for_status: bool = True, **kwargs
    ) -> dict:
        """Site API PUT."""
        return await self.request(
            "PUT", endpoint, raise_for_status=raise_for_status, **kwargs
        )

    async def delete(
        self, endpoint: str, *, raise_for_status: bool = True, **kwargs
    ) -> Optional[dict]:
        """Site API DELETE."""
        async with self.session.delete(self._url_for(endpoint), **kwargs) as resp:
            if resp.status == 204:
                return None

            await self.maybe_raise_for_status(resp, raise_for_status)
            return await resp.json()
