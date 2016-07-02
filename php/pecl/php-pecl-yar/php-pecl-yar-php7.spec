# remirepo spec file for php-pecl-yar
#
# Copyright (c) 2013-2016 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%if 0%{?scl:1}
%global sub_prefix %{scl_prefix}
%scl_package       php-pecl-yar
%endif

%global gh_commit  0e04a6a92347f7e95c9ddf8bbbad36b6286ed87f
%global gh_short   %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner   laruence
%global gh_project yar
#global gh_date    20150914
%global with_zts   0%{!?_without_zts:%{?__ztsphp:1}}
%global pecl_name  yar
%global with_tests %{?_without_tests:0}%{!?_without_tests:1}
%if "%{php_version}" < "5.6"
# After json, msgpack
%global ini_name   %{pecl_name}.ini
%else
# After 40-json, 40-msgpack
%global ini_name   50-%{pecl_name}.ini
%endif

Summary:        Light, concurrent RPC framework
Name:           %{?sub_prefix}php-pecl-%{pecl_name}
Version:        2.0.1
%if 0%{?gh_date:1}
Release:        0.10.%{gh_date}git%{gh_short}%{?dist}%{!?scl:%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}}
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{pecl_name}-%{version}-%{gh_short}.tar.gz
%else
Release:        1%{?dist}%{!?scl:%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}}
Source0:        http://pecl.php.net/get/%{pecl_name}-%{version}.tgz
%endif
License:        PHP
Group:          Development/Languages
URL:            http://pecl.php.net/package/%{pecl_name}

BuildRequires:  curl-devel
BuildRequires:  %{?scl_prefix}php-devel > 7
BuildRequires:  %{?scl_prefix}php-pear
BuildRequires:  %{?scl_prefix}php-json
BuildRequires:  %{?sub_prefix}php-pecl-msgpack-devel

Requires:       %{?scl_prefix}php(zend-abi) = %{php_zend_api}
Requires:       %{?scl_prefix}php(api) = %{php_core_api}
%if "%{php_version}" < "5.4"
# php 5.3.3 in EL-6 don't use arched virtual provides
# so only requires real packages instead
Requires:       %{?scl_prefix}php-common%{?_isa}
%else
Requires:       %{?scl_prefix}php-curl%{?_isa}
Requires:       %{?scl_prefix}php-json%{?_isa}
%endif
Requires:       %{?scl_prefix}php-pecl(msgpack)%{?_isa}
%{?_sclreq:Requires: %{?scl_prefix}runtime%{?_sclreq}%{?_isa}}

Provides:       %{?scl_prefix}php-%{pecl_name}               = %{version}
Provides:       %{?scl_prefix}php-%{pecl_name}%{?_isa}       = %{version}
Provides:       %{?scl_prefix}php-pecl(%{pecl_name})         = %{version}
Provides:       %{?scl_prefix}php-pecl(%{pecl_name})%{?_isa} = %{version}
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
Obsoletes:     php55u-pecl-%{pecl_name} <= %{version}
Obsoletes:     php55w-pecl-%{pecl_name} <= %{version}
Obsoletes:     php56u-pecl-%{pecl_name} <= %{version}
Obsoletes:     php56w-pecl-%{pecl_name} <= %{version}
Obsoletes:     php70u-pecl-%{pecl_name} <= %{version}
Obsoletes:     php70w-pecl-%{pecl_name} <= %{version}
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
Yar (Yet another RPC framework) is a light, concurrent RPC framework,
supports multi package protocols (json, msgpack).

Package built for PHP %(%{__php} -r 'echo PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')%{?scl: as Software Collection (%{scl} by %{?scl_vendor}%{!?scl_vendor:rh})}.


%prep
%setup -qc
%if 0%{?gh_date:1}
mv %{gh_project}-%{gh_commit} NTS
mv NTS/package2.xml .
%else
mv %{pecl_name}-%{version} NTS
%endif

# Don't install/register tests
sed -e 's/role="test"/role="src"/' \
    %{?_licensedir:-e '/LICENSE/s/role="doc"/role="src"/' } \
    -i package2.xml

