from django.urls import path
from .views import equipmentCreate, equipmentEdit, equipmentDelete, equipment, EquipmentList

app_name='inventory'

urlpatterns = [
    path('equipment/', equipment, name='equipment'),
    path('equipment/list', EquipmentList.as_view(), name='equipment_list'),
    path('equipment/create', equipmentCreate, name='equipment_create'),
    path('equipment/<str:id>', equipmentEdit, name='equipment_edit'),
    path('equipment/<str:id>/delete', equipmentDelete, name='equipment_delete'),

]
