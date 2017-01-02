# remirepo/Fedora spec file for php-zendframework-zend-test
#
# Copyright (c) 2015-2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global bootstrap    0
%global gh_commit    f1ee9ae3f69446f19f4015826b7a70d5ff2f5644
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     zendframework
%global gh_project   zend-test
%global php_home     %{_datadir}/php
%global library      Test
%if %{bootstrap}
%global with_tests   0%{?_with_tests:1}
%else
%global with_tests   0%{!?_without_tests:1}
%endif

Name:           php-%{gh_owner}-%{gh_project}
Version:        3.0.2
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
BuildRequires:  php(language) >= 5.6
BuildRequires:  php-composer(phpunit/phpunit)                   >= 4.0
BuildRequires:  php-pcre
BuildRequires:  php-composer(%{gh_owner}/zend-console)          >= 2.6
BuildRequires:  php-composer(%{gh_owner}/zend-dom)              >= 2.6
BuildRequires:  php-composer(%{gh_owner}/zend-eventmanager)     >= 2.6.2
BuildRequires:  php-composer(%{gh_owner}/zend-http)             >= 2.5.4
BuildRequires:  php-composer(%{gh_owner}/zend-mvc)              >= 3.0
BuildRequires:  php-composer(%{gh_owner}/zend-servicemanager)   >= 2.7.5
BuildRequires:  php-composer(%{gh_owner}/zend-stdlib)           >= 2.7
BuildRequires:  php-composer(%{gh_owner}/zend-uri)              >= 2.5
BuildRequires:  php-composer(%{gh_owner}/zend-view)             >= 2.6.3
# From composer, "require-dev": {
#        "fabpot/php-cs-fixer": "1.7.*",
#        "mikey179/vfsStream": "~1.2",
#        "zendframework/zend-i18n": "^2.6",
#        "zendframework/zend-log": "^2.7.1",
#        "zendframework/zend-modulemanager": "^2.7.1",
#        "zendframework/zend-serializer": "^2.6.1",
#        "zendframework/zend-session": "^2.6.2",
#        "zendframework/zend-mvc-plugin-flashmessenger": "^0.1.0",
#        "zendframework/zend-mvc-console": "^1.1.8",
#        "zendframework/zend-validator": "^2.8"
BuildRequires:  php-composer(mikey179/vfsStream)                >= 1.2
BuildRequires:  php-composer(%{gh_owner}/zend-i18n)             >= 2.6
BuildRequires:  php-composer(%{gh_owner}/zend-log)              >= 2.7.1
BuildRequires:  php-composer(%{gh_owner}/zend-modulemanager)    >= 2.7.1
BuildRequires:  php-composer(%{gh_owner}/zend-serializer)       >= 2.6.1
BuildRequires:  php-composer(%{gh_owner}/zend-session)          >= 2.6.2
BuildRequires:  php-composer(%{gh_owner}/zend-mvc-plugin-flashmessenger) >= 0.1.0
BuildRequires:  php-composer(%{gh_owner}/zend-mvc-console)      >= 1.1.8
BuildRequires:  php-composer(%{gh_owner}/zend-validator)        >= 2.8
# Autoloader
BuildRequires:  php-composer(%{gh_owner}/zend-loader)           >= 2.5
%endif

