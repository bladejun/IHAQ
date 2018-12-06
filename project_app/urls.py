"""ssido URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import url
 
urlpatterns = [
    path('', views.main),
    path('cc_test/', views.cc_test),
    url(r'^joinClass/.+$',views.joinClass),
    path('inputClass/', views.inputClass),
    path('main/', views.main),
    path('logout/', views.logout),
    path('login/', views.login),
    path('get_in_class_list/', views.get_in_class_list),
    #path('register/', views.register),
    #path('pdf_upload/', views.pdf_upload),
    #path('pdf/', views.pdf),

    path('updateChat/', views.updateChat),
    path('sendChat/', views.sendChat),
    path('ddabong/', views.ddabong),
    path('delete_msg/', views.delete_msg),
    path('create_class/', views.create_class),
    path('check_class/', views.check_class),
    path('check_login/', views.check_login),
    path('check_set_name/', views.check_set_name),
    path('save_memo/', views.save_memo),
    path('delete_user_list/', views.delte_user_list),
    path('delete_pdf/', views.delete_pdf),

    path('join/', views.join),
    path('check_id/', views.check_id),
    path('join/register_member_db/',views.main),

    path('password-change/', views.password_change),
    path('check_validation/', views.check_validation),
    path('password_change_success/', views.password_change_success),
    path('mypage/', views.mypage),
    path('upload/', views.upload_class),
    url(r'^password_validation_check/.+$',views.password_validation_check),
    url(r'^psw_changed_success/.+$',views.psw_changed_success),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)