cd NTS

# Sanity check, really often broken
extver=$(sed -n '/#define PHP_YAR_VERSION/{s/.* "//;s/".*$//;p}' php_yar.h)
if test "x${extver}" != "x%{version}%{?prever:-%{prever}}%{?gh_date:-dev}"; then
   : Error: Upstream extension version is ${extver}, expecting %{version}%{?prever:-%{prever}}%{?gh_date:-dev}.
   exit 1
fi
cd ..

sed -e 's:tools/yar_debug.inc:yar_debug.inc:' \
    -e 's:tools/yar_debug.php:yar_debug:' \
    -i package2.xml

%if %{with_zts}
# Duplicate source tree for NTS / ZTS build
cp -pr NTS ZTS
%endif

# Create configuration file
cat > %{ini_name} << 'EOF'
; Enable %{pecl_name} extension module
extension=%{pecl_name}.so

; Configuration
;yar.allow_persistent=0
;yar.connect_timeout=1000
;yar.content_type=application/octet-stream
;yar.debug=Off
;yar.expose_info=On
;yar.packager=msgpack
;yar.timeout=5000
;yar.transport=curl
EOF


%build
cd NTS
%{_bindir}/phpize
%configure \
    --enable-msgpack \
    --with-php-config=%{_bindir}/php-config
make %{?_smp_mflags}

%if %{with_zts}
cd ../ZTS
%{_bindir}/zts-phpize
%configure \
    --enable-msgpack \
    --with-php-config=%{_bindir}/zts-php-config
make %{?_smp_mflags}
%endif


%install
make -C NTS install INSTALL_ROOT=%{buildroot}

# install config file
install -D -m 644 %{ini_name} %{buildroot}%{php_inidir}/%{ini_name}

# Install XML package description
install -D -m 644 package2.xml %{buildroot}%{pecl_xmldir}/%{name}.xml

%if %{with_zts}
make -C ZTS install INSTALL_ROOT=%{buildroot}

install -D -m 644 %{ini_name} %{buildroot}%{php_ztsinidir}/%{ini_name}
%endif

# Tools
install -Dpm 644 NTS/tools/yar_debug.inc %{buildroot}%{pear_phpdir}/yar_debug.inc
install -Dpm 755 NTS/tools/yar_debug.php %{buildroot}%{_bindir}/yar_debug

# Documentation
cd NTS
for i in $(grep 'role="doc"' ../package2.xml | sed -e 's/^.*name="//;s/".*$//')
do install -Dpm 644 $i %{buildroot}%{pecl_docdir}/%{pecl_name}/$i
done


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
    %{pecl_uninstall} %{pecl_name} >/dev/null || :
fi
%endif


%check
: Minimal load test for NTS extension
%{__php} --no-php-ini \
    --define extension=json.so \
    --define extension=msgpack.so \
    --define extension=NTS/modules/%{pecl_name}.so \
    --modules | grep %{pecl_name}

%if %{with_zts}
: Minimal load test for ZTS extension
%{__ztsphp} --no-php-ini \
    --define extension=json.so \
    --define extension=msgpack.so \
    --define extension=ZTS/modules/%{pecl_name}.so \
    --modules | grep %{pecl_name}
%endif

%if %{with_tests}
cd NTS

: Create test configuration
export TEST_PHP_EXECUTABLE=%{__php}
export TEST_PHP_ARGS="-n -d extension=json.so -d extension=msgpack.so -d extension=$PWD/modules/%{pecl_name}.so"
export NO_INTERACTION=1
export REPORT_EXIT_STATUS=1

%ifarch x86_64
export YAR_API_PORT=8968
%else
export YAR_API_PORT=8964
%endif

: Run the upstream test suite
%{__php} -n run-tests.php --show-diff
%else
: upstream test suite disabled
%endif


%files
%doc %{pecl_docdir}/%{pecl_name}
%{pecl_xmldir}/%{name}.xml

%config(noreplace) %{php_inidir}/%{ini_name}
%{php_extdir}/%{pecl_name}.so
%{_bindir}/yar_debug
%{pear_phpdir}/yar_debug.inc

