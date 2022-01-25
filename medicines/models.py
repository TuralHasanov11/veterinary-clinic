from django.db import models

class MedicineCompany(models.Model):
    name = models.CharField(max_length=191, null=False, blank=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name


        
class Medicine(models.Model):
    name = models.CharField(max_length=191, null=False, blank=True, unique=True)
    single_quantity = models.IntegerField(null=True, default=0,blank=True)
    quantity = models.IntegerField(null=True, default=0,blank=True)
    price = models.FloatField(null=True, default=0,blank=True)
    our_price = models.FloatField(null=True, default=0,blank=True)
    company = models.ForeignKey(MedicineCompany, on_delete=models.SET_NULL,blank=True, null=True,default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    MEDICINES_PER_PAGE = 25
    MEDICINES_ORDER_BY = ('name',)

    def __str__(self):
        return self.name
    
    @property
    def total_price(self):
        if self.price and self.quantity:
            return self.price*self.quantity
        return 0
    
    @property
    def our_total_price(self):
        if self.our_price and self.quantity:
            return self.our_price*self.quantity
        return 0
