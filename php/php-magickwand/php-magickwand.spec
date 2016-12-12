# spec file for php-magickwand
#
# Copyright (c) 2010-2016 Remi Collet
# Copyright (c) 2006-2010 Robert Scheck
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please, preserve the changelog entries
#

%{?scl:          %scl_package         php-magickwand}

%global pecl_name     magickwand
%global mainversion   1.0.9
%global patchlevel    2
%global with_zts      0%{!?_without_zts:%{?__ztsphp:1}}

# We don't really rely on upstream ABI
%global imbuildver %(pkg-config --silence-errors --modversion ImageMagick 2>/dev/null || echo 65536)

%if "%{php_version}" < "5.6"
%global ini_name    %{pecl_name}.ini
%else
%global ini_name    40-%{pecl_name}.ini
%endif

Summary:       PHP API for ImageMagick
Name:          %{?scl_prefix}php-magickwand
Version:       %{mainversion}%{?patchlevel:.%{patchlevel}}
Release:       10%{?dist}%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}
License:       ImageMagick
Group:         Development/Languages
URL:           http://www.magickwand.org/
# Only latest version is always kept on: http://www.magickwand.org/download/php/
Source0:       http://image_magick.veidrodis.com/image_magick/php/MagickWandForPHP-%{mainversion}%{?patchlevel:-%{patchlevel}}.tar.bz2
Source1:       magickwand.ini


BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: %{?scl_prefix}php-devel < 7
BuildRequires: autoconf, automake, libtool

Requires:      %{?scl_prefix}php(zend-abi) = %{php_zend_api}
Requires:      %{?scl_prefix}php(api) = %{php_core_api}
%{?_sclreq:Requires: %{?scl_prefix}runtime%{?_sclreq}%{?_isa}}

%if "%{?vendor}" == "Remi Collet"
# Ensure we use the more recent version from remi repo
%if 0%{?fedora} > 99
BuildRequires: ImageMagick-devel
Requires:      ImageMagick-libs%{?_isa}  >= %{imbuildver}
%else
BuildRequires: ImageMagick6-devel
Requires:      ImageMagick6-libs%{?_isa}  >= %{imbuildver}
%endif
%else
# From upstream documentation
BuildRequires: ImageMagick-devel >= 6.8.2
Requires:      ImageMagick-libs%{?_isa}  >= %{imbuildver}
%endif

%if "%{?vendor}" == "Remi Collet" && 0%{!?scl:1} && 0%{?rhel}
# Other third party repo stuff
Obsoletes:      php53-magickwand
Obsoletes:      php53u-magickwand
Obsoletes:      php54-magickwand
Obsoletes:      php54w-magickwand
%if "%{php_version}" > "5.5"
Obsoletes:      php55u-magickwand
Obsoletes:      php55w-magickwand
%endif
%if "%{php_version}" > "5.6"
Obsoletes:      php56u-magickwand
Obsoletes:      php56w-magickwand
%endif
%endif

%if 0%{?fedora} < 20 && 0%{?rhel} < 7
# Filter private shared
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}
%endif


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
%if %{with_zts}
cp -pr MagickWandForPHP-%{mainversion} MagickWandForPHP-%{mainversion}-zts
%endif


%build
export PHP_RPATH=no

cd MagickWandForPHP-%{mainversion}
%{_bindir}/phpize
%configure --with-php-config=%{_bindir}/php-config
make %{?_smp_mflags}

%if %{with_zts}
cd ../MagickWandForPHP-%{mainversion}-zts
%{_bindir}/zts-phpize
%configure --with-php-config=%{_bindir}/zts-php-config
make %{?_smp_mflags}
%endif

%install
rm -rf %{buildroot}
make -C MagickWandForPHP-%{mainversion}     install-modules INSTALL_ROOT=%{buildroot}
install -D -m 644 %{SOURCE1} %{buildroot}%{php_inidir}/%{ini_name}

%if %{with_zts}
make -C MagickWandForPHP-%{mainversion}-zts install-modules INSTALL_ROOT=%{buildroot}
install -D -m 644 %{SOURCE1} %{buildroot}%{php_ztsinidir}/%{ini_name}
%endif


%check
# simple module load test
%{__php} --no-php-ini \
    --define extension_dir=MagickWandForPHP-%{mainversion}/modules \
    --define extension=%{pecl_name}.so \
    --modules | grep %{pecl_name}

%if %{with_zts}
%{__ztsphp} --no-php-ini \
    --define extension_dir=MagickWandForPHP-%{mainversion}-zts/modules \
    --define extension=%{pecl_name}.so \
    --modules | grep %{pecl_name}
%endif


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc MagickWandForPHP-%{mainversion}/{AUTHOR,ChangeLog,CREDITS,LICENSE,README,TODO}

%config(noreplace) %{php_inidir}/%{ini_name}
%{php_extdir}/%{pecl_name}.so

%if %{with_zts}
%config(noreplace) %{php_ztsinidir}/%{ini_name}
%{php_ztsextdir}/%{pecl_name}.so
%endif


%changelog
* Sun Dec 11 2016 Remi Collet <remi@fedoraproject.org> - 1.0.9.2-10
- rebuild against ImageMagick6 (6.9.6-8)

* Wed Dec 24 2014 Remi Collet <remi@fedoraproject.org> - 1.0.9.2-8.1
- Fedora 21 SCL mass rebuild

* Mon Aug 25 2014 Remi Collet <rpms@famillecollet.com> - 1.0.9.2-8
- rebuild against new ImageMagick-last version 6.8.7-4

* Mon Aug 25 2014 Remi Collet <rcollet@redhat.com> - 1.0.9.2-8
- improve SCL build

* Mon Apr 14 2014 Remi Collet <rpms@famillecollet.com> - 1.0.9.2-7
- add numerical prefix to extension configuration file
- rebuild for ImageMagick

* Wed Mar 26 2014 Remi Collet <rpms@famillecollet.com> - 1.0.9.2-6
- allow SCL build

* Sat Nov  2 2013 Remi Collet <rpms@famillecollet.com> - 1.0.9.2-5
- rebuild against new ImageMagick-last version 6.8.7-4

* Sun Sep  8 2013 Remi Collet <rpms@famillecollet.com> - 1.0.9.2-4
- rebuild against new ImageMagick-last version 6.8.6-9

* Sun Jun  2 2013 Remi Collet <rpms@famillecollet.com> - 1.0.9.2-3
- rebuild against new ImageMagick-last version 6.8.5-9

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
