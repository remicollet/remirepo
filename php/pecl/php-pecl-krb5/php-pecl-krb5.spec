# spec file for php-pecl-krb5
#
# Copyright (c) 2014 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/3.0/
#
# Please, preserve the changelog entries
#
%{!?php_inidir:  %global php_inidir   %{_sysconfdir}/php.d}
%{!?php_incldir: %global php_incldir  %{_includedir}/php}
%{!?__pecl:      %global __pecl       %{_bindir}/pecl}
%{!?__php:       %global __php        %{_bindir}/php}

%global pecl_name krb5
%global with_zts  0%{?__ztsphp:1}

Summary:        Kerberos authentification extension
Name:           php-pecl-%{pecl_name}
Version:        1.0.0
Release:        2%{?dist}
License:        BSD
Group:          Development/Languages
URL:            http://pecl.php.net/package/%{pecl_name}
Source0:        http://pecl.php.net/get/%{pecl_name}-%{version}.tgz

# http://svn.php.net/viewvc?view=revision&revision=333127
Patch0:         krb5-build.patch

BuildRequires:  krb5-devel >= 1.8
BuildRequires:  pkgconfig(com_err)
BuildRequires:  php-devel > 5.2
BuildRequires:  php-pear

Requires(post): %{__pecl}
Requires(postun): %{__pecl}
Requires:       php(zend-abi) = %{php_zend_api}
Requires:       php(api) = %{php_core_api}

Provides:       php-%{pecl_name} = %{version}
Provides:       php-%{pecl_name}%{?_isa} = %{version}
Provides:       php-pecl(%{pecl_name}) = %{version}
Provides:       php-pecl(%{pecl_name})%{?_isa} = %{version}

%if 0%{?fedora} < 20 && 0%{?rhel} < 7
# Filter shared private
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}
%endif


%description
Features:
+ An interface for maintaining credential caches (KRB5CCache),
  that can be used for authenticating against a kerberos5 realm
+ Bindings for nearly the complete GSSAPI (RFC2744)
+ The administrative interface (KADM5)
+ Support for HTTP Negotiate authentication via GSSAPI


%package devel
Summary:       Kerberos extension developer files (header)
Group:         Development/Libraries
Requires:      %{name}%{?_isa} = %{version}-%{release}
Requires:      php-devel%{?_isa}

%description devel
These are the files needed to compile programs using the Kerberos extension.


%prep
%setup -q -c
mv %{pecl_name}-%{version} NTS

cd NTS
%patch0 -p0 -b .build

# http://svn.php.net/viewvc?view=revision&revision=333126
chmod -x php_krb5_gssapi.h

# Sanity check, really often broken
extver=$(sed -n '/#define PHP_KRB5_EXT_VERSION/{s/.* "//;s/".*$//;p}' php_krb5.h)
if test "x${extver}" != "x%{version}"; then
   : Error: Upstream extension version is ${extver}, expecting %{version}.
   exit 1
fi
cd ..

%if %{with_zts}
# Duplicate source tree for NTS / ZTS build
cp -pr NTS ZTS
%endif

# Create configuration file
cat << 'EOF' | tee %{pecl_name}.ini
; Enable the '%{pecl_name}' extension module
extension=%{pecl_name}.so
EOF


%build
export CFLAGS="%{optflags} $(pkg-config --cflags com_err)"

peclbuild() {
%configure \
    --with-krb5 \
    --with-krb5config=%{_bindir}/krb5-config \
    --with-krb5kadm \
    --with-php-config=$1
make %{?_smp_mflags}
}
cd NTS

%{_bindir}/phpize
peclbuild %{_bindir}/php-config

%if %{with_zts}
cd ../ZTS
%{_bindir}/zts-phpize
peclbuild %{_bindir}/zts-php-config
%endif


%install
make -C NTS install INSTALL_ROOT=%{buildroot}

# install config file
install -D -m 644 %{pecl_name}.ini %{buildroot}%{php_inidir}/%{pecl_name}.ini

# Install XML package description
install -D -m 644 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml

%if %{with_zts}
make -C ZTS install INSTALL_ROOT=%{buildroot}

install -D -m 644 %{pecl_name}.ini %{buildroot}%{php_ztsinidir}/%{pecl_name}.ini
%endif

# Test & Documentation
for i in $(grep 'role="test"' package.xml | sed -e 's/^.*name="//;s/".*$//')
do install -Dpm 644 NTS/$i %{buildroot}%{pecl_testdir}/%{pecl_name}/$i
done
for i in $(grep 'role="doc"' package.xml | sed -e 's/^.*name="//;s/".*$//')
do install -Dpm 644 NTS/$i %{buildroot}%{pecl_docdir}/%{pecl_name}/$i
done


%post
%{pecl_install} %{pecl_xmldir}/%{name}.xml >/dev/null || :


%postun
if [ $1 -eq 0 ] ; then
    %{pecl_uninstall} %{pecl_name} >/dev/null || :
fi


%check
cd NTS
: Minimal load test for NTS extension
%{__php} --no-php-ini \
    --define extension=%{buildroot}%{php_extdir}/%{pecl_name}.so \
    --modules | grep %{pecl_name}

%if %{with_zts}
cd ../ZTS
: Minimal load test for ZTS extension
%{__ztsphp} --no-php-ini \
    --define extension=%{buildroot}%{php_ztsextdir}/%{pecl_name}.so \
    --modules | grep %{pecl_name}
%endif


%files
%doc %{pecl_docdir}/%{pecl_name}
%{pecl_xmldir}/%{name}.xml

%config(noreplace) %{php_inidir}/%{pecl_name}.ini
%{php_extdir}/%{pecl_name}.so

%if %{with_zts}
%config(noreplace) %{php_ztsinidir}/%{pecl_name}.ini
%{php_ztsextdir}/%{pecl_name}.so
%endif


%files devel
%doc %{pecl_testdir}/%{pecl_name}

%{php_incldir}/ext/%{pecl_name}

%if %{with_zts}
%{php_ztsincldir}/ext/%{pecl_name}
%endif


%changelog
* Wed Mar 26 2014 Remi Collet <remi@fedoraproject.org> - 1.0.0-2
- upstream patch to fix SUCCESS definition
- enable --with-krb5kadm with all PHP versions

* Sat Mar  1 2014 Remi Collet <remi@fedoraproject.org> - 1.0.0-1
- initial package, version 1.0.0 (stable)