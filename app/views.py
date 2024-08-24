from django.contrib import messages
from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from .models import *
import json
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout

from django.core.mail import send_mail
from django.conf import settings

from django.core.mail import EmailMessage
from django.template.loader import render_to_string

import datetime

def set_cookie(response, key, value, days_expire=7):
    if days_expire is None:
        max_age = 365 * 24 * 60 * 60  # one year
    else:
        max_age = days_expire * 24 * 60 * 60
    expires = datetime.datetime.strftime(
        datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age),
        "%a, %d-%b-%Y %H:%M:%S GMT",
    )
    response.set_cookie(
        key,
        value,
        max_age=max_age,
        expires=expires,
        domain=settings.SESSION_COOKIE_DOMAIN,
        secure=settings.SESSION_COOKIE_SECURE or None,
    )
# Create your views here.
def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    if(str(request.user) != "AnonymousUser") :
       logged=True
    else:
       logged=False
    order ={'total':0,'quantity':0}
    categories = Category.objects.filter(is_sub =False)
    active_category=request.GET.get('category','')
    context = {'categories':categories,'active_category':active_category,'form':form,'logged':logged ,"order" :order}
    return render(request,'app/register.html',context)
def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST" :
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.info(request,'Tài khoản hoặc mật khẩu không đúng !')
    if(str(request.user) != "AnonymousUser") :
       logged=True
    else:
       logged=False
    order ={'total':0,'quantity':0}
    categories = Category.objects.filter(is_sub =False)
    active_category=request.GET.get('category','')
    context = {'categories':categories,'active_category':active_category,'logged':logged,"order" :order}
    return render(request,'app/login.html',context)
def logoutPage(request):
    logout(request)
    return redirect('home')
def home(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer =customer,complete =False)
        items = order.orderitem_set.all()
        order.quantity=0
        order.total=0
        for item in items:
            item.total=0
            item.product.price=int(item.product.price)
            item.total=item.product.price*item.quantity
            item.total=int(item.total)
            order.total = order.total+item.total
            order.quantity = order.quantity+item.quantity
            item.product.price = "{:,}".format(item.product.price)
            item.total = "{:,}".format(item.total)
        order.total=int(order.total)
        order.total = "{:,}".format(order.total)
    else:
        items =[]
        order ={'total':0,'quantity':0}
    if(request.COOKIES.get('sort') == "asc"):
        products =Product.objects.order_by("price")
        select1=True
        select2=False
    elif (request.COOKIES.get('sort') == "desc"):
        products =Product.objects.order_by("-price")
        select1=False
        select2=True
    else:
        products =Product.objects.all()
        select1=False
        select2=False
    for product in products:
        product.price=int(product.price)
        product.price = "{:,}".format(product.price)
    if(str(request.user) != "AnonymousUser") :
       logged=True
    else:
       logged=False
    categories = Category.objects.filter(is_sub =False)
    active_category=request.GET.get('category','')
    context={'select1':select1,'select2':select2,'categories':categories,'active_category':active_category,'products' : products,'items':items,'order':order,'logged':logged}
    return render(request,'app/home.html',context)
def cart(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer =customer,complete =False)
        items = order.orderitem_set.all()
        order.quantity=0
        order.total=0
        for item in items:
            item.total=0
            item.product.price=int(item.product.price)
            item.total=item.product.price*item.quantity
            item.total=int(item.total)
            order.total = order.total+item.total
            order.quantity = order.quantity+item.quantity
            item.product.price = "{:,}".format(item.product.price)
            item.total = "{:,}".format(item.total)
        order.total=int(order.total)
        order.total = "{:,}".format(order.total)
    else:
        items =[]
        order ={'total':0,'quantity':0}
    if(str(request.user) != "AnonymousUser") :
       logged=True
    else:
       logged=False
    categories = Category.objects.filter(is_sub =False)
    active_category=request.GET.get('category','')
    context={'categories':categories,'active_category':active_category,'items':items,'order':order,'logged':logged}
    return render(request,'app/cart.html',context)
def checkout(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer =customer,complete =False)
        items = order.orderitem_set.all()
        order.quantity=0
        order.total=0
        for item in items:
            item.total=0
            item.product.price=int(item.product.price)
            item.total=item.product.price*item.quantity
            item.total=int(item.total)
            order.total = order.total+item.total
            order.quantity = order.quantity+item.quantity
            item.product.price = "{:,}".format(item.product.price)
            item.total = "{:,}".format(item.total)
        order.total=int(order.total)
        order.total = "{:,}".format(order.total)
    else:
        items =[]
        order ={'total':0,'quantity':0}
       
    if(str(request.user) != "AnonymousUser") :
       logged=True
    else:
       logged=False
    categories = Category.objects.filter(is_sub =False)
    active_category=request.GET.get('category','')
    context={'categories':categories,'active_category':active_category,'items':items,'order':order,'logged':logged}
    return render(request,'app/checkout.html',context)
