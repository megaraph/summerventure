from multiprocessing import context
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def home(request):
    context = {"message": "Sup bruh"}

    return render(request, "challenges/home.html", context=context)
