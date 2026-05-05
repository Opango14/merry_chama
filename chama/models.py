from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal

# Create your models here.
class ChamaGroup(models.Model):
    name = models.CharField(max_length=100)
    contribution_amount = models.DecimalField(max_digits=12, decimal_places=2)
    savings_rate = models.DecimalField(max_digits=5, decimal_places=2, default=10.00)
    frequency = models.CharField(max_length=20, choices=[('weekly', 'Weekly'), ('monthly', 'Monthly')])
    start_date = models.DateField(auto_now_add=True)
    members = models.ManytoManyField(User, through='Membership')
    savings_pot = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    current_cycle = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

