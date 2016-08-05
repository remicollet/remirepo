# remirepo/fedora spec file for php-nette-database
#
# Copyright (c) 2015-2016 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    05aa9112f3da7cf0ef799ad6b0fe223485deb827
#global gh_date      20150728
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     nette
%global gh_project   database
%global ns_vendor    Nette
%global ns_project   Database
%global php_home     %{_datadir}/php
%if 0%{?rhel} == 6
# mockery is too old
%global with_tests   0%{?_with_tests:1}
%else
%global with_tests   0%{!?_without_tests:1}
%endif

Name:           php-%{gh_owner}-%{gh_project}
Version:        2.4.0
%global specrel 1
Release:        %{?gh_date:0.%{specrel}.%{?prever}%{!?prever:%{gh_date}git%{gh_short}}}%{!?gh_date:%{specrel}}%{?dist}
Summary:        Nette Database Component

Group:          Development/Libraries
License:        BSD or GPLv2 or GPLv3
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        %{name}-%{version}-%{gh_short}.tgz
# pull a git snapshot to get test sutie
Source1:        makesrc.sh

Patch0:         %{name}-upstream.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php-composer(theseer/autoload)
%if %{with_tests}
BuildRequires:  php(language) >= 5.6
BuildRequires:  php-pdo
BuildRequires:  php-composer(%{gh_owner}/caching) >= 2.2
BuildRequires:  php-composer(%{gh_owner}/utils) >= 2.4
BuildRequires:  php-date
BuildRequires:  php-json
BuildRequires:  php-pcre
BuildRequires:  php-spl
# From composer.json, "require-dev": {
#               "nette/tester": "~2.0",
#               "nette/di": "~2.4",
#               "mockery/mockery": "~1.0.0",
#               "tracy/tracy": "^2.4"
BuildRequires:  php-composer(%{gh_owner}/tester) >= 2.0
BuildRequires:  php-composer(%{gh_owner}/di) >= 2.4
# version 1.0.0 is not released
BuildRequires:  php-composer(mockery/mockery) >= 0.9.1
BuildRequires:  php-composer(tracy/tracy) >= 2.3
%endif

# from composer.json, "require": {
#        "php": ">=5.6.0"
#        "ext-pdo": "*",
#        "nette/caching": "~2.2",
#        "nette/utils": "~2.4"
Requires:       php(language) >= 5.6
Requires:       php-pdo
Requires:       php-composer(%{gh_owner}/caching) >= 2.2
Requires:       php-composer(%{gh_owner}/caching) <  3
Requires:       php-composer(%{gh_owner}/utils) >= 2.4
Requires:       php-composer(%{gh_owner}/utils) <  3
# from phpcompatinfo report for version 2.4.0
Requires:       php-date
Requires:       php-json
Requires:       php-pcre
Requires:       php-spl

Provides:       php-composer(%{gh_owner}/%{gh_project}) = %{version}


%description
Nette provides a powerful layer for accessing your database easily.

- composes SQL queries with ease
- easily fetches data
- uses efficient queries and does not transmit unnecessary data

The Nette\Database\Connection class is a wrapper around the PDO
and represents a connection to the database. The core functionality
is provided by Nette\Database\Context. Nette\Database\Table layer
provides an enhanced layer for table querying.

To use this library, you just have to add, in your project:
  require_once '%{php_home}/%{ns_vendor}/%{ns_project}/autoload.php';


%prep
%setup -q -n %{gh_project}-%{gh_commit}

%patch0 -p1


%build
: Generate a classmap autoloader
phpab --output src/%{ns_project}/autoload.php src

cat << 'EOF' | tee -a src/%{ns_project}/autoload.php
// Dependencies
require_once '%{php_home}/%{ns_vendor}/Caching/autoload.php';
require_once '%{php_home}/%{ns_vendor}/Utils/autoload.php';
EOF


%install
rm -rf       %{buildroot}
mkdir -p     %{buildroot}%{php_home}/%{ns_vendor}
cp -pr src/* %{buildroot}%{php_home}/%{ns_vendor}/


%check
%if %{with_tests}
export LANG=fr_FR.utf8

%if 0%{?rhel} != 5
: Generate minimal Sqlite condiguration
cat << 'EOF' | tee tests/Database/databases.ini
[sqlite]
dsn = "sqlite::memory:"
EOF
%endif

: Generate autoloader
mkdir vendor
cat << 'EOF' | tee vendor/autoload.php
<?php
require_once '%{php_home}/Tester/autoload.php';
require_once '%{php_home}/%{ns_vendor}/DI/autoload.php';
require_once '%{php_home}/Mockery/autoload.php';
require_once '%{buildroot}%{php_home}/%{ns_vendor}/%{ns_project}/autoload.php';
EOF

: Run test suite in sources tree
# remirepo:11
ret=0
run=0
if which php56; then
   php56 %{_bindir}/nette-tester --colors 0 -p php56 -C tests -s || ret=1
   run=1
fi
if which php71; then
   php71 %{_bindir}/nette-tester --colors 0 -p php71 -C tests -s || ret=1
   run=1
fi
if [ $run -eq 0 ]; then
%{_bindir}/nette-tester --colors 0 -p php -C tests -s
# remirepo:2
fi
exit $ret
%else
: Test suite disabled
%endif


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license license.md
%doc readme.md contributing.md
%doc composer.json
%{php_home}/%{ns_vendor}/%{ns_project}
%{php_home}/%{ns_vendor}/Bridges


%changelog
* Thu Aug  4 2016 Remi Collet <remi@fedoraproject.org> - 2.4.0-1
- update to 2.4.0
- raise dependency on PHP >= 5.6
- raise dependency on nette/utils >= 2.4

* Wed Jun  1 2016 Remi Collet <remi@fedoraproject.org> - 2.3.9-1
- update to 2.3.9

* Thu Dec  3 2015 Remi Collet <remi@fedoraproject.org> - 2.3.8-1
- update to 2.3.8
- run test suite with both php 5 and 7 when available

* Fri Oct 30 2015 Remi Collet <remi@fedoraproject.org> - 2.3.7-1
- initial package
