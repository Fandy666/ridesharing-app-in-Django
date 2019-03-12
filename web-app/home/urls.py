from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    path('owners/', views.OwnerListView.as_view(), name='owners'),
    path('orders/', views.OrderListView.as_view(), name='orders'),
    path('orders/<int:pk>', views.OrderDetailView.as_view(), name='order-detail'),
    path('owners/<int:pk>', views.OwnerDetailView.as_view(), name='owner-detail'),
    path('driver/<int:pk>', views.DriverDetailView.as_view(), name='driver-detail'),
    path('editorders/<int:pk>', views.OrderUpdateView.as_view(), name='editorder'),

]

from django.conf.urls import url
urlpatterns += [ 
    path('login/', views.dlogin, name='login'),
    path('register/', views.dregist,name='register'),
    path('logout/', views.dlogout, name='logout'),
    path('createorder/', views.create_order, name='createrorder'),
    path('registerdriver/', views.registdriver,name='registerdriver'),
    path('edituser/', views.edit_user,name='edituser'),
    
    path('sharesearchorder/', views.share_search_order, name='sharesearchrorder'),
    path('driversearchorder/', views.driver_search_order, name='driversearchrorder'),
]

urlpatterns += [
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='home/password_reset_form.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='home/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='home/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='home/password_reset_complete.html'), name='password_reset_complete'),
]