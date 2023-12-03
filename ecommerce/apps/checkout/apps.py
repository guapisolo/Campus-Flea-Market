from django.apps import AppConfig

VERBOSE_APP_NAME = '交易设置' # 在admin页面中显示的名字

class CheckoutConfig(AppConfig):
    name = 'ecommerce.apps.checkout'  
    verbose_name = VERBOSE_APP_NAME