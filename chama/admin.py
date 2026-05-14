from django.contrib import admin
from .models import ChamaGroup, Membership, Contribution

# Register your models here.
admin.site.register(ChamaGroup)
admin.site.register(Membership)
admin.site.register(Contribution)