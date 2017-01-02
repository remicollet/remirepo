# remirepo/fedora spec file for php-sebastian-object-enumerator
#
# Copyright (c) 2015-2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global bootstrap    0
%global gh_commit    96f8a3f257b69e8128ad74d3a7fd464bcbaa3b35
#global gh_date      20150728
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     sebastianbergmann
%global gh_project   object-enumerator
%global php_home     %{_datadir}/php
%global ns_vendor    SebastianBergmann
%global ns_project   ObjectEnumerator
%if %{bootstrap}
%global with_tests   0%{?_with_tests:1}
%else
%global with_tests   0%{!?_without_tests:1}
%endif

Name:           php-sebastian-%{gh_project}
Version:        2.0.0
%global specrel 1
Release:        %{?gh_date:0.%{specrel}.%{?prever}%{!?prever:%{gh_date}git%{gh_short}}}%{!?gh_date:%{specrel}}%{?dist}
Summary:        Traverses array and object to enumerate all referenced objects

Group:          Development/Libraries
License:        BSD
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}-%{gh_short}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php(language) >= 5.6
BuildRequires:  php-fedora-autoloader-devel
%if %{with_tests}
BuildRequires:  php-composer(sebastian/recursion-context) >= 1.0.4
# From composer.json"require-dev": {
#        "phpunit/phpunit": "~5"
BuildRequires:  php-composer(phpunit/phpunit) >= 5
%endif

# from composer.json
#        "php": ">=5.6.0"
#        "sebastian/recursion-context": "~2.0"
Requires:       php(language) >= 5.6
Requires:       php-composer(sebastian/recursion-context) >= 2.0
Requires:       php-composer(sebastian/recursion-context) <  3
# from phpcompatinfo report for version 1.0.0:
Requires:       php-reflection
Requires:       php-spl
# Autoloader
Requires:       php-composer(fedora/autoloader)

Provides:       php-composer(sebastian/%{gh_project}) = %{version}


%description
Traverses array structures and object graphs to enumerate all
referenced objects.

Autoloader: %{php_home}/%{ns_vendor}/%{ns_project}/autoload.php


%prep
%setup -q -n %{gh_project}-%{gh_commit}


%build
# Generate the Autoloader, from composer.json "autoload": {
#        "classmap": [
#            "src/"
phpab --template fedora --output src/autoload.php src
cat << 'EOF' | tee -a src/autoload.php
// Dependencies
require_once 'SebastianBergmann/RecursionContext/autoload.php';
EOF


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
%{php_home}/%{ns_vendor}/%{ns_project}


%changelog
* Tue Nov 22 2016 Remi Collet <remi@fedoraproject.org> - 2.0.0-1
- update to 2.0.0 (no change)
- raise dependency on sebastian/recursion-context 2.0

* Wed Nov 16 2016 Remi Collet <remi@fedoraproject.org> - 1.0.1-1
- update to 1.0.1
- raise dependency on sebastian/recursion-context 1.0.4

* Mon Oct 31 2016 Remi Collet <remi@fedoraproject.org> - 1.0.0-2
- switch to fedora/autoloader

* Wed Mar 23 2016 Remi Collet <remi@fedoraproject.org> - 1.0.0-1
- initial package

