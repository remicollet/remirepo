%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name:           mysql-connector-python
Version:        0.3.2
Release:        1%{?dist}
Summary:        MySQL Connector/Python 

Group:          Development/Languages
License:        GPLv2+
URL:            https://launchpad.net/myconnpy
Source0:        http://launchpad.net/myconnpy/0.3/%{version}/+download/%{name}-%{version}-devel.tar.gz

BuildArch:      noarch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  python-devel


%description
MySQL Connector/Python is implementing the MySQL Client/Server protocol
completely in Python. No MySQL libraries are needed, and no compilation
is necessary to run this Python DB API v2.0 compliant driver.


%prep
%setup -q -n %{name}-%{version}-devel

%{__chmod} -x python2/examples/*py

%build
# nothin to build


%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install --root $RPM_BUILD_ROOT


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc ChangeLog COPYING EXCEPTIONS-CLIENT README
%doc python2/examples
%{python_sitelib}/*


%changelog
* Wed Mar 09 2011 Remi Collet <Fedora@famillecollet.com> 0.3.2-1
- first RPM

