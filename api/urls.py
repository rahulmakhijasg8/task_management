from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet, ReportView, RegisterView

router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='Task')

urlpatterns = [
    path('', include(router.urls)),
    path('report/', ReportView.as_view()),
    path('register/', RegisterView.as_view())
]