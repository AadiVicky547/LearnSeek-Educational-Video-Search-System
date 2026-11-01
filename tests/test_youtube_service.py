"""Offline unit tests for LearnSeek's YouTube result mapping and error handling."""

import json
import unittest
from unittest.mock import MagicMock, patch

import httplib2
from googleapiclient.errors import HttpError

from src.youtube_service import (
    MissingApiKeyError,
    YouTubeQuotaError,
    YouTubeNetworkError,
    search_youtube_videos,
)


class YouTubeSearchTests(unittest.TestCase):
    @staticmethod
    def _mock_client(response=None, error=None):
        request = MagicMock()
        if error is not None:
            request.execute.side_effect = error
        else:
            request.execute.return_value = response or {"items": []}
        service = MagicMock()
        service.search.return_value.list.return_value = request
        return service

    @patch.dict("os.environ", {"YOUTUBE_API_KEY": "test-key"})
    @patch("src.youtube_service.build")
    def test_maps_video_fields_and_requests_ten(self, build):
        build.return_value = self._mock_client(
            {
                "items": [
                    {
                        "id": {"videoId": "abc123"},
                        "snippet": {
                            "title": "Fractions made simple",
                            "description": "A short lesson.",
                            "channelTitle": "Learn Channel",
                            "publishedAt": "2024-01-02T03:04:05Z",
                            "thumbnails": {
                                "high": {"url": "https://img.youtube.com/high.jpg"},
                                "default": {"url": "https://img.youtube.com/default.jpg"},
                            },
                        },
                    }
                ]
            }
        )

        result = search_youtube_videos("fractions")

        self.assertEqual(
            result[0],
            {
                "title": "Fractions made simple",
                "description": "A short lesson.",
                "video_id": "abc123",
                "video_url": "https://www.youtube.com/watch?v=abc123",
                "thumbnail_url": "https://img.youtube.com/high.jpg",
                "channel_name": "Learn Channel",
                "published_at": "2024-01-02T03:04:05Z",
                "category": "fractions",
            },
        )
        _, kwargs = build.call_args
        self.assertEqual(kwargs["developerKey"], "test-key")
        self.assertTrue(kwargs["cache_discovery"] is False)
        build.return_value.search.return_value.list.assert_called_once_with(
            part="snippet",
            q="fractions",
            type="video",
            maxResults=10,
            safeSearch="moderate",
            order="relevance",
        )

    @patch.dict("os.environ", {"YOUTUBE_API_KEY": ""})
    def test_missing_key_is_reported_before_api_call(self):
        with patch("src.youtube_service.build") as build:
            with self.assertRaises(MissingApiKeyError):
                search_youtube_videos("biology")
        build.assert_not_called()

    @patch.dict("os.environ", {"YOUTUBE_API_KEY": "test-key"})
    @patch("src.youtube_service.build")
    def test_quota_error_is_safe_and_specific(self, build):
        response = httplib2.Response({"status": "403"})
        error = HttpError(
            response,
            json.dumps(
                {"error": {"errors": [{"reason": "quotaExceeded"}]}}
            ).encode("utf-8"),
        )
        build.return_value = self._mock_client(error=error)

        with self.assertRaises(YouTubeQuotaError) as raised:
            search_youtube_videos("biology")
        self.assertNotIn("test-key", str(raised.exception))

    @patch.dict("os.environ", {"YOUTUBE_API_KEY": "test-key"})
    @patch("src.youtube_service.build")
    def test_network_failure_has_a_safe_message(self, build):
        build.return_value = self._mock_client(error=OSError("private request details"))

        with self.assertRaises(YouTubeNetworkError) as raised:
            search_youtube_videos("biology")
        self.assertNotIn("private request details", str(raised.exception))

    def test_blank_query_is_rejected_without_api_call(self):
        with patch("src.youtube_service.build") as build:
            with self.assertRaises(ValueError):
                search_youtube_videos("  ")
        build.assert_not_called()


if __name__ == "__main__":
    unittest.main()
