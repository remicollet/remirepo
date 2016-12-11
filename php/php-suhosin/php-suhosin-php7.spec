# remirepo spec file for php-suhosin (from old fedora spec)
#
# Copyright (c) 2008-2016 Remi Collet
# Copyright (c) 2007-2009 Bart Vanbrabant
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please, preserve the changelog entries
#
%if 0%{?scl:1}
%global sub_prefix %{scl_prefix}
%endif

%global gh_commit    8a5f1a302a848b37ba737e7db3f618f309128700
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     sektioneins
%global gh_project   suhosin7
%global gh_date      20160307

%{?scl:          %scl_package         php-suhosin}

%global ext_name  suhosin7
# https://github.com/sektioneins/suhosin7/issues/4
%global with_zts  0%{!?_without_zts:%{?__ztsphp:1}}
%global ini_name  40-%{ext_name}.ini

Name:           %{?sub_prefix}php-suhosin
Version:        0.10.0
%if 0%{?gh_date}
Release:        0.3.%{gh_date}git%{gh_short}%{?dist}%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}-%{gh_short}.tar.gz
%else
Release:        1%{?dist}%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}
Source0:        http://download.suhosin.org/suhosin-%{version}.tar.gz
%endif

Summary:        Suhosin is an advanced protection system for PHP installations

Group:          Development/Languages
# The Mersenne Twister random number generator is BSD
# Suhosin is PHP variant, which is a BSD variant
License:        BSD
URL:            http://www.hardened-php.net/suhosin/

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  %{?scl_prefix}php-devel > 7

Requires:       %{?scl_prefix}php(zend-abi) = %{php_zend_api}
Requires:       %{?scl_prefix}php(api) = %{php_core_api}
%{?_sclreq:Requires: %{?scl_prefix}runtime%{?_sclreq}%{?_isa}}

## Compat SCL (rh-php56)
Provides:       %{?scl_prefix}php-suhosin          = %{version}-%{release}
Provides:       %{?scl_prefix}php-suhosin%{?_isa}  = %{version}-%{release}
Provides:       %{?scl_prefix}php-suhosin7         = %{version}-%{release}
Provides:       %{?scl_prefix}php-suhosin7%{?_isa} = %{version}-%{release}

%if "%{?vendor}" == "Remi Collet" && 0%{!?scl:1} && 0%{?rhel}
# Other third party repo stuff
Obsoletes:     php53-%{ext_name}   <= %{version}
Obsoletes:     php53u-%{ext_name}  <= %{version}
Obsoletes:     php54-%{ext_name}   <= %{version}
Obsoletes:     php54w-%{ext_name}  <= %{version}
Obsoletes:     php55u-%{ext_name}  <= %{version}
Obsoletes:     php55w-%{ext_name}  <= %{version}
Obsoletes:     php56u-%{ext_name}  <= %{version}
Obsoletes:     php56w-%{ext_name}  <= %{version}
Obsoletes:     php70u-%{ext_name}  <= %{version}
Obsoletes:     php70w-%{ext_name}  <= %{version}
Obsoletes:     php70u-%{ext_name}7 <= %{version}
Obsoletes:     php70w-%{ext_name}7 <= %{version}
%endif

%if 0%{?fedora} < 20 && 0%{?rhel} < 7
# Filter private shared
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}
%endif


%description
Suhosin is an advanced protection system for PHP installations. It was designed
to protect servers and users from known and unknown flaws in PHP applications
and the PHP core.

WARNING: THIS SOFTWARE IS PRE-ALPHA SOFTWARE. DO NOT ATTEMPT TO RUN IN PRODUCTION

Package built for PHP %(%{__php} -r 'echo PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')%{?scl: as Software Collection (%{scl} by %{?scl_vendor}%{!?scl_vendor:rh})}.


%prep
%setup -q -c
%if 0%{?gh_commit:1}
mv %{ext_name}-%{gh_commit} NTS
%else
mv %{ext_name}-%{version} NTS
%endif

