from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
import logging
import sys
from django.core.exceptions import ObjectDoesNotExist
from allauth.socialaccount.models import SocialToken, SocialAccount
from report.forms import DateForm

def inst(request):
    return render(request, 'base/instructions.html')

    
def index(request):
  try:
    fb_acc = SocialAccount.objects.get(user_id = request.user.id,provider='facebook')
    try:
      google_acc = SocialAccount.objects.get(user_id = request.user.id,provider='google')
      loginlist = [True,True]
    except ObjectDoesNotExist:
      loginlist = [True,False]
  except ObjectDoesNotExist:
    try:
      google_acc = SocialAccount.objects.get(user_id = request.user.id,provider='google')
      loginlist = [False,True]
    except ObjectDoesNotExist:
      loginlist = [False,False]


  return render(request, 'base/index.html', {'fb' : loginlist[0], 'google' : loginlist[1]})

