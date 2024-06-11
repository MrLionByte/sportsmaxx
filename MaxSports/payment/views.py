import razorpay
from django.conf import settings
from django.http import JsonResponse
from order_app import views


def initiate_payment(request):
    user = request.user

    selected_address = request.POST.get("selected_address")
    amount = float(request.POST["amount"])
    payment_mode = request.POST["payment_mode"]
    print("Working 1")
    request.session["selected_address"] = selected_address
    request.session["amount"] = amount
    request.session["payment_mode"] = payment_mode
    print("Working 2")
    if payment_mode == "razorpay":
        # Initiate Razorpay payment
        print("Working 3")
        payment_data = {
            "amount": int(amount * 100),  # Amount in paise
            "currency": "INR",
            "receipt": "order_receipt",
            "notes": {
                "email": request.user.email,
            },
        }
        print("Working 4")
        try:
            print("Working 5")
            client = razorpay.Client(
                auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET)
            )
            order = client.order.create(data=payment_data)
            print("Working 6")
            payment_info = {
                "amount": order["amount"],
                "currency": order["currency"],
                "key": settings.RAZORPAY_API_KEY,
                "name": "Sports-Maxx",
                "description": "Happy Shopping",
                "image": "{% static 'img/sport_max_fav.png' %}",
                "order_id": order["id"],
            }
            print("Working 7")
            print('PAYMENT', payment_info)
            if amount == 0.00:
                views.add_to_order(request)
            return JsonResponse(payment_info)

        except razorpay.errors.RazorpayError as e:
            print("Working 8")
            return JsonResponse({"error": str(e)}, status=500)


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
