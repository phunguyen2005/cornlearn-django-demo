"""
e2e_tests/test_tier4_journeys.py
Tier 4 Real-World End-to-End User Journeys:
- S1 (Student Full Journey): Public Registration -> Login -> Profile -> Browse Curriculum -> Register Courses -> View My Courses -> Take Quiz -> Review Results -> Inspect Grade & Assessment Breakdown -> Export Registration Form PDF.
- S2 (Faculty Full Journey): Login -> Profile -> View Teaching Allocations -> Upload Lecture Notes -> Create Quiz & MC Questions -> Inspect Student Submissions -> Select Course for Grading -> Bulk 5-Component Mark Entry -> Export Official Result Sheet PDF.
- S3 (Admin Full Governance Journey): Login -> Operations Center -> Add Faculty & Student -> Academic Calendar Setup -> Create Program & Course -> Allocate Teaching Assignment -> Post Campus Announcement -> Inspect KPI Dashboard -> Global Omnisearch.
"""

from decimal import Decimal
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from accounts.models import Student
from core.models import NewsAndEvents, Semester, Session
from course.models import Course, CourseAllocation, Program, Upload
from e2e_tests.base import BaseE2ETestCase
from quiz.models import Choice, MCQuestion, Quiz, Sitting
from result.models import Result, TakenCourse

User = get_user_model()


class TestTier4StudentJourney(BaseE2ETestCase):
    """S1: Real-world journey of a student from enrollment to assessment."""

    def test_s1_student_complete_journey(self):
        # 1. Public self-registration
        reg_payload = {
            "first_name": "Linh",
            "last_name": "Nguyen",
            "username": "linh_nguyen_s1",
            "email": "linh.nguyen@cornlearn.edu.vn",
            "phone": "0911223344",
            "address": "TP Ho Chi Minh",
            "gender": "F",
            "level": "Bachelor",
            "program": self.program.id,
            "password1": "LinhSecure123!",
            "password2": "LinhSecure123!",
        }
        res_reg = self.client.post(reverse("register"), reg_payload, follow=False)
        self.assertEqual(res_reg.status_code, 302)
        student_user = User.objects.get(email="linh.nguyen@cornlearn.edu.vn")
        student_user.set_password("LinhSecure123!")
        student_user.save()
        student_profile = Student.objects.get(student=student_user)

        # 2. Login
        login_res = self.client.post(
            reverse("login"),
            {"username": student_user.username, "password": "LinhSecure123!"},
            follow=False,
        )
        self.assertEqual(login_res.status_code, 302)

        # 3. View personal profile
        profile_res = self.client.get(reverse("profile"))
        self.assertEqual(profile_res.status_code, 200)
        self.assertIn("Linh Nguyen", profile_res.content.decode("utf-8"))

        # 4. Browse curriculum
        prog_res = self.client.get(reverse("program_detail", kwargs={"pk": self.program.pk}))
        self.assertEqual(prog_res.status_code, 200)
        self.assertIn("IT101", prog_res.content.decode("utf-8"))

        # 5. View course syllabus
        course_res = self.client.get(reverse("course_detail", kwargs={"slug": self.course.slug}))
        self.assertEqual(course_res.status_code, 200)

        # 6. Register for courses
        reg_res = self.client.post(reverse("course_registration"), {str(self.course.pk): "on"}, follow=False)
        self.assertEqual(reg_res.status_code, 302)
        self.assertTrue(TakenCourse.objects.filter(student=student_profile, course=self.course).exists())

        # 7. View enrolled courses in My Courses
        my_courses = self.client.get(reverse("user_course_list"))
        self.assertEqual(my_courses.status_code, 200)
        self.assertIn("IT101", my_courses.content.decode("utf-8"))

        # 8. Take course quiz
        quiz = Quiz.objects.create(course=self.course, title="S1 Final Quiz", pass_mark=50)
        q = MCQuestion.objects.create(content="HTML là ngôn ngữ gì?", explanation="Đánh dấu siêu văn bản")
        q.quiz.add(quiz)
        c_right = Choice.objects.create(question=q, choice_text="Ngôn ngữ đánh dấu", correct=True)
        Choice.objects.create(question=q, choice_text="Ngôn ngữ máy", correct=False)

        take_url = reverse("quiz_take", kwargs={"pk": self.course.pk, "slug": quiz.slug})
        get_quiz = self.client.get(take_url)
        self.assertEqual(get_quiz.status_code, 200)
        self.assertIn("HTML là ngôn ngữ gì?", get_quiz.content.decode("utf-8"))

        # Submit quiz answers
        post_quiz = self.client.post(take_url, {"answers": str(c_right.id)}, follow=True)
        self.assertEqual(post_quiz.status_code, 200)

        # 9. View personal quiz progress history
        prog_history = self.client.get(reverse("quiz_progress"))
        self.assertEqual(prog_history.status_code, 200)
        self.assert_branding_clean(prog_history.content)

        # 10. View semester grade results
        grades = self.client.get(reverse("grade_results"))
        self.assertEqual(grades.status_code, 200)
        self.assertIn("IT101", grades.content.decode("utf-8"))

        # 11. View assessment breakdown
        assess = self.client.get(reverse("ass_results"))
        self.assertEqual(assess.status_code, 200)
        self.assertIn("IT101", assess.content.decode("utf-8"))

        # 12. Export course registration form PDF
        pdf_res = self.client.get(reverse("course_registration_form"))
        self.assertEqual(pdf_res.status_code, 200)
        self.assertEqual(pdf_res["Content-Type"], "application/pdf")


