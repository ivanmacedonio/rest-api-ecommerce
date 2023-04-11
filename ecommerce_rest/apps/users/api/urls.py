from django.urls import path
from apps.users.api.api import userApiView, user_detail_view

urlpatterns = [
    
    path('usuario/' ,userApiView, name='usuario'),
    path('usuario/<int:pk>/', user_detail_view, name='usuario_detail_api_view'),

]

