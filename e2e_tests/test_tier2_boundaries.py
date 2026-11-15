"""
e2e_tests/test_tier2_boundaries.py
Tier 2 Boundary, Edge & Corner Cases:
- Empty states across all modules (bulletins, courses, quizzes, search, documents)
- Duplicate validations (duplicate usernames, duplicate codes)
- Password mismatch guards in registration and password change
- Academic deletion restrictions (cannot delete active session or active semester)
- Session and semester active flag toggles (activating new session/semester unsets prior)
- Course registration without active semester
- Quiz taking edge conditions (0 questions, single attempt duplicate)
- MCQuestion FormSet validations (<2 choices, 0 correct, >1 correct)
- Score entry validation and missing semester handling
- User profile edge conditions (self-detail redirect, PDF query param)
"""

from decimal import Decimal
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.urls import reverse

from accounts.models import Student
from core.models import NewsAndEvents, Semester, Session
from course.models import Course, Program
from e2e_tests.base import BaseE2ETestCase
from quiz.forms import MCQuestionFormSet
from quiz.models import Choice, MCQuestion, Quiz, Sitting
from result.models import TakenCourse

User = get_user_model()


class TestTier2EmptyStates(BaseE2ETestCase):
    """Verifies that all views render clean, user-friendly empty states when records = 0."""

    def test_empty_bulletin_feed(self):
        """Bulletin feed with 0 announcements renders empty state without exception."""
        NewsAndEvents.objects.all().delete()
        self.login_as_student()
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assert_branding_clean(response.content)

    def test_empty_program_courses(self):
        """Program detail with 0 courses displays empty state."""
        empty_prog = Program.objects.create(title="Chương trình Mới", summary="Chưa có môn học")
        self.login_as_student()
        url = reverse("program_detail", kwargs={"pk": empty_prog.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assert_branding_clean(response.content)

    def test_empty_course_registration_no_courses_enrolled(self):
        """Course registration page indicates no courses are currently enrolled."""
        TakenCourse.objects.filter(student=self.student_profile).delete()
        self.login_as_student()
        url = reverse("course_registration")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context.get("no_course_is_registered", False))

    def test_news_post_long_title_and_unicode_vietnamese(self):
        """NewsAndEvents post with long Vietnamese Unicode title renders cleanly on home feed."""
        vn_title = "Thông báo Học vụ Tiếng Việt: Lịch thi học kỳ I năm học 2026-2027"
        NewsAndEvents.objects.create(
            title=vn_title,
            summary="Chi tiết lịch thi học kỳ I bằng Tiếng Việt có dấu đầy đủ.",
            posted_as="News",
        )
        self.login_as_student()
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        html = response.content.decode("utf-8")
        self.assertIn("Tiếng Việt", html)
        self.assertIn(vn_title, html)

    def test_empty_student_quiz_history(self):
        """Quiz progress history renders clean empty state when student has taken 0 quizzes."""
        Sitting.objects.filter(user=self.student_user).delete()
        self.login_as_student()
        response = self.client.get(reverse("quiz_progress"))
        self.assertEqual(response.status_code, 200)
        self.assert_branding_clean(response.content)

    def test_empty_course_materials_and_videos(self):
        """Course single detail handles 0 uploaded files and 0 uploaded videos gracefully."""
        self.login_as_student()
        url = reverse("course_detail", kwargs={"slug": self.course.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context.get("files", [])), 0)
        self.assertEqual(len(response.context.get("videos", [])), 0)

    def test_empty_search_query_handling(self):
        """Empty search query string (?q=) returns count 0 gracefully without exception."""
        self.login_as_student()
        response = self.client.get(reverse("query"), {"q": ""})
        self.assertEqual(response.status_code, 200)
        content = response.content.decode("utf-8")
        self.assert_branding_clean(content)

    def test_nonexistent_search_query(self):
        """Search query with no matching entities returns clean empty state."""
        self.login_as_student()
        response = self.client.get(reverse("query"), {"q": "XYZNonExistentKeyword9999"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context.get("count", 0), 0)


class TestTier2FormValidationsAndDuplicates(BaseE2ETestCase):
    """Verifies duplicate record prevention and input mismatch handling."""

    def test_registration_duplicate_username_rejected(self):
        """Submitting existing username during registration fails with validation error."""
        payload = {
            "first_name": "Tran",
            "last_name": "Duplicate",
            "username": self.student_user.username,  # Already exists!
            "email": "diff_email@cornlearn.edu.vn",
            "phone": "0912345678",
            "address": "Hanoi",
            "gender": "M",
            "level": "Cử nhân",
            "program": self.program.id,
            "password1": "Password123!",
            "password2": "Password123!",
        }
        response = self.client.post(reverse("register"), payload, follow=False)
        self.assertEqual(response.status_code, 200)  # Re-renders form with errors
        form = response.context.get("form")
        self.assertIsNotNone(form)
        self.assertFalse(form.is_valid())
        self.assertTrue("username" in form.errors)

    def test_registration_password_mismatch_rejected(self):
        """Registration with non-matching passwords fails validation."""
        payload = {
            "first_name": "Le",
            "last_name": "Mismatch",
            "email": "mismatch@cornlearn.edu.vn",
            "phone": "0912345678",
            "address": "Hanoi",
            "gender": "F",
            "level": "Cử nhân",
            "program": self.program.id,
            "password1": "Password123!",
            "password2": "CompletelyDifferentPassword456!",
        }
        response = self.client.post(reverse("register"), payload, follow=False)
        self.assertEqual(response.status_code, 200)
        form = response.context.get("form")
        self.assertFalse(form.is_valid())

    def test_password_change_mismatch_rejected(self):
        """Password change form fails when new passwords do not match."""
        self.login_as_student()
        payload = {
            "old_password": "Password123!",
            "new_password1": "NewSecure123!",
            "new_password2": "DifferentNew123!",
        }
        response = self.client.post(reverse("change_password"), payload, follow=False)
        self.assertEqual(response.status_code, 200)
        form = response.context.get("form")
        self.assertFalse(form.is_valid())


class TestTier2AcademicCalendarBoundaries(BaseE2ETestCase):
    """Verifies academic calendar business rules and guardrails."""

    def test_delete_current_active_session_blocked(self):
        """Attempt to delete the current active session is blocked with error message."""
        self.login_as_admin()
        del_url = reverse("delete_session", kwargs={"pk": self.session.pk})
        response = self.client.post(del_url, follow=True)
        self.assertEqual(response.status_code, 200)
        # Session must STILL exist in database
        self.assertTrue(Session.objects.filter(pk=self.session.pk).exists())
        messages = list(response.context.get("messages", []))
        self.assertTrue(
            any("cannot delete the current session" in str(m).lower() for m in messages),
            "Expected error toast when deleting current session",
        )

    def test_delete_current_active_semester_blocked(self):
        """Attempt to delete the current active semester is blocked with error message."""
        self.login_as_admin()
        del_url = reverse("delete_semester", kwargs={"pk": self.semester.pk})
        response = self.client.post(del_url, follow=True)
        self.assertEqual(response.status_code, 200)
        # Semester must STILL exist in database
        self.assertTrue(Semester.objects.filter(pk=self.semester.pk).exists())
        messages = list(response.context.get("messages", []))
        self.assertTrue(
            any("cannot delete the current semester" in str(m).lower() for m in messages),
            "Expected error toast when deleting current semester",
        )

    def test_activating_new_session_unsets_previous(self):
        """Adding a new session marked as current unsets the previous current session."""
        self.login_as_admin()
        new_session_payload = {
            "session": "2028/2029",
            "is_current_session": True,
            "next_session_begins": "2028-09-01",
        }
        res = self.client.post(reverse("add_session"), new_session_payload, follow=False)
        self.assertEqual(res.status_code, 302)

        self.session.refresh_from_db()
        self.assertFalse(self.session.is_current_session)

        new_sess = Session.objects.get(session="2028/2029")
        self.assertTrue(new_sess.is_current_session)

    def test_course_registration_without_active_semester(self):
        """Visiting course registration when no semester is active sets error alert."""
        # Deactivate all semesters
        Semester.objects.all().update(is_current_semester=False)
        self.login_as_student()
        response = self.client.get(reverse("course_registration"))
        self.assertEqual(response.status_code, 200)
        messages = list(response.context.get("messages", []))
        self.assertTrue(
            any("no active semester" in str(m).lower() for m in messages),
        )


class TestTier2QuizAndGradingBoundaries(BaseE2ETestCase):
    """Verifies quiz taking rules and grading input boundaries."""

    def test_grade_boundary_thresholds(self):
        """Verifies TakenCourse grade boundary thresholds across A+ through F."""
        valid_grades = ("A+", "A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D", "F", "NG")
        boundary_cases = [
            (Decimal("20"), Decimal("20"), Decimal("20"), Decimal("10"), Decimal("20"), "A+"),  # 90
            (Decimal("18"), Decimal("18"), Decimal("19"), Decimal("10"), Decimal("20"), "A"),   # 85
            (Decimal("15"), Decimal("15"), Decimal("15"), Decimal("10"), Decimal("20"), "B+"),  # 75
            (Decimal("10"), Decimal("10"), Decimal("10"), Decimal("10"), Decimal("10"), "C-"),  # 50
            (Decimal("10"), Decimal("10"), Decimal("10"), Decimal("5"), Decimal("10"), "D"),    # 45
            (Decimal("5"), Decimal("5"), Decimal("5"), Decimal("5"), Decimal("10"), "F"),       # 30
        ]
        for a, m, q, att, fin, expected_grade in boundary_cases:
            tc, _ = TakenCourse.objects.update_or_create(
                student=self.student_profile,
                course=self.course,
                defaults={
                    "assignment": a,
                    "mid_exam": m,
                    "quiz": q,
                    "attendance": att,
                    "final_exam": fin,
                },
            )
            tc.refresh_from_db()
            self.assertIn(tc.grade, valid_grades)
            self.assertEqual(tc.grade, expected_grade)

    def test_quiz_with_zero_questions_redirects_with_warning(self):
        """Attempting to take a quiz with 0 questions redirects with a warning toast."""
        empty_quiz = Quiz.objects.create(
            course=self.course,
            title="Empty Quiz Test",
            pass_mark=50,
        )
        self.login_as_student()
        url = reverse("quiz_take", kwargs={"pk": self.course.pk, "slug": empty_quiz.slug})
        response = self.client.get(url, follow=False)
        self.assertEqual(response.status_code, 302)

    def test_single_attempt_quiz_already_completed_blocked(self):
        """Attempting to take a single-attempt quiz that is already completed is blocked."""
        quiz = Quiz.objects.create(
            course=self.course,
            title="Single Attempt Exam",
            pass_mark=50,
            single_attempt=True,
        )
        q = MCQuestion.objects.create(content="Q1?", explanation="Exp")
        q.quiz.add(quiz)
        Choice.objects.create(question=q, choice_text="Opt 1", correct=True)
        Choice.objects.create(question=q, choice_text="Opt 2", correct=False)

        # Record a completed sitting
        Sitting.objects.create(
            user=self.student_user,
            quiz=quiz,
            course=self.course,
            question_order=str(q.id),
            question_list=str(q.id),
            incorrect_questions="",
            current_score=1,
            complete=True,
            user_answers="{}",
        )

        self.login_as_student()
        url = reverse("quiz_take", kwargs={"pk": self.course.pk, "slug": quiz.slug})
        response = self.client.get(url, follow=False)
        # Should redirect away with info message
        self.assertEqual(response.status_code, 302)

    def test_mcquestion_formset_validation_rules(self):
        """Validates that MCQuestion choices must have >=2 choices and strictly 1 correct choice."""
        q = MCQuestion.objects.create(content="Test Question?")

        # Case A: Fewer than 2 choices
        data_less_than_2 = {
            "choice_set-TOTAL_FORMS": "1",
            "choice_set-INITIAL_FORMS": "0",
            "choice_set-0-choice_text": "Only one choice",
            "choice_set-0-correct": "True",
        }
        formset_a = MCQuestionFormSet(data=data_less_than_2, instance=q)
        self.assertFalse(formset_a.is_valid())

        # Case B: 0 choices marked correct
        data_zero_correct = {
            "choice_set-TOTAL_FORMS": "2",
            "choice_set-INITIAL_FORMS": "0",
            "choice_set-0-choice_text": "Choice 1",
            "choice_set-0-correct": "False",
            "choice_set-1-choice_text": "Choice 2",
            "choice_set-1-correct": "False",
        }
        formset_b = MCQuestionFormSet(data=data_zero_correct, instance=q)
        self.assertFalse(formset_b.is_valid())

        # Case C: More than 1 choice marked correct
        data_multi_correct = {
            "choice_set-TOTAL_FORMS": "2",
            "choice_set-INITIAL_FORMS": "0",
            "choice_set-0-choice_text": "Choice 1",
            "choice_set-0-correct": "True",
            "choice_set-1-choice_text": "Choice 2",
            "choice_set-1-correct": "True",
        }
        formset_c = MCQuestionFormSet(data=data_multi_correct, instance=q)
        self.assertFalse(formset_c.is_valid())


class TestTier2ProfileEdgeCases(BaseE2ETestCase):
    """Verifies profile single intercept and export options."""

    def test_view_own_detail_profile_redirects_to_personal_profile(self):
        """Admin viewing own profile via /accounts/profile/<id>/detail/ is redirected to /accounts/profile/."""
        self.login_as_admin()
        url = reverse("profile_single", kwargs={"user_id": self.admin_user.id})
        response = self.client.get(url, follow=False)
        self.assertEqual(response.status_code, 302)
        location = response.headers.get("Location", "")
        self.assertTrue("/accounts/profile" in location)

    def test_profile_single_pdf_download_param(self):
        """Appending ?download_pdf=1 to /accounts/profile/<id>/detail/ triggers PDF rendering."""
        self.login_as_admin()
        url = reverse("profile_single", kwargs={"user_id": self.student_user.id}) + "?download_pdf=1"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/pdf")
