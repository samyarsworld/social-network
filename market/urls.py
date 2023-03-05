from django.urls import path
from . import views
from django.contrib.auth.views import PasswordResetView, PasswordChangeDoneView, PasswordResetConfirmView, PasswordResetCompleteView

app_name = 'market'

urlpatterns = [
    path('', views.home, name='home'),

    path('products', views.products, name='products'),
    path('customer-detail/<int:id>', views.customerDetail, name='customer'),
    path('order-create/<int:id>', views.createOrder, name='create_order'),
    path('order-update/<int:id>', views.updateOrder, name='update_order'),
    path('order-delete/<int:id>', views.deleteOrder, name='delete_order'),

    path('reset_password/', PasswordResetView.as_view(template_name='market/password_reset.html'), name='password_reset'),
    path('reset_password_sent/', PasswordChangeDoneView.as_view(template_name='market/password_reset_sent.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='market/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset_password_complete/', PasswordResetCompleteView.as_view(template_name='market/password_reset_complete.html'), name='password_reset_complete')
]