# remirepo spec file for php-pecl-solr2
# with SCL compatibility, from Fedora:
#
# Fedora spec file for php-pecl-solr2
#
# Copyright (c) 2011-2016 Remi Collet
# Copyright (c) 2010 Johan Cwiklinski
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%if 0%{?scl:1}
%scl_package       php-pecl-solr2
%global sub_prefix %{scl_prefix}
%endif

%global pecl_name solr
#global prever    b
%global with_zts  0%{!?_without_zts:%{?__ztsphp:1}}
%if "%{php_version}" < "5.6"
# After curl, json
%global ini_name  %{pecl_name}.ini
%else
# After 20-curl, 40-json
%global ini_name  50-%{pecl_name}.ini
%endif
# For full test (using localhost server) use --with tests
# retrieve: docker pull omars/solr53
# create:   docker run -d -p 8983:8983 --name solr5 -t omars/solr53
# cleanup:  docker stop solr5 && docker rm solr5
%global with_tests 0%{?_with_tests:1}

Summary:        Object oriented API to Apache Solr
Summary(fr):    API orientée objet pour Apache Solr
Name:           %{?sub_prefix}php-pecl-solr2
Version:        2.4.0
Release:        3%{?dist}%{!?scl:%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}}
License:        PHP
Group:          Development/Languages
URL:            http://pecl.php.net/package/solr

Source0:        http://pecl.php.net/get/%{pecl_name}-%{version}%{?prever}.tgz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  %{?scl_prefix}php-devel
BuildRequires:  %{?scl_prefix}php-pear
BuildRequires:  %{?scl_prefix}php-curl
BuildRequires:  %{?scl_prefix}php-json
BuildRequires:  curl-devel
BuildRequires:  libxml2-devel
BuildRequires:  pcre-devel

Requires:       %{?scl_prefix}php(zend-abi) = %{php_zend_api}
Requires:       %{?scl_prefix}php(api) = %{php_core_api}
Requires:       %{?scl_prefix}php-curl%{?_isa}
Requires:       %{?scl_prefix}php-json%{?_isa}
%{?_sclreq:Requires: %{?scl_prefix}runtime%{?_sclreq}%{?_isa}}

Provides:       %{?scl_prefix}php-%{pecl_name}               = %{version}
Provides:       %{?scl_prefix}php-%{pecl_name}%{?_isa}       = %{version}
Provides:       %{?scl_prefix}php-pecl(%{pecl_name})         = %{version}
Provides:       %{?scl_prefix}php-pecl(%{pecl_name})%{?_isa} = %{version}
Provides:       %{?scl_prefix}php-pecl-%{pecl_name}          = %{version}-%{release}
Provides:       %{?scl_prefix}php-pecl-%{pecl_name}%{?_isa}  = %{version}-%{release}
%if "%{?scl_prefix}" != "%{?sub_prefix}"
Provides:       %{?scl_prefix}php-pecl-%{pecl_name}2         = %{version}-%{release}
Provides:       %{?scl_prefix}php-pecl-%{pecl_name}2%{?_isa} = %{version}-%{release}
%endif
%if "%{php_version}" > "7.0"
Obsoletes:      %{?sub_prefix}php-pecl-%{pecl_name}          < 2
Provides:       %{?sub_prefix}php-pecl-%{pecl_name}          = %{version}-%{release}
Provides:       %{?sub_prefix}php-pecl-%{pecl_name}%{?_isa}  = %{version}-%{release}
%else
# Only one version of the extension
Conflicts:      %{?sub_prefix}php-pecl-%{pecl_name}          < 2
Conflicts:      %{?scl_prefix}php-pecl-%{pecl_name}          < 2
%endif

