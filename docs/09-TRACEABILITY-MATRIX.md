# Ma trận truy xuất nguồn gốc

> Baseline SkyLearn `main@d57f57bd505447b59fdf82b16469494443cafe0c`. Các ID nối với [03](03-BUSINESS-REQUIREMENTS.md), [06](06-BACKEND-CONTRACTS.md) và [09](09-TRACEABILITY-MATRIX.md).

Một hàng cho mỗi route-backed BR. Screen “—” là action/PDF/JSON tích hợp vào màn hình nguồn, không phải một màn hình độc lập. TC có cùng số thứ tự với BR để kiểm tra smoke/functional. Role và model là phạm vi liên quan, không phải sự khẳng định mỗi handler ghi mọi model đó.

| Business ID | Nghiệp vụ | Actor | Screen ID | Backend Handler | Route/API | Data Model | Test Case ID |
| --- | --- | --- | --- | --- | --- | --- | --- |
| BR-001 | Xem tin tức và sự kiện | Theo view; xem 05 | SCR-001 | `core.views.home_view` | `/` | NewsAndEvents, Session, Semester, ActivityLog | TC-001 |
| BR-002 | Đăng tin/sự kiện | Theo view; xem 05 | SCR-002 | `core.views.post_add` | `/add_item/` | NewsAndEvents, Session, Semester, ActivityLog | TC-002 |
| BR-003 | Sửa tin/sự kiện | Giảng viên/Admin | SCR-003 | `core.views.edit_post` | `/item/<int:pk>/edit/` | NewsAndEvents, Session, Semester, ActivityLog | TC-003 |
| BR-004 | Xóa tin/sự kiện | Giảng viên/Admin | SCR-004 | `core.views.delete_post` | `/item/<int:pk>/delete/` | NewsAndEvents, Session, Semester, ActivityLog | TC-004 |
| BR-005 | Danh sách niên khóa | Giảng viên/Admin | SCR-005 | `core.views.session_list_view` | `/session/` | NewsAndEvents, Session, Semester, ActivityLog | TC-005 |
| BR-006 | Tạo niên khóa | Giảng viên/Admin | SCR-006 | `core.views.session_add_view` | `/session/add/` | NewsAndEvents, Session, Semester, ActivityLog | TC-006 |
| BR-007 | Sửa niên khóa | Giảng viên/Admin | SCR-007 | `core.views.session_update_view` | `/session/<int:pk>/edit/` | NewsAndEvents, Session, Semester, ActivityLog | TC-007 |
| BR-008 | Xóa niên khóa | Giảng viên/Admin | SCR-008 | `core.views.session_delete_view` | `/session/<int:pk>/delete/` | NewsAndEvents, Session, Semester, ActivityLog | TC-008 |
| BR-009 | Danh sách học kỳ | Giảng viên/Admin | SCR-009 | `core.views.semester_list_view` | `/semester/` | NewsAndEvents, Session, Semester, ActivityLog | TC-009 |
| BR-010 | Tạo học kỳ | Giảng viên/Admin | SCR-010 | `core.views.semester_add_view` | `/semester/add/` | NewsAndEvents, Session, Semester, ActivityLog | TC-010 |
| BR-011 | Sửa học kỳ | Giảng viên/Admin | SCR-011 | `core.views.semester_update_view` | `/semester/<int:pk>/edit/` | NewsAndEvents, Session, Semester, ActivityLog | TC-011 |
| BR-012 | Xóa học kỳ | Giảng viên/Admin | SCR-012 | `core.views.semester_delete_view` | `/semester/<int:pk>/delete/` | NewsAndEvents, Session, Semester, ActivityLog | TC-012 |
| BR-013 | Xem thống kê quản trị | Admin | SCR-013 | `core.views.dashboard_view` | `/dashboard/` | NewsAndEvents, Session, Semester, ActivityLog | TC-013 |
| BR-014 | Mở trang quản trị | Admin | SCR-014 | `accounts.views.admin_panel` | `/accounts/admin_panel/` | User, Student, Parent, DepartmentHead | TC-014 |
| BR-015 | Xem hồ sơ | Theo view; xem 05 | SCR-015 | `accounts.views.profile` | `/accounts/profile/` | User, Student, Parent, DepartmentHead | TC-015 |
| BR-016 | Xem hồ sơ người khác | Admin | SCR-016 | `accounts.views.profile_single` | `/accounts/profile/<int:user_id>/detail/` | User, Student, Parent, DepartmentHead | TC-016 |
| BR-017 | Cập nhật hồ sơ | Theo view; xem 05 | SCR-017 | `accounts.views.profile_update` | `/accounts/setting/` | User, Student, Parent, DepartmentHead | TC-017 |
| BR-018 | Đổi mật khẩu | Theo view; xem 05 | SCR-018 | `accounts.views.change_password` | `/accounts/change_password/` | User, Student, Parent, DepartmentHead | TC-018 |
| BR-019 | Tra cứu giảng viên | Theo view; xem 05 | SCR-019 | `accounts.views.LecturerFilterView` | `/accounts/lecturers/` | User, Student, Parent, DepartmentHead | TC-019 |
| BR-020 | Thêm giảng viên | Admin | SCR-020 | `accounts.views.staff_add_view` | `/accounts/lecturer/add/` | User, Student, Parent, DepartmentHead | TC-020 |
| BR-021 | Sửa giảng viên | Admin | SCR-021 | `accounts.views.edit_staff` | `/accounts/staff/<int:pk>/edit/` | User, Student, Parent, DepartmentHead | TC-021 |
| BR-022 | Xóa giảng viên | Admin | SCR-022 | `accounts.views.delete_staff` | `/accounts/lecturers/<int:pk>/delete/` | User, Student, Parent, DepartmentHead | TC-022 |
| BR-023 | Tra cứu sinh viên | Theo view; xem 05 | SCR-023 | `accounts.views.StudentListView` | `/accounts/students/` | User, Student, Parent, DepartmentHead | TC-023 |
| BR-024 | Thêm sinh viên | Admin | SCR-024 | `accounts.views.student_add_view` | `/accounts/student/add/` | User, Student, Parent, DepartmentHead | TC-024 |
| BR-025 | Sửa sinh viên | Admin | SCR-025 | `accounts.views.edit_student` | `/accounts/student/<int:pk>/edit/` | User, Student, Parent, DepartmentHead | TC-025 |
| BR-026 | Xóa sinh viên | Admin | SCR-026 | `accounts.views.delete_student` | `/accounts/students/<int:pk>/delete/` | User, Student, Parent, DepartmentHead | TC-026 |
| BR-027 | Đổi chương trình của sinh viên | Admin | SCR-027 | `accounts.views.edit_student_program` | `/accounts/edit_student_program/<int:pk>/` | User, Student, Parent, DepartmentHead | TC-027 |
| BR-028 | Thêm phụ huynh | Theo view; xem 05 | SCR-028 | `accounts.views.ParentAdd` | `/accounts/parents/add/` | User, Student, Parent, DepartmentHead | TC-028 |
| BR-029 | Kiểm tra tên đăng nhập | Công khai | — | `accounts.views.validate_username` | `/accounts/ajax/validate-username/` | User, Student, Parent, DepartmentHead | TC-029 |
| BR-030 | Sinh viên tự đăng ký | Công khai | SCR-030 | `accounts.views.register` | `/accounts/register/` | User, Student, Parent, DepartmentHead | TC-030 |
| BR-031 | Xuất danh sách giảng viên PDF | Admin | SCR-031 | `accounts.views.render_lecturer_pdf_list` | `/accounts/create_lecturers_pdf_list/` | User, Student, Parent, DepartmentHead | TC-031 |
| BR-032 | Xuất danh sách sinh viên PDF | Admin | SCR-032 | `accounts.views.render_student_pdf_list` | `/accounts/create_students_pdf_list/` | User, Student, Parent, DepartmentHead | TC-032 |
| BR-033 | Danh sách chương trình | Theo view; xem 05 | SCR-033 | `course.views.ProgramFilterView` | `/programs/` | Program, Course, CourseAllocation, Upload, UploadVideo, CourseOffer | TC-033 |
| BR-034 | Xem chương trình | Theo view; xem 05 | SCR-034 | `course.views.program_detail` | `/programs/<int:pk>/detail/` | Program, Course, CourseAllocation, Upload, UploadVideo, CourseOffer | TC-034 |
| BR-035 | Thêm chương trình | Giảng viên/Admin | SCR-035 | `course.views.program_add` | `/programs/add/` | Program, Course, CourseAllocation, Upload, UploadVideo, CourseOffer | TC-035 |
| BR-036 | Sửa chương trình | Giảng viên/Admin | SCR-036 | `course.views.program_edit` | `/programs/<int:pk>/edit/` | Program, Course, CourseAllocation, Upload, UploadVideo, CourseOffer | TC-036 |
| BR-037 | Xóa chương trình | Giảng viên/Admin | SCR-037 | `course.views.program_delete` | `/programs/<int:pk>/delete/` | Program, Course, CourseAllocation, Upload, UploadVideo, CourseOffer | TC-037 |
| BR-038 | Xem học phần | Theo view; xem 05 | SCR-038 | `course.views.course_single` | `/programs/course/<slug>/detail/` | Program, Course, CourseAllocation, Upload, UploadVideo, CourseOffer | TC-038 |
| BR-039 | Thêm học phần | Giảng viên/Admin | SCR-039 | `course.views.course_add` | `/programs/<int:pk>/course/add/` | Program, Course, CourseAllocation, Upload, UploadVideo, CourseOffer | TC-039 |
| BR-040 | Sửa học phần | Giảng viên/Admin | SCR-040 | `course.views.course_edit` | `/programs/course/<slug>/edit/` | Program, Course, CourseAllocation, Upload, UploadVideo, CourseOffer | TC-040 |
| BR-041 | Xóa học phần | Giảng viên/Admin | SCR-041 | `course.views.course_delete` | `/programs/course/delete/<slug>/` | Program, Course, CourseAllocation, Upload, UploadVideo, CourseOffer | TC-041 |
| BR-042 | Phân công giảng viên | Theo view; xem 05 | SCR-042 | `course.views.CourseAllocationFormView` | `/programs/course/assign/` | Program, Course, CourseAllocation, Upload, UploadVideo, CourseOffer | TC-042 |
| BR-043 | Xem phân công | Theo view; xem 05 | SCR-043 | `course.views.CourseAllocationFilterView` | `/programs/course/allocated/` | Program, Course, CourseAllocation, Upload, UploadVideo, CourseOffer | TC-043 |
| BR-044 | Sửa phân công | Giảng viên/Admin | SCR-044 | `course.views.edit_allocated_course` | `/programs/allocated_course/<int:pk>/edit/` | Program, Course, CourseAllocation, Upload, UploadVideo, CourseOffer | TC-044 |
| BR-045 | Hủy phân công | Giảng viên/Admin | SCR-045 | `course.views.deallocate_course` | `/programs/course/<int:pk>/deallocate/` | Program, Course, CourseAllocation, Upload, UploadVideo, CourseOffer | TC-045 |
| BR-046 | Tải tài liệu | Giảng viên/Admin | SCR-046 | `course.views.handle_file_upload` | `/programs/course/<slug>/documentations/upload/` | Program, Course, CourseAllocation, Upload, UploadVideo, CourseOffer | TC-046 |
| BR-047 | Sửa tài liệu | Giảng viên/Admin | SCR-047 | `course.views.handle_file_edit` | `/programs/course/<slug>/documentations/<int:file_id>/edit/` | Program, Course, CourseAllocation, Upload, UploadVideo, CourseOffer | TC-047 |
| BR-048 | Xóa tài liệu | Giảng viên/Admin | SCR-048 | `course.views.handle_file_delete` | `/programs/course/<slug>/documentations/<int:file_id>/delete/` | Program, Course, CourseAllocation, Upload, UploadVideo, CourseOffer | TC-048 |
| BR-049 | Tải video | Giảng viên/Admin | SCR-049 | `course.views.handle_video_upload` | `/programs/course/<slug>/video_tutorials/upload/` | Program, Course, CourseAllocation, Upload, UploadVideo, CourseOffer | TC-049 |
| BR-050 | Xem video | Theo view; xem 05 | SCR-050 | `course.views.handle_video_single` | `/programs/course/<slug>/video_tutorials/<video_slug>/detail/` | Program, Course, CourseAllocation, Upload, UploadVideo, CourseOffer | TC-050 |
| BR-051 | Sửa video | Giảng viên/Admin | SCR-051 | `course.views.handle_video_edit` | `/programs/course/<slug>/video_tutorials/<video_slug>/edit/` | Program, Course, CourseAllocation, Upload, UploadVideo, CourseOffer | TC-051 |
| BR-052 | Xóa video | Giảng viên/Admin | SCR-052 | `course.views.handle_video_delete` | `/programs/course/<slug>/video_tutorials/<video_slug>/delete/` | Program, Course, CourseAllocation, Upload, UploadVideo, CourseOffer | TC-052 |
| BR-053 | Đăng ký học phần | Sinh viên/Admin | SCR-053 | `course.views.course_registration` | `/programs/course/registration/` | Program, Course, CourseAllocation, Upload, UploadVideo, CourseOffer | TC-053 |
| BR-054 | Hủy học phần | Sinh viên/Admin | SCR-054 | `course.views.course_drop` | `/programs/course/drop/` | Program, Course, CourseAllocation, Upload, UploadVideo, CourseOffer | TC-054 |
| BR-055 | Xem học phần của tôi | Theo view; xem 05 | SCR-055 | `course.views.user_course_list` | `/programs/my_courses/` | Program, Course, CourseAllocation, Upload, UploadVideo, CourseOffer | TC-055 |
| BR-056 | Chọn môn nhập điểm | Giảng viên/Admin | SCR-056 | `result.views.add_score` | `/result/manage-score/` | TakenCourse, Result | TC-056 |
| BR-057 | Nhập điểm thành phần | Giảng viên/Admin | SCR-057 | `result.views.add_score_for` | `/result/manage-score/<int:id>/` | TakenCourse, Result | TC-057 |
| BR-058 | Xem điểm tổng kết | Sinh viên/Admin | SCR-058 | `result.views.grade_result` | `/result/grade/` | TakenCourse, Result | TC-058 |
| BR-059 | Xem điểm đánh giá | Sinh viên/Admin | SCR-059 | `result.views.assessment_result` | `/result/assessment/` | TakenCourse, Result | TC-059 |
| BR-060 | Xuất bảng điểm PDF | Giảng viên/Admin | — | `result.views.result_sheet_pdf_view` | `/result/result/print/<int:id>/` | TakenCourse, Result | TC-060 |
| BR-061 | Xuất phiếu đăng ký PDF | Sinh viên/Admin | — | `result.views.course_registration_form` | `/result/registration/form/` | TakenCourse, Result | TC-061 |
| BR-062 | Xem danh sách quiz | Theo view; xem 05 | SCR-062 | `quiz.views.quiz_list` | `/quiz/<slug>/quizzes/` | Quiz, Progress, Sitting, Question, MCQuestion, Choice, EssayQuestion | TC-062 |
| BR-063 | Xem tiến độ quiz | Theo view; xem 05 | SCR-063 | `quiz.views.QuizUserProgressView` | `/quiz/progress/` | Quiz, Progress, Sitting, Question, MCQuestion, Choice, EssayQuestion | TC-063 |
| BR-064 | Xem bài quiz đã nộp | Giảng viên/Admin | SCR-064 | `quiz.views.QuizMarkingList` | `/quiz/marking_list/` | Quiz, Progress, Sitting, Question, MCQuestion, Choice, EssayQuestion | TC-064 |
| BR-065 | Đánh dấu/chấm bài quiz | Giảng viên/Admin | SCR-065 | `quiz.views.QuizMarkingDetail` | `/quiz/marking/<int:pk>/` | Quiz, Progress, Sitting, Question, MCQuestion, Choice, EssayQuestion | TC-065 |
| BR-066 | Làm bài quiz | Theo view; xem 05 | SCR-066 | `quiz.views.QuizTake` | `/quiz/<int:pk>/<slug>/take/` | Quiz, Progress, Sitting, Question, MCQuestion, Choice, EssayQuestion | TC-066 |
| BR-067 | Tạo quiz | Theo view; xem 05 | SCR-067 | `quiz.views.QuizCreateView` | `/quiz/<slug>/quiz_add/` | Quiz, Progress, Sitting, Question, MCQuestion, Choice, EssayQuestion | TC-067 |
| BR-068 | Sửa quiz | Theo view; xem 05 | SCR-068 | `quiz.views.QuizUpdateView` | `/quiz/<slug>/<int:pk>/add/` | Quiz, Progress, Sitting, Question, MCQuestion, Choice, EssayQuestion | TC-068 |
| BR-069 | Xóa quiz | Giảng viên/Admin | SCR-069 | `quiz.views.quiz_delete` | `/quiz/<slug>/<int:pk>/delete/` | Quiz, Progress, Sitting, Question, MCQuestion, Choice, EssayQuestion | TC-069 |
| BR-070 | Tạo câu hỏi trắc nghiệm | Theo view; xem 05 | SCR-070 | `quiz.views.MCQuestionCreate` | `/quiz/mc-question/add/<slug>/<int:quiz_id>/` | Quiz, Progress, Sitting, Question, MCQuestion, Choice, EssayQuestion | TC-070 |
| BR-071 | Xem lựa chọn thanh toán | Chưa kiểm soát rõ | SCR-071 | `payments.views.PaymentGetwaysView` | `/payments/` | Invoice | TC-071 |
| BR-072 | Xem trang PayPal mẫu | Chưa kiểm soát rõ | SCR-072 | `payments.views.payment_paypal` | `/payments/paypal/` | Invoice | TC-072 |
| BR-073 | Xem trang Stripe mẫu | Chưa kiểm soát rõ | SCR-073 | `payments.views.payment_stripe` | `/payments/stripe/` | Invoice | TC-073 |
| BR-074 | Xem trang Coinbase mẫu | Chưa kiểm soát rõ | SCR-074 | `payments.views.payment_coinbase` | `/payments/coinbase/` | Invoice | TC-074 |
| BR-075 | Xem trang Paylike mẫu | Chưa kiểm soát rõ | SCR-075 | `payments.views.payment_paylike` | `/payments/paylike/` | Invoice | TC-075 |
| BR-076 | Gửi lệnh Stripe mẫu | Chưa kiểm soát rõ | — | `payments.views.stripe_charge` | `/payments/stripe-charge/` | Invoice | TC-076 |
| BR-077 | Gửi lệnh GoPay mẫu | Chưa kiểm soát rõ | — | `payments.views.gopay_charge` | `/payments/gopay-charge/` | Invoice | TC-077 |
| BR-078 | Xem thông báo thanh toán | Chưa kiểm soát rõ | SCR-078 | `payments.views.payment_succeed` | `/payments/payment-succeed/` | Invoice | TC-078 |
| BR-079 | Đánh dấu hoàn tất thanh toán mẫu | Chưa kiểm soát rõ | — | `payments.views.paymentComplete` | `/payments/complete/` | Invoice | TC-079 |
| BR-080 | Tạo/xem hóa đơn | Chưa kiểm soát rõ | SCR-080 | `payments.views.create_invoice` | `/payments/create-invoice/` | Invoice | TC-080 |
| BR-081 | Xem hóa đơn theo mã | Chưa kiểm soát rõ | SCR-081 | `payments.views.invoice_detail` | `/payments/invoice-detail/<int:id>/` | Invoice | TC-081 |
| BR-082 | Tìm kiếm toàn hệ thống | Theo view; xem 05 | SCR-082 | `search.views.SearchView` | `/search/` | NewsAndEvents, Program, Course, Quiz | TC-082 |

## Kiểm tra đối chiếu

- 82 BR ↔ 82 route app ↔ 82 TC; 76 screen IDs và 6 action không có màn hình riêng. Các route auth mặc định và mount hệ thống trình bày riêng trong [06](06-BACKEND-CONTRACTS.md).
- Trước redesign, duyệt toàn bộ template thực tế và rà nút/link theo name URL; một screen có thể chứa thao tác nhiều BR. Payment đánh dấu prototype, không dùng làm tiêu chí “thanh toán thành công” khi backend chưa sửa.

