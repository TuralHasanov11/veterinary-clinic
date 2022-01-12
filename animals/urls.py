from django.urls import path
from .views import (index, create, edit, delete, detail,
                    doctors, DoctorList, doctorCreate, doctorEdit, doctorDelete, 
                    examinations, ExaminationList, examinationCreate, examinationEdit, examinationDelete, 
                    FeedList, feedCreate, feedDelete, feedEdit, feeds,)

app_name='animals'

urlpatterns = [
    path('', index, name='list'),
    path('create/', create, name='create'),

    path('doctors/', doctors, name='doctors'),
    path('doctors/list', DoctorList.as_view(), name='doctor_list'),
    path('doctors/create', doctorCreate, name='doctor_create'),
    path('doctors/<str:id>', doctorEdit, name='doctor_edit'),
    path('doctors/<str:id>/delete', doctorDelete, name='doctor_delete'),

    path('examinations/', examinations, name='examinations'),
    path('examinations/list', ExaminationList.as_view(), name='examination_list'),
    path('examinations/create', examinationCreate, name='examination_create'),
    path('examinations/<str:id>', examinationEdit, name='examination_edit'),
    path('examinations/<str:id>/delete', examinationDelete, name='examination_delete'),

    path('feeds/', feeds, name='feeds'),
    path('feeds/list', FeedList.as_view(), name='feed_list'),
    path('feeds/create', feedCreate, name='feed_create'),
    path('feeds/<str:id>', feedEdit, name='feed_edit'),
    path('feeds/<str:id>/delete', feedDelete, name='feed_delete'),

    path('<str:id>', detail, name='detail'),
    path('<str:id>/edit', edit, name='edit'),
    path('<str:id>/delete', delete, name='delete'),
]