%if %{with_zts}
%config(noreplace) %{php_ztsinidir}/%{ini_name}
%{php_ztsextdir}/%{pecl_name}.so
%endif


%changelog
* Sat Jul  2 2016 Remi Collet <remi@fedoraproject.org> - 2.0.1-1
- update to 2.0.1 (php 7)
- sources from pecl
- drop patch merged upstream

* Sat Jun 11 2016 Remi Collet <remi@fedoraproject.org> - 2.0.0-3
- add patch for PHP 7.1
  open https://github.com/laruence/yar/pull/83

* Sun Mar  6 2016 Remi Collet <remi@fedoraproject.org> - 2.0.0-2
- adapt for F24

* Tue Oct 27 2015 Remi Collet <remi@fedoraproject.org> - 2.0.0-1
- update to 2.0.0 (beta, php 7)

* Tue Oct 13 2015 Remi Collet <remi@fedoraproject.org> - 1.2.5-0.10.20150914git87e4850
- rebuild for PHP 7.0.0RC5 new API version
- new snapshot

* Fri Sep 18 2015 Remi Collet <remi@fedoraproject.org> - 1.2.5-0.9.20150724git47317d6
- F23 rebuild with rh_layout

* Fri Jul 24 2015 Remi Collet <remi@fedoraproject.org> - 1.2.5-0.8.20150724git47317d6
- new snapshot

* Fri Jul 24 2015 Remi Collet <remi@fedoraproject.org> - 1.2.5-0.7.20150717git07b6772
- ignore 1 failed test on i386
- open https://github.com/laruence/yar/issues/56 (1 failed test on i386)

* Wed Jul 22 2015 Remi Collet <remi@fedoraproject.org> - 1.2.5-0.6.20150717git07b6772
- rebuild against php 7.0.0beta2

* Wed Jul  8 2015 Remi Collet <remi@fedoraproject.org> - 1.2.5-0.5.20150701gita937b2f
- rebuild against php 7.0.0beta1

* Wed Jun 24 2015 Remi Collet <remi@fedoraproject.org> - 1.2.5-0.4.20150617gitd1fb4b5
- rebuild for "rh_layout"

* Wed Jun 17 2015 Remi Collet <remi@fedoraproject.org> - 1.2.5-0.3.20150615git410ca7a
- rebuild
- open https://github.com/laruence/yar/pull/51

* Fri Jun 12 2015 Remi Collet <remi@fedoraproject.org> - 1.2.5-0.2.20150612git3b43b26
- enable test suite during the build

* Fri Jun 12 2015 Remi Collet <remi@fedoraproject.org> - 1.2.5-0.1.20150612git7aca9e6
- Update to 1.2.5-dev for PHP 7
- sources from github
- drop runtime dependency on pear, new scriptlets

* Wed Dec 24 2014 Remi Collet <remi@fedoraproject.org> - 1.2.4-1.1
- Fedora 21 SCL mass rebuild

* Sat Oct 25 2014 Remi Collet <remi@fedoraproject.org> - 1.2.4-1
- Update to 1.2.4
- dont install test suite

* Tue Aug 26 2014 Remi Collet <rcollet@redhat.com> - 1.2.3-3
- improve SCL build

* Thu Apr 17 2014 Remi Collet <remi@fedoraproject.org> - 1.2.3-2
- add numerical prefix to extension configuration file (php 5.6)

* Thu Jan 02 2014 Remi Collet <remi@fedoraproject.org> - 1.2.3-1
- Update to 1.2.3 (stable)
- provides yar_debug command
- fix default options in comments
- adapt for SCL

* Tue Dec 31 2013 Remi Collet <remi@fedoraproject.org> - 1.2.2-1
- Update to 1.2.2 (stable)

* Tue Nov 19 2013 Remi Collet <remi@fedoraproject.org> - 1.2.1-1
- Update to 1.2.1 (stable)
- install doc in pecl doc_dir
- install tests in pecl test_dir

* Wed Jul 17 2013 Remi Collet <remi@fedoraproject.org> - 1.2.0-1
- initial package

