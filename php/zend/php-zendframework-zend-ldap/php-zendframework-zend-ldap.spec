# remirepo/Fedora spec file for php-zendframework-zend-ldap
#
# Copyright (c) 2015-2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global bootstrap    0
%global gh_commit    a9284a7440e17ce0ba697670bb4db1baf2340acd
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     zendframework
%global gh_project   zend-ldap
%global php_home     %{_datadir}/php
%global library      Ldap
%if %{bootstrap}
%global with_tests   0%{?_with_tests:1}
%else
%global with_tests   0%{!?_without_tests:1}
%endif

Name:           php-%{gh_owner}-%{gh_project}
Version:        2.8.0
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
BuildRequires:  php(language) >= 5.5
BuildRequires:  php-ldap
BuildRequires:  php-date
BuildRequires:  php-iconv
BuildRequires:  php-json
BuildRequires:  php-mbstring
BuildRequires:  php-pcre
BuildRequires:  php-spl
BuildRequires:  php-composer(%{gh_owner}/zend-stdlib)           >= 2.5
# From composer, "require-dev": {
#        "zendframework/zend-config": "^2.5",
#        "zendframework/zend-eventmanager": "^2.6.3 || ^3.0.1",
#        "zendframework/zend-stdlib": "^2.7 || ^3.0",
#        "phpunit/PHPUnit": "^4.5",
#        "php-mock/php-mock-phpunit": "~0.3",
#        "zendframework/zend-coding-standard": "~1.0.0",
#        "phpunit/phpunit": "^4.6"
BuildRequires:  php-composer(%{gh_owner}/zend-config)           >= 2.5
BuildRequires:  php-composer(%{gh_owner}/zend-eventmanager)     >= 2.6.3
BuildRequires:  php-composer(%{gh_owner}/zend-stdlib)           >= 2.7
BuildRequires:  php-composer(php-mock/php-mock-phpunit)         >= 0.3
BuildRequires:  php-composer(phpunit/phpunit)                   >= 4.6
# Autoloader
BuildRequires:  php-composer(%{gh_owner}/zend-loader)           >= 2.5
%endif

# From composer, "require": {
#        "php": "^5.5 || ^7.0",
#        "ext-ldap": "*"
Requires:       php(language) >= 5.5
Requires:       php-ldap
%if ! %{bootstrap}
# From composer, "suggest": {
#        "zendframework/zend-config": "^2.5",
#        "zendframework/zend-eventmanager": "^2.6.3 || ^3.0.1",
#        "zendframework/zend-stdlib": "^2.7 || ^3.0",
%if 0%{?fedora} >= 21
Suggests:       php-composer(%{gh_owner}/zend-config)           >= 2.5
Suggests:       php-composer(%{gh_owner}/zend-eventmanager)     >= 2.6.3
Suggests:       php-composer(%{gh_owner}/zend-stdlib)           >= 2.7
%endif
%endif
# From phpcompatinfo report for version 2.5.2
Requires:       php-date
Requires:       php-iconv
Requires:       php-json
Requires:       php-mbstring
Requires:       php-pcre
Requires:       php-spl

Obsoletes:      php-ZendFramework2-%{library} < 2.5
Provides:       php-ZendFramework2-%{library} = %{version}
Provides:       php-composer(%{gh_owner}/%{gh_project}) = %{version}


%description
Zend\Ldap\Ldap is a class for performing LDAP operations including but
not limited to binding, searching and modifying entries in an LDAP directory.

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

%{_bindir}/phpunit --include-path=%{buildroot}%{php_home}

if which php70; then
   php70 %{_bindir}/phpunit --include-path=%{buildroot}%{php_home}
fi
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
* Tue Mar  7 2017 Remi Collet <remi@remirepo.net> - 2.8.0-1
- Update to 2.8.0

* Wed May 25 2016 Remi Collet <remi@fedoraproject.org> - 2.7.1-1
- update to 2.7.1

* Fri Apr 22 2016 Remi Collet <remi@fedoraproject.org> - 2.7.0-1
- update to 2.7.0
- dependency on zend-stdlib is now optional

* Thu Apr 21 2016 Remi Collet <remi@fedoraproject.org> - 2.6.1-1
- update to 2.6.1

* Fri Feb 12 2016 Remi Collet <remi@fedoraproject.org> - 2.6.0-2
- add build dependency on php-mock-phpunit

* Fri Feb 12 2016 Remi Collet <remi@fedoraproject.org> - 2.6.0-1
- update to 2.6.0

* Tue Aug  4 2015 Remi Collet <remi@fedoraproject.org> - 2.5.1-1
- initial package
