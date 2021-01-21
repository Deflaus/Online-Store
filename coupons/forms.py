from django import forms


class CouponApplyForm(forms.Form):
    '''
    Форма ввода купона
    '''
    code = forms.CharField()
