# spec file for php-znerol-php-stringprep
#
# Copyright (c) 2014 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/3.0/
#
# Please, preserve the changelog entries
#

%global gh_commit    a23ef2918be09761603dd009b3ad7450620df92f
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     znerol
%global gh_project   Stringprep
%global with_tests   %{?_without_tests:0}%{!?_without_tests:1}
%global topdir       %{_datadir}/php/Znerol
%global basedir      %{topdir}/Component/Stringprep

Name:           php-znerol-php-stringprep
Version:        0
Release:        0.1.20141109git%{gh_short}%{?dist}
Summary:        Implementation of RFC 3454 Preparation of Internationalized Strings

Group:          Development/Libraries
License:        LGPLv3
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
%if %{with_tests}
BuildRequires:  php-iconv
BuildRequires:  php-intl
BuildRequires:  php-spl
BuildRequires:  php-phpunit-PHPUnit
%endif
BuildRequires:  php-theseer-autoload

# From phpcompatinfo
Requires:       php-iconv
Requires:       php-intl
Requires:       php-spl

Provides:       php-composer(znerol/php-stringprep) = %{version}


%description
Implementation of RFC 3454 Preparation of Internationalized Strings.

See: http://tools.ietf.org/html/rfc3454


%prep
%setup -q -n %{gh_project}-%{gh_commit}


%build
# Generate a simple autoloader
%{_bindir}/php -d date.timezone=UTC \
%{_bindir}/phpab \
   --exclude *Test.php \
   --output autoload.php \
   .


%install
rm -rf   %{buildroot}
mkdir -p %{buildroot}%{basedir}
cp -pr Profile RFC3454 *php \
         %{buildroot}%{basedir}


%check
%if %{with_tests}
%{_bindir}/phpunit \
    --bootstrap %{buildroot}%{basedir}/autoload.php \
    -d date.timezone=UTC
%else
: Test suite disabled
%endif


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc README.md doc
%{topdir}


%changelog
* Sun Nov  9 2014 Remi Collet <remi@fedoraproject.org> - 0-0.1.20141109gita23ef29
- initial package (git snapshot)