%{!?__pecl:     %{expand: %%global __pecl     %{_bindir}/pecl}}
%{!?php_inidir: %{expand: %%global php_inidir %{_sysconfdir}/php.d}}

%global pecl_name pdflib
%global extname   pdf

Summary:        Package for generating PDF files
Summary(fr):    Extension pour générer des fichiers PDF
Name:           php-pecl-pdflib
Version:        2.1.10
Release:        1%{?dist}.1
# https://bugs.php.net/60396 ask license file
License:        PHP
Group:          Development/Languages
URL:            http://pecl.php.net/package/pdflib

Source:         http://pecl.php.net/get/pdflib-%{version}.tgz
Source2:        xml2changelog

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  php-devel
BuildRequires:  pdflib-lite-devel
BuildRequires:  php-pear

Requires(post): %{__pecl}
Requires(postun): %{__pecl}
Requires:       php(zend-abi) = %{php_zend_api}
Requires:       php(api) = %{php_core_api}

Provides:       php-%{pecl_name} = %{version}%{?prever}
Provides:       php-%{pecl_name}%{?_isa} = %{version}%{?prever}
Provides:       php-pecl(%{pecl_name}) = %{version}%{?prever}
Provides:       php-pecl(%{pecl_name})%{?_isa} = %{version}%{?prever}

# Filter private shared
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}

# Other third party repo stuff
Obsoletes:     php53-pecl-%{pecl_name}
Obsoletes:     php53u-pecl-%{pecl_name}
%if "%{php_version}" > "5.4"
Obsoletes:     php54-pecl-%{pecl_name}
%endif
%if "%{php_version}" > "5.5"
Obsoletes:     php55-pecl-%{pecl_name}
%endif


%description
This PHP extension wraps the PDFlib programming library
for processing PDF on the fly.

More info on how to use PDFlib with PHP can be found at
http://www.pdflib.com/developer-center/technical-documentation/php-howto


%description -l fr
Cette extension PHP fournit une interface sur la bibliothèque de développement
PDFlib pour générer des fichiers PDF à la volée.

Plus d'informations sur l'utilisation de PDFlib avec PHP sur
http://www.pdflib.com/developer-center/technical-documentation/php-howto


%prep 
%setup -c -q
%{_bindir}/php %{SOURCE2} package.xml >CHANGELOG

sed -e /PHP_PDFLIB_VERSION/s/2.1.9/%{version}/ \
    -i %{pecl_name}-%{version}/php_pdflib.h

# Check version
extver=$(sed -n '/#define PHP_PDFLIB_VERSION/{s/.* "//;s/".*$//;p}' %{pecl_name}-%{version}/php_pdflib.h)
if test "x${extver}" != "x%{version}"; then
   : Error: Upstream version is ${extver}, expecting %{version}.
   exit 1
fi

cp -pr %{pecl_name}-%{version} %{pecl_name}-zts

# Create the config file
cat > %{extname}.ini << 'EOF'
; Enable PDFlib extension module
extension=%{extname}.so
EOF


%build
cd %{pecl_name}-%{version}
%{_bindir}/phpize
%configure --with-php-config=%{_bindir}/php-config
make %{?_smp_mflags}

%if 0%{?__ztsphp:1}
cd ../%{pecl_name}-zts
%{_bindir}/zts-phpize
%configure --with-php-config=%{_bindir}/zts-php-config
make %{?_smp_mflags}
%endif


%install
rm -rf %{buildroot}

make -C %{pecl_name}-%{version} install-modules INSTALL_ROOT=%{buildroot}

# Drop in the bit of configuration
install -D -m 644 %{extname}.ini %{buildroot}%{php_inidir}/%{extname}.ini

# Install XML package description
install -D -m 644 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml

%if 0%{?__ztsphp:1}
make -C %{pecl_name}-zts        install-modules INSTALL_ROOT=%{buildroot}
install -D -m 644 %{extname}.ini %{buildroot}%{php_ztsinidir}/%{extname}.ini
%endif


