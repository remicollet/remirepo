# remirepo spec file for php-JsonSchema, from:
#
# Fedora spec file for php-JsonSchema
#
# Copyright (c) 2012-2015 Shawn Iwinski <shawn.iwinski@gmail.com>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%global github_owner   justinrainbow
%global github_name    json-schema
%global github_version 1.4.3
%global github_commit  44adc6f25592c6990409607c95537f577861f9b1
%global github_short   %(c=%{github_commit}; echo ${c:0:7})

%global php_min_ver    5.3.2

%global lib_name       JsonSchema
%global phpdir         %{_datadir}/php

# Build using "--without tests" to disable tests
%global with_tests     0%{!?_without_tests:1}

Name:          php-%{lib_name}
Version:       %{github_version}
Release:       1%{?dist}
Summary:       PHP implementation of JSON schema

Group:         Development/Libraries
License:       BSD
URL:           https://github.com/%{github_owner}/%{github_name}
Source0:       %{url}/archive/%{github_commit}/%{name}-%{github_version}-%{github_short}.tar.gz
# Autoloader
Source1:       %{name}-autoload.php

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch
%if %{with_tests}
# For tests
BuildRequires: php(language) >= %{php_min_ver}
BuildRequires: php-phpunit-PHPUnit
# For tests: phpcompatinfo (computed from v1.4.3)
BuildRequires: php-curl
BuildRequires: php-date
BuildRequires: php-filter
BuildRequires: php-json
BuildRequires: php-mbstring
BuildRequires: php-pcre
BuildRequires: php-spl
# Autoloader
BuildRequires: php-composer(symfony/class-loader)
%endif

Requires:      php(language) >= %{php_min_ver}
# phpcompatinfo (computed from v1.4.3)
Requires:      php-cli
Requires:      php-curl
Requires:      php-date
Requires:      php-filter
Requires:      php-json
Requires:      php-mbstring
Requires:      php-pcre
Requires:      php-spl
# Autoloader
Requires:      php-composer(symfony/class-loader)

# Composer
Provides:      php-composer(justinrainbow/json-schema) = %{version}


%description
A PHP implementation for validating JSON structures against a given schema.

See http://json-schema.org for more details.


%prep
%setup -qn %{github_name}-%{github_commit}

cp -p %{SOURCE1} src/%{lib_name}/autoload.php


%build
# Empty build section, nothing to build


%install
# Install lib
mkdir -p %{buildroot}%{phpdir}
cp -rp src/* %{buildroot}%{phpdir}/

# Install bin
install -Dpm 0755 bin/validate-json %{buildroot}%{_bindir}/validate-json


%check
%if %{with_tests}
# Remove empty tests
rm -rf tests/%{lib_name}/Tests/Drafts

mkdir vendor
cat <<EOF | tee vendor/autoload.php
<?php
require '%{buildroot}%{phpdir}/%{lib_name}/autoload.php';
\$fedoraClassLoader->addPrefix('%{lib_name}\\\\Tests\\\\', realpath(__DIR__.'/../tests'));
EOF

%{_bindir}/phpunit --verbose
%else
: Tests skipped
%endif


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc README.md composer.json
%{phpdir}/%{lib_name}
%{_bindir}/validate-json


%changelog
* Tue Jul 14 2015 Remi Collet <remi@fedoraproject.org> - 1.4.3-1
- update to 1.4.3
- add autoloader

* Mon Jun 15 2015 Remi Collet <remi@fedoraproject.org> - 1.4.2-1
- update to 1.4.2

* Mon Apr 13 2015 Remi Collet <remi@fedoraproject.org> - 1.4.1-2
- fix tests autoloader (FTBFS detected by Koschei)

* Fri Mar 27 2015 Remi Collet <remi@fedoraproject.org> - 1.4.1-1
- Update to 1.4.1

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
