# remirepo spec file for php-pecl-yaf
#
# Copyright (c) 2012-2016 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%if 0%{?scl:1}
%global sub_prefix %{scl_prefix}
%scl_package       php-pecl-yaf
%endif

%global gh_commit   51e458e9746d7061efc565d49baaca26feacd7ff
%global gh_short    %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner    laruence
%global gh_project  yaf
#global gh_date     20150914
%global with_zts    0%{!?_without_zts:%{?__ztsphp:1}}
%global pecl_name   yaf
%global ini_name    40-%{pecl_name}.ini

Summary:       Yet Another Framework
Name:          %{?sub_prefix}php-pecl-yaf
Version:       3.0.4
%if 0%{?gh_date:1}
Release:       0.8.%{gh_date}git%{gh_short}%{?dist}%{!?scl:%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}}
Source0:       https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{pecl_name}-%{version}-%{gh_short}.tar.gz
%else
Release:       1%{?dist}%{!?scl:%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}}
Source:        http://pecl.php.net/get/%{pecl_name}-%{version}%{?prever}.tgz
%endif
License:       PHP
Group:         Development/Languages
URL:           http://pecl.php.net/package/yaf
Source1:       %{pecl_name}.ini

BuildRequires: %{?scl_prefix}php-devel >= 7
BuildRequires: %{?scl_prefix}php-pear
BuildRequires: pcre-devel

Requires:      %{?scl_prefix}php(zend-abi) = %{php_zend_api}
Requires:      %{?scl_prefix}php(api) = %{php_core_api}
%{?_sclreq:Requires: %{?scl_prefix}runtime%{?_sclreq}%{?_isa}}

Provides:      %{?scl_prefix}php-%{pecl_name}               = %{version}
Provides:      %{?scl_prefix}php-%{pecl_name}%{?_isa}       = %{version}
Provides:      %{?scl_prefix}php-pecl(%{pecl_name})         = %{version}
Provides:      %{?scl_prefix}php-pecl(%{pecl_name})%{?_isa} = %{version}
%if "%{?scl_prefix}" != "%{?sub_prefix}"
Provides:      %{?scl_prefix}php-pecl-%{pecl_name}          = %{version}-%{release}
Provides:      %{?scl_prefix}php-pecl-%{pecl_name}%{?_isa}  = %{version}-%{release}
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
The Yet Another Framework (Yaf) extension is a PHP framework that is used
to develop web applications. 

Package built for PHP %(%{__php} -r 'echo PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')%{?scl: as Software Collection (%{scl} by %{?scl_vendor}%{!?scl_vendor:rh})}.


%prep
%setup -qc
%if 0%{?gh_date:1}
mv %{gh_project}-%{gh_commit} NTS
mv NTS/package.xml .
%else
mv %{pecl_name}-%{version} NTS
%endif

# Don't install/register tests
sed -e 's/role="test"/role="src"/' \
    %{?_licensedir:-e '/LICENSE/s/role="doc"/role="src"/' } \
    -i package.xml

cd NTS

# Sanity check, really often broken
extver=$(sed -n '/#define PHP_YAF_VERSION/{s/.*\t"//;s/".*$//;p}' php_yaf.h )
if test "x${extver}" != "x%{version}%{?gh_date:-dev}"; then
   : Error: Upstream extension version is ${extver}, expecting %{version}%{?gh_date:-dev}.
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
install -D -m 644 %{SOURCE1} %{buildroot}%{php_inidir}/%{ini_name}

# Install the ZTS stuff
%if %{with_zts}
make -C ZTS install INSTALL_ROOT=%{buildroot}
install -D -m 644 %{SOURCE1} %{buildroot}%{php_ztsinidir}/%{ini_name}
%endif

# Install the package XML file
install -D -m 644 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml

# Documentation
for i in $(grep 'role="doc"' package.xml | sed -e 's/^.*name="//;s/".*$//')
do install -Dpm 644 NTS/$i %{buildroot}%{pecl_docdir}/%{pecl_name}/$i
done


%check
cd NTS
: Minimal load test for NTS extension
%{__php} --no-php-ini \
    --define extension=%{buildroot}%{php_extdir}/%{pecl_name}.so \
    --modules | grep %{pecl_name}

: Upstream test suite  for NTS extension
TEST_PHP_EXECUTABLE=%{__php} \
TEST_PHP_ARGS="-n -d extension_dir=$PWD/modules -d extension=%{pecl_name}.so" \
NO_INTERACTION=1 \
REPORT_EXIT_STATUS=1 \
%{__php} -n run-tests.php --show-diff

%if %{with_zts}
cd ../ZTS
# https://github.com/laruence/php-yaf/issues/180
rm tests/016.phpt

: Minimal load test for ZTS extension
%{__ztsphp} --no-php-ini \
    --define extension=%{buildroot}%{php_ztsextdir}/%{pecl_name}.so \
    --modules | grep %{pecl_name}

