# spec file for php-sebastian-global-state
#
# Copyright (c) 2014-2016 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global bootstrap    0
%global gh_commit    bc37d50fea7d017d3d340f230811c9f1d7280af4
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     sebastianbergmann
%global gh_project   global-state
%global php_home     %{_datadir}/php/SebastianBergmann
%if %{bootstrap}
%global with_tests   %{?_with_tests:1}%{!?_with_tests:0}
%else
%global with_tests   %{?_without_tests:0}%{!?_without_tests:1}
%endif

Name:           php-sebastian-global-state
Version:        1.1.1
Release:        3%{?dist}
Summary:        Snapshotting of global state

Group:          Development/Libraries
License:        BSD
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}-%{gh_short}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php(language) >= 5.3.3
BuildRequires:  %{_bindir}/phpab
%if %{with_tests}
# from composer.json, "require-dev": {
#        "phpunit/phpunit": "~4.2"
BuildRequires:  php-composer(phpunit/phpunit) > 4.2
%endif

# from composer.json, "require": {
#        "php": ">=5.3.3"
Requires:       php(language) >= 5.3.3
# from composer.json, "suggest": {
#        "ext-uopz": "*"
%if 0%{?fedora} > 21
Suggests:       php-uopz
%endif

Provides:       php-composer(sebastian/global-state) = %{version}


%description
Snapshotting of global state,
factored out of PHPUnit into a stand-alone component.


%prep
%setup -q -n %{gh_project}-%{gh_commit}


%build
# Generate the Autoloader
phpab --output src/autoload.php src

# For the test suite
phpab --basedir tests --output tests/autoload.php tests/_fixture/


%install
rm -rf     %{buildroot}
mkdir -p   %{buildroot}%{php_home}
cp -pr src %{buildroot}%{php_home}/GlobalState


%check
%if %{with_tests}
cat <<EOF | tee bs.php
<?php
require 'SebastianBergmann/GlobalState/autoload.php';
require 'tests/autoload.php';
EOF

: Run upstream test suite
# remirepo:13
run=0
ret=0
if which php56; then
   php56 -d include_path=.:%{buildroot}%{_datadir}/php:%{_datadir}/php \
   %{_bindir}/phpunit --bootstrap bs.php tests || ret=1
   run=1
fi
if which php71; then
   php71 -d include_path=.:%{buildroot}%{_datadir}/php:%{_datadir}/php \
   %{_bindir}/phpunit --bootstrap bs.php tests || ret=1
   run=1
fi
if [ $run -eq 0 ]; then
%{_bindir}/php -d include_path=.:%{buildroot}%{_datadir}/php:%{_datadir}/php \
%{_bindir}/phpunit --bootstrap bs.php --verbose tests
# remirepo:2
fi
exit $ret

%else
: bootstrap build with test suite disabled
%endif


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc LICENSE README.md composer.json
%dir %{php_home}
%{php_home}/GlobalState


%changelog
* Thu Oct 13 2016 Remi Collet <remi@fedoraproject.org> - 1.1.1-3
- add optional dependency on uopz extension

* Mon Oct 12 2015 Remi Collet <remi@fedoraproject.org> - 1.1.1-1
- update to 1.1.1

* Fri Dec  5 2014 Remi Collet <remi@fedoraproject.org> - 1.0.0-1
- initial package
