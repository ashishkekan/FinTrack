from decimal import Decimal

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render

from stocks.models import StockTransaction


@login_required
def home(request):
    return render(request, "home.html")


@login_required
def portfolio(request):
    transactions = StockTransaction.objects.filter(user=request.user)
    portfolio = {}

    for trans in transactions:
        symbol = trans.stock_symbol
        if symbol not in portfolio:
            portfolio[symbol] = {"quantity": 0, "total_cost": Decimal("0.00")}

        if trans.transaction_type == "BUY":
            portfolio[symbol]["quantity"] += trans.quantity
            portfolio[symbol]["total_cost"] += trans.quantity * trans.price_per_share
        else:  # SELL
            portfolio[symbol]["quantity"] -= trans.quantity
            portfolio[symbol]["total_cost"] -= trans.quantity * trans.price_per_share

    for symbol, data in portfolio.items():
        if data["quantity"] > 0:
            data["avg_price"] = data["total_cost"] / data["quantity"]
        else:
            data["avg_price"] = Decimal("0.00")
            data["quantity"] = 0

    portfolio = {k: v for k, v in portfolio.items() if v["quantity"] > 0}

    return render(request, "portfolio.html", {"portfolio": portfolio})


@login_required
def add_transaction(request):
    if request.method == "POST":
        stock_symbol = request.POST.get("stock_symbol").upper()
        transaction_type = request.POST.get("transaction_type")
        try:
            quantity = int(request.POST.get("quantity"))
            price_per_share = Decimal(request.POST.get("price_per_share"))
        except (ValueError, TypeError):
            messages.error(request, "Please enter valid quantity and price.")
            return redirect("add_transaction")

        if quantity <= 0 or price_per_share <= 0:
            messages.error(request, "Quantity and price must be positive.")
            return redirect("add_transaction")

        if not request.user.is_staff:
            StockTransaction.objects.create(
                user=request.user,
                stock_symbol=stock_symbol,
                transaction_type=transaction_type,
                quantity=quantity,
                price_per_share=price_per_share,
            )
        else:
            user_id = request.POST.get("user_id")
            if user_id:
                user = User.objects.get(id=user_id)
            else:
                user = request.user
            StockTransaction.objects.create(
                user=user,
                stock_symbol=stock_symbol,
                transaction_type=transaction_type,
                quantity=quantity,
                price_per_share=price_per_share,
            )
        messages.success(request, "Transaction added successfully.")
        return redirect("portfolio")

    users = User.objects.all() if request.user.is_staff else None
    return render(request, "transaction_form.html", {"users": users})


def user_login(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Logged in successfully.")
            return redirect("home")
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, "login.html")


def user_logout(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect("home")


def signup(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect("signup")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return redirect("signup")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return redirect("signup")

        user = User.objects.create_user(
            username=username, email=email, password=password1
        )
        user.save()
        login(request, user)
        messages.success(request, "Account created successfully.")
        return redirect("home")

    return render(request, "signup.html")
