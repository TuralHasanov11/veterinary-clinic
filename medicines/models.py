from django.db import models

class MedicineCompany(models.Model):
    name = models.CharField(max_length=191, null=False, blank=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    COMPANIES_PER_PAGE = 2
    COMPANIES_ORDER_BY = ('name')
    
    def __str__(self):
        return self.name


        
class Medicine(models.Model):
    name = models.CharField(max_length=191, null=False, blank=True, unique=True)
    single_quantity = models.IntegerField(null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True)
    price = models.FloatField(null=True, blank=True)
    our_price = models.FloatField(null=True, blank=True)
    company = models.ForeignKey(MedicineCompany, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    MEDICINES_PER_PAGE = 2
    MEDICINES_ORDER_BY = ('name','quantity','price','our_price','total_price')

    def __str__(self):
        return self.name
    
    @property
    def total_price(self):
        return self.price*self.quantity
    
    @property
    def our_total_price(self):
        return self.our_price*self.quantity
