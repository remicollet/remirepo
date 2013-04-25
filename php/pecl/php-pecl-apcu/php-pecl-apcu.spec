%{!?php_inidir:  %{expand: %%global php_inidir  %{_sysconfdir}/php.d}}
%{!?php_incldir: %{expand: %%global php_incldir %{_includedir}/php}}
%global pecl_name apcu
%global with_zts  0%{?__ztsphp:1}

Name:           php-pecl-apcu
Summary:        APC User Cache
Version:        4.0.0
Release:        2%{?dist}
Source0:        http://pecl.php.net/get/%{pecl_name}-%{version}.tgz
Source1:        %{pecl_name}.ini
Source2:        %{pecl_name}-panel.conf
Source3:        %{pecl_name}.conf.php

Patch0:         %{pecl_name}-git.patch

License:        PHP
Group:          Development/Languages
URL:            http://pecl.php.net/package/APCu

BuildRequires:  php-devel
BuildRequires:  php-pear

Obsoletes:      php-apcu < 4.0.0-1
Provides:       php-apcu = %{version}
Provides:       php-apcu%{?_isa} = %{version}
Provides:       php-pecl(apcu) = %{version}
Provides:       php-pecl(apcu)%{?_isa} = %{version}
# Same provides than APC, this is a drop in replacement
Conflicts:      php-pecl-apc
Provides:       php-apc = %{version}
Provides:       php-apc%{?_isa} = %{version}
Provides:       php-pecl-apc = %{version}
Provides:       php-pecl-apc%{?_isa} = %{version}
Provides:       php-pecl(APC) = %{version}
Provides:       php-pecl(APC)%{?_isa} = %{version}

# Filter private shared
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}


%description
APCu is userland caching: APC stripped of opcode caching in preparation
for the deployment of Zend OPcache as the primary solution to opcode
caching in future versions of PHP.

APCu has a revised and simplified codebase, by the time the PECL release
is available, every part of APCu being used will have received review and
where necessary or appropriate, changes.

Simplifying and documenting the API of APCu completely removes the barrier
to maintenance and development of APCu in the future, and additionally allows
us to make optimizations not possible previously because of APC's inherent
complexity.

APCu only supports userland caching (and dumping) of variables, providing an
upgrade path for the future. When O+ takes over, many will be tempted to use
3rd party solutions to userland caching, possibly even distributed solutions;
this would be a grave error. The tried and tested APC codebase provides far
superior support for local storage of PHP variables.


%package devel
Summary:       APCu developer files (header)
Group:         Development/Libraries
Requires:      %{name}%{?_isa} = %{version}-%{release}
Requires:      php-devel%{?_isa}
#Obsoletes:     php-pecl-apc-devel

%description devel
These are the files needed to compile programs using APCu.


%package -n apcu-panel
Summary:       APCu control panel
Group:         Applications/Internet
BuildArch:     noarch
Requires:      %{name} = %{version}-%{release}
Requires:      mod_php, httpd, php-gd
#Obsoletes:     apc-panel

%description  -n apcu-panel
This package provides the APCu control panel, with Apache
configuration, available on http://localhost/apcu-panel/


%prep
%setup -qc
mv %{pecl_name}-%{version} NTS

cd NTS
%patch0 -p1 -b .fromgit

# Sanity check, really often broken
extver=$(sed -n '/#define PHP_APC_VERSION/{s/.* "//;s/".*$//;p}' php_apc.h)
if test "x${extver}" != "x%{version}"; then
   : Error: Upstream extension version is ${extver}, expecting %{version}.
   exit 1
fi
cd ..

%if %{with_zts}
# duplicate for ZTS build
cp -pr NTS ZTS
%endif


%build
cd NTS
%{_bindir}/phpize
%configure --with-php-config=%{_bindir}/php-config
make %{?_smp_mflags}

%if %{with_zts}
cd ../ZTS
%{_bindir}/zts-phpize
%configure --with-php-config=%{_bindir}/zts-php-config
make %{?_smp_mflags}
%endif


%install
# Install the NTS stuff
make -C NTS install INSTALL_ROOT=%{buildroot}
install -D -m 644 %{SOURCE1} %{buildroot}%{php_inidir}/%{pecl_name}.ini

