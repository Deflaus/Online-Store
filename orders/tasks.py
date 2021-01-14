from celery import Celery
from django.core.mail import send_mail
from .models import Order


app = Celery()


@app.task
def order_created(order_id):
    '''
    Задача отправки email-уведомлений при успешном оформлении заказа
    '''
    order = Order.objects.get(id=order_id)
    subject = f'Заказ {order.id}'
    message = f'{order.first_name},\n\nВаш заказ {order.id}'

    mail_sent = send_mail(
        subject,
        message,
        'admin@myshop.com',
        [order.email]
    )

    return mail_sent