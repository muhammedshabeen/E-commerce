from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from .decorators import admin_only
from django.db.models import Prefetch
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


def signin(request):
    next_url = request.GET.get('next')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password,user_type='Admin')
        
        if user is not None and user.status == 'Active':
            if user.user_type == 'Admin':
                login(request, user)
                messages.success(request,'Logined successfully')
                return redirect(next_url if next_url else 'backend_index')
            else:
                messages.error(request, 'Invalid email or password.')
                return render(request, 'registration/signin.html')
        else:
            messages.error(request, 'Invalid email or password.')
            return render(request, 'registration/signin.html')
    return render(request,'registration/signin.html')


@login_required
@admin_only
def signout(request):
    request.session.flush()
    messages.success(request,"Logout successfully")
    return redirect('signin')
    
    
    
@login_required
@admin_only
def backend_index(request):
    pending_order = Order.objects.filter(status='Pending').count()
    approved_order = Order.objects.filter(status='Approved').count()
    shiped_order = Order.objects.filter(status='Shipped').count()
    delivered_order = Order.objects.filter(status='Delivered').count()
    context = {
        "pending_order":pending_order,
        "approved_order":approved_order,
        "shiped_order":shiped_order,
        "delivered_order":delivered_order,
    }
    return render(request,'dashboard/dashboard.html',context)


@login_required
@admin_only
def customer(request):
    user_objs = CustomUser.objects.filter(user_type='Customer').order_by('-id')
    context = {
        "user_objs":user_objs,
    }
    return render(request,'customer/view.html',context)

@login_required
@admin_only
def edit_customer(request,pk):
    
    try:
        customer_obj = CustomUser.objects.get(id=pk)
    except CustomUser.DoesNotExist:
        messages.error(request,"Customer doesnot found")
        return redirect('customer')
    if request.method == 'POST':
        form = CustomUserForm(request.POST,request.FILES,instance=customer_obj)
        if form.is_valid():
            form.save()
            messages.success(request,"Customer edited successfully")
            return redirect('customer')
        else:
            for field_name, errors in form.errors.items():
                for error in errors:
                    messages.error(request, "{}".format(error))
    
    context = {
        'form' : CustomUserForm(instance = customer_obj)
    }
    return render(request,'customer/edit.html',context)

@login_required
@admin_only
def delete_customer(request,pk):
    try:
        user = CustomUser.objects.get(id=pk)
        user.status = 'Deleted'
        user.save()
        messages.success(request,"User deleted successfully")
    except CustomUser.DoesNotExist:
        messages.error(request,"User not found")
    
    return redirect('customer')



@login_required
@admin_only
def product(request):
    product_objs = Product.objects.all().order_by('-id')
    context = {
        "product_objs":product_objs,
    }
    return render(request,'product/view.html',context)

@login_required
@admin_only
def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,"Product added successfully")
            return redirect('product')
        else:
            for field_name, errors in form.errors.items():
                for error in errors:
                    messages.error(request, "{}".format(error))
    
    context = {
        'form' : ProductForm()
    }
    return render(request,'product/create.html',context)

@login_required
@admin_only
def edit_product(request,pk):
    
    try:
        product_obj = Product.objects.get(id=pk)
    except Product.DoesNotExist:
        messages.error(request,"Product doesnot found")
        return redirect('product')
    if request.method == 'POST':
        form = ProductForm(request.POST,request.FILES,instance=product_obj)
        if form.is_valid():
            form.save()
            messages.success(request,"Product edited successfully")
            return redirect('product')
        else:
            for field_name, errors in form.errors.items():
                for error in errors:
                    messages.error(request, "{}".format(error))
    
    context = {
        'form' : ProductForm(instance = product_obj)
    }
    return render(request,'product/edit.html',context)

@login_required
@admin_only
def delete_product(request,pk):
    try:
        product = Product.objects.get(id=pk)
        product.status = 'Deleted'
        product.save()
        messages.success(request,"Product deleted successfully")
    except Product.DoesNotExist:
        messages.error(request,"Product not found")
    return redirect('product')


@login_required
@admin_only
def order_view(request):
    order_objs = Order.objects.all().order_by('-id')
    context = {
        "order_objs":order_objs,
    }
    return render(request,'order/view.html',context)

@csrf_exempt
def update_order_status(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            order_id = data.get("order_id")
            new_status = data.get("status")

            order = Order.objects.get(id=order_id)
            order.status = new_status
            order.save()

            return JsonResponse({"success": True, "message": "Order status updated successfully."})
        except Order.DoesNotExist:
            return JsonResponse({"success": False, "message": "Order not found."})
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)})
    return JsonResponse({"success": False, "message": "Invalid request method."})

@login_required
@admin_only
def order_view_detail(request,order_id):
    print("pppp",order_id)
    try:
        order = Order.objects.prefetch_related(Prefetch('items', queryset=OrderItem.objects.all())).get(order_id=order_id)
        context = {
            "order_obj":order
        }
        return render(request,"order/detail.html",context)
    except Order.DoesNotExist:
        messages.error(request,"Order doesnot exist")
        return redirect('order_view')