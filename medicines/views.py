from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView  
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Medicine, MedicineCompany
from .serializers import MedicineSerializer, MedicineCompanySerializer, MedicineCreateUpdateSerializer
from .pagination import MedicinePagination


@require_http_methods(["GET"])
@login_required
@permission_required('medicines.view_medicine', raise_exception=True)
def medicines(request):

    return render(request, 'medicines/medicines.html')


@require_http_methods(["GET"])
@login_required
@permission_required('medicines.view_medicine_company', raise_exception=True)
def companies(request):

    return render(request, 'medicines/companies.html')


@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('medicines.view_medicine', raise_exception=True), name='dispatch')
class MedicineList(ListAPIView):
    queryset = Medicine.objects.all()
    serializer_class = MedicineSerializer
    pagination_class = MedicinePagination
    filter_backends = [SearchFilter,OrderingFilter]
    search_fields = ['name', 'price', 'quantity','our_price','company__name']


@api_view(['POST'])
@login_required
@permission_required('medicines.add_medicine', raise_exception=True)
def create(request):
    
    serializer = MedicineCreateUpdateSerializer(data=request.data)
    
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        
        return Response({'message':'Dərmanın məlumatları əlavə edildi!', 'medicine':serializer.data}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@login_required
@permission_required('medicines.change_medicine', raise_exception=True)
def edit(request,id):
    
    try:
        medicine = Medicine.objects.get(id=id)
    except Medicine.DoesNotExist:
        return Response({'message':'Dərmanın məlumatları tapılmadı!'}, status=status.HTTP_404_NOT_FOUND)
  
    serializer = MedicineCreateUpdateSerializer(medicine, data=request.data)

    if serializer.is_valid(raise_exception=True):
        serializer.save()

        return Response({'message':'Dərmanın məlumatları yeniləndi!', 'medicine':serializer.data})


@api_view(['POST'])
@login_required
@permission_required('medicines.delete_medicine', raise_exception=True)
def delete(request, id):
    
    try:
        medicine = Medicine.objects.get(id=id)
    except Medicine.DoesNotExist:
        return Response({'message':'Dərmanın məlumatları tapılmadı!'}, status=status.HTTP_404_NOT_FOUND)
    
    if medicine.delete():
        return Response({'message':'Dərmanın məlumatları silindi!'})

    return Response({'message':'Dərmanın məlumatları silinmədi!'}, status=status.HTTP_400_BAD_REQUEST)



# COMPANY
@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('medicines.view_medicine_company', raise_exception=True), name='dispatch')
class MedicineCompanyList(ListAPIView):
    queryset = MedicineCompany.objects.all()
    serializer_class = MedicineCompanySerializer
    filter_backends = [OrderingFilter]


@api_view(['POST'])
@login_required
@permission_required('medicines.add_medicine_company', raise_exception=True)
def companyCreate(request):
    
    serializer = MedicineCompanySerializer(data=request.data)
    
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        
        return Response({'message':'Şirkətin məlumatları əlavə edildi!', 'company':serializer.data}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@login_required
@permission_required('medicines.change_medicine_company', raise_exception=True)
def companyEdit(request,id):
    
    try:
        company = MedicineCompany.objects.get(id=id)
    except MedicineCompany.DoesNotExist:
        return Response({'message':'Şirkətin məlumatları tapılmadı!'}, status=status.HTTP_404_NOT_FOUND)
  
    serializer = MedicineCompanySerializer(company, data=request.data)

    if serializer.is_valid(raise_exception=True):
        serializer.save()

        return Response({'message':'Şirkətin məlumatları yeniləndi!', 'company':serializer.data})


@api_view(['POST'])
@login_required
@permission_required('medicines.delete_medicine_company', raise_exception=True)
def companyDelete(request, id):
    
    try:
        company = MedicineCompany.objects.get(id=id)
    except MedicineCompany.DoesNotExist:
        return Response({'message':'Şirkətin məlumatları tapılmadı!'}, status=status.HTTP_404_NOT_FOUND)
    
    if company.delete():
        return Response({'message':'Şirkətin məlumatları silindi!'})

    return Response({'message':'Şirkətin məlumatları silinmədi!'}, status=status.HTTP_400_BAD_REQUEST)

