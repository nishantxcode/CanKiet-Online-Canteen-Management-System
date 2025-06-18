import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate,login
from django.utils.timezone import now
import uuid
from .forms import LoginForm
from .models import User,Items,Canteen,Order

client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))


def index2(request):
    user=User.objects.all()
    # Check if 'user_id' exists in the session
    if 'user' not in request.session:
        return redirect('login')  # Replace 'login' with the name of your login URL
    # If session exists, render the index page
    return render(request, 'cankiet/index2.html', {'user': user})

def galary(request):
    return render(request,'cankiet/galary.html',)

def login(request):
    user=User.objects.all()
    return render(request, 'cankiet/login.html', {'user': user})  

def logout(request):
    # Clear the session
    request.session.flush()  # Removes all session data
    return redirect('login')  # Redirect to the login page  
 
def orders(request):
    orders=Order.objects.all()
    user=User.objects.all()
    items=Items.objects.all()

    return render(request, 'cankiet/orders.html', {'user': user,'items':items,'order':orders})

def canteens(request,):
    canteen=Canteen.objects.all()
    return render(request, 'cankiet/canteens.html', {'canteen':canteen,})

def menu(request,c_no):
     # Fetch the selected canteen
    canteen = get_object_or_404(Canteen, c_no=c_no)
    # Fetch items for the selected canteen
    items = Items.objects.filter(c_no=canteen.c_no)
    # Pass data to the template
    return render(request, 'cankiet/menu.html', {'canteen': canteen, 'items': items})

def food(request,c_no):
     # Fetch the selected canteen
    canteen = get_object_or_404(Canteen, c_no=c_no)
    # Fetch items for the selected canteen
    items = Items.objects.filter(c_no=canteen.c_no)
    # Pass data to the template
    return render(request, 'cankiet/orderfoodpage.html', {'canteen': canteen, 'items': items})


def cart(request,c_no):
    
     canteen = get_object_or_404(Canteen, c_no=c_no)
     if request.method == 'POST':
         item_id = request.POST.get('i_no')
         quantity = int(request.POST.get('quantity', 1))
         # Fetch the item
         items = get_object_or_404(Items,i_no=item_id)
         total_amount=quantity*items.price

     return render(request, 'cankiet/cart.html',{'canteen': canteen, 'items': items,'quantity':quantity,'total':total_amount})

@csrf_exempt
def start_payment(request,c_no):
    if request.method == 'POST':
        canteen = get_object_or_404(Canteen,c_no=c_no)
        item_id = request.POST.get('i_no')
        quantity = int(request.POST.get('quantity', 1))
        items = get_object_or_404(Items,i_no=item_id)
        # total_amount=(quantity*items.price)*100
        total_amount= int(quantity*items.price*100)  # Convert to paisa

        razorpay_order = client.order.create({
            'amount':total_amount,
            'currency': 'INR',
            "payment_capture":1,  
        })

        order = Order.objects.create(
            item=items,
            razorpay_order_id=razorpay_order['id'],
            quantity=quantity,
            # total_amount=total_amount,
            c_no=canteen,  
            )
        return JsonResponse({
            "order_id": razorpay_order['id'],
            "razorpay_key_id": settings.RAZORPAY_KEY_ID,
            "product_name": items.item,
            "amount": total_amount,
            "razorpay_callback_url":settings.RAZORPAY_CALLBACK_URL
        })    

@csrf_exempt
def verify_payment(request):
    if "razorpay_signature" in request.POST:
        order_id = request.POST.get('razorpay_order_id')
        payment_id = request.POST.get('razorpay_payment_id')
        signature = request.POST.get('razorpay_signature')

        order = get_object_or_404(Order, razorpay_order_id=order_id)

        if client.utility.verify_payment_signature({
            'razorpay_order_id': order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
            }):
            order.payment_id = payment_id
            order.payment_signature = signature
            order.is_paid = True
            order.o_date = now()
            order.status = 'In Progress'
            order.save()
            return render(request, 'cankiet/confirmation.html', {'order': order})
        else:
            order.is_paid = False
            order.save()
            return JsonResponse({'status': 'Payment Failed'})
    else:
        return JsonResponse({'status': ' Failed'})
       

def login_check(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            u_id = form.cleaned_data['username']
            password = form.cleaned_data['password']

            try:
                user = User.objects.get(u_id=u_id)
                # Check if the entered password matches the hashed password
                if check_password(password, user.password):
                    # Store all user attributes in the session
                    request.session['user'] = {
                    'u_id': user.u_id,
                    'name': user.name,
                    'phone': user.phone,
                    'dept': user.branch,
                    }
                    return redirect('index2')
                else:
                    form.add_error(None, "Invalid User ID or Password")
            except User.DoesNotExist:
                form.add_error(None, "Invalid User ID or Password")
    else:
        form = LoginForm()

    return render(request, 'cankiet/login.html', {'form': form})   