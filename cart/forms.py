from django import forms


PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]

class CartAddProductForm(forms.Form):
    '''
    Форма добавления товара в корзину
    '''
    quantity = forms.TypedChoiceField(
        choices=PRODUCT_QUANTITY_CHOICES,
        coerce=int
    ) # количество единиц товара
    update = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.HiddenInput
    ) # обновить или заменить количество единиц для товара
