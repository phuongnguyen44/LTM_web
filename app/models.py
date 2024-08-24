from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


#Change forms register
class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields =['username','email','first_name','last_name','password1','password2']
    
class Category(models.Model):
    sub_category = models.ForeignKey('self',on_delete=models.CASCADE,related_name='sub_categories',null=True,blank=True)
    is_sub=models.BooleanField(default=False)
    name=models.CharField(max_length=200)
    slug=models.SlugField(max_length=200,unique=True)
    def __str__(self):
        return self.name
class Product(models.Model):
    name = models.CharField(max_length=200,null=True)
    price = models.FloatField()
    category = models.ManyToManyField(Category,related_name='product')
    image = models.ImageField(null=True,blank=True)
    detail=models.TextField(null=True,blank=True)

    def __str__(self):
        return self.name
    @property
    def ImageURL(self):
        try:
            url= self.image.url
        except:
            url='static/app/images/placeholder.png'
        return url
class Order(models.Model):
    customer = models.ForeignKey(User,on_delete=models.SET_NULL,blank=True,null=True)
    date_order= models.DateTimeField(auto_now_add=True)
    complete= models.BooleanField(default=False, null=True,blank=False)
    transaction_id = models.CharField(max_length=200,null=True)
    
    def __str__(self):
        return str(self.id)

class OrderItem(models.Model):
    order = models.ForeignKey(Order,on_delete=models.SET_NULL,blank=True,null=True)
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,blank=True,null=True)
    quantity = models.IntegerField(default=0,null=True,blank=True)
    date_added= models.DateTimeField(auto_now_add=True)

class ShippingAddress(models.Model):
    customer = models.ForeignKey(User,on_delete=models.SET_NULL,blank=True,null=True)
    order = models.ForeignKey(Order,on_delete=models.SET_NULL,blank=True,null=True)
    address = models.CharField(max_length=200,null=True)
    country = models.CharField(max_length=200,null=True)
    city = models.CharField(max_length=200,null=True)
    mobile = models.CharField(max_length=200,null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.address)
    



