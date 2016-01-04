# remirepo spec file for php-libvirt
# With SCL stuff, from Fedora:
#
# Fedora spec file for php-libvirt
#
# Copyright (c) 2012-2016 Remi Collet
# Copyright (c) 2011 Michal Novotny
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please, preserve the changelog entries
#
%if 0%{?scl:1}
%if "%{scl}" == "rh-php56"
%global sub_prefix more-php56-
%else
%global sub_prefix %{scl_prefix}
%endif
%endif

%{?scl:          %scl_package        php-libvirt}
%{!?php_inidir:  %global php_inidir  %{_sysconfdir}/php.d}
%{!?__php:       %global __php       %{_bindir}/php}
%{!?_pkgdocdir:  %global _pkgdocdir  %{_docdir}/%{name}-%{version}}

%global  req_libvirt_version 1.2.8
%global  extname             libvirt-php
%if "%{php_version}" < "5.6"
%global ini_name             %{extname}.ini
%else
%global ini_name             40-%{extname}.ini
%endif

Name:          %{?sub_prefix}php-libvirt
Version:       0.5.1
Release:       1%{?dist}%{!?scl:%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}}
Summary:       PHP language binding for Libvirt

Group:         Development/Libraries
License:       PHP
URL:           http://libvirt.org/php
Source0:       http://libvirt.org/sources/php/libvirt-php-%{version}.tar.gz

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: %{?scl_prefix}php-devel
BuildRequires: libvirt-devel >= %{req_libvirt_version}
BuildRequires: libxml2-devel
BuildRequires: libxslt
BuildRequires: xhtml1-dtds

Requires:      %{?scl_prefix}php(zend-abi) = %{php_zend_api}
Requires:      %{?scl_prefix}php(api) = %{php_core_api}
%{?_sclreq:Requires: %{?scl_prefix}runtime%{?_sclreq}%{?_isa}}

## Compat SCL (rh-php56)
Provides:      %{?scl_prefix}php-libvirt         = %{version}-%{release}
Provides:      %{?scl_prefix}php-libvirt%{?_isa} = %{version}-%{release}

%if 0%{?fedora} < 20 && 0%{?rhel} < 7
# Filter shared private
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}
%endif


%description
PHP language bindings for Libvirt API. 
For more details see: http://www.libvirt.org/php/

Package built for PHP %(%{__php} -r 'echo PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')%{?scl: as Software Collection (%{scl} by %{?scl_vendor}%{!?scl_vendor:rh})}.


%package doc
Summary:       Document of php-libvirt
Group:         Development/Libraries
%if 0%{?fedora} >= 11 || 0%{?rhel} >= 6
BuildArch:     noarch
Requires:      %{name} = %{version}-%{release}
%else
Requires:      %{name}%{_isa} = %{version}-%{release}
%endif
## Compat SCL (rh-php56)
Provides:      %{?scl_prefix}php-libvirt-doc         = %{version}-%{release}
Provides:      %{?scl_prefix}php-libvirt-doc%{?_isa} = %{version}-%{release}

%description doc
PHP language bindings for Libvirt API. 
For more details see: http://www.libvirt.org/php/ http://www.php.net/

This package contain the document for php-libvirt.


%prep
%setup -q -n libvirt-php-%{version}

if ! pkg-config libvirt  --atleast-version=1.2.9
then
  sed -e '/VIR_DOMAIN_BLOCK_JOB_SPEED_BANDWIDTH_BYTES/d' \
      -i src/libvirt-php.c
fi

%build
%{?scl:. %{_scl_scripts}/enable}
%configure \
  --with-html-dir=%{_docdir} \
  --with-html-subdir=$(echo %{_pkgdocdir} | sed -e 's|^%{_docdir}/||')/html \
  --libdir=%{php_extdir}
make %{?_smp_mflags}


%install
%{?scl:. %{_scl_scripts}/enable}
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
install -pm 644 COPYING %{buildroot}%{_pkgdocdir}

