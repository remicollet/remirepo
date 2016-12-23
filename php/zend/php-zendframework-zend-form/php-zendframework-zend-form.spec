# remirepo/Fedora spec file for php-zendframework-zend-form
#
# Copyright (c) 2015-2016 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global bootstrap    0
%global gh_commit    2d076100e4c6a779b7676d098192e3d1cf74f34e
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     zendframework
%global gh_project   zend-form
%global php_home     %{_datadir}/php
%global library      Form
%if %{bootstrap}
%global with_tests   0%{?_with_tests:1}
%else
%global with_tests   0%{!?_without_tests:1}
%endif

Name:           php-%{gh_owner}-%{gh_project}
Version:        2.9.2
Release:        1%{?dist}
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
BuildRequires:  php(language) >= 5.3.23
BuildRequires:  php-date
BuildRequires:  php-intl
BuildRequires:  php-pcre
BuildRequires:  php-spl
# Temporary, see https://github.com/zendframework/zend-math/issues/23
BuildRequires:  php-mcrypt
BuildRequires:  php-composer(%{gh_owner}/zend-inputfilter)      >= 2.5
BuildRequires:  php-composer(%{gh_owner}/zend-hydrator)         >= 1.0
BuildRequires:  php-composer(%{gh_owner}/zend-stdlib)           >= 2.7
# From composer, "require-dev": {
#        "doctrine/annotations": "~1.0",
#        "zendframework/zend-cache": "^2.6.1",
#        "zendframework/zend-captcha": "^2.5.4",
#        "zendframework/zend-code": "^2.6 || ^3.0",
#        "zendframework/zend-escaper": "^2.5",
#        "zendframework/zend-eventmanager": "^2.6.2 || ^3.0",
#        "zendframework/zend-filter": "^2.6",
#        "zendframework/zend-i18n": "^2.6",
#        "zendframework/zend-servicemanager": "^2.7.5 || ^3.0.3",
#        "zendframework/zend-session": "^2.6.2",
#        "zendframework/zend-text": "^2.6",
#        "zendframework/zend-validator": "^2.6",
#        "zendframework/zend-view": "^2.6.2",
#        "zendframework/zendservice-recaptcha": "*",
#        "fabpot/php-cs-fixer": "1.7.*",
#        "phpunit/PHPUnit": "~4.8"
BuildRequires:  php-composer(doctrine/annotations)              >= 1.0
BuildRequires:  php-composer(%{gh_owner}/zend-cache)            >= 2.6.1
BuildRequires:  php-composer(%{gh_owner}/zend-captcha)          >= 2.5.4
BuildRequires:  php-composer(%{gh_owner}/zend-code)             >= 2.6
BuildRequires:  php-composer(%{gh_owner}/zend-escaper)          >= 2.5
BuildRequires:  php-composer(%{gh_owner}/zend-eventmanager)     >= 2.6.2
BuildRequires:  php-composer(%{gh_owner}/zend-filter)           >= 2.6
BuildRequires:  php-composer(%{gh_owner}/zend-i18n)             >= 2.6
BuildRequires:  php-composer(%{gh_owner}/zend-servicemanager)   >= 2.7.5
BuildRequires:  php-composer(%{gh_owner}/zend-session)          >= 2.6.2
BuildRequires:  php-composer(%{gh_owner}/zend-text)             >= 2.6
BuildRequires:  php-composer(%{gh_owner}/zend-validator)        >= 2.6
BuildRequires:  php-composer(%{gh_owner}/zend-view)             >= 2.6.2
BuildRequires:  php-composer(phpunit/phpunit)                   >= 4.8
# Missing
BuildRequires:  php-composer(ircmaxell/random-lib)
# Autoloader
#BuildRequires:  php-composer(%{gh_owner}/zend-loader)           >= 2.5
# For dependencies autoloader
BuildRequires:  php-zendframework-zend-loader                   >= 2.5.1-3
%endif

