# Hướng dẫn coding agent cho SkyLearn

## Nguồn sự thật

Baseline upstream: `SkyCascade/SkyLearn main@d57f57bd505447b59fdf82b16469494443cafe0c`. Bản code trong thư mục này là snapshot toàn bộ file ngoài static và các static được template dùng trực tiếp, đã kiểm tra SHA theo `docs/UPSTREAM-SNAPSHOT-MANIFEST.json`; vẫn thiếu phần lớn static vendor/icon và không có git metadata. Xem `docs/11-SETUP-AND-DEPLOYMENT.md`. Trước mọi edit, đọc `docs/01`–`12` liên quan và trực tiếp đọc `models.py`, `views.py`, `forms.py`, `urls.py`, template gốc và tests. Khi tài liệu và source mâu thuẫn, source upstream baseline thắng; cập nhật tài liệu.

## Phạm vi hiện tại

Chỉ phân tích, kiểm thử và viết tài liệu. Chưa triển khai frontend mới cho đến khi người dùng cung cấp thiết kế. Giữ `templates/` gốc để đối chiếu, không dùng bố cục/màu/typography/nhận diện của nó làm thiết kế mới. Không refactor logic, không thêm/bỏ nghiệp vụ, không đổi Django/SQLite/kiến trúc hoặc dependencies khi chưa có quyết định của người dùng.

## Bất biến

Bảo toàn schema/migrations/FK/M2M/validation, grading, quiz attempts/state, auth/role decorators, route names/paths/methods, form POST names, template context, redirect, PDF/file behavior. Mọi lỗi hiện hữu được ghi tại `docs/12-CHANGE-CONTROL.md`, không âm thầm sửa thành hành vi mới. Không coi README/TODO là implementation.

## Quy trình frontend sau khi có thiết kế

1. Tra `docs/09-TRACEABILITY-MATRIX.md` cho BR ↔ Screen ↔ Handler ↔ Model ↔ TC; xác định đủ mọi nghiệp vụ.
2. Đọc `docs/05-ROLES-AND-PERMISSIONS.md`, `docs/06-BACKEND-CONTRACTS.md`, `docs/08-FRONTEND-FUNCTIONAL-SPEC.md`; đối chiếu template và handler thật.
3. Thực hiện thiết kế mới ở lớp presentation; không tự thay contract/logic. Mâu thuẫn thiết kế với nghiệp vụ cần báo người dùng bằng ví dụ route/BR.
4. Sau mỗi thay đổi, chạy `manage.py check`, test hiện có, regression `docs/10-TESTING-AND-ACCEPTANCE.md`, so sánh từng TC với baseline; ghi kết quả thật, không báo pass nếu chưa chạy.
5. Cập nhật docs và change log `docs/12-CHANGE-CONTROL.md` khi source thay đổi.

## Bộ tài liệu chính thức

`docs/01-PROJECT-OVERVIEW.md`, `02-SYSTEM-ARCHITECTURE.md`, `03-BUSINESS-REQUIREMENTS.md`, `04-DATABASE-SCHEMA.md`, `05-ROLES-AND-PERMISSIONS.md`, `06-BACKEND-CONTRACTS.md`, `07-BUSINESS-WORKFLOWS.md`, `08-FRONTEND-FUNCTIONAL-SPEC.md`, `09-TRACEABILITY-MATRIX.md`, `10-TESTING-AND-ACCEPTANCE.md`, `11-SETUP-AND-DEPLOYMENT.md`, `12-CHANGE-CONTROL.md`.


## Commit convention for agents

- Follow Conventional Commits: `<type>(<scope>): <short description>`.
- Allowed types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `build`, `ci`, `chore`, `revert`.
- Use the affected app or area as scope, such as `accounts`, `course`, `quiz`, `result`, `templates`, or `docs`. Omit scope only for broad changes.
- Write the description in English, begin with a lowercase verb, omit the final period, and keep it concise (ideally under 72 characters total).
- Keep each commit focused on one coherent purpose. Add a body only when rationale or impact needs explanation.
- Mark intentional compatibility breaks with `!` and a `BREAKING CHANGE:` footer. Do not introduce a breaking business rule or contract change without explicit authorization.
- Use `Closes #<id>` only for an existing related issue.
- Never include secrets, `.env`, user data, generated build/cache files, or unrelated changes.
- Do not create commits unless requested. When asked, inspect `git status` and the staged diff first to avoid including unrelated work.

Examples:

```text
docs(traceability): clarify quiz attempt mapping
fix(quiz): preserve attempt state after refresh
feat(accounts): add profile update form
test(course): cover enrollment permission checks
```
