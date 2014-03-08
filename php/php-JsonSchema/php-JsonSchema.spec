%global github_owner   justinrainbow
%global github_name    json-schema
%global github_version 1.3.6
%global github_commit  d97cf3ce890fe80f247fc08594a1c8a1029fc7ed

# See https://github.com/justinrainbow/json-schema/pull/96
%global php_min_ver    5.3.2

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
BuildRequires: php-pear(pear.phpunit.de/PHPUnit)
# For tests: phpcompatinfo (computed from v1.3.6)
BuildRequires: php-curl
BuildRequires: php-date
BuildRequires: php-filter
BuildRequires: php-json
BuildRequires: php-mbstring
BuildRequires: php-pcre
BuildRequires: php-spl

Requires:      php(language) >= %{php_min_ver}
# phpcompatinfo (computed from v1.3.6)
Requires:      php-curl
Requires:      php-filter
Requires:      php-json
Requires:      php-mbstring
Requires:      php-pcre
Requires:      php-spl

%description
A PHP implementation for validating JSON structures against a given schema.

See http://json-schema.org for more details.


%prep
%setup -qn %{github_name}-%{github_commit}

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

# Update bin file
sed 's#/usr/bin/env php#%{_bindir}/php#' \
    -i bin/validate-json


%build
# Empty build section, nothing to build


%install
# Install lib
mkdir -pm 755 %{buildroot}%{_datadir}/php
cp -rp src/%{lib_name} %{buildroot}%{_datadir}/php/

# Install bin
mkdir -pm 0755 %{buildroot}%{_bindir}
cp -p bin/validate-json %{buildroot}%{_bindir}/


%check
# Remove empty tests
rm -rf tests/JsonSchema/Tests/Drafts

%{_bindir}/phpunit \
    --include-path="./src:./tests" \
    --bootstrap="./autoload.php" \
    -d date.timezone="UTC"


%files
%defattr(-,root,root,-)
%doc LICENSE README.md composer.json
%{_datadir}/php/%{lib_name}
%{_bindir}/validate-json


%changelog
* Sat Mar  8 2014 Remi Collet <remi@fedoraproject.org> - 1.3.6-1
- backport 1.3.6 for remi repo.

* Fri Mar 07 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.3.6-1
- Updated to 1.3.6 (BZ #1073969)

* Mon Dec 30 2013 Remi Collet <remi@fedoraproject.org> - 1.3.5-1
- backport 1.3.5 for remi repo.

* Sun Dec 29 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 1.3.5-1
- Updated to 1.3.5

* Thu Dec 12 2013 Remi Collet <remi@fedoraproject.org> - 1.3.4-1
- backport 1.3.4 for remi repo.

* Mon Dec 09 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 1.3.4-1
- Updated to 1.3.4
- php-common => php(language)
- Removed the following build requires:
  -- php-pear(pear.phpunit.de/DbUnit),
  -- php-pear(pear.phpunit.de/PHPUnit_Selenium)
  -- php-pear(pear.phpunit.de/PHPUnit_Story)
- Added bin
- Updated %%check to use PHPUnit's "--include-path" option

* Tue Aug 20 2013 Remi Collet <remi@fedoraproject.org> - 1.3.3-1
- backport 1.3.3 for remi repo.

* Sun Aug 11 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 1.3.3-1
- Updated to 1.3.3

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
