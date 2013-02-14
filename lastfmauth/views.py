# -*- coding: UTF-8 -*-
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from urllib import urlencode
from django.core.urlresolvers import reverse

from lastfmauth.models import LastfmProfile

API_KEY = settings.LASTFM_API_KEY

def do_login(request):
    login_complete_url = request.build_absolute_uri(reverse('lastfm_login_complete'))
    parameters = {'api_key': API_KEY}

    if ('next' in request.GET):
	    next = request.GET["next"]
	    redirecturl = "%s?next=%s" % (login_complete_url , next)
	    parameters['cb'] = redirecturl
		
    signin_url = "http://www.last.fm/api/auth/?%s" % urlencode(parameters)
    return HttpResponseRedirect(signin_url)

def login_complete(request):
    token = request.GET["token"]

    user = authenticate(token=token)
    if user:
        login(request, user)

    if ('next' in request.GET):
    	next = request.GET["next"]
    	return HttpResponseRedirect(next)
    elif hasattr(settings, 'LASTFM_AUTH_REDIRECT'):
    	return HttpResponseRedirect(settings.LASTFM_AUTH_REDIRECT)
    else:
    	return HttpResponseRedirect('/admin/')
