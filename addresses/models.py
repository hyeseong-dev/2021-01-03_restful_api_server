from django.db       import models
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles


class Addresses(models.Model):
    name         = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=13)
    address      = models.TextField()
    created      = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name}, {self.phone_number}'

    class Meta:
        ordering = ['created']
        db_table = 'addresses'