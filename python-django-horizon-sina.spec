Name:		python-django-horizon-sina
Version:	2013.1
Release:	1%{?dist}
Summary:	A sina weibo auth plugin for horizon

Group:		Development/Libraries
License:	Apache 2.0
URL:		https://github.com/liyingjun/python-django-horizon-sina
Source0:	%{name}-%{version}.tar.gz

BuildRequires: python2-devel 
BuildRequires: python-setuptools
Requires:	python-django-horizon
Requires:	weibo

%description
Provides auth module to allow the horizon framework to use sina weibo as an auth method

%prep
%setup -q -n %{name}-%{version}


%build
%{__python} setup.py build

%install
mkdir %{buildroot}%{python_sitelib}/horizon/sina/templates/auth/ -p
install -t %{buildroot}%{python_sitelib}/horizon/sina/ horizon/sina/*py*
install -t %{buildroot}%{python_sitelib}/horizon/sina/templates/ horizon/templates/*html
install -t %{buildroot}%{python_sitelib}/horizon/sina/templates/auth/ horizon/templates/auth/*html

%files
%defattr(644, root, root, -)
%doc LICENSE
%{python_sitelib}/horizon/sina/*.py*
%{python_sitelib}/horizon/sina/templates/*.html
%{python_sitelib}/horizon/sina/templates/auth/*.html

%changelog
* Sun June 2 2013 Yingjun Li <liyingjun1988@gmail.com> - 2013.1
- initial packaging
