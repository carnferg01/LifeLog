from django.contrib import admin
from .models import Illness, Injury

admin.site.register(Injury)
admin.site.register(Illness)