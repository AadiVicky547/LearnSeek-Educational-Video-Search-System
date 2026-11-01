"""Tests for concise and honest video metadata presentation."""

import unittest

from src.presentation import (
    build_theme_stylesheet,
    relevance_label,
    short_description,
)


class VideoPresentationTests(unittest.TestCase):
    def test_description_is_compacted_and_truncated(self):
        video = {"description": "A useful   lesson\nabout science " * 10}

        description = short_description(video, limit=50)

        self.assertLessEqual(len(description), 50)
        self.assertNotIn("\n", description)
        self.assertTrue(description.endswith("…"))

    def test_relevance_label_formats_only_a_real_numeric_score(self):
        self.assertEqual(relevance_label({"relevance_percent": 84.6}), "85% match")
        self.assertIsNone(relevance_label({}))
        self.assertIsNone(relevance_label({"relevance_percent": "85"}))

    def test_relevance_label_clamps_out_of_range_scores(self):
        self.assertEqual(relevance_label({"relevance_percent": 120}), "100% match")
        self.assertEqual(relevance_label({"relevance_percent": -2}), "0% match")

    def test_theme_styles_are_emitted_as_one_style_element(self):
        base_styles = ".stApp { background: white; }"
        dark_styles = ".stApp { background: #111927; }"

        light_stylesheet = build_theme_stylesheet(base_styles, dark_styles, False)
        dark_stylesheet = build_theme_stylesheet(base_styles, dark_styles, True)

        self.assertEqual(light_stylesheet.count("<style>"), 1)
        self.assertEqual(dark_stylesheet.count("<style>"), 1)
        self.assertIn(dark_styles, dark_stylesheet)
        self.assertNotIn(dark_styles, light_stylesheet)


if __name__ == "__main__":
    unittest.main()
