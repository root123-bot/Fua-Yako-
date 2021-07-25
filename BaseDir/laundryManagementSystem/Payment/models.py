from django.db import models

# Create your models here.
class Payment(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=30)
    account_number = models.CharField(max_length=10, blank=True, null=True)
    balance = models.PositiveIntegerField()

    def __str__(self):
        return self.username

  