cd NTS
# Check extension version
ver=$(sed -n '/SUHOSIN7_EXT_VERSION/{s/.* "//;s/".*$//;p}' php_suhosin7.h)
if test "$ver" != "%{version}%{?gh_date:dev}"; then
   : Error: Upstream SUHOSIN_EXT_VERSION version is ${ver}, expecting %{version}%{?gh_date:dev}.
   exit 1
fi
cd ..

%if %{with_zts}
# Duplicate source tree for NTS / ZTS build
cp -pr NTS ZTS
%endif

cat << EOF | tee %{ini_name}
; Enable %{summary}
extension=%{ext_name}.so

; Configuration options
; See https://suhosin.org/stories/configuration.html
EOF


%build
# https://github.com/sektioneins/suhosin7/pull/7
sed -e s/c11/c99/ -i ?TS/config.m4

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
rm -rf %{buildroot}

make -C NTS install INSTALL_ROOT=%{buildroot}

# install configuration
install -Dpm 644 %{ini_name} %{buildroot}%{php_inidir}/%{ini_name}

%if %{with_zts}
make -C ZTS install INSTALL_ROOT=%{buildroot}
install -Dpm 644 %{ini_name} %{buildroot}%{php_ztsinidir}/%{ini_name}
%endif


%check
: Minimal load test for NTS extension
%{__php} --no-php-ini \
    --define extension=%{buildroot}%{php_extdir}/%{ext_name}.so \
    --modules | grep suhosin7

%if %{with_zts}
: Minimal load test for NTS extension
%{__ztsphp} --no-php-ini \
    --define extension=%{buildroot}%{php_ztsextdir}/%{ext_name}.so \
    --modules | grep suhosin7
%endif

: Upstream test suite for NTS extension
cd NTS

# drop known to fail tests
TEST_PHP_EXECUTABLE=%{__php} \
TEST_PHP_ARGS="-n -d extension=%{buildroot}%{php_extdir}/%{ext_name}.so" \
REPORT_EXIT_STATUS=1 \
NO_INTERACTION=1 \
%{__php} -n run-tests.php --show-diff


%clean
rm -rf %{buildroot}


%posttrans
cat << EOF
==========================================================================
 WARNING:
 %{name} IS PRE-ALPHA SOFTWARE. DO NOT ATTEMPT TO RUN IN PRODUCTION
==========================================================================
EOF


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license NTS/LICENSE
%doc NTS/{CREDITS,*.md}

%config(noreplace) %{php_inidir}/%{ini_name}
%{php_extdir}/%{ext_name}.so

%if %{with_zts}
%config(noreplace) %{php_ztsinidir}/%{ini_name}
%{php_ztsextdir}/%{ext_name}.so
%endif


%changelog
* Fri Mar 11 2016 Remi Collet <remi@fedoraproject.org> - 0.10.0-0.3.20160307git8a5f1a3
- refresh

* Fri Mar  4 2016 Remi Collet <remi@fedoraproject.org> - 0.10.0-0.2.20160304git5c0b5f3
- refresh
- open https://github.com/sektioneins/suhosin7/pull/7 - gcc < 4.8
- enable ZTS build

* Thu Mar  3 2016 Remi Collet <remi@fedoraproject.org> - 0.10.0-0.1.20160303git6eb6633
- update to 0.10.0 for php 7
- open https://github.com/sektioneins/suhosin7/issues/1 - License
- open https://github.com/sektioneins/suhosin7/issues/2 - suhosin.ini
- open https://github.com/sektioneins/suhosin7/issues/3 - gcc < 5
- open https://github.com/sektioneins/suhosin7/issues/4 - ZTS

* Mon Jun 22 2015 Remi Collet <rcollet@redhat.com> - 0.9.38-3
- add virtual "rh-php56" provides

