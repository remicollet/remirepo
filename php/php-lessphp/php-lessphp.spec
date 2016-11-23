# remirepo spec file for php-lessphp, from:
#
# Fedora spec file for php-lessphp
#
# Copyright (c) 2012-2015 Shawn Iwinski <shawn.iwinski@gmail.com>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%global github_owner     leafo
%global github_name      lessphp
%global github_version   0.5.0
%global github_commit    0f5a7f5545d2bcf4e9fad9a228c8ad89cc9aa283

%global composer_vendor  leafo
%global composer_project lessphp

# Build using "--without tests" to disable tests
%global with_tests 0%{!?_without_tests:1}

%{!?phpdir:  %global phpdir  %{_datadir}/php}

Name:          php-%{composer_project}
Version:       %{github_version}
Release:       4%{?dist}
Summary:       A compiler for LESS written in PHP

Group:         Development/Libraries
License:       MIT or GPLv3
URL:           http://leafo.net/lessphp
Source0:       https://github.com/%{github_owner}/%{github_name}/archive/%{github_commit}/%{name}-%{github_version}-%{github_commit}.tar.gz

# https://github.com/leafo/lessphp/pull/626
Patch0:        %{name}-pr626.patch

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:     noarch
# Tests
%if %{with_tests}
BuildRequires: %{_bindir}/phpunit
## phpcompatinfo (computed from version 0.5.0)
BuildRequires: php(language) >= 5.3.0
BuildRequires: php-ctype
BuildRequires: php-date
BuildRequires: php-fileinfo
BuildRequires: php-pcre
%endif

Requires:      php-cli
# phpcompatinfo (computed from version 0.5.0)
Requires:      php(language) >= 5.3.0
Requires:      php-ctype
Requires:      php-date
Requires:      php-fileinfo
Requires:      php-pcre

# Composer
Provides:      php-composer(%{composer_vendor}/%{composer_project}) = %{version}

%description
lessphp is a compiler that generates CSS from a superset language which
adds a collection of convenient features often seen in other languages.
All CSS is compatible with LESS, so you can start using new features
with your existing CSS.

It is designed to be compatible with less.js (http://lesscss.org/), and
suitable as a drop in replacement for PHP projects.


%prep
%setup -qn %{github_name}-%{github_commit}
%patch0 -p1

: Update bin requires and shebang
sed 's#$path\s*=.*#$path = "%{phpdir}/%{composer_project}/";#' \
    -i plessc


%build
# Empty build section, nothing required


%install
rm -rf %{buildroot}
: Lib
mkdir -p %{buildroot}%{phpdir}/%{composer_project}
cp -p lessc.inc.php %{buildroot}%{phpdir}/%{composer_project}/

: Bin
mkdir -p %{buildroot}%{_bindir}
cp -p plessc %{buildroot}%{_bindir}/


%check
%if %{with_tests}
# remirepo:11
run=0
ret=0
if which php56; then
   php56 %{_bindir}/phpunit tests || ret=1
   run=1
fi
if which php71; then
   php71 %{_bindir}/phpunit tests || ret=1
   run=1
fi
if [ $run -eq 0 ]; then
%{_bindir}/phpunit --verbose tests
# remirepo:2
fi
exit $ret
%else
: Tests skipped
%endif


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc README.md
%doc composer.json
%doc docs/*
%{phpdir}/%{composer_project}
%{_bindir}/plessc


%changelog
* Wed Nov 23 2016 Remi Collet <remi@fedoraproject.org> - 0.5.0-4
- add patch for lib_luma and fix FTBFS with PHP 7.1
  https://github.com/leafo/lessphp/pull/626

* Sun Jun 28 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 0.5.0-2
- Added php-composer(leafo/lessphp) virtual provide

* Sun Jun 28 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 0.5.0-1
- Updated to 0.5.0 (RHBZ #1211066)
- %%license usage
- Unpackaged tests
- Removed bin manpage
- Spec cleanup

* Tue Aug 20 2013 Remi Collet <RPMS@famillecollet.com> 0.4.0-1
- backport 0.4.0 for remi repo

* Sun Aug 11 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 0.4.0-1
- Updated to 0.4.0

* Thu Mar 07 2013 Remi Collet <RPMS@famillecollet.com> 0.3.9-1
- backport 0.3.9 for remi repo

* Sun Mar 03 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 0.3.9-1
- Updated to upstream version 0.3.9
- Added php_min_ver global

* Sun Nov 25 2012 Remi Collet <RPMS@famillecollet.com> 0.3.8-3
- backport 0.3.8 for remi repo

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
