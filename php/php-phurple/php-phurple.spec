# spec file for php-phurple
#
# Copyright (c) 2013-2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%{?scl:          %scl_package        php-phurple}
%{!?php_inidir:  %global php_inidir  %{_sysconfdir}/php.d}
%{!?__pecl:      %global __pecl      %{_bindir}/pecl}
%{!?__php:       %global __php       %{_bindir}/php}

%global gh_commit  46b7db6fc1cd69fc46ffd75c8622a94f3a1079c8
%global gh_short   %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner   weltling
%global gh_project phurple
%global pecl_name  %{gh_project}
#global gh_date    20131007
%global with_zts   0%{?__ztsphp:1}
%if "%{php_version}" < "5.6"
%global ini_name   %{pecl_name}.ini
%else
%global ini_name   40-%{pecl_name}.ini
%endif

Name:           %{?scl_prefix}php-%{gh_project}
Summary:        PHP bindings for libpurple
Version:        0.6.0
Release:        3%{?dist}%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}.1

URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}.tar.gz
License:        MIT
Group:          Development/Libraries

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  libpurple-devel
BuildRequires:  glib2-devel
BuildRequires:  pcre-devel
BuildRequires:  %{?scl_prefix}php-devel

Requires:       %{?scl_prefix}php(zend-abi) = %{php_zend_api}
Requires:       %{?scl_prefix}php(api) = %{php_core_api}
%{?_sclreq:Requires: %{?scl_prefix}runtime%{?_sclreq}%{?_isa}}

%if "%{?vendor}" == "Remi Collet" && 0%{!?scl:1}
# Other third party repo stuff
Obsoletes:     php54-%{gh_project}
Obsoletes:     php54w-%{gh_project}
%if "%{php_version}" > "5.5"
Obsoletes:     php55u-%{gh_project}
Obsoletes:     php55w-%{gh_project}
%endif
%if "%{php_version}" > "5.6"
Obsoletes:     php56u-%{gh_project}
Obsoletes:     php56w-%{gh_project}
%endif
%endif

%if 0%{?fedora} < 20 && 0%{?rhel} < 7
# Filter private shared
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}
%endif


%description
This libpurple PHP bindings, which defines a set of internal classes,
gives a possibility to use AOL and ICQ (OSCAR), Yahoo, Jabber, IRC
and much more protocols directly from PHP. Write your own IM chat
client in PHP, as simply as PHP enables it.


%prep
%setup -qc
mv %{gh_project}-%{gh_commit} NTS

cd NTS
# https://github.com/weltling/phurple/commit/ffef8301f11d2af8ffe8ce4b8396ad8a9b2efc8b
sed -e 's:DIR/lib:DIR/$PHP_LIBDIR:' -i config.m4

# Upstream often forget to change this
extver=$(sed -n '/#define PHP_PHURPLE_VERSION/{s/.* "//;s/".*$//;p}' php_%{gh_project}.h)
if test "x${extver}" != "x%{version}"; then
   : Error: Upstream version is ${extver}, expecting %{version}.
   exit 1
fi
cd ..

cat > %{ini_name} << 'EOF'
; Enable %{summary}
extension = %{pecl_name}.so

; Runtime configuration
;phurple.custom_plugin_path=
EOF

%if %{with_zts}
: Duplicate for ZTS build
cp -pr NTS ZTS
%endif


%build
cd NTS
%{_bindir}/phpize
%configure \
    --with-libdir=%{_lib} \
    --with-php-config=%{_bindir}/php-config
make %{?_smp_mflags}

%if %{with_zts}
cd ../ZTS
%{_bindir}/zts-phpize
%configure \
    --with-libdir=%{_lib} \
    --with-php-config=%{_bindir}/zts-php-config
make %{?_smp_mflags}
%endif


%install
rm -rf %{buildroot}
: Install the NTS stuff
make -C NTS install INSTALL_ROOT=%{buildroot}
install -D -m 644 %{ini_name} %{buildroot}%{php_inidir}/%{ini_name}

: Install the ZTS stuff
%if %{with_zts}
make -C ZTS install INSTALL_ROOT=%{buildroot}
install -D -m 644 %{ini_name} %{buildroot}%{php_ztsinidir}/%{ini_name}
%endif


%check
: Minimal load test for NTS extension
%{__php} --no-php-ini \
    --define extension=NTS/modules/%{pecl_name}.so \
    --modules | grep %{pecl_name}


%if %{with_zts}
: Minimal load test for ZTS extension
%{__ztsphp} --no-php-ini \
    --define extension=ZTS/modules/%{pecl_name}.so \
    --modules | grep %{pecl_name}
%endif


%clean
rm -rf %{buildroot}


%files
%defattr(-, root, root, 0755)
%doc NTS/{CREDITS,LICENSE,README.md,TODO}

%config(noreplace) %{php_inidir}/%{ini_name}
%{php_extdir}/%{pecl_name}.so

%if %{with_zts}
%{php_ztsextdir}/%{pecl_name}.so
%config(noreplace) %{php_ztsinidir}/%{ini_name}
%endif


%changelog
* Wed Dec 24 2014 Remi Collet <remi@fedoraproject.org> - 0.6.0-3.1
- Fedora 21 SCL mass rebuild

* Tue Aug 26 2014 Remi Collet <rcollet@redhat.com> - 0.6.0-3
- improve SCL build

* Wed Apr 16 2014 Remi Collet <remi@fedoraproject.org> - 0.6.0-2
- add numerical prefix to extension configuration file (php 5.6)

* Thu Jan  2 2014 Remi Collet <remi@fedoraproject.org> - 0.6.0-1
- update to 0.6.0 (alpha)
- adapt for SCL

* Thu Oct 17 2013 Remi Collet <remi@fedoraproject.org> - 0.5.0-1
- initial package, version 0.5.0
