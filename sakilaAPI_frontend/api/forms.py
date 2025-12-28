from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=50,
        widget=forms.TextInput(
            attrs={
                "class": "input",
                "placeholder": "Usuario",
                "required": "required"
            }
        )
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "input",
                "placeholder": "Contraseña",
                "required": "required"
            }
        )
    )

class RegisterForm(forms.Form):
    username = forms.CharField(
        max_length=50,
        widget=forms.TextInput(
            attrs={
                "class": "input",
                "placeholder": "Usuario",
                "required": "required"
            }
        )
    )

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": "input",
                "placeholder": "E-mail",
                "required": "required"
            }
        )
    )

    password = forms.CharField(
        min_length=8,
        max_length=72,
        widget=forms.PasswordInput(
            attrs={
                "class": "input",
                "placeholder": "Contraseña (mín. 8 caracteres)",
                "required": "required"
            }
        )
    )

    password_confirm = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "input",
                "placeholder": "Confirmar contraseña",
                "required": "required"
            }
        )
    )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm:
            if password != password_confirm:
                raise forms.ValidationError(
                    "Las contraseñas no coinciden"
                )
        return cleaned_data


class CustomerForm(forms.Form):
    store_id = forms.IntegerField(
        min_value=1,
        widget=forms.NumberInput(
            attrs={
                "class": "input",
                "placeholder": "ID de tienda",
                "required": "required"
            }
        )
    )

    first_name = forms.CharField(
        max_length=45,
        widget=forms.TextInput(
            attrs={
                "class": "input",
                "placeholder": "Nombre",
                "required": "required"
            }
        )
    )

    last_name = forms.CharField(
        max_length=45,
        widget=forms.TextInput(
            attrs={
                "class": "input",
                "placeholder": "Apellido(s)",
                "required": "required"
            }
        )
    )

    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(
            attrs={
                "class": "input",
                "placeholder": "E-mail (opcional)"
            }
        )
    )

    address_id = forms.IntegerField(
        min_value=1,
        widget=forms.NumberInput(
            attrs={
                "class": "input",
                "placeholder": "ID de dirección",
                "required": "required"
            }
        )
    )

    active = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(
            attrs={"class": "checkbox"}
        ),
        label="Cliente activo"
    )

class RentalForm(forms.Form):
    inventory_id = forms.IntegerField(
        min_value=1,
        widget=forms.NumberInput(
            attrs={
                "class": "input",
                "placeholder": "ID de inventario",
                "required": "required"
            }
        )
    )

    customer_id = forms.IntegerField(
        min_value=1,
        widget=forms.NumberInput(
            attrs={
                "class": "input",
                "placeholder": "ID de cliente",
                "required": "required"
            }
        )
    )

    staff_id = forms.IntegerField(
        min_value=1,
        widget=forms.NumberInput(
            attrs={
                "class": "input",
                "placeholder": "ID de personal (staff)",
                "required": "required"
            }
        )
    )