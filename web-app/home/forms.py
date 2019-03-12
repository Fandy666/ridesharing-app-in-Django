from django import forms
from django.contrib.auth.models import User
from django.core import validators
from django.utils.translation import ugettext as _
import re
from .models import Owner,Driver,Order  
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

class RegistrationForm(forms.Form):   
  username = forms.CharField(label='Username:', max_length=50)
  email = forms.EmailField(label='Email:')
  password1 = forms.CharField(label='Password:',widget=forms.PasswordInput)    
  password2 = forms.CharField(label='Password Confirmation:',widget=forms.PasswordInput)
  phone=forms.CharField(label='Phone Number:',validators=[RegexValidator(r'^[0-9]+$', 'Enter a valid country phone number.'),],max_length=14)
  first_name=forms.CharField(label='Firstname:', validators=[RegexValidator(r'^[A-Za-z]+$', 'Enter a valid name.'),],max_length=20)
  last_name=forms.CharField(label='Lastname:',validators=[RegexValidator(r'^[A-Za-z]+$', 'Enter a valid name.'),], max_length=20)

  def clean_username(self):        
    username = self.cleaned_data.get('username')        
    if len(username) < 4:            
      raise forms.ValidationError("Your username must be at least 6 characters long.")        
    elif len(username) > 20:            
      raise forms.ValidationError("Your username is too long.")        
    else:            
      filter_result = User.objects.filter(username__exact=username)            
      if len(filter_result) > 0:                
        raise forms.ValidationError("Your username already exists.")        
    return username 
 
     
  def clean_email(self):        
    email = self.cleaned_data.get('email')                    
    filter_result = User.objects.filter(email__exact=email)            
    if len(filter_result) > 0:                
      raise forms.ValidationError("This email already exists, plear input another one.")               
    return email   
  
  def clean_psw1(self):        
    password1 = self.cleaned_data.get('password1')
    if len(password1) < 4:            
      raise forms.ValidationError("Your username must be at least 6 characters long.")        
    elif len(password1) > 20:            
      raise forms.ValidationError("Your username is too long.")     
    return password1 
    
  
  def clean_psw2(self):                
    password2 = self.cleaned_data.get('password2')        
    if len(password2) < 4:            
      raise forms.ValidationError("Your username must be at least 6 characters long.")        
    elif len(password2) > 20:            
      raise forms.ValidationError("Your username is too long.")     

    return password2 
    
  def clean_phone(self):
    phone = self.cleaned_data.get('phone')
    if len(phone) < 6:            
      raise forms.ValidationError("Your phone number is too short.")  
    filter_resultO = Owner.objects.filter(phone__exact=phone)
    if len(filter_resultO) > 0:
      raise forms.ValidationError("This phone number already registered as an Owner , please input another one.") 
    return phone
  
class RegistDriverForm(forms.Form):    
    size_list = (
         (5, '5 passengers'),
         (7, '7 passengers'),
     ) 
    size=forms.IntegerField(label='select the vecicle type:',widget=forms.Select(choices=size_list))  
    
class LoginForm(forms.Form): 
  username = forms.CharField(label='Username', max_length=50)
  password = forms.CharField(label='Password', widget=forms.PasswordInput)   
  
  
  def clean_username(self):        
    username = self.cleaned_data.get('username')        
    filter_result = User.objects.filter(username__exact=username)            
    if not filter_result:                        
        raise ValidationError("This username does not exist. Please register first.")      
    return username


class EditUserForm(forms.Form): 
  phone=forms.CharField(label='Phone Number:',required=False,validators=[RegexValidator(r'^[0-9]+$', 'Enter a valid country phone number.'),],max_length=16)
  first_name=forms.CharField(label='Firstname:',required=False, max_length=20)
  last_name=forms.CharField(label='Lastname:',required=False, max_length=20)
  size_list = (
         (5, '5 passengers'),
         (7, '7 passengers'),
     ) 
  size=forms.IntegerField(label='select the vehicle type:',widget=forms.Select(choices=size_list)) 
  def clean_phone(self):
    phone = self.cleaned_data.get('phone')
    if len(phone) < 6 and len(phone) > 0:            
      raise forms.ValidationError("Your phone number is too short.") 
    filter_resultO = Owner.objects.filter(phone__exact=phone)
    if len(filter_resultO) > 0:
      raise forms.ValidationError("This phone number already registered as an Owner , please input another one.") 
    return phone
   
