from django.urls import path
from ..views.views_v1 import UserViewSet



urlpatterns = [
    path('create-user/', UserViewSet.as_view({'post': 'create_user'}), name='create_user'),
    path('create-admin/', UserViewSet.as_view({'post': 'create_admin'}), name='create_admin'),
    path('update-user/<str:id>/', UserViewSet.as_view({'put': 'update_user'}), name='update_user'),
    path('update-my-profile/<str:id>/', UserViewSet.as_view({'put': 'update_my_profile'}), name='update_my_profile'),
    path('list-user/', UserViewSet.as_view({'get': 'user_list'}), name='user_list'),
    path('retrieve-user/<str:id>/', UserViewSet.as_view({'get': 'user_retrieve'}), name='user_retrieve')
] 