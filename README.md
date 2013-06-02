==========================
python-django-horizon-sina
==========================

本plugin参考trystack的facebook plugin, facebook plugin详见：
https://github.com/trystack/python-django-horizon-facebook

安装步骤:
=========

    * 修改openstack_dashboard/settings.py::

    Add 'horizon.sina' to INSTALLED_APPS
    Add 'horizon.facebook.backend.SinaBackend' to AUTHENTICATION_BACKENDS

    添加新行::

    AUTH_PROFILE_MODULE = 'horizon.sina.SinaProfile'

    * 修改openstack_dashboard/local_settings.py

    加入如下行，并加入相应参数::

    SINA_APP_ID = ""
    SINA_APP_SECRET = ""
    SINA_SCOPE = "email"
    """The user must followed each other with this user with id SINA_GROUP_ID."""
    SINA_GROUP_ID = ""
    """The keystone admin user name."""
    ADMIN_USER = ""
    """The keystone admin tenant name."""
    ADMIN_TENANT = ""
    """The keystone admin password."""
    ADMIN_PASSWORD = ""
    """The keystone MEMBER_USER_ROLE ID."""
    MEMBER_USER_ROLE = ""
    DATABASES = {'default': {'ENGINE': 'django.db.backends.mysql',
                             'NAME': '',
                             'USER': '',
                             'PASSWORD': ''}}

    * 同步数据库::

        $ ./manager.py syncdb

    * 修改openstack_dashboard/urls.py
    在url(r'', include(horizon.urls))行的上面加入行::

        url(r'sina/', include('horizon.sina.urls')),

    * 覆盖templates文件

        拷贝 horizon/templates/目录下的文件至django-horizon对应的位置覆盖原文件

附:
===
    新浪APP创建:
    
        * http://blog.csdn.net/junheart/article/details/9009147

    回调页最后必须以sina/authentication_callback结尾，如果需要使用其他的结尾，则需要修改代码使url匹配
