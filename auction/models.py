from django.db import models
from django.contrib.auth.models import User
import datetime
from datetime import timedelta


class Phase(models.Model):
    phaseName=models.CharField(max_length = 200, null = True, blank = True)
    spectrum=models.CharField(max_length=100, null = True, blank = True)
    base_price=models.DecimalField(decimal_places=2, max_digits=10, default = 0, null = True, blank = True)
    no_of_blocks=models.IntegerField(null = True, blank = True)

    def __str__(self):
        return self.spectrum

class Round(models.Model):
    phase = models.ForeignKey(Phase, on_delete = models.CASCADE, null = True, blank = True)
    roundName = models.IntegerField(default = 0, null = True, blank = True)
    biddingPrice = models.DecimalField(max_digits=10, decimal_places=2, default=0, null = True, blank = True)
    actionStatus=models.BooleanField(default=False)
    start_time=models.DateTimeField(auto_now_add = True, null = True, blank = True)
    end_time=models.DateTimeField(auto_now_add = False, null = True, blank = True)
    isComplete = models.BooleanField(default=False)

    """ def save(self, *args, **kwargs):
        self.end_time = self.start_time + datetime.timedelta(minutes = 3)

        return super().save(*args, **kwargs) """

    def __str__(self):
        return str(self.roundName)

    

class CurrentRound(models.Model):
    round = models.CharField(max_length=10, null = True, blank = True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.round
    




class BidderInfo(models.Model):
    name = models.CharField(max_length = 200, null = True, blank = True)
    designation=models.CharField(max_length = 200, null = True, blank = True)
    organization=models.CharField(max_length = 200, null = True, blank = True)
    country=models.CharField(max_length = 200, null = True, blank = True)
    user=models.OneToOneField(User, on_delete= models.CASCADE, null = True, blank = True)

    def __str__(self):
        return self.name


class Bidding(models.Model):
    round = models.ForeignKey(Round, on_delete = models.CASCADE, null = True, blank = True)
    bidder = models.ForeignKey(BidderInfo, on_delete = models.CASCADE, null = True, blank = True)
    biddingStatus = models.BooleanField(default = False)
    biddingTime = models.DateTimeField(auto_now_add = False, null = True, blank = True)
    rank = models.IntegerField(default = 0, null = True, blank = True)

    def __str__(self):
        return str(self.round.roundName) + '-' + self.bidder.organization


    @property
    def get_response_time(self):
        resp_time = 0
        if self.biddingTime is not None:
            diff = self.biddingTime - self.round.start_time
            #resp_time = (diff.total_seconds() * 1000)
            resp_time = diff.total_seconds()
        else:
            resp_time = 0

        return resp_time


