from decimal import Decimal
from django.conf import settings
from shop.models import Product
from coupons.models import Coupon


class Cart(object):
    '''
    Класс корзины
    '''
    def __init__(self, request):
        '''
        Инициализация объекта корзины
        '''
        self.session = request.session # Текущая сессия
        cart = self.session.get(settings.CART_SESSION_ID) # Корзина, полученная из сессии
        if not cart: # Если корзина пустая
            # Сохраняем в сессии пустую корзину
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart # Текущая корзина
        self.coupon_id = self.session.get('coupon_id')

    def add(self, product, quantity=1, update_quantity=False):
        '''
        Добавление в корзину или обновление его количества 
        '''
        product_id = str(product.id)
        if product_id not in self.cart: # Если товара нет в корзине
            self.cart[product_id] = {
                'quantity': 0,
                'price': str(product.price),
            } # Добавляем товар в корзину
        if update_quantity: # Если нужно обновить количество товара в корзине
            self.cart[product_id]['quantity'] = quantity
        else: # Если нужно добавить количество товара в корзине
            self.cart[product_id]['quantity'] += quantity
        self.save() # Сохранить сессию
    
    def save(self):
        '''
        Помечаем сессию как измененную
        '''
        self.session.modified = True
    
    def remove(self, product):
        '''
        Удаление товара из корзины
        '''
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()
    
    def __iter__(self):
        '''
        Проходим по товарам и получаем соответствующие объекты Product
        '''
        product_ids = self.cart.keys()
        # Получаем объекты модели Product и передаем их в корзину
        products = Product.objects.filter(id__in=product_ids)

        cart = self.cart.copy() # Копия корзины
        for product in products: # Проход по всем объектам товаров
            cart[str(product.id)]['product'] = product # Добавляем в копию корзины объект товара
        for item in cart.values(): # Проход по содержимому товара
            item['price'] = Decimal(item['price']) # Добавление элемента цены за один товар в содержимое товара в виде decimal
            item['total_price'] = item['price'] * item['quantity'] # Добавление цены за все количество в содержимое товара
        
            yield item
    
    def __len__(self):
        '''
        Возвращает общее количество товаров в корзине
        '''
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        '''
        Подсчет общей стоимости корзины
        '''
        return sum(
            Decimal(item['price']) * item['quantity']
            for item in self.cart.values()
        )
    
    def clear(self):
        '''
        Очистка корзины
        '''
        del self.session[settings.CART_SESSION_ID] # Удаление из сессии корзины
        self.save()

    @property
    def coupon(self):
        '''
        Свойство, возвращающее объект купона по его id
        '''
        if self.coupon_id:
            return Coupon.objects.get(id=self.coupon_id)
        return None
    
    def get_discount(self):
        '''
        Возвращает размер скидки
        '''
        if self.coupon:
            return(self.coupon.discount / Decimal('100')) * self.get_total_price()
        return Decimal('0')
    
    def get_total_price_after_discount(self):
        '''
        Возвращает общую стоимость товаров в корзине с учетом скидки по купону
        '''
        return self.get_total_price() - self.get_discount()