# remirepo/fedora spec file for php-nette-utils
#
# Copyright (c) 2015-2016 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    f213ad4d9dfb7221322bd2808e2004b61c8ece8e
#global gh_date      20150728
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     nette
%global gh_project   utils
%global ns_vendor    Nette
%global php_home     %{_datadir}/php
%global with_tests   0%{!?_without_tests:1}

Name:           php-nette-utils
Version:        2.3.11
%global specrel 1
Release:        %{?gh_date:0.%{specrel}.%{?prever}%{!?prever:%{gh_date}git%{gh_short}}}%{!?gh_date:%{specrel}}%{?dist}
Summary:        Nette Utility Classes

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
BuildRequires:  php-iconv
BuildRequires:  php-intl
BuildRequires:  php-mbstring
BuildRequires:  php-gd
BuildRequires:  php-date
BuildRequires:  php-fileinfo
BuildRequires:  php-json
BuildRequires:  php-mcrypt
BuildRequires:  php-openssl
BuildRequires:  php-pcre
BuildRequires:  php-reflection
BuildRequires:  php-spl
BuildRequires:  php-xml
# From composer.json, "require-dev": {
#        "nette/tester": "~1.0"
BuildRequires:  php-composer(%{gh_owner}/tester)
%endif

# from composer.json, "require": {
#        "php": ">=5.3.1"
Requires:       php(language) >= 5.3.1
# from composer.json, "suggest": {
#        "ext-iconv": "to use Strings::webalize() and toAscii()",
#        "ext-json": "to use Nette\\Utils\\Json",
#        "ext-intl": "for script transliteration in Strings::webalize() and toAscii()",
#        "ext-mbstring": "to use Strings::lower() etc...",
#        "ext-xml": "to use Strings::length() etc. when mbstring is not available",
#        "ext-gd": "to use Image"
Requires:       php-iconv
Requires:       php-json
Requires:       php-intl
Requires:       php-mbstring
Requires:       php-xml
Requires:       php-gd
# from phpcompatinfo report for version 2.3.6 (mcrypt is optional, openssl prefered)
Requires:       php-date
Requires:       php-fileinfo
Requires:       php-openssl
Requires:       php-pcre
Requires:       php-reflection
Requires:       php-spl

Provides:       php-composer(%{gh_owner}/%{gh_project}) = %{version}


%description
Nette Utility Classes.

To use this library, you just have to add, in your project:
  require_once '%{php_home}/%{ns_vendor}/Utils/autoload.php';';


%prep
%setup -q -n %{gh_project}-%{gh_commit}


%build
: Generate a classmap autoloader
phpab --output src/Utils/autoload.php src


%install
rm -rf       %{buildroot}
mkdir -p     %{buildroot}%{php_home}/%{ns_vendor}
cp -pr src/* %{buildroot}%{php_home}/%{ns_vendor}/


%check
%if %{with_tests}
: Ignore failed tests under investigation
rm tests/Utils/Image.alpha1.phpt
rm tests/Utils/Json.decode\(\).phpt
rm tests/Utils/Image.drawing.phpt

: Generate configuration
cat /etc/php.ini /etc/php.d/*ini >php.ini
export LANG=fr_FR.utf8

: For PHP 5.3.3 on RHEL-6
sed -e 's/50303/99999/' -i tests/Utils/Object.magicMethod.errors.phpt

: Generate autoloader
mkdir vendor
cat << 'EOF' | tee vendor/autoload.php
<?php
require_once '%{php_home}/Tester/autoload.php';
require_once '%{buildroot}%{php_home}/%{ns_vendor}/Utils/autoload.php';
EOF

: Run test suite in sources tree
nette-tester --colors 0 -p php -c ./php.ini tests -s
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
     %{php_home}/%{ns_vendor}/Utils
     %{php_home}/%{ns_vendor}/Iterators


%changelog
* Mon Jun 20 2016 Remi Collet <remi@fedoraproject.org> - 2.3.10-1
- update to 2.3.10

* Thu Jun  2 2016 Remi Collet <remi@fedoraproject.org> - 2.3.9-1
- update to 2.3.9

* Sat Apr  2 2016 Remi Collet <remi@fedoraproject.org> - 2.3.8-1
- update to 2.3.8
- run test suite with both php 5 and 7 when available

* Mon Nov 30 2015 Remi Collet <remi@fedoraproject.org> - 2.3.7-1
- update to 2.3.7

* Tue Oct 20 2015 Remi Collet <remi@fedoraproject.org> - 2.3.6-1
- initial package
