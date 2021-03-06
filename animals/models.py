from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator 


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

    name = models.CharField(max_length=191, null=True, default='', blank=True)
    owner = models.CharField(max_length=191, null=False, blank=True)
    breed = models.PositiveIntegerField(null=True, default='',blank=True)
    age = models.PositiveIntegerField(null=True, default='', blank=True)
    weight = models.FloatField(null=True, default='', blank=True)
    color = models.IntegerField(null=True, default='',blank=True)
    entry_date = models.DateTimeField(null=True, default='', blank=True)
    phone = models.CharField(max_length=50, default='', null=True, blank=True)
    note = models.TextField(null=True, default='', blank=True)
    price = models.DecimalField(default=0, max_digits=9, decimal_places=2, blank=True)

    examination = models.ForeignKey(MedicalExamination, on_delete=models.SET_NULL,blank=True, null=True,default='')
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL,blank=True, null=True,default='')
   
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    COLORS = [('', 'R??ngi se??in'), (1, 'A??'), (2, 'Qara'), (3, 'Sar??'), (4, 'Boz'), (5, 'Qar??????q'), (6, 'Dig??r')]
    BREEDS = [('', 'N??v?? se??in'), (1, '??t'), (2, 'Pi??ik'), (3, 'Dov??an'), (4, 'Tutuqu??u'), (5, 'Hamster'), (6, 'Dig??r')]
    ANIMALS_PER_PAGE = 25
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
        if self.entry_date:
            return self.entry_date.date()
        return ''
    
    @property
    def entry_time(self):
        if self.entry_date:
            return self.entry_date.time()
        return ''


class Feed(models.Model):
    name = models.CharField(max_length=255, null=False, blank=True, unique=True)
    quantity = models.IntegerField(null=False, default=0,blank=True)
    weight = models.FloatField(null=False, default=0,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    FEEDS_PER_PAGE=20

    def __str__(self):
        return self.name
    
    @property
    def total_weight(self):
        if self.quantity and self.weight:
            return round(self.weight*self.quantity,2)
        return 0