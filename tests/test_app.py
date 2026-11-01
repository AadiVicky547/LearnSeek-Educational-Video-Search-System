"""Basic offline checks for the Streamlit entry point."""

import ast
import unittest
from pathlib import Path


class LearnSeekAppTests(unittest.TestCase):
    def test_homepage_source_is_valid_and_has_search_controls(self):
        app_path = Path(__file__).resolve().parents[1] / "src" / "app.py"
        source = app_path.read_text(encoding="utf-8")
        presentation_path = app_path.with_name("presentation.py")
        presentation_source = presentation_path.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=str(app_path))

        self.assertTrue(tree.body)
        self.assertIn("LearnSeek", source)
        self.assertIn("st.text_input", source)
        self.assertIn("st.form_submit_button", source)
        self.assertIn("search_youtube_videos", source)
        self.assertIn("for video in videos", source)
        self.assertIn("st.container(border=True)", source)
        self.assertIn("st.image", source)
        self.assertIn("#f7f9fc", source)
        self.assertIn('[data-testid="stHeader"] { display: none !important; }', source)
        self.assertNotIn("position: sticky", source)
        self.assertIn('[data-testid="stToolbar"] { display: none !important; }', source)
        self.assertIn("justify-content: center", source)
        self.assertIn("opacity: 1 !important", source)
        self.assertIn("color: #ffffff !important", source)
        self.assertIn("font-size: clamp(1.65rem, 3vw, 2rem)", source)
        self.assertNotIn('href="#about"', source)
        self.assertNotIn("brand-tagline", source)
        self.assertNotIn("top-nav", source)
        self.assertIn("build_theme_stylesheet", source)
        self.assertIn("theme.type", source)
        self.assertNotIn("theme_toggle", source)
        self.assertIn("data-testid=\"stLinkButton\"", source)
        self.assertIn("color-scheme: dark", source)
        self.assertIn("relevance_label", presentation_source)


if __name__ == "__main__":
    unittest.main()
