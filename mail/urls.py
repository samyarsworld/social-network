from django.urls import path
from . import views

app_name = 'mail'

urlpatterns = [
    path("", views.mail, name="mail"),

    path("emails", views.compose, name="compose"),
    # Note that you shouldn't have slash at the end of the route if you're doing PUT
    path("emails/<int:email_id>", views.email, name="email"),
    path("emails/<str:mailbox>", views.mailbox, name="mailbox")

]

