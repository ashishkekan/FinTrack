import json
from decimal import Decimal

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import F
from django.shortcuts import redirect, render

from stocks.forms import LoginForm, SignUpForm
from stocks.models import StockTransaction


@login_required
def home(request):
    portfolio = {}
    total_value = Decimal("0.00")
    recent_transactions = []
    top_performer = None
    worst_performer = None
    transactions_json = []

    if request.user.is_authenticated:
        # Fetch transactions
        transactions = StockTransaction.objects.filter(user=request.user).order_by(
            "transaction_date"
        )
        recent_transactions = transactions.order_by("-transaction_date")[:5].annotate(
            total_cost=F("quantity") * F("price_per_share")
        )

        # Prepare transactions for Chart.js
        transactions_json = [
            {
                "stock_symbol": trans.stock_symbol,
                "price_per_share": float(trans.price_per_share),
                "transaction_date": trans.transaction_date.isoformat(),
            }
            for trans in transactions
        ]

        # Calculate portfolio
        for trans in transactions:
            symbol = trans.stock_symbol
            if symbol not in portfolio:
                portfolio[symbol] = {
                    "quantity": 0,
                    "total_cost": Decimal("0.00"),
                    "latest_price": trans.price_per_share,
                }

            if trans.transaction_type == "BUY":
                portfolio[symbol]["quantity"] += trans.quantity
                portfolio[symbol]["total_cost"] += (
                    trans.quantity * trans.price_per_share
                )
            else:  # SELL
                portfolio[symbol]["quantity"] -= trans.quantity
                portfolio[symbol]["total_cost"] -= (
                    trans.quantity * trans.price_per_share
                )
            portfolio[symbol]["latest_price"] = trans.price_per_share

        # Calculate average prices and performance
        for symbol, data in list(portfolio.items()):
            if data["quantity"] > 0:
                data["avg_price"] = data["total_cost"] / data["quantity"]
                total_value += data["quantity"] * data["latest_price"]
                # Calculate percentage gain/loss
                if data["avg_price"] > 0:
                    data["percent_change"] = (
                        (data["latest_price"] - data["avg_price"]) / data["avg_price"]
                    ) * 100
                else:
                    data["percent_change"] = Decimal("0.00")
            else:
                del portfolio[symbol]

        # Identify top and worst performers
        if portfolio:
            top_performer = max(
                portfolio.items(), key=lambda x: x[1]["percent_change"], default=None
            )
            worst_performer = min(
                portfolio.items(), key=lambda x: x[1]["percent_change"], default=None
            )
            if top_performer:
                top_performer = {
                    "symbol": top_performer[0],
                    "gain_percent": (
                        top_performer[1]["percent_change"]
                        if top_performer[1]["percent_change"] > 0
                        else None
                    ),
                    "avg_price": top_performer[1]["avg_price"],
                    "current_price": top_performer[1]["latest_price"],
                }
            if worst_performer:
                worst_performer = {
                    "symbol": worst_performer[0],
                    "loss_percent": (
                        abs(worst_performer[1]["percent_change"])
                        if worst_performer[1]["percent_change"] < 0
                        else None
                    ),
                    "avg_price": worst_performer[1]["avg_price"],
                    "current_price": worst_performer[1]["latest_price"],
                }

    return render(
        request,
        "home.html",
        {
            "portfolio": portfolio,
            "total_value": total_value,
            "recent_transactions": recent_transactions,
            "top_performer": top_performer,
            "worst_performer": worst_performer,
            "transactions_json": json.dumps(transactions_json),
        },
    )


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

    # Convert to list of dicts for pagination
    portfolio_list = [
        {"symbol": symbol, **details} for symbol, details in portfolio.items()
    ]

    # Set up pagination (10 items per page)
    paginator = Paginator(portfolio_list, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "portfolio.html", {"page_obj": page_obj})


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

    form = LoginForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Logged in successfully.")
                return redirect("home")
            else:
                messages.error(request, "Invalid username or password.")

    return render(request, "login.html", {"form": form})


def user_logout(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect("login")


def signup(request):
    if request.user.is_authenticated:
        return redirect("home")

    form = SignUpForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password1 = form.cleaned_data["password1"]

            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already taken.")
                return redirect("signup")

            if User.objects.filter(email=email).exists():
                messages.error(request, "Email already registered.")
                return redirect("signup")

            user = User.objects.create_user(
                username=username, email=email, password=password1
            )
            login(request, user)
            messages.success(request, "Account created successfully.")
            return redirect("home")

    return render(request, "signup.html", {"form": form})


@login_required
def avg_price_calculator(request):
    result = None
    existing_shares = None
    existing_total_shares = 0
    existing_total_cost = Decimal("0.00")
    stock_symbol = ""

    if request.method == "POST":
        stock_symbol = request.POST.get("stock_symbol").upper()
        quantities = request.POST.getlist("quantity[]")
        prices = request.POST.getlist("price[]")

        # Fetch existing buy transactions for the stock symbol
        buy_transactions = (
            StockTransaction.objects.filter(
                user=request.user, stock_symbol=stock_symbol, transaction_type="BUY"
            )
            .values("quantity", "price_per_share")
            .annotate(total_cost=F("quantity") * F("price_per_share"))
        )

        existing_shares = [
            {
                "quantity": trans["quantity"],
                "price_per_share": trans["price_per_share"],
                "total_cost": trans["total_cost"],
            }
            for trans in buy_transactions
        ]

        for trans in buy_transactions:
            existing_total_shares += trans["quantity"]
            existing_total_cost += trans["total_cost"]

        try:
            total_shares = existing_total_shares
            total_cost = existing_total_cost

            # Process new transactions
            for qty, price in zip(quantities, prices):
                qty = int(qty)
                price = Decimal(price)
                if qty <= 0 or price <= 0:
                    messages.error(request, "Quantity and price must be positive.")
                    return redirect("avg_price_calculator")
                total_shares += qty
                total_cost += qty * price

            if total_shares > 0:
                avg_price = total_cost / total_shares
                result = {
                    "stock_symbol": stock_symbol,
                    "total_shares": total_shares,
                    "total_cost": total_cost,
                    "avg_price": avg_price,
                }
            else:
                messages.error(
                    request,
                    "At least one valid transaction or existing share is required.",
                )
        except (ValueError, TypeError):
            messages.error(request, "Please enter valid quantities and prices.")

    return render(
        request,
        "avg_price_calculator.html",
        {
            "result": result,
            "existing_shares": existing_shares,
            "existing_total_shares": existing_total_shares,
            "existing_total_cost": existing_total_cost,
            "stock_symbol": stock_symbol,
        },
    )
