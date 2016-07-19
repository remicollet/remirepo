# Fedora spec file for php-pecl-mongodb
# without SCL compatibility, from
#
# remirepo spec file for php-pecl-mongodb
#
# Copyright (c) 2015-2016 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global with_zts   0%{?__ztsphp:1}
%global pecl_name  mongodb
%if "%{php_version}" < "5.6"
%global ini_name   z-%{pecl_name}.ini
%else
# After 40-smbclient.ini, see https://jira.mongodb.org/browse/PHPC-658
%global ini_name   50-%{pecl_name}.ini
%endif
# Still needed because of some private API
%global buildver %(pkg-config --silence-errors --modversion libmongoc-priv 2>/dev/null || echo 65536)

Summary:        MongoDB driver for PHP
Name:           php-pecl-%{pecl_name}
Version:        1.1.8
Release:        3%{?dist}
License:        ASL 2.0
Group:          Development/Languages
URL:            http://pecl.php.net/package/%{pecl_name}
Source0:        http://pecl.php.net/get/%{pecl_name}-%{version}%{?prever}.tgz

BuildRequires:  php-devel > 5.4
BuildRequires:  php-pear
BuildRequires:  cyrus-sasl-devel
BuildRequires:  openssl-devel
BuildRequires:  pkgconfig(libbson-1.0)    >= 1.3.0
BuildRequires:  pkgconfig(libmongoc-1.0)  >= 1.3.0
BuildRequires:  pkgconfig(libmongoc-priv) >= 1.3.0
BuildRequires:  pkgconfig(libmongoc-priv) <  1.4

Requires:       php(zend-abi) = %{php_zend_api}
Requires:       php(api) = %{php_core_api}
Requires:       mongo-c-driver%{?_isa} >= %{buildver}

# Don't provide php-mongodb which is the pure PHP library
Provides:       php-pecl(%{pecl_name})         = %{version}
Provides:       php-pecl(%{pecl_name})%{?_isa} = %{version}


%description
The purpose of this driver is to provide exceptionally thin glue between
MongoDB and PHP, implementing only fundemental and performance-critical
components necessary to build a fully-functional MongoDB driver.


%prep
%setup -q -c
mv %{pecl_name}-%{version}%{?prever} NTS

# Don't install/register tests
sed -e 's/role="test"/role="src"/' \
    %{?_licensedir:-e '/LICENSE/s/role="doc"/role="src"/' } \
    -i package.xml

cd NTS

# Sanity check, really often broken
extver=$(sed -n '/#define MONGODB_VERSION_S/{s/.* "//;s/".*$//;p}' php_phongo.h)
if test "x${extver}" != "x%{version}%{?prever:%{prever}}"; then
   : Error: Upstream extension version is ${extver}, expecting %{version}%{?prever:%{prever}}.
   exit 1
fi
cd ..

%if %{with_zts}
# Duplicate source tree for NTS / ZTS build
cp -pr NTS ZTS
%endif

# Create configuration file
cat << 'EOF' | tee %{ini_name}
; Enable %{summary} extension module
extension=%{pecl_name}.so

; Configuration
;mongodb.debug=''
EOF


%build
peclbuild() {
  %{_bindir}/${1}ize

  # Ensure we use system library
  # Need to be removed only after phpize because of m4_include
  rm -r src/libbson
  rm -r src/libmongoc

  %configure \
    --with-php-config=%{_bindir}/${1}-config \
    --with-libbson \
    --with-libmongoc \
    --enable-mongodb

  make %{?_smp_mflags}
}

cd NTS
peclbuild php

%if %{with_zts}
cd ../ZTS
peclbuild zts-php
%endif


%install
make -C NTS \
     install INSTALL_ROOT=%{buildroot}

# install config file
install -D -m 644 %{ini_name} %{buildroot}%{php_inidir}/%{ini_name}

# Install XML package description
install -D -m 644 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml

%if %{with_zts}
make -C ZTS \
     install INSTALL_ROOT=%{buildroot}

install -D -m 644 %{ini_name} %{buildroot}%{php_ztsinidir}/%{ini_name}
%endif

# Documentation
for i in $(grep 'role="doc"' package.xml | sed -e 's/^.*name="//;s/".*$//')
do install -Dpm 644 NTS/$i %{buildroot}%{pecl_docdir}/%{pecl_name}/$i
done