%if "%{?vendor}" == "Remi Collet" && 0%{!?scl:1}
Obsoletes:     php53-pecl-%{pecl_name}2  <= %{version}
Obsoletes:     php53u-pecl-%{pecl_name}2 <= %{version}
Obsoletes:     php54-pecl-%{pecl_name}2  <= %{version}
Obsoletes:     php54w-pecl-%{pecl_name}2 <= %{version}
%if "%{php_version}" > "5.5"
Obsoletes:     php55u-pecl-%{pecl_name}2 <= %{version}
Obsoletes:     php55w-pecl-%{pecl_name}2 <= %{version}
%endif
%if "%{php_version}" > "5.6"
Obsoletes:     php56u-pecl-%{pecl_name}2 <= %{version}
Obsoletes:     php56w-pecl-%{pecl_name}2 <= %{version}
%endif
%if "%{php_version}" > "7.0"
Obsoletes:     php70u-pecl-%{pecl_name}  <= %{version}
Obsoletes:     php70w-pecl-%{pecl_name}  <= %{version}
Obsoletes:     php70u-pecl-%{pecl_name}2 <= %{version}
Obsoletes:     php70w-pecl-%{pecl_name}2 <= %{version}
%endif
%if "%{php_version}" > "7.1"
Obsoletes:     php71u-pecl-%{pecl_name}  <= %{version}
Obsoletes:     php71w-pecl-%{pecl_name}  <= %{version}
Obsoletes:     php71u-pecl-%{pecl_name}2 <= %{version}
Obsoletes:     php71w-pecl-%{pecl_name}2 <= %{version}
%endif
%endif

%if 0%{?fedora} < 20 && 0%{?rhel} < 7
# Filter shared private
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}
%endif


%description
It effectively simplifies the process of interacting with Apache Solr using
PHP5 and it already comes with built-in readiness for the latest features.

The extension has features such as built-in, serializable query string builder
objects which effectively simplifies the manipulation of name-value pair
request parameters across repeated requests.

The response from the Solr server is also automatically parsed into native php
objects whose properties can be accessed as array keys or object properties
without any additional configuration on the client-side.

Its advanced HTTP client reuses the same connection across multiple requests
and provides built-in support for connecting to Solr servers secured behind
HTTP Authentication or HTTP proxy servers. It is also able to connect to
SSL-enabled containers.

Please consult the documentation for more details on features.
  http://php.net/solr

Warning: PECL Solr 2 is not compatible with Solr Server < 4.0
PECL Solr 1 is available in php-pecl-solr package.

Package built for PHP %(%{__php} -r 'echo PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')%{?scl: as Software Collection (%{scl} by %{?scl_vendor}%{!?scl_vendor:rh})}.


%prep
%setup -c -q

# Don't install/register tests
sed -e 's/role="test"/role="src"/' \
    %{?_licensedir:-e '/LICENSE/s/role="doc"/role="src"/' } \
    -i package.xml

mv %{pecl_name}-%{version}%{?prever} NTS

cd NTS

# Check version
DIR=src/php$(%{__php} -r 'echo PHP_MAJOR_VERSION;')
extver=$(sed -n '/#define PHP_SOLR_VERSION /{s/.* "//;s/".*$//;p}' $DIR/php_solr_version.h)
if test "x${extver}" != "x%{version}%{?prever}"; then
   : Error: Upstream version is ${extver}, expecting %{version}%{?prever}.
   exit 1
fi

cd ..

# Create configuration file
cat > %{ini_name} << 'EOF'
; Enable Solr extension module
extension=%{pecl_name}.so
EOF

%if %{with_zts}
cp -r NTS ZTS
%endif


%build
cd NTS
%{_bindir}/phpize
%configure  --with-php-config=%{_bindir}/php-config
make %{?_smp_mflags}

%if %{with_zts}
cd ../ZTS
%{_bindir}/zts-phpize
%configure  --with-php-config=%{_bindir}/zts-php-config
make %{?_smp_mflags}
%endif


%install
rm -rf %{buildroot}

make -C NTS install INSTALL_ROOT=%{buildroot}

# Install XML package description
install -D -m 644 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml

# install config file
install -D -m 644 %{ini_name} %{buildroot}%{php_inidir}/%{ini_name}

%if %{with_zts}
make -C ZTS install INSTALL_ROOT=%{buildroot}
install -D -m 644 %{ini_name} %{buildroot}%{php_ztsinidir}/%{ini_name}
%endif


# Documentation
for i in $(grep 'role="doc"' package.xml | sed -e 's/^.*name="//;s/".*$//')
do install -Dpm 644 NTS/$i %{buildroot}%{pecl_docdir}/%{pecl_name}/$i
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
: Ignore test with jsonc before 1.3.9
%{__php} -r '
  $v=phpversion("json");
  exit(version_compare($v,"1.3.0",">=") && version_compare($v,"1.3.9","<") ? 0 : 1);
