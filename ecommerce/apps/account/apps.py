from django.apps import AppConfig

VERBOSE_APP_NAME = '账户' # 在admin页面中显示的名字

class AccountConfig(AppConfig):
    name = 'ecommerce.apps.account'  
    verbose_name = VERBOSE_APP_NAME