from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView




urlpatterns = [
    path("",views.register, name="register"),
    path('UNDEF_Application-result', views.first, name='firsturl'),
     path('login/',views.login_view, name='login'),
     path('dashboard/',views.dashboard, name='dashboard'),
    path('picture_upload', views.register2, name='register2'),
    path('notifications/', views.user_notifications, name='notifications'),

    path('card/lock/<int:card_id>/', views.lock_card, name='lock_card'),
    path('card/unlock/<int:card_id>/', views.unlock_card, name='unlock_card'),
    path('deposit/', views.deposit_view, name='deposit'),
    path('profile/', views.profile_view, name='profile'),
    path('settings/', views.settings_view, name='settings'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('transfer/', views.transfer_money, name='transfer'),
    path('transactions/', views.transaction_history, name='transactions'),
    path('paybill/', views.pay_bill, name='paybill'),
    
    path("mobiledeposit", views.mobiledepo, name="mobiledeposit")






]