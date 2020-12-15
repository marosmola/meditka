from django.contrib import admin
from django.urls import path, include

# from gospel.api.urls import router

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('gospel.api.urls')),
]
