# remirepo/Fedora spec file for php-aura-di
#
# Copyright (c) 2015-2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global bootstrap    0
%global gh_commit    76824bdeae99e46e6ae06f29e4bdf86063da86b9
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     auraphp
%global gh_project   Aura.Di
%global pk_owner     aura
%global pk_project   di
%global ns_owner     Aura
%global ns_project   Di
%global php_home     %{_datadir}/php
%global with_tests   0%{!?_without_tests:1}

Name:           php-%{pk_owner}-%{pk_project}
Version:        3.2.0
Release:        1%{?dist}
Summary:        A serializable dependency injection container

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
BuildRequires:  php-composer(container-interop/container-interop) >= 1.0
BuildRequires:  php-reflection
BuildRequires:  php-spl
BuildRequires:  php-composer(phpunit/phpunit)
# From composer.json, "require-dev": {
#        "mouf/picotainer": "~1.0",
#        "acclimate/container": "~1.0"
%endif

# From composer, "require": {
#        "php": ">=5.5.0"
#        "container-interop/container-interop": "~1.0"
Requires:       php(language) >= 5.5.0
Requires:       php-composer(container-interop/container-interop) >= 1.0
Requires:       php-composer(container-interop/container-interop) <  2
# From phpcompatinfo report for version 3.2.0
Requires:       php-reflection
Requires:       php-spl
# Autoloader
Requires:       php-composer(fedora/autoloader)

Provides:       php-composer(%{pk_owner}/%{pk_project}) = %{version}
Provides:       php-composer(container-interop/container-interop-implementation) = 1.0


%description
A serializable dependency injection container with constructor and setter
injection, interface and trait awareness, configuration inheritance, and
much more.

Autoloader: %{php_home}/%{ns_owner}/%{ns_project}/autoload.php


%prep
%setup -q -n %{gh_project}-%{gh_commit}


%build
cat << 'EOF' | tee -a src/autoload.php
<?php
/* Autoloader for %{pk_owner}/%{pk_project} and its dependencies */

require_once '%{_datadir}/php/Fedora/Autoloader/autoload.php';
\Fedora\Autoloader\Autoload::addPsr4('Aura\\Di\\', __DIR__);
\Fedora\Autoloader\Dependencies::required(array(
    '%{php_home}/Interop/Container/autoload.php',
));
EOF


%install
rm -rf %{buildroot}

mkdir -p   %{buildroot}%{php_home}/%{ns_owner}
cp -pr src %{buildroot}%{php_home}/%{ns_owner}/%{ns_project}


%check
%if %{with_tests}
: Ignore test using not available dependency
rm tests/ContainerTest.php

mkdir vendor
cat << 'EOF' | tee -a vendor/autoload.php
<?php
require '%{buildroot}/%{php_home}/%{ns_owner}/%{ns_project}/autoload.php';
\Fedora\Autoloader\Autoload::addPsr4('Aura\\Di\\', dirname(__DIR__) . '/tests');
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
* Thu Dec 15 2016 Remi Collet <remi@fedoraproject.org> - 3.2.0-1
- update to 3.2.0
- License is now MIT
- update package Summary and Description
- raise dependency on PHP 5.5
- add dependency on container-interop/container-interop
- provide container-interop/container-interop-implementation
- switch to fedora/autoloader

* Fri Jul  1 2016 Remi Collet <remi@fedoraproject.org> - 2.2.4-1
- initial package

