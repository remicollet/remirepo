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
Release:        1%{?dist}
Summary:        Zend Framework %{library} component

Group:          Development/Libraries
License:        BSD
URL:            https://framework.zend.com/
Source0:        %{gh_commit}/%{name}-%{version}-%{gh_short}.tgz
Source1:        makesrc.sh
Source2:        %{name}-autoload.php

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

mv LICENSE.md LICENSE


%build
# Empty build section, nothing required


%install
rm -rf %{buildroot}

mkdir -p   %{buildroot}%{php_home}/%{namespace}
cp -pr src %{buildroot}%{php_home}/%{namespace}/%{library}

install -pm 644 %{SOURCE2}  %{buildroot}%{php_home}/%{namespace}/%{library}/autoload.php


%check
%if %{with_tests}
mkdir vendor
cat << EOF | tee vendor/autoload.php
<?php
require_once '%{buildroot}%{php_home}/%{namespace}/%{library}/autoload.php';
EOF
# remirepo:11
run=0
ret=0
if which php56; then
   php56 %{_bindir}/phpunit || ret=1
   run=1
fi
if which php71; then
   php70 %{_bindir}/phpunit6 || ret=1
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
%dir %{php_home}/%{namespace}
     %{php_home}/%{namespace}/%{library}


%changelog
* Mon Feb 20 2017 Remi Collet <remi@fedoraproject.org> - 3.0.0-1
- update to 3.0.0

* Thu Aug  6 2015 Remi Collet <remi@fedoraproject.org> - 2.0.1-1
- initial package
