# remirepo/fedora spec file for php-nette-database
#
# Copyright (c) 2015-2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    ed0dc48c58ddf9042f736f3c1ac431dfdd825019
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
Version:        2.3.10
%global specrel 1
Release:        %{?gh_date:0.%{specrel}.%{?prever}%{!?prever:%{gh_date}git%{gh_short}}}%{!?gh_date:%{specrel}}%{?dist}
Summary:        Nette Database Component

Group:          Development/Libraries
License:        BSD or GPLv2 or GPLv3
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        %{name}-%{version}-%{gh_short}.tgz
# pull a git snapshot to get test sutie
Source1:        makesrc.sh

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php-composer(theseer/autoload)
%if %{with_tests}
BuildRequires:  php(language) >= 5.3.1
BuildRequires:  php-pdo
BuildRequires:  php-composer(%{gh_owner}/caching) >= 2.2
BuildRequires:  php-composer(%{gh_owner}/utils) >= 2.2
BuildRequires:  php-date
BuildRequires:  php-json
BuildRequires:  php-pcre
BuildRequires:  php-spl
# From composer.json, "require-dev": {
#        "nette/tester": "^1.3"
#        "nette/di": "^2.3",
#        "mockery/mockery": "^0.9.1"
BuildRequires:  php-composer(%{gh_owner}/tester) >= 1.3
BuildRequires:  php-composer(%{gh_owner}/di) >= 2.3
BuildRequires:  php-composer(mockery/mockery) >= 0.9.1
%endif

# from composer.json, "require": {
#        "php": ">=5.3.1"
#        "ext-pdo": "*",
#        "nette/caching": "^2.2",
#        "nette/utils": "^2.3.5"
Requires:       php(language) >= 5.3.1
Requires:       php-pdo
Requires:       php-composer(%{gh_owner}/caching) >= 2.2
Requires:       php-composer(%{gh_owner}/caching) <  3
Requires:       php-composer(%{gh_owner}/utils) >= 2.3.5
Requires:       php-composer(%{gh_owner}/utils) <  3
# from phpcompatinfo report for version 2.3.7
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
: Generate configuration
cat /etc/php.ini /etc/php.d/*ini >php.ini
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
%{_bindir}/nette-tester --colors 0 -p php -c ./php.ini tests -s

if which php70; then
  cat /etc/opt/remi/php70/php.ini /etc/opt/remi/php70/php.d/*ini >php.ini
  php70 %{_bindir}/nette-tester --colors 0 -p php70 -c ./php.ini tests -s
fi
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
* Wed Oct 19 2016 Remi Collet <remi@fedoraproject.org> - 2.3.10-1
- update to 2.3.10

* Wed Jun  1 2016 Remi Collet <remi@fedoraproject.org> - 2.3.9-1
- update to 2.3.9

* Thu Dec  3 2015 Remi Collet <remi@fedoraproject.org> - 2.3.8-1
- update to 2.3.8
- run test suite with both php 5 and 7 when available

* Fri Oct 30 2015 Remi Collet <remi@fedoraproject.org> - 2.3.7-1
- initial package