# From composer, "require": {
#        "php": "^5.6 || ^7.0",
#        "phpunit/phpunit": "^4.0 || ^5.0",
#        "zendframework/zend-console": "^2.6",
#        "zendframework/zend-dom": "^2.6",
#        "zendframework/zend-eventmanager": "^2.6.2 || ^3.0",
#        "zendframework/zend-http": "^2.5.4",
#        "zendframework/zend-mvc": "^2.7.1",
#        "zendframework/zend-servicemanager": "^2.7.5 || ^3.0.3",
#        "zendframework/zend-stdlib": "^2.7 || ^3.0",
#        "zendframework/zend-uri": "^2.5",
#        "zendframework/zend-view": "^2.6.3",
#        "sebastian/version": "^1.0.4 || ^2.0"
Requires:       php(language) >= 5.6
Requires:       php-composer(phpunit/phpunit)                   >= 4.0
Requires:       php-composer(phpunit/phpunit)                   <  6
Requires:       php-composer(sebastian/version)                 >= 1.0.4
Requires:       php-composer(sebastian/version)                 <  3
%if ! %{bootstrap}
Requires:       php-composer(%{gh_owner}/zend-console)          >= 2.6
Requires:       php-composer(%{gh_owner}/zend-console)          <  3
Requires:       php-composer(%{gh_owner}/zend-dom)              >= 2.6
Requires:       php-composer(%{gh_owner}/zend-dom)              <  3
Requires:       php-composer(%{gh_owner}/zend-eventmanager)     >= 2.6.2
Requires:       php-composer(%{gh_owner}/zend-eventmanager)     <  4
Requires:       php-composer(%{gh_owner}/zend-http)             >= 2.5.4
Requires:       php-composer(%{gh_owner}/zend-http)             <  3
Requires:       php-composer(%{gh_owner}/zend-mvc)              >= 3.0
Requires:       php-composer(%{gh_owner}/zend-mvc)              <  4
Requires:       php-composer(%{gh_owner}/zend-servicemanager)   >= 2.7.5
Requires:       php-composer(%{gh_owner}/zend-servicemanager)   <  4
Requires:       php-composer(%{gh_owner}/zend-stdlib)           >= 2.7
Requires:       php-composer(%{gh_owner}/zend-stdlib)           <  4
Requires:       php-composer(%{gh_owner}/zend-uri)              >= 2.5
Requires:       php-composer(%{gh_owner}/zend-uri)              <  3
Requires:       php-composer(%{gh_owner}/zend-view)             >= 2.6.3
Requires:       php-composer(%{gh_owner}/zend-view)             <  3
%endif
# From phpcompatinfo report for version 2.5.1
Requires:       php-pcre

Obsoletes:      php-ZendFramework2-%{library} < 2.5
Provides:       php-ZendFramework2-%{library} = %{version}
Provides:       php-composer(%{gh_owner}/%{gh_project}) = %{version}


%description
The Zend\Test component provides tools to facilitate unit testing of your
Zend Framework applications. At this time, we offer facilities to enable
testing of your Zend Framework MVC applications.

PHPUnit is the only library supported currently.

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
   php71 %{_bindir}/phpunit --include-path=%{buildroot}%{php_home} || ret=1
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
* Wed Sep  7 2016 Remi Collet <remi@fedoraproject.org> - 3.0.2-1
- update to 3.0.2

* Wed Jun 29 2016 Remi Collet <remi@fedoraproject.org> - 3.0.1-1
- update to 3.0.1 for ZendFramework 3
- raise dependency on PHP 5.6
- raise dependency on zend-mvc >= 3.0

* Mon Apr 18 2016 Remi Collet <remi@fedoraproject.org> - 2.6.1-2
- allow sebastian/version 2.0

* Thu Mar  3 2016 Remi Collet <remi@fedoraproject.org> - 2.6.1-1
- update to 2.6.1
- raise dependency on zend-mvc >= 2.7.1

* Wed Mar  2 2016 Remi Collet <remi@fedoraproject.org> - 2.6.0-1
- update to 2.6.0
- raise dependency on zend-console >= 2.6
- raise dependency on zend-dom >= 2.6
- raise dependency on zend-eventmanager >= 2.6.2
- raise dependency on zend-http >= 2.5.4
- raise dependency on zend-mvc >= 2.7
- raise dependency on zend-servicemanager >= 2.7.5
- raise dependency on zend-stdlib >= 2.7
- raise dependency on zend-view >= 2.6.3
- add dependency on sebastian/version

* Wed Dec  9 2015 Remi Collet <remi@fedoraproject.org> - 2.5.2-1
- update to 2.5.2
- raise dependency on PHP >= 5.5
- allow PHPUnit 5

* Fri Oct  2 2015 Remi Collet <remi@fedoraproject.org> - 2.5.1-2
- ignore phpunit upstream recommended max version

* Tue Aug  4 2015 Remi Collet <remi@fedoraproject.org> - 2.5.1-1
- initial package
