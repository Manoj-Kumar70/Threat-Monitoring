from django.urls import path, include
from .views import RegisterView
from rest_framework.routers import DefaultRouter
from .views import EventViewSet, AlertViewSet, dashboard

router = DefaultRouter()
router.register(r'events', EventViewSet)
router.register(r'alerts', AlertViewSet)

urlpatterns = [
    path('dashboard/', dashboard),
    path('register/', RegisterView.as_view(), name='register'),
    path('', include(router.urls)),
]
