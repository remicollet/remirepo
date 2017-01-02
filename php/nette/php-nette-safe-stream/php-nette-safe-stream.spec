# remirepo/fedora spec file for php-nette-safe-stream
#
# Copyright (c) 2015-2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    4b9bb3266a537e59b10a2932f05dca47333420fc
#global gh_date      20150728
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     nette
%global gh_project   safe-stream
%global ns_vendor    Nette
%global ns_project   SafeStream
%global php_home     %{_datadir}/php
%global with_tests   0%{!?_without_tests:1}

Name:           php-%{gh_owner}-%{gh_project}
Version:        2.3.2
%global specrel 1
Release:        %{?gh_date:0.%{specrel}.%{?prever}%{!?prever:%{gh_date}git%{gh_short}}}%{!?gh_date:%{specrel}}%{?dist}
Summary:        Nette SafeStream: Atomic Operations

Group:          Development/Libraries
License:        BSD or GPLv2 or GPLv3
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        %{name}-%{version}-%{gh_short}.tgz
# pull a git snapshot to get test suite
Source1:        makesrc.sh

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php-composer(theseer/autoload)
%if %{with_tests}
BuildRequires:  php(language) >= 5.3.1
BuildRequires:  php-date
# From composer.json, "require-dev": {
#        "nette/tester": "~1.0"
#		"tracy/tracy": "^2.3"
BuildRequires:  php-composer(%{gh_owner}/tester) >= 1.0
BuildRequires:  php-composer(tracy/tracy) >= 2.3
%endif

# from composer.json, "require": {
#        "php": ">=5.3.1"
Requires:       php(language) >= 5.3.1
# from phpcompatinfo report for version 2.3.1
Requires:       php-date

Provides:       php-composer(%{gh_owner}/%{gh_project}) = %{version}


%description
The Nette\Utils\SafeStram protocol for file manipulation guarantees
atomicity and isolation of every file operation.

To use this library, you just have to add, in your project:
  require_once '%{php_home}/%{ns_vendor}/%{ns_project}/autoload.php';


%prep
%setup -q -n %{gh_project}-%{gh_commit}


%build
# Notice: upstream provides src/loader.php, but out of the NS tree

: Generate a classmap autoloader
phpab --output src/%{ns_project}/autoload.php src

cat << 'EOF' | tee -a src/%{ns_project}/autoload.php
Nette\Utils\SafeStream::register();
EOF


%install
rm -rf       %{buildroot}
mkdir -p     %{buildroot}%{php_home}/%{ns_vendor}
cp -pr src/* %{buildroot}%{php_home}/%{ns_vendor}/
rm  %{buildroot}%{php_home}/%{ns_vendor}/loader.php

%check
%if %{with_tests}
: Generate configuration
cat /etc/php.ini /etc/php.d/*ini >php.ini
export LANG=fr_FR.utf8

: Generate autoloader
mkdir vendor
cat << 'EOF' | tee vendor/autoload.php
<?php
require_once '%{php_home}/Tester/autoload.php';
require_once '%{php_home}/Tracy/autoload.php';
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
%{_bindir}/nette-tester --colors 0 -p php -c ./php.ini tests -s
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
%dir %{php_home}/%{ns_vendor}
     %{php_home}/%{ns_vendor}/%{ns_project}


%changelog
* Sat Apr  2 2016 Remi Collet <remi@fedoraproject.org> - 2.3.2-1
- update to 2.3.2
- run test suite with both php 5 and 7 when available

* Mon Nov  9 2015 Remi Collet <remi@fedoraproject.org> - 2.3.1-2
- fix directory ownership, from review #1277441

* Fri Oct 30 2015 Remi Collet <remi@fedoraproject.org> - 2.3.1-1
- initial package
