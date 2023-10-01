from django.urls import path
from . import views
from django.contrib import admin


urlpatterns = [
     path('', views.index, name="index"),
     path('login/',  views.login_user, name="login"),
     path('logout', views.logout, name="logout"),
     path('forgot-password/', views.pwd_reset, name='forgot'),
     path('resetpassword/<uidb64>/<token>', views.forgot_password_validation, name='forgot_password_validation'),
     path('resetpassword/', views.reset_password, name='pwdreset'),
     path('password_reset_confirm/', views.password_reset_confirmation, name='confirmresetpwd'),
     path('edit_profile', views.edit_profile, name='edit'),
     path('movie_description', views.movie_description, name='details'),
     path('show_time', views.show_time, name='show_time'),
     path('ticketcount', views.ticketcount, name='ticketcount'),
     path('registration', views.registration, name="registration"),
     path('regisconfirmation/<uidb64>/<token>', views.regisconfirmation, name='regisconfirmation'),
     path('edit_card', views.edit_card, name='editcard'),
     path('edit_password', views.edit_password, name='editpassword'),
     path('checkout', views.checkout, name='checkout'),
     path('confirmPayment', views.confirmPayment, name='confirmPayment'),
     path('bookingConfirmed', views.bookingConfirmed, name='bookingConfirmed'),
     path('seatselect/', views.seats, name='seats'),
     path('orderconfirmation/<order>/', views.orderconfirmation, name='orderconfirmation'),
     path('summary', views.summary, name='summary'),
     path('bookmovie/', views.book_movie, name='bookmovie'),
     path('base', views.base, name='base'),
     path('accountSuccess/',views.account_success, name='accountSuccess'),
     path('accountVerify/',views.account_verify, name='accountVerify'),
     path('accountNotVerified',views.account_notverified, name='accountNotVerified'),
     path('orderHistory/',views.order_history,name='history'),
     path('admin/', admin.site.urls)
]
