#
# RPM spec file for php-JsonSchema
#
# Copyright (c) 2012-2014 Shawn Iwinski <shawn.iwinski@gmail.com>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%global github_owner   justinrainbow
%global github_name    json-schema
%global github_version 1.4.0
%global github_commit  680d026082c3aa234b2d8617c50e9c73999913ba
%global github_short   %(c=%{github_commit}; echo ${c:0:7})

# See https://github.com/justinrainbow/json-schema/pull/96
%global php_min_ver    5.3.2

%global lib_name       JsonSchema

# Build using "--without tests" to disable tests
%global with_tests     %{?_without_tests:0}%{!?_without_tests:1}

Name:          php-%{lib_name}
Version:       %{github_version}
Release:       1%{?dist}
Summary:       PHP implementation of JSON schema

Group:         Development/Libraries
License:       BSD
URL:           https://github.com/%{github_owner}/%{github_name}
Source0:       %{url}/archive/%{github_commit}/%{name}-%{github_version}-%{github_short}.tar.gz

# PHP < 5.4.0 compatibility for "--dump-schema"
# https://github.com/justinrainbow/json-schema/pull/109
Patch0:        %{name}-php-lt-5-4-0-compat.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch
%if %{with_tests}
# For tests
BuildRequires: php(language) >= %{php_min_ver}
BuildRequires: php-phpunit-PHPUnit
# For tests: phpcompatinfo (computed from v1.4.0)
BuildRequires: php-curl
BuildRequires: php-date
BuildRequires: php-filter
BuildRequires: php-json
BuildRequires: php-mbstring
BuildRequires: php-pcre
BuildRequires: php-spl
%endif

Requires:      php(language) >= %{php_min_ver}
# phpcompatinfo (computed from v1.4.0)
Requires:      php-curl
Requires:      php-filter
Requires:      php-json
Requires:      php-mbstring
Requires:      php-pcre
Requires:      php-spl

Provides:      php-composer(justinrainbow/json-schema) = %{version}


%description
A PHP implementation for validating JSON structures against a given schema.

See http://json-schema.org for more details.


%prep
%setup -qn %{github_name}-%{github_commit}

%patch0 -p1

# Update bin shebang
sed 's#/usr/bin/env php#%{_bindir}/php#' \
    -i bin/validate-json


%build
# Empty build section, nothing to build


%install
# Install lib
mkdir -pm 0755 %{buildroot}%{_datadir}/php
cp -rp src/* %{buildroot}%{_datadir}/php/

# Install bin
mkdir -pm 0755 %{buildroot}%{_bindir}
install -pm 0755 bin/validate-json %{buildroot}%{_bindir}/


%check
%if %{with_tests}
# Create autoloader
cat > autoload.php <<'AUTOLOAD'
<?php
spl_autoload_register(function ($class) {
    $src = str_replace('\\', '/', $class).'.php';
    require_once $src;
});
AUTOLOAD

# Remove empty tests
rm -rf tests/JsonSchema/Tests/Drafts

# Create PHPUnit config w/ colors turned off
sed 's/colors\s*=\s*"true"/colors="false"/' phpunit.xml.dist > phpunit.xml

%{_bindir}/phpunit \
    --include-path="./src:./tests" \
    --bootstrap="./autoload.php" \
    -d date.timezone="UTC"
%else
: Tests skipped
%endif


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc README.md composer.json
%{_datadir}/php/%{lib_name}
%{_bindir}/validate-json


%changelog
* Tue Mar 24 2015 Remi Collet <remi@fedoraproject.org> - 1.4.0-1
- Update to 1.4.0

* Sat Aug 30 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.3.7-2
- PHP < 5.4.0 compatibility patch instead of in-spec logic

* Fri Aug 29 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.3.7-1
- Updated to 1.3.7 (BZ #1133519)
- Added option to build without tests ("--without tests")
- Added "php-composer(justinrainbow/json-schema)" virtual provide
- Added PHP < 5.4.0 compatibility for "--dump-schema"
- %%check tweaks
- Added %%license usage

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
