# remirepo spec file for php-pecl-seaslog
#
# Copyright (c) 2015-2016 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%if 0%{?scl:1}
%global sub_prefix %{scl_prefix}
%scl_package       php-pecl-seaslog
%else
%global _root_libdir %{_libdir}
%endif

%global with_zts   0%{!?_without_zts:%{?__ztsphp:1}}
%global proj_name  SeasLog
%global pecl_name  seaslog
%global with_tests 0%{!?_without_tests:1}
%if "%{php_version}" < "5.6"
%global ini_name   %{pecl_name}.ini
%else
%global ini_name   40-%{pecl_name}.ini
%endif

Summary:        A effective,fast,stable log extension for PHP
Name:           %{?sub_prefix}php-pecl-%{pecl_name}
Version:        1.6.8
Release:        2%{?dist}%{!?scl:%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}}
License:        ASL 2.0
Group:          Development/Languages
URL:            http://pecl.php.net/package/%{proj_name}
Source0:        http://pecl.php.net/get/%{proj_name}-%{version}.tgz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  %{?scl_prefix}php-devel
BuildRequires:  %{?scl_prefix}php-pear

Requires:       %{?scl_prefix}php(zend-abi) = %{php_zend_api}
Requires:       %{?scl_prefix}php(api) = %{php_core_api}
%{?_sclreq:Requires: %{?scl_prefix}runtime%{?_sclreq}%{?_isa}}

Provides:       %{?scl_prefix}php-%{pecl_name}               = %{version}
Provides:       %{?scl_prefix}php-%{pecl_name}%{?_isa}       = %{version}
Provides:       %{?scl_prefix}php-pecl(%{proj_name})         = %{version}
Provides:       %{?scl_prefix}php-pecl(%{proj_name})%{?_isa} = %{version}
%if "%{?scl_prefix}" != "%{?sub_prefix}"
Provides:       %{?scl_prefix}php-pecl-%{pecl_name}          = %{version}-%{release}
Provides:       %{?scl_prefix}php-pecl-%{pecl_name}%{?_isa}  = %{version}-%{release}
%endif

%if "%{?vendor}" == "Remi Collet" && 0%{!?scl:1}
# Other third party repo stuff
Obsoletes:     php53-pecl-%{pecl_name}  <= %{version}
Obsoletes:     php53u-pecl-%{pecl_name} <= %{version}
Obsoletes:     php54-pecl-%{pecl_name}  <= %{version}
Obsoletes:     php54w-pecl-%{pecl_name} <= %{version}
%if "%{php_version}" > "5.5"
Obsoletes:     php55u-pecl-%{pecl_name} <= %{version}
Obsoletes:     php55w-pecl-%{pecl_name} <= %{version}
%endif
%if "%{php_version}" > "5.6"
Obsoletes:     php56u-pecl-%{pecl_name} <= %{version}
Obsoletes:     php56w-pecl-%{pecl_name} <= %{version}
%endif
%if "%{php_version}" > "7.0"
Obsoletes:     php70u-pecl-%{pecl_name} <= %{version}
Obsoletes:     php70w-pecl-%{pecl_name} <= %{version}
%endif
%if "%{php_version}" > "7.1"
Obsoletes:     php71u-pecl-%{pecl_name} <= %{version}
Obsoletes:     php71w-pecl-%{pecl_name} <= %{version}
%endif
%endif

%if 0%{?fedora} < 20 && 0%{?rhel} < 7
# Filter shared private
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}
%endif


%description
A effective,fast,stable log extension for PHP.
- In the PHP project, for convenient record log
- The default log directory and module configuration.
- Specify the log directory and get the current configuration
- Analysis of early warning framework preliminary
- Buffer debug efficient log buffer, convenient
- With PSR-3 Logger interface

Package built for PHP %(%{__php} -r 'echo PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')%{?scl: as Software Collection (%{scl} by %{?scl_vendor}%{!?scl_vendor:rh})}.


%prep
%setup -q -c
mv %{proj_name}-%{version} NTS

# Don't install tests
sed -e 's/role="test"/role="src"/' \
    %{?_licensedir:-e '/LICENSE/s/role="doc"/role="src"/' } \
    -i package.xml

cd NTS

: Sanity check, really often broken
extver=$(sed -n '/#define SEASLOG_VERSION/{s/.* "//;s/".*$//;p}' php_seaslog.h)
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
cat << 'EOF' | tee %{ini_name}
; Enable %{pecl_name} extension module
extension=%{pecl_name}.so

