from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static

from API.views import (
    PredictionViewSet,
    UserViewSet,
    signup_view,
    login_view,
    logout_view,
    check_auth_view,
    get_csrf
)

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')
router.register(r'cancer', PredictionViewSet, basename='cancer')

urlpatterns = [
    path('admin/', admin.site.urls),

    # Authentication Endpoints
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('check-auth/', check_auth_view, name='check_auth'),

    # DRF API Routes
    path('api/', include(router.urls)),

    # DRF Session Login (Browsable API)
    path('api-auth/', include('rest_framework.urls')),
    
    path('csrf/', get_csrf),
]

# Serve media files
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)