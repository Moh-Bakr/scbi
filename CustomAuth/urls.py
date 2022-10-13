from django.urls import path, include
from . import views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('register/', views.Register, name='register'),
    path('login/', views.Login, name='login'),
    path('password_reset/', include(
        'django_rest_passwordreset.urls', namespace='password_reset')),
    # path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]
