from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.decorators.http import require_POST
from .models import Coupon
from .forms import CouponApplyForm


@require_POST
def coupon_apply(request):
    '''
    Обработчик добавления купона
    '''
    now = timezone.now()
    form = CouponApplyForm(request.POST)
    if form.is_valid():
        code = form.cleaned_data['code']
        try:
            coupon = Coupon.objects.get(
                code__iexact=code, # iexact - без учета регистра
                valid_from__lte=now, # lte - меньше или равно
                valid_to__gte=now, # gte - больше или равно
                active=True
            )
            request.session['coupon_id'] = coupon.id # сохраняем id купона в сесиию
        except Coupon.DoesNotExist:
            request.session['coupon_id'] = None
    return redirect('cart:cart_detail')
