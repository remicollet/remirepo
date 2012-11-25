%global libname lessphp

Name:          php-%{libname}
Version:       0.3.8
Release:       3%{?dist}
Summary:       A compiler for LESS written in PHP

Group:         Development/Libraries
License:       MIT or GPLv3
URL:           http://leafo.net/lessphp
Source0:       %{url}/src/%{libname}-%{version}.tar.gz

BuildArch:     noarch
BuildRequires: help2man
# Test requires
BuildRequires: php-pear(pear.phpunit.de/PHPUnit)
# Test requires: phpci
BuildRequires: php-ctype
BuildRequires: php-date
BuildRequires: php-pcre

Requires:      php-common
# phpci requires
Requires:      php-ctype
Requires:      php-date
Requires:      php-pcre

%description
lessphp is a compiler that generates CSS from a superset language which
adds a collection of convenient features often seen in other languages.
All CSS is compatible with LESS, so you can start using new features
with your existing CSS.

It is designed to be compatible with less.js (http://lesscss.org/), and
suitable as a drop in replacement for PHP projects.


%prep
%setup -q -n %{libname}

# Create man page for bin
# Required here b/c path to include file is changed in next command
help2man --version-option='-v' --no-info ./plessc > plessc.1

# Update path in bin file
sed 's#$path\s*=.*#$path = "%{_datadir}/php/%{libname}/";#' \
    -i plessc

# Update tests' require
sed -e 's#.*require.*lessc.inc.php.*#require_once "%{_datadir}/php/%{libname}/lessc.inc.php";#' \
    -i tests/*.php


%build
# Empty build section, nothing required


%install
mkdir -p -m 755 %{buildroot}%{_datadir}/php/%{libname}
cp -p lessc.inc.php %{buildroot}%{_datadir}/php/%{libname}/

mkdir -p -m 755 %{buildroot}%{_datadir}/tests/%{name}
cp -rp tests/* %{buildroot}%{_datadir}/tests/%{name}/

mkdir -p %{buildroot}%{_bindir}
cp -p plessc %{buildroot}%{_bindir}/

mkdir -p %{buildroot}%{_mandir}/man1
cp -p plessc.1 %{buildroot}%{_mandir}/man1/


%check
# Update tests' require to use buildroot
sed 's#%{_datadir}#%{buildroot}%{_datadir}#' -i tests/*.php

%{_bindir}/phpunit tests


%files
%doc LICENSE README.md docs composer.json
%doc %{_mandir}/man1/plessc.1*
%{_datadir}/php/%{libname}
%{_bindir}/plessc
%dir %{_datadir}/tests
     %{_datadir}/tests/%{name}


%changelog
* Sun Nov 18 2012 Shawn Iwinski <shawn.iwinski@gmail.com> 0.3.8-3
- Fixed man page creation
- Added tests directory ownership

* Sat Nov 17 2012 Shawn Iwinski <shawn.iwinski@gmail.com> 0.3.8-2
- Added phpci requires to build requires
- Simplified %%prep and updated %%install and %%check
- Moved tests to %%{_datadir}/tests/%%{name}

* Wed Nov  7 2012 Shawn Iwinski <shawn.iwinski@gmail.com> 0.3.8-1
- Updated to upstream version 0.3.8
- Removed adding of shebang to bootstrap script (fixed upstream)
- Fixed man file creation and removed manual gzip

* Mon Aug 13 2012 Shawn Iwinski <shawn.iwinski@gmail.com> 0.3.6-1
- Updated to upstream version 0.3.6

* Thu Jul 12 2012 Shawn Iwinski <shawn.iwinski@gmail.com> 0.3.5-1
- Initial package
