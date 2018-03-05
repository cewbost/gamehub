from django.contrib import admin
from .models import Game, GamePlayed, PaymentDetail
# Register your models here.
class GameAdmin(admin.ModelAdmin):
    pass
admin.site.register(Game, GameAdmin)
admin.site.register(GamePlayed)
admin.site.register(PaymentDetail)