from django.core.validators import MaxValueValidator
from django.core.validators import MinValueValidator
from django import forms
from django.contrib.admin import widgets     
class CreateOrderForm(forms.Form): 
  passenger = forms.IntegerField(label='Number of Passenger',validators=[MaxValueValidator(7),MinValueValidator(1)])
  #can not eariler than current time£¡£¡
  aptime = forms.SplitDateTimeField(label='Appointment DateTime',widget=widgets.AdminSplitDateTime())  
  destination = forms.CharField(label='Destination', max_length=200)   
  departure= forms.CharField(label='Departure',   max_length=200)   
  def clean_aptime(self):
    aptime = self.cleaned_data.get('aptime')
    datetime_now = timezone.now()
    if aptime < datetime_now:
      raise forms.ValidationError("Datetime should not earlier than current datetime.") 
    return aptime 

from django.utils import timezone   
class ShareSearchOrderForm(forms.Form): 

  passenger = forms.IntegerField(label='Number of Passenger',validators=[MaxValueValidator(6),MinValueValidator(1)])
  #can not eariler than current time£¡£¡
  earliest_aptime = forms.SplitDateTimeField(label='Earliest Accetable DateTime',widget=widgets.AdminSplitDateTime())  
  latest_aptime = forms.SplitDateTimeField(label='Latest Accetable DateTime',widget=widgets.AdminSplitDateTime())
  departure= forms.CharField(label='Departure', required=False, max_length=200)   
  destination = forms.CharField(label='Destination',required=False,  max_length=200)  
  
  def clean_earliest_aptime(self):
    earliest_aptime = self.cleaned_data.get('earliest_aptime')
    datetime_now = timezone.now()
    if earliest_aptime < datetime_now:
      raise forms.ValidationError("Datetime should not earlier than current datetime.") 
    return earliest_aptime
  def clean_latest_aptime(self):
    latest_aptime = self.cleaned_data.get('latest_aptime')
    datetime_now = timezone.now()
    if latest_aptime < datetime_now:
      raise forms.ValidationError("Datetime should not earlier than current datetime.") 
    return latest_aptime
    
 
class EditOrderForm(forms.ModelForm): 
  #can not eariler than current time£¡£¡
  passenger=forms.IntegerField(label='Passenger:',validators=[MaxValueValidator(7),MinValueValidator(1)])
  departure= forms.CharField(label='Departure:',  max_length=200) 
  class Meta:
        model = Order
        fields = ('passenger', 'departure')
  
  
class DriverSearchOrderForm(forms.Form): 
  #can not eariler than current time£¡£¡
  earliest_aptime = forms.SplitDateTimeField(label='Earliest Accetable DateTime',widget=widgets.AdminSplitDateTime())  
  latest_aptime = forms.SplitDateTimeField(label='Latest Accetable DateTime',widget=widgets.AdminSplitDateTime()) 
  departure= forms.CharField(label='Departure', required=False, max_length=200)  
  destination = forms.CharField(label='Destination',required=False, max_length=200)   
    
  def clean_earliest_aptime(self):
    earliest_aptime = self.cleaned_data.get('earliest_aptime')
    datetime_now = timezone.now()
    if earliest_aptime < datetime_now:
      raise forms.ValidationError("Datetime should not earlier than current datetime.") 
    return earliest_aptime
  def clean_latest_aptime(self):
    latest_aptime = self.cleaned_data.get('latest_aptime')
    datetime_now = timezone.now()
    if latest_aptime < datetime_now:
      raise forms.ValidationError("Datetime should not earlier than current datetime.") 
    return latest_aptime 
