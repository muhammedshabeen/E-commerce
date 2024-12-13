from django.shortcuts import render, redirect
from backend.models import *
from django.contrib import messages
from django.db import transaction
from django.db.models import Prefetch
from .forms import *
from django.db.models import Avg
from django.contrib.auth import login, authenticate
from .decorators import login_required_frontend





def frontend_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            
            login(request, user)
            messages.success(request, "You are now logged in!")
            return redirect('home') 
        else:
            # Invalid credentials
            messages.error(request, "Invalid username or password")
            return redirect('frontend_login')
    return render(request,"login.html")

def frontend_register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not username or not email or not password:
            messages.error(request, "All fields are required.")
            return redirect('frontend_register')

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('frontend_register')

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect('frontend_register')

        user = CustomUser.objects.create_user(username=username, email=email, password=password,user_type="Customer")
        user.save()

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect('home')
    return render(request,"register.html")

@login_required_frontend
def frontend_logout(request):
    request.session.flush()
    messages.success(request,"logout success")
    return redirect('home')



def home(request):
    product_objs = Product.objects.filter(status='Active')
    
    context = {
        "product_objs":product_objs
    }
    return render(request,'home.html',context)



def product_detail(request,slug):
    try:
        product_obj = Product.objects.get(slug=slug,status="Active")
        reviews = Review.objects.filter(product=product_obj).order_by('-id')
        overall_rating = reviews.aggregate(Avg('rating'))['rating__avg'] if reviews.exists() else 0
        context = {
        "product_obj":product_obj,
        "reviews_objs":reviews,
        "form" : ReviewForm(),
        "overall_rating":overall_rating,
        "reviews_count":reviews.count()
        }
        return render(request,'product_details.html',context)
    except Product.DoesNotExist:
        messages.error(request,"Product not found")
        return redirect('home')

@login_required_frontend
def add_to_cart(request):
    if not request.user.is_authenticated:
        messages.error(request, "Please log in to add items to your cart.")
        return redirect('login')
    print("USER IS",request.user.username)
    
    if request.method == 'POST':
        user = request.user
        try:
            quantity = request.POST.get('qty','1')
            slug = request.POST.get('product_slug')
            try:
                product_obj = Product.objects.get(slug=slug,status="Active")
            except Product.DoesNotExist:
                messages.error(request,'Product doesnot exist')
                return redirect('home')
            
            if int(quantity) > int(product_obj.stock):
                messages.error(request,"Quantity is higher than product stock")
                return redirect('home')
            
            cart_item, created = Cart.objects.get_or_create(user=user, product=product_obj)
            if created:
                cart_item.quantity = quantity
            else:
                new_quantity = cart_item.quantity + int(quantity)
                if new_quantity > product_obj.stock:
                    messages.error(request, "Cannot add more than available stock.")
                    return redirect('home')
                cart_item.quantity = new_quantity
            
            cart_item.save()
            messages.success(request, f"Added {product_obj.title} to your cart.")
            return redirect('view_cart')
        
        except Exception as e:
            messages.error(request,str(e))
            return redirect('home')
        
    else:
        messages.error(request,"Invalid request")
        return redirect('home')
    
@login_required_frontend
def view_cart(request):
    user = request.user
    cart_objs = Cart.objects.filter(user=user).order_by('-id')
    user_cart_total = Cart.get_user_cart_total(request.user)
    if user.is_authenticated:
        try:
            address = Address.objects.get(user=user)
        except Address.DoesNotExist:
            address = None
    context = {
        "cart_objs":cart_objs,
        "user_cart_total":user_cart_total,
        "address":address,
    }
    return render(request,'cart.html',context)

@login_required_frontend
def update_cart(request):
    if request.method == 'POST':
        user = request.user

        for cart_obj in Cart.objects.filter(user=user).order_by('-id'):
            cart_quantity = request.POST.get(f'qty_{cart_obj.id}')
            if cart_quantity:
                try:
                    quantity = int(cart_quantity)
                    if quantity > 0 and quantity <= cart_obj.product.stock:
                        cart_obj.quantity = quantity
                        cart_obj.save()
                    else:
                        messages.error(request, f"Invalid quantity for {cart_obj.product.title}")
                except ValueError:
                    messages.error(request, f"Invalid quantity for {cart_obj.product.title}")

        messages.success(request, 'Cart updated successfully.')
        return redirect('view_cart')

    return redirect('home')


@login_required_frontend
def delete_cart_item(request,pk):
    user = request.user
    if pk and user.is_authenticated:
        try:
            cart_obj = Cart.objects.get(id=pk,user=user)
            cart_obj.delete()
            messages.success(request,"Cart item removed")
        except Cart.DoesNotExist:
            messages.error(request,"Cart item doesnot exist")
    else:
        messages.error(request,"an error occured please try again!!")
    return redirect('view_cart')


