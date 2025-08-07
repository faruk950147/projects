# views.py

import random
from django.shortcuts import render
from .models import Participant

def raffle_draw(request):
    participants = Participant.objects.all()
    winner = None
    if request.method == 'POST' and participants.exists():
        winner = random.choice(participants)
    return render(request, 'raffle_draw.html', {'winner': winner, 'participants': participants})
