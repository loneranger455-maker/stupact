"""stupact URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from . import views
import dataforstupact.views as views2


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/',views.login,name="login"),
    path('',views.start),
    path('home/',views.home,name="home"),
    path('services/',views.services,name="servicestab"),
    path('signup/',views.signup,name="signup"),
    path('user/',views.user,name="userbio"),
    path('user/logout',views.logout,name="logout"),
    path('stumart',views.stumartfunc,name="stumart"),
    path('stumart/<str:tabvalue>',views.productmenu,name="productmenu"),
    path('stumart/order/<uuid:uniquevalue>',views.orderproduct,name="placeorder"),
    path('notification/',views.notification,name="notification"),
    path('notificationcount/',views.notificationcount,name="notificationcount"),
    path('updateinfo/',views.updateinfo,name="updateinfo"),
    path('changepassword/',views.changepassword,name="changepassword"), 
    path('deleteproduct',views.deleteproduct,name="deleteproduct"),
    path('stumart/search/cat?=<str:category>',views.searchbycategory,name="searchbycategory"),
    path('tutor/',views.tutor,name="tutor_intro"),
    path('tutor/dashboard',views.tutor_dashboard,name="dashboard"),
    path('verify/',views.verify,name="verify"),
    path('/stumart/productinfo/<uuid:uniquevalue>',views.productinfo,name="productinfo"),
    path('adminpanel',views2.adminstart),
    path('adminpanel/<str:menuvalue>',views2.adminpanel,name="adminpanel"),
    path('adminpanel/verify/<int:value>/<str:username>',views2.verifycontrol,name="verifycontrol"),
    path('adminpanel/order/<int:value>/<str:productid>',views2.ordercontrol,name="ordercontrol")
]
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
