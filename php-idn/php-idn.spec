%global php_apiver %((echo 0; php -i 2>/dev/null | sed -n 's/^PHP API => //p') | tail -1)

Summary:	PHP API for GNU LibIDN
Name:		php-idn
Version:	1.2c
Release:	3%{?dist}
License:	GPLv2+
Group:		Development/Languages
Source0:	http://php-idn.bayour.com/idn_%{version}.tar.gz
Source1:	idn.ini
URL:		http://php-idn.bayour.com/
BuildRequires:	php-devel >= 4.3.0, libidn-devel >= 0.4.0, autoconf, automake, libtool
%if 0%{?rhel}%{?fedora} > 4
%if 0%{?php_zend_api:1}
Requires:	php(zend-abi) = %{php_zend_api}, php(api) = %{php_core_api}
%else
Requires:	php-api = %{php_apiver}
%endif
%if 0%(echo '%{?php_zend_api}' | sed -e 's/-.*//') >= 20090626
Requires:	php-intl
%endif
%endif
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
This is the PHP API for the GNU LibIDN software
made by Simon Josefsson. It's intention is to
have international characters in the DNS system.

%prep
%setup -q -n idn-%{version}
export PHP_RPATH=no
phpize
%configure

%build
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install-modules INSTALL_ROOT=$RPM_BUILD_ROOT
install -D -p -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/php.d/idn.ini

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc CHANGES COPYRIGHT CREDITS README.documentation THANX_TO idn.php
%if 0%{?rhel}%{?fedora} > 4
%{_libdir}/php/modules/idn.so
%else
%{_libdir}/php4/idn.so
%endif
%config(noreplace) %{_sysconfdir}/php.d/idn.ini

%changelog
* Sat Jun 25 2011 Robert Scheck <robert@fedoraproject.org> 1.2c-3
- Changed %%php_zend_api macro usage (#716054)

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2c-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Apr 06 2010 Robert Scheck <robert@fedoraproject.org> 1.2c-1
- Upgrade to 1.2c (includes a minor fix for the 1.2 release)

* Fri Jul 31 2009 Remi Collet <Fedora@FamilleCollet.com> 1.2-7
- rebuild for new PHP 5.3.0 ABI (20090626)
- better PHP ABI check
- use php_extdir
- patch for PHP 5.3.0 provided functions

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Feb 23 2009 Robert Scheck <robert@fedoraproject.org> 1.2-5
- Rebuilt against gcc 4.4 and rpm 4.6

* Sun Feb 10 2008 Robert Scheck <robert@fedoraproject.org> 1.2-4
- Rebuilt against gcc 4.3

* Wed Aug 29 2007 Robert Scheck <robert@fedoraproject.org> 1.2-3
- Updated the license tag according to the guidelines

* Mon May 07 2007 Robert Scheck <robert@fedoraproject.org> 1.2-2
- Rebuild

* Fri Nov 24 2006 Robert Scheck <robert@fedoraproject.org> 1.2-1
- Upgrade to 1.2b (includes a minor fix for the 1.2 release)

* Sun Sep 03 2006 Robert Scheck <robert@fedoraproject.org> 1.1-7
- Rebuild for Fedora Core 6

* Sat Jun 17 2006 Robert Scheck <robert@fedoraproject.org> 1.1-6
- Changes to match with Fedora Packaging Guidelines (#194479)

* Sat Mar 11 2006 Robert Scheck <robert@fedoraproject.org> 1.1-5
- Rebuilt against PHP 5.1.2 and gcc 4.1
- Require the virtual php-api instead the current PHP version

* Fri Sep 16 2005 Robert Scheck <robert@fedoraproject.org> 1.1-4
- Rebuilt against PHP 5.0.5 and glibc 2.4

* Wed Apr 06 2005 Robert Scheck <robert@fedoraproject.org> 1.1-3
- Rebuilt against PHP 5.0.4

* Mon Mar 21 2005 Robert Scheck <robert@fedoraproject.org> 1.1-2
- Rebuilt against gcc 4.0

* Sun Dec 19 2004 Robert Scheck <robert@fedoraproject.org> 1.1-1
- Rebuilt against PHP 5.0.3
- Upgrade to 1.1 and some spec file cleanup

* Sat Dec 18 2004 Robert Scheck <robert@fedoraproject.org> 1.0-5
- Improved patch for rebuilding with PHP 4 and 5

* Sat Nov 20 2004 Robert Scheck <robert@fedoraproject.org> 1.0-4
- Rebuilt against PHP 5.0.2

* Fri Sep 24 2004 Robert Scheck <robert@fedoraproject.org> 1.0-3
- Rebuilt against PHP 4.3.9

* Wed Jul 14 2004 Robert Scheck <robert@fedoraproject.org> 1.0-2
- Rebuilt against PHP 4.3.8

* Fri Jun 04 2004 Robert Scheck <robert@fedoraproject.org> 1.0-1
- Upgrade to 1.0

* Fri Apr 16 2004 Robert Scheck <robert@fedoraproject.org> 0.9-1
- Upgrade to 0.9
- Initial spec file for Red Hat Linux and Fedora Core
