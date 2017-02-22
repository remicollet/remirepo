# remirepo/Fedora spec file for php-zendframework-zend-filter
#
# Copyright (c) 2015-2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global bootstrap    0
%global gh_commit    84c50246428efb0a1e52868e162dab3e149d5b80
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     zendframework
%global gh_project   zend-filter
%global php_home     %{_datadir}/php
%global library      Filter
%if %{bootstrap}
%global with_tests   0%{?_with_tests:1}
%else
%global with_tests   0%{!?_without_tests:1}
%endif
%global php_version  %(php -r 'echo PHP_VERSION;')

Name:           php-%{gh_owner}-%{gh_project}
Version:        2.7.1
Release:        3%{?dist}
Summary:        Zend Framework %{library} component

Group:          Development/Libraries
License:        BSD
URL:            https://zendframework.github.io/%{gh_project}/
Source0:        %{gh_commit}/%{name}-%{version}-%{gh_short}.tgz
Source1:        makesrc.sh

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch:      noarch
# Tests
%if %{with_tests}
BuildRequires:  php(language) >= 5.5
BuildRequires:  php-date
BuildRequires:  php-iconv
BuildRequires:  php-mbstring
BuildRequires:  php-mcrypt
BuildRequires:  php-pcre
BuildRequires:  php-spl
BuildRequires:  php-zip
BuildRequires:  php-composer(%{gh_owner}/zend-stdlib)           >= 2.7
# From composer, "require-dev": {
#        "pear/archive_tar": "^1.4",
#        "zendframework/zend-crypt": "^2.6",
#        "zendframework/zend-servicemanager": "^2.7.5 || ^3.0.3",
#        "zendframework/zend-uri": "^2.5",
#        "fabpot/php-cs-fixer": "1.7.*",
#        "phpunit/PHPUnit": "~4.0"
BuildRequires:  php-composer(pear/archive_tar)                  >= 1.4
BuildRequires:  php-composer(%{gh_owner}/zend-crypt)            >= 2.5
BuildRequires:  php-composer(%{gh_owner}/zend-servicemanager)   >= 2.5
BuildRequires:  php-composer(%{gh_owner}/zend-uri)              >= 2.5
BuildRequires:  php-composer(phpunit/phpunit)                   >= 4.0
# Autoloader
BuildRequires:  php-composer(%{gh_owner}/zend-loader)           >= 2.5
%endif

# From composer, "require": {
#        "php": "^5.5 || ^7.0",
#        "zendframework/zend-stdlib": "^2.7 || ^3.0"
Requires:       php(language) >= 5.5
Requires:       php-composer(%{gh_owner}/zend-stdlib)           >= 2.7
Requires:       php-composer(%{gh_owner}/zend-stdlib)           <  4
%if ! %{bootstrap}
# From composer, "suggest": {
#        "zendframework/zend-crypt": "Zend\\Crypt component",
#        "zendframework/zend-i18n": "Zend\\I18n component",
#        "zendframework/zend-servicemanager": "Zend\\ServiceManager component",
#        "zendframework/zend-uri": "Zend\\Uri component for UriNormalize filter"
%if 0%{?fedora} >= 21
Suggests:       php-composer(%{gh_owner}/zend-crypt)
Suggests:       php-composer(%{gh_owner}/zend-i18n)
Suggests:       php-composer(%{gh_owner}/zend-servicemanager)
Suggests:       php-composer(%{gh_owner}/zend-uri)
%endif
%endif
# From phpcompatinfo report for version 2.5.2
Requires:       php-date
Requires:       php-iconv
Requires:       php-mbstring
Requires:       php-pcre
Requires:       php-spl
Requires:       php-zip

Obsoletes:      php-ZendFramework2-%{library} < 2.5
Provides:       php-ZendFramework2-%{library} = %{version}
Provides:       php-composer(%{gh_owner}/%{gh_project}) = %{version}


%description
The Zend\Filter component provides a set of commonly needed data filters.
It also provides a simple filter chaining mechanism by which multiple
filters may be applied to a single datum in a user-defined order.

Documentation: https://zendframework.github.io/%{gh_project}/


%prep
%setup -q -n %{gh_project}-%{gh_commit}

mv LICENSE.md LICENSE


%build
# Empty build section, nothing required


%install
rm -rf %{buildroot}

mkdir -p   %{buildroot}%{php_home}/Zend/
cp -pr src %{buildroot}%{php_home}/Zend/%{library}


%check
%if %{with_tests}
mkdir vendor
cat << 'EOF' | tee vendor/autoload.php
<?php
require_once '%{php_home}/Zend/Loader/AutoloaderFactory.php';
Zend\Loader\AutoloaderFactory::factory(array(
    'Zend\Loader\StandardAutoloader' => array(
        'namespaces' => array(
           'ZendTest\\%{library}' => dirname(__DIR__).'/test/',
           'Zend\\%{library}'     => '%{buildroot}%{php_home}/Zend/%{library}'
))));
require_once '%{php_home}/Zend/autoload.php';
EOF

# remirepo:18
run=0
ret=0
if which php56; then
   php56 %{_bindir}/phpunit || ret=1
   run=1
fi
if which php70; then
   php70 %{_bindir}/phpunit || ret=1
   run=1
fi
if which php71; then
   # For mcrypt and PHP 7.1
   sed -e '/error_reporting/s/. E_STRICT/- E_DEPRECATED/' -i test/bootstrap.php
   sed -e 's/colors=/convertErrorsToExceptions="false" colors=/' phpunit.xml.dist > phpunit.xml
   php71 %{_bindir}/phpunit || ret=1
   run=1
fi
if [ $run -eq 0 ]; then
%if "%{php_version}" > "7.1"
   sed -e '/error_reporting/s/. E_STRICT/- E_DEPRECATED/' -i test/bootstrap.php
   sed -e 's/colors=/convertErrorsToExceptions="false" colors=/' phpunit.xml.dist > phpunit.xml
%endif
%{_bindir}/phpunit --verbose
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
%license LICENSE
%doc *.md
%doc composer.json
%{php_home}/Zend/%{library}


%changelog
* Wed Feb 22 2017 Remi Collet <remi@fedoraproject.org> - 2.7.1-3
- don't convertErrorsToExceptions, fix FTBFS #1424085

* Fri Nov 25 2016 Remi Collet <remi@fedoraproject.org> - 2.7.1-2
- fix FTBFS, disable E_DEPRECATED during test suite

* Tue Apr 19 2016 Remi Collet <remi@fedoraproject.org> - 2.7.1-1
- update to 2.7.1

* Wed Apr  6 2016 Remi Collet <remi@fedoraproject.org> - 2.7.0-1
- update to 2.7.0

* Fri Feb 12 2016 Remi Collet <remi@fedoraproject.org> - 2.6.1-1
- update to 2.6.1

* Fri Feb  5 2016 Remi Collet <remi@fedoraproject.org> - 2.6.0-1
- update to 2.6.0
- raise dependency on PHP >= 5.5
- raise dependency on zend-stdlib >= 2.7

* Tue Aug  4 2015 Remi Collet <remi@fedoraproject.org> - 2.5.1-1
- initial package
