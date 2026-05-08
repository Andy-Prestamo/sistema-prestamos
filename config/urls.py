from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views # Importante

urlpatterns = [
    path('admin/', admin.site.name),
    path('', include('prestamos.urls')),
    
    # Esta línea es la que falta para que reconozca /login/
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
]