class TestTier4FacultyJourney(BaseE2ETestCase):
    """S2: Real-world journey of a faculty instructor managing content and grading."""

    def test_s2_faculty_complete_journey(self):
        # 1. Login
        login_res = self.client.post(
            reverse("login"),
            {"username": self.lecturer_user.username, "password": "Password123!"},
            follow=False,
        )
        self.assertEqual(login_res.status_code, 302)

        # 2. View faculty profile
        prof_res = self.client.get(reverse("profile"))
        self.assertEqual(prof_res.status_code, 200)
        self.assertIn("Nguyen Van A", prof_res.content.decode("utf-8"))

        # 3. Check allocated teaching assignments
        alloc_res = self.client.get(reverse("course_allocation_view"))
        self.assertEqual(alloc_res.status_code, 200)
        self.assertIn("IT101", alloc_res.content.decode("utf-8"))

        # 4. Upload lecture PDF
        sample_doc = SimpleUploadedFile("lecture1.pdf", b"%PDF-1.4 sample lecture content", content_type="application/pdf")
        upload_url = reverse("upload_file_view", kwargs={"slug": self.course.slug})
        upload_res = self.client.post(upload_url, {"title": "Bài giảng Chương 1", "file": sample_doc}, follow=False)
        self.assertEqual(upload_res.status_code, 302)

        # 5. Create quiz
        create_quiz_url = reverse("quiz_create", kwargs={"slug": self.course.slug})
        quiz_payload = {
            "course": self.course.id,
            "title": "Kiểm tra Đọc hiểu Chương 1",
            "description": "Đọc hiểu tài liệu bài giảng",
            "pass_mark": 50,
            "category": "practice",
        }
        res_quiz = self.client.post(create_quiz_url, quiz_payload, follow=False)
        self.assertEqual(res_quiz.status_code, 302)
        new_quiz = Quiz.objects.get(title="Kiểm tra Đọc hiểu Chương 1")

        # 6. Add multiple choice question
        q = MCQuestion.objects.create(content="Khái niệm MVC là gì?", explanation="Model-View-Controller")
        q.quiz.add(new_quiz)
        Choice.objects.create(question=q, choice_text="Model-View-Controller", correct=True)
        Choice.objects.create(question=q, choice_text="Machine-Voice-Core", correct=False)

        # 7. Check marking roster
        mark_roster = self.client.get(reverse("quiz_marking"))
        self.assertEqual(mark_roster.status_code, 200)

        # 8. Select course for grade entry
        select_res = self.client.get(reverse("add_score"))
        self.assertEqual(select_res.status_code, 200)
        self.assertIn("IT101", select_res.content.decode("utf-8"))

        # 9. Enter component grades for enrolled student (keyed by TakenCourse.id)
        taken, _ = TakenCourse.objects.get_or_create(student=self.student_profile, course=self.course)
        grade_url = reverse("add_score_for", kwargs={"id": self.course.id})
        grade_payload = {
            str(taken.id): ["17", "18", "19", "9", "18"],
        }
        post_grade = self.client.post(grade_url, grade_payload, follow=False)
        self.assertEqual(post_grade.status_code, 302)
        taken.refresh_from_db()
        self.assertEqual(taken.total, Decimal("81.00"))
        self.assertEqual(taken.grade, "A-")

        # 10. Generate official Result Sheet PDF
        pdf_res = self.client.get(reverse("result_sheet_pdf_view", kwargs={"id": self.course.id}))
        self.assertEqual(pdf_res.status_code, 200)
        self.assertEqual(pdf_res["Content-Type"], "application/pdf")


