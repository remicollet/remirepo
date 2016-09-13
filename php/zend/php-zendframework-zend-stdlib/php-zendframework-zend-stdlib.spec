# remirepo/Fedora spec file for php-zendframework-zend-stdlib
#
# Copyright (c) 2015-2016 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global bootstrap    0
%global gh_commit    debedcfc373a293f9250cc9aa03cf121428c8e78
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     zendframework
%global gh_project   zend-stdlib
%global php_home     %{_datadir}/php
%global library      Stdlib
%if %{bootstrap}
%global with_tests   0%{?_with_tests:1}
%else
%global with_tests   0%{!?_without_tests:1}
%endif

Name:           php-%{gh_owner}-%{gh_project}
Version:        3.1.0
Release:        1%{?dist}
Summary:        Zend Framework %{library} component

Group:          Development/Libraries
License:        BSD
URL:            https://framework.zend.com/
Source0:        %{gh_commit}/%{name}-%{version}-%{gh_short}.tgz
Source1:        makesrc.sh

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch:      noarch
# Tests
%if %{with_tests}
BuildRequires:  php(language) >= 5.6
BuildRequires:  php-composer(%{gh_owner}/zend-hydrator)         >= 1.1
BuildRequires:  php-date
BuildRequires:  php-iconv
BuildRequires:  php-intl
BuildRequires:  php-mbstring
BuildRequires:  php-pcre
BuildRequires:  php-reflection
BuildRequires:  php-spl
# From composer, "require-dev": {
#        "athletic/athletic": "~0.1",
#        "fabpot/php-cs-fixer": "1.7.*",
#        "phpunit/PHPUnit": "~4.0",
#        "squizlabs/php_codesniffer": "^2.6.2"
BuildRequires:  php-composer(phpunit/phpunit)                   >= 4.0
# Autoloader
BuildRequires:  php-composer(%{gh_owner}/zend-loader)           >= 2.5
%endif

# From composer, "require": {
#        "php": "^5.6 || ^7.0",
Requires:       php(language) >= 5.6
# From phpcompatinfo report for version 2.7.4
Requires:       php-date
Requires:       php-iconv
Requires:       php-intl
Requires:       php-mbstring
Requires:       php-pcre
Requires:       php-reflection
Requires:       php-spl
# Autoloader
Requires:       php-composer(%{gh_owner}/zend-loader)           >= 2.5

Obsoletes:      php-ZendFramework2-%{library} < 2.5
Provides:       php-ZendFramework2-%{library} = %{version}
Provides:       php-composer(%{gh_owner}/%{gh_project}) = %{version}


%description
Zend\Stdlib is a set of components that implements general purpose utility
class for different scopes like:
* array utilities functions;
* hydrators;
* json serializable interfaces;
* general messaging systems;
* string wrappers;
* etc.

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

# remirepo:11
run=0
ret=0
if which php56; then
   php56 %{_bindir}/phpunit --include-path=%{buildroot}%{php_home} || ret=1
   run=1
fi
if which php71; then
   php70 %{_bindir}/phpunit --include-path=%{buildroot}%{php_home} || ret=1
   run=1
fi
if [ $run -eq 0 ]; then
%{_bindir}/phpunit --include-path=%{buildroot}%{php_home} --verbose
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
* Tue Sep 13 2016 Remi Collet <remi@fedoraproject.org> - 3.1.0-1
- update to 3.1.0
- raise dependency on PHP >= 5.6

* Wed Jun 29 2016 Remi Collet <remi@fedoraproject.org> - 3.0.1-1
- update to 3.0.1 for ZendFramework 3
- drop dependency on zend-hydrator

* Wed Apr 13 2016 Remi Collet <remi@fedoraproject.org> - 2.7.7-1
- update to 2.7.7

* Fri Feb 19 2016 Remi Collet <remi@fedoraproject.org> - 2.7.6-1
- update to 2.7.6
- raise dependency on zendframework/zend-hydrator >= 1.1

* Tue Feb 16 2016 Remi Collet <remi@fedoraproject.org> - 2.7.5-1
- update to 2.7.5

* Thu Jan 28 2016 Remi Collet <remi@fedoraproject.org> - 2.7.4-1
- update to 2.7.4
- add dependency on zendframework/zend-hydrator ^1.0.0

* Tue Aug  4 2015 Remi Collet <remi@fedoraproject.org> - 2.5.2-1
- initial package
