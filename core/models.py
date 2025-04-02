from django.db import models
from django.conf import settings

class Shanyrak(models.Model):
    TYPE_CHOICES = [
        ('sale', 'Продажа'),
        ('rent', 'Аренда'),
    ]
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    price = models.DecimalField(max_digits=15, decimal_places=2)
    address = models.CharField(max_length=255)
    area = models.DecimalField(max_digits=5, decimal_places=1)
    rooms_count = models.IntegerField()
    description = models.TextField()
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='shanyraks'
    )

    def __str__(self):
        return f"{self.get_type_display()} - {self.address}"

class Comment(models.Model):
    shanyrak = models.ForeignKey(Shanyrak, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Комментарий от {self.author.username} к объявлению {self.shanyrak.id}"