; Configuration
;seaslog.default_basepath = '/var/log/www'
;seaslog.default_datetime_format = 'Y:m:d H:i:s	'
;seaslog.logger = 'default'
;seaslog.disting_type = 0
;seaslog.disting_by_hour = 0
;seaslog.use_buffer = 0
;seaslog.trace_error = 1
;seaslog.trace_exception = 0
;seaslog.buffer_size = 0
;seaslog.level = 0
;seaslog.appender = 1
;seaslog.remote_host = '127.0.0.1'
;seaslog.remote_port = 514
EOF


%build
cd NTS
%{_bindir}/phpize
%configure \
    --with-seaslog \
    --with-php-config=%{_bindir}/php-config
make %{?_smp_mflags}

%if %{with_zts}
cd ../ZTS
%{_bindir}/zts-phpize
%configure \
    --with-seaslog \
    --with-php-config=%{_bindir}/zts-php-config
make %{?_smp_mflags}
%endif


%install
rm -rf %{buildroot}

make -C NTS install INSTALL_ROOT=%{buildroot}

# install config file
install -D -m 644 %{ini_name} %{buildroot}%{php_inidir}/%{ini_name}

# Install XML package description
install -D -m 644 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml

%if %{with_zts}
make -C ZTS install INSTALL_ROOT=%{buildroot}

install -D -m 644 %{ini_name} %{buildroot}%{php_ztsinidir}/%{ini_name}
%endif

# Documentation
for i in $(grep 'role="doc"' package.xml | sed -e 's/^.*name="//;s/".*$//')
do install -Dpm 644 NTS/$i %{buildroot}%{pecl_docdir}/%{pecl_name}/$i
done


%check
# No useful test in tests directory

cd NTS
: Minimal load test for NTS extension
%{__php} --no-php-ini \
    --define extension=%{buildroot}%{php_extdir}/%{pecl_name}.so \
    --modules | grep -i %{pecl_name}

%if %{with_zts}
cd ../ZTS
: Minimal load test for ZTS extension
%{__ztsphp} --no-php-ini \
    --define extension=%{buildroot}%{php_ztsextdir}/%{pecl_name}.so \
    --modules | grep -i %{pecl_name}
%endif


%if 0%{?fedora} < 24
# when pear installed alone, after us
%triggerin -- %{?scl_prefix}php-pear
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
    %{pecl_uninstall} %{proj_name} >/dev/null || :
fi
%endif


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc %{pecl_docdir}/%{pecl_name}
%{?_licensedir:%license NTS/LICENSE}

%{pecl_xmldir}/%{name}.xml
%config(noreplace) %{php_inidir}/%{ini_name}
%{php_extdir}/%{pecl_name}.so

%if %{with_zts}
%config(noreplace) %{php_ztsinidir}/%{ini_name}
%{php_ztsextdir}/%{pecl_name}.so
%endif


%changelog
* Thu Dec  1 2016 Remi Collet <remi@fedoraproject.org> - 1.6.8-2
- rebuild with PHP 7.1.0 GA

* Mon Oct 17 2016 Remi Collet <remi@fedoraproject.org> - 1.6.8-1
- Update to 1.6.8

* Wed Sep 14 2016 Remi Collet <remi@fedoraproject.org> - 1.6.2-2
- rebuild for PHP 7.1 new API version

* Fri Jul 08 2016 Remi Collet <remi@fedoraproject.org> - 1.6.2-1
- Update to 1.6.2

* Tue Jul 05 2016 Remi Collet <remi@fedoraproject.org> - 1.6.0-1
- Update to 1.6.0
- update provided configuration for new options

* Thu May 19 2016 Remi Collet <remi@fedoraproject.org> - 1.5.6-1
- Update to 1.5.6

* Thu Apr 07 2016 Remi Collet <remi@fedoraproject.org> - 1.5.3-1
- Update to 1.5.3

* Sun Mar  6 2016 Remi Collet <remi@fedoraproject.org> - 1.5.0-2
- adapt for F24

* Sun Dec 06 2015 Remi Collet <remi@fedoraproject.org> - 1.5.0-1
- Update to 1.5.0

* Tue Nov 10 2015 Remi Collet <remi@fedoraproject.org> - 1.4.8-1
- Update to 1.4.8 (stable)

* Fri Oct 23 2015 Remi Collet <remi@fedoraproject.org> - 1.4.6-1
- Update to 1.4.6 (stable)

* Wed Sep 23 2015 Remi Collet <remi@fedoraproject.org> - 1.4.4-1
- Update to 1.4.4 (stable)

* Tue Sep 15 2015 Remi Collet <remi@fedoraproject.org> - 1.4.2-1
- Update to 1.4.2 (stable)

* Mon Sep 14 2015 Remi Collet <remi@fedoraproject.org> - 1.4.0-1
- initial package, version 1.4.0 (stable)
