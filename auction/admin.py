from django.contrib import admin
from auction.models import *
# Register your models here.

admin.site.register(Phase)
admin.site.register(Round)
admin.site.register(BidderInfo)
admin.site.register(Bidding)
admin.site.register(CurrentRound)