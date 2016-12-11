# remirepo spec file for php-pecl-yac
# with SCL compatibility, from:
#
# Fedora spec file for php-pecl-yac (previously php-yac)
#
# Copyright (c) 2013-2016 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%if 0%{?scl:1}
%global sub_prefix %{scl_prefix}
%scl_package        php-pecl-yac
%endif

%global gh_commit   7e5a9edfcfb6ad064c165a0b6abf8d11218fe4b5
%global gh_short    %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner    laruence
%global gh_project  yac
#global gh_date     20150908
%global with_zts    0%{!?_without_zts:%{?__ztsphp:1}}
%global pecl_name   yac
%global with_tests  %{!?_without_tests:1}%{?_without_tests:0}
%if "%{php_version}" < "5.6"
%global ini_name    %{pecl_name}.ini
%else
%global ini_name    40-%{pecl_name}.ini
%endif
%global with_fastlz 1

Summary:        Lockless user data cache
Name:           %{?sub_prefix}php-pecl-%{pecl_name}
Version:        2.0.1
%if 0%{?gh_date:1}
Release:        0.7.%{gh_date}git%{gh_short}%{?dist}%{!?scl:%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}}
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{pecl_name}-%{version}-%{gh_short}.tar.gz
%else
Release:        3%{?dist}%{!?scl:%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}}
Source0:        http://pecl.php.net/get/%{pecl_name}-%{version}.tgz
%endif

License:        PHP
Group:          Development/Languages
URL:            http://pecl.php.net/package/%{pecl_name}

BuildRequires:  %{?scl_prefix}php-devel > 7
BuildRequires:  %{?scl_prefix}php-pear
%if %{with_fastlz}
BuildRequires:  fastlz-devel
%endif

Requires:       %{?scl_prefix}php(zend-abi) = %{php_zend_api}
Requires:       %{?scl_prefix}php(api) = %{php_core_api}
%{?_sclreq:Requires: %{?scl_prefix}runtime%{?_sclreq}%{?_isa}}

# Package have be renamed
Obsoletes:      %{?scl_prefix}php-%{pecl_name}               < %{version}
Provides:       %{?scl_prefix}php-%{pecl_name}               = %{version}
Provides:       %{?scl_prefix}php-%{pecl_name}%{?_isa}       = %{version}
Provides:       %{?scl_prefix}php-pecl(%{pecl_name})         = %{version}
Provides:       %{?scl_prefix}php-pecl(%{pecl_name})%{?_isa} = %{version}
%if "%{?scl_prefix}" != "%{?sub_prefix}"
Provides:       %{?scl_prefix}php-pecl-%{pecl_name}          = %{version}-%{release}
Provides:       %{?scl_prefix}php-pecl-%{pecl_name}%{?_isa}  = %{version}-%{release}
%endif

%if "%{?vendor}" == "Remi Collet" && 0%{!?scl:1} && 0%{?rhel}
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
# Filter private shared object
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}
%endif


%description
Yac (Yet Another Cache) is a shared memory user data cache for PHP.

It can be used to replace APC or local memcached.

Yac is lockless, that means, it is very fast, but there could be a
chance you will get a wrong data(depends on how many key slots are
allocated and how many keys are stored), so you'd better make sure
that your product is not very sensitive to that.

Package built for PHP %(%{__php} -r 'echo PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')%{?scl: as Software Collection (%{scl} by %{?scl_vendor}%{!?scl_vendor:rh})}.


%prep
%setup -qc
%if 0%{?gh_date:1}
mv %{gh_project}-%{gh_commit} NTS
mv NTS/package.xml .
%else
mv %{pecl_name}-%{version} NTS
%endif

# Don't install (register) the tests
sed -e 's/role="test"/role="src"/' \
    %{?_licensedir:-e '/LICENSE/s/role="doc"/role="src"/' } \
    -i package.xml

