from django import forms
from django.contrib.auth.models import User

from stocks.models import StockTransaction


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(
            attrs={
                "class": "w-full p-3 border rounded-lg focus:border-indigo-600 focus:outline-none"
            }
        ),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "w-full p-3 border rounded-lg focus:border-indigo-600 focus:outline-none"
            }
        )
    )


class SignUpForm(forms.ModelForm):
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={
                "class": "w-full p-3 border rounded-lg focus:border-indigo-600 focus:outline-none"
            }
        ),
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(
            attrs={
                "class": "w-full p-3 border rounded-lg focus:border-indigo-600 focus:outline-none"
            }
        ),
    )

    class Meta:
        model = User
        fields = ["username", "email"]
        widgets = {
            "username": forms.TextInput(
                attrs={
                    "class": "w-full p-3 border rounded-lg focus:border-indigo-600 focus:outline-none"
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "w-full p-3 border rounded-lg focus:border-indigo-600 focus:outline-none"
                }
            ),
        }

    def clean(self):
        super().clean()
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match.")

        return self.cleaned_data


class StockTransactionForm(forms.ModelForm):
    class Meta:
        model = StockTransaction
        fields = ["stock_symbol", "transaction_type", "quantity", "price_per_share"]
        widgets = {
            "stock_symbol": forms.TextInput(
                attrs={
                    "class": "w-full p-3 border rounded-lg focus:border-indigo-600 focus:outline-none"
                }
            ),
            "transaction_type": forms.Select(
                attrs={
                    "class": "w-full p-3 border rounded-lg focus:border-indigo-600 focus:outline-none"
                }
            ),
            "quantity": forms.NumberInput(
                attrs={
                    "class": "w-full p-3 border rounded-lg focus:border-indigo-600 focus:outline-none"
                }
            ),
            "price_per_share": forms.NumberInput(
                attrs={
                    "step": "0.01",
                    "class": "w-full p-3 border rounded-lg focus:border-indigo-600 focus:outline-none",
                }
            ),
        }


class AdminStockTransactionForm(StockTransactionForm):
    user_id = forms.ModelChoiceField(
        queryset=User.objects.all(),
        required=False,
        label="User",
        widget=forms.Select(
            attrs={
                "class": "w-full p-3 border rounded-lg focus:border-indigo-600 focus:outline-none"
            }
        ),
    )
