"""lostandfound_django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path
from lostandfound import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('view/', views.IndexView.as_view(), name='view'),
    path('', views.home, name='index'),
    path('found', views.FoundView, name='found'),
    path('about/', views.about_us, name='about_us'),
    path('create/', views.create_item, name='create'),
    path('<int:pk>/edit/', views.update_item, name='edit'),
    path('<int:pk>/delete/', views.delete_item, name='delete'),
    path('<int:pk>/', views.item_detail, name='detail'),
    path('accounts/login/', views.my_login_view, name='login'),
    path('logout/', views.my_logout_view, name='logout'),
    path('search/', views.search_items, name='search'),
    path('registration/', views.my_registration_view, name='registration'),
    path('accounts/profile', views.profile, name='profile')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
