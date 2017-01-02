# remirepo/fedora spec file for php-gecko-packages-gecko-php-unit
#
# Copyright (c) 2016-2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    40a697ec261f3526e8196363b481b24383740c13
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
#global gh_date      20150717
%global gh_owner     GeckoPackages
%global gh_project   GeckoPHPUnit
%global pk_owner     gecko-packages
%global pk_project   gecko-php-unit
%global php_home     %{_datadir}/php
%global with_tests   0%{!?_without_tests:1}

Name:           php-%{pk_owner}-%{pk_project}
Version:        2.0.0
Release:        1%{?gh_date:.%{gh_date}git%{gh_short}}%{?dist}
Summary:        Additional PHPUnit tests

Group:          Development/Tools
License:        MIT
URL:            https://github.com/%{gh_owner}/%{gh_project}
# git snapshot to get upstream test suite
Source0:        %{name}-%{version}-%{gh_short}.tgz
Source1:        makesrc.sh

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
%if %{with_tests}
# For tests
BuildRequires:  php(language) >= 5.3.6
BuildRequires:  php-ctype
BuildRequires:  php-dom
BuildRequires:  php-libxml
BuildRequires:  php-pcre
BuildRequires:  php-spl
# From composer.json,     "require-dev": {
#        "phpunit/phpunit": "4.0"
BuildRequires:  php-composer(phpunit/phpunit)
# Autoloader
BuildRequires:  php-composer(fedora/autoloader)
%endif

# From composer.json,     "require": {
#        "php": "^5.3.6 || ^7.0"
Requires:       php(language) >= 5.3.6
# From phpcompatinfo report for version 2.0.0
Requires:       php-ctype
Requires:       php-dom
Requires:       php-libxml
Requires:       php-pcre
Requires:       php-spl
# Autoloader
Requires:       php-composer(fedora/autoloader)

Provides:       php-composer(%{pk_owner}/%{pk_project}) = %{version}


%description
Provides additional asserts to be used in PHPUnit tests.
The asserts are provided using Traits so no changes are needed
in the hierarchy of test classes.

Autoloader: %{php_home}/GeckoPackages/PHPUnit/autoload.php

%prep
%setup -q -n %{gh_project}-%{gh_commit}

cat << 'EOF' | tee src/PHPUnit/autoload.php
<?php
/* Autoloader for friendsofphp/php-cs-fixer and its dependencies */

require_once '%{php_home}/Fedora/Autoloader/autoload.php';
\Fedora\Autoloader\Autoload::addPsr4('GeckoPackages\\PHPUnit\\', __DIR__);

EOF


%build
# Empty build section, most likely nothing required.


%install
rm -rf %{buildroot}

mkdir -p           %{buildroot}%{php_home}/GeckoPackages
cp -pr src/PHPUnit %{buildroot}%{php_home}/GeckoPackages/PHPUnit



%check
%if %{with_tests}
mkdir vendor
ln -s %{buildroot}%{php_home}/GeckoPackages/PHPUnit/autoload.php vendor/autoload.php

: Fix paths in unit tests
for unit in $(find tests -name \*Test.php -print); do
  sed -e 's:PHPUnit/tests:tests:' -i $unit
done

# remirepo:11
run=0
ret=0
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
%doc composer.json
%doc *.md
%dir %{php_home}/GeckoPackages
     %{php_home}/GeckoPackages/PHPUnit


%changelog
* Thu Dec  1 2016 Remi Collet <remi@fedoraproject.org> - 2.0.0-1
- initial package, version 2.0.0

