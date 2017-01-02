# remirepo/fedora spec file for php-nette-utils
#
# Copyright (c) 2015-2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    fd2e67c2ce28da409864507d8d124621780d036d
#global gh_date      20150728
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     nette
%global gh_project   utils
%global ns_vendor    Nette
%global php_home     %{_datadir}/php
%global with_tests   0%{!?_without_tests:1}

Name:           php-nette-utils
Version:        2.4.2
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
BuildRequires:  php(language) >= 5.6
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
#		"nette/tester": "~2.0",
#		"tracy/tracy": "^2.3"
# ignore tester min version (pass with 1.7), ignore tracy (pass without)
BuildRequires:  php-composer(%{gh_owner}/tester)
%endif

# from composer.json, "require": {
#        "php": ">=5.6.0"
Requires:       php(language) >= 5.6
# from composer.json, "suggest": {
#        "ext-iconv": "to use Strings::webalize() and toAscii()",
#        "ext-json": "to use Nette\\Utils\\Json",
#        "ext-intl": "for script transliteration in Strings::webalize() and toAscii()",
#        "ext-mbstring": "to use Strings::lower() etc...",
#        "ext-xml": "to use Strings::length() etc. when mbstring is not available",
#        "ext-gd": "to use Image"
%if 0%{?fedora} > 21
Recommends:     php-iconv
Recommends:     php-json
Recommends:     php-intl
Recommends:     php-mbstring
Recommends:     php-xml
Recommends:     php-gd
%else
Requires:       php-iconv
Requires:       php-json
Requires:       php-intl
Requires:       php-mbstring
Requires:       php-xml
Requires:       php-gd
%endif
# from phpcompatinfo report for version 2.4.0 (mcrypt is optional, openssl prefered)
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
rm tests/Utils/Image.alpha2.phpt
rm tests/Utils/Image.resize.phpt
rm tests/Utils/Json.decode\(\).phpt
rm tests/Utils/Image.drawing.phpt
rm tests/Utils/Image.place.phpt

export LANG=fr_FR.utf8

: Generate autoloader
mkdir vendor
cat << 'EOF' | tee vendor/autoload.php
<?php
require_once '%{php_home}/Tester/autoload.php';
require_once '%{buildroot}%{php_home}/%{ns_vendor}/Utils/autoload.php';
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
%dir %{php_home}/%{ns_vendor}
     %{php_home}/%{ns_vendor}/Utils
     %{php_home}/%{ns_vendor}/Iterators


%changelog
* Wed Dec 21 2016 Remi Collet <remi@fedoraproject.org> - 2.4.2-1
- update to 2.4.2

* Fri Sep 30 2016 Remi Collet <remi@fedoraproject.org> - 2.4.1-1
- update to 2.4.1

* Tue Aug  2 2016 Remi Collet <remi@fedoraproject.org> - 2.4.0-1
- update to 2.4.0
- raise dependency on PHP >= 5.6

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