class TestTier4AdminJourney(BaseE2ETestCase):
    """S3: Real-world governance journey of an institutional administrator."""

    def test_s3_admin_complete_governance_journey(self):
        # 1. Login
        login_res = self.client.post(
            reverse("login"),
            {"username": "admin_user", "password": "Password123!"},
            follow=False,
        )
        self.assertEqual(login_res.status_code, 302)

        # 2. Open Admin Operations Center
        panel_res = self.client.get(reverse("admin_panel"))
        self.assertEqual(panel_res.status_code, 200)

        # 3. Add new faculty member
        lec_payload = {
            "first_name": "Tran",
            "last_name": "Van Giao",
            "email": "giao.tran@cornlearn.edu.vn",
            "phone": "0988776655",
            "address": "Da Nang",
            "gender": "M",
            "password1": "GiaoPass123!",
            "password2": "GiaoPass123!",
        }
        r_lec = self.client.post(reverse("add_lecturer"), lec_payload, follow=False)
        self.assertEqual(r_lec.status_code, 302)
        new_faculty = User.objects.get(email="giao.tran@cornlearn.edu.vn", is_lecturer=True)

        # 4. Add new student member
        stu_payload = {
            "first_name": "Ngo",
            "last_name": "Bao Chau",
            "email": "chau.ngo@cornlearn.edu.vn",
            "phone": "0977665544",
            "address": "Hanoi",
            "gender": "M",
            "level": "Bachelor",
            "program": self.program.id,
            "password1": "ChauPass123!",
            "password2": "ChauPass123!",
        }
        r_stu = self.client.post(reverse("add_student"), stu_payload, follow=False)
        self.assertEqual(r_stu.status_code, 302)

        # 5. Manage academic calendar: create session & semester
        s_res = self.client.post(
            reverse("add_session"),
            {"session": "2029/2030", "is_current_session": False, "next_session_begins": "2029-09-01"},
            follow=False,
        )
        self.assertEqual(s_res.status_code, 302)
        sess = Session.objects.get(session="2029/2030")

        sem_res = self.client.post(
            reverse("add_semester"),
            {"semester": "First", "is_current_semester": False, "session": sess.id, "next_semester_begins": "2029-09-01"},
            follow=False,
        )
        self.assertEqual(sem_res.status_code, 302)

        # 6. Create program and course
        p_res = self.client.post(
            reverse("add_program"),
            {"title": "An toàn Thông tin", "summary": "Chương trình đào tạo Kỹ sư An toàn Thông tin"},
            follow=False,
        )
        self.assertEqual(p_res.status_code, 302)
        prog_sec = Program.objects.get(title="An toàn Thông tin")

        c_res = self.client.post(
            reverse("course_add", kwargs={"pk": prog_sec.pk}),
            {
                "title": "Mật mã học",
                "code": "SEC101",
                "credit": 3,
                "summary": "Môn học nền tảng mật mã và bảo mật",
                "program": prog_sec.id,
                "level": "Bachelor",
                "year": 1,
                "semester": "First",
            },
            follow=False,
        )
        self.assertEqual(c_res.status_code, 302)
        sec_course = Course.objects.get(code="SEC101")

        # 7. Allocate course to newly added faculty
        alloc_res = self.client.post(
            reverse("course_allocation"),
            {"lecturer": new_faculty.id, "courses": [sec_course.id]},
            follow=False,
        )
        self.assertEqual(alloc_res.status_code, 302)

        # 8. Post campus news bulletin
        post_res = self.client.post(
            reverse("add_item"),
            {
                "title": "Thông báo Khai mạc Tuần sinh hoạt Công dân",
                "summary": "Tuần sinh hoạt công dân đầu khóa dành cho tân sinh viên.",
                "posted_as": "News",
            },
            follow=False,
        )
        self.assertEqual(post_res.status_code, 302)

        # 9. Inspect analytics dashboard KPI metrics
        dash_res = self.client.get(reverse("dashboard"))
        self.assertEqual(dash_res.status_code, 200)
        self.assertIn("dashboard", dash_res.content.decode("utf-8").lower())

        # 10. Execute global omnisearch across all models
        search_res = self.client.get(reverse("query"), {"q": "Thông tin"})
        self.assertEqual(search_res.status_code, 200)
        self.assertIn("An toàn Thông tin", search_res.content.decode("utf-8"))
