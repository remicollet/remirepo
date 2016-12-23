# remirepo/Fedora spec file for php-zendframework-zend-feed
#
# Copyright (c) 2015-2016 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global bootstrap    0
%global gh_commit    12b328d382aa5200f1de53d4147033b885776b67
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     zendframework
%global gh_project   zend-feed
%global php_home     %{_datadir}/php
%global library      Feed
%if %{bootstrap}
%global with_tests   0%{?_with_tests:1}
%else
%global with_tests   0%{!?_without_tests:1}
%endif

Name:           php-%{gh_owner}-%{gh_project}
Version:        2.7.0
Release:        2%{?dist}
Summary:        Zend Framework %{library} component

Group:          Development/Libraries
License:        BSD
URL:            https://zendframework.github.io/%{gh_project}/
Source0:        %{gh_commit}/%{name}-%{version}-%{gh_short}.tgz
Source1:        makesrc.sh

Patch0:         %{name}-pr35.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch:      noarch
# Tests
%if %{with_tests}
BuildRequires:  php(language) >= 5.5
BuildRequires:  php-ctype
BuildRequires:  php-date
BuildRequires:  php-dom
BuildRequires:  php-hash
BuildRequires:  php-libxml
BuildRequires:  php-pcre
BuildRequires:  php-spl
BuildRequires:  php-tidy
BuildRequires:  php-composer(%{gh_owner}/zend-escaper)          >= 2.5
BuildRequires:  php-composer(%{gh_owner}/zend-stdlib)           >= 2.5
# From composer, "require-dev": {
#        "zendframework/zend-db": "^2.5",
#        "zendframework/zend-cache": "^2.5",
#        "zendframework/zend-http": "^2.5",
#        "zendframework/zend-servicemanager": "^2.7.5 || ^3.0.3",
#        "zendframework/zend-validator": "^2.5",
#        "fabpot/php-cs-fixer": "1.7.*",
#        "phpunit/PHPUnit": "~4.0",
#        "psr/http-message": "^1.0"
BuildRequires:  php-composer(%{gh_owner}/zend-db)               >= 2.5
BuildRequires:  php-composer(%{gh_owner}/zend-cache)            >= 2.5
BuildRequires:  php-composer(%{gh_owner}/zend-http)             >= 2.5
BuildRequires:  php-composer(%{gh_owner}/zend-servicemanager)   >= 2.7.5
BuildRequires:  php-composer(%{gh_owner}/zend-validator)        >= 2.5
BuildRequires:  php-composer(phpunit/phpunit)                   >= 4.0
BuildRequires:  php-composer(psr/http-message)                  >= 1.0
# Because of boostraped Db
BuildRequires:  php-composer(%{gh_owner}/zend-eventmanager)   >= 2.5
# Autoloader
BuildRequires:  php-composer(%{gh_owner}/zend-loader)           >= 2.5
%endif

# From composer, "require": {
#        "php": "^5.5 || ^7.0",
#        "zendframework/zend-escaper": "^2.5",
#        "zendframework/zend-stdlib": "^2.7 || ^3.0"
Requires:       php(language) >= 5.5
%if ! %{bootstrap}
Requires:       php-composer(%{gh_owner}/zend-escaper)          >= 2.5
Requires:       php-composer(%{gh_owner}/zend-escaper)          <  3
Requires:       php-composer(%{gh_owner}/zend-stdlib)           >= 2.7
Requires:       php-composer(%{gh_owner}/zend-stdlib)           <  4
# From composer, "suggest": {
#        "psr/http-message": "PSR-7 ^1.0, if you wish to use Zend\\Feed\\Reader\\Http\\Psr7ResponseDecorator",
#        "zendframework/zend-cache": "Zend\\Cache component, for optionally caching feeds between requests",
#        "zendframework/zend-db": "Zend\\Db component, for use with PubSubHubbub",
#        "zendframework/zend-http": "Zend\\Http for PubSubHubbub, and optionally for use with Zend\\Feed\\Reader",
#        "zendframework/zend-servicemanager": "Zend\\ServiceManager component, for easily extending ExtensionManager implementations",
#        "zendframework/zend-validator": "Zend\\Validator component, for validating feeds and Atom entries in the Writer subcomponent"
%if 0%{?fedora} >= 21
Suggests:       php-composer(psr/http-message)
Suggests:       php-composer(%{gh_owner}/zend-cache)
Suggests:       php-composer(%{gh_owner}/zend-db)
Suggests:       php-composer(%{gh_owner}/zend-http)
Suggests:       php-composer(%{gh_owner}/zend-servicemanager)
Suggests:       php-composer(%{gh_owner}/zend-validator)
%endif
%endif
# From phpcompatinfo report for version 2.6.0
Requires:       php-ctype
Requires:       php-date
Requires:       php-dom
Requires:       php-hash
Requires:       php-libxml
Requires:       php-pcre
Requires:       php-spl
Requires:       php-tidy

Obsoletes:      php-ZendFramework2-%{library} < 2.5
Provides:       php-ZendFramework2-%{library} = %{version}
Provides:       php-composer(%{gh_owner}/%{gh_project}) = %{version}


%description
Zend\Feed provides functionality for consuming RSS and Atom feeds.
It provides a natural syntax for accessing elements of feeds, feed attributes,
and entry attributes. Zend\Feed also has extensive support for modifying feed
and entry structure with the same natural syntax, and turning the result back
into XML.

Documentation: https://zendframework.github.io/%{gh_project}/


%prep
%setup -q -n %{gh_project}-%{gh_commit}
%patch0 -p1

mv LICENSE.md LICENSE

# NOTICE: psr/http-message is PSR-0 compliant
# autoload will be managed by fallback_autoloader


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
%if 0%{?rhel} == 5
# sqlite is too old
rm test/PubSubHubbub/Model/SubscriptionTest.php
%endif

# remirepo:11
run=0
ret=0
if which php56; then
   php56 %{_bindir}/phpunit || ret=1
   run=1
fi
if which php71; then
   php70 %{_bindir}/phpunit || ret=1
   run=1
fi
if [ $run -eq 0 ]; then
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
* Tue Nov 15 2016 Remi Collet <remi@fedoraproject.org> - 2.7.0-2
- add path for PHP 7.1
  open https://github.com/zendframework/zend-feed/pull/35

* Fri Feb 12 2016 Remi Collet <remi@fedoraproject.org> - 2.7.0-1
- update to 2.7.0
- raise dependency on zend-stdlib >= 2.7

* Thu Jan 28 2016 Remi Collet <remi@fedoraproject.org> - 2.6.0-1
- update to 2.6.0
- raise minimal php version to 5.5
- drop build dependency on zend-servicemanager
- add optional dependency on psr/http-message

* Tue Aug  4 2015 Remi Collet <remi@fedoraproject.org> - 2.5.2-1
- initial package
