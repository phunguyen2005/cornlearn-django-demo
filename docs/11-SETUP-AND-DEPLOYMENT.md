# Cài đặt, chạy thử và trạng thái môi trường

> Baseline SkyLearn `main@d57f57bd505447b59fdf82b16469494443cafe0c`. Các ID nối với [03](03-BUSINESS-REQUIREMENTS.md), [06](06-BACKEND-CONTRACTS.md) và [09](09-TRACEABILITY-MATRIX.md).

## Baseline acquisition

URL `https://github.com/SkyCascade/SkyLearn.git`; branch `main`; commit `d57f57bd505447b59fdf82b16469494443cafe0c` (GitHub branch API). `git clone --depth 1` thất bại vì Git trong môi trường này trả `getaddrinfo() thread failed to start`; GitHub Download ZIP bị Brave chặn ở codeload. Theo yêu cầu tiếp theo, thư mục hiện tại là **snapshot tái tạo từ GitHub connector**, gồm toàn bộ 210 file ngoài `static/` (bao gồm 209 file văn bản và `media/default.png`), cộng 11 file static được chọn theo mã/template. Tổng 221 file gốc đã được đối chiếu Git blob SHA, 0 sai lệch; manifest ở `docs/UPSTREAM-SNAPSHOT-MANIFEST.json`. Còn 2195 file static không thuộc snapshot, phần lớn là tài nguyên vendor/font/icon. Nó **không phải Git clone**, không có `.git`, không đủ để chứng minh giao diện gốc chạy nguyên vẹn. Không thay đổi logic source.

## Yêu cầu và lệnh dự kiến

README yêu cầu Python >=3.8; pinned Django 4.0.8 và packages tại `requirements/base.txt`, `local.txt`, `production.txt`; tránh khẳng định chúng tương thích mọi Python mới. Cần Git network và Python interpreter thực trước khi chạy:

```powershell
git clone https://github.com/SkyCascade/SkyLearn.git SkyLearn-full
cd SkyLearn-full
git checkout d57f57bd505447b59fdf82b16469494443cafe0c
py -m venv .venv
.venv\\Scripts\\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
# Đặt EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, EMAIL_FROM_ADDRESS và SECRET_KEY trong .env
python manage.py check
python manage.py migrate
python manage.py createsuperuser
python manage.py test
python manage.py runserver
```

`config/settings.py` đọc email variables bắt buộc ngay khi import; `.env.example` có console backend mẫu. SQLite `db.sqlite3` tự tạo khi migrate; không commit dữ liệu thật. `scripts/` có tooling tạo sample data nhưng kiểm tra nội dung và chạy trên DB riêng trước; không tự chạy vào dữ liệu người dùng. Static production dùng WhiteNoise, `collectstatic` cần đầy đủ assets. Production requirements có gunicorn/storages/anymail; repo không cung cấp quy trình production hoàn chỉnh. `ALLOWED_HOSTS`, DEBUG, secret, email và payment keys cần cấu hình phù hợp nhưng thay đổi triển khai phải có phê duyệt.

## Kết quả kiểm tra thực tế

`git clone`: fail kết nối GitHub trong shell; `py --version`: “No installed Python found”; `python` là WindowsApps stub không khởi chạy. Vì thế chưa thể `pip install`, `manage.py check`, migrate, test hoặc xác minh UI. `templates/core/dashboard.html` tham chiếu `static/js/dashboard.js` nhưng file đó không có trong tree upstream. Các trường hợp chặn được liệt kê tại [12](12-CHANGE-CONTROL.md). Không gọi snapshot này là bản chạy được.

