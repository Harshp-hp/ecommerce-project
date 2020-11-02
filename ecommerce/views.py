from django.shortcuts import render, redirect, HttpResponseRedirect
from django.http import HttpResponse
from .models.product import Products
from .models.category import Category
from .models.customer import Customer
from django.views import View
from .models.orders import Order
from django.contrib.auth.hashers import check_password
# Create your views here.


class Index(View):

    def post(self, request):
        product=request.POST.get('product')
        remove=request.POST.get('remove')
        cart = request.session.get('cart')
        if cart:
            quantity=cart.get(product)
            if quantity:
                if remove:
                    if quantity <= 1:
                        cart.pop(product)
                    else:
                        cart[product]= quantity - 1
                else:
                    cart[product] = quantity + 1
            else:
                cart[product] = 1
        else:
            cart = {}
            cart[product] = 1

        request.session['cart']= cart
        print(request.session['cart'])
        return redirect('homepage')


    def get(self, request):
        cart =  request.session.get('cart')
        if not cart:
            request.session['cart'] = {}
        product = None

        categories = Category.get_all_categories()
        categoryID = request.GET.get('category')
        if categoryID:
            product = Products.get_all_products_by_categoryid(categoryID)
        else:
            product = Products.get_all_products();

        data = {}
        data['product'] = product
        data['categories'] = categories

        return render(request, 'index.html', data)



class Signup(View):
    def get(self, request):
        return render(request, 'signup.html')
    def post(self, request):
        postData = request.POST
        first_name = postData.get('firstname')
        last_name = postData.get('lastName')
        phone = postData.get('Phone')
        email = postData.get('email')
        password = postData.get('password')
        customer = Customer(first_name=first_name,
                            last_name=last_name,
                            phone=phone,
                            email=email,
                            password=password)
        customer.register()
        return redirect('homepage')


class Login(View):
    return_url = None
    def get(self, request):
        Login.return_url = request.GET.get('return_url')
        return render(request, 'login.html')
    def post(self, request):
            email = request.POST.get('email')
            password = request.POST.get('password')
            customer = Customer.get_customer_by_email(email)
            error_message = None
            request.session['customer'] = customer.id
            if Login.return_url:
                return HttpResponseRedirect(Login.return_url)
            else:
                Login.return_url = None
            return redirect('homepage')

class Cart(View):
    def get(self, request):
        ids = list(request.session.get('cart').keys())
        products = Products.get_products_by_id(ids)
        return render(request, 'cart.html', {'products': products})

class Checkout(View):
    def post(self, request):
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        customer = request.session.get('customer')
        cart = request.session.get('cart')
        products = Products.get_products_by_id(list(cart.keys()))
        print(address, phone, customer)

        for product in products:
            order = Order(customer = Customer(id = customer),
                          product = product,
                          price = product.price,
                          address=address,
                          phone = phone,
                          quantity = cart.get(str(product.id))
                          )
            order.save()
            request.session['cart'] = {}

        return redirect('cart')



class OrderView(View):
    def get(self, request):
        customer = request.session.get('customer')
        orders = Order.get_orders_by_customer(customer)
        print(orders)
        return render(request, 'order.html', {'orders': orders})

def logout(request):
    request.session.clear()
    return redirect('login')