# Install the ZTS stuff
%if %{with_zts}
make -C ZTS install INSTALL_ROOT=%{buildroot}
install -D -m 644 %{SOURCE1} %{buildroot}%{php_ztsinidir}/%{pecl_name}.ini
%endif

# Install the package XML file
install -D -m 644 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml

# Install the Control Panel
# Pages
install -d -m 755 %{buildroot}%{_datadir}/apcu-panel
sed -e s:apc.conf.php:%{_sysconfdir}/apcu-panel/conf.php:g \
    NTS/apc.php >%{buildroot}%{_datadir}/apcu-panel/index.php
# Apache config
install -D -m 644 -p %{SOURCE2} \
        %{buildroot}%{_sysconfdir}/httpd/conf.d/apcu-panel.conf
# Panel config
install -D -m 644 -p %{SOURCE3} \
        %{buildroot}%{_sysconfdir}/apcu-panel/conf.php


%check
cd NTS

# Check than both extensions are reported (BC mode)
%{_bindir}/php -n -d extension_dir=modules -d extension=apcu.so -m | grep 'apcu'
%{_bindir}/php -n -d extension_dir=modules -d extension=apcu.so -m | grep 'apc$'

# Upstream test suite
TEST_PHP_EXECUTABLE=%{_bindir}/php \
TEST_PHP_ARGS="-n -d extension_dir=$PWD/modules -d extension=%{pecl_name}.so" \
NO_INTERACTION=1 \
REPORT_EXIT_STATUS=1 \
%{_bindir}/php -n run-tests.php

%if %{with_zts}
cd ../ZTS

%{__ztsphp}    -n -d extension_dir=modules -d extension=apcu.so -m | grep 'apcu'
%{__ztsphp}    -n -d extension_dir=modules -d extension=apcu.so -m | grep 'apc$'

TEST_PHP_EXECUTABLE=%{__ztsphp} \
TEST_PHP_ARGS="-n -d extension_dir=$PWD/modules -d extension=%{pecl_name}.so" \
NO_INTERACTION=1 \
REPORT_EXIT_STATUS=1 \
%{__ztsphp} -n run-tests.php
%endif


%files
%doc NTS/{NOTICE,LICENSE,README.md}
%{pecl_xmldir}/%{name}.xml

%config(noreplace) %{php_inidir}/%{pecl_name}.ini
%{php_extdir}/%{pecl_name}.so

%if %{with_zts}
%{php_ztsextdir}/%{pecl_name}.so
%config(noreplace) %{php_ztsinidir}/%{pecl_name}.ini
%endif

%files devel
%{php_incldir}/ext/%{pecl_name}
%if %{with_zts}
%{php_ztsincldir}/ext/%{pecl_name}
%endif

%files -n apcu-panel
%defattr(-,root,root,-)
# Need to restrict access, as it contains a clear password
%attr(750,apache,root) %dir %{_sysconfdir}/apcu-panel
%config(noreplace) %{_sysconfdir}/apcu-panel/conf.php
%config(noreplace) %{_sysconfdir}/httpd/conf.d/apcu-panel.conf
%{_datadir}/apcu-panel


%changelog
* Thu Apr 25 2013 Remi Collet <remi@fedoraproject.org> - 4.0.0-2
- fix segfault when used from command line

* Wed Mar 27 2013 Remi Collet <remi@fedoraproject.org> - 4.0.0-1
- first pecl release
- rename from php-apcu to php-pecl-apcu

* Tue Mar 26 2013 Remi Collet <remi@fedoraproject.org> - 4.0.0-0.4.git4322fad
- new snapshot (test before release)

* Mon Mar 25 2013 Remi Collet <remi@fedoraproject.org> - 4.0.0-0.3.git647cb2b
- new snapshot with our pull request
- allow to run test suite simultaneously on 32/64 arch
- build warning free

* Mon Mar 25 2013 Remi Collet <remi@fedoraproject.org> - 4.0.0-0.2.git6d20302
- new snapshot with full APC compatibility

* Sat Mar 23 2013 Remi Collet <remi@fedoraproject.org> - 4.0.0-0.1.git44e8dd4
- initial package, version 4.0.0
