"""
URL configuration for vehicleproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from userapp import views as user_views
from adminapp import views as admin_views
from miningapp import views as mining_views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    #user urls
    path("adminlogin/",user_views.user_admin,name="user_admin"),
    path("contact/",user_views.user_contact,name="user_contact"),
    path("",user_views.user_index,name="user_index"),
    path("mining/",user_views.user_mining,name="user_mining"),
    path("scan/",user_views.user_scan,name="user_scan"),
    path("security/",user_views.user_security,name="user_security"),
    path("dashboard/",user_views.user_dashboard,name="user_dashboard"),
    path("result/",user_views.user_result,name="user_result"),


    #mining urls
    path("mining-dashboard/",mining_views.mining_dashboard,name="mining_dashboard"),
    path("vehicle-activities/",mining_views.mining_allusers,name="vehicle_activity"),
    
    #admin views
    path("adminindex/",admin_views.admin_index,name="admin_index"),
    path("pendingusers/",admin_views.admin_addcompany,name="admin_addcompany"),
    path("manageusers/",admin_views.admin_managecompany,name="admin_managecompany"),
    path("adduser/",admin_views.admin_adduser,name="admin_adduser"),
    path("manageuser/",admin_views.admin_users,name="admin_users"),
    path("addvehicle/",admin_views.admin_addvehicle,name="admin_addvehicle"),
    path("managevehicles/",admin_views.admin_managevehicle,name="admin_managevehicle"),
    path("validvehicle/",admin_views.admin_validvehicle,name="admin_validvehicle"),
    path("delete-user/<int:user_id>",admin_views.delete_User,name="delete_User"),
    path("delete_security_user/<int:Security_id>",admin_views.delete_security_user,name="delete_security_user"),
    path("delete_vehicle/<int:vehicle_id>",admin_views.delete_vehicle,name="delete_vehicle"),
    path('admin-change-status/<int:id>',admin_views.Change_Status, name ='change_status'),



]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
   