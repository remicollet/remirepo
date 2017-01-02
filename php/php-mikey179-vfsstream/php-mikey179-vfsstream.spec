# spec file for php-mikey179-vfsstream
#
# Copyright (c) 2014-2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    0247f57b2245e8ad2e689d7cee754b45fbabd592
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     mikey179
%global gh_project   vfsStream
%global with_tests   %{?_without_tests:0}%{!?_without_tests:1}

Name:           php-mikey179-vfsstream
Version:        1.6.4
Release:        1%{?dist}
Summary:        PHP stream wrapper for a virtual file system

Group:          Development/Libraries
License:        BSD
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}-%{gh_short}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php(language) >= 5.3
BuildRequires:  %{_bindir}/phpab
%if %{with_tests}
# From composer.json, "require-dev": {
#        "phpunit/phpunit": "~4.5"
BuildRequires:  php-composer(phpunit/phpunit) >= 4.5
%endif

# From composer.json, "require": {
#        "php": ">=5.3.0"
Requires:       php(language) >= 5.3
# From phpcompatifo report for 1.6.0
Requires:       php-date
Requires:       php-dom
Requires:       php-pcre
Requires:       php-posix
Requires:       php-spl
Requires:       php-xml
Requires:       php-zip

Provides:       php-composer(%{gh_owner}/%{gh_project}) = %{version}


%description
vfsStream is a PHP stream wrapper for a virtual file system that may be
helpful in unit tests to mock the real file system.

It can be used with any unit test framework, like PHPUnit or SimpleTest.

To use this library, you just have to add, in your project:
  require_once '%{_datadir}/php/org/bovigo/vfs/autoload.php';


%prep
%setup -q -n %{gh_project}-%{gh_commit}


%build
: Generate autoloader
%{_bindir}/phpab \
    --output src/main/php/org/bovigo/vfs/autoload.php \
             src/main/php/org/bovigo/vfs


%install
rm -rf                  %{buildroot}
mkdir -p                %{buildroot}%{_datadir}/php
cp -pr src/main/php/org %{buildroot}%{_datadir}/php/org


%if %{with_tests}
%check
# erratic result in mock
rm src/test/php/org/bovigo/vfs/vfsStreamWrapperLargeFileTestCase.php

# remirepo:15
run=0
ret=0
if which php56; then
   php56 %{_bindir}/phpunit \
    --bootstrap %{buildroot}%{_datadir}/php/org/bovigo/vfs/autoload.php \
    --verbose || ret=1
   run=1
fi
if which php71; then
   php71 %{_bindir}/phpunit \
     --bootstrap %{buildroot}%{_datadir}/php/org/bovigo/vfs/autoload.php \
     --verbose || ret=1
   run=1
fi
if [ $run -eq 0 ]; then
: Run test suite with installed library
%{_bindir}/phpunit \
  --bootstrap %{buildroot}%{_datadir}/php/org/bovigo/vfs/autoload.php \
  --verbose
# remirepo:2
fi
exit $ret
%endif


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc CHANGELOG.md README.md composer.json

%dir %{_datadir}/php/org
%dir %{_datadir}/php/org/bovigo
     %{_datadir}/php/org/bovigo/vfs


%changelog
* Mon Jul 18 2016 Remi Collet <remi@fedoraproject.org> - 1.6.4-1
- update to 1.6.4

* Wed Apr 13 2016 Remi Collet <remi@fedoraproject.org> - 1.6.3-1
- update to 1.6.3

* Wed Jan 13 2016 Remi Collet <remi@fedoraproject.org> - 1.6.2-1
- update to 1.6.2

* Fri Dec  4 2015 Remi Collet <remi@fedoraproject.org> - 1.6.1-1
- update to 1.6.1

* Wed Oct  7 2015 Remi Collet <remi@fedoraproject.org> - 1.6.0-1
- update to 1.6.0
- add generated autoloader

* Sun Mar 29 2015 Remi Collet <remi@fedoraproject.org> - 1.5.0-1
- update to 1.5.0
- create source from git snapshot for test suite
  see https://github.com/mikey179/vfsStream/issues/108

* Sun Sep 14 2014 Remi Collet <remi@fedoraproject.org> - 1.4.0-1
- update to 1.4.0

* Tue Jul 22 2014 Remi Collet <remi@fedoraproject.org> - 1.3.0-1
- update to 1.3.0
- fix license handling

* Fri Jun  6 2014 Remi Collet <remi@fedoraproject.org> - 1.2.0-2
- provides php-composer(mikey179/vfsstream)

* Tue May 13 2014 Remi Collet <remi@fedoraproject.org> - 1.2.0-1
- initial package
