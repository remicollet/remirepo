# remirepo/Fedora spec file for php-zendframework-zend-eventmanager
#
# Copyright (c) 2015-2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global bootstrap    0
%global gh_commit    c3bce7b7d47c54040b9ae51bc55491c72513b75d
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     zendframework
%global gh_project   zend-eventmanager
%global php_home     %{_datadir}/php
%global library      EventManager
%if %{bootstrap}
%global with_tests   0%{?_with_tests:1}
%else
%global with_tests   0%{!?_without_tests:1}
%endif

Name:           php-%{gh_owner}-%{gh_project}
Version:        3.1.0
Release:        1%{?dist}
Summary:        Trigger and listen to events within a PHP application

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
BuildRequires:  php-spl
BuildRequires:  php-composer(%{gh_owner}/zend-stdlib)      >= 2.5
# From composer, "require-dev": {
#        "phpunit/PHPUnit": "~5.6",
#        "athletic/athletic": "^0.1",
#        "zendframework/zend-stdlib": "^2.7.3 || ^3.0",
#        "container-interop/container-interop": "^1.1.0",
#        "zendframework/zend-coding-standard": "~1.0.0"
BuildRequires:  php-composer(phpunit/phpunit)              >= 5.6
BuildRequires:  php-composer(%{gh_owner}/zend-stdlib)      >= 2.7.3
BuildRequires:  php-composer(container-interop/container-interop) >= 1.1.0
# Autoloader
BuildRequires:  php-composer(%{gh_owner}/zend-loader)      >= 2.5
%endif

# From composer, "require": {
#        "php": "^5.6 || ^7.0",
Requires:       php(language) >= 5.6
%if ! %{bootstrap}
# From composer, "suggest": {
#        "container-interop/container-interop": "^1.1.0, to use the lazy listeners feature",
#        "zendframework/zend-stdlib": "^2.7.3 || ^3.0, to use the FilterChain feature"
%if 0%{?fedora} >= 21
Suggests:       php-composer(container-interop/container-interop)
Suggests:       php-composer(%{gh_owner}/zend-stdlib)
%endif
%endif
# From phpcompatinfo report for version 2.5.2
Requires:       php-spl

Obsoletes:      php-ZendFramework2-%{library} < 2.5
Provides:       php-ZendFramework2-%{library} = %{version}
Provides:       php-composer(%{gh_owner}/%{gh_project}) = %{version}


%description
The Zend\EventManager is a component designed for the following use cases:

    Implementing simple subject/observer patterns.
    Implementing Aspect-Oriented designs.
    Implementing event-driven architectures.

The basic architecture allows you to attach and detach listeners to named
events, both on a per-instance basis as well as via shared collections;
trigger events; and interrupt execution of listeners.

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
* Tue Dec 20 2016 Remi Collet <remi@fedoraproject.org> - 3.1.0-1
- update to 3.1.0
- raise dependency on PHP 5.6

* Wed Jun 29 2016 Remi Collet <remi@fedoraproject.org> - 3.0.1-1
- update to 3.0.1 for ZendFramework 3
- dependency on zend-stdlib is optional

* Fri Feb 19 2016 Remi Collet <remi@fedoraproject.org> - 2.6.3-1
- update to 2.6.3
- raise dependency on zend-stdlib >= 2.7

* Thu Jan 28 2016 Remi Collet <remi@fedoraproject.org> - 2.6.2-1
- update to 2.6.2

* Tue Aug  4 2015 Remi Collet <remi@fedoraproject.org> - 2.5.2-1
- initial package