%check
%{_bindir}/php -n \
    -d extension_dir=%{pecl_name}-%{version}/modules \
    -d extension=%{extname}.so \
    -m | grep %{extname}

%if 0%{?__ztsphp:1}
%{__ztsphp} -n \
    -d extension_dir=%{pecl_name}-zts/modules \
    -d extension=%{extname}.so \
    -m | grep %{extname}
%endif


%post
%{pecl_install} %{pecl_xmldir}/%{name}.xml >/dev/null || :


%postun
if [ $1 -eq 0 ] ; then
    %{pecl_uninstall} %{pecl_name} >/dev/null || :
fi


%clean
rm -rf %{buildroot}


%files
%defattr(-, root, root, -)
%doc CHANGELOG %{pecl_name}-%{version}/CREDITS
%config(noreplace) %{php_inidir}/%{extname}.ini
%{php_extdir}/%{extname}.so
%{pecl_xmldir}/%{name}.xml

%if 0%{?__ztsphp:1}
%config(noreplace) %{php_ztsinidir}/%{extname}.ini
%{php_ztsextdir}/%{extname}.so
%endif


%changelog
* Tue Apr 09 2013 Remi Collet <remi@fedoraproject.org> - 2.1.10-1
- Update to 2.1.10

* Wed Mar 20 2013 Remi Collet <RPMS@FamilleCollet.com> 2.1.9-2
- cleanups

* Sat Jun 09 2012 Remi Collet <RPMS@FamilleCollet.com> 2.1.9-1
- update to 2.1.9

* Sun Nov 27 2011 Remi Collet <RPMS@FamilleCollet.com> 2.1.8-3
- php 5.4 build
- add ZTS extension
- add patch for PHP 5.4 https://bugs.php.net/60397
- request upstream to provides LICENSE file https://bugs.php.net/60396

* Sat Jul 23 2011 Remi Collet <rpmfusion@FamilleCollet.com> 2.1.8-2.1
- fix %%check (php 5.1 doesnt have --modules)

* Sat Jul 23 2011 Remi Collet <rpmfusion@FamilleCollet.com> 2.1.8-2
- fix private-shared-object-provides rpmlint warning
- fix macro usage
- add %%check, minimal load test

* Thu May 06 2010 Remi Collet <rpmfusion@FamilleCollet.com> 2.1.8-1
- update to 2.1.8

* Sat Oct 24 2009 Remi Collet <rpmfusion@FamilleCollet.com> 2.1.7-2
- rebuild

* Tue Jul 14 2009 Remi Collet <rpmfusion@FamilleCollet.com> 2.1.7-1
- update to 2.1.7, rebuild against php 5.3.0

* Sun Mar 29 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.1.6-2
- rebuild for new F11 features

* Thu Mar 19 2009 Remi Collet <RPMS@FamilleCollet.com> 2.1.6-1
- update to 2.1.6

* Sun Sep 28 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info - 2.1.5-2
- rebuild

* Fri Mar 28 2008 Remi Collet <RPMS@FamilleCollet.com> 2.1.5-2
- rebuild against pdflib-lite-7.0.3

* Sat Mar 15 2008 Remi Collet <RPMS@FamilleCollet.com> 2.1.5-1
- update to 2.1.5

* Tue Sep 25 2007 Remi Collet <RPMS@FamilleCollet.com> 2.1.4-2
- add missing BR php-pear

* Tue Sep 25 2007 Remi Collet <RPMS@FamilleCollet.com> 2.1.4-1
- update to 2.1.4
- convert package from v1 to v2
- register extension (new PHP Guidelines)
- remove License file (not provided upstream)

* Sat Mar 17 2007 Remi Collet <RPMS@FamilleCollet.com> 2.1.3-2
- rebuild againt pdflib-lite-7.0.1

* Fri Mar  9 2007 Remi Collet <RPMS@FamilleCollet.com> 2.1.3-1
- requires php(zend-abi) and php(api) when available
- update to 2.1.3

* Sat Dec 09 2006 Remi Collet <RPMS@FamilleCollet.com> 2.1.2-1
- initial spec for Livna
