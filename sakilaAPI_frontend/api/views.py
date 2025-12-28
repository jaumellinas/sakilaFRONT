from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from api.api_client import APIClient
from api.forms import (
    LoginForm,
    RegisterForm,
    CustomerForm,
    RentalForm,
)
from datetime import datetime

def format_datetime(iso_string):
    if not iso_string:
        return None
    try:
        dt = datetime.fromisoformat(
            iso_string.replace("Z", "+00:00")
        )
        return dt.strftime("%d/%m/%Y %H:%M")
    except:
        return iso_string

def format_rentals(rentals):
    for rental in rentals:
        if rental.get("rental_date"):
            rental["rental_date"] = format_datetime(
                rental["rental_date"]
            )
        if rental.get("return_date"):
            rental["return_date"] = format_datetime(
                rental["return_date"]
            )
    return rentals

def format_customer(customer):
    if customer.get("create_date"):
        customer["create_date"] = format_datetime(
            customer["create_date"]
        )
    return customer

def get_token_from_session(request):
    return request.session.get("access_token")

def home(request):
    return render(request, "home.html")

@require_http_methods(["GET", "POST"])
def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            try:
                client = APIClient()
                response = client.login(
                    form.cleaned_data["username"],
                    form.cleaned_data["password"]
                )
                request.session["access_token"] = (
                    response["access_token"]
                )
                request.session["username"] = (
                    form.cleaned_data["username"]
                )
                messages.success(request, "Sesión iniciada correctamente")
                return redirect("home")
            except Exception as e:
                messages.error(request, f"Error: {str(e)}")
    else:
        form = LoginForm()
    return render(request, "login.html", {"form": form})

@require_http_methods(["GET", "POST"])
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            try:
                client = APIClient()
                client.register(
                    form.cleaned_data["username"],
                    form.cleaned_data["email"],
                    form.cleaned_data["password"]
                )
                messages.success(
                    request,
                    "Usuario registrado correctamente. Ya puedes iniciar sesión"
                )
                return redirect("login")
            except Exception as e:
                messages.error(request, f"Error: {str(e)}")
    else:
        form = RegisterForm()
    return render(request, "register.html", {"form": form})

def logout(request):
    request.session.flush()
    messages.success(request, "Sesión cerrada correctamente. ¡Hasta pronto!")
    return redirect("home")


def customers_list(request):
    from django.core.paginator import Paginator

    token = get_token_from_session(request)
    if not token:
        messages.warning(request, "Acceso denegado. Por favor, inicia sesión con tu usuario")
        return redirect("login")

    try:
        client = APIClient(token)
        customers_list = client.get_customers()

        for customer in customers_list:
            format_customer(customer)

        paginator = Paginator(customers_list, 100)
        page_number = request.GET.get('page')
        customers = paginator.get_page(page_number)

        return render(
            request,
            "customers/list.html",
            {"customers": customers}
        )
    except Exception as e:
        messages.error(request, f"Error: {str(e)}")
        return redirect("home")

def customer_detail(request, customer_id):
    token = get_token_from_session(request)
    if not token:
        return redirect("login")

    try:
        client = APIClient(token)
        customer = client.get_customer(customer_id)
        format_customer(customer)
        rentals = client.get_customer_rentals(customer_id)

        format_rentals(rentals)

        return render(
            request,
            "customers/detail.html",
            {"customer": customer, "rentals": rentals}
        )
    except Exception as e:
        messages.error(request, f"Error: {str(e)}")
        return redirect("customers_list")

@require_http_methods(["GET", "POST"])
def customer_create(request):
    token = get_token_from_session(request)
    if not token:
        return redirect("login")

    if request.method == "POST":
        form = CustomerForm(request.POST)
        if form.is_valid():
            try:
                client = APIClient(token)
                data = {
                    "store_id": form.cleaned_data["store_id"],
                    "first_name": form.cleaned_data["first_name"],
                    "last_name": form.cleaned_data["last_name"],
                    "email": form.cleaned_data["email"] or None,
                    "address_id": form.cleaned_data["address_id"],
                    "active": form.cleaned_data["active"],
                }
                client.create_customer(data)
                messages.success(request, "Cliente creado correctamente")
                return redirect("customers_list")
            except Exception as e:
                messages.error(request, f"Error: {str(e)}")
    else:
        form = CustomerForm()

    return render(request, "customers/form.html", {"form": form})


