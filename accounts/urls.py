from django.urls import path
from .views import index, create, edit, delete
 
app_name='accounts'

urlpatterns = [
    path('', index, name='list'),
    path('create/', create, name='create'),
    path('edit/<str:id>', edit, name='edit'),
    path('delete/<str:id>', delete, name='delete'),
]