@login_required_frontend
def add_address(request):
    if request.method == "POST" and request.user.is_authenticated:
        user = request.user
        Address.objects.create(
            user=user,
            street=request.POST['street'],
            city=request.POST['city'],
            state=request.POST['state'],
            pin_code=request.POST['pin_code'],
            country=request.POST['country'],
            phone_no=request.POST['phone_no']
        )
        messages.success(request, "Address added successfully!")
        return redirect('view_cart')
    else:
        messages.error(request, "Failed to add address. Try again.")
        return redirect('view_cart')
    
@login_required_frontend
def update_address(request):
    user = request.user
    if not user.is_authenticated:
        messages.error(request, "You need to be logged in to update your address.")
        return redirect('frontend_login')
    
    try:
        address = Address.objects.get(user=user)
    except Address.DoesNotExist:
        messages.error(request,"Address doesnot exist")
        return redirect('home')
    
    if request.method == "POST":
        # Update the address details
        address.street = request.POST.get('street')
        address.city = request.POST.get('city')
        address.state = request.POST.get('state')
        address.pin_code = request.POST.get('pin_code')
        address.country = request.POST.get('country')
        address.phone_no = request.POST.get('phone_no')
        address.save()

        messages.success(request, "Address updated successfully!")
        return redirect('view_cart')

    return render(request, 'update_address.html', {'address': address})



@login_required_frontend
def checkout(request):
    user = request.user
    cart_objs = Cart.objects.filter(user=user)

    if not user.is_authenticated:
        messages.error(request, "You must be logged in to checkout.")
        return redirect('frontend_login')

    if not cart_objs.exists():
        messages.error(request, "Your cart is empty.")
        return redirect('home')
    
    try:
        address = f'{user.address.street}\n{user.address.city}\n{user.address.state}\n{user.address.country}\nPin Code: {user.address.pin_code}\nPhone: {user.address.phone_no}'
    except Exception as e:
        messages.error(request, "Please add an address before proceeding to checkout.")
        return redirect('view_cart')
    
    with transaction.atomic():
        for cart_item in cart_objs:
            product = cart_item.product
            if product.stock < cart_item.quantity:
                messages.error(request, f"Not enough stock for {product.title}. Available: {product.stock}")
                return redirect('checkout') 

        total_amount = sum(cart_item.product.price * cart_item.quantity for cart_item in cart_objs)
        order = Order.objects.create(
            user=user,
            address=address,
            total_amount=total_amount
        )

        for cart_item in cart_objs:
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.product.price
            )

            product = cart_item.product
            product.stock -= cart_item.quantity
            product.save()

        cart_objs.delete()

    messages.success(request, f"Your order {order.order_id} has been placed successfully!")
    return redirect('order_confirmation', order_id=order.order_id)


@login_required_frontend
def order_confirmation(request,order_id):
    try:
        order = Order.objects.prefetch_related(Prefetch('items', queryset=OrderItem.objects.all())).get(order_id=order_id, user=request.user)
        context = {
            "order":order
        }
        return render(request,"order_confirm.html",context)
    except Order.DoesNotExist:
        messages.error(request,"Order doesnot exist")
        return redirect('home')
    
@login_required_frontend
def user_orders(request):
    orders = Order.objects.filter(user=request.user).prefetch_related('items')
    context = {
        'orders': orders,
    }
    return render(request, 'user_orders.html', context)



@login_required_frontend
def add_review(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        messages.error(request,"Product doesnot exist")
        return redirect('home')
    
    if Review.objects.filter(product=product, user=request.user).exists():
        messages.error(request, "You have already reviewed this product.")
        return redirect('product_detail', slug=product.slug)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()

            messages.success(request, "Thank you for your review!")
            return redirect('product_detail', slug=product.slug)
    else:
        return redirect('home')
    
    
    
@login_required_frontend
def add_to_cart_home(request):
    if not request.user.is_authenticated:
        messages.error(request, "Please log in to add items to your cart.")
        return redirect('frontend_login')
    print("USER IS",request.user.username)
    
    if request.method == 'GET':
        user = request.user
        try:
            quantity = request.GET.get('quantity')
            slug = request.GET.get('product_slug')
            try:
                product_obj = Product.objects.get(slug=slug,status="Active")
            except Product.DoesNotExist:
                messages.error(request,'Product doesnot exist')
                return redirect('home')
            
            if int(quantity) > int(product_obj.stock):
                messages.error(request,"Quantity is higher than product stock")
                return redirect('home')
            
            cart_item, created = Cart.objects.get_or_create(user=user, product=product_obj)
            if created:
                cart_item.quantity = quantity
            else:
                new_quantity = cart_item.quantity + int(quantity)
                if new_quantity > product_obj.stock:
                    messages.error(request, "Cannot add more than available stock.")
                    return redirect('home')
                cart_item.quantity = new_quantity
            
            cart_item.save()
            messages.success(request, f"Added {product_obj.title} to your cart.")
            return redirect('view_cart')
        
        except Exception as e:
            messages.error(request,str(e))
            return redirect('home')
        
    else:
        messages.error(request,"Invalid request")
        return redirect('home')