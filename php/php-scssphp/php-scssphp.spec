#
# RPM spec file for php-scssphp
#
# Copyright (c) 2012-2014 Shawn Iwinski <shawn.iwinski@gmail.com>
#                         Remi Collet <remi@fedoraproject.org>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%global github_owner    leafo
%global github_name     scssphp
%global github_version  0.0.15
%global github_commit   85348dde6f193fe390aff76b21d816415ffef93b

# "php": ">=5.3.0"
%global php_min_ver     5.3.0
# "phpunit/phpunit": "3.7.*"
#     NOTE: Max version ignored
%global phpunit_min_ver 3.7.0

# Build using "--without tests" to disable tests
%global with_tests      %{?_without_tests:0}%{!?_without_tests:1}

Name:          php-%{github_name}
Version:       %{github_version}
Release:       1%{?dist}
Summary:       A compiler for SCSS written in PHP

Group:         Development/Libraries
License:       MIT or GPLv3
URL:           http://leafo.net/%{github_name}
Source0:       https://github.com/%{github_owner}/%{github_name}/archive/%{github_commit}/%{name}-%{github_version}-%{github_commit}.tar.gz

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:     noarch
BuildRequires: help2man
%if %{with_tests}
# For tests: composer.json
BuildRequires: php(language) >= %{php_min_ver}
BuildRequires: php-phpunit-PHPUnit >= %{phpunit_min_ver}
# For tests: phpcompatinfo (computed from version 0.0.15)
BuildRequires: php-ctype
BuildRequires: php-date
BuildRequires: php-pcre
%endif

# composer.json
Requires:      php(language) >= %{php_min_ver}
# phpcompatinfo (computed from version 0.0.15)
Requires:      php-ctype
Requires:      php-date
Requires:      php-pcre

Provides:      php-composer(leafo/scssphp) = %{version}


%description
SCSS (http://sass-lang.com/) is a CSS preprocessor that adds many features like
variables, mixins, imports, color manipulation, functions, and tons of other
powerful features.

The entire compiler comes in a single class file ready for including in any kind
of project in addition to a command line tool for running the compiler from the
terminal.

scssphp implements SCSS (3.2.12). It does not implement the SASS syntax, only
the SCSS syntax.


%prep
%setup -qn %{github_name}-%{github_commit}

# Fix version (see https://github.com/leafo/scssphp/pull/174)
sed -i 's/0.0.11/0.0.12/' scss.inc.php

# Create man page for bin
# Required here b/c path to include file is changed in next command
help2man --no-info ./pscss > pscss.1

# Update bin she-bang and require
sed -e 's#/usr/bin/env php#%{_bindir}/php#' \
    -e 's#scss.inc.php#%{_datadir}/php/%{github_name}/scss.inc.php#' \
    -i pscss


%build
# Empty build section, nothing to build


%install
mkdir -p %{buildroot}%{_datadir}/php/%{github_name}
install -pm 0644 scss.inc.php %{buildroot}%{_datadir}/php/%{github_name}/

mkdir -p %{buildroot}%{_bindir}
install -pm 0755 pscss %{buildroot}%{_bindir}/

mkdir -p %{buildroot}%{_mandir}/man1
install -pm 0644 pscss.1 %{buildroot}%{_mandir}/man1/


%check
%if %{with_tests}
# Create PHPUnit config w/ colors turned off
sed 's/colors\s*=\s*"true"/colors="false"/' phpunit.xml.dist > phpunit.xml

%{_bindir}/phpunit tests
%else
: Tests skipped
%endif


%files
%defattr(-,root,root,-)
%doc *.md composer.json
%doc %{_mandir}/man1/pscss.1*
%{_datadir}/php/%{github_name}
%{_bindir}/pscss


%changelog
* Tue Aug 19 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 0.0.15-1
- Updated to 0.0.15 (BZ #1126612)

* Mon Jul 07 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 0.0.12-1
- Updated to 0.0.12 (BZ #1116615)
- Added option to build without tests ("--without tests")

* Sun Jun  8 2014 Remi Collet <remi@fedoraproject.org> - 0.0.10-2
- fix FTBFS, ignore max version of PHPUnit
- provides php-composer(leafo/scssphp)

* Tue Apr 22 2014 Remi Collet <remi@fedoraproject.org> 0.0.10-1
- backport 0.0.9 for remi repo.

* Mon Apr 21 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 0.0.10-1
- Updated to 0.0.10 (BZ #1087738)

* Mon Dec 30 2013 Remi Collet <remi@fedoraproject.org> 0.0.9-1
- backport 0.0.9 for remi repo.

* Sun Dec 29 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 0.0.9-1
- Updated to 0.0.9 (BZ #1046671)
- Spec cleanup

* Sat Nov 16 2013 Remi Collet <remi@fedoraproject.org> 0.0.8-1
- backport 0.0.8 for remi repo.

* Fri Nov 15 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 0.0.8-1
- Updated to 0.0.8

* Fri Jun 07 2013 Remi Collet <remi@fedoraproject.org> 0.0.7-1
- backport 0.0.7 for remi repo.

* Fri Jun 07 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 0.0.7-1
- Updated to 0.0.7

* Tue Mar 19 2013 Remi Collet <remi@fedoraproject.org> 0.0.5-1
- backport 0.0.5 for remi repo.

* Sat Mar 16 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 0.0.5-1
- Updated to version 0.0.5
- php-cli => php(language)
- %%{__php} => %%{_bindir}/php

* Sat Mar 09 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 0.0.4-2.20130301git3463d7d
- Updated to latest snapshot
- php-common => php-cli
- Added man page
- Removed tests from package

* Tue Nov 27 2012 Shawn Iwinski <shawn.iwinski@gmail.com> 0.0.4-1
- Initial package
