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

from django.conf import settings
from django.contrib.auth.models import User
from django.db import IntegrityError
import logging
import string
import random
from models import SinaProfile
from keystoneclient.v2_0 import client as keystone_client
from django.contrib import messages
from openstack_auth.backend import KeystoneBackend
from weibo import APIClient


LOG = logging.getLogger(__name__)


class SinaBackend:
    def _admin_client(self):
        return  keystone_client.Client(username=settings.ADMIN_USER,
                                      password=settings.ADMIN_PASSWORD,
                                      tenant_name=settings.ADMIN_TENANT,
                                      auth_url=settings.OPENSTACK_KEYSTONE_URL)

    def authenticate(self, token=None, request=None):
        """ Reads in a Sina code and asks Sina
            if it's valid and what user it points to. """
        keystone = KeystoneBackend()
        self.keystone = keystone
        redirect_uri = request.build_absolute_uri('authentication_callback')
        sina_client = APIClient(app_key=settings.SINA_APP_ID,
                                app_secret=settings.SINA_APP_SECRET,
                                redirect_uri=redirect_uri)

        # Get a legit access token
        access_token_dict = sina_client.request_access_token(token)
        access_token = access_token_dict.access_token
        sina_client.set_access_token(access_token,
                                     access_token_dict.expires_in)

        # Read the user's profile information
        try:
            sina_profile = sina_client.account.profile.basic.get()
        except Exception as e:
            LOG.warn("SinaAPIClient Error: %s", e)
            messages.error(request, 'You SinaID is not authorized to login.')
            return
        sina_id = sina_profile['id']
        sina_email = sina_profile['email']
        password = ""
        try:
            # Try and find existing user
            sina_user = SinaProfile.objects.get(sina_id=sina_id)
            user = sina_user.user
            # Update access_token
            sina_user.access_token = access_token
            password = sina_user.password
            sina_user.save()

        except SinaProfile.DoesNotExist:
            # No existing user
            try:
                username = "sina%s" % sina_id
                try:
                    user = User.objects.create_user(username, sina_email)
                except IntegrityError:
                    # Username already exists, make it unique
                    existing_user = User.objects.get(username=username)
                    existing_user.delete()
                    user = User.objects.create_user(username, sina_email)
                user.save()

                password = "".join([random.choice(
                                        string.ascii_lowercase + string.digits)
                                   for i in range(8)])
                # Create the SinaProfile
                sina_user = SinaProfile(user=user, sina_id=sina_id,
                                        access_token=access_token,
                                        password=password)
                tenant_name = "sina%s" % sina_id
                keystone_admin = self._admin_client()

                tenant = keystone_admin.tenants.create(tenant_name,
                                                       "Auto created account",
                                                       True)
                user = keystone_admin.users.create(tenant_name,
                                                   password,
                                                   sina_email,
                                                   tenant.id,
                                                   True)
                member_user_role = settings.MEMBER_USER_ROLE
                keystone_admin.roles.add_user_role(user.id,
                                                   member_user_role,
                                                   tenant.id)
                sina_user.tenant_id = tenant.id
                sina_user.save()
            except:
                sina_user.delete()

        username = "sina%s" % sina_id
        try:
            # Get the user's bilateral friends.
            uid = settings.SINA_GROUP_ID
            friends = sina_client.friendships.friends.bilateral.get(uid=uid)
            user_ids = [user['id'] for user in friends['users']]
            if sina_id not in user_ids:
                messages.error(
                    request, "Your sinaID is not followed by %s yet.", uid)
            else:
                user = keystone.authenticate(request=request,
                                      username=username,
                                      password=password,
                                      tenant=None,
                                      auth_url=settings.OPENSTACK_KEYSTONE_URL)
                return user
        except Exception as e:
            messages.error(
                request, "Failed to login sinaID %s" % e)

    def get_user(self, user_id):
        """ Just returns the user of a given ID. """
        keystone = KeystoneBackend()
        keystone.request = self.request
        return keystone.get_user(user_id)

    supports_object_permissions = False
    supports_anonymous_user = True
