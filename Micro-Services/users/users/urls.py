from django.urls import path
from . import views
from . import consumers
from .api import UpdateSessionAPIView, RemoveChannelFromSessionAPIView

urlpatterns = [
    path('register/', views.register_view, name='register_view'),
    path('login/', views.login_view, name='login_view'),
    path('logout/', views.logout_view, name='logout_view'),
    path('profile/', views.user_profile_view, name='user_profile_view'),
    path('remove_channel_name_from_session', consumers.remove_channel_name_from_session),
    path('update-session/', UpdateSessionAPIView.as_view(), name='update-session'),
    path('remove_channel_from_session/', RemoveChannelFromSessionAPIView.as_view(), name='remove_channel_from_session'),
    path('update_user_session_id_api/', RemoveChannelFromSessionAPIView.as_view(), name='update_user_session_id_api'),
]
