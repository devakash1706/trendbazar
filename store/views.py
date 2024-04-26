from django.shortcuts import render,redirect
from django.views.generic import View
from store.forms import RegistrationForm,LoginForm
from django.contrib.auth import authenticate,login,logout
from store.models import Product,Size,Basket,BasketItem,Order
from django.utils.decorators import method_decorator
import razorpay
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

KEY_ID="rzp_test_razrayRFz14CME"
KEY_SECRET="IriOERiba50kWdWbdbAPI1Qq"
class SignUpView(View):
    def get(self,request,*args,**kwargs):
        form=RegistrationForm()
        return render(request,'register.html',{'form':form})
    def post(self,request,*args,**kwargs):
        form=RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('signin')
        else:
            return render(request,'login.html',{'form':form})
    
class SignInView(View):
    def get(self,request,*args,**kwargs):
        form=LoginForm()
        return render(request,'login.html',{'form':form})
    def post(self,request,*args,**kwargs):
        form=LoginForm(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            user_object=authenticate(request,username=uname,password=pwd)
            if user_object:
                login(request,user_object)
                print('sucess')
                return redirect('home')
        print('error')
        return render(request,'login.html',{'form':form})

class HomeView(View):
    def get(self,request,*args,**kwargs):
        qs=Product.objects.all()
        return render(request,'home.html',{"data":qs})
    
class ProductDetailView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get('pk')
        qs=Product.objects.get(id=id)
        return render(request,'product_detail.html',{'data':qs})
    

class AddToCartView(View):
    def post(self,request,*args,**kwargs):
        id=kwargs.get('pk')
        product_obj=Product.objects.get(id=id)
        size_name=request.POST.get('size')
        size_obj=Size.objects.get(name=size_name)
        # basket_obj=Basket.objects.get(owner=request.user)
        basket_obj=request.user.cart
        BasketItem.objects.create(
            basket_object=basket_obj,
            product_object=product_obj,
            size_object=size_obj,
        )
        return redirect('cart-list')
    
class CartItemListView(View):
    def get(self,request,*args,**kwargs):
        qs=request.user.cart.cartitems.filter(is_order_placed=False)
        return render(request,'cart_items.html',{"data":qs})


class BasketItemDeleteView(View):
     def get(self,request,*args,**kwargs):
         id=kwargs.get('pk')
         basket_item_object=BasketItem.objects.get(id=id)
         basket_item_object.delete()
         return redirect('cart-list')

# url:localhost8000/basket/item(id)/quantity/change   
class BasketItemUpdateView(View):
    def post(self,request,*args,**kwargs):
        id=kwargs.get('pk')
        basket_item_obj=BasketItem.objects.get(id=id)
        action=request.POST.get("action")
        if action=="inc":
            basket_item_obj.quantity+=1
        elif action=='dec':
            basket_item_obj.quantity-=1
        basket_item_obj.save()
        return redirect('cart-list')
class CheckoutView(View):
    def get(self,request,*args,**kwargs):
        return render(request,'checkout.html')

    def post(self,request,*args,**kwargs):
        phone=request.POST.get("phone")
        email=request.POST.get("email")
        address=request.POST.get("delivery_address")
        payment_method=request.POST.get("payment_mode")
        user_object=request.user
        basket_item_objects=user_object.cart.get_cart_items()
        order_object=Order.objects.create(
            user_object=user_object,
            delivery_address=address,
            phone=phone,
            email=email,
            payment_mode=payment_method,
        )

        for bi in basket_item_objects:
            order_object.basket_item_objects.add(bi)
            bi.is_order_placed=True
            bi.save()
        if payment_method=="online" and order_object:
            client = razorpay.Client(auth=(KEY_ID, KEY_SECRET))
            total_amount=order_object.order_total*100
            data = {"amount": total_amount, "currency": "INR", "receipt": "order_rcptid_11"}
            payment = client.order.create(data=data)
            order_object.order_id=payment.get('id')
            order_object.save()
            data={"order_id":payment.get('id'),'key_id':KEY_ID,'amount':'total_amount'}
            return render(request,'payment.html',{'data':data})
        return redirect("orders")

class MyOrdersView(View):
    def get(self, request, *args, **kwargs):
        qs=Order.objects.filter(user_object=request.user).exclude(status='cancelled')
        return render(request,'myorder.html',{'data':qs})


@method_decorator(csrf_exempt,name="dispatch")
class PaymentVerificationView(View):
    def post(self, request, *args, **kwargs):
        data=request.POST
        client = razorpay.Client(auth=(KEY_ID, KEY_SECRET))
        try:
            client.utility.verify_payment_signature(data)
            print('payment sucess')
        except:
            print('payment failed')
        return redirect('home')



