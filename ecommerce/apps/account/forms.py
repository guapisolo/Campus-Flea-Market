from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordResetForm,
    SetPasswordForm,
)

from ecommerce.apps.catalogue.models import Product, ProductImage

from .models import Address, Customer


class UserAddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ["full_name", "phone", "address_line", "address_line2", "town_city", "postcode"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["full_name"].widget.attrs.update(
            {"class": "form-control mb-2 account-form", "placeholder": "姓名"}
        )
        self.fields["phone"].widget.attrs.update({"class": "form-control mb-2 account-form", "placeholder": "电话"})
        self.fields["address_line"].widget.attrs.update(
            {"class": "form-control mb-2 account-form", "placeholder": "地址"}
        )
        self.fields["address_line2"].widget.attrs.update(
            {"class": "form-control mb-2 account-form", "placeholder": "详细地址"}
        )
        self.fields["town_city"].widget.attrs.update(
            {"class": "form-control mb-2 account-form", "placeholder": "省市"}
        )
        self.fields["postcode"].widget.attrs.update(
            {"class": "form-control mb-2 account-form", "placeholder": "邮编"}
        )


class UserLoginForm(AuthenticationForm):

    username = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control mb-3", "placeholder": "邮箱", "id": "login-username"})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "密码",
                "id": "login-pwd",
            }
        )
    )


class RegistrationForm(forms.ModelForm):

    name = forms.CharField(label="输入用户名", min_length=4, max_length=50, help_text="必填")
    email = forms.EmailField(
        max_length=100, help_text="必填", error_messages={"required": "必须填写邮箱"}
    )
    password = forms.CharField(label="密码", widget=forms.PasswordInput)
    password2 = forms.CharField(label="重复密码", widget=forms.PasswordInput)

    class Meta:
        model = Customer
        fields = (
            "name",
            "email",
        )

    def clean_username(self):
        name = self.cleaned_data["name"].lower()
        r = Customer.objects.filter(name=name)
        if r.count():
            raise forms.ValidationError("该用户名已存在")
        return name

    def clean_password2(self):
        cd = self.cleaned_data
        if cd["password"] != cd["password2"]:
            raise forms.ValidationError("两次密码不一致")
        return cd["password2"]

    def clean_email(self):
        email = self.cleaned_data["email"]
        if Customer.objects.filter(email=email).exists():
            raise forms.ValidationError("该邮箱已被注册")
        return email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].widget.attrs.update({"class": "form-control mb-3", "placeholder": "用户名"})
        self.fields["email"].widget.attrs.update(
            {"class": "form-control mb-3", "placeholder": "邮箱", "name": "email", "id": "id_email"}
        )
        self.fields["password"].widget.attrs.update({"class": "form-control mb-3", "placeholder": "密码"})
        self.fields["password2"].widget.attrs.update({"class": "form-control", "placeholder": "重复密码"})


class PwdResetForm(PasswordResetForm):

    email = forms.EmailField(
        max_length=254,
        widget=forms.TextInput(attrs={"class": "form-control mb-3", "placeholder": "您的邮箱", "id": "form-email"}),
    )

    def clean_email(self):
        email = self.cleaned_data["email"]
        u = Customer.objects.filter(email=email)
        if not u:
            raise forms.ValidationError("很抱歉，我们无法找到该邮箱的用户信息")
        return email


class PwdResetConfirmForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label="新密码",
        widget=forms.PasswordInput(
            attrs={"class": "form-control mb-3", "placeholder": "请输入您的新密码", "id": "form-newpass"}
        ),
    )
    new_password2 = forms.CharField(
        label="重复新密码",
        widget=forms.PasswordInput(
            attrs={"class": "form-control mb-3", "placeholder": "请再次输入您的新密码", "id": "form-new-pass2"}
        ),
    )


class UserEditForm(forms.ModelForm):

    email = forms.EmailField(
        label="账号邮箱 (不可修改)",
        max_length=200,
        widget=forms.TextInput(
            attrs={"class": "form-control mb-3", "placeholder": "邮箱", "id": "form-email", "readonly": "readonly"}
        ),
    )

    mobile = forms.IntegerField(
        label="手机号",
        widget=forms.TextInput(
            attrs={"class": "form-control mb-3", "placeholder": "手机号", "id": "mobile"}
        ),
    )

    resume = forms.CharField(
        label="个人简介",
        max_length=1000,
        widget=forms.Textarea(
            attrs={"class": "form-control mb-3", "rows":"7", "placeholder": "一个自我介绍", "id": "resume"},
        ),
    )

    class Meta:
        model = Customer
        fields = ("email","mobile","resume")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].required = True


class ProductAddForm(forms.ModelForm):
    class Meta:
        model = Product  # 基于该Model的表单
        exclude = ("seller", "users_wishlist")
        # fields = ["title"]
    
    def __init__(self, *args, **kwargs) :
        super().__init__(*args, **kwargs)
        self.fields["category"].widget.attrs.update(
            {"class": "form-select mb-2", "placeholder": ""}
        )
        self.fields["title"].widget.attrs.update(
            {"class": "form-control mb-2", "placeholder": ""}
        )
        self.fields["quantity"].widget.attrs.update(
            {"class": "form-control mb-2", "placeholder": ""}
        )
        self.fields["description"].widget.attrs.update(
            {"class": "form-control mb-2", "placeholder": ""}
        )
        self.fields["title"].widget.attrs.update(
            {"class": "form-control mb-2", "placeholder": ""}
        )
        self.fields["regular_price"].widget.attrs.update(
            {"class": "form-control mb-2", "placeholder": ""}
        )
        self.fields["discount_price"].widget.attrs.update(
            {"class": "form-control mb-2", "placeholder": ""}
        )



class ProductUpdateForm(forms.ModelForm):
    class Meta:
        model = Product  # 基于该Model的表单
        exclude = ("seller", "users_wishlist")

    def __init__(self, *args, **kwargs) :
        super().__init__(*args, **kwargs)
        self.fields["category"].widget.attrs.update(
            {"class": "form-select mb-2", "placeholder": ""}
        )
        self.fields["title"].widget.attrs.update(
            {"class": "form-control mb-2", "placeholder": ""}
        )
        self.fields["quantity"].widget.attrs.update(
            {"class": "form-control mb-2", "placeholder": ""}
        )
        self.fields["description"].widget.attrs.update(
            {"class": "form-control mb-2", "placeholder": ""}
        )
        self.fields["title"].widget.attrs.update(
            {"class": "form-control mb-2", "placeholder": ""}
        )
        self.fields["regular_price"].widget.attrs.update(
            {"class": "form-control mb-2", "placeholder": ""}
        )
        self.fields["discount_price"].widget.attrs.update(
            {"class": "form-control mb-2", "placeholder": ""}
        )

class ProductImageAddForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        exclude = ("alt_text", "product")

    def __init__(self, *args, **kwargs) :
        super().__init__(*args, **kwargs);
        self.fields["image"].widget.attrs.update(
            {"class": "form-control mb-2", "placeholder": ""}
        )

class ProductImageUpdateForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        exclude = ("alt_text", "product")
    
    def __init__(self, *args, **kwargs) :
        super().__init__(*args, **kwargs);
        self.fields["image"].widget.attrs.update(
            {"class": "form-control mb-2", "placeholder": ""}
        )
