# remirepo/Fedora spec file for php-zendframework-zend-code
#
# Copyright (c) 2015-2016 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global bootstrap    0
%global gh_commit    c5272131d3acb0f470a2462ed088fca3b6ba61c2
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     zendframework
%global gh_project   zend-code
%global php_home     %{_datadir}/php
%global library      Code
%if %{bootstrap}
%global with_tests   0%{?_with_tests:1}
%else
%global with_tests   0%{!?_without_tests:1}
%endif

Name:           php-%{gh_owner}-%{gh_project}
Version:        3.0.4
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
BuildRequires:  php-pcre
BuildRequires:  php-reflection
BuildRequires:  php-spl
BuildRequires:  php-tokenizer
BuildRequires:  php-composer(%{gh_owner}/zend-eventmanager)     >= 2.6
# From composer, "require-dev": {
#        "ext-phar": "*",
#        "doctrine/annotations": "~1.0",
#        "zendframework/zend-stdlib": "^2.7 || ^3.0",
#        "zendframework/zend-version": "~2.5",
#        "squizlabs/php_codesniffer": "^2.5",
#        "phpunit/PHPUnit": "^4.8.21"
BuildRequires:  php-composer(doctrine/annotations)              >= 1.0
BuildRequires:  php-composer(%{gh_owner}/zend-stdlib)           >= 2.7
BuildRequires:  php-composer(phpunit/phpunit)                   >= 4.8.21
# Autoloader
BuildRequires:  php-composer(%{gh_owner}/zend-loader)           >= 2.5
%endif

# From composer, "require": {
#        "php": "^5.5 || 7.0.0 - 7.0.4 || ^7.0.6",
#        "zendframework/zend-eventmanager": "^2.6 || ^3.0""
Requires:       php(language) >= 5.5
%if ! %{bootstrap}
Requires:       php-composer(%{gh_owner}/zend-eventmanager)     >= 2.6
Requires:       php-composer(%{gh_owner}/zend-eventmanager)     <  4
# From composer, "suggest": {
#         "doctrine/annotations": "Doctrine\\Common\\Annotations >=1.0 for annotation features",
#         "zendframework/zend-stdlib": "Zend\\Stdlib component"
%if 0%{?fedora} >= 21
Suggests:       php-composer(doctrine/annotations)
Suggests:       php-composer(%{gh_owner}/zend-stdlib)
%endif
%endif
# From phpcompatinfo report for version 2.6.2
Requires:       php-pcre
Requires:       php-reflection
Requires:       php-spl
Requires:       php-tokenizer

Obsoletes:      php-ZendFramework2-%{library} < 2.5
Provides:       php-ZendFramework2-%{library} = %{version}
Provides:       php-composer(%{gh_owner}/%{gh_project}) = %{version}


%description
Zend\Code\Generator provides facilities to generate arbitrary code using
an object-oriented interface, both to create new code as well as to update
existing code. While the current implementation is limited to generating
PHP code, you can easily extend the base class in order to provide code
generation for other tasks: JavaScript, configuration files, apache vhosts,
etc.

Documentation: https://zendframework.github.io/%{gh_project}/


%prep
%setup -q -n %{gh_project}-%{gh_commit}


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
%license LICENSE.md
%doc CHANGELOG.md CONDUCT.md CONTRIBUTING.md README.md
%doc composer.json
%{php_home}/Zend/%{library}


%changelog
* Fri Jul  1 2016 Remi Collet <remi@fedoraproject.org> - 3.0.4-1
- update to 3.0.4

* Wed Jun 29 2016 Remi Collet <remi@fedoraproject.org> - 3.0.3-2
- add patch for ocramius/proxy-manager
  https://github.com/zendframework/zend-code/pull/80

* Wed Jun 29 2016 Remi Collet <remi@fedoraproject.org> - 3.0.3-1
- update to 3.0.0 for ZendFramework 3

* Thu Apr 21 2016 Remi Collet <remi@fedoraproject.org> - 2.6.3-1
- update to 2.6.3

* Thu Jan 28 2016 Remi Collet <remi@fedoraproject.org> - 2.6.2-1
- update to 2.6.2
- dependency on doctrine/annotations instrad of doctrine/common
- raise dependency on zend-stdlib ~2.7
- raise dependency on zend-eventmanager ~2.6

* Thu Nov 19 2015 Remi Collet <remi@fedoraproject.org> - 2.5.3-1
- update to 2.5.3
- run test suite with both PHP 5 and 7 when available

* Tue Aug  4 2015 Remi Collet <remi@fedoraproject.org> - 2.5.2-1
- initial package
- open https://github.com/zendframework/zend-code/pull/5
  avoid using 'vendor' path
