from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal

# Create your models here.
class ChamaGroup(models.Model):
    name = models.CharField(max_length=100)
    contribution_amount = models.DecimalField(max_digits=12, decimal_places=2)
    savings_rate = models.DecimalField(max_digits=5, decimal_places=2, default=10.00)
    frequency = models.CharField(max_length=20, choices=[('daily', 'Daily'), ('weekly', 'Weekly'), ('monthly', 'Monthly')])
    start_date = models.DateField(auto_now_add=True)
    members = models.ManyToManyField(User, through='Membership')
    savings_pot = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    current_cycle = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Membership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(ChamaGroup, on_delete=models.CASCADE)
    rotation_order = models.PositiveIntegerField()

    class Meta:
        unique_together = ('user', 'group')

class Contribution(models.Model):
    group = models.ForeignKey(ChamaGroup, on_delete=models.CASCADE)
    member = models.ForeignKey(User, on_delete=models.CASCADE)
    cycle = models.PositiveIntegerField()
    total_paid = models.DecimalField(max_digits=12, decimal_places=12)
    savings_amount = models.DecimalField(max_digits=12, decimal_places=12)
    payout_amount = models.DecimalField(max_digits=12, decimal_places=12)
    paid_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.member.username} - Cycle {self.cycle}"
