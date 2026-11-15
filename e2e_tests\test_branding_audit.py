"""
e2e_tests/test_branding_audit.py
Automated zero-tolerance branding audit:
- Ensures 0 occurrences of 'SkyLearn' (case-insensitive) across all 80 HTML templates.
- Ensures 0 occurrences of legacy 'DjangoSMS' across all HTML templates.
- Verifies positive presence of 'CornLearn' in key brand anchors.
- Validates brand assets (brand.svg, brand.png, favicon.png).
- Validates admin site header and email templates.
- Dynamic rendered response checks across anonymous and authenticated personas.
"""

import os
import re
from django.conf import settings
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.test import SimpleTestCase
from django.urls import reverse

from e2e_tests.base import BaseE2ETestCase

User = get_user_model()


class TemplateBrandingAuditStaticTest(SimpleTestCase):
    """Static file scanning across all templates and static assets."""

    def setUp(self):
        self.templates_dir = os.path.join(settings.BASE_DIR, "templates")
        self.static_img_dir = os.path.join(settings.BASE_DIR, "static", "img")
        self.static_js_dir = os.path.join(settings.BASE_DIR, "static", "js")

    @staticmethod
    def _strip_comments(text):
        """Strips Django {% comment %} blocks and HTML <!-- --> comments."""
        text = re.sub(r"\{%\s*comment\b.*?\{%\s*endcomment\s*%\}", "", text, flags=re.DOTALL | re.IGNORECASE)
        text = re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)
        return text

    def test_zero_skylearn_in_html_templates(self):
        """Scans all .html files under templates/ to ensure no lingering 'SkyLearn'."""
        violations = []
        brand_regex = re.compile(r"sky[\s\-]*learn", re.IGNORECASE)

        for root, _, files in os.walk(self.templates_dir):
            for file in files:
                if file.endswith(".html"):
                    file_path = os.path.join(root, file)
                    rel_path = os.path.relpath(file_path, settings.BASE_DIR)
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                        raw_content = f.read()
                    for line_no, line in enumerate(raw_content.splitlines(), 1):
                        if brand_regex.search(line):
                            violations.append(f"{rel_path}:{line_no} -> {line.strip()}")
                    cleaned = self._strip_comments(raw_content)
                    if brand_regex.search(cleaned) and not any(v.startswith(rel_path) for v in violations):
                        violations.append(f"{rel_path}:multiline -> SkyLearn match")

        self.assertEqual(
            len(violations),
            0,
            f"Found {len(violations)} lingering 'SkyLearn' occurrences in templates:\n"
            + "\n".join(violations),
        )

    def test_zero_legacy_brand_strings_in_templates_and_static(self):
        """Scans templates/*.html and static/js/*.js (line-by-line and full content) for legacy brand strings."""
        violations = []
        legacy_regex = re.compile(r"(sky[\s\-]*learn|djangosms)", re.IGNORECASE)

        # 1. Scan all HTML templates
        for root, _, files in os.walk(self.templates_dir):
            for file in files:
                if file.endswith(".html"):
                    file_path = os.path.join(root, file)
                    rel_path = os.path.relpath(file_path, settings.BASE_DIR)
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                        raw_content = f.read()
                    cleaned = self._strip_comments(raw_content)
                    for line_no, line in enumerate(cleaned.splitlines(), 1):
                        if legacy_regex.search(line):
                            violations.append(f"{rel_path}:{line_no} -> {line.strip()}")
                    # Also check with tags stripped across newlines for multiline splits
                    text_only = re.sub(r"<[^>]+>", "", cleaned)
                    if legacy_regex.search(text_only) and not any(v.startswith(rel_path) for v in violations):
                        violations.append(f"{rel_path}:full_content -> legacy brand match")

        # 2. Scan static/js/*.js
        if os.path.exists(self.static_js_dir):
            for root, _, files in os.walk(self.static_js_dir):
                for file in files:
                    if file.endswith(".js"):
                        file_path = os.path.join(root, file)
                        rel_path = os.path.relpath(file_path, settings.BASE_DIR)
                        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                            js_content = f.read()
                        for line_no, line in enumerate(js_content.splitlines(), 1):
                            if legacy_regex.search(line):
                                violations.append(f"{rel_path}:{line_no} -> {line.strip()}")
                        if legacy_regex.search(js_content) and not any(v.startswith(rel_path) for v in violations):
                            violations.append(f"{rel_path}:full_content -> legacy brand match")

        self.assertEqual(
            len(violations),
            0,
            f"Found legacy brand occurrences in templates or static JS:\n" + "\n".join(violations),
        )

    def test_zero_djangosms_in_html_templates(self):
        """Ensures legacy project name 'DjangoSMS' is eliminated across templates."""
        violations = []
        legacy_regex = re.compile(r"DjangoSMS", re.IGNORECASE)

        for root, _, files in os.walk(self.templates_dir):
            for file in files:
                if file.endswith(".html"):
                    file_path = os.path.join(root, file)
                    rel_path = os.path.relpath(file_path, settings.BASE_DIR)
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                        for line_no, line in enumerate(f, 1):
                            if legacy_regex.search(line):
                                violations.append(f"{rel_path}:{line_no} -> {line.strip()}")

        self.assertEqual(
            len(violations),
            0,
            f"Found legacy 'DjangoSMS' occurrences in templates:\n" + "\n".join(violations),
        )

    def test_core_templates_contain_cornlearn(self):
        """Checks positive presence of 'CornLearn' in core layout templates."""
        core_templates = ["base.html", "sidebar.html", "navbar.html"]
        for tmpl in core_templates:
            with self.subTest(template=tmpl):
                path = os.path.join(self.templates_dir, tmpl)
                self.assertTrue(os.path.exists(path), f"{tmpl} must exist.")
                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                    self.assertIn(
                        "CornLearn",
                        content,
                        f"Template {tmpl} must display 'CornLearn' brand name.",
                    )

    def test_brand_assets_files_exist(self):
        """Verifies presence of modern CornLearn brand assets in static/img/."""
        brand_svg = os.path.join(self.static_img_dir, "brand.svg")
        brand_png = os.path.join(self.static_img_dir, "brand.png")
        favicon = os.path.join(self.static_img_dir, "favicon.png")

        self.assertTrue(os.path.exists(brand_svg), "static/img/brand.svg must exist")
        self.assertTrue(os.path.exists(brand_png), "static/img/brand.png must exist")
        self.assertTrue(os.path.exists(favicon), "static/img/favicon.png must exist")

    def test_static_brand_assets_exist(self):
        """Verifies brand assets exist and brand.svg renders 'CornLearn' when XML tags are stripped."""
        brand_svg = os.path.join(self.static_img_dir, "brand.svg")
        brand_png = os.path.join(self.static_img_dir, "brand.png")
        favicon = os.path.join(self.static_img_dir, "favicon.png")

        self.assertTrue(os.path.exists(brand_svg), "static/img/brand.svg must exist")
        self.assertTrue(os.path.exists(brand_png), "static/img/brand.png must exist")
        self.assertTrue(os.path.exists(favicon), "static/img/favicon.png must exist")

        with open(brand_svg, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
        stripped_text = re.sub(r"<[^>]+>", "", content).lower()
        self.assertNotIn("skylearn", stripped_text)
        self.assertIn("cornlearn", stripped_text)

    def test_brand_svg_contains_cornlearn(self):
        """Checks that brand.svg contains 'CornLearn' (after stripping XML tags like <tspan>) and not 'SkyLearn'."""
        brand_svg = os.path.join(self.static_img_dir, "brand.svg")
        self.assertTrue(os.path.exists(brand_svg), "static/img/brand.svg must exist")
        with open(brand_svg, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
        stripped_text = re.sub(r"<[^>]+>", "", content).lower()
        self.assertNotIn("skylearn", stripped_text)
        self.assertIn("cornlearn", stripped_text)

    def test_email_templates_rebranded(self):
        """Verifies that account confirmation email templates are completely rebranded."""
        email_dir = os.path.join(self.templates_dir, "accounts", "email")
        for filename in [
            "new_lecturer_account_confirmation.html",
            "new_student_account_confirmation.html",
        ]:
            with self.subTest(email_template=filename):
                file_path = os.path.join(email_dir, filename)
                self.assertTrue(os.path.exists(file_path), f"Email template {filename} must exist.")
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                    self.assertNotIn(
                        "skylearn",
                        content.lower(),
                        f"Email template {filename} must not contain 'SkyLearn'.",
                    )
                    self.assertIn(
                        "CornLearn",
                        content,
                        f"Email template {filename} must contain 'CornLearn'.",
                    )


class RenderedBrandingAuditTest(BaseE2ETestCase):
    """Dynamic response auditing via Django Client across all user personas."""

    def test_admin_site_header_branding(self):
        """Validates that Django admin site header has been updated to CornLearn."""
        self.assertNotIn("SkyLearn", admin.site.site_header)
        self.assertIn("CornLearn", admin.site.site_header)

    def test_public_auth_views_branding(self):
        """Validates that public unauthenticated pages render CornLearn without SkyLearn."""
        public_urls = [
            reverse("login"),
            reverse("register"),
            reverse("password_reset"),
            reverse("terms"),
            reverse("privacy"),
        ]
        for url in public_urls:
            with self.subTest(url=url):
                response = self.client.get(url, follow=True)
                self.assertEqual(response.status_code, 200)
                content = response.content.decode("utf-8", errors="ignore")
                self.assertNotIn("skylearn", content.lower())
                self.assertIn("CornLearn", content)

    def test_student_rendered_views_branding(self):
        """Validates that student authenticated pages contain CornLearn and 0 SkyLearn."""
        self.login_as_student()
        student_urls = [
            reverse("home"),
            reverse("profile"),
            reverse("user_course_list"),
            reverse("course_registration"),
        ]
        for url in student_urls:
            with self.subTest(url=url):
                response = self.client.get(url, follow=True)
                self.assertEqual(response.status_code, 200)
                self.assert_branding_clean(response.content)

    def test_lecturer_rendered_views_branding(self):
        """Validates that faculty authenticated pages contain CornLearn and 0 SkyLearn."""
        self.login_as_lecturer()
        lecturer_urls = [
            reverse("home"),
            reverse("profile"),
            reverse("session_list"),
            reverse("semester_list"),
            reverse("course_allocation_view"),
        ]
        for url in lecturer_urls:
            with self.subTest(url=url):
                response = self.client.get(url, follow=True)
                self.assertEqual(response.status_code, 200)
                self.assert_branding_clean(response.content)

    def test_admin_rendered_views_branding(self):
        """Validates that admin operations hub and dashboard contain CornLearn and 0 SkyLearn."""
        self.login_as_admin()
        admin_urls = [
            reverse("admin_panel"),
            reverse("dashboard"),
            reverse("lecturer_list"),
            reverse("student_list"),
        ]
        for url in admin_urls:
            with self.subTest(url=url):
                response = self.client.get(url, follow=True)
                self.assertEqual(response.status_code, 200)
                self.assert_branding_clean(response.content)
