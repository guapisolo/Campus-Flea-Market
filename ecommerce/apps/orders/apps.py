from django.apps import AppConfig

VERBOSE_APP_NAME = '订单' # 在admin页面中显示的名字

class OrdersConfig(AppConfig):
    name = 'ecommerce.apps.orders'  
    verbose_name = VERBOSE_APP_NAME