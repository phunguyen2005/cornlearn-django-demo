"""
e2e_tests/test_responsive_tokens.py
Verifies responsive viewport meta tags, Be Vietnam Pro typography,
design token colors, layout dimensions, and table responsive classes.
"""

import os
import re
from django.conf import settings
from django.test import SimpleTestCase
from django.urls import reverse

from e2e_tests.base import BaseE2ETestCase


class ResponsiveTokensTest(SimpleTestCase):
    """Validates responsive viewport tags, typography, and design tokens."""

    def setUp(self):
        self.templates_dir = os.path.join(settings.BASE_DIR, "templates")
        self.static_dir = os.path.join(settings.BASE_DIR, "static")

    def test_base_template_viewport_meta_tag(self):
        """Ensures base.html defines proper viewport meta tag."""
        path = os.path.join(self.templates_dir, "base.html")
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        viewport_regex = re.compile(
            r'<meta\s+name=["\']viewport["\']\s+content=["\'][^"\']*width=device-width[^"\']*["\']',
            re.IGNORECASE,
        )
        self.assertRegex(
            content,
            viewport_regex,
            "base.html must define responsive viewport meta tag with width=device-width",
        )

    def _read_stylesheets(self):
        """Reads cornlearn.css, style.css, style.min.css, and style.scss into a combined lowercase string."""
        candidates = [
            os.path.join(self.static_dir, "css", "cornlearn.css"),
            os.path.join(self.static_dir, "css", "style.css"),
            os.path.join(self.static_dir, "css", "style.min.css"),
            os.path.join(self.static_dir, "scss", "style.scss"),
        ]
        combined = ""
        for file_path in candidates:
            if os.path.exists(file_path):
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    combined += "\n" + f.read()
        self.assertTrue(len(combined) > 0, "At least one stylesheet must exist in static/css/")
        return combined

    def test_be_vietnam_pro_font_inclusion(self):
        """Ensures Be Vietnam Pro Google font is loaded in base.html and configured in CSS."""
        path = os.path.join(self.templates_dir, "base.html")
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        self.assertTrue(
            "Be+Vietnam+Pro" in content or "Be Vietnam Pro" in content,
            "base.html must include Google Fonts link for 'Be Vietnam Pro'",
        )
        css_content = self._read_stylesheets().lower()
        self.assertIn(
            "be vietnam pro",
            css_content,
            "Stylesheets (cornlearn.css) must configure 'Be Vietnam Pro' font-family",
        )

    def test_typography_be_vietnam_pro_configured(self):
        """Verifies Be Vietnam Pro typography is configured in stylesheets and base template."""
        self.test_be_vietnam_pro_font_inclusion()

    def test_design_tokens_in_css(self):
        """Ensures CSS defines Institutional Navy (#164E80), CTA (#2563EB), and Canvas (#FAF8FF)."""
        content = self._read_stylesheets().lower()

        self.assertIn(
            "164e80",
            content,
            "CSS must define primary institutional navy color token #164E80",
        )
        self.assertIn(
            "2563eb",
            content,
            "CSS must define primary CTA action color token #2563EB",
        )
        self.assertIn(
            "faf8ff",
            content,
            "CSS must define primary canvas background color token #FAF8FF",
        )

    def test_design_system_color_tokens_in_stylesheets(self):
        """Verifies #164E80, #2563EB, and #FAF8FF design tokens in static/css/cornlearn.css."""
        self.test_design_tokens_in_css()

    def test_critical_tables_have_table_responsive(self):
        """Ensures data tables are wrapped in .table-responsive for mobile support."""
        table_templates = [
            "accounts/student_list.html",
            "accounts/lecturer_list.html",
            "course/course_registration.html",
            "result/grade_results.html",
            "result/assessment_results.html",
            "quiz/sitting_list.html",
        ]
        for rel_path in table_templates:
            with self.subTest(template=rel_path):
                path = os.path.join(self.templates_dir, rel_path)
                if os.path.exists(path):
                    with open(path, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()
                    self.assertIn(
                        "table-responsive",
                        content,
                        f"{rel_path} table must be wrapped in a table-responsive container",
                    )

    def test_auth_pages_split_grid_classes(self):
        """Ensures login.html and register.html use 5:7 split responsive layout."""
        reg_base_path = os.path.join(self.templates_dir, "registration", "registration_base.html")
        reg_base_content = ""
        if os.path.exists(reg_base_path):
            with open(reg_base_path, "r", encoding="utf-8", errors="ignore") as f:
                reg_base_content = f.read()
        css_content = self._read_stylesheets()

        for name in ["login.html", "register.html"]:
            with self.subTest(template=name):
                path = os.path.join(self.templates_dir, "registration", name)
                self.assertTrue(os.path.exists(path), f"registration/{name} must exist")
                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                combined = content
                if "registration_base.html" in content:
                    combined += "\n" + reg_base_content + "\n" + css_content
                has_split = (
                    ("col-lg-5" in combined and "col-lg-7" in combined)
                    or ("lg:col-span-5" in combined and "lg:col-span-7" in combined)
                    or (
                        "auth-split-wrapper" in combined
                        and "auth-brand-side" in combined
                        and "auth-form-side" in combined
                        and "flex: 5" in combined
                        and "flex: 7" in combined
                    )
                )
                self.assertTrue(
                    has_split,
                    f"registration/{name} must use 5:7 split layout per Stitch specification",
                )

    def test_sidebar_fixed_width_token(self):
        """Ensures sidebar contract maintains 248px academic sidebar specification."""
        sidebar_path = os.path.join(self.templates_dir, "sidebar.html")
        content = self._read_stylesheets()
        if os.path.exists(sidebar_path):
            with open(sidebar_path, "r", encoding="utf-8", errors="ignore") as f:
                content += "\n" + f.read()

        # Strictly verify 248px (or 240px/250px) sidebar width token without tautological fallback
        self.assertTrue(
            any(width_token in content for width_token in ("248px", "240px", "250px")),
            "Sidebar must define 248px fixed width token in cornlearn.css or sidebar.html",
        )
        self.assertIn("248px", content)


class ResponsiveRenderedTest(BaseE2ETestCase):
    """Dynamic client rendering checks for responsive shells."""

    def test_responsive_meta_in_rendered_dashboard(self):
        """Checks viewport meta in rendered dashboard response."""
        self.login_as_admin()
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 200)
        content = response.content.decode("utf-8")
        self.assertIn('name="viewport"', content)
        self.assertIn('width=device-width', content)

    def test_responsive_meta_in_rendered_auth(self):
        """Checks viewport meta in rendered login page."""
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)
        content = response.content.decode("utf-8")
        self.assertIn('name="viewport"', content)
