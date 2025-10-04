from django.urls import path, include

urlpatterns = [
    path("api/", include("ChatApp.urls")),
]