cd NTS
%if %{with_fastlz}
sed -e '\:name="compressor/fastlz:d' -i ../package.xml
rm -r compressor/fastlz
%endif

# Check version as upstream often forget to update this
extver=$(sed -n '/#define PHP_YAC_VERSION/{s/.* "//;s/".*$//;p}' php_yac.h)
if test "x${extver}" != "x%{version}%{?prever}%{?gh_date:-dev}"; then
   : Error: Upstream YAC version is ${extver}, expecting %{version}%{?prever}%{?gh_date:-dev}.
   exit 1
fi
cd ..

# Drop in the bit of configuration
cat > %{ini_name} << 'EOF'
; Enable Yet Another Cache extension module
extension = %{pecl_name}.so

;yac.enable=1
;yac.enable_cli=0
;yac.debug=0
;yac.keys_memory_size=4M
;yac.values_memory_size=64M
;yac.compress_threshold=-1
EOF


%if %{with_zts}
# duplicate for ZTS build
cp -pr NTS ZTS
%endif


%build
peclconf() {
%configure \
%if %{with_fastlz}
    --with-system-fastlz \
%endif
    --with-php-config=$1
}

cd NTS
%{_bindir}/phpize
peclconf %{_bindir}/php-config
make %{?_smp_mflags}

%if %{with_zts}
cd ../ZTS
%{_bindir}/zts-phpize
peclconf %{_bindir}/zts-php-config
make %{?_smp_mflags}
%endif


%install
# Install the NTS stuff
make -C NTS install INSTALL_ROOT=%{buildroot}
install -D -m 644 %{ini_name} %{buildroot}%{php_inidir}/%{ini_name}

# Install XML package description
install -D -m 644 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml

# Install the ZTS stuff
%if %{with_zts}
make -C ZTS install INSTALL_ROOT=%{buildroot}
install -D -m 644 %{ini_name} %{buildroot}%{php_ztsinidir}/%{ini_name}
%endif

# Documentation
for i in README.md $(grep 'role="doc"' package.xml | sed -e 's/^.*name="//;s/".*$//')
do [ -f NTS/$i ] &&  install -Dpm 644 NTS/$i %{buildroot}%{pecl_docdir}/%{pecl_name}/$i
done


%check
sed -e 's/Catchable/%s/' -i ?TS/tests/005.phpt

cd NTS

: Minimal load test for NTS extension
%{_bindir}/php --no-php-ini \
    --define extension=%{buildroot}%{php_extdir}/%{pecl_name}.so \
    --modules | grep %{pecl_name}

%if %{with_tests}
: Upstream test suite for NTS extension
TEST_PHP_EXECUTABLE=%{__php} \
TEST_PHP_ARGS="-n -d extension_dir=$PWD/modules -d extension=%{pecl_name}.so" \
NO_INTERACTION=1 \
REPORT_EXIT_STATUS=1 \
%{__php} -n run-tests.php --show-diff
%else
: Upstream test suite disabled
%endif

%if %{with_zts}
cd ../ZTS

: Minimal load test for ZTS extension
%{__ztsphp} --no-php-ini \
    --define extension=%{buildroot}%{php_ztsextdir}/%{pecl_name}.so \
    --modules | grep %{pecl_name}

%if %{with_tests}
: Upstream test suite for ZTS extension
TEST_PHP_EXECUTABLE=%{__ztsphp} \
TEST_PHP_ARGS="-n -d extension_dir=$PWD/modules -d extension=%{pecl_name}.so" \
NO_INTERACTION=1 \
REPORT_EXIT_STATUS=1 \
%{__ztsphp} -n run-tests.php --show-diff
%else
: Upstream test suite disabled
%endif
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
    %{pecl_uninstall} %{pecl_name} >/dev/null || :
fi
%endif


%files
%{?_licensedir:%license NTS/LICENSE}
%doc %{pecl_docdir}/%{pecl_name}
%{pecl_xmldir}/%{name}.xml

