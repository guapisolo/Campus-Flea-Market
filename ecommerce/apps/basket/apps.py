from django.apps import AppConfig

VERBOSE_APP_NAME = '购物车' # 在admin页面中显示的名字

class BasketConfig(AppConfig):
    name = 'ecommerce.apps.basket'  
    verbose_name = VERBOSE_APP_NAME