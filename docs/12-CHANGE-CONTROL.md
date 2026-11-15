# Kiểm soát thay đổi

> Baseline SkyLearn `main@d57f57bd505447b59fdf82b16469494443cafe0c`. Các ID nối với [03](03-BUSINESS-REQUIREMENTS.md), [06](06-BACKEND-CONTRACTS.md) và [09](09-TRACEABILITY-MATRIX.md).

## Bất biến cho giai đoạn frontend

Giữ nguyên 24 model, migrations, relationships, validation, `settings.py`, authentication/authorization, 82 app route names/paths, key GET/POST, context/template contracts, grading/quiz state và PDF/upload behavior. Frontend gốc ở `templates/` và `static/` là đối chứng; thiết kế mới chỉ áp dụng khi bạn cung cấp. Không tự bổ sung nghiệp vụ, công nghệ hoặc API.

## Quy trình thay đổi

1. Truy BR/TC/Screen trong [09](09-TRACEABILITY-MATRIX.md), đọc handler, form, model, template và test tương ứng.
2. Nếu thiết kế thiếu nghiệp vụ, ghi mâu thuẫn và đề xuất vị trí UI; không cắt nghiệp vụ. Nếu cần đổi backend/schema/quyền, lập change request với before/after contract, migration, test và ảnh hưởng vai trò để bạn quyết định.
3. Sau thay đổi UI, cập nhật [06](06-BACKEND-CONTRACTS.md), [08](08-FRONTEND-FUNCTIONAL-SPEC.md), [09](09-TRACEABILITY-MATRIX.md), [10](10-TESTING-AND-ACCEPTANCE.md), ghi thay đổi dưới đây. Chạy smoke + regression với baseline đầy đủ.

## Các vấn đề gốc cần giữ dấu vết

- `payments/views.py`: endpoint invoice URL `<int:id>` không khớp `invoice_detail(request, slug)`; `stripe_charge` redirect `completed` không khai báo; invoice session code/id bất nhất; GoPay dùng placeholder; `request.is_ajax()` đã lỗi thời.
- `course/views.py::course_registration`: POST không xác minh lại program/level/semester, không ngăn bản ghi trùng; `TakenCourse` không unique pair.
- `quiz/models.py::Progress.list_all_cat_scores` trả `{}`; README mô tả tiến độ theo category rộng hơn thực thi. `quiz/views.py::QuizTake` bắt đăng nhập dù README nói anonymous có thể làm tiếp bài.
- `accounts/decorators.py`: biểu thức lecturer/student có `or user.is_superuser`; `core/views.py::post_add`, vài CBV và payment views thiếu role/login guard. Không coi UI ẩn là bảo mật.
- `course/decorators.py` import `coursemanagement.models` không tồn tại trong cây này; chưa thấy được import vào route đang dùng.
- `result/views.py::add_score_for` catch-all `except`, Result string session/semester, và không tự đồng bộ điểm quiz vào điểm môn.
- `README.md`/TODO chưa nhất quán với code ở essay/True-False/payment/calendar/dashboard: `quiz/models.py` có `EssayQuestion` nhưng `check_if_correct` luôn false và không có màn hình tạo essay riêng; không có model True/False riêng trong module quiz. Ưu tiên luồng thực thi đã xác minh từ source.

## Change log

| Ngày | Phạm vi | Kết quả |
| --- | --- | --- |
| 2026-11-15 | Phân tích và tạo docs, không sửa logic/frontend | Baseline ảo từ GitHub; chưa thể full clone/chạy tests do môi trường |
| 2026-11-15 | Tái tạo mã nghiệp vụ theo yêu cầu | Toàn bộ 210 file ngoài static và 11 asset static được lưu byte-identical, xác minh 221 Git blob SHA; không sửa logic |

