import os
import django
from decimal import Decimal
from django.core.files.base import ContentFile

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from accounts.models import User, Student, Parent
from course.models import Course, Program, Upload, UploadVideo
from quiz.models import Quiz, MCQuestion, Choice, Progress, Sitting
from payments.models import Invoice
from result.models import TakenCourse, Result
from core.models import Semester, Session

user = User.objects.get(username="SV202601")
student = Student.objects.get(student=user)
course_it101 = Course.objects.filter(code="IT101").first()
course_it202 = Course.objects.filter(code="IT202").first()

# 1. Parent Profile
parent_user, _ = User.objects.get_or_create(
    username="PH202601",
    defaults={
        "first_name": "Trần",
        "last_name": "Văn An",
        "email": "phuhuynh.an@cornlearn.edu.vn",
        "phone": "0987654321",
        "address": "Số 123 Đường Nguyễn Huệ, Quận 1, TP. Hồ Chí Minh",
        "is_parent": True,
        "gender": "M",
    }
)
parent, _ = Parent.objects.get_or_create(
    student=student,
    defaults={
        "user": parent_user,
        "first_name": "Trần",
        "last_name": "Văn An",
        "email": "phuhuynh.an@cornlearn.edu.vn",
        "phone": "0987654321",
        "relation_ship": "Father",
    }
)
print("Parent configured:", parent)

# 2. Documents & Videos for IT101
if course_it101:
    up, created = Upload.objects.get_or_create(
        course=course_it101,
        title="Đề cương & Giáo trình Lập trình Web với Python/Django",
        defaults={
            "file": ContentFile(b"%PDF-1.4 Mock syllabus content for CornLearn", name="De_cuong_Django_2026.pdf")
        }
    )
    vid, vid_created = UploadVideo.objects.get_or_create(
        course=course_it101,
        title="Bài giảng 01: Kiến trúc MVT & Thiết lập Môi trường Django",
        defaults={
            "video": ContentFile(b"\x00\x00\x00 ftypisom", name="Bai_giang_01.mp4"),
            "summary": "Giới thiệu tổng quan về framework Django, mô hình Model-View-Template và cách cấu hình dự án chuẩn CornLearn."
        }
    )
    print("Uploads & Video configured:", up, vid)

# 3. Quiz for IT101
if course_it101:
    quiz, q_created = Quiz.objects.get_or_create(
        course=course_it101,
        title="Kiểm tra Trắc nghiệm: Kiến trúc & Mô hình MVT trong Django",
        defaults={
            "description": "Bài kiểm tra đánh giá kiến thức cơ bản về kiến trúc Django MVT, ORM và URL Routing.",
            "pass_mark": 50,
            "single_attempt": False,
            "exam_paper": True,
            "draft": False,
        }
    )
    
    # Question 1
    q1, _ = MCQuestion.objects.get_or_create(
        content="Trong kiến trúc MVT của Django, chữ cái 'T' đại diện cho thành phần nào?",
        defaults={
            "explanation": "'T' đại diện cho Template (Giao diện hiển thị HTML).",
        }
    )
    q1.quiz.add(quiz)
    Choice.objects.get_or_create(question=q1, choice_text="Template (Lớp giao diện)", defaults={"correct": True})
    Choice.objects.get_or_create(question=q1, choice_text="Thread (Xử lý đa luồng)", defaults={"correct": False})
    Choice.objects.get_or_create(question=q1, choice_text="Transaction (Giao dịch CSDL)", defaults={"correct": False})
    Choice.objects.get_or_create(question=q1, choice_text="Type (Định kiểu dữ liệu)", defaults={"correct": False})

    # Question 2
    q2, _ = MCQuestion.objects.get_or_create(
        content="Lệnh nào sau đây dùng để áp dụng các thay đổi migration vào cơ sở dữ liệu?",
        defaults={
            "explanation": "python manage.py migrate dùng để chạy migrations vào database.",
        }
    )
    q2.quiz.add(quiz)
    Choice.objects.get_or_create(question=q2, choice_text="python manage.py migrate", defaults={"correct": True})
    Choice.objects.get_or_create(question=q2, choice_text="python manage.py makemigrations", defaults={"correct": False})
    Choice.objects.get_or_create(question=q2, choice_text="python manage.py sqlmigrate", defaults={"correct": False})
    Choice.objects.get_or_create(question=q2, choice_text="python manage.py runserver", defaults={"correct": False})

    # Question 3
    q3, _ = MCQuestion.objects.get_or_create(
        content="File cấu hình chính của dự án Django chứa danh sách INSTALLED_APPS là file nào?",
        defaults={
            "explanation": "settings.py lưu trữ cấu hình INSTALLED_APPS.",
        }
    )
    q3.quiz.add(quiz)
    Choice.objects.get_or_create(question=q3, choice_text="settings.py", defaults={"correct": True})
    Choice.objects.get_or_create(question=q3, choice_text="urls.py", defaults={"correct": False})
    Choice.objects.get_or_create(question=q3, choice_text="wsgi.py", defaults={"correct": False})
    Choice.objects.get_or_create(question=q3, choice_text="manage.py", defaults={"correct": False})

    print("Quiz configured with questions:", quiz)

# 4. TakenCourse Grades
for tc in TakenCourse.objects.filter(student=student):
    tc.assignment = Decimal("8.50")
    tc.mid_exam = Decimal("8.00")
    tc.quiz = Decimal("9.00")
    tc.attendance = Decimal("10.00")
    tc.final_exam = Decimal("8.50")
    tc.save()
print("Grades updated for taken courses.")

# 5. Tuition Invoice
inv, inv_created = Invoice.objects.get_or_create(
    user=user,
    invoice_code="INV-2026-001",
    defaults={
        "amount": Decimal("1500000"),
        "total": Decimal("1500000"),
        "payment_complete": False,
    }
)
print("Invoice configured:", inv)
