# remirepo spec file for php-php-gettext, from:
#
# Fedora spec file for php-php-gettext
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

Summary:	Gettext emulation in PHP
Name:		php-php-gettext
Version:	1.0.12
Release:	1%{?dist}
License:	GPLv2+
Group:		Development/Libraries
URL:		https://launchpad.net/php-gettext
Source0:	http://launchpad.net/php-gettext/trunk/%{version}/+download/php-gettext-%{version}.tar.gz
Patch0:		php-php-gettext-1.0.11-php7.patch
Requires:	php-common
Requires:	php-mbstring
Obsoletes:	php-gettext < 1.0.11-5
Obsoletes:	php53-php-gettext
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
This library provides PHP functions to read MO files even when gettext is 
not compiled in or when appropriate locale is not present on the system.

%prep
%setup -q -n php-gettext-%{version}
%patch0 -p1 -b .php7

%build

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_datadir}/php/gettext/
install -p -m 644 gettext.php streams.php gettext.inc $RPM_BUILD_ROOT%{_datadir}/php/gettext/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc README AUTHORS
%{_datadir}/php/gettext/

%changelog
* Tue Nov 29 2016 Robert Scheck <robert@fedoraproject.org> 1.0.12-1
- Upgrade to 1.0.12 (#1367462)

* Fri Sep 04 2015 Robert Scheck <robert@fedoraproject.org> 1.0.11-12
- Added a patch for compatibility with PHP 7

* Mon Sep  3 2012 Remi Collet <RPMS@FamilleCollet.com> 1.0.11-4
- obsoletes php53-php-gettext

* Mon Sep 19 2011 Robert Scheck <robert@fedoraproject.org> 1.0.11-3
- Renamed package from php-gettext to php-php-gettext (#727000)

* Mon Aug 01 2011 Robert Scheck <robert@fedoraproject.org> 1.0.11-2
- Moved library data to /usr/share/php/gettext
- Added runtime dependency to php-mbstring package

* Sun Jul 31 2011 Robert Scheck <robert@fedoraproject.org> 1.0.11-1
- Upgrade to 1.0.11

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> 1.0.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Dec 06 2009 David Nalley <david@gnsa.us> 1.0.9-2
- corrected license field 

* Sun Dec 06 2009 David Nalley <david@gnsa.us> 1.0.9-1
- Initial Packaging
