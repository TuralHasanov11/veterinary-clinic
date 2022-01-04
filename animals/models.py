from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator 
from accounts.models import Account
import datetime
from datetime import datetime

class Doctor(models.Model):
    name = models.CharField(max_length=191, null=False, blank=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name


class MedicalExamination(models.Model):
    name = models.CharField(max_length=191, null=False, blank=True, unique=True)
    min_price = models.FloatField(null=False, blank=True)
    max_price = models.FloatField(null=False, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

    @property
    def price(self):
        if self.min_price == self.max_price:
            return self.min_price
        return str(self.min_price)+'-'+str(self.max_price)


class Animal(models.Model):

    name = models.CharField(max_length=191, null=False, blank=True)
    owner = models.CharField(max_length=191, null=False, blank=True)
    breed = models.PositiveIntegerField(null=False,blank=True)
    age = models.PositiveIntegerField(null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(100)])
    weight = models.FloatField(null=False, blank=True, validators=[MinValueValidator(0), MaxValueValidator(100)])
    color = models.IntegerField(null=True,blank=True)
    entry_date = models.DateTimeField(null=False, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    note = models.TextField(null=True, blank=True)

    examination = models.ForeignKey(MedicalExamination, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
   
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    COLORS = [('', 'Rəngi seçin'), (1, 'Ağ'), (2, 'Qara'), (3, 'Sarı'), (4, 'Boz'), (5, 'Qarışıq'), (6, 'Digər')]
    BREEDS = [('', 'Növü seçin'), (1, 'İt'), (2, 'Pişik'), (3, 'Dovşan'), (4, 'Tutuquşu'), (5, 'Hamster'), (6, 'Digər')]
    ANIMALS_PER_PAGE = 20
    ANIMALS_ORDER_BY = ('name','owner','entry_date', 'created_at')

    def __str__(self):
        return self.name

    @property
    def breed_name(self):
        for b in Animal.BREEDS:
            if b[0] == self.breed:
                return b[1]
        return '' 
        
    @property
    def color_name(self):
        for b in Animal.COLORS:
            if b[0] == self.color:
                return b[1]
        return '' 
    
    @property
    def entry_day(self):
        return self.entry_date.date()
    
    @property
    def entry_time(self):
        return self.entry_date.time()


class Feed(models.Model):
    name = models.CharField(max_length=255, null=False, blank=True, unique=True)
    quantity = models.IntegerField()
    weight = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    FEEDS_PER_PAGE=2

    def __str__(self):
        return self.name
    
    @property
    def total_weight(self):
        return round(self.weight*self.quantity,2)