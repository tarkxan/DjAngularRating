
from django.contrib import admin
from django.urls import include, path
from rover_app import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.csv_file_upload, name = 'csv_file_upload'),
    path('sitters/', include('rover_app.urls')),
]