%config(noreplace) %{php_inidir}/%{ini_name}
%{php_extdir}/%{pecl_name}.so

%if %{with_zts}
%{php_ztsextdir}/%{pecl_name}.so
%config(noreplace) %{php_ztsinidir}/%{ini_name}
%endif


%changelog
* Thu Dec  1 2016 Remi Collet <remi@fedoraproject.org> - 2.0.1-3
- rebuild with PHP 7.1.0 GA

* Wed Sep 14 2016 Remi Collet <remi@fedoraproject.org> - 2.0.1-2
- rebuild for PHP 7.1 new API version

* Sat Jul  2 2016 Remi Collet <remi@fedoraproject.org> - 2.0.1-1
- update to 2.0.1 (php 7)
- sources from pecl

* Sun Mar  6 2016 Remi Collet <remi@fedoraproject.org> - 2.0.0-2
- adapt for F24

* Tue Oct 27 2015 Remi Collet <remi@fedoraproject.org> - 2.0.0-1
- update to 2.0.0 (php 7)

* Tue Oct 13 2015 Remi Collet <remi@fedoraproject.org> - 0.9.3-0.6.20150908gita406e46
- rebuild for PHP 7.0.0RC5 new API version
- new snapshot

* Fri Sep 18 2015 Remi Collet <remi@fedoraproject.org> - 0.9.3-0.5.20150717git74fa8e2
- F23 rebuild with rh_layout

* Wed Jul 22 2015 Remi Collet <remi@fedoraproject.org> - 0.9.3-0.4.20150717git74fa8e2
- rebuild against php 7.0.0beta2

* Wed Jul  8 2015 Remi Collet <remi@fedoraproject.org> - 0.9.3-0.3.20150701git85f6e35
- rebuild against php 7.0.0beta1

* Wed Jun 24 2015 Remi Collet <remi@fedoraproject.org> - 0.9.3-0.2.20150616git1d26cd4
- rebuild for "rh_layout" (php70)

* Tue Jun 16 2015 Remi Collet <remi@fedoraproject.org> - 0.9.3-0.1.20150616git1d26cd4
- update to 0.9.3-dev for PHP 7
- sources from github

* Sun Mar  1 2015 Remi Collet <remi@fedoraproject.org> - 0.9.2-2
- drop runtime dependency on pear, new scriplets

* Wed Dec 24 2014 Remi Collet <remi@fedoraproject.org> - 0.9.2-1.1
- Fedora 21 SCL mass rebuild

* Sat Oct 25 2014 Remi Collet <remi@fedoraproject.org> - 0.9.2-1
- Update to 0.9.2

* Sat Sep  6 2014 Remi Collet <remi@fedoraproject.org> - 0.9.1-3
- test build with system fastlz
- don't install the tests

* Tue Aug 26 2014 Remi Collet <rcollet@redhat.com> - 0.9.1-2
- improve SCL build

* Fri Jul 25 2014 Remi Collet <remi@fedoraproject.org> - 0.9.1-1
- Update to 0.9.1 (beta)

* Thu Jul 24 2014 Remi Collet <remi@fedoraproject.org> - 0.9.0-1
- upstream move to pecl
- rename from php-yac to php-pecl-yac
- update to 0.9.0 (beta)

* Thu Apr 17 2014 Remi Collet <remi@fedoraproject.org> - 0.1.1-3
- add numerical prefix to extension configuration file (php 5.6)

* Tue Mar 25 2014 Remi Collet <remi@fedoraproject.org> - 0.1.1-2
- allow SCL build

* Sun Mar 16 2014 Remi Collet <remi@fedoraproject.org> - 0.1.1-1
- version 0.1.1

* Sat Mar 23 2013 Remi Collet <remi@fedoraproject.org> - 0.1.0-0.1.git57fe00d
- initial package, version 0.1.0 (experimental)

