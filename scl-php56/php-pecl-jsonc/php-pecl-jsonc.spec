# spec file for php-pecl-jsonc
#
# Copyright (c) 2013-2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%{?scl:     %scl_package       php-pecl-jsonc}
%{!?__pecl: %global __pecl     %{_bindir}/pecl}

%global pecl_name  json
%global proj_name  jsonc
%if "%{php_version}" < "5.6"
%global ini_name  %{pecl_name}.ini
%else
%global ini_name  40-%{pecl_name}.ini
%endif

Summary:       Support for JSON serialization
Name:          %{?scl_prefix}php-pecl-%{proj_name}
Version:       1.3.6
Release:       1%{?dist}
License:       PHP
Group:         Development/Languages
URL:           http://pecl.php.net/package/%{proj_name}
Source0:       http://pecl.php.net/get/%{proj_name}-%{version}.tgz

BuildRequires: %{?scl_prefix}php-devel >= 5.4
BuildRequires: %{?scl_prefix}php-pear
BuildRequires: pcre-devel

Requires(post): %{__pecl}
Requires(postun): %{__pecl}
Requires:      %{?scl_prefix}php(zend-abi) = %{php_zend_api}
Requires:      %{?scl_prefix}php(api) = %{php_core_api}

Provides:      %{?scl_prefix}php-%{pecl_name} = %{version}
Provides:      %{?scl_prefix}php-%{pecl_name}%{?_isa} = %{version}
Provides:      %{?scl_prefix}php-pecl(%{pecl_name}) = %{version}
Provides:      %{?scl_prefix}php-pecl(%{pecl_name})%{?_isa} = %{version}
Provides:      %{?scl_prefix}php-pecl(%{proj_name}) = %{version}
Provides:      %{?scl_prefix}php-pecl(%{proj_name})%{?_isa} = %{version}

%if 0%{?fedora} < 20 && 0%{?rhel} < 7
# Filter private shared
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}
%endif


%description
The %{name} module will add support for JSON (JavaScript Object Notation)
serialization to PHP.

This is a dropin alternative to standard PHP JSON extension which
use the json-c library parser.


%package devel
Summary:       JSON developer files (header)
Group:         Development/Libraries
Requires:      %{name}%{?_isa} = %{version}-%{release}
Requires:      %{?scl_prefix}php-devel%{?_isa}

%description devel
These are the files needed to compile programs using JSON serializer.


%prep
%setup -q -c 
cd %{proj_name}-%{version}

# Sanity check, really often broken
extver=$(sed -n '/#define PHP_JSON_VERSION/{s/.* "//;s/".*$//;p}' php_json.h )
if test "x${extver}" != "x%{version}%{?prever:-%{prever}}"; then
   : Error: Upstream extension version is ${extver}, expecting %{version}%{?prever:-%{prever}}.
   exit 1
fi
cd ..

cat << 'EOF' | tee %{ini_name}
; Enable %{pecl_name} extension module
extension = %{pecl_name}.so
EOF


%build
cd %{proj_name}-%{version}
%{_bindir}/phpize
%configure \
  --with-php-config=%{_bindir}/php-config
make %{?_smp_mflags}


%install
# Install the NTS stuff
make -C %{proj_name}-%{version} \
     install INSTALL_ROOT=%{buildroot}
install -D -m 644 %{ini_name} %{buildroot}%{php_inidir}/%{ini_name}

# Install the package XML file
install -D -m 644 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml


%check
cd %{proj_name}-%{version}

TEST_PHP_EXECUTABLE=%{_bindir}/php \
TEST_PHP_ARGS="-n -d extension_dir=$PWD/modules -d extension=%{pecl_name}.so" \
NO_INTERACTION=1 \
REPORT_EXIT_STATUS=1 \
%{_bindir}/php -n run-tests.php


%post
%{pecl_install} %{pecl_xmldir}/%{name}.xml >/dev/null || :


%postun
if [ $1 -eq 0 ] ; then
    %{pecl_uninstall} %{proj_name} >/dev/null || :
fi


%files
%doc %{proj_name}-%{version}%{?prever}/{LICENSE,CREDITS,README.md}
%config(noreplace) %{php_inidir}/%{ini_name}
%{php_extdir}/%{pecl_name}.so
%{pecl_xmldir}/%{name}.xml


%files devel
%{php_incldir}/ext/json


%changelog
* Sun Aug 24 2014 Remi Collet <rcollet@redhat.com> - 1.3.6-1
- release 1.3.6
- adapted for php 5.6

* Thu Apr 10 2014 Remi Collet <rcollet@redhat.com> - 1.3.5-1
- release 1.3.5 (stable) for CVE-2013-6371 CVE-2013-6370

* Mon Dec 16 2013 Remi Collet <rcollet@redhat.com> - 1.3.3-1
- release 1.3.3 (stable) #1042701

* Tue Nov  5 2013 Remi Collet <rcollet@redhat.com> - 1.3.2-2
- fix decode of string value with null-byte
  https://github.com/remicollet/pecl-json-c/issues/7

* Mon Sep  9 2013 Remi Collet <rcollet@redhat.com> - 1.3.2-1
- release 1.3.2 (stable)

* Fri Aug  2 2013 Remi Collet <rcollet@redhat.com> - 1.3.1-1
- adapt for SCL, without ZTS

* Wed Jun 12 2013 Remi Collet <rcollet@redhat.com> - 1.3.1-1
- release 1.3.1 (beta)
- rename to php-pecl-jsonc

* Tue Jun  4 2013 Remi Collet <rcollet@redhat.com> - 1.3.0-1
- release 1.3.0 (beta)
- use system json-c when available (fedora >= 20)
- use jsonc name for module and configuration

* Mon Apr 29 2013 Remi Collet <rcollet@redhat.com> - 1.3.0-0.3
- rebuild with latest changes
- use system json-c library
- temporarily rename to jsonc-c.so

* Sat Apr 27 2013 Remi Collet <rcollet@redhat.com> - 1.3.0-0.2
- rebuild with latest changes

* Sat Apr 27 2013 Remi Collet <rcollet@redhat.com> - 1.3.0-0.1
- initial package
