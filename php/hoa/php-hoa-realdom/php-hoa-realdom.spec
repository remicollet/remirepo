# remirepo/fedora spec file for php-hoa-Realdom
#
# Copyright (c) 2016 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global bootstrap    1
%global gh_commit    3bca30e793aecdcd9b14f80b7fafb2d7730bac8b
#global gh_date      20150728
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     hoaproject
%global gh_project   Realdom
%global php_home     %{_datadir}/php
%global ns_vendor    Hoa
%global ns_project   Realdom
%global pk_vendor    hoa
%global pk_project   realdom
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
BuildRequires:  php-composer(%{pk_vendor}/compiler)        >= 3.0
BuildRequires:  php-composer(%{pk_vendor}/consistency)     >= 1.0
BuildRequires:  php-composer(%{pk_vendor}/exception)       >= 1.0
BuildRequires:  php-composer(%{pk_vendor}/file)            >= 1.0
BuildRequires:  php-composer(%{pk_vendor}/iterator)        >= 2.0
BuildRequires:  php-composer(%{pk_vendor}/math)            >= 1.0
BuildRequires:  php-composer(%{pk_vendor}/praspel)         >= 1.0
BuildRequires:  php-composer(%{pk_vendor}/regex)           >= 1.0
BuildRequires:  php-composer(%{pk_vendor}/ustring)         >= 4.0
BuildRequires:  php-composer(%{pk_vendor}/visitor)         >= 2.0
%endif

# from composer.json, "require": {
#        "hoa/compiler"   : "~3.0",
#        "hoa/consistency": "~1.0",
#        "hoa/exception"  : "~1.0",
#        "hoa/file"       : "~1.0",
#        "hoa/iterator"   : "~2.0",
#        "hoa/math"       : "~1.0",
#        "hoa/praspel"    : "~1.0",
#        "hoa/regex"      : "~1.0",
#        "hoa/ustring"    : "~4.0",
#        "hoa/visitor"    : "~2.0"
Requires:       php-composer(%{pk_vendor}/compiler)        >= 3.0
Requires:       php-composer(%{pk_vendor}/compiler)        <  4
Requires:       php-composer(%{pk_vendor}/consistency)     >= 1.0
Requires:       php-composer(%{pk_vendor}/consistency)     <  2
Requires:       php-composer(%{pk_vendor}/exception)       >= 1.0
Requires:       php-composer(%{pk_vendor}/exception)       <  2
Requires:       php-composer(%{pk_vendor}/file)            >= 1.0
Requires:       php-composer(%{pk_vendor}/file)            <  2
Requires:       php-composer(%{pk_vendor}/iterator)        >= 2.0
Requires:       php-composer(%{pk_vendor}/iterator)        <  3
Requires:       php-composer(%{pk_vendor}/math)            >= 1.0
Requires:       php-composer(%{pk_vendor}/math)            <  2
Requires:       php-composer(%{pk_vendor}/praspel)         >= 1.0
Requires:       php-composer(%{pk_vendor}/praspel)         <  2
Requires:       php-composer(%{pk_vendor}/regex)           >= 1.0
Requires:       php-composer(%{pk_vendor}/regex)           <  2
Requires:       php-composer(%{pk_vendor}/ustring)         >= 4.0
Requires:       php-composer(%{pk_vendor}/ustring)         <  5
Requires:       php-composer(%{pk_vendor}/visitor)         >= 2.0
Requires:       php-composer(%{pk_vendor}/visitor)         <  3
# from phpcompatinfo report for version 1.16.01.15
Requires:       php-reflection
Requires:       php-date
Requires:       php-mbstring
Requires:       php-pcre
Requires:       php-spl

Provides:       php-composer(%{pk_vendor}/%{pk_project}) = %{version}


%description
The %{ns_vendor}\%{ns_project} library.

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
  cp -pr {}  %{buildroot}%{php_home}/%{ns_vendor}/%{ns_project} \;


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
* Fri Apr  8 2016 Remi Collet <remi@fedoraproject.org> - 1.16.01.15-0
- initial package
- bootstrap build

