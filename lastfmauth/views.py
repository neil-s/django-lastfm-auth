# -*- coding: UTF-8 -*-
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from urllib import urlencode
from django.core.urlresolvers import reverse
from django.shortcuts import redirect

API_KEY = settings.LASTFM_API_KEY


def do_login(request):
    login_complete_url = request.build_absolute_uri(reverse('lastfm_login_complete'))
    parameters = {'api_key': API_KEY}

    if ('next' in request.GET):
        next = request.GET["next"]
        redirecturl = "%s?next=%s" % (login_complete_url, next)
        parameters['cb'] = redirecturl

    signin_url = "http://www.last.fm/api/auth/?%s" % urlencode(parameters)
    return HttpResponseRedirect(signin_url)


def login_complete(request):
    token = request.GET["token"]

    # user, new_user = authenticate(token=token)
    user = authenticate(token=token)
    new_user = user.authuser.newuser
    if user:
        login(request, user)

    #Redirect to next, unless new user and next is home page.
    #If next is not set, redirect based on setting or to home page.
    if ('next' in request.GET):
        next = request.GET["next"]
        if new_user and next == "/":
            redirect('artists')
        return HttpResponseRedirect(next)
    elif hasattr(settings, 'LASTFM_AUTH_REDIRECT'):
        return HttpResponseRedirect(settings.LASTFM_AUTH_REDIRECT)
    else:
        return HttpResponseRedirect('/')


def do_logout(request):
    logout(request)
    return redirect('home')
