%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%{!?pyver: %define pyver %(%{__python} -c "import sys ; print sys.version[:3]")}

Name:           moksha 
Version:        0.3.1
Release:        1%{?dist}
Summary:        A flexable platform for creating live collaborative web applications
Group:          Applications/Internet
License:        AGPLv3
URL:            https://fedorahosted.org/moksha
Source0:        moksha-%{version}.tar.bz2

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires: python-setuptools 
BuildRequires: python-setuptools-devel
BuildRequires: python-devel
BuildRequires: python-pygments
BuildRequires: python-paver
BuildRequires: python-sphinx
BuildRequires: python-nose

Requires: TurboGears2
Requires: python-toscawidgets >= 0.9.1
Requires: python-zope-sqlalchemy 
Requires: python-shove
Requires: python-feedcache
Requires: python-feedparser
Requires: python-tw-jquery >= 0.9.4.1
#Requires: python-repoze-squeeze
#Requires: python-repoze-profile
Requires: orbited
Requires: python-twisted
Requires: python-stomper
Requires: python-sphinx
Requires: python-paver
Requires: python-tw-forms
Requires: python-morbid
Requires: pytz
Requires: pyevent
Requires: python-repoze-who-testutil

%description
Moksha is a platform for creating real-time collaborative web applications.  It 
provides a set of Python and JavaScript API's that make it simple to create 
rich applications that can acquire, manipulate, and visualize data from 
external services. It is a unified framework build using the best available 
open source technologies such as TurboGears2, jQuery, AMQP, and Orbited.  More 
information can be found on the Moksha Project Page at 

%package docs
Summary: Developer documentation for Moksha
Group: Documentation
Requires: %{name} = %{version}-%{release}

%description docs
This package contains developer documentation for Moksha along with
other supporting documentation

%prep
%setup -q

%build
%{__python} setup.py build
make -C docs html

%install
%{__rm} -rf %{buildroot}

%{__python} setup.py install -O1 --skip-build \
    --install-data=%{_datadir} --root %{buildroot}

# Wipe out moksha/apps because that is where other app packages install
%{__rm} -fr %{buildroot}%{python_sitelib}/moksha/apps/*

%{__mkdir_p} %{buildroot}%{_datadir}/%{name}/production/apache
%{__mkdir_p} %{buildroot}%{_datadir}/%{name}/production/nginx
%{__mkdir_p} %{buildroot}%{_datadir}/%{name}/production/rabbitmq

%{__mkdir_p} -m 0755 %{buildroot}/%{_localstatedir}/log/%{name}
%{__mkdir_p} -m 0700 %{buildroot}/%{_localstatedir}/cache/%{name}

%{__install} production/*.* %{buildroot}%{_datadir}/%{name}/production/
%{__install} production/apache/* %{buildroot}%{_datadir}/%{name}/production/apache
%{__install} production/nginx/* %{buildroot}%{_datadir}/%{name}/production/nginx
%{__install} production/rabbitmq/* %{buildroot}%{_datadir}/%{name}/production/rabbitmq

%clean
%{__rm} -rf %{buildroot}


%files 
%defattr(-,root,root,-)
%doc README AUTHORS LICENSE COPYING
%{python_sitelib}/%{name}/
%attr(-,apache,root) %{_datadir}/%{name}
%attr(-,apache,root) %{_localstatedir}/log/%{name}
%{python_sitelib}/%{name}-%{version}-py%{pyver}.egg-info/
%attr(-,apache,apache) %dir %{_localstatedir}/cache/%{name}
%{_bindir}/moksha-hub

%files docs
%defattr(-,root,root)
%doc docs/_build/html 

%changelog
* Fri Aug 14 2009 Luke Macken <lmacken@redhat.com> - 0.3.1-1
- 0.3.1

* Mon Aug 03 2009 Luke Macken <lmacken@redhat.com> - 0.3-1
- 0.3, bugfix release

* Wed Jun 03 2009 Luke Macken <lmacken@redhat.com> - 0.2-1
- Add nose to the build requirements

* Wed May 27 2009 John (J5) Palmieri <johnp@redhat.com> - 0.1-0.1
- first package

