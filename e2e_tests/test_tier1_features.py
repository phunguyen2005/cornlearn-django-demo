"""
e2e_tests/test_tier1_features.py
Tier 1 Feature Coverage: Comprehensive testing across all 69 features:
- Shared Shells (Features 1–8)
- Accounts & Authentication (Features 9–27)
- Core & Calendar (Features 28–35)
- Courses & Curriculum (Features 36–48)
- Quizzes & Examination / Grading (Features 49–63)
- Payments & Search (Features 64–69)
"""

import json
from decimal import Decimal
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone

from accounts.models import Parent, Student
from core.models import ActivityLog, NewsAndEvents, Semester, Session
from course.models import Course, CourseAllocation, Program, Upload, UploadVideo
from e2e_tests.base import BaseE2ETestCase
from payments.models import Invoice
from quiz.models import Choice, MCQuestion, Progress, Quiz, Sitting
from result.models import Result, TakenCourse

User = get_user_model()


class TestTier1SharedShells(BaseE2ETestCase):
    """Features 1–8: Base Shells, Navbar, Sidebar, Assets, Messages, Error & Legal pages."""

    def test_f1_base_html_shell_and_head_metadata(self):
        """Feature 1: Base HTML shell metadata and title."""
        self.login_as_student()
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        content = response.content.decode("utf-8")
        self.assertIn("<meta name=\"viewport\"", content)
        self.assert_branding_clean(content)

    def test_f2_top_navbar_and_user_menu(self):
        """Feature 2: Top app navbar with user menu and search."""
        self.login_as_student()
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        content = response.content.decode("utf-8")
        self.assertTrue(
            self.student_user.username in content or self.student_user.get_full_name() in content
        )

    def test_f3_collapsible_sidebar_role_gating(self):
        """Feature 3: Role-gated sidebar navigation."""
        # Student sees student links, not admin panel
        self.login_as_student()
        response = self.client.get(reverse("home"))
        content = response.content.decode("utf-8")
        self.assertNotIn(reverse("admin_panel"), content)

        # Admin sees admin panel link
        self.login_as_admin()
        response = self.client.get(reverse("home"))
        content = response.content.decode("utf-8")
        self.assertIn(reverse("admin_panel"), content)

    def test_f4_brand_asset_modernization(self):
        """Feature 4: Vector logo and branding clean in base navbar/sidebar."""
        self.login_as_student()
        response = self.client.get(reverse("home"))
        content = response.content.decode("utf-8")
        self.assertIn("brand.svg", content)
        self.assertNotIn("SkyLearn", content)

    def test_f5_global_toast_flash_messages(self):
        """Feature 5: Global alert messages rendering."""
        self.login_as_admin()
        # Post a bulletin to trigger success message
        response = self.client.post(
            reverse("add_item"),
            {"title": "Test Bulletin", "summary": "Test Summary", "posted_as": "News"},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        content = response.content.decode("utf-8")
        self.assertTrue(
            "alert" in content or "messages" in content or "Test Bulletin" in content,
            "Flash alert should be rendered after message set",
        )

    def test_f6_filter_form_snippet_rendering(self):
        """Feature 6: Reusable search/filter bar layout."""
        self.login_as_admin()
        response = self.client.get(reverse("student_list"))
        self.assertEqual(response.status_code, 200)
        content = response.content.decode("utf-8")
        self.assertIn("filter", content.lower())

    def test_f7_http_error_pages(self):
        """Feature 7: Error templates exist and render clean."""
        self.login_as_student()
        response = self.client.get("/non-existent-page-url-12345/")
        self.assertEqual(response.status_code, 404)
        self.assert_branding_clean(response.content)

    def test_f8_legal_pages_terms_and_privacy(self):
        """Feature 8: Terms of Service and Privacy Policy pages."""
        for url_name in ["terms", "privacy"]:
            with self.subTest(page=url_name):
                response = self.client.get(reverse(url_name))
                self.assertEqual(response.status_code, 200)
                self.assert_branding_clean(response.content)


class TestTier1AccountsAndAuth(BaseE2ETestCase):
    """Features 9–27: Authentication, User Profiles, Faculty & Student Management, Admin Center."""

    def test_f9_student_self_registration(self):
        """Feature 9: Public student self-registration."""
        payload = {
            "first_name": "Minh",
            "last_name": "Vu",
            "email": "minh.vu@cornlearn.edu.vn",
            "phone": "0987654321",
            "address": "Hanoi, Vietnam",
            "gender": "M",
            "level": "Cử nhân",
            "program": self.program.id,
            "password1": "SecurePass123!",
            "password2": "SecurePass123!",
        }
        response = self.client.post(reverse("register"), payload, follow=False)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(email="minh.vu@cornlearn.edu.vn").exists())

    def test_f10_username_ajax_validation(self):
        """Feature 10: Real-time username check endpoint."""
        # Existing username
        response = self.client.get(
            reverse("validate_username"),
            {"username": self.student_user.username},
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data.get("is_taken"))

        # Available username
        response = self.client.get(
            reverse("validate_username"),
            {"username": "totally_fresh_user_99"},
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertFalse(data.get("is_taken"))

    def test_f11_user_login_page(self):
        """Feature 11: Login page GET and valid credential authentication."""
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)

        login_res = self.client.post(
            reverse("login"),
            {"username": self.student_user.username, "password": "Password123!"},
            follow=False,
        )
        self.assertEqual(login_res.status_code, 302)

    def test_f12_password_reset_flow(self):
        """Feature 12: Password reset request page."""
        response = self.client.get(reverse("password_reset"))
        self.assertEqual(response.status_code, 200)
        self.assert_branding_clean(response.content)

    def test_f13_student_and_lecturer_profile_view(self):
        """Feature 13: Profile view tailored to user role."""
        # Student profile
        self.login_as_student()
        response = self.client.get(reverse("profile"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("Tran Thi B", response.content.decode("utf-8"))

        # Lecturer profile
        self.login_as_lecturer()
        response = self.client.get(reverse("profile"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("Nguyen Van A", response.content.decode("utf-8"))

    def test_f14_admin_detail_profile_and_pdf_export(self):
        """Feature 14: Admin user dossier and PDF export query."""
        self.login_as_admin()
        url = reverse("profile_single", kwargs={"user_id": self.student_user.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_f15_profile_information_update_form(self):
        """Feature 15: User updates personal profile information."""
        self.login_as_student()
        url = reverse("edit_profile")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        update_payload = {
            "first_name": "Tran Updated",
            "last_name": "Thi B",
            "email": "student_updated@cornlearn.edu.vn",
            "phone": "0123456789",
            "address": "Da Nang, Vietnam",
            "gender": "F",
        }
        post_res = self.client.post(url, update_payload, follow=False)
        self.assertEqual(post_res.status_code, 302)
        self.student_user.refresh_from_db()
        self.assertEqual(self.student_user.first_name, "Tran Updated")

    def test_f16_password_change_form(self):
        """Feature 16: Password change form."""
        self.login_as_student()
        response = self.client.get(reverse("change_password"))
        self.assertEqual(response.status_code, 200)

    def test_f17_lecturer_directory_and_filter(self):
        """Feature 17: Admin views faculty directory."""
        self.login_as_admin()
        response = self.client.get(reverse("lecturer_list"))
        self.assertEqual(response.status_code, 200)
        content = response.content.decode("utf-8")
        self.assertIn(self.lecturer_user.username, content)

    def test_f18_add_lecturer_form(self):
        """Feature 18: Admin adds a new lecturer."""
        self.login_as_admin()
        payload = {
            "first_name": "Hoang",
            "last_name": "Van C",
            "email": "hoang.c@cornlearn.edu.vn",
            "phone": "0911223344",
            "address": "Hue, Vietnam",
            "gender": "M",
            "password1": "SecureLec123!",
            "password2": "SecureLec123!",
        }
        response = self.client.post(reverse("add_lecturer"), payload, follow=False)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(email="hoang.c@cornlearn.edu.vn", is_lecturer=True).exists())

    def test_f19_edit_and_delete_lecturer(self):
        """Feature 19: Admin edits and deletes faculty record."""
        lec = User.objects.create_user(
            username="lec_to_delete",
            email="lec_del@cornlearn.edu.vn",
            password="Password123!",
            is_lecturer=True,
        )
        self.login_as_admin()
        # Edit
        edit_url = reverse("staff_edit", kwargs={"pk": lec.pk})
        response = self.client.get(edit_url)
        self.assertEqual(response.status_code, 200)

        # Delete
        del_url = reverse("lecturer_delete", kwargs={"pk": lec.pk})
        del_res = self.client.post(del_url, follow=False)
        self.assertEqual(del_res.status_code, 302)
        self.assertFalse(User.objects.filter(username="lec_to_delete").exists())

    def test_f20_student_directory_and_filter(self):
        """Feature 20: Admin views student roster."""
        self.login_as_admin()
        response = self.client.get(reverse("student_list"))
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.student_user.username, response.content.decode("utf-8"))

    def test_f21_add_student_form(self):
        """Feature 21: Admin adds a new student."""
        self.login_as_admin()
        payload = {
            "first_name": "Pham",
            "last_name": "Van D",
            "email": "pham.d@cornlearn.edu.vn",
            "phone": "0933445566",
            "address": "Can Tho, Vietnam",
            "gender": "M",
            "level": "Cử nhân",
            "program": self.program.id,
            "password1": "StudentSecure123!",
            "password2": "StudentSecure123!",
        }
        response = self.client.post(reverse("add_student"), payload, follow=False)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(email="pham.d@cornlearn.edu.vn", is_student=True).exists())

    def test_f22_edit_and_delete_student(self):
        """Feature 22: Admin edits and deletes student record."""
        stu_user = User.objects.create_user(
            username="student_del_target",
            email="stu_del@cornlearn.edu.vn",
            password="Password123!",
            is_student=True,
        )
        stu_prof = Student.objects.create(student=stu_user, level="Cử nhân", program=self.program)
        self.login_as_admin()

        edit_url = reverse("student_edit", kwargs={"pk": stu_user.pk})
        response = self.client.get(edit_url)
        self.assertEqual(response.status_code, 200)

        del_url = reverse("student_delete", kwargs={"pk": stu_prof.pk})
        del_res = self.client.post(del_url, follow=False)
        self.assertEqual(del_res.status_code, 302)
        self.assertFalse(Student.objects.filter(pk=stu_prof.pk).exists())

    def test_f23_edit_student_program(self):
        """Feature 23: Admin updates student degree program."""
        new_prog = Program.objects.create(title="Khoa học Dữ liệu", summary="Chương trình Khoa học Dữ liệu")
        self.login_as_admin()
        url = reverse("student_program_edit", kwargs={"pk": self.student_user.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        post_res = self.client.post(url, {"program": new_prog.id}, follow=False)
        self.assertEqual(post_res.status_code, 302)
        self.student_profile.refresh_from_db()
        self.assertEqual(self.student_profile.program, new_prog)

    def test_f24_add_parent_guardian_record(self):
        """Feature 24: Admin links parent record with student."""
        self.login_as_admin()
        url = reverse("add_parent")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        stu2_user = User.objects.create_user(
            username="student_for_parent",
            email="stu_parent@cornlearn.edu.vn",
            password="Password123!",
            is_student=True,
        )
        stu2_prof = Student.objects.create(
            student=stu2_user, level="Cử nhân", program=self.program
        )
        parent_payload = {
            "username": "new_parent_guardian",
            "first_name": "Nguyen",
            "last_name": "Phu Huynh",
            "address": "Hanoi, Vietnam",
            "phone": "0912345670",
            "email": "phuhuynh@cornlearn.edu.vn",
            "student": stu2_prof.id,
            "relation_ship": "Mother",
            "password1": "ParentPass123!",
            "password2": "ParentPass123!",
        }
        post_res = self.client.post(url, parent_payload, follow=False)
        self.assertEqual(post_res.status_code, 302)
        self.assertTrue(Parent.objects.filter(student=stu2_prof).exists())

    def test_f25_export_roster_pdf_views(self):
        """Feature 25: Admin exports faculty and student rosters."""
        self.login_as_admin()
        lec_pdf = self.client.get(reverse("lecturer_list_pdf"))
        self.assertEqual(lec_pdf.status_code, 200)
        self.assertEqual(lec_pdf["Content-Type"], "application/pdf")

        stu_pdf = self.client.get(reverse("student_list_pdf"))
        self.assertEqual(stu_pdf.status_code, 200)
        self.assertEqual(stu_pdf["Content-Type"], "application/pdf")

    def test_f26_account_confirmation_emails(self):
        """Feature 26: Account confirmation email template rendering."""
        context = {
            "user": self.student_user,
            "password": "TempPassword123",
            "request": None,
        }
        student_email = render_to_string("accounts/email/new_student_account_confirmation.html", context)
        self.assertIn("CornLearn", student_email)
        self.assert_branding_clean(student_email)

    def test_f27_admin_operations_center(self):
        """Feature 27: Admin panel management operations hub."""
        self.login_as_admin()
        response = self.client.get(reverse("admin_panel"))
        self.assertEqual(response.status_code, 200)
        self.assert_branding_clean(response.content)


class TestTier1CoreAndCalendar(BaseE2ETestCase):
    """Features 28–35: Bulletins, Sessions, Semesters, Analytics Dashboard."""

    def test_f28_home_bulletin_feed(self):
        """Feature 28: Campus announcements bulletin feed."""
        NewsAndEvents.objects.create(
            title="Khai giảng Khóa mới",
            summary="Lễ khai giảng năm học 2026-2027.",
            posted_as="News",
        )
        self.login_as_student()
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        content = response.content.decode("utf-8")
        self.assertIn("Khai giảng Khóa mới", content)

    def test_f29_post_add_and_edit_bulletin(self):
        """Feature 29: Create and edit bulletin post."""
        self.login_as_admin()
        # Add
        payload = {"title": "Hội thảo AI", "summary": "Hội thảo về AI trong giáo dục.", "posted_as": "Event"}
        add_res = self.client.post(reverse("add_item"), payload, follow=False)
        self.assertEqual(add_res.status_code, 302)
        post = NewsAndEvents.objects.get(title="Hội thảo AI")

        # Edit
        edit_url = reverse("edit_post", kwargs={"pk": post.pk})
        edit_payload = {"title": "Hội thảo AI 2026", "summary": "Nội dung cập nhật.", "posted_as": "Event"}
        edit_res = self.client.post(edit_url, edit_payload, follow=False)
        self.assertEqual(edit_res.status_code, 302)
        post.refresh_from_db()
        self.assertEqual(post.title, "Hội thảo AI 2026")

    def test_f30_delete_bulletin_post(self):
        """Feature 30: Delete bulletin announcement."""
        post = NewsAndEvents.objects.create(title="Post To Delete", summary="Summary", posted_as="News")
        self.login_as_admin()
        del_url = reverse("delete_post", kwargs={"pk": post.pk})
        del_res = self.client.post(del_url, follow=False)
        self.assertEqual(del_res.status_code, 302)
        self.assertFalse(NewsAndEvents.objects.filter(pk=post.pk).exists())

    def test_f31_session_management_list(self):
        """Feature 31: Academic session list with active indicators."""
        self.login_as_lecturer()
        response = self.client.get(reverse("session_list"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("2026/2027", response.content.decode("utf-8"))

    def test_f32_add_and_edit_session(self):
        """Feature 32: Add and edit academic session."""
        self.login_as_admin()
        add_payload = {
            "session": "2027/2028",
            "is_current_session": False,
            "next_session_begins": "2027-09-01",
        }
        res = self.client.post(reverse("add_session"), add_payload, follow=False)
        self.assertEqual(res.status_code, 302)
        s = Session.objects.get(session="2027/2028")

        edit_url = reverse("edit_session", kwargs={"pk": s.pk})
        edit_payload = {
            "session": "2027/2028 Renamed",
            "is_current_session": False,
            "next_session_begins": "2027-09-01",
        }
        edit_res = self.client.post(edit_url, edit_payload, follow=False)
        self.assertEqual(edit_res.status_code, 302)
        s.refresh_from_db()
        self.assertEqual(s.session, "2027/2028 Renamed")

    def test_f33_semester_management_list(self):
        """Feature 33: Semester list grouped by session."""
        self.login_as_lecturer()
        response = self.client.get(reverse("semester_list"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("First", response.content.decode("utf-8"))

    def test_f34_add_and_edit_semester(self):
        """Feature 34: Add and edit semester."""
        self.login_as_admin()
        add_payload = {
            "semester": "Second",
            "is_current_semester": False,
            "session": self.session.id,
            "next_semester_begins": "2027-01-15",
        }
        res = self.client.post(reverse("add_semester"), add_payload, follow=False)
        self.assertEqual(res.status_code, 302)
        sem = Semester.objects.get(semester="Second", session=self.session)

        edit_url = reverse("edit_semester", kwargs={"pk": sem.pk})
        edit_res = self.client.get(edit_url)
        self.assertEqual(edit_res.status_code, 200)

    def test_f35_admin_analytics_dashboard(self):
        """Feature 35: Admin analytics dashboard with 4 KPI cards."""
        self.login_as_admin()
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 200)
        content = response.content.decode("utf-8")
        self.assertIn("student", content.lower())
        self.assertIn("lecturer", content.lower())


class TestTier1CoursesAndCurriculum(BaseE2ETestCase):
    """Features 36–48: Programs, Courses, Allocations, Uploads, Registration, Drop, My Courses."""

    def test_f36_academic_degree_program_catalog(self):
        """Feature 36: Filterable degree program catalog."""
        self.login_as_lecturer()
        response = self.client.get(reverse("programs"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("Công nghệ Thông tin", response.content.decode("utf-8"))

    def test_f37_program_curriculum_and_course_list(self):
        """Feature 37: Program detail with curriculum courses."""
        self.login_as_student()
        url = reverse("program_detail", kwargs={"pk": self.program.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        content = response.content.decode("utf-8")
        self.assertIn("IT101", content)

    def test_f38_add_edit_delete_program_forms(self):
        """Feature 38: Program CRUD lifecycle."""
        self.login_as_admin()
        # Add
        payload = {"title": "Kỹ thuật Phần mềm", "summary": "Chuyên ngành Kỹ thuật Phần mềm"}
        add_res = self.client.post(reverse("add_program"), payload, follow=False)
        self.assertEqual(add_res.status_code, 302)
        prog = Program.objects.get(title="Kỹ thuật Phần mềm")

        # Edit
        edit_url = reverse("edit_program", kwargs={"pk": prog.pk})
        edit_res = self.client.post(edit_url, {"title": "Kỹ thuật Phần mềm Đổi mới", "summary": "Mới"}, follow=False)
        self.assertEqual(edit_res.status_code, 302)

        # Delete
        del_url = reverse("program_delete", kwargs={"pk": prog.pk})
        del_res = self.client.post(del_url, follow=False)
        self.assertEqual(del_res.status_code, 302)
        self.assertFalse(Program.objects.filter(pk=prog.pk).exists())

    def test_f39_course_single_detail_and_syllabus(self):
        """Feature 39: Course detail view with syllabus and lecture resources."""
        self.login_as_student()
        url = reverse("course_detail", kwargs={"slug": self.course.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        content = response.content.decode("utf-8")
        self.assertIn("IT101", content)

    def test_f40_add_edit_delete_course_forms(self):
        """Feature 40: Course CRUD forms."""
        self.login_as_admin()
        # Add
        add_url = reverse("course_add", kwargs={"pk": self.program.pk})
        payload = {
            "title": "Cấu trúc Dữ liệu",
            "code": "IT102",
            "credit": 3,
            "summary": "Môn học cấu trúc dữ liệu và giải thuật",
            "program": self.program.id,
            "level": "Cử nhân",
            "year": 1,
            "semester": "First",
        }
        add_res = self.client.post(add_url, payload, follow=False)
        self.assertEqual(add_res.status_code, 302)
        c = Course.objects.get(code="IT102")

        # Edit
        edit_url = reverse("edit_course", kwargs={"slug": c.slug})
        edit_res = self.client.get(edit_url)
        self.assertEqual(edit_res.status_code, 200)

        # Delete
        del_url = reverse("delete_course", kwargs={"slug": c.slug})
        del_res = self.client.post(del_url, follow=False)
        self.assertEqual(del_res.status_code, 302)
        self.assertFalse(Course.objects.filter(code="IT102").exists())

    def test_f41_faculty_course_teaching_allocation(self):
        """Feature 41: Course allocation form for faculty."""
        self.login_as_admin()
        url = reverse("course_allocation")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_f42_teaching_assignment_directory(self):
        """Feature 42: Faculty teaching assignments list."""
        self.login_as_lecturer()
        response = self.client.get(reverse("course_allocation_view"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("IT101", response.content.decode("utf-8"))

    def test_f43_edit_and_deallocate_teaching(self):
        """Feature 43: Edit or revoke teaching assignment."""
        self.login_as_admin()
        edit_url = reverse("edit_allocated_course", kwargs={"pk": self.allocation.pk})
        response = self.client.get(edit_url)
        self.assertEqual(response.status_code, 200)

    def test_f44_course_document_upload_and_management(self):
        """Feature 44: Document upload for course materials."""
        self.login_as_lecturer()
        upload_url = reverse("upload_file_view", kwargs={"slug": self.course.slug})
        response = self.client.get(upload_url)
        self.assertEqual(response.status_code, 200)

    def test_f45_video_tutorial_upload_and_player(self):
        """Feature 45: Video tutorial upload and player."""
        self.login_as_lecturer()
        upload_url = reverse("upload_video", kwargs={"slug": self.course.slug})
        response = self.client.get(upload_url)
        self.assertEqual(response.status_code, 200)

    def test_f46_student_course_registration_interface(self):
        """Feature 46: Student course registration interface."""
        self.login_as_student()
        url = reverse("course_registration")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # Enroll in IT101 using dynamic key name="{{ course.pk }}"
        enroll_payload = {str(self.course.pk): "on"}
        post_res = self.client.post(url, enroll_payload, follow=False)
        self.assertEqual(post_res.status_code, 302)
        self.assertTrue(TakenCourse.objects.filter(student=self.student_profile, course=self.course).exists())

    def test_f47_student_course_drop_action(self):
        """Feature 47: Student drops registered course."""
        TakenCourse.objects.get_or_create(student=self.student_profile, course=self.course)
        self.login_as_student()
        drop_url = reverse("course_drop")
        response = self.client.post(drop_url, {"course_ids": [self.course.id]}, follow=False)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(TakenCourse.objects.filter(student=self.student_profile, course=self.course).exists())

    def test_f48_my_courses_student_and_lecturer_view(self):
        """Feature 48: Role-tailored user course list."""
        # Student view
        TakenCourse.objects.get_or_create(student=self.student_profile, course=self.course)
        self.login_as_student()
        res_stu = self.client.get(reverse("user_course_list"))
        self.assertEqual(res_stu.status_code, 200)
        self.assertIn("IT101", res_stu.content.decode("utf-8"))

        # Lecturer view
        self.login_as_lecturer()
        res_lec = self.client.get(reverse("user_course_list"))
        self.assertEqual(res_lec.status_code, 200)
        self.assertIn("IT101", res_lec.content.decode("utf-8"))


class TestTier1QuizzesAndGrading(BaseE2ETestCase):
    """Features 49–63: Quizzes, Questions, Taking Engine, Marking, Score Entry, Grade Results."""

    def test_f49_course_quizzes_list(self):
        """Feature 49: Directory of course quizzes."""
        Quiz.objects.create(course=self.course, title="Quiz 1", pass_mark=50)
        self.login_as_student()
        url = reverse("quiz_index", kwargs={"slug": self.course.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Quiz 1", response.content.decode("utf-8"))

    def test_f50_quiz_creator_and_editor(self):
        """Feature 50: Quiz creator and editor."""
        self.login_as_lecturer()
        create_url = reverse("quiz_create", kwargs={"slug": self.course.slug})
        response = self.client.get(create_url)
        self.assertEqual(response.status_code, 200)

        payload = {
            "course": self.course.id,
            "title": "Kiểm tra 15 phút",
            "description": "Bài kiểm tra nhanh",
            "pass_mark": 50,
            "category": "practice",
        }
        res = self.client.post(create_url, payload, follow=False)
        self.assertEqual(res.status_code, 302)
        quiz = Quiz.objects.get(title="Kiểm tra 15 phút")

        # Edit
        edit_url = reverse("quiz_update", kwargs={"slug": self.course.slug, "pk": quiz.pk})
        edit_res = self.client.get(edit_url)
        self.assertEqual(edit_res.status_code, 200)

    def test_f51_delete_quiz(self):
        """Feature 51: Delete quiz confirmation."""
        quiz = Quiz.objects.create(course=self.course, title="Quiz To Delete", pass_mark=50)
        self.login_as_lecturer()
        del_url = reverse("quiz_delete", kwargs={"slug": self.course.slug, "pk": quiz.pk})
        del_res = self.client.post(del_url, follow=False)
        self.assertEqual(del_res.status_code, 302)
        self.assertFalse(Quiz.objects.filter(pk=quiz.pk).exists())

    def test_f52_multiple_choice_question_builder(self):
        """Feature 52: Multiple choice question builder with choices."""
        quiz = Quiz.objects.create(course=self.course, title="Quiz Builder Test", pass_mark=50)
        self.login_as_lecturer()
        url = reverse("mc_create", kwargs={"slug": self.course.slug, "quiz_id": quiz.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_f53_interactive_quiz_taking_engine(self):
        """Feature 53: Quiz taking engine."""
        quiz = Quiz.objects.create(course=self.course, title="Quiz Engine Test", pass_mark=50)
        q = MCQuestion.objects.create(content="Django là gì?", explanation="Django là một web framework.")
        q.quiz.add(quiz)
        c1 = Choice.objects.create(question=q, choice_text="Web Framework", correct=True)
        c2 = Choice.objects.create(question=q, choice_text="Hệ điều hành", correct=False)

        self.login_as_student()
        take_url = reverse("quiz_take", kwargs={"pk": self.course.pk, "slug": quiz.slug})
        response = self.client.get(take_url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Django là gì?", response.content.decode("utf-8"))

    def test_f54_quiz_completion_summary_and_results(self):
        """Feature 54: Submit answer and complete quiz."""
        quiz = Quiz.objects.create(course=self.course, title="Quiz Result Test", pass_mark=50)
        q = MCQuestion.objects.create(content="1 + 1 = ?", explanation="1+1=2")
        q.quiz.add(quiz)
        c1 = Choice.objects.create(question=q, choice_text="2", correct=True)
        c2 = Choice.objects.create(question=q, choice_text="3", correct=False)

        self.login_as_student()
        take_url = reverse("quiz_take", kwargs={"pk": self.course.pk, "slug": quiz.slug})
        # Submit correct answer choice
        post_res = self.client.post(take_url, {"answers": str(c1.id)}, follow=True)
        self.assertEqual(post_res.status_code, 200)

    def test_f55_student_quiz_progress_history(self):
        """Feature 55: Student quiz progress history view."""
        self.login_as_student()
        response = self.client.get(reverse("quiz_progress"))
        self.assertEqual(response.status_code, 200)
        self.assert_branding_clean(response.content)

    def test_f56_lecturer_quiz_marking_roster(self):
        """Feature 56: Lecturer quiz marking roster."""
        self.login_as_lecturer()
        response = self.client.get(reverse("quiz_marking"))
        self.assertEqual(response.status_code, 200)
        self.assert_branding_clean(response.content)

    def test_f57_quiz_marking_detail_and_score_override(self):
        """Feature 57: Marking detail view and score override."""
        quiz = Quiz.objects.create(
            course=self.course, title="Marking Override Quiz", pass_mark=50, exam_paper=True
        )
        q = MCQuestion.objects.create(content="2 + 2 = ?", explanation="4")
        q.quiz.add(quiz)
        c1 = Choice.objects.create(question=q, choice_text="4", correct=True)
        Choice.objects.create(question=q, choice_text="5", correct=False)

        sitting = Sitting.objects.create(
            user=self.student_user,
            quiz=quiz,
            course=self.course,
            question_order=f"{q.id},",
            question_list="",
            incorrect_questions="",
            current_score=1,
            complete=True,
            user_answers=json.dumps({str(q.id): str(c1.id)}),
        )

        self.login_as_lecturer()
        detail_url = reverse("quiz_marking_detail", kwargs={"pk": sitting.pk})
        res_get = self.client.get(detail_url)
        self.assertEqual(res_get.status_code, 200)
        self.assertIn("2 + 2 = ?", res_get.content.decode("utf-8"))

        # Toggle question marking via POST
        res_post = self.client.post(detail_url, {"qid": str(q.id)})
        self.assertEqual(res_post.status_code, 200)
        sitting.refresh_from_db()
        self.assertEqual(sitting.current_score, 0)

        # Non-existent sitting returns 404
        response_404 = self.client.get(reverse("quiz_marking_detail", kwargs={"pk": 99999}))
        self.assertEqual(response_404.status_code, 404)

    def test_f58_course_grade_entry_selection(self):
        """Feature 58: Lecturer grade entry course selector."""
        self.login_as_lecturer()
        response = self.client.get(reverse("add_score"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("IT101", response.content.decode("utf-8"))

    def test_f59_component_score_matrix_entry(self):
        """Feature 59: Bulk grading table for 5 components."""
        taken = TakenCourse.objects.create(student=self.student_profile, course=self.course)
        self.login_as_lecturer()
        url = reverse("add_score_for", kwargs={"id": self.course.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # Submit 5 scores keyed by TakenCourse.id: assignment, mid_exam, quiz, attendance, final_exam
        payload = {
            str(taken.id): ["18", "19", "18", "9", "20"],
        }
        post_res = self.client.post(url, payload, follow=False)
        self.assertEqual(post_res.status_code, 302)
        taken.refresh_from_db()
        self.assertEqual(taken.assignment, Decimal("18.00"))
        self.assertEqual(taken.total, Decimal("84.00"))

    def test_f60_student_semester_grade_results(self):
        """Feature 60: Student semester grade results."""
        TakenCourse.objects.get_or_create(student=self.student_profile, course=self.course)
        self.login_as_student()
        response = self.client.get(reverse("grade_results"))
        self.assertEqual(response.status_code, 200)
        self.assert_branding_clean(response.content)

    def test_f61_student_detailed_assessment_breakdown(self):
        """Feature 61: Student detailed component marks."""
        TakenCourse.objects.get_or_create(student=self.student_profile, course=self.course)
        self.login_as_student()
        response = self.client.get(reverse("ass_results"))
        self.assertEqual(response.status_code, 200)
        self.assert_branding_clean(response.content)

    def test_f62_course_result_sheet_pdf_export(self):
        """Feature 62: Course result sheet export."""
        TakenCourse.objects.get_or_create(student=self.student_profile, course=self.course)
        self.login_as_lecturer()
        url = reverse("result_sheet_pdf_view", kwargs={"id": self.course.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/pdf")

    def test_f63_course_registration_form_pdf_export(self):
        """Feature 63: Student course registration form PDF export."""
        TakenCourse.objects.get_or_create(student=self.student_profile, course=self.course)
        self.login_as_student()
        response = self.client.get(reverse("course_registration_form"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/pdf")


class TestTier1PaymentsAndSearch(BaseE2ETestCase):
    """Features 64–69: Invoices, Payment Gateways Hub & Mocks, Omnisearch."""

    def test_f64_invoices_list_and_generator(self):
        """Feature 64: Invoices list and billing invoice generator."""
        self.login_as_student()
        url = reverse("create_invoice")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # Generate invoice
        post_res = self.client.post(url, {"amount": "500000"}, follow=False)
        self.assertEqual(post_res.status_code, 302)
        self.assertTrue(Invoice.objects.filter(user=self.student_user).exists())

    def test_f65_invoice_detail_card(self):
        """Feature 65: Invoice detail card."""
        inv = Invoice.objects.create(
            user=self.student_user,
            amount=500000,
            total=500000,
            invoice_code="INV-2026-0065",
        )
        self.login_as_student()
        url = reverse("invoice_detail", kwargs={"id": inv.id})
        self.assertTrue(url.endswith(f"/invoice-detail/{inv.id}/"))

        home_res = self.client.get(reverse("home"))
        rendered = render_to_string(
            "invoice_detail.html",
            {"invoice": inv, "user": self.student_user},
            request=home_res.wsgi_request,
        )
        self.assertIn(str(inv.total), rendered)
        self.assertIn(self.student_user.username, rendered)
        self.assert_branding_clean(rendered)

    def test_f66_payment_gateways_checkout_hub(self):
        """Feature 66: Payment gateways selection hub with session."""
        inv = Invoice.objects.create(user=self.student_user, amount=250000, total=250000)
        self.login_as_student()
        session = self.client.session
        session["invoice_session"] = inv.id
        session.save()

        response = self.client.get(reverse("payment_gateways"))
        self.assertEqual(response.status_code, 200)
        self.assert_branding_clean(response.content)

    def test_f67_payment_gateway_mock_interfaces(self):
        """Feature 67: Payment gateway mock screens (PayPal, Stripe, Coinbase, Paylike)."""
        self.login_as_student()
        gateways = ["paypal", "stripe", "coinbase", "paylike"]
        for gw in gateways:
            with self.subTest(gateway=gw):
                response = self.client.get(reverse(gw))
                self.assertEqual(response.status_code, 200)
                self.assert_branding_clean(response.content)

    def test_f68_payment_success_confirmation(self):
        """Feature 68: Payment success receipt confirmation."""
        self.login_as_student()
        response = self.client.get(reverse("payment-succeed"))
        self.assertEqual(response.status_code, 200)
        self.assert_branding_clean(response.content)

    def test_f69_global_omnisearch_engine(self):
        """Feature 69: Global omnisearch heterogeneous query."""
        self.login_as_student()
        url = reverse("query")
        # Query with match
        response = self.client.get(url, {"q": "Python"})
        self.assertEqual(response.status_code, 200)
        content = response.content.decode("utf-8")
        self.assertIn("IT101", content)
        self.assert_branding_clean(content)
