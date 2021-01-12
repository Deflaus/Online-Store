from django.db import models


class Category(models.Model):
    '''
    Модель категории товаров
    '''
    name = models.CharField(max_length=200, db_index=True) # Название категории
    slug = models.SlugField(max_length=200, unique=True) # Slug категории

    class Meta:
        ordering = ('name',) # Сортировка по названию категории
        verbose_name = 'category' # Название модели в ед. числе
        verbose_name_plural = 'categories' # Название модели во мн. числе
    
    def __str__(self):
        return self.name


class Product(models.Model):
    '''
    Модель Товара
    '''
    category = models.ForeignKey(Category,
                                 related_name='products',
                                 on_delete=models.CASCADE) # Внешний ключ категория товара
    name = models.CharField(max_length=200, db_index=True) # Название товара
    slug = models.SlugField(max_length=200, db_index=True) # Slug товара
    image = models.ImageField(upload_to='products', blank=True) # Изображение товара
    description = models.TextField(blank=True) # Описание товара
    price = models.DecimalField(max_digits=10, decimal_places=2) # Цена товара
    available = models.BooleanField(default=True) # Наличие товара
    created = models.DateTimeField(auto_now_add=True) # Создание товара
    updated = models.DateTimeField(auto_now=True) # Изменение товара 

    class Meta:
        ordering = ('name',) # Сортировка по названию товара
        index_together = (('id', 'slug'),) # Объединение двух индексов в один
    
    def __str__(self):
        return self.name
