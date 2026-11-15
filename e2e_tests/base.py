"""
e2e_tests/base.py
Base test case, fixtures, and assertion helpers for CornLearn LMS E2E test suite.
"""

import re
from datetime import date
from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone, translation

from accounts.models import Parent, Student
from core.models import Semester, Session
from course.models import Course, CourseAllocation, Program

User = get_user_model()


@override_settings(
    STATICFILES_STORAGE="django.contrib.staticfiles.storage.StaticFilesStorage",
    PASSWORD_HASHERS=["django.contrib.auth.hashers.MD5PasswordHasher"],
)
class BaseE2ETestCase(TestCase):
    """
    Base test case for all CornLearn LMS E2E tests.
    Sets up fast in-memory test DB, academic cycles, programs, courses,
    and pre-configured accounts for Student, Lecturer, Parent, and Admin.
    """

    def setUp(self):
        super().setUp()
        translation.activate("en")

    @classmethod
    def setUpTestData(cls):
        today = timezone.now().date()

        # 1. Academic Cycle Fixtures
        cls.session = Session.objects.create(
            session="2026/2027",
            is_current_session=True,
            next_session_begins=today,
        )
        cls.semester = Semester.objects.create(
            semester="First",
            is_current_semester=True,
            session=cls.session,
            next_semester_begins=today,
        )

        # 2. Program & Course Fixtures
        cls.program = Program.objects.create(
            title="Công nghệ Thông tin",
            summary="Chương trình đào tạo Kỹ sư Công nghệ Thông tin chuẩn chất lượng cao.",
        )
        cls.course = Course.objects.create(
            title="Lập trình Python Web",
            code="IT101",
            credit=3,
            program=cls.program,
            level="Cử nhân",
            semester="First",
            year=1,
            summary="Khóa học lập trình web toàn diện với Django framework.",
        )
        cls.course_elective = Course.objects.create(
            title="Học máy Nâng cao",
            code="IT201",
            credit=4,
            program=cls.program,
            level="Cử nhân",
            semester="First",
            year=2,
            is_elective=True,
            summary="Khóa học học máy chuyên sâu cho kỹ sư dữ liệu.",
        )

        # 3. User Roles Fixtures
        cls.admin_user = User.objects.create_superuser(
            username="admin_user",
            email="admin@cornlearn.edu.vn",
            password="Password123!",
        )

        cls.lecturer_user = User.objects.create_user(
            username="lecturer_user",
            first_name="Nguyen",
            last_name="Van A",
            email="lecturer@cornlearn.edu.vn",
            password="Password123!",
            is_lecturer=True,
            gender="M",
        )
        cls.lecturer_user.set_password("Password123!")
        cls.lecturer_user.save()
        # Allocate course to lecturer
        cls.allocation = CourseAllocation.objects.create(
            lecturer=cls.lecturer_user,
            session=cls.session,
        )
        cls.allocation.courses.add(cls.course)

        cls.student_user = User.objects.create_user(
            username="student_user",
            first_name="Tran",
            last_name="Thi B",
            email="student@cornlearn.edu.vn",
            password="Password123!",
            is_student=True,
            gender="F",
        )
        cls.student_user.set_password("Password123!")
        cls.student_user.save()
        cls.student_profile = Student.objects.create(
            student=cls.student_user,
            level="Cử nhân",
            program=cls.program,
        )

        cls.parent_user = User.objects.create_user(
            username="parent_user",
            first_name="Le",
            last_name="Van C",
            email="parent@cornlearn.edu.vn",
            password="Password123!",
            is_parent=True,
            gender="M",
        )
        cls.parent_profile = Parent.objects.create(
            user=cls.parent_user,
            student=cls.student_profile,
            first_name="Le",
            last_name="Van C",
            email="parent@cornlearn.edu.vn",
            relation_ship="Father",
        )

    # --- Authentication Helpers ---
    def login_as_student(self):
        """Forces login as pre-configured student persona."""
        self.client.force_login(self.student_user)

    def login_as_lecturer(self):
        """Forces login as pre-configured faculty persona."""
        self.client.force_login(self.lecturer_user)

    def login_as_admin(self):
        """Forces login as pre-configured superuser persona."""
        self.client.force_login(self.admin_user)

    def login_as_parent(self):
        """Forces login as pre-configured parent guardian persona."""
        self.client.force_login(self.parent_user)

    def login_as_anonymous(self):
        """Logs out client to simulate unauthenticated visitor."""
        self.client.logout()

    # --- Assertion & Routing Helpers ---
    def reverse_url(self, viewname, *args, **kwargs):
        """Resolves URL name using django.urls.reverse."""
        return reverse(viewname, args=args, kwargs=kwargs)

    def assertResponseSuccess(self, response, template_name=None):
        """Asserts HTTP status 200 and optionally checks template usage."""
        self.assertEqual(response.status_code, 200)
        if template_name:
            self.assertTemplateUsed(response, template_name)

    def assert_redirects_to_login(self, response):
        """Asserts response redirects unauthenticated visitor to login."""
        self.assertEqual(response.status_code, 302)
        location = response.headers.get("Location", "")
        self.assertTrue(
            "/accounts/login" in location or "login" in location,
            f"Expected redirect to login, got location: {location}",
        )

    def assert_redirects_to_home(self, response):
        """Asserts response redirects unauthorized user to home or root."""
        self.assertEqual(response.status_code, 302)
        location = response.headers.get("Location", "")
        home_urls = ["/", "/en/", reverse("home")]
        self.assertTrue(
            any(location == u or location.endswith(u) for u in home_urls),
            f"Expected redirect to home ('/' or '/en/'), got location: {location}",
        )

    def assert_branding_clean(self, content):
        """
        Zero-tolerance check: ensures no lingering 'SkyLearn' or 'DjangoSMS'
        in HTML string or byte payload.
        """
        if isinstance(content, bytes):
            content = content.decode("utf-8", errors="ignore")

        skylearn_match = re.search(r"\bSkyLearn\b", content, re.IGNORECASE)
        self.assertIsNone(
            skylearn_match,
            f"Lingering legacy brand 'SkyLearn' found: {skylearn_match}",
        )

        djangosms_match = re.search(r"\bDjangoSMS\b", content, re.IGNORECASE)
        self.assertIsNone(
            djangosms_match,
            f"Lingering legacy project name 'DjangoSMS' found: {djangosms_match}",
        )
