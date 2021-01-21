from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Coupon(models.Model):
    '''
    Модель купона
    '''
    code = models.CharField(max_length=50, unique=True) # код купона
    valid_from = models.DateTimeField() # дата и время начала действия купона
    valid_to = models.DateTimeField() # дата и время окончания действия купона
    discount = models.IntegerField( 
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    ) # размер скидки в процентах, принимающий значения от 0 до 100
    active = models.BooleanField() # активность купона

    def __str__(self):
        return self.code