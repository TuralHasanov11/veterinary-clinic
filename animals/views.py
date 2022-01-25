from django.http.response import Http404, JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect
from django.db.models import Q
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.contrib import messages
from django.utils.decorators import method_decorator

from django.utils.translation import activate
activate('az')

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import ListAPIView  
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import filters

from .models import Animal, MedicalExamination, Doctor, Feed
from .forms import CreateAnimalForm, UpdateAnimalForm
from .serializers import FeedSerializer, DoctorSerializer, MedicalExaminationSerializer
from .pagination import FeedPagination


@require_http_methods(["GET"])
@login_required
@permission_required('animals.view_animal', raise_exception=True)
def index(request):

    query = request.GET.get('q','')
    per_page=Animal.ANIMALS_PER_PAGE
    order_by = Animal.ANIMALS_ORDER_BY[-1]
    order_dir = '-'

    if request.GET.get('order_dir',0) and int(request.GET.get('order_dir',0)) == 1:
        order_dir = ''

    if request.GET.get('order_by','') in Animal.ANIMALS_ORDER_BY:
        order_by = request.GET.get('order_by')
    
    animals = getAnimalQuerySet(query)
    animals = animals.order_by(order_dir+order_by)

    page = request.GET.get('page',1)
    paginator = Paginator(animals, per_page) 
    
    try:
        animals = paginator.page(page)
    except PageNotAnInteger:
        animals = paginator.page(per_page)
    except EmptyPage:
        animals = paginator.page(paginator.num_pages)

    return render(request, 'animals/list.html', context={
        'animals':animals,
        'query':str(query),
        'order_by':order_by,
        'order_dir':order_dir,
        'per_page':per_page,
    })


@login_required
@require_http_methods(["GET", "POST"])
@permission_required('animals.add_animal', raise_exception=True)
def create(request):
    form = CreateAnimalForm(request.POST or None)
        
    if form.is_valid():
        data = form.save(commit=False)
        doctor = get_object_or_404(Doctor, id=form.cleaned_data['doctor'].id)
        examination = get_object_or_404(MedicalExamination, id=form.cleaned_data['examination'].id)
        data.doctor = doctor
        data.examination = examination

        data.save()
        
        messages.success(request, 'Heyvan məlumatları əlavə edildi!')
        return redirect('animals:list')

    return render(request, 'animals/create.html', context={
        'form':form
    })


@login_required
@require_http_methods(['GET'])
@permission_required('animals.view_animal', raise_exception=True)
def detail(request,id):

    try:
        animal = Animal.objects.prefetch_related('examination','doctor').get(id=id)
    except Animal.DoesNotExist:
        return Http404('Heyvan məlumatları tapılmadı!')

    return render(request, 'animals/detail.html', context={'animal':animal})


@login_required
@require_http_methods(['GET','POST'])
@permission_required('animals.change_animal', raise_exception=True)
def edit(request,id):

    animal = get_object_or_404(Animal, id=id)

    if request.POST:
        form = UpdateAnimalForm(request.POST or None, instance=animal)

        if form.is_valid():
            data = form.save(commit=False)
            doctor = get_object_or_404(Doctor, id=form.cleaned_data['doctor'].id)
            examination = get_object_or_404(MedicalExamination, id=form.cleaned_data['examination'].id)
            data.doctor = doctor
            data.examination = examination

            data.save()

            messages.success(request, 'Heyvan məlumatları yeniləndi!')
            return redirect('animals:edit', animal.id)

    form = UpdateAnimalForm(instance=animal)

    return render(request, 'animals/edit.html', context={
        'form':form, 'animal':animal
    })


@login_required
@require_http_methods(['POST'])
@permission_required('animals.delete_animal', raise_exception=True)
def delete(request, id):

    try:
        animal = Animal.objects.get(id=id)
    except Animal.DoesNotExist:
        return JsonResponse(data={'message':'Heyvan məlumatları tapılmadı!'}, status=status.HTTP_404_NOT_FOUND)

    if animal.delete():
        if request.GET.get('redirect',''):
            messages.success(request, 'Heyvan məlumatları silindi!')
            return redirect('animals:list')
        return JsonResponse(data={'message':'Heyvan məlumatları silindi!'})
    else:
        return JsonResponse(data={'message':'Heyvan məlumatları silinmədi!'}, status=status.HTTP_400_BAD_REQUEST)
    


def getAnimalQuerySet(query=None, company=None):
    queryset = Animal.objects
    queries = query.split(" ")
    for q in queries:
        queryset = queryset.filter(Q(name__icontains=q) | Q(owner__icontains=q) | Q(breed__icontains=q) | 
            Q(color__icontains=q) | Q(age__icontains=q) | Q(weight__icontains=q) | Q(phone__icontains=q) | Q(entry_date__icontains=q))
    
    queryset = queryset.distinct()

    return queryset


# DOCTORS
@require_http_methods(["GET"])
@login_required
def doctors(request):

    return render(request, 'animals/doctors.html')


