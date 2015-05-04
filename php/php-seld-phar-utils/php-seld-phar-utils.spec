# spec file for php-seld-phar-utils
#
# Copyright (c) 2015 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    336bb5ee20de511f3c1a164222fcfd194afcab3a
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     Seldaek
%global gh_project   phar-utils

Name:           php-seld-phar-utils
Version:        1.0.0
Release:        1%{?dist}
Summary:        PHAR file format utilities

Group:          Development/Libraries
License:        MIT
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}-%{gh_short}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php(language) >= 5.3

# From composer.json
#       "php": ">=5.3.0",
Requires:       php(language) >= 5.3.0
# From phpcompatifo report for 1.0.0
Requires:       php-date
Requires:       php-hash
Requires:       php-pcre
Requires:       php-spl

Provides:       php-composer(seld/phar-utils) = %{version}


%description
PHAR file format utilities, for when PHP phars you up.


%prep
%setup -q -n %{gh_project}-%{gh_commit}


%build
# Nothing


%install
rm -rf       %{buildroot}
# Restore PSR-0 tree
mkdir -p     %{buildroot}%{_datadir}/php/Seld/PharUtils/
cp -pr src/* %{buildroot}%{_datadir}/php/Seld/PharUtils/


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc README.md composer.json
%{_datadir}/php/Seld


%changelog
* Mon May  4 2015 Remi Collet <remi@fedoraproject.org> - 1.0.0-1
- initial package