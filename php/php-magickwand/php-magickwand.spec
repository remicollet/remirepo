%global pecl_name     magickwand
%global mainversion   1.0.9
%global patchlevel    2

# We don't really rely on upstream ABI
%global imbuildver %(pkg-config --silence-errors --modversion ImageMagick 2>/dev/null || echo 65536)

Summary:       PHP API for ImageMagick
Name:          php-magickwand
Version:       %{mainversion}%{?patchlevel:.%{patchlevel}}
Release:       2%{?dist}.1
License:       ImageMagick
Group:         Development/Languages
URL:           http://www.magickwand.org/
# Only latest version is always kept on: http://www.magickwand.org/download/php/
Source0:       http://image_magick.veidrodis.com/image_magick/php/MagickWandForPHP-%{mainversion}%{?patchlevel:-%{patchlevel}}.tar.bz2
Source1:       magickwand.ini


BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: php-devel
BuildRequires: autoconf, automake, libtool
%if 0%{?fedora} > 20
BuildRequires: ImageMagick-devel >= 6.8.2
Requires:      ImageMagick-libs  >= %{imbuildver}
%else
BuildRequires: ImageMagick-last-devel >= 6.8.2
Requires:      ImageMagick-last-libs  >= %{imbuildver}
%endif

Requires:      php(zend-abi) = %{php_zend_api}
Requires:      php(api) = %{php_core_api}

# Other third party repo stuff
Obsoletes:      php53-magickwand
Obsoletes:      php53u-magickwand
%if "%{php_version}" > "5.4"
Obsoletes:      php54-magickwand
%endif
%if "%{php_version}" > "5.5"
Obsoletes:      php55-magickwand
%endif

# Filter private shared
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}


%description
MagickWand for PHP is a native PHP interface to the new
ImageMagick MagickWand API. It is an almost complete port
of the ImageMagick C API, excluding some X-Server related
functionality and progress monitoring.

%prep
%setup -q -c

cd MagickWandForPHP-%{mainversion}

# fix version
sed -i -e /MAGICKWAND_VERSION/s/1.0.8/%{version}/ magickwand.h

# Check version
extver=$(sed -n '/#define MAGICKWAND_VERSION/{s/.* "//;s/".*$//;p}' magickwand.h)
if test "x${extver}" != "x%{version}"; then
   : Error: Upstream version is ${extver}, expecting %{version}.
   exit 1
fi

# Fix incorrect end-of-line encoding
sed -i 's/\r//' README

cd ..
cp -pr MagickWandForPHP-%{mainversion} MagickWandForPHP-%{mainversion}-zts


%build
export PHP_RPATH=no

cd MagickWandForPHP-%{mainversion}
%{_bindir}/phpize
%configure --with-php-config=%{_bindir}/php-config
make %{?_smp_mflags}

cd ../MagickWandForPHP-%{mainversion}-zts
%{_bindir}/zts-phpize
%configure --with-php-config=%{_bindir}/zts-php-config
make %{?_smp_mflags}


%install
rm -rf %{buildroot}
make -C MagickWandForPHP-%{mainversion}     install-modules INSTALL_ROOT=%{buildroot}
make -C MagickWandForPHP-%{mainversion}-zts install-modules INSTALL_ROOT=%{buildroot}

install -D -m 644 %{SOURCE1} %{buildroot}%{php_inidir}/%{pecl_name}.ini
install -D -m 644 %{SOURCE1} %{buildroot}%{php_ztsinidir}/%{pecl_name}.ini


%check
# simple module load test
%{__php} --no-php-ini \
    --define extension_dir=MagickWandForPHP-%{mainversion}/modules \
    --define extension=%{pecl_name}.so \
    --modules | grep %{pecl_name}

%{__ztsphp} --no-php-ini \
    --define extension_dir=MagickWandForPHP-%{mainversion}-zts/modules \
    --define extension=%{pecl_name}.so \
    --modules | grep %{pecl_name}


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc MagickWandForPHP-%{mainversion}/{AUTHOR,ChangeLog,CREDITS,LICENSE,README,TODO}
%config(noreplace) %{php_inidir}/%{pecl_name}.ini
%config(noreplace) %{php_ztsinidir}/%{pecl_name}.ini
%{php_extdir}/%{pecl_name}.so
%{php_ztsextdir}/%{pecl_name}.so


%changelog
* Sat Apr  6 2013 Remi Collet <rpms@famillecollet.com> 1.0.9.2-2
- rebuild against new ImageMagick-last version 6.8.4-6
- improve dependency on ImageMagick library

* Thu Mar 14 2013 Remi Collet <rpms@famillecollet.com> 1.0.9.2-1
- update to 1.0.9-2

* Wed Mar 13 2013 Remi Collet <rpms@famillecollet.com> 1.0.9-4
- rebuild against new ImageMagick-last version 6.8.3.9

* Thu Aug 16 2012 Remi Collet <rpms@famillecollet.com> 1.0.9-3
- rebuild against new ImageMagick-last version 6.7.8.10

* Fri Apr 27 2012 Remi Collet <rpms@famillecollet.com> 1.0.9-2
- fix macro usage

* Sat Nov 26 2011 Remi Collet <rpms@famillecollet.com> 1.0.9-2
- php 5.4 build

* Sat Nov 26 2011 Remi Collet <rpms@famillecollet.com> 1.0.9-1
- update to 1.0.9
- patch for php 5.4 and ZTS build

* Thu Oct 06 2011 Remi Collet <rpms@famillecollet.com> 1.0.8-10
- ZTS extension
- spec cleanups

* Fri Nov 26 2010 Remi Collet <rpms@famillecollet.com> 1.0.8-8
- rebuild against latest ImageMagick 6.6.5.10

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
