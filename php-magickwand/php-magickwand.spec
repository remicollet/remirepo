%global php_apiver	%((echo 0; php -i 2>/dev/null | sed -n 's/^PHP API => //p') | tail -1)
%{!?php_extdir:		%{expand: %%global php_extdir %(php-config --extension-dir)}}

Summary:	PHP API for ImageMagick
Name:		php-magickwand
Version:	1.0.8
Release:	8%{?dist}
License:	ImageMagick
Group:		Development/Languages
# Only latest version is always kept on: http://www.magickwand.org/download/php/
Source0:	http://image_magick.veidrodis.com/image_magick/php/MagickWandForPHP-%{version}.tar.bz2
Source1:	magickwand.ini
URL:		http://www.magickwand.org/
BuildRequires:	php-devel >= 4.3.0, ImageMagick-devel >= 6.4.0, autoconf, automake, libtool
%if %{?php_zend_api}0
Requires:	php(zend-abi) = %{php_zend_api}
Requires:	php(api) = %{php_core_api}
%else
Requires:	php-api = %{php_apiver}
%endif
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
MagickWand for PHP is a native PHP interface to the new
ImageMagick MagickWand API. It is an almost complete port
of the ImageMagick C API, excluding some X-Server related
functionality and progress monitoring.

%prep
%setup -q -n MagickWandForPHP-%{version}
export PHP_RPATH=no
phpize
%configure

%build
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install-modules INSTALL_ROOT=$RPM_BUILD_ROOT
install -D -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/php.d/magickwand.ini

# Fix incorrect end-of-line encoding
sed -i 's/\r//' README

%check
make test

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc AUTHOR ChangeLog CREDITS LICENSE README TODO
%{php_extdir}/magickwand.so
%config(noreplace) %{_sysconfdir}/php.d/magickwand.ini

%changelog
* Wed Sep 29 2010 jkeating - 1.0.8-8
- Rebuilt for gcc bug 634757

* Mon Sep 20 2010 Tom "spot" Callaway <tcallawa@redhat.com> 1.0.8-7
- rebuild for new ImageMagick

* Tue Feb 09 2010 Robert Scheck <robert@fedoraproject.org> 1.0.8-6
- Rebuild against ImageMagick 6.6.0.2

* Tue Aug 11 2009 Ville Skyttä <ville.skytta@iki.fi> - 1.0.8-5
- Use bzipped upstream tarball.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jul 13 2009 Remi Collet <Fedora@FamilleCollet.com> 1.0.8-3
- rebuild for new PHP 5.3.0 ABI (20090626)
- better PHP ABI check
- use php_extdir

* Tue Mar 10 2009 Robert Scheck <robert@fedoraproject.org> 1.0.8-2
- Rebuild against ImageMagick 6.4.9.6

* Mon Feb 23 2009 Robert Scheck <robert@fedoraproject.org> 1.0.8-1
- Upgrade to 1.0.8
- Rebuild against gcc 4.4 and rpm 4.6

* Sat May 17 2008 Robert Scheck <robert@fedoraproject.org> 1.0.7-2
- Rebuild against ImageMagick 6.4.0.10

* Sun Apr 27 2008 Robert Scheck <robert@fedoraproject.org> 1.0.7-1
- Upgrade to 1.0.7

* Thu Feb 14 2008 Robert Scheck <robert@fedoraproject.org> 1.0.6-2
- Require ImageMagick >= 6.3.7.10 to avoid breakage (#432794)

* Sat Feb 09 2008 Robert Scheck <robert@fedoraproject.org> 1.0.6-1
- Upgrade to 1.0.6

* Fri Dec 28 2007 Robert Scheck <robert@fedoraproject.org> 1.0.5-1
- Upgrade to 1.0.5 (#229401)

* Fri Dec 28 2007 Robert Scheck <robert@fedoraproject.org> 1.0.1-1
- Upgrade to 1.0.1 (#394961)

* Fri Dec 28 2007 Robert Scheck <robert@fedoraproject.org> 0.1.9-1
- Upgrade to 0.1.9

* Wed Aug 29 2007 Robert Scheck <robert@fedoraproject.org> 0.1.8-4
- Updated the license tag according to the guidelines

* Sun Sep 03 2006 Robert Scheck <robert@fedoraproject.org> 0.1.8-3
- Rebuild for Fedora Core 6

* Sat Jun 17 2006 Robert Scheck <robert@fedoraproject.org> 0.1.8-2
- Changes to match with Fedora Packaging Guidelines (#194470)

* Mon May 29 2006 Robert Scheck <robert@fedoraproject.org> 0.1.8-1
- Upgrade to 0.1.8
- Initial spec file for Fedora Core
