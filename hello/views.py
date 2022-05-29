from django.shortcuts import render
from urllib3 import HTTPResponse


def track_cookies(request):
    num_visits = request.session.get('num_visits', 0) + 1
    request.session['num_visits'] = num_visits
    if num_visits > 4:
        del(request.session['num_visits'])

    resp = render(request, 'hello/main.html', {'view_count': num_visits})
    resp.set_cookie('dj4e_cookie', '0801f1b5', max_age=1000)

    return resp
