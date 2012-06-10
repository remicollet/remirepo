%{!?__pecl:     %{expand: %%global __pecl     %{_bindir}/pecl}}
%{!?php_extdir: %{expand: %%global php_extdir %(php-config --extension-dir)}}

%global pecl_name zip


Summary:      A zip management extension
Summary(fr):  Une extension de gestion des ZIP
Name:         php-pecl-zip
Version:      1.10.2
Release:      1%{?dist}
License:      PHP
Group:        Development/Languages
URL:          http://pecl.php.net/package/zip

Source:       http://pecl.php.net/get/%{pecl_name}-%{version}.tgz
# http://svn.php.net/viewvc/pecl/zip/trunk/tests/bug38943.inc?view=co
# http://pecl.php.net/bugs/22604 - missing file
Source1:      bug38943.inc
Source2:      xml2changelog

Patch0:       zip-systemlibzip.patch

BuildRoot:    %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: php-devel, zlib-devel
BuildRequires: php-pear(PEAR) >= 1.7.0
BuildRequires: libzip2-devel

Requires(post): %{__pecl}
Requires(postun): %{__pecl}
Requires:     php(zend-abi) = %{php_zend_api}
Requires:     php(api) = %{php_core_api}
Provides:     php-pecl(%{pecl_name}) = %{version}, php-pecl(%{pecl_name})%{?_isa} = %{version}
Provides:     php-%{pecl_name} = %{version}-%{release}, php-%{pecl_name}%{?_isa} = %{version}-%{release}

%description
Zip is an extension to create and read zip files.

%description -l fr
Zip est une extension pour créer et lire les archives au format ZIP.


%prep 
%setup -c -q

%{_bindir}/php -n %{SOURCE2} package.xml | tee CHANGELOG | head -n 10
%{__cp} %{SOURCE1} %{pecl_name}-%{version}/tests/bug38943.inc

cd %{pecl_name}-%{version}
%patch0 -p1 -b .systemlibzip


%build
cd %{pecl_name}-%{version}
phpize
%configure --with-libzip-dir=%{_prefix}
%{__make} %{?_smp_mflags}


%install
cd %{pecl_name}-%{version}
%{__rm} -rf %{buildroot}
%{__make} install INSTALL_ROOT=%{buildroot}

# Drop in the bit of configuration
%{__mkdir_p} %{buildroot}%{_sysconfdir}/php.d
%{__cat} > %{buildroot}%{_sysconfdir}/php.d/%{pecl_name}.ini << 'EOF'
; Enable ZIP extension module
extension=%{pecl_name}.so
EOF

# Install XML package description
%{__mkdir_p} %{buildroot}%{pecl_xmldir}
%{__install} -m 644 ../package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml


%check
cd %{pecl_name}-%{version}
php --no-php-ini \
    --define extension_dir=modules \
    --define extension=%{pecl_name}.so \
    --modules | grep %{pecl_name}

TEST_PHP_ARGS="-n -d extension_dir=$PWD/modules -d extension=%{pecl_name}.so" \
   REPORT_EXIT_STATUS=1 \
   NO_INTERACTION=1 \
   TEST_PHP_EXECUTABLE=%{_bindir}/php \
   %{_bindir}/php \
   run-tests.php


%clean
%{__rm} -rf %{buildroot}


%post
%{pecl_install} %{pecl_xmldir}/%{name}.xml >/dev/null || :


%postun
if [ $1 -eq 0 ] ; then
    %{pecl_uninstall} %{pecl_name} >/dev/null || :
fi


%files
%defattr(-, root, root, -)
# http://pecl.php.net/bugs/22603 - License file
%doc CHANGELOG 
%doc %{pecl_name}-%{version}/CREDITS
%doc %{pecl_name}-%{version}/examples
%config(noreplace) %{_sysconfdir}/php.d/%{pecl_name}.ini
%{php_extdir}/%{pecl_name}.so
%{pecl_xmldir}/%{name}.xml


%changelog
* Sun Mar 20 2011 Remi Collet <Fedora@FamilleCollet.com> 1.10.2-1
- Version 1.10.2 (stable) - API 2.0.0 (stable)
- mostly rewriten for latest PHP Guidelines

* Thu Jun 07 2007 Remi Collet <Fedora@FamilleCollet.com> 1.8.10-1
- update to 1.8.10

* Sun Mar 25 2007 Remi Collet <Fedora@FamilleCollet.com> 1.8.8-1
- update to 1.8.8

* Mon Feb 26 2007 Remi Collet <Fedora@FamilleCollet.com> 1.8.6-1
- update to 1.8.6

* Sat Feb 24 2007 Remi Collet <Fedora@FamilleCollet.com> 1.8.5-1
- update to 1.8.5
- requires php(zend-abi) and php(api) when available

* Sat Dec 02 2006 Remi Collet <Fedora@FamilleCollet.com> 1.8.2-1
- update to 1.8.2

* Thu Nov 02 2006 Remi Collet <Fedora@FamilleCollet.com> 1.8.0-1
- update to 1.8.0

* Tue Oct 24 2006 Remi Collet <Fedora@FamilleCollet.com> 1.7.5-1
- update to 1.7.5

* Wed Sep 27 2006 Remi Collet <Fedora@FamilleCollet.com> 1.7.4-1
- update to 1.7.4

* Sun Sep 17 2006 Remi Collet <Fedora@FamilleCollet.com> 1.7.3-1
- update to 1.7.3
- remove PECL from sumnary
- change to %%setup -c -q
- add generated CHANGELOG to %%doc

* Mon Aug 28 2006 Remi Collet <Fedora@FamilleCollet.com> 1.7.2-2
- rebuild for FE6

* Sun Aug 27 2006 Remi Collet <Fedora@FamilleCollet.com> 1.7.2-1
- update to 1.7.2

* Sat Aug 26 2006 Remi Collet <Fedora@FamilleCollet.com> 1.7.1-2
- use php_zip.c version 1.73 from CVS 
- see http://pecl.php.net/bugs/bug.php?id=8564

* Fri Aug 25 2006 Remi Collet <Fedora@FamilleCollet.com> 1.7.1-1
- update to 1.7.1
- change macros to conform to PHP Guidelines

* Sun Aug 20 2006 Remi Collet <Fedora@FamilleCollet.com> 1.7.0-1
- update to 1.7.0

* Sun Jul 30 2006 Remi Collet <Fedora@FamilleCollet.com> 1.6.0-1
- update to 1.6.0 (Big change : Rename Class Zip to ZipArchive)

* Sun Jul 16 2006 Remi Collet <Fedora@FamilleCollet.com> 1.5.0-1
- update to 1.5.0
- Requires: php-api

* Thu Jun 29 2006 Remi Collet <Fedora@FamilleCollet.com> 1.4.1-1
- update to 1.4.1
- bundle the v3.01 PHP LICENSE file
- Suppr. Requires zip, Add Provides php-pecl(zip) and php-zip
- change defattr

* Fri Apr 28 2006 Remi Collet <Fedora@FamilleCollet.com> 1.3.1-2
- Add zlib(devel) to Requires

* Thu Apr 27 2006 Remi Collet <Fedora@FamilleCollet.com> 1.3.1-1
- update to 1.3.1

* Wed Apr 26 2006 Remi Collet <Fedora@FamilleCollet.com> 1.2.3-1
- initial RPM for extras
- add french summary & description
- add examples to doc.

* Tue Apr 11 2006 Remi Collet <RPMS@FamilleCollet.com> 1.2.3-1
- initial RPM

