%global php_apiver %((echo 0; php -i 2>/dev/null | sed -n 's/^PHP API => //p') | tail -1)

Summary:	PHP API for GNU LibIDN
Name:		php-idn
Version:	1.2c
Release:	6%{?dist}
License:	GPLv2+
Group:		Development/Languages
Source0:	http://php-idn.bayour.com/idn_%{version}.tar.gz
Source1:	idn.ini

Patch0:         idn-php54.patch

URL:		http://php-idn.bayour.com/

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	php-devel >= 4.3.0, libidn-devel >= 0.4.0, autoconf, automake, libtool

Requires:	php(zend-abi) = %{php_zend_api}
Requires:	php(api) = %{php_core_api}
Requires:	php-intl%{?_isa}

# Filter private shared
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}


%description
This is the PHP API for the GNU LibIDN software
made by Simon Josefsson. It's intention is to
have international characters in the DNS system.


%prep
%setup -q -c

cd idn-%{version}
%patch0 -p1 -b .php54
cd ..

cp -pr idn-%{version} idn-zts


%build
export PHP_RPATH=no

cd idn-%{version}
phpize
%configure  --with-php-config=%{_bindir}/php-config
make %{?_smp_mflags}

cd ../idn-zts
zts-phpize
%configure  --with-php-config=%{_bindir}/zts-php-config
make %{?_smp_mflags}


%install
rm -rf %{buildroot}
make -C idn-%{version} \
     install-modules INSTALL_ROOT=%{buildroot}
make -C idn-zts \
     install-modules INSTALL_ROOT=%{buildroot}

install -D -p -m 644 %{SOURCE1} %{buildroot}%{php_inidir}/idn.ini
install -D -p -m 644 %{SOURCE1} %{buildroot}%{php_ztsinidir}/idn.ini


%check
# No test provided by upstream, so
# minimal load test for the PHP extension
%{__php} -n \
    -d extension_dir=idn-%{version}/modules \
    -d extension=idn.so -m \
    | grep idn
%{__ztsphp} -n \
    -d extension_dir=idn-zts/modules \
    -d extension=idn.so -m \
    | grep idn


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc idn-%{version}/{CHANGES,COPYRIGHT,CREDITS,README.documentation,THANX_TO,idn.php}
%config(noreplace) %{php_inidir}/idn.ini
%config(noreplace) %{php_ztsinidir}/idn.ini
%{php_extdir}/idn.so
%{php_ztsextdir}/idn.so


%changelog
* Tue Jan  8 2013 Remi Collet <remi@fedoraproject.org> - 1.2c-6
- also build ZTS extension

* Wed Dec 28 2011 Remi Collet <remi@fedoraproject.org> - 1.2c-3
- build against php 5.4 with patch
- add minimal load test

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
