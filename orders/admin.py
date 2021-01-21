from django.contrib import admin
from .models import Order, OrderItem

import csv
import datetime
from django.http import HttpResponse

from django.urls import reverse
from django.utils.safestring import mark_safe


# def order_pdf(obj):
#     return mark_safe('<a href="{}">PDF</a>'.format(
#         reverse('orders:admin_order_pdf', args=[obj.id])))


# order_pdf.short_description = 'Счет'


def order_detail(obj):
    return mark_safe('<a href="{}">Посмотреть подробнее</a>'.format(
        reverse('orders:admin_order_detail', args=[obj.id])))


class OrderItemInline(admin.TabularInline):
    '''
    Класс для модели OrderItem, чтобы добавить ее в  виде списка
    связанных объектов на страницу заказа, зарегистрированную
    через OrderAdmin
    '''
    model = OrderItem
    raw_id_fields = ['product']


def export_to_csv(modeladmin, request, queryset):
    '''
    Функция экспорта заказа в csv файл
    '''
    # опции meta модели ModelAdmin, которая отображается
    opts = modeladmin.model._meta

    # Объект ответа класса HttpResponse с типом содержимого 
    # text/csv, чтобы браузер работал с файлом так же, как с CSV
    response = HttpResponse(content_type='text/csv')

    # Добавляем заголовок Content-Disposition, 
    # т. к. к ответу будет прикреплен файл
    response['Content-Disposition'] = 'attachment;'\
        'filename={}.csv'.format(opts.verbose_name)
    
    # Объект, который будет записывать данные файла
    # в объект response
    writer = csv.writer(response)

    # динамически получаем поля модели с помощью метода
    # get_fields() опций meta модели,
    # исключая отношения «многие ко многим»
    # и «один ко многим»;
    fields = [
        field for field in opts.get_fields() if not field.many_to_many\
            and not field.one_to_many
    ]

    # Записываем первую строку с заголовками полей
    writer.writerow([field.verbose_name for field in fields])

    # Записываем данные
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')
            data_row.append(value)
        writer.writerow(data_row)
    return response

export_to_csv.short_description = 'Export to CSV'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'first_name',
        'last_name',
        'email',
        'address',
        'postal_code',
        'city',
        'paid',
        'created',
        'updated',
        order_detail,
        # order_pdf
    ]
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]
    actions = [export_to_csv]