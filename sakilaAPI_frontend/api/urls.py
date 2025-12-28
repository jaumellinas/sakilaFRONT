from django.urls import path
from api import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.login, name="login"),
    path("register/", views.register, name="register"),
    path("logout/", views.logout, name="logout"),
    path("customers/", views.customers_list, name="customers_list"),
    path(
        "customers/<int:customer_id>/",
        views.customer_detail,
        name="customer_detail"
    ),
    path(
        "customers/new/",
        views.customer_create,
        name="customer_create"
    ),
    path(
        "customers/<int:customer_id>/edit/",
        views.customer_update,
        name="customer_update"
    ),
    path(
        "customers/<int:customer_id>/delete/",
        views.customer_delete,
        name="customer_delete"
    ),
    path("rentals/", views.rentals_list, name="rentals_list"),
    path(
        "rentals/<int:rental_id>/",
        views.rental_detail,
        name="rental_detail"
    ),
    path("rentals/new/", views.rental_create, name="rental_create"),
    path(
        "rentals/<int:rental_id>/return/",
        views.rental_return,
        name="rental_return"
    ),
]