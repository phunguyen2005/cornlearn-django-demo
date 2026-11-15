"""
e2e_tests/test_tier3_pairwise.py
Tier 3 Cross-Module Interactions, Pairwise Role Boundaries & Multi-Step Workflows:
- RBAC Role Access Matrix (Anonymous vs Student vs Lecturer vs Admin across protected routes)
- Workflow 1: Academic Governance (Session -> Semester -> Program -> Course)
- Workflow 2: Faculty Allocation & Content Publishing (Allocation -> Syllabus -> File Upload)
- Workflow 3: Student Enrollment & Registration (Program -> Course Registration -> TakenCourse -> My Courses)
- Workflow 4: Examination & Assessment Flow (Quiz -> Questions -> Taking Engine -> Sitting -> Marking Roster)
- Workflow 5: Grading, GPA Calculation & Report Generation (Component Grading -> GPA -> Result Records -> PDF Export)
"""

from decimal import Decimal
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from accounts.models import Student
from core.models import Semester, Session
from course.models import Course, CourseAllocation, Program, Upload
from e2e_tests.base import BaseE2ETestCase
from quiz.models import Choice, MCQuestion, Quiz, Sitting
from result.models import Result, TakenCourse

User = get_user_model()


class TestTier3RoleAccessBoundaries(BaseE2ETestCase):
    """Pairwise validation of role permissions across distinct application endpoints."""

    def test_anonymous_user_redirected_to_login(self):
        """Anonymous user attempting to access protected endpoints is redirected to login."""
        self.login_as_anonymous()
        protected_urls = [
            reverse("home"),
            reverse("profile"),
            reverse("course_registration"),
            reverse("session_list"),
            reverse("dashboard"),
            reverse("admin_panel"),
        ]
        for url in protected_urls:
            with self.subTest(url=url):
                response = self.client.get(url, follow=False)
                self.assert_redirects_to_login(response)

    def test_student_restricted_from_admin_and_faculty_routes(self):
        """Student is blocked from accessing administrative and faculty-only routes."""
        self.login_as_student()
        # Both @admin_required and @lecturer_required in accounts/decorators.py
        # redirect unauthorized users to redirect_to="/" (home).
        admin_restricted_urls = [
            reverse("admin_panel"),
            reverse("dashboard"),
            reverse("lecturer_list"),
            reverse("student_list"),
            reverse("add_lecturer"),
            reverse("add_student"),
        ]
        faculty_restricted_urls = [
            reverse("session_list"),
            reverse("semester_list"),
            reverse("add_session"),
            reverse("add_semester"),
            reverse("add_program"),
            reverse("programs"),
            reverse("course_allocation"),
            reverse("add_score"),
            reverse("quiz_marking"),
        ]
        for url in admin_restricted_urls + faculty_restricted_urls:
            with self.subTest(url=url):
                response = self.client.get(url, follow=False)
                self.assert_redirects_to_home(response)

        # Conversely, student IS permitted to view program_detail and course_detail (HTTP 200)
        prog_detail_res = self.client.get(reverse("program_detail", kwargs={"pk": self.program.pk}))
        self.assertEqual(prog_detail_res.status_code, 200)
        course_detail_res = self.client.get(reverse("course_detail", kwargs={"slug": self.course.slug}))
        self.assertEqual(course_detail_res.status_code, 200)

    def test_lecturer_restricted_from_admin_and_student_only_routes(self):
        """Lecturer cannot access admin-only panel or student-specific course registration."""
        self.login_as_lecturer()
        # Admin-only routes
        admin_urls = [
            reverse("admin_panel"),
            reverse("dashboard"),
            reverse("lecturer_list"),
            reverse("student_list"),
        ]
        for url in admin_urls:
            with self.subTest(url=url):
                response = self.client.get(url, follow=False)
                self.assert_redirects_to_home(response)

        # Student-only route: course_registration
        reg_res = self.client.get(reverse("course_registration"), follow=False)
        self.assert_redirects_to_home(reg_res)

    def test_admin_elevated_access(self):
        """Admin has full access to academic operations, dashboard, and management hubs."""
        self.login_as_admin()
        accessible_urls = [
            reverse("admin_panel"),
            reverse("dashboard"),
            reverse("lecturer_list"),
            reverse("student_list"),
            reverse("session_list"),
            reverse("semester_list"),
            reverse("programs"),
            reverse("course_allocation"),
            reverse("add_score"),
            reverse("quiz_marking"),
        ]
        for url in accessible_urls:
            with self.subTest(url=url):
                response = self.client.get(url, follow=False)
                self.assertEqual(response.status_code, 200)


