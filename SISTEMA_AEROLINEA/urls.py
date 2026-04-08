from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.contrib.admin import AdminSite

AdminSite.logout = lambda self, request, extra_context=None: auth_views.LogoutView.as_view(next_page='/')(request)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('AEROLINEA.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)