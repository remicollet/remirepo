# remirepo/Fedora spec file for php-aura-router
# Copyright (c) 2015-2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global bootstrap    0
%global gh_commit    52507bc813c92511dbcacc7463f163ef5149ad38
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     auraphp
%global gh_project   Aura.Router
%global pk_owner     aura
%global pk_project   router
%global ns_owner     Aura
%global ns_project   Router
%global php_home     %{_datadir}/php
%global with_tests   0%{!?_without_tests:1}

Name:           php-%{pk_owner}-%{pk_project}
Version:        3.1.0
Release:        1%{?dist}
Summary:        Powerful, flexible web routing for PSR-7 requests

Group:          Development/Libraries
License:        MIT
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}-%{gh_short}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch:      noarch
BuildRequires:  php-composer(fedora/autoloader)
# Tests
%if %{with_tests}
BuildRequires:  php(language) >= 5.5.0
BuildRequires:  php-composer(psr/http-message) >= 1.0
BuildRequires:  php-composer(psr/log) >= 1.0
BuildRequires:  php-pcre
BuildRequires:  php-spl
# From composer.json, "require-dev": {
#        "zendframework/zend-diactoros": "~1.0",
#        "phpunit/phpunit": "~5.7 || ~4.8"
BuildRequires:  php-composer(zendframework/zend-diactoros) >= 1.0
BuildRequires:  php-composer(phpunit/phpunit) >= 4.8
%endif

# From composer, "require": {
#        "php": ">=5.5.0",
#        "psr/http-message": "~1.0",
#        "psr/log": "~1.0"
Requires:       php(language) >= 5.5.0
Requires:       php-composer(psr/http-message) >= 1.0
Requires:       php-composer(psr/http-message) <  2
Requires:       php-composer(psr/log) >= 1.0
Requires:       php-composer(psr/log) <  2
# From phpcompatinfo report for version 2.3.0
Requires:       php-pcre
Requires:       php-spl
# Autoloader
Requires:       php-composer(fedora/autoloader)

Provides:       php-composer(%{pk_owner}/%{pk_project}) = %{version}


%description
Powerful, flexible web routing for PSR-7 requests.

Autoloader: %{php_home}/%{ns_owner}/%{ns_project}/autoload.php


%prep
%setup -q -n %{gh_project}-%{gh_commit}


%build
cat << 'EOF' | tee -a src/autoload.php
<?php
/* Autoloader for %{pk_owner}/%{pk_project} and its dependencies */

require_once '%{_datadir}/php/Fedora/Autoloader/autoload.php';
\Fedora\Autoloader\Autoload::addPsr4('Aura\\Router\\', __DIR__);
\Fedora\Autoloader\Dependencies::required(array(
    '%{php_home}/Psr/Http/Message/autoload.php',
    '%{php_home}/Psr/Log/autoload.php',
));
EOF


%install
rm -rf %{buildroot}

mkdir -p   %{buildroot}%{php_home}/%{ns_owner}
cp -pr src %{buildroot}%{php_home}/%{ns_owner}/%{ns_project}


%check
%if %{with_tests}
mkdir vendor
cat << 'EOF' | tee -a vendor/autoload.php
<?php
require '%{buildroot}/%{php_home}/%{ns_owner}/%{ns_project}/autoload.php';
require '%{php_home}/Zend/Diactoros/autoload.php';
\Fedora\Autoloader\Autoload::addPsr4('Aura\\Router\\', dirname(__DIR__) . '/tests');
EOF

# remirepo:11
run=0
ret=0
if which php56; then
   php56 %{_bindir}/phpunit --verbose || ret=1
   run=1
fi
if which php71; then
   php71 %{_bindir}/phpunit --verbose || ret=1
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
%dir %{php_home}/%{ns_owner}/
     %{php_home}/%{ns_owner}/%{ns_project}/


%changelog
* Thu Mar  2 2017 Remi Collet <remi@remirepo.net> - 3.1.0-1
- Update to 3.1.0

* Thu Dec 15 2016 Remi Collet <remi@fedoraproject.org> - 3.0.1-1
- update to 3.0.0
- License is now MIT
- update package Summary and Description
- raise dependency on PHP 5.5
- add dependency on psr/http-message and psr/log
- switch to fedora/autoloader

* Fri Jul  1 2016 Remi Collet <remi@fedoraproject.org> - 2.3.0-1
- initial package