class TestTier3MultiStepWorkflows(BaseE2ETestCase):
    """End-to-end multi-step state transitions and cross-module interactions."""

    def test_workflow_1_academic_governance_lifecycle(self):
        """
        Flow 1: Admin creates Session -> Semester -> Program -> Course -> verifies curriculum.
        """
        self.login_as_admin()

        # Step 1: Create new session
        sess_payload = {"session": "2030/2031", "is_current_session": False, "next_session_begins": "2030-09-01"}
        r1 = self.client.post(reverse("add_session"), sess_payload, follow=False)
        self.assertEqual(r1.status_code, 302)
        new_sess = Session.objects.get(session="2030/2031")

        # Step 2: Create new semester
        sem_payload = {"semester": "First", "is_current_semester": False, "session": new_sess.id, "next_semester_begins": "2030-09-01"}
        r2 = self.client.post(reverse("add_semester"), sem_payload, follow=False)
        self.assertEqual(r2.status_code, 302)
        new_sem = Semester.objects.get(session=new_sess, semester="First")

        # Step 3: Create academic program
        prog_payload = {"title": "Trí tuệ Nhân tạo", "summary": "Chuyên ngành AI"}
        r3 = self.client.post(reverse("add_program"), prog_payload, follow=False)
        self.assertEqual(r3.status_code, 302)
        new_prog = Program.objects.get(title="Trí tuệ Nhân tạo")

        # Step 4: Add course unit to program
        course_payload = {
            "title": "Nhập môn AI",
            "code": "AI101",
            "credit": 3,
            "summary": "Kiến thức cơ bản về AI",
            "program": new_prog.id,
            "level": "Cử nhân",
            "year": 1,
            "semester": "First",
        }
        r4 = self.client.post(reverse("course_add", kwargs={"pk": new_prog.pk}), course_payload, follow=False)
        self.assertEqual(r4.status_code, 302)
        ai_course = Course.objects.get(code="AI101")
        self.assertEqual(ai_course.program, new_prog)

        # Step 5: Verify curriculum list displays newly created course
        detail_res = self.client.get(reverse("program_detail", kwargs={"pk": new_prog.pk}))
        self.assertEqual(detail_res.status_code, 200)
        self.assertIn("AI101", detail_res.content.decode("utf-8"))

    def test_workflow_2_course_allocation_and_syllabus_setup(self):
        """
        Flow 2: Admin allocates course -> Lecturer sees allocation -> Uploads syllabus note.
        """
        # Step 1: Allocate course to lecturer
        self.login_as_admin()
        alloc_payload = {
            "lecturer": self.lecturer_user.id,
            "courses": [self.course.id, self.course_elective.id],
        }
        r1 = self.client.post(reverse("course_allocation"), alloc_payload, follow=False)
        self.assertEqual(r1.status_code, 302)

        # Step 2: Lecturer logs in and checks allocated courses
        self.login_as_lecturer()
        r2 = self.client.get(reverse("course_allocation_view"))
        self.assertEqual(r2.status_code, 200)
        content2 = r2.content.decode("utf-8")
        self.assertIn("IT101", content2)
        self.assertIn("IT201", content2)

        # Step 3: Lecturer uploads lecture note
        sample_file = SimpleUploadedFile("syllabus.pdf", b"%PDF-1.4 test syllabus", content_type="application/pdf")
        upload_payload = {"title": "Đề cương Môn học", "file": sample_file}
        upload_url = reverse("upload_file_view", kwargs={"slug": self.course.slug})
        r3 = self.client.post(upload_url, upload_payload, follow=False)
        self.assertEqual(r3.status_code, 302)

        # Step 4: Verify syllabus file appears on course detail
        r4 = self.client.get(reverse("course_detail", kwargs={"slug": self.course.slug}))
        self.assertEqual(r4.status_code, 200)
        self.assertIn("Đề cương Môn học", r4.content.decode("utf-8"))

    def test_workflow_3_student_enrollment_and_registration(self):
        """
        Flow 3: Student registers for course -> TakenCourse created -> Enrolled course in my_courses.
        """
        self.login_as_student()

        # Step 1: Visit registration page
        reg_url = reverse("course_registration")
        r1 = self.client.get(reg_url)
        self.assertEqual(r1.status_code, 200)

        # Step 2: Submit course enrollment checkbox
        r2 = self.client.post(reg_url, {str(self.course.pk): "on"}, follow=False)
        self.assertEqual(r2.status_code, 302)

        # Step 3: Verify TakenCourse record
        self.assertTrue(TakenCourse.objects.filter(student=self.student_profile, course=self.course).exists())

        # Step 4: View user_course_list (My Courses)
        r4 = self.client.get(reverse("user_course_list"))
        self.assertEqual(r4.status_code, 200)
        self.assertIn("IT101", r4.content.decode("utf-8"))

    def test_workflow_4_quiz_taking_and_marking_lifecycle(self):
        """
        Flow 4: Lecturer creates Quiz & Questions -> Student takes quiz -> Lecturer reviews sitting.
        """
        # Step 1: Lecturer creates quiz
        self.login_as_lecturer()
        create_url = reverse("quiz_create", kwargs={"slug": self.course.slug})
        quiz_payload = {
            "course": self.course.id,
            "title": "Kiểm tra Giữa kỳ",
            "description": "Bài kiểm tra giữa kỳ 45 phút",
            "pass_mark": 60,
            "category": "exam",
            "exam_paper": True,
        }
        r1 = self.client.post(create_url, quiz_payload, follow=False)
        self.assertEqual(r1.status_code, 302)
        quiz = Quiz.objects.get(title="Kiểm tra Giữa kỳ")

        # Step 2: Lecturer adds question with choices
        q = MCQuestion.objects.create(content="HTML viết tắt của từ gì?", explanation="HyperText Markup Language")
        q.quiz.add(quiz)
        c_correct = Choice.objects.create(question=q, choice_text="HyperText Markup Language", correct=True)
        Choice.objects.create(question=q, choice_text="High Tech Modern Language", correct=False)

        # Step 3: Student takes quiz
        self.login_as_student()
        take_url = reverse("quiz_take", kwargs={"pk": self.course.pk, "slug": quiz.slug})
        r3 = self.client.get(take_url)
        self.assertEqual(r3.status_code, 200)

        # Submit answer
        r4 = self.client.post(take_url, {"answers": str(c_correct.id)}, follow=True)
        self.assertEqual(r4.status_code, 200)

        # Step 4: Lecturer checks marking roster
        self.login_as_lecturer()
        r5 = self.client.get(reverse("quiz_marking"))
        self.assertEqual(r5.status_code, 200)
        self.assertIn("Kiểm tra Giữa kỳ", r5.content.decode("utf-8"))

    def test_workflow_5_grade_entry_gpa_calculation_and_pdf_export(self):
        """
        Flow 5: Student enrolled -> Lecturer enters 5 components -> Total & GPA calculated -> Student views grades -> PDF.
        """
        # Step 1: Setup TakenCourse enrollment
        taken = TakenCourse.objects.create(student=self.student_profile, course=self.course)

        # Step 2: Lecturer submits 5 component marks keyed by TakenCourse.id
        self.login_as_lecturer()
        grade_url = reverse("add_score_for", kwargs={"id": self.course.id})
        grade_payload = {
            str(taken.id): ["18", "19", "18", "10", "20"],
        }
        r1 = self.client.post(grade_url, grade_payload, follow=False)
        self.assertEqual(r1.status_code, 302)

        # Step 3: Verify TakenCourse computed total and Result GPA
        taken.refresh_from_db()
        self.assertEqual(taken.total, Decimal("85.00"))
        self.assertEqual(taken.grade, "A")
        self.assertEqual(taken.comment, "PASS")

        # Step 4: Student views semester grade results
        self.login_as_student()
        r2 = self.client.get(reverse("grade_results"))
        self.assertEqual(r2.status_code, 200)
        content2 = r2.content.decode("utf-8")
        self.assertIn("IT101", content2)
        self.assertIn("PASS", content2)

        # Step 5: Student views assessment breakdown
        r3 = self.client.get(reverse("ass_results"))
        self.assertEqual(r3.status_code, 200)
        self.assertIn("18.00", r3.content.decode("utf-8"))

        # Step 6: Lecturer exports official result sheet PDF
        self.login_as_lecturer()
        pdf_res = self.client.get(reverse("result_sheet_pdf_view", kwargs={"id": self.course.id}))
        self.assertEqual(pdf_res.status_code, 200)
        self.assertEqual(pdf_res["Content-Type"], "application/pdf")
