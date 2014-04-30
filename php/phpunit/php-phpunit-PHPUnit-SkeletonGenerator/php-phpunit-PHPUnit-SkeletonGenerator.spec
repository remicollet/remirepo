# spec file for php-phpunit-PHPUnit-SkeletonGenerator
#
# Copyright (c) 2012-2014 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/3.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    8a524d3a65ebebc89ce63c937b9e5a4b305e90e1
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     sebastianbergmann
%global gh_project   phpunit-skeleton-generator
%global php_home     %{_datadir}/php
%global pear_name    PHPUnit_SkeletonGenerator
%global pear_channel pear.phpunit.de
# Circular dependency with phpunit
%global with_tests   %{?_with_tests:1}%{!?_with_tests:0}

Name:           php-phpunit-PHPUnit-SkeletonGenerator
Version:        1.2.1
Release:        4%{?dist}
Summary:        Tool that can generate skeleton test classes

Group:          Development/Libraries
License:        BSD
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php(language) >= 5.3.3

Requires:       php(language) >= 5.3.3
Requires:       php-date
Requires:       php-pcre
Requires:       php-reflection
Requires:       php-spl
Requires:       php-tokenizer
Requires:       php-phpunit-Text-Template >= 1.1.1
Requires:       php-pear(components.ez.no/ConsoleTools) >= 1.6

# For compatibility with PEAR mode
Provides:       php-pear(%{pear_channel}/%{pear_name}) = %{version}


%description
Tool that can generate skeleton test classes from production code classes
and vice versa.


%prep
%setup -q -n %{gh_project}-%{gh_commit}

rm src/autoload.php.in

# Fix loader
sed -e 's:/usr/bin/env php:%{_bindir}/php:' \
    -e 's:@php_bin@:%{php_home}:' \
    -i phpunit-skelgen.php


%build
# Empty build section, most likely nothing required.

# If upstream drop Autoload.php, command to generate it.
# Also remember to fix the command to use it.

#phpab \
#  --output   src/autoload.php \
#  --template src/autoload.php.in \
#  src


%install
rm -rf     %{buildroot}
mkdir -p   %{buildroot}%{php_home}/SebastianBergmann/PHPUnit
cp -pr src %{buildroot}%{php_home}/SebastianBergmann/PHPUnit/SkeletonGenerator

install -D -p -m 755 phpunit-skelgen.php %{buildroot}%{_bindir}/phpunit-skelgen


%clean
rm -rf %{buildroot}


%if %{with_tests}
%check
phpunit \
  --test-suffix .phpt \
  -d date.timezone=UTC \
  tests
%endif


%post
if [ -x %{_bindir}/pear ]; then
   %{_bindir}/pear uninstall --nodeps --ignore-errors --register-only \
      %{pear_channel}/%{pear_name} >/dev/null
fi


%files
%defattr(-,root,root,-)
%doc README.markdown ChangeLog.markdown LICENSE
%{_bindir}/phpunit-skelgen
%dir %{php_home}/SebastianBergmann
%dir %{php_home}/SebastianBergmann/PHPUnit
     %{php_home}/SebastianBergmann/PHPUnit/SkeletonGenerator


%changelog
* Wed Apr 30 2014 Remi Collet <remi@fedoraproject.org> - 1.2.1-4
- cleanup pear registry

* Tue Apr 29 2014 Remi Collet <remi@fedoraproject.org> - 1.2.1-3
- sources from github

* Sat Jun 01 2013 Remi Collet <remi@fedoraproject.org> - 1.2.1-1
- Update to 1.2.1
- add explicit requires

* Thu Oct 11 2012 Remi Collet <remi@fedoraproject.org> - 1.2.0-1
- Version 1.2.0 (stable) - API 1.2.0 (stable)
- raise dependency: php >= 5.3.3

* Sat Mar 03 2012 Remi Collet <remi@fedoraproject.org> - 1.1.0-1
- Version 1.1.0 (stable) - API 1.1.0 (stable)

* Sat Jan 21 2012 Remi Collet <remi@fedoraproject.org> - 1.0.0-1
- initial package