: Upstream test suite  for NTS extension
TEST_PHP_EXECUTABLE=%{__ztsphp} \
TEST_PHP_ARGS="-n -d extension_dir=$PWD/modules -d extension=%{pecl_name}.so" \
NO_INTERACTION=1 \
REPORT_EXIT_STATUS=1 \
%{__ztsphp} -n run-tests.php --show-diff
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
* Thu Sep  1 2016 Remi Collet <remi@fedoraproject.org> - 3.0.4-1
- update to 3.0.4

* Sat Jul  2 2016 Remi Collet <remi@fedoraproject.org> - 3.0.3-1
- update to 3.0.3
- drop patch merged upstream

* Sat Jun 11 2016 Remi Collet <remi@fedoraproject.org> - 3.0.2-3
- add patch for PHP 7.1
  open https://github.com/laruence/yaf/pull/289

* Sun Mar  6 2016 Remi Collet <remi@fedoraproject.org> - 3.0.2-2
- adapt for F24

* Mon Dec 28 2015 Remi Collet <remi@fedoraproject.org> - 3.0.2-1
- update to 3.0.2 (beta, php 7)

* Sun Dec 13 2015 Remi Collet <remi@fedoraproject.org> - 3.0.1-1
- update to 3.0.1 (beta, php 7)

* Tue Oct 27 2015 Remi Collet <remi@fedoraproject.org> - 3.0.0-1
- update to 3.0.0 (php 7)

* Tue Oct 13 2015 Remi Collet <remi@fedoraproject.org> - 3.0.0-0.8.20150914gitaeb6457
- rebuild for PHP 7.0.0RC5 new API version
- new snapshot

* Sun Sep  6 2015 Remi Collet <remi@fedoraproject.org> - 3.0.0-0.7.20150906git63222a2
- new shapshot (changes from 2.3.5)

* Thu Aug 13 2015 Remi Collet <remi@fedoraproject.org> - 3.0.0-0.6.20150813git2dd49ab
- new shapshot

* Fri Jul 24 2015 Remi Collet <remi@fedoraproject.org> - 3.0.0-0.6.20150720git629d412
- ignore 1 failed test on ZTS
- open https://github.com/laruence/php-yaf/issues/180 (1 failed on ZTS)

* Wed Jul 22 2015 Remi Collet <remi@fedoraproject.org> - 3.0.0-0.5.20150720git629d412
- rebuild against php 7.0.0beta2

* Wed Jul  8 2015 Remi Collet <remi@fedoraproject.org> - 3.0.0-0.4.20150701gitfb20f6c
- rebuild against php 7.0.0beta1

* Wed Jun 24 2015 Remi Collet <remi@fedoraproject.org> - 3.0.0-0.3.20150618gita40f01e
- new snapshot
- rebuild for "rh_layout"

* Wed Jun 17 2015 Remi Collet <remi@fedoraproject.org> - 3.0.0-0.2.20150612gita1bd3ac
- rebuild

* Fri Jun 12 2015 Remi Collet <remi@fedoraproject.org> - 3.0.0-0.1.20150612gita1bd3ac
- Update to 3.0.0-dev for PHP 7
- sources from github
- drop runtime dependency on pear, new scriptlets

* Wed Dec 24 2014 Remi Collet <remi@fedoraproject.org> - 2.3.3-1.1
- Fedora 21 SCL mass rebuild

* Sat Oct 25 2014 Remi Collet <remi@fedoraproject.org> - 2.3.3-1
- Update to 2.3.3

* Tue Aug 26 2014 Remi Collet <rcollet@redhat.com> - 2.3.2-4
- improve SCL build

* Thu Jun 26 2014 Remi Collet <remi@fedoraproject.org> - 2.3.2-3
- upstream patch for PHP 5.6

* Thu Apr 17 2014 Remi Collet <remi@fedoraproject.org> - 2.3.2-2
- add numerical prefix to extension configuration file (php 5.6)

* Thu Jan 09 2014 Remi Collet <remi@fedoraproject.org> - 2.3.2-1
- Update to 2.3.2 (beta)

* Wed Jan 08 2014 Remi Collet <remi@fedoraproject.org> - 2.3.1-1
- Update to 2.3.1 (beta)

* Wed Jan 08 2014 Remi Collet <remi@fedoraproject.org> - 2.3.0-1
- Update to 2.3.0 (beta)
- install doc in pecl doc_dir
- install tests in pecl test_dir
- adapt for SCL
- add missing files from upstream git repo
  https://github.com/laruence/php-yaf/issues/82

* Fri Jan  4 2013 Remi Collet <remi@fedoraproject.org> - 2.2.9-1
- version 2.2.9 (stable)

* Tue Dec 18 2012 Remi Collet <remi@fedoraproject.org> - 2.2.8-1
- version 2.2.8 (stable)

* Mon Nov 19 2012 Remi Collet <remi@fedoraproject.org> - 2.2.7-1
- version 2.2.7 (stable)

* Thu Nov  1 2012 Remi Collet <remi@fedoraproject.org> - 2.2.6-1
- version 2.2.6 (stable)

* Mon Oct 22 2012 Remi Collet <remi@fedoraproject.org> - 2.2.5-1
- version 2.2.5 (stable)
- LICENSE now provided by upstream

* Tue Sep  4 2012 Remi Collet <remi@fedoraproject.org> - 2.2.4-1
- version 2.2.4 (beta)
- initial package
