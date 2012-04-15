%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

# From README.txt
# Python 2.6 or later but Python 3.x is not supported (yet).
%global with_python3 0

%if 0%{?fedora} >= 14 || 0%{?rhel} >= 6
%global with_man 1
%else
%global with_man 0
%endif

Name:           mysql-utilities
Version:        1.0.5
Release:        2%{?dist}
Summary:        MySQL Utilities

Group:          Applications/Databases
License:        GPLv2
URL:            https://launchpad.net/mysql-utilities
# wget http://bazaar.launchpad.net/~mysql/mysql-utilities/trunk/tarball/247 -O mysql-utilities-1.0.5.tgz
Source0:        %{name}-%{version}.tgz

# Fix man page destination path
Patch0:         %{name}-man.patch


BuildArch:      noarch
BuildRequires:  python2-devel >= 2.6
%if %{with_man}
BuildRequires:  python-sphinx >= 1.0
%endif
%if %{with_python3}
BuildRequires:  python3-devel
%endif

Requires:       mysql-connector-python

%description
The MySQL Utilities is a set of easy-to-use scripts intended to make working
with servers easier. It is part of the MySQL Workbench.

Documentation:
http://dev.mysql.com/doc/workbench/en/mysql-utilities.html


%prep
%setup -q -n ~mysql/%{name}/trunk

%patch0 -p0 -b .manpath


%build
%if %{with_man}
%{__python} setup.py build_man
%else
: No man will be generated
%endif


%install 
install --directory %{buildroot}%{_mandir}/man1

%if %{with_python3}
# Python 3 build
%{__python3} setup.py install --skip-profile --root %{buildroot}
rm -rf build
%endif

# Python 2 build (end with this for tests)
%{__python} setup.py install --skip-profile --root %{buildroot}


%check
%{__python} check.py


%files
%doc CHANGES.txt LICENSE.txt
%{_bindir}/mysqldbcompare
%{_bindir}/mysqldbcopy
%{_bindir}/mysqldbexport
%{_bindir}/mysqldbimport
%{_bindir}/mysqldiff
%{_bindir}/mysqldiskusage
%{_bindir}/mysqlfailover
%{_bindir}/mysqlindexcheck
%{_bindir}/mysqlmetagrep
%{_bindir}/mysqlprocgrep
%{_bindir}/mysqlreplicate
%{_bindir}/mysqlrpladmin
%{_bindir}/mysqlrplcheck
%{_bindir}/mysqlrplshow
%{_bindir}/mysqlserverclone
%{_bindir}/mysqlserverinfo
%{_bindir}/mysqluserclone
%{python_sitelib}/mysql/utilities
%{python_sitelib}/mysql_utilities*
%if %{with_man}
%{_mandir}/man1/mysql*
# mut command is not installed.
%exclude %{_mandir}/man1/mut*
%endif
# empty file already provided by mysql-connector-python
%exclude %{python_sitelib}/mysql/__init*


%changelog
* Sun Apr 15 2012 Remi Collet <remi@fedoraproject.org> - 1.0.5-2
- fix BR to python2-devel
- incorrect-fsf-address and non-executable-script referenced as
  Oracle BUG#13956819
- remove mut man page (command not installed)

* Thu Apr 11 2012 Remi Collet <remi@fedoraproject.org> - 1.0.5-1
- initial RPM

