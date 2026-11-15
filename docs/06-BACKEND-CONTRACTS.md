# Hợp đồng backend hiện hữu

> Baseline: [SkyCascade/SkyLearn](https://github.com/SkyCascade/SkyLearn), nhánh `main`, commit `d57f57bd505447b59fdf82b16469494443cafe0c`. Đây là bản kiểm kê mã nguồn, không phải đặc tả tính năng mới. Trạng thái tải source và kiểm thử: [11-SETUP-AND-DEPLOYMENT.md](11-SETUP-AND-DEPLOYMENT.md).

Django server-side rendering, không phải REST API. 82 route app khai báo tường minh dưới đây; ngoài ra root mount `/admin/`, `/i18n/`, `/jsi18n/`, `/jet/`, `/jet/dashboard/` và các route mặc định của `django.contrib.auth.urls`. Regex excludes commented paths. HTTP methods ghi theo xử lý thực sự trong handler, không suy diễn schema JSON.

| BR | Route | Handler | Method/kiểu | Auth/role | Nguồn |
| --- | --- | --- | --- | --- | --- |
| BR-001 | `/` | `home_view` | GET/HTML | Theo view; xem 05 | [`core/views.py::home_view`](../core/views.py) |
| BR-002 | `/add_item/` | `post_add` | GET/HTML | Theo view; xem 05 | [`core/views.py::post_add`](../core/views.py) |
| BR-003 | `/item/<int:pk>/edit/` | `edit_post` | GET/HTML | Giảng viên/Admin | [`core/views.py::edit_post`](../core/views.py) |
| BR-004 | `/item/<int:pk>/delete/` | `delete_post` | GET/HTML | Giảng viên/Admin | [`core/views.py::delete_post`](../core/views.py) |
| BR-005 | `/session/` | `session_list_view` | GET/HTML | Giảng viên/Admin | [`core/views.py::session_list_view`](../core/views.py) |
| BR-006 | `/session/add/` | `session_add_view` | GET/HTML | Giảng viên/Admin | [`core/views.py::session_add_view`](../core/views.py) |
| BR-007 | `/session/<int:pk>/edit/` | `session_update_view` | GET/HTML | Giảng viên/Admin | [`core/views.py::session_update_view`](../core/views.py) |
| BR-008 | `/session/<int:pk>/delete/` | `session_delete_view` | GET/HTML | Giảng viên/Admin | [`core/views.py::session_delete_view`](../core/views.py) |
| BR-009 | `/semester/` | `semester_list_view` | GET/HTML | Giảng viên/Admin | [`core/views.py::semester_list_view`](../core/views.py) |
| BR-010 | `/semester/add/` | `semester_add_view` | GET/HTML | Giảng viên/Admin | [`core/views.py::semester_add_view`](../core/views.py) |
| BR-011 | `/semester/<int:pk>/edit/` | `semester_update_view` | GET/HTML | Giảng viên/Admin | [`core/views.py::semester_update_view`](../core/views.py) |
| BR-012 | `/semester/<int:pk>/delete/` | `semester_delete_view` | GET/HTML | Giảng viên/Admin | [`core/views.py::semester_delete_view`](../core/views.py) |
| BR-013 | `/dashboard/` | `dashboard_view` | GET/HTML | Admin | [`core/views.py::dashboard_view`](../core/views.py) |
| BR-014 | `/accounts/admin_panel/` | `admin_panel` | GET/HTML | Admin | [`accounts/views.py::admin_panel`](../accounts/views.py) |
| BR-015 | `/accounts/profile/` | `profile` | GET/HTML | Theo view; xem 05 | [`accounts/views.py::profile`](../accounts/views.py) |
| BR-016 | `/accounts/profile/<int:user_id>/detail/` | `profile_single` | GET/HTML | Admin | [`accounts/views.py::profile_single`](../accounts/views.py) |
| BR-017 | `/accounts/setting/` | `profile_update` | GET/HTML | Theo view; xem 05 | [`accounts/views.py::profile_update`](../accounts/views.py) |
| BR-018 | `/accounts/change_password/` | `change_password` | GET/HTML | Theo view; xem 05 | [`accounts/views.py::change_password`](../accounts/views.py) |
| BR-019 | `/accounts/lecturers/` | `LecturerFilterView` | GET/HTML | Theo view; xem 05 | [`accounts/views.py::LecturerFilterView`](../accounts/views.py) |
| BR-020 | `/accounts/lecturer/add/` | `staff_add_view` | GET/HTML | Admin | [`accounts/views.py::staff_add_view`](../accounts/views.py) |
| BR-021 | `/accounts/staff/<int:pk>/edit/` | `edit_staff` | GET/HTML | Admin | [`accounts/views.py::edit_staff`](../accounts/views.py) |
| BR-022 | `/accounts/lecturers/<int:pk>/delete/` | `delete_staff` | GET/HTML | Admin | [`accounts/views.py::delete_staff`](../accounts/views.py) |
| BR-023 | `/accounts/students/` | `StudentListView` | GET/HTML | Theo view; xem 05 | [`accounts/views.py::StudentListView`](../accounts/views.py) |
| BR-024 | `/accounts/student/add/` | `student_add_view` | GET/HTML | Admin | [`accounts/views.py::student_add_view`](../accounts/views.py) |
| BR-025 | `/accounts/student/<int:pk>/edit/` | `edit_student` | GET/HTML | Admin | [`accounts/views.py::edit_student`](../accounts/views.py) |
| BR-026 | `/accounts/students/<int:pk>/delete/` | `delete_student` | GET/HTML | Admin | [`accounts/views.py::delete_student`](../accounts/views.py) |
| BR-027 | `/accounts/edit_student_program/<int:pk>/` | `edit_student_program` | GET/HTML | Admin | [`accounts/views.py::edit_student_program`](../accounts/views.py) |
| BR-028 | `/accounts/parents/add/` | `ParentAdd` | GET/HTML | Theo view; xem 05 | [`accounts/views.py::ParentAdd`](../accounts/views.py) |
| BR-029 | `/accounts/ajax/validate-username/` | `validate_username` | GET/JSON | Công khai | [`accounts/views.py::validate_username`](../accounts/views.py) |
| BR-030 | `/accounts/register/` | `register` | GET/HTML | Công khai | [`accounts/views.py::register`](../accounts/views.py) |
| BR-031 | `/accounts/create_lecturers_pdf_list/` | `render_lecturer_pdf_list` | GET/PDF | Admin | [`accounts/views.py::render_lecturer_pdf_list`](../accounts/views.py) |
| BR-032 | `/accounts/create_students_pdf_list/` | `render_student_pdf_list` | GET/PDF | Admin | [`accounts/views.py::render_student_pdf_list`](../accounts/views.py) |
| BR-033 | `/programs/` | `ProgramFilterView` | GET/HTML | Theo view; xem 05 | [`course/views.py::ProgramFilterView`](../course/views.py) |
| BR-034 | `/programs/<int:pk>/detail/` | `program_detail` | GET/HTML | Theo view; xem 05 | [`course/views.py::program_detail`](../course/views.py) |
| BR-035 | `/programs/add/` | `program_add` | GET/HTML | Giảng viên/Admin | [`course/views.py::program_add`](../course/views.py) |
| BR-036 | `/programs/<int:pk>/edit/` | `program_edit` | GET/HTML | Giảng viên/Admin | [`course/views.py::program_edit`](../course/views.py) |
| BR-037 | `/programs/<int:pk>/delete/` | `program_delete` | GET/HTML | Giảng viên/Admin | [`course/views.py::program_delete`](../course/views.py) |
| BR-038 | `/programs/course/<slug>/detail/` | `course_single` | GET/HTML | Theo view; xem 05 | [`course/views.py::course_single`](../course/views.py) |
| BR-039 | `/programs/<int:pk>/course/add/` | `course_add` | GET/HTML | Giảng viên/Admin | [`course/views.py::course_add`](../course/views.py) |
| BR-040 | `/programs/course/<slug>/edit/` | `course_edit` | GET/HTML | Giảng viên/Admin | [`course/views.py::course_edit`](../course/views.py) |
| BR-041 | `/programs/course/delete/<slug>/` | `course_delete` | GET/HTML | Giảng viên/Admin | [`course/views.py::course_delete`](../course/views.py) |
| BR-042 | `/programs/course/assign/` | `CourseAllocationFormView` | GET/HTML | Theo view; xem 05 | [`course/views.py::CourseAllocationFormView`](../course/views.py) |
| BR-043 | `/programs/course/allocated/` | `CourseAllocationFilterView` | GET/HTML | Theo view; xem 05 | [`course/views.py::CourseAllocationFilterView`](../course/views.py) |
| BR-044 | `/programs/allocated_course/<int:pk>/edit/` | `edit_allocated_course` | GET/HTML | Giảng viên/Admin | [`course/views.py::edit_allocated_course`](../course/views.py) |
| BR-045 | `/programs/course/<int:pk>/deallocate/` | `deallocate_course` | GET/HTML | Giảng viên/Admin | [`course/views.py::deallocate_course`](../course/views.py) |
| BR-046 | `/programs/course/<slug>/documentations/upload/` | `handle_file_upload` | GET/HTML | Giảng viên/Admin | [`course/views.py::handle_file_upload`](../course/views.py) |
| BR-047 | `/programs/course/<slug>/documentations/<int:file_id>/edit/` | `handle_file_edit` | GET/HTML | Giảng viên/Admin | [`course/views.py::handle_file_edit`](../course/views.py) |
| BR-048 | `/programs/course/<slug>/documentations/<int:file_id>/delete/` | `handle_file_delete` | GET/HTML | Giảng viên/Admin | [`course/views.py::handle_file_delete`](../course/views.py) |
| BR-049 | `/programs/course/<slug>/video_tutorials/upload/` | `handle_video_upload` | GET/HTML | Giảng viên/Admin | [`course/views.py::handle_video_upload`](../course/views.py) |
| BR-050 | `/programs/course/<slug>/video_tutorials/<video_slug>/detail/` | `handle_video_single` | GET/HTML | Theo view; xem 05 | [`course/views.py::handle_video_single`](../course/views.py) |
| BR-051 | `/programs/course/<slug>/video_tutorials/<video_slug>/edit/` | `handle_video_edit` | GET/HTML | Giảng viên/Admin | [`course/views.py::handle_video_edit`](../course/views.py) |
| BR-052 | `/programs/course/<slug>/video_tutorials/<video_slug>/delete/` | `handle_video_delete` | GET/HTML | Giảng viên/Admin | [`course/views.py::handle_video_delete`](../course/views.py) |
| BR-053 | `/programs/course/registration/` | `course_registration` | GET/HTML | Sinh viên/Admin | [`course/views.py::course_registration`](../course/views.py) |
| BR-054 | `/programs/course/drop/` | `course_drop` | GET/HTML | Sinh viên/Admin | [`course/views.py::course_drop`](../course/views.py) |
| BR-055 | `/programs/my_courses/` | `user_course_list` | GET/HTML | Theo view; xem 05 | [`course/views.py::user_course_list`](../course/views.py) |
| BR-056 | `/result/manage-score/` | `add_score` | GET/HTML | Giảng viên/Admin | [`result/views.py::add_score`](../result/views.py) |
| BR-057 | `/result/manage-score/<int:id>/` | `add_score_for` | GET/HTML | Giảng viên/Admin | [`result/views.py::add_score_for`](../result/views.py) |
| BR-058 | `/result/grade/` | `grade_result` | GET/HTML | Sinh viên/Admin | [`result/views.py::grade_result`](../result/views.py) |
| BR-059 | `/result/assessment/` | `assessment_result` | GET/HTML | Sinh viên/Admin | [`result/views.py::assessment_result`](../result/views.py) |
| BR-060 | `/result/result/print/<int:id>/` | `result_sheet_pdf_view` | GET/PDF | Giảng viên/Admin | [`result/views.py::result_sheet_pdf_view`](../result/views.py) |
| BR-061 | `/result/registration/form/` | `course_registration_form` | GET/PDF | Sinh viên/Admin | [`result/views.py::course_registration_form`](../result/views.py) |
| BR-062 | `/quiz/<slug>/quizzes/` | `quiz_list` | GET/HTML | Theo view; xem 05 | [`quiz/views.py::quiz_list`](../quiz/views.py) |
| BR-063 | `/quiz/progress/` | `QuizUserProgressView` | GET/HTML | Theo view; xem 05 | [`quiz/views.py::QuizUserProgressView`](../quiz/views.py) |
| BR-064 | `/quiz/marking_list/` | `QuizMarkingList` | GET/HTML | Giảng viên/Admin | [`quiz/views.py::QuizMarkingList`](../quiz/views.py) |
| BR-065 | `/quiz/marking/<int:pk>/` | `QuizMarkingDetail` | GET/HTML | Giảng viên/Admin | [`quiz/views.py::QuizMarkingDetail`](../quiz/views.py) |
| BR-066 | `/quiz/<int:pk>/<slug>/take/` | `QuizTake` | GET/HTML | Theo view; xem 05 | [`quiz/views.py::QuizTake`](../quiz/views.py) |
| BR-067 | `/quiz/<slug>/quiz_add/` | `QuizCreateView` | GET/HTML | Theo view; xem 05 | [`quiz/views.py::QuizCreateView`](../quiz/views.py) |
| BR-068 | `/quiz/<slug>/<int:pk>/add/` | `QuizUpdateView` | GET/HTML | Theo view; xem 05 | [`quiz/views.py::QuizUpdateView`](../quiz/views.py) |
| BR-069 | `/quiz/<slug>/<int:pk>/delete/` | `quiz_delete` | GET/HTML | Giảng viên/Admin | [`quiz/views.py::quiz_delete`](../quiz/views.py) |
| BR-070 | `/quiz/mc-question/add/<slug>/<int:quiz_id>/` | `MCQuestionCreate` | GET/HTML | Theo view; xem 05 | [`quiz/views.py::MCQuestionCreate`](../quiz/views.py) |
| BR-071 | `/payments/` | `PaymentGetwaysView` | GET/HTML | Chưa kiểm soát rõ | [`payments/views.py::PaymentGetwaysView`](../payments/views.py) |
| BR-072 | `/payments/paypal/` | `payment_paypal` | GET/HTML | Chưa kiểm soát rõ | [`payments/views.py::payment_paypal`](../payments/views.py) |
| BR-073 | `/payments/stripe/` | `payment_stripe` | GET/HTML | Chưa kiểm soát rõ | [`payments/views.py::payment_stripe`](../payments/views.py) |
| BR-074 | `/payments/coinbase/` | `payment_coinbase` | GET/HTML | Chưa kiểm soát rõ | [`payments/views.py::payment_coinbase`](../payments/views.py) |
| BR-075 | `/payments/paylike/` | `payment_paylike` | GET/HTML | Chưa kiểm soát rõ | [`payments/views.py::payment_paylike`](../payments/views.py) |
| BR-076 | `/payments/stripe-charge/` | `stripe_charge` | POST/JSON | Chưa kiểm soát rõ | [`payments/views.py::stripe_charge`](../payments/views.py) |
| BR-077 | `/payments/gopay-charge/` | `gopay_charge` | POST/JSON | Chưa kiểm soát rõ | [`payments/views.py::gopay_charge`](../payments/views.py) |
| BR-078 | `/payments/payment-succeed/` | `payment_succeed` | GET/HTML | Chưa kiểm soát rõ | [`payments/views.py::payment_succeed`](../payments/views.py) |
| BR-079 | `/payments/complete/` | `paymentComplete` | POST/JSON | Chưa kiểm soát rõ | [`payments/views.py::paymentComplete`](../payments/views.py) |
| BR-080 | `/payments/create-invoice/` | `create_invoice` | GET/HTML | Chưa kiểm soát rõ | [`payments/views.py::create_invoice`](../payments/views.py) |
| BR-081 | `/payments/invoice-detail/<int:id>/` | `invoice_detail` | GET/HTML | Chưa kiểm soát rõ | [`payments/views.py::invoice_detail`](../payments/views.py) |
| BR-082 | `/search/` | `SearchView` | GET/HTML | Theo view; xem 05 | [`search/views.py::SearchView`](../search/views.py) |

## Request và response chi tiết theo họ chức năng

- **Auth/profile:** `register` POST `StudentAddForm`; `change_password` dùng form đổi password; `profile_update` dùng `ProfileUpdateForm` với first_name, last_name, gender, email, phone, address, picture. Django auth URLs xử lý login/logout/password reset; xem [`accounts/forms.py`](../accounts/forms.py), [`accounts/urls.py`](../accounts/urls.py), [`accounts/views.py`](../accounts/views.py).
- **CRUD học vụ:** `ProgramForm` title, summary; `CourseAddForm` các field model Course; `CourseAllocationForm` lecturer và courses; upload `UploadFormFile(title,file)` / `UploadFormVideo(title,video)`. Invalid form render lại template với `form.errors`; successful handler redirect theo code. [`course/forms.py`](../course/forms.py), [`course/views.py`](../course/views.py).
- **Add/drop:** POST `course_registration` dùng *tên các key POST* làm Course ID; `course_drop` dùng `course_ids` là danh sách; đều redirect `course_registration`. GET registration cung cấp `current_semester,courses,registered_courses,total_registered_credit,student` cùng flags và tổng tín chỉ kỳ. [`course/views.py`](../course/views.py).
- **Nhập điểm:** `add_score_for` POST key = TakenCourse.id, value list 5 phần tử theo thứ tự assignment, mid_exam, quiz, attendance, final_exam; lưu `TakenCourse`, `Result`, redirect lại cùng route. [`result/views.py`](../result/views.py), [`result/models.py`](../result/models.py).
- **Quiz:** `QuizAddForm` gồm trường Quiz và questions M2M; `MCQuestionFormSet` có choices với `choice_text,correct,DELETE`; `QuizTake` POST `answers`, render từng câu và trang result có `course,quiz,score,max_score,percent,sitting,previous`. GET progress có `cat_scores,exams,exams_counter`. [`quiz/forms.py`](../quiz/forms.py), [`quiz/views.py`](../quiz/views.py).
- **Search:** GET `q`, 20 kết quả/trang; context `count,query,object_list` từ NewsAndEvents/Program/Course/Quiz. [`search/views.py`](../search/views.py).
- **PDF:** các handler trong `accounts/views.py`, `result/views.py` render ReportLab/xhtml2pdf; kiểm tra response headers tại handler trước khi thay nút tải. 
- **Payment:** `create_invoice` POST `amount`, GET invoices của user; `stripe_charge` POST `stripeToken`; `gopay_charge` trả JSON `message`; `paymentComplete` trả JSON string. Đây là prototype có lỗi, không có response schema ổn định để thiết kế mới dựa vào. [`payments/views.py`](../payments/views.py).

### Các response JSON xác định được

| Route | Method/input | Response hiện tại | Handler |
| --- | --- | --- | --- |
| `/accounts/ajax/validate-username/` | GET `username` | `{"is_taken": boolean}` | `accounts.views.validate_username` |
| `/payments/gopay-charge/` | POST; GoPay dùng cấu hình mẫu | `{"message": string}`; GET cũng trả message `GET requested` | `payments.views.gopay_charge` |
| `/payments/complete/` | POST hoặc AJAX, đọc session/body | JSON string `"Payment completed!"`, có khả năng lỗi trước khi trả | `payments.views.paymentComplete` |

Không thấy REST serializer/viewset/API router trong `config/urls.py` và `INSTALLED_APPS`. `stripe_charge` gọi SDK rồi redirect, không trả JSON theo code hiện tại.

## Context, template và điều hướng

Các template gốc còn ở `templates/`; mapping chính xác `render(..., template, context)` nằm tại handler trong bảng. Django messages hiển thị success/error; CSRF cần giữ cho POST. Redirect không nên đổi tên route; `reverse_lazy` và `{% url %}` phụ thuộc name trong `urls.py`. Không có yêu cầu JSON API mới trong scope.

## Kiểm kê trực tiếp các literal trong handler

Bảng được trích từ `views.py`: chỉ ghi khóa `request.GET/POST.get*`, tên form, template và redirect xuất hiện trực tiếp trong thân handler. Dấu “—” nghĩa là **không có literal được trích**, không chứng minh contract trống: form bind `request.POST`, class inheritance, template gián tiếp hoặc dữ liệu POST động vẫn phải đọc hàm nguồn. Đây là điểm đối chiếu khi thay template.

| BR | Query key | POST key tường minh | Form class | Template literal | Redirect name |
| --- | --- | --- | --- | --- | --- |
+| BR-001 | — | — | — | `core/index.html` | — |
| BR-002 | — | — | `NewsAndEventsForm` | `core/post_add.html` | `home` |
| BR-003 | — | — | `NewsAndEventsForm` | `core/post_add.html` | `home` |
| BR-004 | — | — | — | — | `home` |
| BR-005 | — | — | — | `core/session_list.html` | — |
| BR-006 | — | — | `SessionForm` | `core/session_update.html` | `session_list` |
| BR-007 | — | — | `SessionForm` | `core/session_update.html` | `session_list` |
| BR-008 | — | — | — | — | `session_list` |
| BR-009 | — | — | — | `core/semester_list.html` | — |
| BR-010 | — | — | `SemesterForm` | `core/semester_update.html` | `semester_list` |
| BR-011 | — | — | `SemesterForm` | `core/semester_update.html` | `semester_list` |
| BR-012 | — | — | — | — | `semester_list` |
| BR-013 | — | — | — | `core/dashboard.html` | — |
| BR-014 | — | — | — | `setting/admin_panel.html` | — |
| BR-015 | — | — | — | `accounts/profile.html` | — |
| BR-016 | `download_pdf` | — | — | `accounts/profile_single.html` | `profile` |
| BR-017 | — | — | `ProfileUpdateForm` | `setting/profile_info_change.html` | `profile` |
| BR-018 | — | — | `PasswordChangeForm` | `setting/password_change.html` | `profile` |
| BR-019 | — | — | — | `accounts/lecturer_list.html` | — |
| BR-020 | — | — | `StaffAddForm` | `accounts/add_staff.html` | `lecturer_list` |
| BR-021 | — | — | `ProfileUpdateForm` | `accounts/edit_lecturer.html` | `lecturer_list` |
| BR-022 | — | — | — | — | `lecturer_list` |
| BR-023 | — | — | — | `accounts/student_list.html` | — |
| BR-024 | — | — | `StudentAddForm` | `accounts/add_student.html` | `student_list` |
| BR-025 | — | — | `ProfileUpdateForm` | `accounts/edit_student.html` | `student_list` |
| BR-026 | — | — | — | — | `student_list` |
| BR-027 | — | — | `ProgramUpdateForm` | `accounts/edit_student_program.html` | `profile_single` |
| BR-028 | — | — | — | `accounts/parent_form.html` | — |
| BR-029 | `username` | — | — | — | — |
| BR-030 | — | — | `StudentAddForm` | `registration/register.html` | `login` |
| BR-031 | — | — | — | — | — |
| BR-032 | — | — | — | — | — |
| BR-033 | — | — | — | `course/program_list.html` | — |
| BR-034 | `page` | — | — | `course/program_single.html` | — |
| BR-035 | — | — | `ProgramForm` | `course/program_add.html` | `programs` |
| BR-036 | — | — | `ProgramForm` | `course/program_add.html` | `programs` |
| BR-037 | — | — | — | — | `programs` |
| BR-038 | — | — | — | `course/course_single.html` | — |
| BR-039 | — | — | `CourseAddForm` | `course/course_add.html` | `program_detail` |
| BR-040 | — | — | `CourseAddForm` | `course/course_add.html` | `program_detail` |
| BR-041 | — | — | — | — | `program_detail` |
| BR-042 | — | — | — | `course/course_allocation_form.html` | `course_allocation_view` |
| BR-043 | — | — | — | `course/course_allocation_view.html` | — |
| BR-044 | — | — | `EditCourseAllocationForm` | `course/course_allocation_form.html` | `course_allocation_view` |
| BR-045 | — | — | — | — | `course_allocation_view` |
| BR-046 | — | — | — | `upload/upload_file_form.html` | `course_detail` |
| BR-047 | — | — | — | `upload/upload_file_form.html` | `course_detail` |
| BR-048 | — | — | — | — | `course_detail` |
| BR-049 | — | — | — | `upload/upload_video_form.html` | `course_detail` |
| BR-050 | — | — | — | `upload/video_single.html` | — |
| BR-051 | — | — | — | `upload/upload_video_form.html` | `course_detail` |
| BR-052 | — | — | — | — | `course_detail` |
| BR-053 | — | — | — | `course/course_registration.html` | `course_registration` |
| BR-054 | — | `course_ids` | — | — | `course_registration` |
| BR-055 | — | — | — | `course/user_course_list.html` | — |
| BR-056 | — | — | — | `result/add_score.html` | — |
| BR-057 | — | — | — | `result/add_score_for.html` | `add_score_for` |
| BR-058 | — | — | — | `result/grade_results.html` | — |
| BR-059 | — | — | — | `result/assessment_results.html` | — |
| BR-060 | — | — | — | — | — |
| BR-061 | — | — | — | — | — |
| BR-062 | — | — | — | `quiz/quiz_list.html` | — |
| BR-063 | — | — | — | `quiz/progress.html` | — |
| BR-064 | `quiz_filter`, `user_filter` | — | — | `quiz/quiz_marking_list.html` | — |
| BR-065 | — | `qid` | — | `quiz/quiz_marking_detail.html` | — |
| BR-066 | — | — | — | `quiz/question.html`, `quiz/result.html` | `quiz_index` |
| BR-067 | — | — | — | `quiz/quiz_form.html` | `mc_create` |
| BR-068 | — | — | — | `quiz/quiz_form.html` | `quiz_index` |
| BR-069 | — | — | — | — | `quiz_index` |
| BR-070 | — | — | `MCQuestionFormSet` | `quiz/mcquestion_form.html` | `mc_create`, `quiz_index` |
| BR-071 | — | — | — | `payments/payment_gateways.html` | — |
| BR-072 | — | — | — | `payments/paypal.html` | — |
| BR-073 | — | — | — | `payments/stripe.html` | — |
| BR-074 | — | — | — | `payments/coinbase.html` | — |
| BR-075 | — | — | — | `payments/paylike.html` | — |
| BR-076 | — | — | — | `payments/charge.html` | `completed` |
| BR-077 | — | — | — | — | — |
| BR-078 | — | — | — | `payments/payment_succeed.html` | — |
| BR-079 | — | — | — | — | `invoice` |
| BR-080 | — | `amount` | — | `invoices.html` | `payment_gateways` |
| BR-081 | — | — | — | `invoice_detail.html` | — |
| BR-082 | `q` | — | — | `search/search_view.html` | — |

