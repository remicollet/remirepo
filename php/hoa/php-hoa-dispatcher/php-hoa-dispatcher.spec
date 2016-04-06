# remirepo/fedora spec file for php-hoa-dispatcher
#
# Copyright (c) 2016 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global bootstrap    1
%global gh_commit    a0ea27587a0a12ddcee6a00fac5ebc158a2186c3
#global gh_date      20150728
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     hoaproject
%global gh_project   Dispatcher
%global php_home     %{_datadir}/php
%global ns_vendor    Hoa
%global ns_project   Dispatcher
%global pk_vendor    hoa
%global pk_project   dispatcher
%if %{bootstrap}
%global with_tests   0%{?_with_tests:1}
%else
%global with_tests   0%{!?_without_tests:1}
%endif

Name:           php-%{pk_vendor}-%{pk_project}
Version:        1.16.01.15
%global specrel 0
Release:        %{?gh_date:0.%{specrel}.%{?prever}%{!?prever:%{gh_date}git%{gh_short}}}%{!?gh_date:%{specrel}}%{?dist}
Summary:        The %{ns_vendor}\%{ns_project} library.

Group:          Development/Libraries
License:        BSD
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{name}-%{version}-%{gh_short}.tar.gz
Source1:        %{name}-autoload.php
Source2:        http://hoa-project.net/LICENSE

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
%if %{with_tests}
BuildRequires:  php-composer(%{pk_vendor}/consistency)     >= 1.0
BuildRequires:  php-composer(%{pk_vendor}/exception)       >= 1.0
BuildRequires:  php-composer(%{pk_vendor}/zformat)         >= 1.0
# From composer.json, "require-dev": {
#        "hoa/router": "~3.0",
#        "hoa/test"  : "~2.0",
#        "hoa/view"  : "~3.0"
BuildRequires:  php-composer(%{pk_vendor}/router)          >= 3.0
BuildRequires:  php-composer(%{pk_vendor}/test)            >= 2.0
BuildRequires:  php-composer(%{pk_vendor}/view)            >= 3.0
%endif

# from composer.json, "require": {
#        "hoa/consistency": "~1.0",
#        "hoa/exception"  : "~1.0",
#        "hoa/zformat"    : "~1.0"
Requires:       php-composer(%{pk_vendor}/consistency)     >= 1.0
Requires:       php-composer(%{pk_vendor}/consistency)     <  2
Requires:       php-composer(%{pk_vendor}/exception)       >= 1.0
Requires:       php-composer(%{pk_vendor}/exception)       <  2
Requires:       php-composer(%{pk_vendor}/zformat)         >= 1.0
Requires:       php-composer(%{pk_vendor}/zformat)         <  2
# from composer.json, "suggest": {
#        "hoa/router": "Provide routers.",
#        "hoa/view"  : "Provide view interface."
Suggests:       php-composer(%{pk_vendor}/router)
Suggests:       php-composer(%{pk_vendor}/view)
# from phpcompatinfo report for version 1.16.01.15
Requires:       php-reflection
Requires:       php-pcre

Provides:       php-composer(%{pk_vendor}/%{pk_project}) = %{version}


%description
The %{ns_vendor}\%{ns_project} library dispatches a task defined
by some data on a callable, or with the appropriated vocabulary,
on a controller and an action. It is often used in conjunction
with the Hoa\Router library and the Hoa\View library.

The link between libraries and the application is represented by
a kit which aggregates all important data, such as the dispatcher,
the router, the view and data associated to the view.

Autoloader: %{php_home}/%{ns_vendor}/%{ns_project}/autoload.php


%prep
%setup -q -n %{gh_project}-%{gh_commit}
cp %{SOURCE1} autoload.php
cp %{SOURCE2} LICENSE

%build
: Nothing

%install
rm -rf      %{buildroot}
mkdir -p    %{buildroot}%{php_home}/%{ns_vendor}/%{ns_project}
cp -pr *php %{buildroot}%{php_home}/%{ns_vendor}/%{ns_project}/
find . -mindepth 1 -maxdepth 1 -type d \! \( -name Test -o -name Documentation \) -print -exec \
  cp -pr {}  %{buildroot}%{php_home}/%{ns_vendor}/%{ns_project} \; \


%check
%if %{with_tests}
%else
: bootstrap build with test suite disabled
%endif


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc composer.json
%doc *md
%{php_home}/%{ns_vendor}/%{ns_project}


%changelog
* Wed Apr  6 2016 Remi Collet <remi@fedoraproject.org> - 1.16.01.15-0
- initial package
- bootstrap build

