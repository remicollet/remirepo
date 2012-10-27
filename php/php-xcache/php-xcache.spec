%global ext_name     xcache
%global with_zts     0%{?__ztsphp:1}

Summary:       Fast, stable PHP opcode cacher
Name:          php-xcache
Version:       2.0.1
Release:       4%{?dist}
License:       BSD
Group:         Development/Languages
URL:           http://xcache.lighttpd.net/

Source0:       http://xcache.lighttpd.net/pub/Releases/%{version}/%{ext_name}-%{version}.tar.gz
Source1:       xcache-admin.conf
Source2:       xcache-coverager.conf

# Specific RPM extension PATH
Patch0:        %{ext_name}-conf.patch

BuildRequires: php-devel

Requires:      php(zend-abi) = %{php_zend_api}
Requires:      php(api) = %{php_core_api}

# Only one opcode cache
Conflicts:     php-pecl-apc, php-eaccelerator

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
BuildArch:     noarch

%description -n xcache-admin
This package provides the XCache Administration web application,
with Apache configuration, on http://localhost/xcache-admin

This requires to configure xcache.admin.user and xcache.admin.pass options
in XCache configuration file (xcache.ini).


%package -n xcache-coverager
Summary:       XCache PHP Code Coverage Viewer
Group:         Development/Languages
Requires:      mod_php, httpd
Requires:      %{name} = %{version}-%{release}
BuildArch:     noarch

%description -n xcache-coverager
This package provides the XCache PHP Code Coverage Viewer web application,
with Apache configuration, on http://localhost/xcache-coverager

This requires to configure xcache.coveragedump_directory option in XCache
configuration file (xcache.ini).


%prep
%setup -q -c 

# rename source folder
mv %{ext_name}-%{version} nts

# Sanity check, really often broken
extver=$(sed -n '/define XCACHE_VERSION/{s/.* "//;s/".*$//;p}' nts/xcache.h)
if test "x${extver}" != "x%{version}"; then
   : Error: Upstream extension version is ${extver}, expecting %{version}.
   exit 1
fi

%if %{with_zts}
# duplicate for ZTS build
cp -pr nts zts
%endif

cd nts
%patch0 -p0 -b .upstream
sed -e 's:@EXTDIR@:%{php_extdir}:'    -i %{ext_name}.ini

%if %{with_zts}
cd ../zts
%patch0 -p0 -b .upstream
sed -e 's:@EXTDIR@:%{php_ztsextdir}:' -i %{ext_name}.ini
%endif


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

%if %{with_zts}
cd ../zts
%{_bindir}/zts-phpize
%configure \
    --enable-xcache \
    --enable-xcache-constant \
    --enable-xcache-optimizer \
    --enable-xcache-coverager \
    --with-php-config=%{_bindir}/zts-php-config
make %{?_smp_mflags}
%endif


%install
# Install the NTS stuff
make -C nts install INSTALL_ROOT=%{buildroot}
install -D -m 644 nts/%{ext_name}.ini %{buildroot}%{_sysconfdir}/php.d/%{ext_name}.ini

%if %{with_zts}
# Install the ZTS stuff
make -C zts install INSTALL_ROOT=%{buildroot}
install -D -m 644 zts/%{ext_name}.ini %{buildroot}%{php_ztsinidir}/%{ext_name}.ini
%endif

# Install the admin stuff
install -d -m 755 %{buildroot}%{_datadir}/xcache/admin
install -p -m 644 nts/admin/* %{buildroot}%{_datadir}/xcache/admin
install -D -m 644 -p %{SOURCE1} \
        %{buildroot}%{_sysconfdir}/httpd/conf.d/xcache-admin.conf

# Install the coverager stuff
install -d -m 755 %{buildroot}%{_datadir}/xcache/coverager
install -p -m 644 nts/coverager/* %{buildroot}%{_datadir}/xcache/coverager
install -D -m 644 -p %{SOURCE2} \
        %{buildroot}%{_sysconfdir}/httpd/conf.d/xcache-coverager.conf


%check
# simple module load test
php --no-php-ini \
    --define zend_extension=%{buildroot}%{php_extdir}/%{ext_name}.so \
    --modules | grep XCache

%if %{with_zts}
%{__ztsphp} --no-php-ini \
    --define zend_extension=%{buildroot}%{php_ztsextdir}/%{ext_name}.so \
    --modules | grep XCache
%endif


%files
%doc nts/{AUTHORS,ChangeLog,COPYING,README,THANKS}
%config(noreplace) %{_sysconfdir}/php.d/%{ext_name}.ini
%{php_extdir}/%{ext_name}.so

%if %{with_zts}
%{php_ztsextdir}/%{ext_name}.so
%config(noreplace) %{php_ztsinidir}/%{ext_name}.ini
%endif

%files -n xcache-admin
%config(noreplace) %{_sysconfdir}/httpd/conf.d/xcache-admin.conf
%dir %{_datadir}/xcache
%{_datadir}/xcache/admin

%files -n xcache-coverager
%config(noreplace) %{_sysconfdir}/httpd/conf.d/xcache-coverager.conf
%dir %{_datadir}/xcache
%{_datadir}/xcache/coverager


%changelog
* Sat Oct 27 2012 Remi Collet <remi@fedoraproject.org> - 2.0.1-4
- drop php prefix from sub packages
- clean EL-5 stuff

* Fri Sep 21 2012 Remi Collet <remi@fedoraproject.org> - 2.0.1-3
- prepare for review with EL-5 stuff

* Fri Sep 21 2012 Remi Collet <remi@fedoraproject.org> - 2.0.1-2
- add admin and coverager sub-package

* Sun Sep  9 2012 Remi Collet <remi@fedoraproject.org> - 2.0.1-1
- initial package

