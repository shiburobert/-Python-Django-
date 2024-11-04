from django.db import models
from django.contrib.auth.models import User
import datetime
import os
def getFileName(request,filename):
    now_time=datetime.datetime.now().strftime("%Y%m%d%H:%M:%S")
    new_filename="%s%s"%(now_time,filename)
    return os.path.join('uploads/',new_filename)

class Catagory(models.Model):
    name=models.CharField(max_length=150,null=False,blank=False)
    image=models.ImageField(upload_to=getFileName,null=True,blank=True)
    description=models.TextField(max_length=500,null=False,blank=False)
    status=models.BooleanField(default=False,help_text="0-shows,1-Hidden")
    trending=models.BooleanField(default=False,help_text="0-default,1-trending")
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self) :
         return self.name
    
class Product(models.Model):
    Catagory=models.ForeignKey(Catagory,on_delete=models.CASCADE)
    name=models.CharField(max_length=150,null=False,blank=False)
    vendors=models.CharField(max_length=150,null=False,blank=False)
    product_image=models.ImageField(upload_to=getFileName,null=True,blank=True)
    quantity=models.IntegerField(null=False,blank=False)
    original_price=models.FloatField(null=False,blank=False)
    selling_price=models.FloatField(null=False,blank=False) 
    description=models.TextField(max_length=500,null=False,blank=False)
    status=models.BooleanField(default=False,help_text="0-shows,1-Hidden")
    trending=models.BooleanField(default=False,help_text="0-default,1-trending")
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self) :
         return self.name


class Cart(models.Model):
    user=models.ForeignKey (User,on_delete=models.CASCADE)
    product=models.ForeignKey (Product,on_delete=models.CASCADE)
    product_qty=models.IntegerField(null=False, blank=False)
    created_at=models.DateTimeField(auto_now_add=True)

    @property
    def total_cost(self):
        return self.product_qty*self.product.selling_price
    

# class Favourite(models.Model):
#     user=models.ForeignKey(User,on_delete=models.CASCADE)
#     Product=models.ForeignKey(Product,on_delete=models.CASCADE)
#     created_at=models.DateTimeField(auto_now_add=True)

from django.db import models
from django.contrib.auth.models import User

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
    ]
    
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_qty = models.IntegerField(null=False, blank=False)
    total_price = models.FloatField(null=False, blank=False)
    full_name = models.CharField(max_length=150, null=False, blank=False)
    email = models.EmailField(max_length=150, null=False, blank=False)
    shipping_address = models.TextField(null=False, blank=False)
    payment_method = models.CharField(max_length=50, null=False, blank=False)
    ordered_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"Order {self.id} - {self.product.name} by {self.user.username}"



# class Contactmessage(models.Model):
#     name = models.CharField(max_length=50)
#     email = models.EmailField(unique=True)
#     message = models.TextField()

#     def _str_(self):
#         return self.name

from django.db import models

class ContactMessage(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name}"
