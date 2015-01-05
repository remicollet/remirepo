#
# RPM spec file for php-jsonlint
#
# Copyright (c) 2013-2015 Shawn Iwinski <shawn.iwinski@gmail.com>
#                         Remi Collet <remi@fedoraproject.org>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%global github_owner   Seldaek
%global github_name    jsonlint
%global github_version 1.3.1
%global github_commit  863ae85c6d3ef60ca49cb12bd051c4a0648c40c4

# "php": ">=5.3.0"
%global php_min_ver    5.3.0

# Build using "--without tests" to disable tests
%global with_tests     %{?_without_tests:0}%{!?_without_tests:1}

Name:          php-%{github_name}
Version:       %{github_version}
Release:       1%{?dist}
Summary:       JSON Lint for PHP

Group:         Development/Libraries
License:       MIT
URL:           https://github.com/%{github_owner}/%{github_name}
Source0:       %{url}/archive/%{github_commit}/%{name}-%{github_version}-%{github_commit}.tar.gz

# Bin usage without Composer autoloader
Patch0:        %{name}-bin-without-composer-autoloader.patch

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:     noarch
%if %{with_tests}
# For tests: composer.json
BuildRequires: php(language) >= %{php_min_ver}
BuildRequires: php-phpunit-PHPUnit
# For tests: phpcompatinfo (computed from version 1.3.1)
BuildRequires: php-pcre
%endif

Requires:      php(language) >= %{php_min_ver}
# phpcompatinfo (computed from version 1.3.1)
Requires:      php-pcre

Provides:      php-composer(seld/jsonlint) = %{version}


%description
%{summary}.

This library is a port of the JavaScript jsonlint
(https://github.com/zaach/jsonlint) library.


%prep
%setup -q -n %{github_name}-%{github_commit}

%patch0 -p1


%build
# Empty build section, nothing to build


%install
# Lib
mkdir -p %{buildroot}%{_datadir}/php/Seld
cp -rp src/Seld/JsonLint %{buildroot}%{_datadir}/php/Seld/

# Bin
mkdir -p %{buildroot}%{_bindir}
install -pm 0755 bin/jsonlint %{buildroot}%{_bindir}/


%check
%if %{with_tests}
# Create autoloader
cat > autoload.php <<'AUTOLOAD'
<?php
spl_autoload_register(function ($class) {
    $src = str_replace('\\', '/', $class).'.php';
    @include_once $src;
});
AUTOLOAD

%{_bindir}/phpunit --bootstrap ./autoload.php --include-path %{buildroot}%{_datadir}/php .
%else
: Tests skipped
%endif


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc *.mdown composer.json
%dir %{_datadir}/php/Seld
     %{_datadir}/php/Seld/JsonLint
%{_bindir}/jsonlint


%changelog
* Mon Jan  5 2015 Remi Collet <remi@fedoraproject.org> - 1.3.1-1
- Updated to 1.3.1

* Thu Sep 11 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.3.0-1
- Updated to 1.3.0 (BZ #1138911)

* Sat Aug 23 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.2.0-2
- %%license usage

* Wed Aug 20 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.2.0-1
- Updated to 1.2.0 (BZ #1124228)
- Added option to build without tests ("--without tests")
- Added bin

* Mon Jun  9 2014 Remi Collet <remi@fedoraproject.org> - 1.1.2-2
- fix FTBFS, include path during test
- upstream patch for latest PHPUnit
- provides php-composer(seld/jsonlint)

* Sat Nov 16 2013 Remi Collet <RPMS@FamilleCollet.com> - 1.1.2-1
- backport 1.1.2 for remi repo

* Fri Nov 15 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 1.1.2-1
- Updated to upstream version 1.1.2
- php-common => php(language)

* Wed Feb 13 2013 Remi Collet <RPMS@FamilleCollet.com> - 1.1.1-1
- backport 1.1.1 for remi repo

* Tue Feb 12 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 1.1.1-1
- Updated to upstream version 1.1.1
- Updates per new Fedora packaging guidelines for Git repos

* Wed Jan  9 2013 Remi Collet <RPMS@FamilleCollet.com> - 1.1.0-1
- backport for remi repo

* Mon Jan 07 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 1.1.0-1
- Initial package
