%global github_owner   justinrainbow
%global github_name    json-schema
%global github_version 1.3.2
%global github_commit  3ec2db504e7a79d6504ad8172a706adec5eec681

%global php_min_ver    5.3.0

%global lib_name       JsonSchema

Name:          php-%{lib_name}
Version:       %{github_version}
Release:       1%{?dist}
Summary:       PHP implementation of JSON schema

Group:         Development/Libraries
License:       BSD
URL:           https://github.com/%{github_owner}/%{github_name}
Source0:       %{url}/archive/%{github_commit}/%{name}-%{github_version}-%{github_commit}.tar.gz

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch
# For tests
BuildRequires: php(language) >= %{php_min_ver}
BuildRequires: php-pear(pear.phpunit.de/DbUnit)
BuildRequires: php-pear(pear.phpunit.de/PHPUnit)
BuildRequires: php-pear(pear.phpunit.de/PHPUnit_Selenium)
BuildRequires: php-pear(pear.phpunit.de/PHPUnit_Story)

# For tests: phpci
BuildRequires: php-curl
BuildRequires: php-json
BuildRequires: php-mbstring
BuildRequires: php-pcre
BuildRequires: php-spl
BuildRequires: php-filter

Requires:      php(language) >= %{php_min_ver}
# phpci
Requires:      php-curl
Requires:      php-json
Requires:      php-mbstring
Requires:      php-pcre
Requires:      php-spl
Requires:      php-filter

%description
A PHP implementation for validating JSON structures against a given schema.

See http://json-schema.org for more details.


%prep
%setup -q -n %{github_name}-%{github_commit}

# Clean up unnecessary files
find . -type f -name '.git*' -delete

# Create autoloader for tests
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
mkdir -p -m 755 %{buildroot}%{_datadir}/php
cp -rp src/%{lib_name} %{buildroot}%{_datadir}/php/


%check
# Remove empty tests
rm -f tests/JsonSchema/Tests/Drafts/Draft3Test.php \
      tests/JsonSchema/Tests/Drafts/Draft4Test.php

%{_bindir}/phpunit \
    -d include_path="./src:./tests:.:%{pear_phpdir}" \
    -d date.timezone="UTC" \
    --bootstrap=./autoload.php \
    .


%files
%defattr(-,root,root,-)
%doc LICENSE README.md composer.json
%{_datadir}/php/%{lib_name}


%changelog
* Mon Jul  8 2013 Remi Collet <remi@fedoraproject.org> - 1.3.2-1
- backport 1.3.2 for remi repo.

* Fri Jul 05 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 1.3.2-1
- Updated to 1.3.2
- Added php-pear(pear.phpunit.de/DbUnit), php-pear(pear.phpunit.de/PHPUnit_Selenium),
  and php-pear(pear.phpunit.de/PHPUnit_Story) build requires
- Removed php-ctype require
- Added php-mbstring require

* Sat Mar 23 2013 Remi Collet <remi@fedoraproject.org> - 1.3.1-1
- backport 1.3.1 for remi repo.

* Thu Mar 21 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 1.3.1-1
- Updated to upstream version 1.3.1

* Tue Feb 26 2013 Remi Collet <remi@fedoraproject.org> - 1.3.0-1
- backport 1.3.0 for remi repo.

* Sun Feb 24 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 1.3.0-1
- Updated to upstream version 1.3.0

* Thu Feb  7 2013 Remi Collet <remi@fedoraproject.org> - 1.2.4-1
- backport 1.2.4 for remi repo.

* Mon Feb 04 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 1.2.4-1
- Updated to upstream version 1.2.4
- Updates per new Fedora packaging guidelines for Git repos

* Mon Dec 17 2012 Remi Collet <remi@fedoraproject.org> - 1.2.2-2
- backport for remi repo.

* Sun Dec  9 2012 Shawn Iwinski <shawn.iwinski@gmail.com> 1.2.2-2
- Fixed failing Mock/Koji builds
- Removed "docs" directory from %%doc

* Sat Dec  8 2012 Shawn Iwinski <shawn.iwinski@gmail.com> 1.2.2-1
- Updated to upstream version 1.2.2
- Added php-ctype require
- Added PSR-0 autoloader for tests
- Added %%check

* Tue Nov 27 2012 Shawn Iwinski <shawn.iwinski@gmail.com> 1.2.1-1
- Initial package
