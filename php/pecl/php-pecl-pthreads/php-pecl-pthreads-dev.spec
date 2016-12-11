# remirepo spec file for php-pecl-pthreads
#
# Copyright (c) 2013-2016 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%{?scl:          %scl_package        php-pecl-pthreads}

%global pecl_name   pthreads
%global ini_name    40-%{pecl_name}.ini
# https://github.com/krakjoe/pthreads/commits/master
%global gh_commit   959ab0ff5fbd59d29a9d77f0309065cdfe62531f
%global gh_short    %(c=%{gh_commit}; echo ${c:0:7})
%global gh_date     20161111
%global gh_owner    krakjoe
%global gh_project  pthreads

Summary:        Threading API
Name:           %{?scl_prefix}php-pecl-%{pecl_name}
Version:        3.1.7
%if 0%{?gh_date:1}
Release:        0.4.%{gh_date}git%{gh_short}%{?dist}%{!?scl:%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}}
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{pecl_name}-%{version}-%{gh_short}.tar.gz
%else
Release:        2%{?dist}%{!?scl:%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}}
Source0:        http://pecl.php.net/get/%{pecl_name}-%{version}.tgz
%endif
License:        PHP
Group:          Development/Languages
URL:            http://pecl.php.net/package/%{pecl_name}

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  %{?scl_prefix}php-zts-devel > 7
BuildRequires:  %{?scl_prefix}php-pear

Requires:       %{?scl_prefix}php(zend-abi) = %{php_zend_api}
Requires:       %{?scl_prefix}php(api) = %{php_core_api}
%{?_sclreq:Requires: %{?scl_prefix}runtime%{?_sclreq}%{?_isa}}

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
# Filter shared private
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}
%endif


%description
A compatible Threading API for PHP.

Documentation: http://php.net/pthreads

This extension is only available for PHP in ZTS mode.

Package built for PHP %(%{__php} -r 'echo PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')%{?scl: as Software Collection (%{scl} by %{?scl_vendor}%{!?scl_vendor:rh})}.


%prep
%setup -q -c
%if 0%{?gh_date:1}
mv %{gh_project}-%{gh_commit} ZTS
%{__php} -r '
  $pkg = simplexml_load_file("ZTS/package.xml");
  $pkg->date = substr("%{gh_date}",0,4)."-".substr("%{gh_date}",4,2)."-".substr("%{gh_date}",6,2);
  $pkg->version->release = "%{version}dev";
  $pkg->stability->release = "devel";
  $pkg->asXML("package.xml");
'
%else
mv %{pecl_name}-%{version} ZTS
%endif

# Don't install/register tests
sed -e 's/role="test"/role="src"/' \
    %{?_licensedir:-e '/LICENSE/s/role="doc"/role="src"/' } \
    -i package.xml

cd ZTS

# Sanity check, really often broken
extver=$(sed -n '/#define PHP_PTHREADS_VERSION/{s/.* "//;s/".*$//;p}' php_pthreads.h)
if test "x${extver}" != "x%{version}%{?gh_date:dev}"; then
   : Error: Upstream extension version is ${extver}, expecting %{version}%{?gh_date:dev}.
   exit 1
fi
cd ..

# Create configuration file
cat > %{ini_name} << 'EOF'
; Enable %{pecl_name} extension module
extension=%{pecl_name}.so
EOF


%build
cd ZTS
%{_bindir}/zts-phpize
%configure \
    --with-php-config=%{_bindir}/zts-php-config
make %{?_smp_mflags}


%install
rm -rf %{buildroot}

make -C ZTS install INSTALL_ROOT=%{buildroot}

# install config file
install -D -m 644 %{ini_name} %{buildroot}%{php_ztsinidir}/%{ini_name}

# Install XML package description
install -D -m 644 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml

# Documentation
cd ZTS
for i in $(grep 'role="doc"' ../package.xml | sed -e 's/^.*name="//;s/".*$//')
do sed -e 's/\r//' -i $i
   install -Dpm 644 $i %{buildroot}%{pecl_docdir}/%{pecl_name}/$i
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
cd ZTS
%ifnarch x86_64
rm tests/trait-alias-bug.phpt
%endif

: Minimal load test for ZTS extension
%{__ztsphp} --no-php-ini \
    --define extension=%{buildroot}%{php_ztsextdir}/%{pecl_name}.so \
    --modules | grep %{pecl_name}

: Upstream test suite  for ZTS extension
TEST_PHP_EXECUTABLE=%{_bindir}/zts-php \
TEST_PHP_ARGS="-n -d extension=$PWD/modules/%{pecl_name}.so" \
NO_INTERACTION=1 \
REPORT_EXIT_STATUS=1 \
%{_bindir}/zts-php -n run-tests.php --show-diff


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{?_licensedir:%license ZTS/LICENSE}
%doc %{pecl_docdir}/%{pecl_name}
%{pecl_xmldir}/%{name}.xml

%config(noreplace) %{php_ztsinidir}/%{ini_name}
%{php_ztsextdir}/%{pecl_name}.so


%changelog
* Mon Dec  5 2016 Remi Collet <remi@fedoraproject.org> - 3.1.7-0.4.20161111git959ab0f
- refresh with a newer snapshot

* Thu Dec  1 2016 Remi Collet <remi@fedoraproject.org> - 3.1.7-0.3.20160529gitd814b0c
- rebuild with PHP 7.1.0 GA

