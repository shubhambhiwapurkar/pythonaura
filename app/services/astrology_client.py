import httpx
import logging
from app.core.config import get_settings

settings = get_settings()
logger = logging.getLogger(__name__)

class AstrologyServiceError(Exception):
    """Base exception for Astrology Service errors."""
    pass

class AstrologyServiceConnectionError(AstrologyServiceError):
    """Exception for connection errors to the Astrology Service."""
    pass

class AstrologyServiceClientError(AstrologyServiceError):
    """Exception for 4xx client errors from the Astrology Service."""
    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail
        super().__init__(f"Astrology Service returned {status_code}: {detail}")

class AstrologyServiceServerError(AstrologyServiceError):
    """Exception for 5xx server errors from the Astrology Service."""
    pass


async def create_birth_chart(birth_data: dict) -> dict:
    """Call the Astrology Service to create a new birth chart."""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{settings.ASTROLOGY_SERVICE_URL}/chart",
                json=birth_data,
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            if 400 <= e.response.status_code < 500:
                logger.warning(f"Client error from astrology service: {e.response.status_code} {e.response.text}")
                raise AstrologyServiceClientError(e.response.status_code, e.response.text) from e
            else:
                logger.error(f"Server error from astrology service: {e.response.status_code} {e.response.text}")
                raise AstrologyServiceServerError("Astrology service failed") from e
        except (httpx.RequestError, httpx.TimeoutException) as e:
            logger.error(f"Connection error calling astrology service: {e}")
            raise AstrologyServiceConnectionError("Could not connect to astrology service") from e

async def get_daily_transits(birth_chart_id: str) -> dict:
    """Call the Astrology Service to get daily transits for a birth chart."""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{settings.ASTROLOGY_SERVICE_URL}/chart/{birth_chart_id}/transits",
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            if 400 <= e.response.status_code < 500:
                logger.warning(f"Client error getting daily transits: {e.response.status_code} {e.response.text}")
                raise AstrologyServiceClientError(e.response.status_code, e.response.text) from e
            else:
                logger.error(f"Server error getting daily transits: {e.response.status_code} {e.response.text}")
                raise AstrologyServiceServerError("Astrology service failed") from e
        except (httpx.RequestError, httpx.TimeoutException) as e:
            logger.error(f"Connection error getting daily transits: {e}")
            raise AstrologyServiceConnectionError("Could not connect to astrology service") from e