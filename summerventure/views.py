from django.shortcuts import render, redirect


def landing_page_view(request):
    if request.user.is_authenticated:
        return redirect("challenges:explore")

    return render(request, "landing.html", context={})
