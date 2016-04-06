# remirepo/fedora spec file for php-hoa-cli
#
# Copyright (c) 2016 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global bootstrap    1
%global gh_commit    43af0d453d85705f6711eb9c7020710a8785bcb2
#global gh_date      20150728
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     hoaproject
%global gh_project   Cli
%global php_home     %{_datadir}/php
%global ns_vendor    Hoa
%global ns_project   Cli
%global pk_vendor    hoa
%global pk_project   cli
%if %{bootstrap}
%global with_tests   0%{?_with_tests:1}
%else
%global with_tests   0%{!?_without_tests:1}
%endif

Name:           php-%{pk_vendor}-%{pk_project}
Version:        2.16.03.15
%global specrel 0
Release:        %{?gh_date:0.%{specrel}.%{?prever}%{!?prever:%{gh_date}git%{gh_short}}}%{!?gh_date:%{specrel}}%{?dist}
Summary:        The %{ns_vendor}\%{ns_project} library.

Group:          Development/Libraries
License:        BSD
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{name}-%{version}-%{gh_short}.tar.gz
Source1:        %{name}-autoload.php
Source2:        http://hoa-project.net/LICENSE

# Use our autoloader
Patch0:         %{name}-rpm.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
%if %{with_tests}
BuildRequires:  php-composer(%{pk_vendor}/consistency)     >= 1.0
BuildRequires:  php-composer(%{pk_vendor}/console)         >= 3.0
BuildRequires:  php-composer(%{pk_vendor}/dispatcher)      >= 1.0
BuildRequires:  php-composer(%{pk_vendor}/exception)       >= 1.0
BuildRequires:  php-composer(%{pk_vendor}/protocol)        >= 1.0
BuildRequires:  php-composer(%{pk_vendor}/router)          >= 3.0
%endif

# from composer.json, "require": {
#        "hoa/consistency": "~1.0",
#        "hoa/console"    : "~3.0",
#        "hoa/dispatcher" : "~1.0",
#        "hoa/exception"  : "~1.0",
#        "hoa/protocol"   : "~1.0",
#        "hoa/router"     : "~3.0"
Requires:       php-composer(%{pk_vendor}/consistency)     >= 1.0
Requires:       php-composer(%{pk_vendor}/consistency)     <  2
Requires:       php-composer(%{pk_vendor}/console)         >= 3.0
Requires:       php-composer(%{pk_vendor}/console)         <  4
Requires:       php-composer(%{pk_vendor}/dispatcher)      >= 1.0
Requires:       php-composer(%{pk_vendor}/dispatcher)      <  2
Requires:       php-composer(%{pk_vendor}/exception)       >= 1.0
Requires:       php-composer(%{pk_vendor}/exception)       <  2
Requires:       php-composer(%{pk_vendor}/protocol)        >= 1.0
Requires:       php-composer(%{pk_vendor}/protocol)        <  2
Requires:       php-composer(%{pk_vendor}/router)          >= 3.0
Requires:       php-composer(%{pk_vendor}/router)          <  4
# from phpcompatinfo report for version 2.16.03.15
Requires:       php-cli
Requires:       php-mbstring
Requires:       php-spl

Provides:       php-composer(%{pk_vendor}/%{pk_project}) = %{version}


%description
The %{ns_vendor}\%{ns_project} meta-library provides the hoa
command line. This is a shell tool to access libraries' commands.

Autoloader: %{php_home}/%{ns_vendor}/%{ns_project}/autoload.php


%prep
%setup -q -n %{gh_project}-%{gh_commit}
cp %{SOURCE1} autoload.php
cp %{SOURCE2} LICENSE

%patch0 -p1 -b .rpm


%build
: Nothing

%install
rm -rf          %{buildroot}
mkdir -p        %{buildroot}%{php_home}/%{ns_vendor}/%{ns_project}/Bin
cp -pr *php     %{buildroot}%{php_home}/%{ns_vendor}/%{ns_project}/
cp -pr Bin/*php %{buildroot}%{php_home}/%{ns_vendor}/%{ns_project}/Bin/

install -Dpm 0755 Bin/hoa %{buildroot}%{_bindir}/hoa


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
%{_bindir}/hoa
%{php_home}/%{ns_vendor}/%{ns_project}


%changelog
* Wed Apr  6 2016 Remi Collet <remi@fedoraproject.org> - 2.16.03.15-0
- initial package
- bootstrap build