' && rm ?TS/tests/bug_67394.phpt

: Ignore test with old PHP 5.3
%if "%{php_version}" < "5.4"
  rm ?TS/tests/151.solrcollapsefunction_illegal_operations.phpt
%endif

%if %{with_tests}
sed -e '/SOLR_SERVER_CONFIGURED/s/false/true/' \
    -e '/SOLR_SERVER_HOSTNAME/s/solr5/localhost/' \
    -i ?TS/tests/test.config.inc
%else
sed -e '/SOLR_SERVER_CONFIGURED/s/true/false/' \
    -i ?TS/tests/test.config.inc
%endif

: Minimal load test for NTS installed extension
%{__php} \
   -n \
   -d extension=curl.so \
   -d extension=json.so \
   -d extension=%{buildroot}%{php_extdir}/%{pecl_name}.so \
   -m | grep %{pecl_name}

: Upstream test suite for NTS extension
cd NTS
TEST_PHP_ARGS="-n -d extension=curl.so -d extension=json.so -d extension=%{buildroot}%{php_extdir}/%{pecl_name}.so" \
REPORT_EXIT_STATUS=1 \
NO_INTERACTION=1 \
TEST_PHP_EXECUTABLE=%{__php} \
%{__php} -n run-tests.php --show-diff

%if %{with_zts}
: Minimal load test for ZTS installed extension
%{__ztsphp} \
   -n \
   -d extension=curl.so \
   -d extension=json.so \
   -d extension=%{buildroot}%{php_ztsextdir}/%{pecl_name}.so \
   -m | grep %{pecl_name}

: Upstream test suite for ZTS extension
cd ../ZTS
TEST_PHP_ARGS="-n -d extension=curl.so -d extension=json.so -d extension=%{buildroot}%{php_ztsextdir}/%{pecl_name}.so" \
REPORT_EXIT_STATUS=1 \
NO_INTERACTION=1 \
TEST_PHP_EXECUTABLE=%{__ztsphp} \
%{__ztsphp} -n run-tests.php --show-diff
%endif


%clean
rm -rf %{buildroot}


%files
%defattr(-, root, root, -)
%{?_licensedir:%license NTS/LICENSE}
%doc %{pecl_docdir}/%{pecl_name}
%{pecl_xmldir}/%{name}.xml

%config(noreplace) %{php_inidir}/%{ini_name}
%{php_extdir}/%{pecl_name}.so

%if %{with_zts}
%config(noreplace) %{php_ztsinidir}/%{ini_name}
%{php_ztsextdir}/%{pecl_name}.so
%endif


%changelog
* Thu Dec  1 2016 Remi Collet <remi@fedoraproject.org> - 2.4.0-3
- rebuild with PHP 7.1.0 GA

* Wed Sep 14 2016 Remi Collet <remi@fedoraproject.org> - 2.4.0-2
- rebuild for PHP 7.1 new API version

* Wed Mar 30 2016 Remi Collet <remi@fedoraproject.org> - 2.4.0-1
- update to 2.4.0 (stable)

* Fri Mar 25 2016 Remi Collet <remi@fedoraproject.org> - 2.4.0-0
- test build for upcoming 2.4.0

* Wed Mar 16 2016 Remi Collet <remi@fedoraproject.org> - 2.3.1-0
- test build for upcoming 2.3.1

* Tue Mar  8 2016 Remi Collet <remi@fedoraproject.org> - 2.3.0-2
- adapt for F24

* Wed Dec  2 2015 Remi Collet <remi@fedoraproject.org> - 2.3.0-1
- update to 2.3.0 (stable)

* Tue Dec  1 2015 Remi Collet <remi@fedoraproject.org> - 2.3.0-0
- test build for upcoming 2.3.0

* Mon Sep 28 2015 Remi Collet <remi@fedoraproject.org> - 2.2.1-3
- add upstream patch for zpp calls (fix broken ppc64)

* Sun Sep 27 2015 Remi Collet <remi@fedoraproject.org> - 2.2.1-2
- ignore test with jsonc < 1.3.9

* Sun Sep 27 2015 Remi Collet <remi@fedoraproject.org> - 2.2.1-1
- update to 2.2.1 (stable)

* Sun Sep 27 2015 Remi Collet <remi@fedoraproject.org> - 2.2.1-0.1
- test build for upcoming 2.2.1

