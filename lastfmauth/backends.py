# -*- coding: UTF-8 -*-

from django.conf import settings
from django.contrib.auth.models import User


API_KEY = settings.LASTFM_API_KEY
WS_URL = settings.LASTFM_WS_BASE_URL
client = settings.CLIENT


class LastfmAuthBackend:

    def authenticate(self, token=None):

        authuser = client.login(token=token)

        # try to find a user instance with a matching Authuser
        user, user_created = User.objects.get_or_create(username=authuser.user.name)
        user.first_name = authuser.session_key
        #^ Hack using superfluous first_name field to store session key to avoid extra profile class.

        if user_created:
            user.set_password(User.objects.make_random_password())
            user.save()
        user.authuser = authuser

        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
