# remirepo/Fedora spec file for php-zendframework-zend-log
#
# Copyright (c) 2015-2016 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global bootstrap    0
%global gh_commit    115d75db1f8fb29efbf1b9a49cb91c662b7195dc
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     zendframework
%global gh_project   zend-log
%global php_home     %{_datadir}/php
%global library      Log
%if %{bootstrap}
%global with_tests   0%{?_with_tests:1}
%else
%global with_tests   0%{!?_without_tests:1}
%endif

Name:           php-%{gh_owner}-%{gh_project}
Version:        2.9.1
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
BuildRequires:  php-ctype
BuildRequires:  php-date
BuildRequires:  php-dom
BuildRequires:  php-json
BuildRequires:  php-pcre
BuildRequires:  php-spl
BuildRequires:  php-composer(%{gh_owner}/zend-servicemanager)   >= 2.5
BuildRequires:  php-composer(%{gh_owner}/zend-stdlib)           >= 2.5
BuildRequires:  php-composer(psr/log)                           >= 1.0
# From composer, "require-dev": {
#        "zendframework/zend-db": "^2.6",
#        "zendframework/zend-escaper": "^2.5",
#        "zendframework/zend-filter": "^2.5",
#        "zendframework/zend-mail": "^2.6.1",
#        "zendframework/zend-validator": "^2.6",
#        "friendsofphp/php-cs-fixer": "~1.7.0",
#        "phpunit/PHPUnit": "~4.0",
#        "mikey179/vfsStream": "^1.6"
BuildRequires:  php-composer(%{gh_owner}/zend-console)          >= 2.5
BuildRequires:  php-composer(%{gh_owner}/zend-db)               >= 2.6
BuildRequires:  php-composer(%{gh_owner}/zend-escaper)          >= 2.5
BuildRequires:  php-composer(%{gh_owner}/zend-filter)           >= 2.5
BuildRequires:  php-composer(%{gh_owner}/zend-mail)             >= 2.6.1
BuildRequires:  php-composer(%{gh_owner}/zend-validator)        >= 2.6
BuildRequires:  php-composer(phpunit/phpunit)                   >= 4.0
BuildRequires:  php-composer(mikey179/vfsStream)                >= 1.6
# Optional dep
BuildRequires:  php-composer(%{gh_owner}/zend-mime)             >= 2.5
# Autoloader
BuildRequires:  php-composer(%{gh_owner}/zend-loader)           >= 2.5
%endif

# From composer, "require": {
#        "php": "^5.6 || ^7.0",
#        "zendframework/zend-servicemanager": "^2.7.5 || ^3.0.3",
#        "zendframework/zend-stdlib": "^2.7 || ^3.0",
#        "psr/log": "^1.0"
Requires:       php(language) >= 5.6
%if ! %{bootstrap}
Requires:       php-composer(%{gh_owner}/zend-servicemanager)   >= 2.7.5
Requires:       php-composer(%{gh_owner}/zend-servicemanager)   <  4
Requires:       php-composer(%{gh_owner}/zend-stdlib)           >= 2.7
Requires:       php-composer(%{gh_owner}/zend-stdlib)           <  4
Requires:       php-composer(psr/log)                           >= 1.0
Requires:       php-composer(psr/log)                           <  2
# From composer, "suggest": {
#        "ext-mongo": "mongo extension to use Mongo writer",
#        "ext-mongodb": "mongodb extension to use MongoDB writer",
#        "zendframework/zend-console": "Zend\\Console component to use the RequestID log processor",
#        "zendframework/zend-db": "Zend\\Db component to use the database log writer",
#        "zendframework/zend-escaper": "Zend\\Escaper component, for use in the XML log formatter",
#        "zendframework/zend-mail": "Zend\\Mail component to use the email log writer",
#        "zendframework/zend-validator": "Zend\\Validator component to block invalid log messages"
%if 0%{?fedora} >= 21
Suggests:       php-pecl(mongo)
Suggests:       php-pecl(mongodb)
Suggests:       php-composer(%{gh_owner}/zend-console)
Suggests:       php-composer(%{gh_owner}/zend-db)
Suggests:       php-composer(%{gh_owner}/zend-escaper)
Suggests:       php-composer(%{gh_owner}/zend-mail)
Suggests:       php-composer(%{gh_owner}/zend-validator)
%endif
%endif
# From phpcompatinfo report for version 2.6.0
Requires:       php-ctype
Requires:       php-date
Requires:       php-dom
Requires:       php-json
Requires:       php-pcre
Requires:       php-spl
# mongo is optional

Obsoletes:      php-ZendFramework2-%{library} < 2.5
Provides:       php-ZendFramework2-%{library} = %{version}
Provides:       php-composer(%{gh_owner}/%{gh_project}) = %{version}
Provides:       php-composer(psr/log-implementation) = 1.0.0


%description
Zend\Log is a component for general purpose logging. It supports multiple
log backends, formatting messages sent to the log, and filtering messages
from being logged.

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

require __DIR__ . '/../test/Writer/TestAsset/chmod.php';
EOF

# remirepo:11
ret=0
run=0
if which php56; then
   php56 %{_bindir}/phpunit || ret=1
   run=1
fi
if which php71; then
   php71 %{_bindir}/phpunit || ret=1
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
* Fri Aug 12 2016 Remi Collet <remi@fedoraproject.org> - 2.9.1-1
- update to 2.9.1

* Thu Jun 23 2016 Remi Collet <remi@fedoraproject.org> - 2.9.0-1
- update to 2.9.0
- provide php-composer(psr/log-implementation)
- raise dependency on PHP 5.6
- suggest mongodb instead of mongo extension

* Fri May 27 2016 Remi Collet <remi@fedoraproject.org> - 2.8.3-1
- update to 2.8.3

* Tue Apr 19 2016 Remi Collet <remi@fedoraproject.org> - 2.8.2-1
- update to 2.8.2

* Thu Apr  7 2016 Remi Collet <remi@fedoraproject.org> - 2.8.1-1
- update to 2.8.1

* Fri Feb 19 2016 Remi Collet <remi@fedoraproject.org> - 2.7.1-1
- update to 2.7.1

* Fri Feb 12 2016 Remi Collet <remi@fedoraproject.org> - 2.7.0-1
- update to 2.7.0
- raise dependency on zend-stdlib >= 2.7
- raise dependency on zend-servicemanager >= 2.7.5

* Thu Jan 28 2016 Remi Collet <remi@fedoraproject.org> - 2.6.0-1
- update to 2.6.0
- add dependency on psr/log

* Tue Aug  4 2015 Remi Collet <remi@fedoraproject.org> - 2.5.2-1
- initial package
