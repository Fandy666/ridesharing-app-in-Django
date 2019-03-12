from django.urls import reverse
from django.contrib import auth
from django.contrib.auth.models import User,Group
from django.contrib.auth import authenticate
from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import render,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Permission,ContentType    
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth.decorators import permission_required
# Create your views here.
from .models import Owner, Order, Driver

def index(request):
  request.session['No_access']='yes'
  if request.user.has_perm('home.confirm_order'):
       driver1=request.user.driver_set.all().first()
       for order in driver1.order_set.all():
       
         name1='key'+str(order.pk)
         if not name1 in request.session:
           request.session[name1]=order.pk
           
  return render(
        request,
        'index.html',    )
from django.views import generic


class OrderListView(LoginRequiredMixin,generic.ListView):
    login_url = '/home/login/'
    redirect_field_name = 'redirect_to'
    model = Order
    
    
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
class OrderDetailView(LoginRequiredMixin,generic.DetailView):
    login_url = '/home/login/'
    redirect_field_name = 'redirect_to'
    model = Order
    def get_ownerlist(self,request,pk):
      orderid=get_object_or_404(Order, pk=pk)
      if orderid.owner_set.all().count()>1:
         owner_select=list(orderid.owner_set.all())[1:]
      else:
         owner_select=[]      
      return render(request,'order_detail.html',context={'owner_select':owner_select})
    def post(self,request,pk):
        if request.method == 'POST':
           if 'sss' in request.POST:
             order_inst=get_object_or_404(Order, pk=pk) 
             drivernow=request.user.driver_set.all().first()
             if drivernow.size=='5':
              capacity=5;
             else:
              capacity=7;
             if capacity<order_inst.passenger: 
                return HttpResponse( 'You vehicle size does not match this order!') 
             owners_list=order_inst.owner_set.all()
             receive_list=[owner.user.email for owner in owners_list]
             res = send_mail(
                       'Your order has been confirmed',
                        'Your order has been confirmed, you can login to see the detail.',
                        'fz48@duke.edu',
                        receive_list,
                        fail_silently=False)
             order_inst.status = 'c'
             order_inst.driver=request.user.driver_set.all().first()
             order_inst.save()
             return HttpResponseRedirect("/home/")
           if 'aaa' in request.POST:
             order_inst=get_object_or_404(Order, pk=pk)             
             order_inst.status = 'f'
             order_inst.save()
             return HttpResponseRedirect("/home/")
           if 'ccc' in request.POST:
             order_inst=get_object_or_404(Order, pk=pk)
             order_inst.passenger+=request.session['share_pass']
             order_inst.status='s'
             del request.session['share_pass']
             owner111=request.user.owner_set.all().first()
             owner111.order.add(order_inst)
             owner111.save()
             #order_inst.owner.add(request.user.owner_set.all().first())
             order_inst.save()
             return HttpResponseRedirect("/home/")   
 

class OwnerListView(LoginRequiredMixin,generic.ListView):
    login_url = '/home/login/'
    redirect_field_name = 'redirect_to'
    model = Owner


class OwnerDetailView(LoginRequiredMixin,generic.DetailView):
    login_url = '/home/login/'
    redirect_field_name = 'redirect_to'
    model = Owner
    
class DriverDetailView(LoginRequiredMixin,generic.DetailView):
    login_url = '/home/login/'
    redirect_field_name = 'redirect_to'
    model = Driver

from django.views.generic.edit import UpdateView
 
    
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm,RegistDriverForm, LoginForm,CreateOrderForm,ShareSearchOrderForm,DriverSearchOrderForm,EditOrderForm,EditUserForm
from django.core.exceptions import ObjectDoesNotExist
def dregist(request):
    if request.method == 'GET':
        form = RegistrationForm()
    if request.method == 'POST':       
        form = RegistrationForm(request.POST)   
        if form.is_valid():
          username = form.clean_username()     
          email = form.clean_email()
          password1 = form.clean_psw1()     
          password = form.clean_psw2()  
          phone=form.clean_phone()
          first_name=form.cleaned_data.get('first_name')
          last_name=form.cleaned_data.get('last_name')
          if password1 and password and password1 != password:                   
            return render(request, 'home/register.html', {'form': form,'message': 'Password mismatch. Please enter again.'})  
          else:               
            user = User.objects.create_user(username=username,email=email,password=password)
            user.first_name=first_name
            user.last_name=last_name
            user.save()
            permission = Permission.objects.get(codename='change_order_info')
            user.user_permissions.add(permission)
            permission = Permission.objects.get(codename='create_order')
            user.user_permissions.add(permission)
            user.save()
            if user.has_perm('home.change_order_info'):
              print('owner can change order info')
            owner=Owner.objects.create(user=user); 
            owner.phone=phone
            owner.save()                 
            return HttpResponseRedirect("/home/login/")
            
    return render(request, 'home/register.html', {'form': form})

