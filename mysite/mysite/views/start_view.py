#COPYRIGHT KEVIN J REIF
#2020 BRIGHTON MI

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render


def start_view(request):
    request.session.set_test_cookie()
    return render(request, "start_view.html", {})

