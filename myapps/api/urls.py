from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter

from api.views import UsersViewSet, ProductViewSet, LessonViewSet, GroupViewSet

router_v1 = DefaultRouter()

router_v1.register('users', UsersViewSet, basename='users')
router_v1.register('products', ProductViewSet, basename='products')
router_v1.register('lessons', LessonViewSet, basename='lessons')
router_v1.register('groups', GroupViewSet, basename='groups')


urlpatterns = [
    path('', include(router_v1.urls)),
    re_path('auth/', include('djoser.urls.authtoken')),
]
