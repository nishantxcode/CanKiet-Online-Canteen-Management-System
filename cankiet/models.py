from django.db import models
from django.contrib.auth.hashers import make_password
from django.utils.timezone import now
# Create your models here.

class User(models.Model):
    branches=[
        ('Mca','MCA'),
        ('Bph','Btech Pharmacy'),
        ('Bcse','Btech CSE'),
        ('Bit','Btech IT'),
        ('Bece','Btech ECE'),
        ('Mba','MBA'),
    ]

    u_id=models.CharField(max_length=12,primary_key=True)
    name=models.CharField(max_length=30)
    phone=models.CharField(max_length=10)
    password=models.CharField(max_length=20)
    branch=models.CharField(max_length=4,choices=branches)

    def save(self, *args, **kwargs):
        # Hash the password only if it is not already hashed
        if not self.password.startswith('pbkdf2_'):  # Check if password is already hashed
            self.password = make_password(self.password)
        super(User, self).save(*args, **kwargs)

    def __str__(self):
        return self.u_id

class Items(models.Model):
    i_no=models.CharField(max_length=12,primary_key=True)
    item=models.CharField(max_length=20)
    i_image=models.ImageField(upload_to='images/',blank=True)
    price=models.IntegerField()
    c_no=models.CharField(max_length=12)
    availability=models.CharField(max_length=1)

    def __str__(self):
        return self.item

class Canteen(models.Model):
    c_no=models.CharField(max_length=2,primary_key=True,)
    c_name=models.CharField(max_length=20)

    def __str__(self):
        return f"{self.c_name}  {self.c_no}"
    
class Order(models.Model):

    st=[
        ('Rejected','rejected'),
        ('In Progress','in-progress'),
        ('Compeleted','completed'),
    ]

    razorpay_order_id = models.CharField(max_length=100, blank=True, null=True)
    payment_id = models.CharField(max_length=100, blank=True, null=True)
    payment_signature = models.CharField(max_length=100, blank=True, null=True)
    is_paid = models.BooleanField(default=False)
    o_no = models.CharField(max_length=30)  # Auto-incrementing primary key
    o_date = models.DateTimeField(default=now)  # Automatically stores current date and time
    # u_id = models.ForeignKey(User, on_delete=models.CASCADE)  # Foreign key to User table
    c_no = models.ForeignKey(Canteen, on_delete=models.CASCADE)  # Foreign key to Canteen table
    item = models.ForeignKey(Items, on_delete=models.CASCADE)  # Single-valued attribute (ForeignKey to Item)
    quantity = models.IntegerField(default=1)  # Quantity of the item in the order
    total_amount = models.IntegerField(default=0)  # Store the total amount
    status=models.CharField(max_length=11,choices=st,default='In Progress')

    def save(self, *args, **kwargs):
        # Automatically calculate the total_amount before saving
        self.total_amount = self.item.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.razorpay_order_id} ---- {self.item.item} ({self.quantity} pcs) - Total: ₹{self.total_amount} ----- paid: {self.is_paid} ----- {self.o_date} ----- {self.status}"