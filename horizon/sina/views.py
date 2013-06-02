# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2013, Yingjun Li
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import urllib

from django.http import HttpResponseRedirect
from django.conf import settings
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate
from openstack_auth.user import set_session_from_user
from openstack_auth.forms import Login


def login(request):
    """ First step of process, redirects user to sina,
        which redirects to authentication_callback. """
    uri = '/sina/authentication_callback'
    args = {
        'client_id': settings.SINA_APP_ID,
        'scope': settings.SINA_SCOPE,
        'redirect_uri': request.build_absolute_uri(uri)
    }
    r_uri = 'https://api.weibo.com/oauth2/authorize?' + urllib.urlencode(args)
    return HttpResponseRedirect(r_uri)


def authentication_callback(request):
    """ Second step of the login process.
    It reads in a code from Sina, then redirects back to the home page. """
    code = request.GET.get('code')
    user = authenticate(token=code, request=request)
    auth_login(request, user)
    set_session_from_user(request, user)
    region = request.user.endpoint
    region_name = dict(Login.get_region_choices()).get(region)
    request.session['region_endpoint'] = region
    request.session['region_name'] = region_name
    url = getattr(settings, "LOGIN_REDIRECT_URL", "/")
    resp = HttpResponseRedirect(url)

    return resp
