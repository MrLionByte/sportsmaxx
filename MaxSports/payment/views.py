import razorpay
from django.conf import settings
from django.http import JsonResponse
from order_app import views
from django.shortcuts import render, redirect


def initiate_payment(request):
    user = request.user

    selected_address = request.POST.get("selected_address")
    amount = float(request.POST["amount"])
    payment_mode = 'razorpay'
    order_id = request.POST.get("order_id")
    request.session["selected_address"] = selected_address
    request.session["amount"] = amount
    request.session["payment_mode"] = payment_mode
    if order_id:
        request.session["order_id"] = order_id
    if payment_mode == "razorpay":
        payment_data = {
            "amount": int(amount * 100),  
            "currency": "INR",
            "receipt": "order_receipt",
            "notes": {
                "email": request.user.email,
            },
        }
        try:
            client = razorpay.Client(
                auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET)
            )
            order = client.order.create(data=payment_data)
            payment_info = {
                "amount": order["amount"],
                "currency": order["currency"],
                "key": settings.RAZORPAY_API_KEY,
                "name": "Sports-Maxx",
                "description": "Happy Shopping",
                "image": "{% static 'img/sport_max_fav.png' %}",
                "order_id": order["id"],
            }
            return JsonResponse(payment_info)

        except razorpay.errors.RazorpayError as e:
            return JsonResponse({"error": str(e)}, status=500)


def payment_failure(request):
    user = request.user
    request.session["amount"] = 0.00
    request.session["payment_mode"] = 'None'

    payment_info = None
            
    return redirect('add_to_order')


def initiate_payment_for_wallet(request):
    if request.method == "POST":
        amount = float(request.POST.get("amount", 0))
        payment_id = request.POST.get("payment_id")
        request.session["wallet_amount"] = amount
        request.session["wallet_payment_id"] = payment_id
        payment_data = {
            "amount": int(amount * 100),  # Amount in paise
            "currency": "INR",
            "receipt": "order_receipt",
            "notes": {
                "email": request.user.email,
            },
        }
        try:
            client = razorpay.Client(
                auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET)
            )
            order = client.order.create(data=payment_data)
            payment_info = {
                "amount": order["amount"],
                "currency": order["currency"],
                "key": settings.RAZORPAY_API_KEY,
                "name": "Sports-Maxx",
                "description": "Happy Shopping",
                "image": "{% static 'img/sport_max_fav.png' %}",  # Ensure this path is correct
                "order_id": order["id"],
            }
            return JsonResponse(payment_info)

        except razorpay.errors.RazorpayError as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Invalid request"}, status=400)


