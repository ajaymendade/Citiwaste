from django.contrib import admin
from django.urls import path
from dashboard import views
from django.conf import settings
from django.conf.urls.static import static


app_name = 'dashboard'

urlpatterns = [
    path("register/", views.register, name="register"),
    path("login/", views.login, name="login"),
    path("profile/", views.profile, name="profile"),
    
    
    #-----------------Admin------------------
    path("adminregister/", views.admin_register, name="adminregister"),
    path("admin-dashboard/", views.adminhome, name="adminhome"),
    path("admin-driver/", views.driverreg, name = "driverreg"),
    path("driverregistration/", views.registerdriver, name = "driverregistration"),
    
    #----------------Driver-------------------
    path("driver-dashboard/", views.driverhome, name="driverhome"),
    path("driverprofile/", views.driverprofile, name="driverprofile"),
    path("completedcomplaints/", views.completedcomplaints, name="completedcomplaints"),
    path('mapview/<int:complaint_id>/', views.mapview, name='mapview'),
    path('statuschange/<int:complaint_id>/', views.change_status, name='statuschange'),
    
    
    #--------------Citizen------------------
    path("dashboard/", views.citizen_dashboard, name = "citizendashboard"),
    path("citizenprofile/", views.citizenprofile, name="citizenprofile"),
    path("complaint/", views.complaint, name="complaint"),
] 
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)