* Sat Sep 26 2015 Remi Collet <rcollet@redhat.com> - 2.2.0-1
- update to 2.2.0 (stable)

* Fri Sep 25 2015 Remi Collet <rcollet@redhat.com> - 2.2.0-0.3
- test build for upcoming 2.2.0

* Wed Sep 23 2015 Remi Collet <rcollet@redhat.com> - 2.2.0-0.2
- test build for upcoming 2.2.0

* Thu Sep 17 2015 Remi Collet <rcollet@redhat.com> - 2.2.0-0.1
- test build for upcoming 2.2.0

* Tue Jun 23 2015 Remi Collet <rcollet@redhat.com> - 2.1.0-3
- allow build against rh-php56 (as more-php56)

* Fri Jan 23 2015 Remi Collet <remi@fedoraproject.org> - 2.1.0-2
- fix %%postun scriplet

* Sun Jan 18 2015 Remi Collet <remi@fedoraproject.org> - 2.1.0-1
- update to 2.1.0
- drop runtime dependency on pear, new scriptlets

* Sun Jan 11 2015 Remi Collet <remi@fedoraproject.org> - 2.1.0-0.1
- test build of upcomming 2.1.0

* Wed Dec 24 2014 Remi Collet <remi@fedoraproject.org> - 2.0.0-2.1
- Fedora 21 SCL mass rebuild

* Mon Aug 25 2014 Remi Collet <rcollet@redhat.com> - 2.0.0-2
- improve SCL build

* Tue Jun 24 2014 Remi Collet <remi@fedoraproject.org> - 2.0.0-1
- update to 2.0.0

* Mon Jun 23 2014 Remi Collet <remi@fedoraproject.org> - 2.0.0-0.4
- test build before 2.0.0 finale

* Thu Apr 17 2014 Remi Collet <remi@fedoraproject.org> - 2.0.0-0.3.beta
- add numerical prefix to extension configuration file (php 5.6)

* Tue Mar 25 2014 Remi Collet <remi@fedoraproject.org> - 2.0.0-0.2.beta
- allow SCL build

* Sat Mar  8 2014 Remi Collet <remi@fedoraproject.org> - 2.0.0-0.1.beta
- update to 2.0.0b (beta)
- install doc in pecl_docdir
- install tests in pecl_testdir

* Sun Oct 21 2012 Remi Collet <remi@fedoraproject.org> - 1.0.2-4
- rebuild

* Tue Nov 29 2011 Remi Collet <remi@fedoraproject.org> - 1.0.2-2
- php 5.4 build

* Tue Nov 29 2011 Remi Collet <remi@fedoraproject.org> - 1.0.2-1
- update to 1.0.2

* Mon Nov 28 2011 Remi Collet <remi@fedoraproject.org> - 1.0.1-4.svn320130
- svn snapshot (test suite is now ok)

* Wed Nov 16 2011 Remi Collet <remi@fedoraproject.org> - 1.0.1-3
- build against php 5.4
- ignore test result because of https://bugs.php.net/60313

* Thu Oct 06 2011 Remi Collet <Fedora@FamilleCollet.com> - 1.0.1-2
- ZTS extension
- spec cleanups

* Fri Jun 10 2011 Remi Collet <Fedora@famillecollet.com> - 1.0.1-1
- Version 1.0.1 (stable) - API 1.0.1 (stable)
- run test suite after build

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jun 23 2010 Johan Cwiklinski <johan AT x-tnd DOT be> 0.9.11-1
- update to latest release

* Thu May 13 2010 Johan Cwiklinski <johan AT x-tnd DOT be> 0.9.10-2
- consitent use of pecl_name macro
- add %%check
- fixes some typos
- thanks Remi :)

* Thu May 13 2010 Johan Cwiklinski <johan AT x-tnd DOT be> 0.9.10-1
- update to latest release

* Tue Apr 27 2010 Johan Cwiklinski <johan AT x-tnd DOT be> 0.9.9-2
- Add missing Requires
- Remove conditionnal 'php_zend_api' 'pecl_install' no longer required
- %%define no longer must be used
- Thanks to Remi :)

* Mon Apr 26 2010 Johan Cwiklinski <johan AT x-tnd DOT be> 0.9.9-1
- Initial packaging
