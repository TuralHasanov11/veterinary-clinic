from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView  
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Equipment
from .serializers import EquipmentSerializer
from .pagination import EquipmentPagination


@require_http_methods(["GET",'POST'])
@login_required
@permission_required('inventory.view_equipment', raise_exception=True)
def equipment(request):

    return render(request, 'inventory/equipment.html')


@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('inventory.view_equipment', raise_exception=True), name='dispatch')
class EquipmentList(ListAPIView):
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer
    pagination_class = EquipmentPagination
    filter_backends = [SearchFilter,OrderingFilter]
    search_fields = ['name', 'price', 'quantity']

  
    
@api_view(['POST'])
@login_required
@permission_required('inventory.add_equipment', raise_exception=True)
def equipmentCreate(request):
    
    serializer = EquipmentSerializer(data=request.data)
    
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        
        return Response({'message':'Təchizatın məlumatları əlavə edildi!', 'item':serializer.data}, status=status.HTTP_201_CREATED)
    

@api_view(['POST'])
@login_required
@permission_required('inventory.change_equipment', raise_exception=True)
def equipmentEdit(request,id):
    
    try:
        item = Equipment.objects.get(id=id)
    except Equipment.DoesNotExist:
        return Response({'message':'Təchizatın məlumatları tapılmadı!'}, status=status.HTTP_404_NOT_FOUND)
  
    serializer = EquipmentSerializer(item, data=request.data)

    if serializer.is_valid(raise_exception=True):
        serializer.save()

        return Response({'message':'Təchizatın məlumatları yeniləndi!', 'item':serializer.data})


@api_view(['POST'])
@login_required
@permission_required('inventory.delete_equipment', raise_exception=True)
def equipmentDelete(request, id):
    
    try:
        item = Equipment.objects.get(id=id)
    except Equipment.DoesNotExist:
        return Response({'message':'Təchizatın məlumatları tapılmadı!'}, status=status.HTTP_404_NOT_FOUND)
    
    if item.delete():
        return Response({'message':'Təchizatın məlumatları silindi!'})

    return Response({'message':'Təchizatın məlumatları silinmədi!'}, status=status.HTTP_400_BAD_REQUEST)




