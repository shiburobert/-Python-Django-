from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from shop.form import CustomUserForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import *
import json
from django.contrib.auth.decorators import login_required
from .models import Cart, Product, Order
from .form import ContactForm
from django.views.decorators.cache import never_cache

def home(request):
    products = Product.objects.filter(trending=1)
    return render(request, "shop/index.html", {'products': products})
    
@never_cache
def login_page(request):
    if request.user.is_authenticated:
        return redirect("/")
    else:
        if request.method == 'POST':  
            name = request.POST.get('username')
            pwd = request.POST.get('password')
            user = authenticate(request, username=name, password=pwd)
            if user is not None:
                login(request, user)
                messages.success(request, "Logged in Successfully")
                return redirect("/")
            else:
                messages.error(request, "Invalid User Name or Password")
                return redirect("/login/")
        return render(request, "shop/login.html")

def logout_page(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "Logged out Successfully")
        return redirect("login")
    else:
        messages.error(request, "You are not logged in")
        return redirect("/login")
    
@never_cache  # This prevents the page from being cached
def register(request):
    # If the user is already authenticated, redirect to the homepage or another page
    if request.user.is_authenticated:
        return redirect('/')
    
    form = CustomUserForm()
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration Success! You can Login Now!")
            return redirect('/login/')
    return render(request, "shop/register.html", {"form": form})

def collections(request):
    catagory=Catagory.objects.filter(status=0)  
    return render(request, "shop/collections.html", {'catagory': catagory})

def collectionsview(request, name):
    if (Catagory.objects.filter(name=name, status=0)):
        products = Product.objects.filter(Catagory__name=name)
        return render(request, "shop/products/index.html", {'products': products,"category_name":name})
    else:
        messages.warning(request, "No Such Category Found")
        return redirect('collections')

def product_details(request, cname, pname):
    if (Catagory.objects.filter(name=cname, status=0).exists()):
        if (Product.objects.filter(name=pname, status=0).exists()):
            products = Product.objects.filter(name=pname, status=0).first()
            return render(request, "shop/products/product_details.html", {"product": products})
        else:
            messages.error(request, "No Such Product Found")
            return redirect('collections')
    else:
        messages.error(request, "No Such Category Found")
        return redirect('collections')

# def forgot_password(request):
#     return render(request, 'shop/forgot_password.html')
def add_to_cart(request):
    if request.headers.get('X-Requested-With')=='XMLHttpRequest':
        if request.user.is_authenticated:
            data=json.load(request)
            product_qty=(data['product_qty'])
            product_id=(data['pid'])
            # print(request.user.id)
            product_status=Product.objects.get(id=product_id)
            if product_status:
                if Cart.objects.filter(user=request.user.id,product_id=product_id):
                    return JsonResponse({'status':'Product already in cart'},status=200)
                else:
                    if product_status.quantity>=product_qty:
                        Cart.objects.create(user=request.user,product_id=product_id,product_qty=product_qty)
                        return JsonResponse({'status':'Product add to cart success'},status=200)
                    else:
                        return JsonResponse({'status':'Product stock not avavialble'},status=200)
                    
            return JsonResponse({'status':'Product add to cart success'},status=200)
        else:
            return JsonResponse({'status':'Login to add cart'},status=200)
    else:
        return JsonResponse({'status':'Ivalid Access'},status=200)
    

def cart_page(request):
    if request.user.is_authenticated:
        cart=Cart.objects.filter(user=request.user)
        return render(request, "shop/cart.html", {"cart": cart})
    else:
        messages.warning(request, "You need to log in to view your cart.")
        return redirect("/")
    
    
def remove_cart(request,cid):
    cartitem= Cart.objects.get(id=cid)
    cartitem.delete()
    return redirect("/cart/")



# def fav_page(request):
#     if request.headers.get('X-Requested-With')=='XMLHttpRequest':
#         if request.user.is_authenticated:
#             data=json.load(request)
#             product_id=(data['pid'])
#             product_status=Product.objects.get(id=product_id)
#             if product_status:
#                 if Favourite.objects.filter(user=request.user.id,product_id=product_id):
#                     return JsonResponse({'status':'Product already in fav'},status=200)
#                 else:
#                     Favourite.objects.create(user=request.user,product_id=product_id)        
#             return JsonResponse({'status':'Product add to fav success'},status=200)
#         else:
#             return JsonResponse({'status':'Login to add fav'},status=200)
#     else:
#         return JsonResponse({'status':'Ivalid Access'},status=200)

    



@login_required
def check_page(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.product.selling_price * item.product_qty for item in cart_items)
    
    if request.method == "POST":
        data = request.POST
        payment_method = data.get('payment_method')
        
        for item in cart_items:
            Order.objects.create(
                user=request.user,
                product=item.product,
                product_qty=item.product_qty,
                total_price=item.product.selling_price * item.product_qty,
                full_name=data.get('full_name'),
                email=data.get('email'),
                shipping_address=data.get('shipping_address'),
                payment_method=payment_method
            )
        
        # Clear the user's cart after purchase
        cart_items.delete()

        messages.success(request, "Order placed successfully!")
        return redirect('/cart/')
    
    return render(request, 'shop/check.html', {'cart_items': cart_items, 'total_price': total_price})

def about_us(request):
    return render(request, 'shop/aboutus.html')


# def contact_us(request):
#     return render(request, 'shop/contactus.html')


# def contact(request):
#     if request.method == 'POST':
#         name = request.POST['firstname']
#         email = request.POST['email']
#         message = request.POST['message']
#         Contactmessage.objects.create(first_name=full_name, email=email, message=message)
#         messages.success(request, 'Your message has been sent successfully!')
#         return redirect('/contact')
#     return render(request, "shop/contactus.html")



def product_search(request):
    query = request.GET.get('q')
    
    if query:
        products = Product.objects.filter(name__icontains=query)  # Filter by product name containing the query
        if not products:
            message = "No products found for your search query."
        else:
            message = ""
    else:
        products = None
        message = "Please enter a search term."

    context = {
        'products': products,
        'message': message
    }
    return render(request, 'shop/index.html', context)




def contact_us(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()  # Save the form data to the database
            messages.success(request, 'Your message has been sent successfully!')  # Add success message
            return redirect('contact_us')  # Redirect to the same page to clear the form
    else:
        form = ContactForm()
        
    return render(request, 'shop/contactus.html', {'form': form})


# def success_page(request):
#     return render(request, 'shop/success.html')

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Order

@login_required
def track_order(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'shop/track_order.html', {'orders': orders})
