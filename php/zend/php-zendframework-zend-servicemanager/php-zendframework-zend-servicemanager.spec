# remirepo/Fedora spec file for php-zendframework-zend-servicemanager
#
# Copyright (c) 2015-2016 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global bootstrap    0
%global gh_commit    f701b0d322741b0c8d8ca1288f249a49438029cd
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     zendframework
%global gh_project   zend-servicemanager
%global php_home     %{_datadir}/php
%global library      ServiceManager
%if %{bootstrap}
%global with_tests   0%{?_with_tests:1}
%else
%global with_tests   0%{!?_without_tests:1}
%endif

Name:           php-%{gh_owner}-%{gh_project}
Version:        3.1.1
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
BuildRequires:  php(language) >= 5.5
BuildRequires:  php-composer(container-interop/container-interop) >= 1.0
BuildRequires:  php-spl
# From composer, "require-dev": {
#        "phpunit/phpunit": "^4.6 || ^5.2.10",
#        "ocramius/proxy-manager": "^1.0 || ^2.0",
#        "squizlabs/php_codesniffer": "^2.5.1",
#        "phpbench/phpbench": "^0.10.0"
BuildRequires:  php-composer(phpunit/phpunit)                   >= 4.6
BuildRequires:  php-composer(ocramius/proxy-manager)            >= 1.0
# Autoloader
BuildRequires:  php-composer(%{gh_owner}/zend-loader)           >= 2.5
# For dependencies autoloader
BuildRequires:  php-zendframework-zend-loader                   >= 2.5.1-3
%endif

# From composer, "require": {
#        "php": "^5.5 || ^7.0"
#        "container-interop/container-interop": "~1.0"
Requires:       php(language) >= 5.5
Requires:       php-composer(container-interop/container-interop) >= 1.0
Requires:       php-composer(container-interop/container-interop) <  2
# From phpcompatinfo report for version 2.7.4
Requires:       php-spl
%if ! %{bootstrap}
# From composer, "suggest": {
#        "ocramius/proxy-manager": "ProxyManager 1.* to handle lazy initialization of services",
#        "zendframework/zend-stdlib": "zend-stdlib ^2.5 if you wish to use the MergeReplaceKey or MergeRemoveKey features in Config instances"
%if 0%{?fedora} >= 21
Suggests:       php-composer(ocramius/proxy-manager)
Suggests:       php-composer(%{gh_owner}/zend-stdlib)
%endif
# Autoloader
Requires:       php-composer(%{gh_owner}/zend-loader)           >= 2.5
Requires:       php-zendframework-zend-loader                   >= 2.5.1-3
%endif

Obsoletes:      php-ZendFramework2-%{library} < 2.5
Provides:       php-ZendFramework2-%{library} = %{version}
Provides:       php-composer(%{gh_owner}/%{gh_project}) = %{version}
Provides:       php-composer(container-interop/container-interop-implementation) = 1.1


%description
The Service Locator design pattern is implemented by the Zend\ServiceManager
component. The Service Locator is a service/object locator, tasked with
retrieving other objects.

Documentation: https://zendframework.github.io/%{gh_project}/


%prep
%setup -q -n %{gh_project}-%{gh_commit}

mv LICENSE.md LICENSE

: Create dependency autoloader
cat << 'EOF' | tee autoload.php
<?php
require_once '%{php_home}/Interop/Container/autoload.php';
if (file_exists('%{php_home}/ProxyManager/autoload.php')) {
	require_once '%{php_home}/ProxyManager/autoload.php';
}
EOF


%build
# Empty build section, nothing required


%install
rm -rf %{buildroot}

mkdir -p   %{buildroot}%{php_home}/Zend/
cp -pr src %{buildroot}%{php_home}/Zend/%{library}

install -m644 autoload.php %{buildroot}%{php_home}/Zend/%{library}-autoload.php


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
   php56 %{_bindir}/phpunit --include-path=%{buildroot}%{php_home} || : ignore
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
%{php_home}/Zend/%{library}-autoload.php


%changelog
* Sun Jul 17 2016 Remi Collet <remi@fedoraproject.org> - 3.1.1-1
- update to 3.1.1

* Wed Jun 29 2016 Remi Collet <remi@fedoraproject.org> - 3.1.0-1
- update to 3.1.0 for ZendFramework 3
- add dependencies autoloader

* Thu Apr 28 2016 Remi Collet <remi@fedoraproject.org> - 2.7.6-1
- update to 2.7.6

* Tue Feb  2 2016 Remi Collet <remi@fedoraproject.org> - 2.7.5-1
- update to 2.7.5

* Thu Jan 28 2016 Remi Collet <remi@fedoraproject.org> - 2.7.4-2
- update to 2.7.4
- raise minimal php version to 5.5
- add dependency on container-interop/container-interop ~1.0

* Thu Aug  6 2015 Remi Collet <remi@fedoraproject.org> - 2.5.1-2
- fix description

* Tue Aug  4 2015 Remi Collet <remi@fedoraproject.org> - 2.5.1-1
- initial package
