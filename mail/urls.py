from django.urls import path
from . import views

app_name = 'mail'

urlpatterns = [
    path("mail", views.mail, name="mail"),

    path("mail/emails", views.compose, name="compose"),
    # Note that you shouldn't have slash at the end of the route if you're doing PUT
    path("mail/emails/<int:email_id>", views.email, name="email"),
    path("mail/emails/<str:mailbox>", views.mailbox, name="mailbox")

]

