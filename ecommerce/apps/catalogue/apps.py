from django.apps import AppConfig

VERBOSE_APP_NAME = '商店' # 在admin页面中显示的名字

# name字段要写settings.py中注册的installed_app的名字
class CatalogueConfig(AppConfig):
    name = 'ecommerce.apps.catalogue'  
    verbose_name = VERBOSE_APP_NAME