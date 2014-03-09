# spec file for php-pecl-solr2
#
# Copyright (c) 2011-2014 Remi Collet
# Copyright (c) 2010 Johan Cwiklinski
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/3.0/
#
# Please, preserve the changelog entries
#
%{!?php_inidir:  %global php_inidir   %{_sysconfdir}/php.d}
%{!?__pecl:      %global __pecl       %{_bindir}/pecl}
%{!?__php:       %global __php        %{_bindir}/php}

%global pecl_name solr
%global prever    b
%global with_zts  0%{?__ztsphp:1}

Summary:        Object oriented API to Apache Solr
Summary(fr):    API orientée objet pour Apache Solr
Name:           php-pecl-solr2
Version:        2.0.0
Release:        0.1.beta%{?dist}%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}
License:        PHP
Group:          Development/Languages
URL:            http://pecl.php.net/package/solr

Source0:        http://pecl.php.net/get/%{pecl_name}-%{version}%{prever}.tgz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  php-devel
BuildRequires:  php-pear
BuildRequires:  php-curl
BuildRequires:  php-json
BuildRequires:  curl-devel
BuildRequires:  libxml2-devel

Requires(post): %{__pecl}
Requires(postun): %{__pecl}
Requires:       php(zend-abi) = %{php_zend_api}
Requires:       php(api) = %{php_core_api}
%if "%{php_version}" < "5.4"
# php 5.3.3 in EL-6 don't use arched virtual provides
# so only requires real packages instead
Requires:       %{?scl_prefix}php-common%{?_isa}
%else
Requires:       %{?scl_prefix}php-curl%{?_isa}
Requires:       %{?scl_prefix}php-json%{?_isa}
%endif

Provides:       php-%{pecl_name} = %{version}
Provides:       php-%{pecl_name}%{?_isa} = %{version}
Provides:       php-pecl(%{pecl_name}) = %{version}
Provides:       php-pecl(%{pecl_name})%{?_isa} = %{version}
# Only one version of the extension
Conflicts:      php-pecl-solr < 2

# Other third party repo stuff
%if "%{php_version}" > "5.4"
Obsoletes:     php53-pecl-%{pecl_name}2
Obsoletes:     php53u-pecl-%{pecl_name}2
Obsoletes:     php54-pecl-%{pecl_name}2
%endif
%if "%{php_version}" > "5.5"
Obsoletes:     php55u-pecl-%{pecl_name}2
%endif
%if "%{php_version}" > "5.6"
Obsoletes:     php56u-pecl-%{pecl_name}2
%endif

%if 0%{?fedora} < 20
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


%prep
%setup -c -q

mv %{pecl_name}-%{version}%{?prever} NTS
cd NTS

# Check version
extver=$(sed -n '/#define PHP_SOLR_VERSION /{s/.* "//;s/".*$//;p}' php_solr_version.h)
if test "x${extver}" != "x%{version}%{?prever}"; then
   : Error: Upstream version is ${extver}, expecting %{version}%{?prever}.
   exit 1
fi

# Fix rights (fixed upstream)
find . -type f -exec chmod -x {} \;
cd ..

# Create configuration file
cat > %{pecl_name}.ini << 'EOF'
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
install -D -m 644 %{pecl_name}.ini %{buildroot}%{php_inidir}/%{pecl_name}.ini

%if %{with_zts}
make -C ZTS install INSTALL_ROOT=%{buildroot}
install -D -m 644 %{pecl_name}.ini %{buildroot}%{php_ztsinidir}/%{pecl_name}.ini
%endif


# Test & Documentation
for i in $(grep 'role="test"' package.xml | sed -e 's/^.*name="//;s/".*$//')
do install -Dpm 644 NTS/$i %{buildroot}%{pecl_testdir}/%{pecl_name}/$i
done
for i in LICENSE $(grep 'role="doc"' package.xml | sed -e 's/^.*name="//;s/".*$//')
do install -Dpm 644 NTS/$i %{buildroot}%{pecl_docdir}/%{pecl_name}/$i
done


%post
%{pecl_install} %{pecl_xmldir}/%{name}.xml >/dev/null || :


%postun
if [ $1 -eq 0 ] ; then
    %{pecl_uninstall} %{pecl_name} >/dev/null || :
fi


%check
cd NTS

: Minimal load test for NTS extension
%{__php} \
   -n \
   -d extension=curl.so \
   -d extension=json.so \
   -d extension=$PWD/modules/%{pecl_name}.so \
   -m | grep %{pecl_name}

: Upstream test suite for NTS extension
# http://git.php.net/?p=pecl/search_engine/solr.git;a=commitdiff;h=a7ac6ee8f09b28e848436f7d972cc74b8eb1ae1c
sed -e '/SOLR_SERVER_CONFIGURED/s/true/false/' \
    -i tests/test.config.inc

# http://git.php.net/?p=pecl/search_engine/solr.git;a=commitdiff;h=224c40fd3118ae675b5bbc2194370198918b18d0
sed -e '/^curl$/d' -i tests/*phpt

TEST_PHP_ARGS="-n -d extension=curl.so -d extension=json.so -d extension=$PWD/modules/%{pecl_name}.so" \
REPORT_EXIT_STATUS=1 \
NO_INTERACTION=1 \
TEST_PHP_EXECUTABLE=%{__php} \
%{__php} run-tests.php

%if %{with_zts}
cd ../ZTS

: Minimal load test for ZTS extension
%{__ztsphp} \
   -n \
   -d extension=curl.so \
   -d extension=json.so \
   -d extension=$PWD/modules/%{pecl_name}.so \
   -m | grep %{pecl_name}

: Upstream test suite for ZTS extension
sed -e '/SOLR_SERVER_CONFIGURED/s/true/false/' \
    -i tests/test.config.inc
sed -e '/^curl$/d' -i tests/*phpt

TEST_PHP_ARGS="-n -d extension=curl.so -d extension=json.so -d extension=$PWD/modules/%{pecl_name}.so" \
REPORT_EXIT_STATUS=1 \
NO_INTERACTION=1 \
TEST_PHP_EXECUTABLE=%{__ztsphp} \
%{__ztsphp} run-tests.php
%endif


%clean
rm -rf %{buildroot}


%files
%defattr(-, root, root, -)
%doc %{pecl_docdir}/%{pecl_name}
%doc %{pecl_testdir}/%{pecl_name}
%config(noreplace) %{php_inidir}/%{pecl_name}.ini
%{php_extdir}/%{pecl_name}.so
%{pecl_xmldir}/%{name}.xml
%if %{with_zts}
%config(noreplace) %{php_ztsinidir}/%{pecl_name}.ini
%{php_ztsextdir}/%{pecl_name}.so
%endif


%changelog
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
