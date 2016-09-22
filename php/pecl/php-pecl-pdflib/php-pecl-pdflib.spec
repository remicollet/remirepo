# remirepo spec file for php-pecl-pdflib
#
# Copyright (c) 2006-2016 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%{?scl:          %scl_package        php-pecl-pdflib}

%global with_zts  0%{?__ztsphp:1}
%global pecl_name pdflib
%global extname   pdf
%if "%{php_version}" < "5.6"
%global ini_name  %{extname}.ini
%else
%global ini_name  40-%{extname}.ini
%endif

Summary:        Package for generating PDF files
Name:           %{?scl_prefix}php-pecl-pdflib
Version:        3.0.4
Release:        4%{?dist}%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}
# https://bugs.php.net/60396 ask license file
License:        PHP
Group:          Development/Languages
URL:            http://pecl.php.net/package/pdflib

Source0:        http://pecl.php.net/get/pdflib-%{version}.tgz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  %{?scl_prefix}php-devel
BuildRequires:  %{?scl_prefix}php-pear
BuildRequires:  pdflib-lite-devel

Requires:       %{?scl_prefix}php(zend-abi) = %{php_zend_api}
Requires:       %{?scl_prefix}php(api) = %{php_core_api}
%{?_sclreq:Requires: %{?scl_prefix}runtime%{?_sclreq}%{?_isa}}

Provides:       %{?scl_prefix}php-%{pecl_name}               = %{version}
Provides:       %{?scl_prefix}php-%{pecl_name}%{?_isa}       = %{version}
Provides:       %{?scl_prefix}php-pecl(%{pecl_name})         = %{version}
Provides:       %{?scl_prefix}php-pecl(%{pecl_name})%{?_isa} = %{version}
%if "%{?scl_prefix}" != "%{?sub_prefix}"
Provides:       %{?scl_prefix}php-pecl-%{pecl_name}          = %{version}-%{release}
Provides:       %{?scl_prefix}php-pecl-%{pecl_name}%{?_isa}  = %{version}-%{release}
%endif

%if 0%{?fedora} < 20 && 0%{?rhel} < 7
# Filter private shared
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}
%endif

%if "%{?vendor}" == "Remi Collet" && 0%{!?scl:1}
# Other third party repo stuff
Obsoletes:     php53-pecl-%{pecl_name}
Obsoletes:     php53u-pecl-%{pecl_name}
Obsoletes:     php54-pecl-%{pecl_name}
Obsoletes:     php54w-pecl-%{pecl_name}
%if "%{php_version}" > "5.5"
Obsoletes:     php55u-pecl-%{pecl_name}
Obsoletes:     php55w-pecl-%{pecl_name}
%endif
%if "%{php_version}" > "5.6"
Obsoletes:     php56u-pecl-%{pecl_name}
Obsoletes:     php56w-pecl-%{pecl_name}
%endif
%endif


%description
This PHP extension wraps the PDFlib programming library
for processing PDF on the fly.

More info on how to use PDFlib with PHP can be found at
http://www.pdflib.com/developer-center/technical-documentation/php-howto

Package built for PHP %(%{__php} -r 'echo PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')%{?scl: as Software Collection (%{scl} by %{?scl_vendor}%{!?scl_vendor:rh})}.


%prep
%setup -c -q

# Check version
extver=$(sed -n '/#define PHP_PDFLIB_VERSION/{s/.* "//;s/".*$//;p}' %{pecl_name}-%{version}/php_pdflib.h)
if test "x${extver}" != "x%{version}"; then
   : Error: Upstream version is ${extver}, expecting %{version}.
   exit 1
fi

%if %{with_zts}
cp -pr %{pecl_name}-%{version} %{pecl_name}-zts
%endif

# Create the config file
cat > %{ini_name} << 'EOF'
; Enable PDFlib extension module
extension=%{extname}.so
EOF


%build
cd %{pecl_name}-%{version}
%{_bindir}/phpize
%configure --with-php-config=%{_bindir}/php-config
make %{?_smp_mflags}

%if %{with_zts}
cd ../%{pecl_name}-zts
%{_bindir}/zts-phpize
%configure --with-php-config=%{_bindir}/zts-php-config
make %{?_smp_mflags}
%endif


%install
rm -rf %{buildroot}

make -C %{pecl_name}-%{version} install-modules INSTALL_ROOT=%{buildroot}

# Drop in the bit of configuration
install -D -m 644 %{ini_name} %{buildroot}%{php_inidir}/%{ini_name}

# Install XML package description
install -D -m 644 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml

%if %{with_zts}
make -C %{pecl_name}-zts        install-modules INSTALL_ROOT=%{buildroot}
install -D -m 644 %{ini_name} %{buildroot}%{php_ztsinidir}/%{ini_name}
%endif

# Test & Documentation
cd %{pecl_name}-%{version}
for i in $(grep 'role="doc"' ../package.xml | sed -e 's/^.*name="//;s/".*$//')
do install -Dpm 644 $i %{buildroot}%{pecl_docdir}/%{pecl_name}/$i
done


%check
%{__php} -n \
    -d extension_dir=%{pecl_name}-%{version}/modules \
    -d extension=%{extname}.so \
    -m | grep -i %{extname}

%if %{with_zts}
%{__ztsphp} -n \
    -d extension_dir=%{pecl_name}-zts/modules \
    -d extension=%{extname}.so \
    -m | grep -i %{extname}
%endif


%if 0%{?fedora} < 24
# when pear installed alone, after us
%triggerin -- %{?scl_prefix}php-pear
if [ -x %{__pecl} ] ; then
    %{pecl_install} %{pecl_xmldir}/%{name}.xml >/dev/null || :
fi

# posttrans as pear can be installed after us
%posttrans
if [ -x %{__pecl} ] ; then
    %{pecl_install} %{pecl_xmldir}/%{name}.xml >/dev/null || :
fi

%postun
if [ $1 -eq 0 -a -x %{__pecl} ] ; then
    %{pecl_uninstall} %{pecl_name} >/dev/null || :
fi
%endif


%clean
rm -rf %{buildroot}


%files
%defattr(-, root, root, -)
%doc %{pecl_docdir}/%{pecl_name}
%{pecl_xmldir}/%{name}.xml

%config(noreplace) %{php_inidir}/%{ini_name}
%{php_extdir}/%{extname}.so

%if %{with_zts}
%config(noreplace) %{php_ztsinidir}/%{ini_name}
%{php_ztsextdir}/%{extname}.so
%endif


%changelog
* Tue Mar  8 2016 Remi Collet <remi@fedoraproject.org> - 3.0.4-4
- adapt for F24

* Wed Dec 24 2014 Remi Collet <remi@fedoraproject.org> - 3.0.4-3.1
- Fedora 21 SCL mass rebuild

* Mon Aug 25 2014 Remi Collet <remi@fedoraproject.org> - 3.0.4-3
- allow SCL build

* Wed Apr 16 2014 Remi Collet <remi@fedoraproject.org> - 3.0.4-2
- add numerical prefix to extension configuration file (php 5.6)

* Thu Jan 16 2014 Remi Collet <remi@fedoraproject.org> - 3.0.4-1
- Update to 3.0.4 (stable)

* Mon Dec 30 2013 Remi Collet <remi@fedoraproject.org> - 3.0.3-1
- Update to 3.0.3 (stable)

* Thu Dec 19 2013 Remi Collet <remi@fedoraproject.org> - 3.0.2-1
- Update to 3.0.2 (stable)
- move doc to pecl_docdir

* Thu Jul 25 2013 Remi Collet <remi@fedoraproject.org> - 3.0.1-1
- Update to 3.0.1

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
