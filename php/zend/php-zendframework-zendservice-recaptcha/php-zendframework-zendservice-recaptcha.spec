# remirepo/Fedora spec file for php-zendframework-zendservice-recaptcha
#
# Copyright (c) 2015-2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    6c6877c07c8ac73b187911ea5d264a640b234361
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     zendframework
%global gh_project   ZendService_ReCaptcha
%global pk_project   zendservice-recaptcha
%global php_home     %{_datadir}/php
%global namespace    ZendService
%global library      ReCaptcha
%global with_tests   0%{!?_without_tests:1}

Name:           php-%{gh_owner}-%{pk_project}
Version:        3.0.0
Release:        3%{?dist}
Summary:        Zend Framework %{library} component

Group:          Development/Libraries
License:        BSD
URL:            https://framework.zend.com/
Source0:        %{gh_commit}/%{name}-%{version}-%{gh_short}.tgz
Source1:        makesrc.sh

# See https://github.com/zendframework/ZendService_ReCaptcha/pull/12
Patch0:         %{name}-pr12.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch:      noarch
# Tests
%if %{with_tests}
BuildRequires:  php(language) >= 5.6
BuildRequires:  php-json
BuildRequires:  php-composer(%{gh_owner}/zend-http)             >= 2.5.4
BuildRequires:  php-composer(%{gh_owner}/zend-json)             >= 2.6.1
# From composer.json, "require-dev": {
#        "phpunit/phpunit": "^5.7 || ^6.0",
#        "zendframework/zend-coding-standard": "~1.0.0",
#        "zendframework/zend-config": "^2.0",
#        "zendframework/zend-validator": "^2.8.2"
BuildRequires:  php-composer(phpunit/phpunit)                   >= 5.7
BuildRequires:  php-composer(%{gh_owner}/zend-config)           >= 2.0
BuildRequires:  php-composer(%{gh_owner}/zend-validator)        >= 2.8.2
# Autoloader
BuildRequires:  php-composer(%{gh_owner}/zend-loader)
%endif

# From composer, "require": {
#        "php": "^5.6 || ^7.0",
#        "zendframework/zend-http": "^2.5.4",
#        "zendframework/zend-json": "^2.6.1 || ^3.0"
Requires:       php(language) >= 5.6
Requires:       php-composer(%{gh_owner}/zend-http)             >= 2.5.4
Requires:       php-composer(%{gh_owner}/zend-http)             <  3
Requires:       php-composer(%{gh_owner}/zend-json)             >= 2.6.1
Requires:       php-composer(%{gh_owner}/zend-json)             <  4
# From compsoer, "suggest": {
#        "zendframework/zend-validator": "~2.0, if using ReCaptcha's Mailhide API"
%if 0%{?fedora} >= 21
Suggests:       php-composer(%{gh_owner}/zend-validator)
%endif
# From phpcompatinfo report for version 3.0.0 (mcrypt is optional)
Requires:       php-json

Provides:       php-composer(%{gh_owner}/%{pk_project}) = %{version}


%description
%{summary}.


%prep
%setup -q -n %{gh_project}-%{gh_commit}
%patch0 -p1

mv LICENSE.md LICENSE

# Generate autoloader for this framework extension
cat << 'EOF' | tee autoload.php
<?php
Zend\Loader\AutoloaderFactory::factory(array(
    'Zend\Loader\StandardAutoloader' => array(
        'namespaces' => array(
            '%{namespace}\\%{library}' => dirname(__DIR__) . '/%{namespace}/%{library}',
))));
EOF

# Redirect to framework autoloader
ln -s ../../Zend/autoload.php src/autoload.php


%build
# Empty build section, nothing required


%install
rm -rf %{buildroot}

mkdir -p   %{buildroot}%{php_home}/%{namespace}
cp -pr src %{buildroot}%{php_home}/%{namespace}/%{library}

install -Dpm 644 autoload.php %{buildroot}%{php_home}/Zend/%{namespace}-%{library}-autoload.php


%check
%if %{with_tests}
mkdir vendor
cat << EOF | tee vendor/autoload.php
<?php
require_once '%{php_home}/Zend/autoload.php';
Zend\\Loader\\AutoloaderFactory::factory(array(
    'Zend\\Loader\\StandardAutoloader' => array(
        'namespaces' => array(
            '%{namespace}\\%{library}' => '%{buildroot}%{php_home}/%{namespace}/%{library}',
))));
EOF
# remirepo:11
run=0
ret=0
if which php56; then
   php56 %{_bindir}/phpunit  --exclude online || ret=1
   run=1
fi
if which php71; then
   php70 %{_bindir}/phpunit6 --exclude online || ret=1
   run=1
fi
if [ $run -eq 0 ]; then
%{_bindir}/phpunit --exclude online --verbose
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
%dir %{php_home}/%{namespace}
     %{php_home}/%{namespace}/%{library}
     %{php_home}/Zend/%{namespace}-%{library}-autoload.php


%changelog
* Thu Mar  2 2017 Remi Collet <remi@fedoraproject.org> - 3.0.0-3
- add patch to skip online tests, from
  https://github.com/zendframework/ZendService_ReCaptcha/pull/12

* Fri Feb 24 2017 Remi Collet <remi@fedoraproject.org> - 3.0.0-2
- rewrite autoloader as framework extension

* Mon Feb 20 2017 Remi Collet <remi@fedoraproject.org> - 3.0.0-1
- update to 3.0.0

* Thu Aug  6 2015 Remi Collet <remi@fedoraproject.org> - 2.0.1-1
- initial package
