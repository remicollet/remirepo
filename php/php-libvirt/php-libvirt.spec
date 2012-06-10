%global		req_libvirt_version 0.6.2
%global		php_confdir %{_sysconfdir}/php.d
%global		php_extdir  %{_libdir}/php/modules

%global         extname   libvirt-php

Name:		php-libvirt
Version:	0.4.5
Release:	1%{?dist}%{?extra_release}
Summary:	PHP language binding for Libvirt

Group:		Development/Libraries
License:	PHP
URL:		http://libvirt.org/php
Source0:	http://libvirt.org/sources/php/libvirt-php-%{version}.tar.gz

# https://www.redhat.com/archives/libvir-list/2011-November/msg01476.html
Patch0:         libvirt-php54.patch

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires:	php-devel
BuildRequires:	libvirt-devel >= %{req_libvirt_version}
BuildRequires:	libxml2-devel
BuildRequires:	libxslt
BuildRequires:	xhtml1-dtds

Requires:	libvirt >= %{req_libvirt_version}
Requires:	php(zend-abi) = %{php_zend_api}
Requires:	php(api) = %{php_core_api}

%define		debug_package	%{nil} 
%global		_use_internal_dependency_generator	0

%description
PHP language bindings for Libvirt API. 
For more details see: http://www.libvirt.org/php/

%package -n php-libvirt-doc
Summary:	Document of php-libvirt
Group:		Development/Libraries
%if 0%{?fedora} >= 11 || 0%{?rhel} >= 6
BuildArch:	noarch
%endif
Requires:	php-libvirt = %{version}

%description -n php-libvirt-doc
PHP language bindings for Libvirt API. 
For more details see: http://www.libvirt.org/php/ http://www.php.net/

This package contain the document for php-libvirt.

%prep
%setup -q -n libvirt-php-%{version}

%patch0 -p1 -b .php54


%build
%configure --with-html-dir=%{_datadir}/doc \
           --with-html-subdir=%{name}-%{version}/html \
           --libdir=%{php_extdir}
make %{?_smp_mflags}


%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

# simple module load test
%{__php} --no-php-ini \
    --define extension_dir=src \
    --define extension=%{extname}.so \
    --modules | grep libvirt


%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc
%{php_extdir}/%{extname}.so
%config(noreplace) %{php_confdir}/%{extname}.ini

%files -n php-libvirt-doc
%defattr(-,root,root,-)
%doc README
%dir %{_datadir}/doc/%{name}-%{version}
%{_datadir}/doc/%{name}-%{version}/html


%changelog
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

* Tue Feb 8 2011 Michal Novotny <minovotn@redhat.com> - 0.4.1-1
- Initial commit (from github)
