from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app_catalog.urls', namespace='app_catalog')),
    path('', include('app_blog.urls', namespace='app_blog')),
    path('', include('app_newsletter.urls', namespace='app_newsletter')),
    path('user/', include('app_user.urls', namespace='app_user'))
]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
