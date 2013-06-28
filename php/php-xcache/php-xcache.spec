# spec file for php-xcache
#
# Copyright (c) 2012-2013 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/3.0/
#
# Please, preserve the changelog entries
#
%global ext_name     xcache

Summary:       Fast, stable PHP opcode cacher
Name:          php-xcache
Version:       3.0.3
Release:       1%{?dist}
License:       BSD
Group:         Development/Languages
URL:           http://xcache.lighttpd.net/

Source0:       http://xcache.lighttpd.net/pub/Releases/%{version}/%{ext_name}-%{version}.tar.gz
Source1:       xcache-httpd.conf

# Relocation of configuration files to /etc/xcache
Patch0:        xcache-config.patch

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: php-devel

Requires:      php(zend-abi) = %{php_zend_api}
Requires:      php(api) = %{php_core_api}

# Only one opcode cache can be installed
Conflicts:     php-pecl-apc < 3.1.15
Conflicts:     php-eaccelerator
Conflicts:     php-pecl-zendopcache

# Other third party repo stuff
Obsoletes: php53-xcache
Obsoletes: php53u-xcache
Obsoletes: php54-xcache

# Filter private shared object
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}


%description
XCache is a fast, stable  PHP opcode cacher that has been tested and is now
running on production servers under high load. 

It is tested (on linux) and supported on all of the latest PHP release. 
ThreadSafe is also perfectly supported. 

It overcomes a lot of problems that has been with other competing opcachers
such as being able to be used with new  PHP versions. 


%package -n xcache-admin
Summary:       XCache Administration
Group:         Development/Languages
Requires:      mod_php, httpd
Requires:      %{name} = %{version}-%{release}
%if 0%{?fedora} >= 12 || 0%{?rhel} >= 6
BuildArch:     noarch
%endif

%description -n xcache-admin
This package provides the XCache Administration web application,
with Apache configuration, on http://localhost/xcache

This requires to configure, in XCache configuration file (xcache.ini):
- xcache.admin.user
- xcache.admin.pass
- xcache.coveragedump_directory


%prep
%setup -q -c 

# rename source folder
mv %{ext_name}-%{version} nts

cd nts
%patch0 -p1

# Sanity check, really often broken
extver=$(sed -n '/define XCACHE_VERSION/{s/.* "//;s/".*$//;p}' xcache.h)
if test "x${extver}" != "x%{version}"; then
   : Error: Upstream extension version is ${extver}, expecting %{version}.
   exit 1
fi
cd ..

# duplicate for ZTS build
cp -pr nts zts


%build
# Without --enable-xcache-assembler, --enable-xcache-encoder, --enable-xcache-decoder
# This seems not yet implemented

cd nts
%{_bindir}/phpize
%configure \
    --enable-xcache \
    --enable-xcache-constant \
    --enable-xcache-optimizer \
    --enable-xcache-coverager \
    --with-php-config=%{_bindir}/php-config
make %{?_smp_mflags}

cd ../zts
%{_bindir}/zts-phpize
%configure \
    --enable-xcache \
    --enable-xcache-constant \
    --enable-xcache-optimizer \
    --enable-xcache-coverager \
    --with-php-config=%{_bindir}/zts-php-config
make %{?_smp_mflags}


%install
# Install the NTS stuff
make -C nts install INSTALL_ROOT=%{buildroot}
install -D -m 644 nts/%{ext_name}.ini %{buildroot}%{php_inidir}/%{ext_name}.ini

# Install the ZTS stuff
make -C zts install INSTALL_ROOT=%{buildroot}
install -D -m 644 zts/%{ext_name}.ini %{buildroot}%{php_ztsinidir}/%{ext_name}.ini

# Install the admin stuff
install -d -m 755 %{buildroot}%{_datadir}
cp -pr nts/htdocs %{buildroot}%{_datadir}/xcache
install -d -m 755 %{buildroot}%{_sysconfdir}/xcache/cacher
install -d -m 755 %{buildroot}%{_sysconfdir}/xcache/coverager
mv %{buildroot}%{_datadir}/xcache/config.example.php \
   %{buildroot}%{_sysconfdir}/xcache
mv %{buildroot}%{_datadir}/xcache/cacher/config.example.php \
   %{buildroot}%{_sysconfdir}/xcache/cacher
mv %{buildroot}%{_datadir}/xcache/coverager/config.example.php \
   %{buildroot}%{_sysconfdir}/xcache/coverager

install -D -m 644 -p %{SOURCE1} \
        %{buildroot}%{_sysconfdir}/httpd/conf.d/xcache.conf


%check
cd nts

# simple module load test
%{__php} --no-php-ini \
    --define extension_dir=%{buildroot}%{php_extdir}/\
    --define extension=%{ext_name}.so \
    --modules | grep XCache

# upstream unit tests
TEST_PHP_EXECUTABLE=%{_bindir}/php \
NO_INTERACTION=1 \
REPORT_EXIT_STATUS=1 \
php run-tests.php -n -c xcache-test.ini tests

cd ../zts
%{__ztsphp} --no-php-ini \
    --define extension_dir=%{buildroot}%{php_ztsextdir}/\
    --define extension=%{ext_name}.so \
    --modules | grep XCache

TEST_PHP_EXECUTABLE=%{__ztsphp} \
NO_INTERACTION=1 \
REPORT_EXIT_STATUS=1 \
%{__ztsphp} run-tests.php -n -c xcache-test.ini tests


%files
%defattr(-,root,root,-)
%doc nts/{AUTHORS,ChangeLog,COPYING,README,THANKS}
%config(noreplace) %{php_inidir}/%{ext_name}.ini
%config(noreplace) %{php_ztsinidir}/%{ext_name}.ini
%{php_extdir}/%{ext_name}.so
%{php_ztsextdir}/%{ext_name}.so

%files -n xcache-admin
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/httpd/conf.d/xcache.conf
%{_datadir}/xcache
# No real configuration files, only sample files
%{_sysconfdir}/xcache


%changelog
* Fri Jun 28 2013 Remi Collet <remi@fedoraproject.org> - 3.0.3-1
- bump version, no change

* Fri Jun 14 2013 Remi Collet <remi@fedoraproject.org> - 3.0.2-1
- bugfixes version

* Thu Jan 17 2013 Remi Collet <remi@fedoraproject.org> - 3.0.1-1
- bugfixes version

* Sat Nov 22 2012 Remi Collet <remi@fedoraproject.org> - 3.0.0-1.1
- upstream have fixed the sources (review #859504)

* Wed Oct 31 2012 Remi Collet <remi@fedoraproject.org> - 3.0.0-1
- new major version
- drop xcache-coverager subpackage
- xcache-admin now provides cacher, coverager and diagnosis
- run unit tests provided by upstream

* Sat Oct 27 2012 Remi Collet <remi@fedoraproject.org> - 2.0.1-4
- drop php prefix from sub packages
- clean EL-5 stuff

* Fri Sep 21 2012 Remi Collet <remi@fedoraproject.org> - 2.0.1-3
- prepare for review with EL-5 stuff

* Fri Sep 21 2012 Remi Collet <remi@fedoraproject.org> - 2.0.1-2
- add admin and coverager sub-package

* Sun Sep  9 2012 Remi Collet <remi@fedoraproject.org> - 2.0.1-1
- initial package

