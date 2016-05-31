# spec file for php-iamcal-lib-autolink
#
# Copyright (c) 2016 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    b3a86d8437e5d635fb85b155a86288d94f6a924d
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     iamcal
%global gh_project   lib_autolink
%global with_tests   0%{!?_without_tests:1}


Name:           php-iamcal-lib-autolink
Version:        1.7
Release:        1%{?dist}
Summary:        Adds anchors to urls in a text

Group:          Development/Libraries
License:        MIT
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        %{name}-%{version}-%{gh_short}.tgz
# Used to retrieve a git snapshot with test suite
Source1:        makesrc.sh

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
# For tests
%if %{with_tests}
BuildRequires:  php-cli
BuildRequires:  php-pcre
%endif

# From composer.json, nothing
# From phpcompatinfo report for 1.7
Requires:       php-pcre

Provides:       php-composer(%{gh_owner}/%{gh_project}) = %{version}


%description
Find URLs in HTML that are not already links, and make them into links.

Autoloader: %{_datadir}/php/%{name}/autoload.php


%prep
%setup -q -n %{gh_project}-%{gh_commit}


%build
: Nothing


%install
rm -rf       %{buildroot}

: Single file, only functions
install -Dpm 0644 lib_autolink.php %{buildroot}%{_datadir}/php/%{name}/lib_autolink.php

# from composer.json, "autoload": {
#    "files": ["lib_autolink.php"]
ln -s lib_autolink.php %{buildroot}%{_datadir}/php/%{name}/autoload.php


%check
%if %{with_tests}
for unit in t/*.t; do
   %{_bindir}/php $unit | tee -a tests.log
done

if which php70; then
   for unit in t/*.t; do
      php70 $unit | tee -a tests.log
   done
fi

grep -q '^not ok' tests.log && exit 1
%else
: Test suite disabled
%endif


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc *.md
%doc composer.json
%{_datadir}/php/%{name}


%changelog
* Tue Apr 26 2016 Remi Collet <remi@fedoraproject.org> - 1.7-1
- initial package, version 1.7

