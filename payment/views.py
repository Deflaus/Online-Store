from django.shortcuts import render, redirect, get_object_or_404
import braintree
from orders.models import Order


def process(request):
    order_id = request.session.get('order_id')
    # Заказ по добавленному в order_create после оформления
    # покупателем заказа ключу order_id из сессии
    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        # Получение токена для создания транзакции
        nonce = request.POST.get('payment_method_nonce', None)
        # Создание и сохранение транзакции
        result = braintree.Transaction.sale(
            {
                'amount': '{:.2f}'.format(order.get_total_cost()), # Общая сумма заказа
                'payment_method_nonce': nonce, # Токен, сгенерированный Braintree для платежной транзакции
                'options': { # Доп. параметры
                    'submit_for_settlement': True, # Транзакция будет обрабатываться автоматически
                }
            }
        )

        if result.is_success:
            # Отметка заказа как оплаченного
            order.paid = True
            # Сохранение ID транзакции в заказе
            order.braintree_id = result.transaction.id
            order.save()
            return redirect('payment:done')
        else:
            return redirect('payment:canceled')
    else:
        # Формирование одноразового токена для JS SDK
        client_token = braintree.ClientToken.generate()
        return render(
            request,
            'payment/process.html',
            {
                'order': order,
                'client_token': client_token,
            }
        )


def done(request):
    return render(
        request,
        'payment/done.html',
    )


def canceled(request):
    return render(
        request,
        'payment/canceled.html',
    )