@login_required(login_url='/home/login/')    
def registdriver(request):
    if request.method == 'GET':
        form = RegistDriverForm()
    if request.method == 'POST':       
        form = RegistDriverForm(request.POST)   
        if form.is_valid():
          size=form.cleaned_data.get('size')
          thisuser=request.user
          if thisuser.driver_set.count()!=0: 
            return render(request, 'home/registerdriver.html', {'form': form,'message': 'You have already registered as a driver'})  
          permission = Permission.objects.get(codename='confirm_order')
          thisuser.user_permissions.add(permission)
          thisuser.save()
          driver=Driver.objects.create(user=thisuser); 
          if size==5:
            driver.size='5'
          else:
            driver.size='7'
          driver.save()                       
          return HttpResponseRedirect("/home/")           
    return render(request, 'home/register.html', {'form': form})
        
def dlogin(request):
  if request.method == 'GET':
    form = LoginForm()    
  if request.method == 'POST':       
    form = LoginForm(request.POST)        
    if form.is_valid():  
             
      username = form.clean_username()                   
      password=form.cleaned_data.get('password')        
              
      user = auth.authenticate(username=username, password=password)            
      if user:               
        auth.login(request, user)              
        return HttpResponseRedirect("/home/")
      else :
        return render(request, 'home/login.html', {'form': form,'message': 'Wrong password. Please try again.'})
        
  return render(request, 'home/login.html', {'form': form})
  

def dlogout(request):

    if request.method == 'GET':
        auth.logout(request)
        return render(request, 'home/logout.html', {'message': 'You are logout.'})

class OrderUpdateView(LoginRequiredMixin,UpdateView):
  login_url = '/home/login/'
  redirect_field_name = 'redirect_to'
  model = Order     
  template_name_suffix = '_update_form'
  success_url = '/home/'    
  permission_required = 'home.change_order_info'    
  permission_fail_message = ('You don\'t have permission to change order info.')    
  form_class = EditOrderForm 
  def get_queryset(self):
        return Order.objects.filter(owner = self.request.user.owner_set.filter().first())
 

@login_required(login_url='/home/login/')
def edit_user(request):  
  if request.method == 'GET':
    form = EditUserForm()     
  if request.method == "POST":        
    form = EditUserForm(request.POST)               
    if form.is_valid():            
      phone=form.clean_phone()
      first_name=form.cleaned_data.get('first_name')
      last_name=form.cleaned_data.get('last_name')
      size=form.cleaned_data.get('size')
      thisuser=request.user
      if first_name:
        thisuser.first_name=first_name
      if last_name:
        thisuser.last_name=last_name
      thisuser.save()
      owner = Owner.objects.get(user=thisuser)
      if phone:
        owner.phone=phone
        owner.save()
      if thisuser.driver_set.count()!=0: 
        driver = Driver.objects.get(user=request.user)
        if size==5:
            driver.size='5'
        else:
            driver.size='7'
        print(size)
        driver.save()
      return HttpResponseRedirect('/home/')
       
  return render(request, "home/edituser.html", {"form":form}) 

    
@permission_required('home.create_order', login_url='/home/login/')
def create_order(request):
  if request.method == 'GET':
    form = CreateOrderForm()    
  if request.method == 'POST':       
    form = CreateOrderForm(request.POST)        
    if form.is_valid():  
      passenger = form.cleaned_data.get('passenger')
      aptime = form.clean_aptime()
      destination = form.cleaned_data.get('destination')
      departure= form.cleaned_data.get('departure')
      order = Order.objects.create(passenger=passenger,destination=destination,aptime=aptime,departure=departure )
      order.save()
      print(request.user.owner_set.all().count())
      ownernow=request.user.owner_set.filter().first()
      ownernow.order.add(order)
      ownernow.save()
      return HttpResponseRedirect("/home/")
  return render(request, 'home/createorder.html', {'form': form})   
  
