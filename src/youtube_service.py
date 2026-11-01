"""Small YouTube Data API v3 client used by the LearnSeek Phase 1 UI."""

from __future__ import annotations

import os
import socket
import ssl
from pathlib import Path
from typing import Any

import httplib2
from dotenv import load_dotenv
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


PROJECT_ROOT = Path(__file__).resolve().parent.parent
ENV_FILE = PROJECT_ROOT / ".env"
load_dotenv(dotenv_path=ENV_FILE)

API_SERVICE_NAME = "youtube"
API_VERSION = "v3"
RESULT_LIMIT = 10
QUOTA_REASONS = {
    "quotaExceeded",
    "dailyLimitExceeded",
    "rateLimitExceeded",
    "userRateLimitExceeded",
}


class YouTubeSearchError(Exception):
    """Safe-to-display base error for a YouTube search failure."""


class MissingApiKeyError(YouTubeSearchError):
    """Raised when the YouTube API key is not configured."""


class YouTubeQuotaError(YouTubeSearchError):
    """Raised when the API reports that its quota has been exhausted."""


class YouTubeNetworkError(YouTubeSearchError):
    """Raised when a network problem prevents an API request."""


class YouTubeAPIError(YouTubeSearchError):
    """Raised for other YouTube API or response failures."""


def _read_api_key() -> str:
    """Read the key from the process environment without exposing it."""
    load_dotenv(dotenv_path=ENV_FILE)
    key = os.getenv("YOUTUBE_API_KEY", "").strip()
    if not key:
        raise MissingApiKeyError(
            "The YouTube API key is missing. Add YOUTUBE_API_KEY to the project .env file."
        )
    return key


def _get_error_reasons(error: HttpError) -> set[str]:
    """Extract only API reason codes; never return or display raw error content."""
    try:
        payload = error.content
        if isinstance(payload, bytes):
            payload = payload.decode("utf-8", errors="ignore")
        import json

        body = json.loads(payload or "{}")
        error_items = body.get("error", {}).get("errors", [])
        return {item.get("reason", "") for item in error_items if item.get("reason")}
    except (AttributeError, TypeError, ValueError):
        return set()


def search_youtube_videos(query: str) -> list[dict[str, str]]:
    """Fetch up to 10 current video results for a non-empty query.

    The ``category`` value records the user's search topic. YouTube's search
    endpoint does not return LearnSeek's own nine subject categories.
    """
    clean_query = query.strip()
    if not clean_query:
        raise ValueError("Enter a search topic before searching.")

    api_key = _read_api_key()
    try:
        youtube = build(
            API_SERVICE_NAME,
            API_VERSION,
            developerKey=api_key,
            cache_discovery=False,
        )
        response: dict[str, Any] = (
            youtube.search()
            .list(
                part="snippet",
                q=clean_query,
                type="video",
                maxResults=RESULT_LIMIT,
                safeSearch="moderate",
                order="relevance",
            )
            .execute()
        )
    except HttpError as error:
        if _get_error_reasons(error) & QUOTA_REASONS:
            raise YouTubeQuotaError(
                "The YouTube API quota is currently exhausted. Try again later."
            ) from None
        raise YouTubeAPIError(
            "YouTube could not complete the search. Please try again later."
        ) from None
    except (httplib2.HttpLib2Error, socket.timeout, ssl.SSLError, OSError, TimeoutError):
        raise YouTubeNetworkError(
            "A network problem prevented the YouTube search. Check your connection and try again."
        ) from None
    except Exception:
        # Keep unexpected library errors safe for the UI: some exception text
        # may contain request details, so do not forward it to users or logs.
        raise YouTubeAPIError(
            "YouTube search is temporarily unavailable. Please try again later."
        ) from None

    videos: list[dict[str, str]] = []
    for item in response.get("items", []):
        video_id = item.get("id", {}).get("videoId")
        snippet = item.get("snippet", {})
        if not video_id:
            continue

        thumbnails = snippet.get("thumbnails", {})
        thumbnail_url = next(
            (
                thumbnails[size].get("url", "")
                for size in ("maxres", "high", "standard", "medium", "default")
                if isinstance(thumbnails.get(size), dict)
                and thumbnails[size].get("url")
            ),
            "",
        )

        videos.append(
            {
                "title": snippet.get("title", "Untitled video"),
                "description": snippet.get("description", ""),
                "video_id": video_id,
                "video_url": f"https://www.youtube.com/watch?v={video_id}",
                "thumbnail_url": thumbnail_url,
                "channel_name": snippet.get("channelTitle", "Unknown channel"),
                "published_at": snippet.get("publishedAt")
                or snippet.get("publishTime", ""),
                "category": clean_query,
            }
        )

    return videos
