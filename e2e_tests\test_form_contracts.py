"""
e2e_tests/test_form_contracts.py
Verifies critical form contracts, input names, HTTP methods, and CSRF protection:
- Course registration checkbox name="{{ course.pk }}"
- Course drop checkbox name="course_ids" and value="{{ course.id }}"
- Grade entry 5 inputs per student name="{{ student.id }}" (assignment, mid_exam, quiz, attendance, final_exam)
- MCQuestion inline formset choice_set management form and choice fields
- Omnisearch filter {% load class_name %}
- CSRF token verification across all POST forms
- Dynamic client rendering verification
"""

import os
import re
from django.conf import settings
from django.test import SimpleTestCase
from django.urls import reverse

from accounts.models import Student
from e2e_tests.base import BaseE2ETestCase
from quiz.models import Quiz
from result.models import TakenCourse


class FormContractStaticInspectionTest(SimpleTestCase):
    """Inspects template contracts directly from disk."""

    def setUp(self):
        self.templates_dir = os.path.join(settings.BASE_DIR, "templates")

    def test_course_registration_form_contract(self):
        """Ensures course_registration.html preserves exact input names for add/drop."""
        path = os.path.join(self.templates_dir, "course", "course_registration.html")
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        # Enrolling checkbox contract: name="{{ course.pk }}"
        enroll_regex = re.compile(
            r'<input[^>]+name=["\']\{\{\s*course\.pk\s*\}\}["\'][^>]*type=["\']checkbox["\']|'
            r'<input[^>]+type=["\']checkbox["\'][^>]+name=["\']\{\{\s*course\.pk\s*\}\}["\']'
        )
        self.assertRegex(
            content,
            enroll_regex,
            "Course registration template must have checkbox input with name='{{ course.pk }}'",
        )

        # Dropping checkbox contract: name="course_ids" and value="{{ course.id }}"
        drop_regex = re.compile(
            r'<input[^>]+name=["\']course_ids["\'][^>]+value=["\']\{\{\s*course\.id\s*\}\}["\']|'
            r'<input[^>]+value=["\']\{\{\s*course\.id\s*\}\}["\'][^>]+name=["\']course_ids["\']'
        )
        self.assertRegex(
            content,
            drop_regex,
            "Course drop form must have checkbox input with name='course_ids' and value='{{ course.id }}'",
        )

        # CSRF tags
        self.assertIn("{% csrf_token %}", content)

    def test_grade_entry_matrix_form_contract(self):
        """Ensures add_score_for.html provides 5 score inputs per student with name='{{ student.id }}'."""
        path = os.path.join(self.templates_dir, "result", "add_score_for.html")
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        # Input names contract: name="{{ student.id }}"
        student_id_inputs = re.findall(
            r'<input[^>]+name=["\']\{\{\s*student\.id\s*\}\}["\']', content
        )
        self.assertGreaterEqual(
            len(student_id_inputs),
            5,
            "add_score_for.html must contain at least 5 score inputs sharing name='{{ student.id }}'",
        )

        # Verifies presence of each expected input ID: assignment, mid_exam, quiz, attendance, final_exam
        expected_order = ["assignment", "mid_exam", "quiz", "attendance", "final_exam"]
        for field_id in expected_order:
            self.assertIn(
                f'id="{field_id}"',
                content,
                f"Grade entry matrix must include input with id='{field_id}'",
            )

        # Verify exact DOM positional ordering of the 5 inputs
        ordered_ids = re.findall(
            r'id=["\'](assignment|mid_exam|quiz|attendance|final_exam)["\']',
            content,
        )
        self.assertEqual(
            ordered_ids,
            expected_order,
            f"Score inputs must appear in exact positional order {expected_order}",
        )

        self.assertIn("{% csrf_token %}", content)

    def test_score_entry_positional_inputs_contract(self):
        """Verifies the 5 score inputs appear in exact DOM order required by result/views.py."""
        path = os.path.join(self.templates_dir, "result", "add_score_for.html")
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        expected_order = ["assignment", "mid_exam", "quiz", "attendance", "final_exam"]
        ordered_ids = re.findall(
            r'id=["\'](assignment|mid_exam|quiz|attendance|final_exam)["\']',
            content,
        )
        self.assertEqual(
            ordered_ids,
            expected_order,
            "add_score_for.html must render the 5 score inputs in exact order: "
            "['assignment', 'mid_exam', 'quiz', 'attendance', 'final_exam']",
        )
        positional_regex = re.compile(
            r'id=["\']assignment["\'].*?id=["\']mid_exam["\'].*?id=["\']quiz["\'].*?'
            r'id=["\']attendance["\'].*?id=["\']final_exam["\']',
            re.DOTALL,
        )
        self.assertRegex(
            content,
            positional_regex,
            "DOM order of score inputs must match positional unpacking in result/views.py",
        )

    def test_mcquestion_inline_formset_contract(self):
        """Ensures mcquestion_form.html renders management_form and choice fields."""
        path = os.path.join(self.templates_dir, "quiz", "mcquestion_form.html")
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        self.assertIn(
            "{{ formset.management_form }}",
            content,
            "mcquestion_form.html must render {{ formset.management_form }}",
        )
        self.assertIn("choice_text", content)
        self.assertIn("correct", content)
        self.assertIn("{% csrf_token %}", content)

    def test_search_view_class_name_contract(self):
        """Ensures search_view.html loads class_name filter and checks model classes."""
        path = os.path.join(self.templates_dir, "search", "search_view.html")
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        self.assertIn("{% load class_name %}", content)
        self.assertIn('"Program"', content)
        self.assertIn('"Course"', content)
        self.assertIn('"NewsAndEvents"', content)
        self.assertIn('"Quiz"', content)

    def test_csrf_token_in_all_post_forms(self):
        """Validates that every template with a POST form contains {% csrf_token %}."""
        form_post_regex = re.compile(r'<form[^>]+method=["\']post["\']', re.IGNORECASE)
        missing_csrf = []

        for root, _, files in os.walk(self.templates_dir):
            for file in files:
                if file.endswith(".html"):
                    file_path = os.path.join(root, file)
                    rel_path = os.path.relpath(file_path, settings.BASE_DIR)
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()
                        if form_post_regex.search(content):
                            if "{% csrf_token %}" not in content:
                                missing_csrf.append(rel_path)

        self.assertEqual(
            len(missing_csrf),
            0,
            f"Templates with POST forms missing {{% csrf_token %}}: {missing_csrf}",
        )


