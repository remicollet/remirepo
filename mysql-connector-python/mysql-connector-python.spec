%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

%if 0%{?fedora} >= 13
%global with_python3 1
%else
%global with_python3 0
%endif

Name:           mysql-connector-python
Version:        0.3.2
Release:        2%{?dist}
Summary:        MySQL Connector for Python 2

Group:          Development/Languages
License:        GPLv2 with exceptions
URL:            https://launchpad.net/myconnpy
Source0:        http://launchpad.net/myconnpy/0.3/%{version}/+download/%{name}-%{version}-devel.tar.gz

BuildArch:      noarch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  python-devel
%if 0%{?with_python3}
BuildRequires:  python3-devel
%endif
# for unittest
BuildRequires:  mysql-server


%description
MySQL Connector/Python is implementing the MySQL Client/Server protocol
completely in Python. No MySQL libraries are needed, and no compilation
is necessary to run this Python DB API v2.0 compliant driver.

%if 0%{?with_python3}
%package -n mysql-connector-python3

Summary:        MySQL Connector for Python 3

%description -n mysql-connector-python3
MySQL Connector/Python is implementing the MySQL Client/Server protocol
completely in Python. No MySQL libraries are needed, and no compilation
is necessary to run this Python DB API v2.0 compliant driver.
%endif


%prep
%setup -q -n %{name}-%{version}-devel

%{__chmod} -x python?/examples/*py


%build
# nothin to build


%install
%{__rm} -rf $RPM_BUILD_ROOT

%if 0%{?with_python3}
# Python 3 build
%{__python3} setup.py install --root $RPM_BUILD_ROOT
%{__rm} -rf build
%endif

# Python 2 build (end with this for tests)
%{__python} setup.py install --root $RPM_BUILD_ROOT


%check
%{__python} unittests.py --mysql-basedir=%{_prefix}


%clean
%{__rm} -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc ChangeLog COPYING EXCEPTIONS-CLIENT README
%doc python2/examples
%{python_sitelib}/*


%if 0%{?with_python3}
%files -n mysql-connector-python3
%defattr(-,root,root,-)
%doc ChangeLog COPYING EXCEPTIONS-CLIENT README
%doc python3/examples
%{python3_sitelib}/*
%endif

%changelog
* Sun Mar 20 2011 Remi Collet <Fedora@famillecollet.com> 0.3.2-2
- run unittest during %%check
- fix License
- add python3 sub package

* Wed Mar 09 2011 Remi Collet <Fedora@famillecollet.com> 0.3.2-1
- first RPM

