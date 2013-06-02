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

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from models import SinaProfile

# We want to display our sinabook profile, not the default user
admin.site.unregister(User)

class SinaProfileInline(admin.StackedInline):
    model = SinaProfile

class SinaProfileAdmin(UserAdmin):
    inlines = [SinaProfileInline]

admin.site.register(User, SinaProfileAdmin)
