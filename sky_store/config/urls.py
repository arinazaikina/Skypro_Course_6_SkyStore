from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app_catalog.urls', namespace='app_catalog'))
]

urlpatterns += staticfiles_urlpatterns()