class DynamicFormContractsRenderedTest(BaseE2ETestCase):
    """Validates rendered DOM elements of critical forms via Django Test Client."""

    def test_course_registration_rendered_checkboxes(self):
        """Verifies rendered course registration table has checkbox with name matching course pk."""
        self.login_as_student()
        url = reverse("course_registration")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        content = response.content.decode("utf-8")
        # Should render input name="<pk>" for IT101
        expected_input_name = f'name="{self.course.pk}"'
        self.assertIn(
            expected_input_name,
            content,
            f"Rendered registration page must have checkbox with name='{self.course.pk}'",
        )
        self.assertIn('csrfmiddlewaretoken', content)

    def test_grade_entry_rendered_matrix_inputs(self):
        """Verifies rendered score matrix page has 5 inputs named after TakenCourse.id."""
        # Create a TakenCourse record first
        taken = TakenCourse.objects.create(
            student=self.student_profile,
            course=self.course,
        )
        self.login_as_lecturer()
        url = reverse("add_score_for", kwargs={"id": self.course.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        content = response.content.decode("utf-8")
        expected_taken_name = f'name="{taken.id}"'
        self.assertIn(
            expected_taken_name,
            content,
            f"Rendered grading table must have inputs named '{taken.id}' (TakenCourse.id)",
        )
        ordered_ids = re.findall(
            r'id=["\'](assignment|mid_exam|quiz|attendance|final_exam)["\']',
            content,
        )
        self.assertEqual(
            ordered_ids,
            ["assignment", "mid_exam", "quiz", "attendance", "final_exam"],
        )

    def test_mcquestion_builder_rendered_formset(self):
        """Verifies question builder renders inline formset management form inputs."""
        quiz = Quiz.objects.create(
            course=self.course,
            title="Kiểm tra Lập trình",
            pass_mark=60,
        )
        self.login_as_lecturer()
        url = reverse("mc_create", kwargs={"slug": self.course.slug, "quiz_id": quiz.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        content = response.content.decode("utf-8")
        self.assertIn("choice_set-TOTAL_FORMS", content)
        self.assertIn("choice_set-INITIAL_FORMS", content)
        self.assertIn("csrfmiddlewaretoken", content)
