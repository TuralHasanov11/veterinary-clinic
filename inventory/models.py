from django.db import models

class Equipment(models.Model):
    name = models.CharField(max_length=255, null=False, blank=True, unique=True)
    quantity = models.IntegerField(null=False, blank=True,)
    price = models.FloatField(null=False, blank=True,)
    note = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    EQUIPMENT_PER_PAGE = 2
    EQUIPMENT_ORDER_BY = ('name','quantity','price')
    
    def __str__(self):
        return self.name

    @property
    def total_price(self):
        return round(self.price*self.quantity,2)


# class Device(models.Model):
#     name = models.CharField(max_length=191, null=False, blank=True, unique=True)
#     quantity = models.IntegerField()
#     price = models.FloatField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
    
#     TYPES = [('1', 'First'), ('2', 'Second')]

#     def __str__(self):
#         return self.name

#     def total_price(self):
#         return self.price*self.quantity