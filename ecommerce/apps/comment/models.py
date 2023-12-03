from django.db import models
from django.urls import reverse
from ecommerce.apps.orders.models import Order

class Comment(models.Model):

    order = models.OneToOneField(
        Order,
        related_name='comments',
        on_delete=models.CASCADE,
    )
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created',)
        verbose_name = "评论"
        verbose_name_plural = "评论"

    def __str__(self):
        return self.body[:20]

    def get_absolute_url(self):
        return reverse("comment:post_comment", args=[self.order.id])
