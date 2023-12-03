from django.apps import AppConfig

VERBOSE_APP_NAME = '评论' # 在admin页面中显示的名字

class CommentConfig(AppConfig):
    name = 'ecommerce.apps.comment'  
    verbose_name = VERBOSE_APP_NAME