def updateItem(request):
    try:
        data=json.loads(request.body)
        productId = data['productId']
        action = data['action']
        customer = request.user
        product =Product.objects.get(id = productId)
        order, created = Order.objects.get_or_create(customer =customer,complete =False)
        orderItem, created = OrderItem.objects.get_or_create(order =order,product =product)
        items = order.orderitem_set.all()
        if action =='add':
            orderItem.quantity +=1
        elif action == 'remove':
            orderItem.quantity -=1
        orderItem.save()
        if orderItem.quantity<=0:
            orderItem.delete()
        order.quantity=0
        for item in items:
            order.quantity = order.quantity+item.quantity
        return JsonResponse(order.quantity,safe=False)    
    except:
        return JsonResponse('notadded',safe=False) 
def search(request):
    if request.method == "POST" :
        searched = request.POST["searched"]
        keys=Product.objects.filter(name__contains = searched)
    for key in keys:
        key.price=int(key.price)
        key.price = "{:,}".format(key.price)
    if(str(request.user) != "AnonymousUser") :
       logged=True
    else:
       logged=False
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer =customer,complete =False)
        items = order.orderitem_set.all()
        order.quantity=0
        for item in items:
            order.quantity = order.quantity+item.quantity
    else:
        items =[]
        order ={'quantity':0}
    categories = Category.objects.filter(is_sub =False)
    active_category=request.GET.get('category','')

    
    return render(request,'app/search.html',{'categories':categories,'active_category':active_category,"searched":searched,"keys":keys,'logged':logged,'items':items,'order':order}) 

def complete(request):
    if request.method == "POST" :
        name= request.POST["name"]
        email=request.POST["email"]
        address=request.POST["address"]
        city=request.POST["city"]
        country=request.POST["country"]
        mobile=request.POST["mobile"]
        if request.user.is_authenticated:
            customer=request.user
            order, created = Order.objects.get_or_create(customer =customer,complete =False)
            items = order.orderitem_set.all()
            count=0
            for item in items:
                item.total=0
                item.product.price=int(item.product.price)
                item.total=item.product.price*item.quantity
                item.total=int(item.total)
                item.product.price = "{:,}".format(item.product.price)
                item.total = "{:,}".format(item.total)
                count=count+1
            if count !=0:
                shippingAddr, created = ShippingAddress.objects.get_or_create(customer =customer,order=order)
                shippingAddr.order=order
                shippingAddr.mobile=mobile
                shippingAddr.address=address
                shippingAddr.country=country
                shippingAddr.city=city
                order.complete=True
                shippingAddr.save()
                order.save()
                # send_mail(
                #     "Đặt hàng thành công",
                #     "Bạn đã đặt hàng thành công. Vui lòng chờ 2-3 ngày để nhận hàng",
                #     'settings.EMAIL_HOST_USER',
                #     [email],
                #     fail_silently=False
                # )
                subject = 'Đặt hàng thành công'
                email_from = 'settings.EMAIL_HOST_USER'
                recipient_list = [email]

                # Tạo nội dung HTML
                html_content = render_to_string('app/email_template.html', {'items': items})

                # Tạo EmailMessage
                email = EmailMessage(subject, html_content, email_from, recipient_list)
                email.content_subtype = "html"  # Đặt loại nội dung là HTML
                
                # Gửi email
                email.send()


    return redirect('home')

def category(request):
    categories = Category.objects.filter(is_sub =False)
    active_category=request.GET.get('category','')
    if active_category:
        products =Product.objects.filter(category__slug =active_category)
    for product in products:
        product.price=int(product.price)
        product.price = "{:,}".format(product.price)
    if(str(request.user) != "AnonymousUser") :
       logged=True
    else:
       logged=False
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer =customer,complete =False)
        items = order.orderitem_set.all()
        order.quantity=0
        for item in items:
            order.quantity = order.quantity+item.quantity
    else:
        items =[]
        order ={'quantity':0}
    context={'categories':categories,'products':products,'active_category':active_category,'logged':logged,'items':items,'order':order}
    return render(request,'app/category.html',context)    
def detail(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer =customer,complete =False)
        items = order.orderitem_set.all()
        order.quantity=0
        order.total=0
        for item in items:
            item.total=0
            item.product.price=int(item.product.price)
            item.total=item.product.price*item.quantity
            item.total=int(item.total)
            order.total = order.total+item.total
            order.quantity = order.quantity+item.quantity
            item.product.price = "{:,}".format(item.product.price)
            item.total = "{:,}".format(item.total)
        order.total=int(order.total)
        order.total = "{:,}".format(order.total)
    else:
        items =[]
        order ={'total':0,'quantity':0}
    if(str(request.user) != "AnonymousUser") :
       logged=True
    else:
       logged=False
    id=request.GET.get('id','')
    product = Product.objects.filter(id=id)
    for p in product:
        if not p.detail:
            p.detail=""
        p.price=int(p.price)
        p.price = "{:,}".format(p.price)
    categories = Category.objects.filter(is_sub =False)
    active_category=request.GET.get('category','')
    context={'product':product,'categories':categories,'active_category':active_category,'items':items,'order':order,'logged':logged}
    return render(request,'app/detail.html',context) 
    
   