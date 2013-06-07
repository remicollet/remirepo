%global github_owner   leafo
%global github_name    scssphp
%global github_version 0.0.7
%global github_commit  e5a79218c349cbc03dc99004fbad938c7b82391f

%global php_min_ver    5.3.0

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
# For tests
BuildRequires: php(language) >= %{php_min_ver}
BuildRequires: php-pear(pear.phpunit.de/PHPUnit)
# For tests: phpci
BuildRequires: php-ctype
BuildRequires: php-date
BuildRequires: php-pcre

Requires:      php(language) >= %{php_min_ver}
# phpci
Requires:      php-ctype
Requires:      php-date
Requires:      php-pcre

%description
SCSS (http://sass-lang.com/) is a CSS preprocessor that adds many features like
variables, mixins, imports, color manipulation, functions, and tons of other
powerful features.

The entire compiler comes in a single class file ready for including in any kind
of project in addition to a command line tool for running the compiler from the
terminal.

scssphp implements SCSS (3.2.7). It does not implement the SASS syntax, only
the SCSS syntax.


%prep
%setup -q -n %{github_name}-%{github_commit}

# Create man page for bin
# Required here b/c path to include file is changed in next command
help2man --no-info ./pscss > pscss.1

# Update bin shebang and require
sed -e 's#/usr/bin/env php#%{_bindir}/php#' \
    -e 's#scss.inc.php#%{_datadir}/php/%{github_name}/scss.inc.php#' \
    -i pscss


%build
# Empty build section, nothing to build


%install
mkdir -p -m 755 %{buildroot}%{_datadir}/php/%{github_name}
install -p -m 644 scss.inc.php %{buildroot}%{_datadir}/php/%{github_name}/

mkdir -p -m 755 %{buildroot}%{_bindir}
install -p -m 755 pscss %{buildroot}%{_bindir}/

mkdir -p -m 755  %{buildroot}%{_mandir}/man1
install -p -m 644 pscss.1 %{buildroot}%{_mandir}/man1/


%check
%{_bindir}/phpunit tests


%files
%defattr(-,root,root,-)
%doc *.md composer.json
%doc %{_mandir}/man1/pscss.1*
%{_datadir}/php/%{github_name}
%{_bindir}/pscss


%changelog
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