import datetime
@permission_required('home.create_order', login_url='/home/login/')
def share_search_order(request):
  if 'confirm_key' in request.session:
     del request.session['confirm_key']
  if 'No_access' in request.session:
     del request.session['No_access']   
  if request.method == 'GET':
    form = ShareSearchOrderForm()    
  if request.method == 'POST':       
    form = ShareSearchOrderForm(request.POST)       
    if form.is_valid():  
      request.session['share_key']='true'
      passenger = form.cleaned_data.get('passenger')  
      request.session['share_pass']=passenger
      earliest_aptime = form.clean_earliest_aptime()
      latest_aptime= form.clean_latest_aptime()
      destination = form.cleaned_data.get('destination')
      departure = form.cleaned_data.get('departure')
      if latest_aptime <= earliest_aptime:
        return render(request, 'home/driversearchorder.html', {'form': form,'message': 'Earliest accetable DateTime should not later than latest DateTime'}) 
      passenger_cons=7-passenger
      if not departure and not destination:
        searchorder_list = Order.objects.filter(aptime__range=(earliest_aptime,latest_aptime),passenger__lte=passenger_cons,status__in=['r','s'])
      elif not departure:
        searchorder_list = Order.objects.filter(aptime__range=(earliest_aptime,latest_aptime),destination__exact=destination,passenger__lte=passenger_cons,status__in=['r','s'])
      elif not destination:
        searchorder_list = Order.objects.filter(aptime__range=(earliest_aptime,latest_aptime),passenger__lte=passenger_cons,status__in=['r','s'],departure__exact=departure)
      else:
        searchorder_list = Order.objects.filter(aptime__range=(earliest_aptime,latest_aptime),destination__exact=destination,passenger__lte=passenger_cons,status__in=['r','s'],departure__exact=departure)
      drivernow=request.user.driver_set.filter().first()  
      ownernow=request.user.owner_set.filter().first()
      if drivernow:
        searchorder_list =searchorder_list.exclude(driver=drivernow)
      searchorder_list =searchorder_list.exclude(owner=ownernow)
      if not searchorder_list:
        return render(request, 'home/sharesearchorder.html', {'message': 'No such ride exist.Please search again.'})
      return render(request, 'home/searchorder_list.html', {'passenger_request':passenger,'searchorder_list': searchorder_list})
  return render(request, 'home/sharesearchorder.html', {'form': form}) 
  
  
@permission_required('home.confirm_order', login_url='/home/login/')
def driver_search_order(request):
  if 'share_key' in request.session:
     del request.session['share_key']
  if 'No_access' in request.session:
     del request.session['No_access']
  if request.method == 'GET':
    form = DriverSearchOrderForm()    
  if request.method == 'POST':       
    form = DriverSearchOrderForm(request.POST)       
    if form.is_valid(): 
      request.session['confirm_key']='true'
      earliest_aptime = form.clean_earliest_aptime()
      latest_aptime= form.clean_latest_aptime()  
      destination = form.cleaned_data.get('destination')
      departure = form.cleaned_data.get('departure')
      if latest_aptime <= earliest_aptime:
        return render(request, 'home/driversearchorder.html', {'form': form,'message': 'Earliest accetable DateTime should not later than latest DateTime'}) 
      drivernow=request.user.driver_set.filter().first()
      ownernow=request.user.owner_set.filter().first()
      if drivernow.size=='5':
        capacity=5;
      else:
        capacity=7;
      if not departure and not destination:
        searchorder_list = Order.objects.filter(aptime__range=(earliest_aptime,latest_aptime),passenger__lte=capacity,status__in=['r','s'])
      elif not departure:
        searchorder_list = Order.objects.filter(aptime__range=(earliest_aptime,latest_aptime),destination__exact=destination,passenger__lte=capacity,status__in=['r','s'])
      elif not destination:
        searchorder_list = Order.objects.filter(aptime__range=(earliest_aptime,latest_aptime),passenger__lte=capacity,status__in=['r','s'],departure__exact=departure)
      else:
        searchorder_list = Order.objects.filter(aptime__range=(earliest_aptime,latest_aptime),destination__exact=destination,passenger__lte=capacity,status__in=['r','s'],departure__exact=departure)
      searchorder_list =searchorder_list.exclude(owner=ownernow)
      if not searchorder_list:
        return render(request, 'home/driversearchorder.html', {'message': 'No such ride exist.Please search again.'})
      return render(request, 'home/searchorder_list.html', {'searchorder_list': searchorder_list})
  return render(request, 'home/driversearchorder.html', {'form': form}) 
  
  