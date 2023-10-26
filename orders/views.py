from django.shortcuts import render, redirect
from urllib import response
from django.http import HttpResponse, JsonResponse
from marketplace.models import Cart, Tax
from .utils import generate_order_number
from marketplace.context_processor import get_cart_amounts
from .forms import OrderForm
from .models import Order, OrderedFood, Payment
import simplejson as json
from accounts.utils import send_notification
from menu.models import FoodItem
# Create your views here.


def place_order(request):
    cart_items = Cart.objects.filter(user=request.user).order_by('created_at')
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('marketplace')
    
    vendors_ids = []
    for i in cart_items:
        if i.fooditem.vendor.id not in vendors_ids:
            vendors_ids.append(i.fooditem.vendor.id)
    
    get_tax = Tax.objects.filter(is_active=True)
    subtotal = 0
    total_data = {}
    k = {}
    for i in cart_items:
        fooditem = FoodItem.objects.get(pk=i.fooditem.id, vendor_id__in=vendors_ids)
        v_id = fooditem.vendor.id
        if v_id in k:
            subtotal = k[v_id]
            subtotal += (fooditem.price * i.quantity)
            k[v_id] = subtotal
        else:
            subtotal = (fooditem.price * i.quantity)
            k[v_id] = subtotal
    
        # Calculate the tax_data
        tax_dict = {}
        for i in get_tax:
            tax_type = i.tax_type
            tax_percentage = i.tax_percentage
            tax_amount = round((tax_percentage * subtotal)/100, 2)
            tax_dict.update({tax_type: {str(tax_percentage) : str(tax_amount)}})
        # Construct total data
        total_data.update({fooditem.vendor.id: {str(subtotal): str(tax_dict)}})
    


    subtotal = get_cart_amounts(request)['subtotal']
    total_tax = get_cart_amounts(request)['tax']
    grand_total = get_cart_amounts(request)['grand_total']
    tax_data = get_cart_amounts(request)['tax_dict']

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = Order()
            order.first_name = form.cleaned_data['first_name']
            order.last_name = form.cleaned_data['last_name']
            order.phone = form.cleaned_data['phone']
            order.email = form.cleaned_data['email']
            order.address = form.cleaned_data['address']
            order.country = form.cleaned_data['country']
            order.state = form.cleaned_data['state']
            order.city = form.cleaned_data['city']
            order.pin_code = form.cleaned_data['pin_code']
            order.user = request.user
            order.total = grand_total
            order.tax_data = json.dumps(tax_data)
            order.total_data = json.dumps(total_data)
            order.total_tax = total_tax
            order.payment_method = request.POST['payment_method']
            order.save() 
            order.order_number = generate_order_number(order.id)
            order.vendors.add(*vendors_ids)
            order.save()

            context = {
                'order': order,
                'cart_items': cart_items,
            }
            return render(request, 'orders/place_order.html', context)
        else:
            print(form.errors)      

    return render(request,'orders/place_order.html')




def payments(request):
    # check request ajax 
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == 'POST':
        # STORE THE PAYMENT DETAILS IN THE PAYMENT MODEL
        order_number = request.POST.get('order_number')
        transaction_id = request.POST.get('transaction_id')
        payment_method = request.POST.get('payment_method')
        status = request.POST.get('status')
        print(order_number, transaction_id, payment_method, status)

        order = Order.objects.get(user=request.user, order_number=order_number)
        payment = Payment(
            user = request.user,
            transaction_id = transaction_id,
            amount = order.total,
            payment_method = payment_method,
            status = status,
        )
        payment.save()

        #update order model

        order.payment=payment
        order.is_ordered=True
        order.save()

        #move order to order food
        cart_items =Cart.objects.filter(user=request.user)
        for item in cart_items:
            ordered_food = OrderedFood()
            ordered_food.order = order
            ordered_food.payment = payment
            ordered_food.user = request.user
            ordered_food.fooditem = item.fooditem
            ordered_food.quantity = item.quantity
            ordered_food.price = item.fooditem.price
            ordered_food.amount = item.fooditem.price * item.quantity
            ordered_food.save()
        # SEND ORDER CONFIRMATION EMAIL TO THE CUSTOMER
        mail_subject = 'Thank you for ordering with us.'
        mail_template = 'orders/order_confirmation_email.html'

    
        context = {
            'user': request.user,
            'order': order,
            'to_email': order.email,
            
        }
        #send_notification(mail_subject, mail_template, context)


        #send order received  email  to  the  vendor


        mail_subject = 'You Have Received A New Order.'
        mail_template = 'orders/new_order_received.html'

        to_email=[]
        for i in cart_items:
            if i.fooditem.vendor.user.email not in to_email:
                to_email.append(i.fooditem.vendor.user.email)

    
        context = {
            
            'order': order,
            'to_email': to_email,
            
        }
        

        #send_notification(mail_subject, mail_template, context)

        #CLEAR THE CART IF THE PAYMENT IS SUCCESS
        cart_items.delete()
        response={
            'order_number': order_number,
            'transaction_id':transaction_id
        }
        return JsonResponse(response)    
    return HttpResponse('test')




def order_complete(request):

    order_number = request.GET.get('order_no')
    transaction_id = request.GET.get('trans_id')

    try:
        order = Order.objects.get(order_number=order_number, payment__transaction_id=transaction_id, is_ordered=True)
        ordered_food = OrderedFood.objects.filter(order=order)
        context = {
            'order': order,
            'ordered_food':ordered_food,
        }
        return render(request,'orders/order_complete.html', context)
    except:
        return redirect('index')