* Thu Sep 15 2016 Remi Collet <remi@fedoraproject.org> - 3.1.7-0.2.20160529gitd814b0c
- rebuild for PHP 7.1 new API version

* Sat Jul 23 2016 Remi Collet <remi@fedoraproject.org> - 3.1.7-0.1.20160529gitd814b0c
- update to 3.1.7dev for PHP 7.1

* Sat Feb 13 2016 Remi Collet <remi@fedoraproject.org> - 3.1.6-1
- Update to 3.1.6 (stable)

* Sun Dec  6 2015 Remi Collet <remi@fedoraproject.org> - 3.1.5-1
- Update to 3.1.5 (stable)

* Wed Dec  2 2015 Remi Collet <remi@fedoraproject.org> - 3.1.4-2
- add upstream patch to fix segfault on i386
  https://github.com/krakjoe/pthreads/issues/523

* Wed Dec  2 2015 Remi Collet <remi@fedoraproject.org> - 3.1.4-1
- Update to 3.1.4 (stable)

* Wed Nov 25 2015 Remi Collet <remi@fedoraproject.org> - 3.1.3-1
- Update to 3.1.3 (stable)
- open https://github.com/krakjoe/pthreads/issues/523 segfault on i386

* Wed Oct  7 2015 Remi Collet <remi@fedoraproject.org> - 3.0.8-1
- Update to 3.0.8 (stable)

* Sun Sep 27 2015 Remi Collet <remi@fedoraproject.org> - 3.0.7-1
- Update to 3.0.7 (stable)

* Tue Sep 22 2015 Remi Collet <remi@fedoraproject.org> - 3.0.6-1
- Update to 3.0.6 (stable)

* Mon Sep 21 2015 Remi Collet <remi@fedoraproject.org> - 3.0.5-1
- Update to 3.0.5 (stable)

* Fri Sep 18 2015 Remi Collet <remi@fedoraproject.org> - 3.0.4-1
- Update to 3.0.4 (stable)

* Thu Sep 17 2015 Remi Collet <remi@fedoraproject.org> - 3.0.3-1
- Update to 3.0.3 (stable)

* Sun Sep 13 2015 Remi Collet <remi@fedoraproject.org> - 3.0.2-1
- Update to 3.0.2 (stable)

* Thu Sep 10 2015 Remi Collet <remi@fedoraproject.org> - 3.0.1-1
- Update to 3.0.1 (stable)

* Thu Sep 10 2015 Remi Collet <remi@fedoraproject.org> - 3.0.0-1
- Update to 3.0.0 (stable)
- raise minimum PHP version to 7

* Wed Oct 01 2014 Remi Collet <remi@fedoraproject.org> - 2.0.10-1
- Update to 2.0.10 (stable)

* Wed Sep 24 2014 Remi Collet <remi@fedoraproject.org> - 2.0.9-1
- Update to 2.0.9 (stable)

* Mon Sep 15 2014 Remi Collet <remi@fedoraproject.org> - 2.0.8-1
- Update to 2.0.8 (stable)

* Sun May 11 2014 Remi Collet <remi@fedoraproject.org> - 2.0.7-1
- Update to 2.0.7 (stable)

* Sat May 10 2014 Remi Collet <remi@fedoraproject.org> - 2.0.5-1
- Update to 2.0.5 (stable)
- add numerical prefix to extension configuration file

* Sun Mar 30 2014 Remi Collet <remi@fedoraproject.org> - 2.0.4-1
- Update to 2.0.4 (stable)

* Thu Mar 27 2014 Remi Collet <remi@fedoraproject.org> - 2.0.3-1
- Update to 2.0.3 (stable)
- allow SCL build, even if php54 and php55 don't have ZTS

* Fri Mar 21 2014 Remi Collet <remi@fedoraproject.org> - 2.0.2-1
- Update to 2.0.2 (stable)

* Mon Mar 17 2014 Remi Collet <remi@fedoraproject.org> - 2.0.1-1
- Update to 2.0.1 (stable)
- open https://github.com/krakjoe/pthreads/issues/262
  segfault in test suite

* Fri Mar 14 2014 Remi Collet <remi@fedoraproject.org> - 2.0.0-1
- Update to 2.0.0 (stable)
- open https://github.com/krakjoe/pthreads/issues/258
  tests/pools.phpt use PHP 5.5 syntax

* Sun Mar 09 2014 Remi Collet <remi@fedoraproject.org> - 1.0.1-1
- Update to 1.0.1 (stable)
- open https://github.com/krakjoe/pthreads/pull/251
  fix build + fix warnings

* Fri Mar 07 2014 Remi Collet <remi@fedoraproject.org> - 1.0.0-2
- rebuild with new sources :(
- open https://github.com/krakjoe/pthreads/pull/249
  fix test suite for PHP 5.4, and clean build warnings

* Fri Mar 07 2014 Remi Collet <remi@fedoraproject.org> - 1.0.0-1
- Update to 1.0.0 (stable)

* Sat Jan 18 2014 Remi Collet <remi@fedoraproject.org> - 0.1.0-1
- Update to 0.1.0 (stable)

* Sat Oct 26 2013 Remi Collet <remi@fedoraproject.org> - 0.0.45-1
- initial package, version 0.0.45 (stable)
  open https://github.com/krakjoe/pthreads/pull/193