class DoctorList(ListAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer

    
@api_view(['POST'])
@login_required
@permission_required('animals.add_doctor', raise_exception=True)
def doctorCreate(request):
    
    serializer = DoctorSerializer(data=request.data)
    
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        
        return Response({'message':'Həkimin məlumatları əlavə edildi!', 'doctor':serializer.data}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@login_required
@permission_required('animals.change_doctor', raise_exception=True)
def doctorEdit(request,id):
    
    try:
        doctor = Doctor.objects.get(id=id)
    except Doctor.DoesNotExist:
        return Response({'message':'Həkimin məlumatları tapılmadı!'}, status=status.HTTP_404_NOT_FOUND)
  
    serializer = DoctorSerializer(doctor, data=request.data)

    if serializer.is_valid(raise_exception=True):
        serializer.save()

        return Response({'message':'Həkimin məlumatları yeniləndi!', 'doctor':serializer.data})


@api_view(['POST'])
@login_required
@permission_required('animals.delete_doctor', raise_exception=True)
def doctorDelete(request, id):
    
    try:
        doctor = Doctor.objects.get(id=id)
    except Doctor.DoesNotExist:
        return Response({'message':'Həkimin məlumatları tapılmadı!'}, status=status.HTTP_404_NOT_FOUND)
    
    if doctor.delete():
        return Response({'message':'Həkimin məlumatları silindi!'})

    return Response({'message':'Həkimin məlumatları silinmədi!'}, status=status.HTTP_400_BAD_REQUEST)


# EXAMINATIONS
@require_http_methods(["GET"])
@login_required
def examinations(request):

    return render(request, 'animals/examinations.html')


class ExaminationList(ListAPIView):
    queryset = MedicalExamination.objects.all()
    serializer_class = MedicalExaminationSerializer

    
@api_view(['POST'])
@login_required
@permission_required('animals.add_medical_examination', raise_exception=True)
def examinationCreate(request):
    
    serializer = MedicalExaminationSerializer(data=request.data)
    
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        
        return Response({'message':'Müayinənin məlumatları əlavə edildi!', 'examination':serializer.data}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@login_required
@permission_required('animals.change_medical_examination', raise_exception=True)
def examinationEdit(request,id):
    
    try:
        examination = MedicalExamination.objects.get(id=id)
    except MedicalExamination.DoesNotExist:
        return Response({'message':'Müayinənin məlumatları tapılmadı!'}, status=status.HTTP_404_NOT_FOUND)
  
    serializer = MedicalExaminationSerializer(examination, data=request.data)

    if serializer.is_valid(raise_exception=True):
        serializer.save()

        return Response({'message':'Müayinənin məlumatları yeniləndi!', 'examination':serializer.data})


@api_view(['POST'])
@login_required
@permission_required('animals.delete_medical_examination', raise_exception=True)
def examinationDelete(request, id):
    
    try:
        examination = MedicalExamination.objects.get(id=id)
    except MedicalExamination.DoesNotExist:
        return Response({'message':'Müayinənin məlumatları tapılmadı!'}, status=status.HTTP_404_NOT_FOUND)
    
    if examination.delete():
        return Response({'message':'Müayinənin məlumatları silindi!'})

    return Response({'message':'Müayinənin məlumatları silinmədi!'}, status=status.HTTP_400_BAD_REQUEST)



# FEEDS
@require_http_methods(["GET"])
@login_required
def feeds(request):

    return render(request, 'animals/feeds.html')


@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('animals.view_feed', raise_exception=True), name='dispatch')
class FeedList(ListAPIView):
    queryset = Feed.objects.all()
    serializer_class = FeedSerializer
    pagination_class = FeedPagination
    filter_backends = [SearchFilter,OrderingFilter]
    search_fields = ['name', 'weight', 'quantity']

    
@api_view(['POST'])
@login_required
@permission_required('animals.add_feed', raise_exception=True)
def feedCreate(request):
    
    serializer = FeedSerializer(data=request.data)
    
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        
        return Response({'message':'Yemin məlumatları əlavə edildi!', 'feed':serializer.data}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@login_required
@permission_required('animals.change_feed', raise_exception=True)
def feedEdit(request,id):
    
    try:
        feed = Feed.objects.get(id=id)
    except Feed.DoesNotExist:
        return Response({'message':'Yemin məlumatları tapılmadı!'}, status=status.HTTP_404_NOT_FOUND)
  
    serializer = FeedSerializer(feed, data=request.data)

    if serializer.is_valid(raise_exception=True):
        serializer.save()

        return Response({'message':'Yemin məlumatları yeniləndi!', 'feed':serializer.data})


@api_view(['POST'])
@login_required
@permission_required('animals.delete_feed', raise_exception=True)
def feedDelete(request, id):
    
    try:
        company = Feed.objects.get(id=id)
    except Feed.DoesNotExist:
        return Response({'message':'Yemin məlumatları tapılmadı!'}, status=status.HTTP_404_NOT_FOUND)
    
    if company.delete():
        return Response({'message':'Yemin məlumatları silindi!'})

    return Response({'message':'Yemin məlumatları silinmədi!'}, status=status.HTTP_400_BAD_REQUEST)



