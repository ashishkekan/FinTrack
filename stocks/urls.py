from django.urls import path

from . import views

urlpatterns = [
    path("home/", views.home, name="home"),
    path("portfolio/", views.portfolio, name="portfolio"),
    path("transaction/add/", views.add_transaction, name="add_transaction"),
    path("", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path("signup/", views.signup, name="signup"),
    path("calculator/", views.avg_price_calculator, name="avg_price_calculator"),
    path("search/", views.search_transactions, name="search_transactions"),
]
