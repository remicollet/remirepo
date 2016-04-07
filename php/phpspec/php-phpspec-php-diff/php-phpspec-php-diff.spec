# spec file for php-phpspec-php-diff
#
# Copyright (c) 2015-2016 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    0464787bfa7cd13576c5a1e318709768798bec6a
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     phpspec
%global gh_project   php-diff

Name:           php-phpspec-php-diff
Version:        1.1.0
Release:        1%{?dist}
Summary:        A library for generating differences between two hashable objects

Group:          Development/Libraries
# LICENSE text is inclued in the README file
License:        BSD
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}.tar.gz

# Fix example to use our generated autoloader
Patch0:         %{gh_project}-example.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
# For minimal test
BuildRequires:  php-cli
# To generate an autoloader
BuildRequires:  %{_bindir}/phpab

Requires:       php(language)
Requires:       php-pcre

Provides:       php-composer(phpspec/php-diff) = %{version}


%description
A comprehensive library for generating differences between two hashable
objects (strings or arrays). Generated differences can be rendered in
all of the standard formats including:
 * Unified
 * Context
 * Inline HTML
 * Side by Side HTML

The logic behind the core of the diff engine (ie, the sequence matcher)
is primarily based on the Python difflib package. The reason for doing
so is primarily because of its high degree of accuracy.


%prep
%setup -q -n %{gh_project}-%{gh_commit}

%patch0 -p0


%build
: Generate a simple autoloader
%{_bindir}/phpab --output lib/autoload.php lib


%install
# No namespace, so use a package specific dir
rm -rf       %{buildroot}
mkdir -p     %{buildroot}%{_datadir}/php/phpspec/php-diff
cp -pr lib/* %{buildroot}%{_datadir}/php/phpspec/php-diff


%check
# Not really a test... but should work without error
cd example
%{_bindir}/php -d include_path=%{buildroot}%{_datadir}/php example.php >/dev/null


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc README example
%doc composer.json
%{_datadir}/php/phpspec


%changelog
* Thu Apr  7 2016 Remi Collet <remi@fedoraproject.org> - 1.1.0-1
- update to 1.1.0

* Tue Feb 17 2015 Remi Collet <remi@fedoraproject.org> - 1.0.2-1
- initial package
