# remirepo/fedora spec file for php-nette-di
#
# Copyright (c) 2015-2016 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    fe4d3264d1b1907a934e8a6627a5b87f35046089
#global gh_date      20150728
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     nette
%global gh_project   di
%global ns_vendor    Nette
%global ns_project   DI
%global php_home     %{_datadir}/php
%global with_tests   0%{!?_without_tests:1}

Name:           php-%{gh_owner}-%{gh_project}
Version:        2.3.13
%global specrel 1
Release:        %{?gh_date:0.%{specrel}.%{?prever}%{!?prever:%{gh_date}git%{gh_short}}}%{!?gh_date:%{specrel}}%{?dist}
Summary:        Nette Dependency Injection Component

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
BuildRequires:  php-pcre
BuildRequires:  php-reflection
BuildRequires:  php-spl
BuildRequires:  php-tokenizer
BuildRequires:  php-composer(%{gh_owner}/neon) >= 2.3.3
BuildRequires:  php-composer(%{gh_owner}/php-generator) >= 2.3.6
BuildRequires:  php-composer(%{gh_owner}/utils) >= 2.3.5
# From composer.json, "require-dev": {
#        "nette/tester": "~1.6"
BuildRequires:  php-composer(%{gh_owner}/tester) >= 1.6
%endif

# from composer.json, "require": {
#        "php": ">=5.3.1"
#        "nette/neon": "^2.3.3",
#        "nette/php-generator": "^2.3.6",
#        "nette/utils": "^2.3.5"
Requires:       php(language) >= 5.3.1
Requires:       php-composer(%{gh_owner}/neon) >= 2.3.3
Requires:       php-composer(%{gh_owner}/neon) <  3
Requires:       php-composer(%{gh_owner}/php-generator) >= 2.3.6
Requires:       php-composer(%{gh_owner}/php-generator) <  3
Requires:       php-composer(%{gh_owner}/utils) >= 2.3.5
Requires:       php-composer(%{gh_owner}/utils) <  3
# from phpcompatinfo report for version 2.3.6
Requires:       php-pcre
Requires:       php-reflection
Requires:       php-spl
Requires:       php-tokenizer

Provides:       php-composer(%{gh_owner}/%{gh_project}) = %{version}


%description
Purpose of the Dependecy Injection (DI) is to free classes from the
responsibility for obtaining objects that they need for its operation
(these objects are called services). To pass them these services on their
instantiation instead.

Nette DI is one of the most interesting part of framework.
It is compiled DI container, extremely fast and easy to configure.

To use this library, you just have to add, in your project:
  require_once '%{php_home}/%{ns_vendor}/%{ns_project}/autoload.php';


%prep
%setup -q -n %{gh_project}-%{gh_commit}


%build
: Generate a classmap autoloader
phpab --output src/%{ns_project}/autoload.php src

cat << 'EOF' | tee -a src/%{ns_project}/autoload.php
// Dependencies
require_once '%{php_home}/%{ns_vendor}/Neon/autoload.php';
require_once '%{php_home}/%{ns_vendor}/PhpGenerator/autoload.php';
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

: See https://github.com/nette/di/commit/0b83ea7a788cef9d2bceafd543201aa309790ed3
sed -e 's/file_put_contents/@mkdir(TEMP_DIR,0777,true); file_put_contents/' -i tests/bootstrap.php

: Generate autoloader
mkdir vendor
cat << 'EOF' | tee vendor/autoload.php
<?php
require_once '%{php_home}/Tester/autoload.php';
require_once '%{buildroot}%{php_home}/%{ns_vendor}/%{ns_project}/autoload.php';
EOF

: Run test suite in sources tree
%{_bindir}/nette-tester --colors 0 -p php -c ./php.ini tests -s
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
* Wed Dec 21 2016 Remi Collet <remi@fedoraproject.org> - 2.3.13-1
- update to 2.3.13

* Sun Jul 31 2016 Remi Collet <remi@fedoraproject.org> - 2.3.12-1
- update to 2.3.12

* Mon Jun 20 2016 Remi Collet <remi@fedoraproject.org> - 2.3.11-1
- update to 2.3.11

* Sat Apr  2 2016 Remi Collet <remi@fedoraproject.org> - 2.3.10-1
- update to 2.3.10

* Sat Feb 20 2016 Remi Collet <remi@fedoraproject.org> - 2.3.9-1
- update to 2.3.9

* Wed Jan 20 2016 Remi Collet <remi@fedoraproject.org> - 2.3.8-1
- update to 2.3.8

* Thu Dec  3 2015 Remi Collet <remi@fedoraproject.org> - 2.3.7-1
- update to 2.3.7
- run test suite with both php 5 and 7 when available

* Tue Oct 20 2015 Remi Collet <remi@fedoraproject.org> - 2.3.6-1
- initial package
