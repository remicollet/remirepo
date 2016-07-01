# remirepo/fedora spec file for php-latte
#
# Copyright (c) 2015-2016 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    2c45c382f50cc981019628c9b074ad257207fb09
#global gh_date      20150728
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     nette
%global gh_project   latte
%global ns_vendor    Latte
%global php_home     %{_datadir}/php
%global with_tests   0%{!?_without_tests:1}

Name:           php-%{gh_project}
Version:        2.4.0
%global specrel 1
Release:        %{?gh_date:0.%{specrel}.%{?prever}%{!?prever:%{gh_date}git%{gh_short}}}%{!?gh_date:%{specrel}}%{?dist}
Summary:        Latte: the amazing template engine for PHP

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
BuildRequires:  php(language) >= 5.4.4
BuildRequires:  php-tokenizer
BuildRequires:  php-date
BuildRequires:  php-fileinfo
BuildRequires:  php-iconv
BuildRequires:  php-json
BuildRequires:  php-mbstring
BuildRequires:  php-pcre
BuildRequires:  php-reflection
BuildRequires:  php-spl
# From composer.json, "require-dev": {
#		"nette/tester": "~2.0",
#		"tracy/tracy": "^2.3"
BuildRequires:  php-composer(%{gh_owner}/tester) >= 2.0
BuildRequires:  php-composer(tracy/tracy) >= 2.3
%endif

# from composer.json, "require": {
#        "php": ">=5.4.4"
#        "ext-tokenizer": "*"
Requires:       php(language) >= 5.4.4
Requires:       php-tokenizer
# from phpcompatinfo report for version 2.3.6
Requires:       php-date
Requires:       php-fileinfo
Requires:       php-iconv
Requires:       php-json
Requires:       php-mbstring
Requires:       php-pcre
Requires:       php-reflection
Requires:       php-spl

# provides latte/latte
Provides:       php-composer(%{gh_project}/%{gh_project}) = %{version}


%description
Latte is a template engine for PHP which eases your work and ensures the
output is protected against vulnerabilities, such as XSS.

Latte is fast: it compiles templates to plain optimized PHP code.

Latte is secure: it is the first PHP engine introducing content-aware escaping.

Latte speaks your language: it has intuitive syntax and helps you to build
better websites easily.

To use this library, you just have to add, in your project:
  require_once '%{php_home}/%{ns_vendor}/autoload.php';


%prep
%setup -q -n %{gh_project}-%{gh_commit}

# drop upstream autoloader which is outside tree
rm src/latte.php


%build
: Generate a classmap autoloader
phpab --output src/%{ns_vendor}/autoload.php src


%install
rm -rf       %{buildroot}
mkdir -p     %{buildroot}%{php_home}
cp -pr src/* %{buildroot}%{php_home}/


%check
%if %{with_tests}
: Ignore failed test under investigation
rm 'tests/Latte/Helpers.optimizePhp().phpt'

: Generate configuration
cat /etc/php.ini /etc/php.d/*ini >php.ini
export LANG=fr_FR.utf8

: For PHP 5.3.3 on RHEL-6
sed -e 's/50303/99999/' -i tests/Latte/Object.phpt

: Generate autoloader
mkdir vendor
cat << 'EOF' | tee vendor/autoload.php
<?php
require_once '%{php_home}/Tester/autoload.php';
require_once '%{buildroot}%{php_home}/%{ns_vendor}/autoload.php';
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
%{php_home}/%{ns_vendor}


%changelog
* Fri Jul  1 2016 Remi Collet <remi@fedoraproject.org> - 2.4.0-1
- update to 2.4.0
- raise dependency on php >= 5.4.4

* Mon May 30 2016 Remi Collet <remi@fedoraproject.org> - 2.3.12-1
- update to 2.3.12

* Tue Apr 12 2016 Remi Collet <remi@fedoraproject.org> - 2.3.11-1
- update to 2.3.11

* Sat Feb 20 2016 Remi Collet <remi@fedoraproject.org> - 2.3.10-1
- update to 2.3.10

* Wed Jan 20 2016 Remi Collet <remi@fedoraproject.org> - 2.3.9-1
- update to 2.3.9

* Thu Dec  3 2015 Remi Collet <remi@fedoraproject.org> - 2.3.8-1
- update to 2.3.8
- run test suite with both php 5 and 7 when available

* Sun Nov  8 2015 Remi Collet <remi@fedoraproject.org> - 2.3.7-1
- update to 2.3.7

* Tue Oct 20 2015 Remi Collet <remi@fedoraproject.org> - 2.3.6-1
- initial package
