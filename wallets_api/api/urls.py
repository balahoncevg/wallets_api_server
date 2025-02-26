from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import WalletViewSet


app_name='api'


class NoTrailingSlashRouter(DefaultRouter):
    """Устанавливаем обращение без слеша на конце."""
    def __init__(self):
        super().__init__()
        self.trailing_slash = ''


api_v1 = NoTrailingSlashRouter()
api_v1.register(
    r'wallets', WalletViewSet,
    basename='wallets'
)

urlpatterns = [
    path('', include(api_v1.urls)),
]
