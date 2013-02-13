%global github_owner   Seldaek
%global github_name    jsonlint
%global github_version 1.1.1
%global github_commit  2b5b57008ec93148fa46110d42c7a201a6677fe0

%global php_min_ver    5.3.0

Name:          php-%{github_name}
Version:       %{github_version}
Release:       1%{?dist}
Summary:       JSON Lint for PHP

Group:         Development/Libraries
License:       MIT
URL:           https://github.com/%{github_owner}/%{github_name}
Source0:       %{url}/archive/%{github_commit}/%{name}-%{github_version}-%{github_commit}.tar.gz

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:     noarch
# For tests
BuildRequires: php(language) >= %{php_min_ver}
BuildRequires: php-pear(pear.phpunit.de/PHPUnit)
# For tests: phpci
BuildRequires: php-pcre

Requires:      php(language) >= %{php_min_ver}
# phpci
Requires:      php-pcre

%description
%{summary}.

This library is a port of the JavaScript jsonlint
(https://github.com/zaach/jsonlint) library.


%prep
%setup -q -n %{github_name}-%{github_commit}

# Create PSR-0 autoloader for tests
( cat <<'AUTOLOAD'
<?php
spl_autoload_register(function ($class) {
    $src = str_replace('\\', '/', $class).'.php';
    require_once $src;
});
AUTOLOAD
) > autoload.php


%build
# Empty build section, nothing to build


%install
mkdir -p -m 755 %{buildroot}%{_datadir}/php/Seld
cp -rp src/Seld/JsonLint %{buildroot}%{_datadir}/php/Seld/


%check
%{_bindir}/phpunit --bootstrap=./autoload.php \
    -d include_path="./src:./tests:.:%{pear_phpdir}" .


%files
%defattr(-,root,root,-)
%doc LICENSE README.mdown composer.json
%dir %{_datadir}/php/Seld
     %{_datadir}/php/Seld/JsonLint


%changelog
* Wed Feb 13 2013 Remi Collet <RPMS@FamilleCollet.com> - 1.1.1-1
- backport 1.1.1 for remi repo

* Tue Feb 12 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 1.1.1-1
- Updated to upstream version 1.1.1
- Updates per new Fedora packaging guidelines for Git repos

* Wed Jan  9 2013 Remi Collet <RPMS@FamilleCollet.com> - 1.1.0-1
- backport for remi repo

* Mon Jan 07 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 1.1.0-1
- Initial package
