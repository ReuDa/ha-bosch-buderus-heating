"""Bounded, authenticated read access to the Bacon claiming service."""

from __future__ import annotations

import json
import math
from collections.abc import Callable
from time import monotonic
from typing import Protocol

import aiohttp

from ..pointt.exceptions import AuthenticationError, PointTError, RateLimited
from .models import (
    CLAIM_URL,
    MAX_BYTES,
    USER_AGENT,
    BaconError,
    device_list,
    token_subject,
)


class TokenProvider(Protocol):
    async def get_access_token(
        self, *, force_refresh: bool = False, rejected_token: str | None = None
    ) -> str: ...


class BaconClient:
    def __init__(
        self,
        session: aiohttp.ClientSession,
        tokens: TokenProvider,
        *,
        url: str = CLAIM_URL,
        clock: Callable[[], float] = monotonic,
    ) -> None:
        self.session, self.tokens, self.url, self.clock = session, tokens, url, clock
        self.retry_at = 0.0
        self.subject: str | None = None

    async def access_token(self, *, rejected: str | None = None) -> str:
        """Share the existing serialized refresh and classify errors locally."""
        try:
            token = await self.tokens.get_access_token(
                force_refresh=rejected is not None, rejected_token=rejected
            )
        except AuthenticationError as err:
            raise BaconError("authentication") from err
        except RateLimited as err:
            delay = max(60, err.retry_after or 60)
            self.retry_at = self.clock() + delay
            raise BaconError("rate_limited", delay) from err
        except PointTError as err:
            raise BaconError("connection") from err
        subject = token_subject(token)
        if self.subject is not None and self.subject != subject:
            raise BaconError("account_changed")
        self.subject = subject
        return token

    async def get_devices(self) -> tuple[str, ...]:
        if self.clock() < self.retry_at:
            raise BaconError("rate_limited", self.retry_at - self.clock())
        token = await self.access_token()
        for attempt in range(2):
            try:
                async with self.session.get(
                    self.url,
                    headers={
                        "Authorization": f"Bearer {token}",
                        "User-Agent": USER_AGENT,
                    },
                    timeout=aiohttp.ClientTimeout(total=20),
                    allow_redirects=False,
                ) as response:
                    if response.status == 401 and attempt == 0:
                        token = await self.access_token(rejected=token)
                        continue
                    if response.status in (401, 403):
                        raise BaconError("authentication")
                    if response.status == 429:
                        try:
                            delay = float(response.headers.get("Retry-After", "60"))
                        except ValueError:
                            delay = 60
                        if not math.isfinite(delay) or delay < 0:
                            delay = 60
                        self.retry_at = self.clock() + max(60, delay)
                        raise BaconError("rate_limited", max(60, delay))
                    if response.status != 200:
                        raise BaconError("service_unavailable")
                    body = bytearray()
                    async for chunk in response.content.iter_chunked(16384):
                        body.extend(chunk)
                        if len(body) > MAX_BYTES:
                            raise BaconError("invalid_device_list")
                    result = device_list(json.loads(body))
                    return result
            except (TimeoutError, aiohttp.ClientError) as err:
                raise BaconError("connection") from err
            except (ValueError, UnicodeError) as err:
                raise BaconError("invalid_device_list") from err
        raise BaconError("authentication")