if [ "%{extname}.ini" != "%{ini_name}" ]; then
  mv %{buildroot}%{php_inidir}/%{extname}.ini \
     %{buildroot}%{php_inidir}/%{ini_name}
fi

: Fix installation
rm %{buildroot}%{php_extdir}/%{extname}.la
rm %{buildroot}%{php_extdir}/%{extname}.so
rm %{buildroot}%{php_extdir}/%{extname}.so.0
mv %{buildroot}%{php_extdir}/%{extname}.so.0.0.0 %{buildroot}%{php_extdir}/%{extname}.so


%check
: simple module load test
%{?scl:. %{_scl_scripts}/enable}
php --no-php-ini \
    --define extension=%{buildroot}%{php_extdir}/%{extname}.so \
    --modules | grep libvirt


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%dir %{_pkgdocdir}
%{!?_licensedir:%global license %%doc}
%license %{_pkgdocdir}/COPYING
%{php_extdir}/%{extname}.so
%config(noreplace) %{php_inidir}/%{ini_name}

%files doc
%defattr(-,root,root,-)
%{_pkgdocdir}/html


%changelog
* Fri Nov 27 2015 Remi Collet <remi@fedoraproject.org> - 0.5.1-1
- update to 0.5.1
- raise dependency on libvirt 1.2.8

* Tue Jun 23 2015 Remi Collet <rcollet@redhat.com> - 0.4.8-3
- allow build against rh-php56 (as more-php56)

* Wed Dec 24 2014 Remi Collet <remi@fedoraproject.org> - 0.4.8-2.1
- Fedora 21 SCL mass rebuild

* Wed Apr 16 2014 Remi Collet <remi@fedoraproject.org> - 0.4.8-2
- add numerical prefix to extension configuration file

* Mon Jan  6 2014 Remi Collet <remi@fedoraproject.org> - 0.4.8-1
- update to 0.4.8
- spec cleanups
- adapt for SCL

* Tue Jan  8 2013 Remi Collet <remi@fedoraproject.org> - 0.4.5-2
- rebuild

* Sun Nov 27 2011 Remi Collet <RPMS@FamilleCollet.com> - 0.4.5-1
- update to 0.4.5
- fix for php 5.4 (and some of compiler warnings)
  https://www.redhat.com/archives/libvir-list/2011-November/msg01476.html

* Tue Aug 23 2011 Remi Collet <RPMS@FamilleCollet.com> - 0.4.4-1
- rebuild for remi repo

* Mon Aug 22 2011 Michal Novotny <minovotn@redhat.com> - 0.4.4
- Several bugfixes and updated SPEC file and codes not to require open tags

* Sun Aug 21 2011 Remi Collet <RPMS@FamilleCollet.com> - 0.4.3-1
- rebuild for remi repo

* Thu Aug 11 2011 Michal Novotny <minovotn@redhat.com> - 0.4.3
- Rebase to 0.4.3 from master branch

* Sat Jul 16 2011 Remi Collet <RPMS@FamilleCollet.com> - 0.4.1-5
- rebuild for remi repo

* Tue Apr 19 2011 Michal Novotny <minovotn@redhat.com> - 0.4.1-5
- Minor memory leak fixes
- Several bug fixes

* Mon Apr 11 2011 Michal Novotny <minovotn@redhat.com> - 0.4.1-4
- Add new storagepool API functions
- Add optional xPath argument for *_get_xml_desc() functions
- Add new network API functions
- Add new API functions to add/remove disks

* Wed Mar 23 2011 Michal Novotny <minovotn@redhat.com> - 0.4.1-3
- Add connection information function
- Add coredump support
- Add snapshots support
- Improve error reporting for destructors

* Thu Mar 10 2011 Michal Novotny <minovotn@redhat.com> - 0.4.1-2
- Changes done to comply with Fedora package policy

* Tue Feb  8 2011 Michal Novotny <minovotn@redhat.com> - 0.4.1-1
- Initial commit (from github)
