from django.contrib import admin
from django.conf import settings
from django.urls import path, include

admin.site.site_header = settings.ADMIN_SITE_HEADER

urlpatterns = [
    path('candidate/', include('candidate.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
]
