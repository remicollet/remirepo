# remirepo/fedora spec file for php-sebastian-resource-operations
#
# Copyright (c) 2015-2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global bootstrap    0
%global gh_commit    ce990bb21759f94aeafd30209e8cfcdfa8bc3f52
#global gh_date      20150728
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     sebastianbergmann
%global gh_project   resource-operations
%global php_home     %{_datadir}/php
%global ns_vendor    SebastianBergmann
%global ns_project   ResourceOperations
%if %{bootstrap}
%global with_tests   0%{?_with_tests:1}
%else
%global with_tests   0%{!?_without_tests:1}
%endif

Name:           php-sebastian-resource-operations
Version:        1.0.0
%global specrel 2
Release:        %{?gh_date:0.%{specrel}.%{?prever}%{!?prever:%{gh_date}git%{gh_short}}}%{!?gh_date:%{specrel}}%{?dist}
Summary:        Provides a list of PHP built-in functions that operate on resources

Group:          Development/Libraries
License:        BSD
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}-%{gh_short}.tar.gz

# https://github.com/sebastianbergmann/resource-operations/pull/2
Source1:        https://raw.githubusercontent.com/remicollet/resource-operations/issue-tests/tests/ResourceOperationsTest.php

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php(language) >= 5.6
BuildRequires:  php-fedora-autoloader-devel
%if %{with_tests}
BuildRequires:  %{_bindir}/phpunit
%endif

# from composer.json
#        "php": ">=5.6.0"
Requires:       php(language) >= 5.6
# Autoloader
Requires:       php-composer(fedora/autoloader)
# from phpcompatinfo report for version 1.0.0: nothing

Provides:       php-composer(sebastian/resource-operations) = %{version}


%description
%{summary}.


%prep
%setup -q -n %{gh_project}-%{gh_commit}

mkdir tests
cp %{SOURCE1} tests/


%build
# Generate the Autoloader
phpab --template fedora --output src/autoload.php src


%install
rm -rf     %{buildroot}
mkdir -p   %{buildroot}%{php_home}/%{ns_vendor}
cp -pr src %{buildroot}%{php_home}/%{ns_vendor}/%{ns_project}


%check
%if %{with_tests}
: Run upstream test suite
# remirepo:13
run=0
ret=0
if which php56; then
  php56 -d include_path=.:%{buildroot}%{_datadir}/php:%{_datadir}/php \
  %{_bindir}/phpunit --bootstrap %{buildroot}%{php_home}/%{ns_vendor}/%{ns_project}/autoload.php tests || ret=1
   run=1
fi
if which php71; then
  php71 -d include_path=.:%{buildroot}%{_datadir}/php:%{_datadir}/php \
  %{_bindir}/phpunit --bootstrap %{buildroot}%{php_home}/%{ns_vendor}/%{ns_project}/autoload.php tests || ret=1
   run=1
fi
if [ $run -eq 0 ]; then
%{_bindir}/php -d include_path=.:%{buildroot}%{_datadir}/php:%{_datadir}/php \
%{_bindir}/phpunit --bootstrap %{buildroot}%{php_home}/%{ns_vendor}/%{ns_project}/autoload.php tests --verbose
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
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc README.md composer.json
%dir %{php_home}/%{ns_vendor}
     %{php_home}/%{ns_vendor}/%{ns_project}


%changelog
* Mon Oct 31 2016 Remi Collet <remi@fedoraproject.org> - 1.0.0-2
- switch to fedora/autoloader

* Fri Oct  2 2015 Remi Collet <remi@fedoraproject.org> - 1.0.0-1
- Update to 1.0.0 (no change)

* Tue Sep 29 2015 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.1.20150728gitce990bb
- initial package
