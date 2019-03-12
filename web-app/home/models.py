from django.db import models
from django.contrib.auth.models import User


# Create your models here.
from django.urls import reverse         
class Order(models.Model):
    destination = models.CharField(max_length=200 )
    departure = models.CharField(max_length=200)
    aptime = models.DateTimeField()
    driver=models.ForeignKey('Driver',on_delete=models.SET_NULL,null=True,blank=True) 
    passenger=models.IntegerField()
    ORDER_STATUS = (
        ('r', 'Request'),
        ('s', 'Shared'),
        ('c', 'Confirmed'),
        ('f', 'Finished'),
    )
 
    status = models.CharField(
        max_length=1,
        choices=ORDER_STATUS,
        blank=True,
        default='r',
        help_text='order',
    )

    class Meta:
        ordering = ['-aptime']
            # Methods
        permissions = (
            ("confirm_order", "Can change order status"),
            ("change_order_info", "Can change order information"),
            ("create_order", "Can create"),
        )
    def get_absolute_url(self):
        """Returns the url to access a particular instance of MyModelName."""
        return reverse('order-detail', args=[str(self.id)])
    def get_edit_url(self):
        """Returns the url to access a particular instance of MyModelName."""
        return reverse('editorder', args=[str(self.id)])
    def __str__(self):
        """String for representing the Model object."""
        return self.destination

from django.urls import reverse
class Owner(models.Model):
    """A typical class defining a model, derived from the Model class."""

    # Fields
    phone = models.CharField(max_length=16)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    order = models.ManyToManyField(Order) 

    # Metadata
#    class Meta: 
#        ordering = ['-user.name']

    # Methods
    def get_absolute_url(self):
        """Returns the url to access a particular instance of MyModelName."""
        return reverse('owner-detail', args=[str(self.id)])
    
    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return self.user.username   
    
class Driver(models.Model):
    """Model representing a specific copy of a book (i.e. that can be borrowed from the library)."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)


#    order = models.ManyToManyField(Order, related_name = "order_driver")

    V_SIZE = (
        ('5', '5 passenger'),
        ('7', '7 passenger'),
    )

    size = models.CharField(
        max_length=1,
        choices=V_SIZE,
        blank=True,
        default='5',
        help_text='vehicle status',
    )

#    class Meta:
#        ordering = ['user.name']

    def get_absolute_url(self):
        """Returns the url to access a particular instance of MyModelName."""
        return reverse('driver-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return self.user.username
