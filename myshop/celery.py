import os
from celery import Celery


# Переменная окружения, содержащая название файла настроек нашего проекта.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myshop.settings')

# Создаем экземпляр приложения
app = Celery('myshop') 

# Загружаем конфигурацию из настроек нашего проекта
# Параметр namespace определяет префикс, который
# мы будем добавлять для всех настроек, связанных с  Celery
app.config_from_object('django.conf:settings', namespace='CELERY')

# вызываем процесс поиска и  загрузки асинхронных задач по нашему проекту
app.autodiscover_tasks()