@require_http_methods(["GET", "POST"])
def customer_update(request, customer_id):
    token = get_token_from_session(request)
    if not token:
        return redirect("login")

    try:
        client = APIClient(token)
        customer = client.get_customer(customer_id)

        if request.method == "POST":
            form = CustomerForm(request.POST)
            if form.is_valid():
                data = {
                    "store_id": form.cleaned_data["store_id"],
                    "first_name": form.cleaned_data["first_name"],
                    "last_name": form.cleaned_data["last_name"],
                    "email": form.cleaned_data["email"] or None,
                    "address_id": form.cleaned_data["address_id"],
                    "active": form.cleaned_data["active"],
                }
                client.update_customer(customer_id, data)
                messages.success(request, "Cliente actualizado correctamente")
                return redirect(
                    "customer_detail",
                    customer_id=customer_id
                )
        else:
            form = CustomerForm(initial={
                "store_id": customer["store_id"],
                "first_name": customer["first_name"],
                "last_name": customer["last_name"],
                "email": customer["email"],
                "address_id": customer["address_id"],
                "active": customer["active"],
            })

        return render(
            request,
            "customers/form.html",
            {"form": form, "customer": customer}
        )
    except Exception as e:
        messages.error(request, f"Error: {str(e)}")
        return redirect("customers_list")


@require_http_methods(["GET", "POST"])
def customer_delete(request, customer_id):
    token = get_token_from_session(request)
    if not token:
        return redirect("login")

    try:
        client = APIClient(token)
        customer = client.get_customer(customer_id)

        if request.method == "POST":
            try:
                client.delete_customer(customer_id)
                messages.success(request, "Cliente eliminado")
                return redirect("customers_list")
            except Exception as e:
                error_msg = str(e)
                if "409" in error_msg or "existing rentals" in error_msg:
                    messages.error(
                        request,
                        "No se puede eliminar este cliente, ya que tiene reservas activas asociadas."
                    )
                    return redirect("customers_list")
                else:
                    messages.error(request, f"Error: {error_msg}")
                    return redirect("customers_list")
                return render(
                    request,
                    "customers/delete.html",
                    {"customer": customer}
                )

        return render(
            request,
            "customers/delete.html",
            {"customer": customer}
        )
    except Exception as e:
        messages.error(request, f"Error: {str(e)}")
        return redirect("customers_list")

def rentals_list(request):
    from django.core.paginator import Paginator

    token = get_token_from_session(request)
    if not token:
        return redirect("login")

    try:
        client = APIClient(token)
        rentals_list = client.get_rentals()

        format_rentals(rentals_list)

        paginator = Paginator(rentals_list, 50)
        page_number = request.GET.get('page')
        rentals = paginator.get_page(page_number)

        return render(
            request,
            "rentals/list.html",
            {"rentals": rentals}
        )
    except Exception as e:
        messages.error(request, f"Error: {str(e)}")
        return redirect("home")

def rental_detail(request, rental_id):
    token = get_token_from_session(request)
    if not token:
        return redirect("login")

    try:
        client = APIClient(token)
        rental = client.get_rental(rental_id)

        if rental.get("rental_date"):
            rental["rental_date"] = format_datetime(
                rental["rental_date"]
            )
        if rental.get("return_date"):
            rental["return_date"] = format_datetime(
                rental["return_date"]
            )

        return render(
            request,
            "rentals/detail.html",
            {"rental": rental}
        )
    except Exception as e:
        messages.error(request, f"Error: {str(e)}")
        return redirect("rentals_list")

@require_http_methods(["GET", "POST"])
def rental_create(request):
    token = get_token_from_session(request)
    if not token:
        return redirect("login")

    if request.method == "POST":
        form = RentalForm(request.POST)
        if form.is_valid():
            try:
                client = APIClient(token)
                data = {
                    "rental_date": datetime.now().isoformat(),
                    "inventory_id": (
                        form.cleaned_data["inventory_id"]
                    ),
                    "customer_id": form.cleaned_data["customer_id"],
                    "staff_id": form.cleaned_data["staff_id"],
                }
                client.create_rental(data)
                messages.success(request, "Reserva creada correctamente")
                return redirect("rentals_list")
            except Exception as e:
                messages.error(request, f"Error: {str(e)}")
    else:
        form = RentalForm()

    return render(request, "rentals/form.html", {"form": form})

@require_http_methods(["POST"])
def rental_return(request, rental_id):
    token = get_token_from_session(request)
    if not token:
        return redirect("login")

    try:
        client = APIClient(token)
        client.return_rental(rental_id)
        messages.success(request, "Reserva devuelta correctamente")
        return redirect("rental_detail", rental_id=rental_id)
    except Exception as e:
        messages.error(request, f"Error: {str(e)}")
        return redirect("rentals_list")