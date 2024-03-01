"""
URL configuration for ERINFABRICS project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from Website import urls as WebUrls
from Admin import urls as AdminUrls
from Admin import views as AdminViews

urlpatterns = [
    path('django-admin/', admin.site.urls),
    # path('login/', AdminViews.admin_login),
    path('create_new_account/', AdminViews.create_new_account, name='create_new_account'),
    path('login/', AdminViews.login_account, name='login_account'),
    path("accounts/", include("allauth.urls")), # new

    path('logout/', AdminViews.logout, name="logout"),
    path('', include(WebUrls)),
    path('admin/', include(AdminUrls)),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
