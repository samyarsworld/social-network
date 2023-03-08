
from django.contrib import admin
from django.urls import include, path
from django.shortcuts import redirect


urlpatterns = [
    path("", lambda request: redirect('network/', permanent=True)),
    path("admin/", admin.site.urls),
    path("network/", include("network.urls")),
    path("mail/", include("mail.urls")),
    path('auction/', include("auction.urls"))
]