%if 0%{?fedora} < 24
# when pear installed alone, after us
%triggerin -- php-pear
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
%license NTS/LICENSE
%doc %{pecl_docdir}/%{pecl_name}
%{pecl_xmldir}/%{name}.xml

%config(noreplace) %{php_inidir}/%{ini_name}
%{php_extdir}/%{pecl_name}.so

%if %{with_zts}
%config(noreplace) %{php_ztsinidir}/%{ini_name}
%{php_ztsextdir}/%{pecl_name}.so
%endif


%changelog
* Tue Jul 19 2016 Remi Collet <remi@fedoraproject.org> - 1.1.8-2
- License is ASL 2.0, from review #1269056

* Wed Jul 06 2016 Remi Collet <remi@fedoraproject.org> - 1.1.8-1
- Update to 1.1.8

* Thu Jun  2 2016 Remi Collet <remi@fedoraproject.org> - 1.1.7-1
- Update to 1.1.7

* Thu Apr  7 2016 Remi Collet <remi@fedoraproject.org> - 1.1.6-1
- Update to 1.1.6

* Thu Mar 31 2016 Remi Collet <remi@fedoraproject.org> - 1.1.5-3
- load after smbclient to workaround
  https://jira.mongodb.org/browse/PHPC-658

* Fri Mar 18 2016 Remi Collet <remi@fedoraproject.org> - 1.1.5-1
- Update to 1.1.5 (stable)

* Thu Mar 10 2016 Remi Collet <remi@fedoraproject.org> - 1.1.4-1
- Update to 1.1.4 (stable)

* Sat Mar  5 2016 Remi Collet <remi@fedoraproject.org> - 1.1.3-1
- Update to 1.1.3 (stable)

* Thu Jan 07 2016 Remi Collet <remi@fedoraproject.org> - 1.1.2-1
- Update to 1.1.2 (stable)

* Thu Dec 31 2015 Remi Collet <remi@fedoraproject.org> - 1.1.1-3
- fix patch for 32bits build
  open https://github.com/mongodb/mongo-php-driver/pull/191

* Sat Dec 26 2015 Remi Collet <remi@fedoraproject.org> - 1.1.1-1
- Update to 1.1.1 (stable)
- add patch for 32bits build,
  open https://github.com/mongodb/mongo-php-driver/pull/185

* Wed Dec 16 2015 Remi Collet <remi@fedoraproject.org> - 1.1.0-1
- Update to 1.1.0 (stable)
- raise dependency on libmongoc >= 1.3.0

* Tue Dec  8 2015 Remi Collet <remi@fedoraproject.org> - 1.0.1-1
- update to 1.0.1 (stable)
- ensure libmongoc >= 1.2.0 and < 1.3 is used

* Fri Oct 30 2015 Remi Collet <remi@fedoraproject.org> - 1.0.0-1
- update to 1.0.0 (stable)

* Tue Oct 27 2015 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.6.RC0
- Update to 1.0.0RC0 (beta)

* Tue Oct  6 2015 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.4-beta2
- drop SCL compatibility for Fedora

* Tue Oct  6 2015 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.3-beta2
- Update to 1.0.0beta2 (beta)

* Fri Sep 11 2015 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.2-beta1
- Update to 1.0.0beta1 (beta)

* Mon Aug 31 2015 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.1.alpha2
- Update to 1.0.0alpha2 (alpha)
- buid with system libmongoc

* Thu May 07 2015 Remi Collet <remi@fedoraproject.org> - 0.6.3-1
- Update to 0.6.3 (alpha)

* Wed May 06 2015 Remi Collet <remi@fedoraproject.org> - 0.6.2-1
- Update to 0.6.2 (alpha)

* Wed May 06 2015 Remi Collet <remi@fedoraproject.org> - 0.6.0-1
- Update to 0.6.0 (alpha)

* Sat Apr 25 2015 Remi Collet <remi@fedoraproject.org> - 0.5.1-1
- Update to 0.5.1 (alpha)

* Thu Apr 23 2015 Remi Collet <remi@fedoraproject.org> - 0.5.0-2
- build with system libbson
- open https://jira.mongodb.org/browse/PHPC-259

* Wed Apr 22 2015 Remi Collet <remi@fedoraproject.org> - 0.5.0-1
- initial package, version 0.5.0 (alpha)

