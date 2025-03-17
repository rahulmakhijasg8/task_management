from rest_framework import viewsets, status
from .models import Task
from .serializers import TaskSerializer, UserSerializer, SuperUserTaskSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
import concurrent.futures
from rest_framework.views import APIView
from django.core.cache import cache
from .tasks import send_notification
from channels.layers import get_channel_layer
from rest_framework.throttling import UserRateThrottle


class TaskViewSet(viewsets.ModelViewSet):
    throttle_classes = [UserRateThrottle]
    serializer_class = TaskSerializer
    filterset_fields = ['priority', 'status','due_date']

    def get_serializer_class(self):
        if self.request.user.is_superuser:
            return SuperUserTaskSerializer
        return TaskSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Task.objects.all()
        return Task.objects.filter(assigned_to=self.request.user)
    
    def list(self, request, *args, **kwargs):
        cache_key = f'tasks_list_{request.user.id}'
        cached_data = cache.get(cache_key)
        
        if cached_data:
            return Response(cached_data)
        
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        tasks_data = serializer.data
        cache.set(cache_key, tasks_data, timeout=60)
        
        return Response(tasks_data)

    def perform_create(self, serializer):
        serializer.save(assigned_to=self.request.user)
        print(self.request.user.email,serializer.data['id'],serializer.data['title'],'assigned')
        send_notification.delay(
    self.request.user.email,
    serializer.data['id'],
    serializer.data['title'],
    'assigned'
)
        channel_layer = get_channel_layer()
        task_data = {
        'id': serializer.data['id'],
        'title': serializer.data['title'],
        'status': serializer.data['status'],
        'assigned_to': self.request.user.email,
    }
        channel_layer.group_send(
            f"task_task_updates",  # Group name
            {
                'type': 'task_update',
                'task_data': task_data,
            }
        )
        cache.delete(f'tasks_list_{self.request.user.id}')

    def perform_update(self, serializer):
        cache.delete(f'tasks_list_{self.request.user.id}')
        channel_layer = get_channel_layer()
        task_data = {
        'id': serializer.data['id'],
        'title': serializer.data['title'],
        'status': serializer.data['status'],
        'assigned_to': serializer.data['assigned_to'].username,
    }
        channel_layer.group_send(
            f"task_task_updates",  # Group name
            {
                'type': 'task_update',
                'task_data': task_data,
            }
        )
        return super().perform_update(serializer)
    
    def perform_destroy(self, instance):
        cache.delete(f'tasks_list_{self.request.user.id}')
        return super().perform_destroy(instance)


class RegisterView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def generate_report(tasks):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(process_report, tasks)
        return future.result()

def process_report(tasks):
    completed = tasks.filter(status='Completed').count()
    pending = tasks.filter(status='Pending').count()
    high_priority = tasks.filter(priority='High').count()
    
    return {
        'completed': completed,
        'pending': pending,
        'high_priority': high_priority
    }


class ReportView(APIView):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            tasks = Task.objects.all()
            report = generate_report(tasks)
            return Response(report, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_401_UNAUTHORIZED)