from django.contrib import admin
from django.urls import include, path
from django.db import connection
from django.core.cache import cache
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenRefreshView
from apps.users.views import ActivateAccountView, LoginView, MeView, RegisterView
from apps.users.throttles import AuthRefreshThrottle
from core import admin as platform_admin  # noqa: F401


class HealthView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        db_ok = False
        cache_ok = False
        try:
            with connection.cursor() as c:
                c.execute('SELECT 1')
            db_ok = True
        except Exception:
            pass
        try:
            cache.set('healthcheck', '1', 5)
            cache_ok = cache.get('healthcheck') == '1'
        except Exception:
            pass

        status_code = 200 if (db_ok and cache_ok) else 503
        return Response({
            'status': 'ok' if status_code == 200 else 'degraded',
            'db': db_ok,
            'cache': cache_ok,
            'version': '2.0.0',
        }, status=status_code)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/health/', HealthView.as_view()),
    path('api/v1/auth/login/', LoginView.as_view()),
    path('api/v1/auth/register/', RegisterView.as_view()),
    path('api/v1/auth/activate/', ActivateAccountView.as_view()),
    path('api/v1/auth/refresh/', TokenRefreshView.as_view(throttle_classes=[AuthRefreshThrottle])),
    path('api/v1/auth/me/', MeView.as_view()),
    path('api/v1/users/', include('apps.users.urls')),
    path('api/v1/referral/', include('apps.referral.urls')),
    path('api/v1/tree/', include('apps.tree.urls')),
    path('api/v1/catalog/', include('apps.catalog.urls')),
    path('api/v1/forum/', include('apps.forum.urls')),
    path('api/v1/wallet/', include('apps.wallet.urls')),
]
