#
# RPM spec file for php-doctrine-lexer
#
# Copyright (c) 2013-2015 Shawn Iwinski <shawn.iwinski@gmail.com>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%global github_owner     doctrine
%global github_name      lexer
%global github_version   1.0.1
%global github_commit    83893c552fd2045dd78aef794c31e694c37c0b8c

%global composer_vendor  doctrine
%global composer_project lexer

# "php": ">=5.3.2"
%global php_min_ver      5.3.2

Name:          php-%{composer_vendor}-%{composer_project}
Version:       %{github_version}
Release:       1%{?github_release}%{?dist}
Summary:       Base library for a lexer that can be used in top-down, recursive descent parsers

Group:         Development/Libraries
License:       MIT
URL:           https://github.com/%{github_owner}/%{github_name}
Source0:       %{url}/archive/%{github_commit}/%{name}-%{github_version}-%{github_commit}.tar.gz

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:     noarch

Requires:      php(language) >= %{php_min_ver}
# phpcompatinfo (computed from version 1.0.1)
Requires:      php-pcre
Requires:      php-reflection

# Composer
Provides:      php-composer(%{composer_vendor}/%{composer_project}) = %{version}

%description
Base library for a lexer that can be used in top-down, recursive descent
parsers.

This lexer is used in Doctrine Annotations and in Doctrine ORM (DQL).


%prep
%setup -qn %{github_name}-%{github_commit}


%build
# Empty build section, nothing required


%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/%{_datadir}/php
cp -rp lib/* %{buildroot}/%{_datadir}/php/


%check
# No upstream tests


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc *.md composer.json
%dir %{_datadir}/php/Doctrine
%dir %{_datadir}/php/Doctrine/Common
     %{_datadir}/php/Doctrine/Common/Lexer


%changelog
* Mon Jan 05 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.0.1-1
- Updated to 1.0.1 (same commit but tagged version instead of snapshot; BZ #1178808)
- %%license usage

* Sun Dec 07 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.0-5.20140909git83893c5
- Updated to latest snapshot (required for php-egulias-email-validator 1.2.6)

* Fri Jun 20 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.0-4.20131220gitf12a5f7
- Added php-composer(%%{composer_vendor}/%%{composer_project}) virtual provide

* Sat Jan 11 2014 Remi Collet <rpms@famillecollet.com> 1.0-2.20131220gitf12a5f7
- backport for remi repo

* Mon Jan 06 2014 Shawn Iwinski <shawn.iwinski@gmail.com> 1.0-2.20131220gitf12a5f7
- Conditional %%{?dist}

* Mon Dec 23 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 1.0-1.20131220gitf12a5f7
- Initial package