# From composer, "require": {
#        "php": ">=5.5",
#        "zendframework/zend-inputfilter": "^2.6",
#        "zendframework/zend-hydrator": "^1.1 || ^2.1",
#        "zendframework/zend-stdlib": "^2.7 || ^3.0"
Requires:       php(language) >= 5.5
%if ! %{bootstrap}
Requires:       php-composer(%{gh_owner}/zend-inputfilter)      >= 2.6
Requires:       php-composer(%{gh_owner}/zend-inputfilter)      <  3
Requires:       php-composer(%{gh_owner}/zend-hydrator)         >= 1.1
Requires:       php-composer(%{gh_owner}/zend-hydrator)         <  3
Requires:       php-composer(%{gh_owner}/zend-stdlib)           >= 2.7
Requires:       php-composer(%{gh_owner}/zend-stdlib)           <  4
# From composer, "suggest": {
#        "zendframework/zend-captcha": "^2.5.4, required for using CAPTCHA form elements",
#        "zendframework/zend-code": "^2.6 || ^3.0, required to use zend-form annotations support",
#        "zendframework/zend-eventmanager": "^2.6.2 || ^3.0, reuired for zend-form annotations support",
#        "zendframework/zend-i18n": "^2.6, required when using zend-form view helpers",
#        "zendframework/zend-servicemanager": "^2.7.5 || ^3.0.3, required to use the form factories or provide services",
#        "zendframework/zend-view": "^2.6.2, required for using the zend-form view helpers",
#        "zendframework/zendservice-recaptcha": "in order to use the ReCaptcha form element"
%if 0%{?fedora} >= 21
Suggests:       php-composer(%{gh_owner}/zend-captcha)
Suggests:       php-composer(%{gh_owner}/zend-code)
Suggests:       php-composer(%{gh_owner}/zend-eventmanager)
Suggests:       php-composer(%{gh_owner}/zend-i18n)
Suggests:       php-composer(%{gh_owner}/zend-servicemanager)
Suggests:       php-composer(%{gh_owner}/zend-view)
#Suggests:       php-composer(%{gh_owner}/zendservice-recaptcha)
%endif
%endif
# From phpcompatinfo report for version 2.6.0
Requires:       php-date
Requires:       php-intl
Requires:       php-pcre
Requires:       php-spl

Obsoletes:      php-ZendFramework2-%{library} < 2.5
Provides:       php-ZendFramework2-%{library} = %{version}
Provides:       php-composer(%{gh_owner}/%{gh_project}) = %{version}


%description
The Zend\Form is intended primarily as a bridge between your domain models
and the View Layer. It composes a thin layer of objects representing form
elements, an InputFilter, and a small number of methods for binding data to
and from the form and attached objects.

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

cp -p autoload/formElementManagerPolyfill.php \
      %{buildroot}%{php_home}/Zend/%{library}-autoload.php


%check
%if %{with_tests}
mkdir vendor
cat << 'EOF' | tee vendor/autoload.php
<?php
define('RPM_BUILDROOT', '%{buildroot}%{php_home}/Zend');

require_once '%{php_home}/Zend/Loader/AutoloaderFactory.php';
Zend\Loader\AutoloaderFactory::factory(array(
    'Zend\Loader\StandardAutoloader' => array(
        'namespaces' => array(
           'ZendTest\\%{library}' => dirname(__DIR__).'/test/',
           'Zend\\%{library}'     => '%{buildroot}%{php_home}/Zend/%{library}'
))));
require_once '%{php_home}/Zend/autoload.php';
EOF

# remirepo:11
run=0
ret=0
if which php56; then
   php56 %{_bindir}/phpunit -d memory_limit=1G || ret=1
   run=1
fi
if which php71; then
   php71 %{_bindir}/phpunit -d memory_limit=1G || ret=1
   run=1
fi
if [ $run -eq 0 ]; then
%{_bindir}/phpunit -d memory_limit=1G --verbose
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
%{php_home}/Zend/%{library}-autoload.php


%changelog
* Fri Sep 23 2016 Remi Collet <remi@fedoraproject.org> - 2.9.2-1
- update to 2.9.2

* Thu Sep 15 2016 Remi Collet <remi@fedoraproject.org> - 2.9.1-1
- update to 2.9.1

* Fri Jun 10 2016 Remi Collet <remi@fedoraproject.org> - 2.9.0-1
- update to 2.9.0

* Wed May  4 2016 Remi Collet <remi@fedoraproject.org> - 2.8.3-1
- update to 2.8.3

* Mon May  2 2016 Remi Collet <remi@fedoraproject.org> - 2.8.2-1
- update to 2.8.2
- raise dependency on zend-loader >= 2.5.1-3

* Sun May  1 2016 Remi Collet <remi@fedoraproject.org> - 2.8.1-1
- update to 2.8.1

* Fri Apr  8 2016 Remi Collet <remi@fedoraproject.org> - 2.8.0-1
- update to 2.8.0

* Tue Feb 23 2016 Remi Collet <remi@fedoraproject.org> - 2.7.0-1
- update to 2.7.0
- raise dependency on zend-inputfilter >= 2.6
- raise dependency on zend-hydrator >= 1.1

* Thu Jan 28 2016 Remi Collet <remi@fedoraproject.org> - 2.6.0-1
- update to 2.6.0
- raise dependency on zend-stdlib ~2.7
- add dependency on zend-hydrator ~1.0

* Wed Sep 23 2015 Remi Collet <remi@fedoraproject.org> - 2.5.3-1
- update to 2.5.3

* Thu Sep 10 2015 Remi Collet <remi@fedoraproject.org> - 2.5.2-1
- update to 2.5.2
- raise minimum php version to 5.5

* Tue Aug  4 2015 Remi Collet <remi@fedoraproject.org> - 2.5.1-1
- initial package
