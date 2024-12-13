from django.db import models
from django.contrib.auth.models import AbstractUser
from core.managers import CustomUserManager
from core.utils import BaseModel
import uuid
from django.utils.text import slugify
from django.db.models import Avg


class CustomUser(AbstractUser):
    STATUS_CHOICES = [
        ('Admin', 'Admin'),
        ('Customer', 'Customer'),
    ]
    
    username = models.CharField(max_length=100,unique=True)
    email = models.EmailField(unique=True,null=True,blank=True)
    user_type = models.CharField(max_length=25,choices=STATUS_CHOICES,default="Admin")
    status = models.CharField(
        max_length=20,
        choices=[
            ('Active', 'Active'),
            ('Inactive', 'Inactive'),
            ('Deleted', 'Deleted')
        ],
        default='Active'
    )

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()
    
    
class Product(BaseModel):
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    average_rating = models.FloatField(default=0)
    image = models.FileField(upload_to='product')
    color = models.CharField(max_length=30,null=True,blank=True)
    size = models.CharField(max_length=30,null=True,blank=True)
    slug = models.CharField(max_length=30,null=True,blank=True,unique=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            unique_id = uuid.uuid4().hex[:8]
            self.slug = f"{base_slug}-{unique_id}"
        
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    

class Cart(BaseModel):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    
    @staticmethod
    def get_user_cart_total(user):
        cart_items = Cart.objects.filter(user=user)
        total_amount = sum(item.product.price * item.quantity for item in cart_items)
        return total_amount
    
    
    def __str__(self):
        return f'{self.user.username}-{self.product.title}'
    
    
class Address(BaseModel):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='address')
    street = models.CharField(max_length=955)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pin_code = models.CharField(max_length=10)
    country = models.CharField(max_length=100)
    phone_no = models.CharField(max_length=12)
    
    def __str__(self):
        return self.user.username
    
    
class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
    ]
    order_id = models.CharField(max_length=10, unique=True, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    address = models.TextField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    def save(self, *args, **kwargs):
        if not self.order_id:
            last_order = Order.objects.order_by('id').last()
            if last_order:
                last_id = int(last_order.order_id[3:])  
                new_id = f"ORD{last_id + 1:03}"  
            else:
                new_id = "ORD001"
            self.order_id = new_id
        super(Order, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.order_id} - {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('product', 'user')

    def __str__(self):
        return f"Review by {self.user.username} for {self.product.title}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.update_product_rating()
    
    def update_product_rating(self):
        average_rating = Review.objects.filter(product=self.product).aggregate(Avg('rating'))['rating__avg'] or 0
        self.product.average_rating = round(average_rating, 2)
        self.product.save()