* Sat Jun 20 2015 Remi Collet <remi@fedoraproject.org> - 0.9.38-2
- allow build against rh-php56 (as more-php56)

* Fri May 22 2015 Remi Collet <remi@fedoraproject.org> - 0.9.38-1
- update to 0.9.38

* Wed Dec 24 2014 Remi Collet <remi@fedoraproject.org> - 0.9.37.1-1.1
- Fedora 21 SCL mass rebuild

* Mon Dec 15 2014 Remi Collet <remi@fedoraproject.org> - 0.9.37.1-1
- update to 0.9.37.1

* Wed Dec  3 2014 Remi Collet <remi@fedoraproject.org> - 0.9.37-1
- update to 0.9.37

* Mon Nov 24 2014 Remi Collet <remi@fedoraproject.org> - 0.9.37-0.1.0fa87e1
- update to 0.9.37RC1
- fix license handling

* Tue Aug 26 2014 Remi Collet <rcollet@redhat.com> - 0.9.36-2
- improve SCL build

* Wed Jun 11 2014 Remi Collet <remi@fedoraproject.org> - 0.9.36-1
- update to 0.9.36

* Thu Apr 17 2014 Remi Collet <remi@fedoraproject.org> - 0.9.35-2
- add numerical prefix to extension configuration file (php 5.6)

* Mon Mar 24 2014 Remi Collet <remi@fedoraproject.org> 0.9.35-1
- update to 0.9.35 for php >= 5.4
- add ZTS build
- add missing LICENSE file
- allow SCL build
- don't ignore test results, just drop a few tests

* Tue Jul 27 2010 Remi Collet <rpms@famillecollet.com> 0.9.32.1-1
- update to 0.9.32.1

* Tue Mar  2 2010 Remi Collet <rpms@famillecollet.com> 0.9.29-3.el5.remi
- rebuild to have remi's EVR > epel's EVR

* Sat Oct 31 2009 Bart Vanbrabant <bart.vanbrabant@zoeloelip.be> - 0.9.29-1
Update to version 0.9.29
- Fixing crash bugs with PHP 5.3.0 caused by unexpected NULL in 
  EG(active_symbol_table)
- Added more compatible way to retrieve ext/session globals
- Increased default length and count limit for POST variables 
  (for people not reading docu)
- Fixed crash bug with PHP 5.2.10 caused by a change in extension 
  load order of ext/session
- Fixed harmless parameter order error in a bogus memset()
- Disable suhosin.session.cryptua by default because of 
  Internet Explorer 8 "features"
- Added suhosin.executor.include.allow_writable_files which can be 
  disabled to disallow inclusion of files writable by the webserver

* Thu Sep 18 2008 Remi Collet <rpms@famillecollet.com> 0.9.27-1.fc9.remi.1
- rebuild for php 5.3.0-dev

* Thu Sep 18 2008 Remi Collet <rpms@famillecollet.com> 0.9.27-1.###.remi
- rebuild for php 5.2.6 all FC/EL version

* Tue Aug 26 2008 Bart Vanbrabant <bart.vanbrabant@zoeloelip.be> 0.9.27-1
- Update to version 0.9.27

* Thu Aug 7 2008 Bart Vanbrabant <bart.vanbrabant@zoeloelip.be> 0.9.25-1
- Update to version 0.9.25

* Wed Jun 18 2008 Bart Vanbrabant <bart.vanbrabant@zoeloelip.be> 0.9.24-1
- Update to version 0.9.24

* Tue Apr 29 2008 Bart Vanbrabant <bart.vanbrabant@zoeloelip.be> 0.9.23-1
- Update to version 0.9.23
- Some specfile updates for review

* Fri Jan 4 2008 Bart Vanbrabant <bart.vanbrabant@zoeloelip.be> 0.9.22-2
- Use short name for license

* Wed Dec 5 2007 Bart Vanbrabant <bart.vanbrabant@zoeloelip.be> 0.9.22-1
- Initial packaging of 0.9.22
