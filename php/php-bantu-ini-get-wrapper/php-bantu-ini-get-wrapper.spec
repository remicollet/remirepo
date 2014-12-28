%global github_owner    bantuXorg
%global github_name     php-ini-get-wrapper
%global github_version  1.0.1
%global github_commit   4770c7feab370c62e23db4f31c112b7c6d90aee2
%global packagist_owner bantu
%global packagist_name  ini-get-wrapper
%global psr4_namespace  bantu
%global psr4_prefix     %{psr4_namespace}/IniGetWrapper

# phpci: uses namespaces
%global php_min_ver    5.3.0

Name:          php-%{packagist_owner}-%{packagist_name}
Version:       %{github_version}
Release:       1%{?dist}
Summary:       Convenience wrapper around PHP's ini_get() function

Group:         Development/Libraries
License:       MIT
URL:           https://github.com/%{github_owner}/%{github_name}
# Must use commit-based not tag-based github tarball:
# https://fedoraproject.org/wiki/Packaging:SourceURL#Github
Source0:       https://github.com/%{github_owner}/%{github_name}/archive/%{github_commit}/%{github_name}-%{github_commit}.tar.gz

BuildArch:     noarch
# For tests
BuildRequires: php(language) >= %{php_min_ver}
BuildRequires: %{_bindir}/phpunit
BuildRequires: %{_bindir}/phpab

Requires:      php(language) >= %{php_min_ver}

Provides:       php-composer(%{packagist_owner}/%{packagist_name}) = %{version}

%description
Convenience wrapper around ini_get().


%prep
%setup -qn %{github_name}-%{github_commit}


%build
# Empty build section, nothing required


%install
# use PSR-0 layout relative to _datadir/php
mkdir -p %{buildroot}%{_datadir}/php/%{psr4_prefix}
cp -pr src/* %{buildroot}%{_datadir}/php/%{psr4_prefix}


%check
# roll our own loader to run tests
%{_bindir}/phpab --output bootstrap.php --exclude *Test.php --basedir . src tests

# run tests
%{_bindir}/phpunit --bootstrap bootstrap.php


%files
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc *.md composer.json
%{_datadir}/php/%{psr4_namespace}


%changelog
* Fri Dec 12 2014 Adam Williamson <awilliam@redhat.com> - 1.0.1-1
- initial package
