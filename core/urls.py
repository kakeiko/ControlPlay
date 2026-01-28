from django.urls import path
from .views import dashboard, view_profiles, view_profile, add_time, create_profile, view_device, view_devices, create_device, start_session, get_sessions, get_session, finish_session, liberar, get_Logs

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('profiles/', view_profiles, name='profiles'),
    path('profile/<int:id>', view_profile, name='profile'),
    path('criar_profile/', create_profile, name='create_profile'),
    path('addTime/<int:id>', add_time, name='add_time'),
    path('devices/', view_devices, name='devices'),
    path('device/<int:id>', view_device, name='device'),
    path('criar_device/', create_device, name='create_device'),
    path('criar_session/', start_session, name='create_session'),
    path('sessions/', get_sessions, name='sessions'),
    path('session/<int:id>', get_session, name='session'),
    path('finaliza/<int:id>', finish_session, name='finaliza'),
    path('liberar/<int:id>', liberar, name='liberar'),
    path('logs/', get_Logs, name='LOGS'),
]