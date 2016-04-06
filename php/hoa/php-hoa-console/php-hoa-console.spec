# remirepo/fedora spec file for php-hoa-console
#
# Copyright (c) 2016 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global bootstrap    1
%global gh_commit    8d279675fd421abe3b16982c5a58f24d1726db3b
#global gh_date      20150728
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     hoaproject
%global gh_project   Console
%global php_home     %{_datadir}/php
%global ns_vendor    Console
%global ns_project   File
%global pk_vendor    hoa
%global pk_project   console
%if %{bootstrap}
%global with_tests   0%{?_with_tests:1}
%else
%global with_tests   0%{!?_without_tests:1}
%endif

Name:           php-%{pk_vendor}-%{pk_project}
Version:        3.16.01.14
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
BuildRequires:  php-composer(%{pk_vendor}/event)           >= 1.0
BuildRequires:  php-composer(%{pk_vendor}/exception)       >= 1.0
BuildRequires:  php-composer(%{pk_vendor}/file)            >= 1.0
BuildRequires:  php-composer(%{pk_vendor}/protocol)        >= 1.0
BuildRequires:  php-composer(%{pk_vendor}/stream)          >= 1.0
BuildRequires:  php-composer(%{pk_vendor}/ustring)         >= 4.0
# From composer.json, "require-dev": {
#        "hoa/test": "~2.0"
BuildRequires:  php-composer(%{pk_vendor}/test)            >= 2.0
%endif

# from composer.json, "require": {
#        "hoa/consistency": "~1.0",
#        "hoa/event"      : "~1.0",
#        "hoa/exception"  : "~1.0",
#        "hoa/file"       : "~1.0",
#        "hoa/protocol"   : "~1.0",
#        "hoa/stream"     : "~1.0",
#        "hoa/ustring"    : "~4.0"
Requires:       php-composer(%{pk_vendor}/consistency)     >= 1.0
Requires:       php-composer(%{pk_vendor}/consistency)     <  2
Requires:       php-composer(%{pk_vendor}/event)           >= 1.0
Requires:       php-composer(%{pk_vendor}/event)           <  2
Requires:       php-composer(%{pk_vendor}/exception)       >= 1.0
Requires:       php-composer(%{pk_vendor}/exception)       <  2
Requires:       php-composer(%{pk_vendor}/file)            >= 1.0
Requires:       php-composer(%{pk_vendor}/file)            <  2
Requires:       php-composer(%{pk_vendor}/protocol)        >= 1.0
Requires:       php-composer(%{pk_vendor}/protocol)        <  2
Requires:       php-composer(%{pk_vendor}/stream)          >= 1.0
Requires:       php-composer(%{pk_vendor}/stream)          <  2
Requires:       php-composer(%{pk_vendor}/ustring)         >= 4.0
Requires:       php-composer(%{pk_vendor}/ustring)         <  5
# from composer.json, "suggest": {
#        "hoa/dispatcher": "To use the console kit.",
#        "hoa/router"    : "To use the console kit.",
#        "ext-pcntl"     : "To enable hoa://Event/Console/Window:resize."
%if 0%{?fedora} >= 21
Suggests:       php-composer(%{pk_vendor}/dispatcher)
Suggests:       php-composer(%{pk_vendor}/router)
%endif
# from phpcompatinfo report for version 3.16.01.14
Requires:       php-cli
Requires:       php-ctype
Requires:       php-mbstring
Requires:       php-pcre
Requires:       php-spl

Provides:       php-composer(%{pk_vendor}/%{pk_project}) = %{version}


%description
The %{ns_vendor}\%{ns_project} library allows to interact easily
with a terminal: getoption, cursor, window, processus, readline etc.

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
* Wed Apr  6 2016 Remi Collet <remi@fedoraproject.org> - 3.16.01.14-0
- initial package
- bootstrap build

