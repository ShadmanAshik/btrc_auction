from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView
from django.contrib import messages
from django.utils import timezone

from auction.forms import *
from auction.models import *

from django.template.loader import render_to_string


@login_required(login_url='login')
def test(request):
    data = dict()
    rounds = []
    bidders = []
    start_time = None
    end_time = None
    
    curBid = CurrentRound.objects.get(status = False)
    
    try:
        rounds = Round.objects.get(roundName = curBid.round)
        bidders = Bidding.objects.filter(round = rounds) .order_by('bidder__organization')
        data['html_product_list'] = render_to_string('auction/bidding.html', {
            'bidders': bidders
        })
        start_time = rounds.start_time.strftime("%Y-%m-%dT%H:%M:%S")
        end_time = rounds.end_time.strftime("%Y-%m-%dT%H:%M:%S")
    except:
        rounds = []
        bidders = []


    context = {
        'rounds' : rounds,
        'bidders' : bidders,
        'start_time' : start_time,
        'end_time' : end_time,
    }
    return render(request, 'auction/base1.html', context)




###############################################################################################
@login_required(login_url='login')
def startRound(request):
    bidderlist = BidderInfo.objects.all()
    phase = Phase.objects.get(pk = 1)
    curRound = CurrentRound.objects.get(status = False)
    actionStatus=False

    chkRound = Round.objects.filter(roundName = curRound.round, actionStatus = True, isComplete = False)
    if chkRound.count() == 0:
        try:
            auction = Round.objects.create(phase = phase, roundName = curRound.round, actionStatus = True, end_time = datetime.datetime.today() + datetime.timedelta(minutes = 3))
            auction.save()

            for i in bidderlist:
                bidding = Bidding.objects.create(round = auction, bidder = i)
                bidding.save()
            
            context={'actionStatus': actionStatus}
            return redirect('home')
            # return render(request, 'auction/base1.html', context)
        except Exception as e:
            messages.error(request, str(e))
            return redirect('home')
        
    else:
        messages.error(request, "Auction process is going on...")
        return redirect('home')
        


@login_required(login_url = 'login')
def bidparticipation(request,varRound):
    now = timezone.now()
    round = Round.objects.get(id = varRound)
    bidder = Bidding.objects.get(round = round, bidder__user = request.user)

    if bidder.biddingStatus == False:
        if round.actionStatus == True and round.isComplete == False:
            if now >= round.start_time and now <= round.end_time:
                bidder.biddingTime = datetime.datetime.now()
                bidder.biddingStatus = True
                bidder.save()
            else:
                if round.start_time > now:
                    messages.error(request, 'Auction not startted yet')
                else:
                    messages.error(request, 'Auction time expired')
        
        else:
            messages.error(request, 'Selected auction is not active')

    else:
        messages.error(request, 'You already participated in the Bidding')

    return redirect('home')



@login_required(login_url = 'login')
def endround(request, varRound):
    try:
        ## Ending Current Round
        round = Round.objects.get(id = varRound)
        round.actionStatus = False
        round.isComplete = True
        round.save()
        
        curRound = CurrentRound.objects.get(round = round.roundName)
        curRound.status = True
        curRound.save()

        ## Creating Next Round
        nextRound = CurrentRound.objects.create(round = (int(curRound.round) + 1), status = False)
        nextRound.save()
        return redirect('home')

    except Exception as e:
        messages.error(request, str(e))
        return redirect('home')






###############################################################################################






## LOGIN
def userlogin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username = username, password = password)

        if user is not None:
            login(request, user)    
            return redirect('home')

        else:
            messages.error(request,'User name or password is incorrect.')
            

    context = {}
    return render(request, 'auction/login.html',context)


## LOGOUT
def logout_user(request):
    logout(request)
    return redirect('login')



@login_required(login_url='login')
def changepassword(request):
    headerText = 'Change Password'

    if request.method == 'POST':
        form = ChangePasswordForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password changed successfully.')
            return redirect('home')
        
    else:
        form = ChangePasswordForm(request.user)

    context = {
        'form' : form,
        'headerText' : headerText,
    }  
    return render(request, 'auction/entry.html', context)




