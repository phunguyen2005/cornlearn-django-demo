from django.contrib import admin
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views import defaults as default_views
from django.conf.urls.i18n import i18n_patterns
from django.views.i18n import JavaScriptCatalog

admin.site.site_header = "CornLearn Admin"
admin.site.site_title = "CornLearn Portal"
admin.site.index_title = "Quản trị hệ thống CornLearn"


def terms_view(request):
    modal_html = render_to_string("term.html", request=request)
    shell_html = render_to_string(
        "registration/registration_base.html",
        {"title": "Điều khoản dịch vụ - CornLearn"},
        request=request,
    )
    card_html = (
        '<div class="mb-3">'
        '<h2 class="fw-bold mb-2" style="font-size: 1.5rem; color: #131B2E;">Điều khoản dịch vụ CornLearn</h2>'
        '<p class="text-muted small mb-3">Quy định sử dụng Hệ thống Quản lý Học tập và Đào tạo CornLearn.</p>'
        "</div>"
        + modal_html
    )
    return HttpResponse(
        shell_html.replace(
            '<div class="auth-form-card">',
            '<div class="auth-form-card">' + card_html,
            1,
        )
    )


def privacy_view(request):
    modal_html = render_to_string("privacy.html", request=request)
    shell_html = render_to_string(
        "registration/registration_base.html",
        {"title": "Chính sách bảo mật - CornLearn"},
        request=request,
    )
    card_html = (
        '<div class="mb-3">'
        '<h2 class="fw-bold mb-2" style="font-size: 1.5rem; color: #131B2E;">Chính sách bảo mật CornLearn</h2>'
        '<p class="text-muted small mb-3">Cam kết bảo vệ dữ liệu cá nhân và hồ sơ học vụ trên hệ thống CornLearn.</p>'
        "</div>"
        + modal_html
    )
    return HttpResponse(
        shell_html.replace(
            '<div class="auth-form-card">',
            '<div class="auth-form-card">' + card_html,
            1,
        )
    )


urlpatterns = [
    path("admin/", admin.site.urls),
    path("i18n/", include("django.conf.urls.i18n")),
]

urlpatterns += i18n_patterns(
    path("jsi18n/", JavaScriptCatalog.as_view(), name="javascript-catalog"),
    path("terms/", terms_view, name="terms"),
    path("term/", terms_view, name="term"),
    path("privacy/", privacy_view, name="privacy"),
    path("", include("core.urls")),
    path("jet/", include("jet.urls", "jet")),  # Django JET URLS
    path(
        "jet/dashboard/", include("jet.dashboard.urls", "jet-dashboard")
    ),  # Django JET dashboard URLS
    path("accounts/", include("accounts.urls")),
    path("programs/", include("course.urls")),
    path("result/", include("result.urls")),
    path("search/", include("search.urls")),
    path("quiz/", include("quiz.urls")),
    path("payments/", include("payments.urls")),
)


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
