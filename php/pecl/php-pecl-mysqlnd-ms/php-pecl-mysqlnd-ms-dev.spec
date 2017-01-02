# spec file for php-pecl-mysqlnd-ms
#
# Copyright (c) 2011-2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%{?scl:          %scl_package        php-pecl-mysqlnd-ms}

%global pecl_name mysqlnd_ms
%global with_zts  0%{?__ztsphp:1}
%global versufix  -alpha
%global svnrev    333506
%if "%{php_version}" < "5.6"
# After json, mysqlnd
%global ini_name  %{pecl_name}.ini
%else
# After 40-json, 20-mysqlnd
%global ini_name  50-%{pecl_name}.ini
%endif

Summary:      A replication and load balancing plugin for mysqlnd
Name:         %{?scl_prefix}php-pecl-mysqlnd-ms
Version:      1.6.0
Release:      6.svn%{svnrev}%{?dist}%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}

License:      PHP
Group:        Development/Languages
URL:          http://pecl.php.net/package/mysqlnd_ms

%if 0%{?svnrev}
# svn export -r 333506 https://svn.php.net/repository/pecl/mysqlnd_ms/trunk
# cd trunk
# pecl package
# mv mysqlnd_ms-1.6.0.tgz ../mysqlnd_ms-1.6.0-333506.tgz
Source0:      %{pecl_name}-%{version}-%{svnrev}.tgz
%else
Source0:      http://pecl.php.net/get/%{pecl_name}-%{version}.tgz
%endif

# From http://www.php.net/manual/en/mysqlnd-ms.configuration.php
Source1:      %{pecl_name}.ini

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: %{?scl_prefix}php-devel >= 5.3.6
BuildRequires: %{?scl_prefix}php-mysqlnd
BuildRequires: %{?scl_prefix}php-json
BuildRequires: %{?scl_prefix}php-pear
BuildRequires: libxml2-devel

Requires:     %{?scl_prefix}php-mysqlnd%{?_isa}
Requires:     %{?scl_prefix}php-json%{?_isa}
Requires:     %{?scl_prefix}php(zend-abi) = %{php_zend_api}
Requires:     %{?scl_prefix}php(api) = %{php_core_api}
%{?_sclreq:Requires: %{?scl_prefix}runtime%{?_sclreq}%{?_isa}}

Provides:     %{?scl_prefix}php-%{pecl_name}               = %{version}
Provides:     %{?scl_prefix}php-%{pecl_name}%{?_isa}       = %{version}
Provides:     %{?scl_prefix}php-pecl(%{pecl_name})         = %{version}
Provides:     %{?scl_prefix}php-pecl(%{pecl_name})%{?_isa} = %{version}
Provides:     %{?scl_prefix}php-pecl-mysqlnd-ms            = %{version}-%{release}
Provides:     %{?scl_prefix}php-pecl-mysqlnd-ms%{?_isa}    = %{version}-%{release}

%if "%{?vendor}" == "Remi Collet" && 0%{!?scl:1} && 0%{?rhel}
# Other third party repo stuff
Obsoletes:     php53-pecl-mysqlnd-ms  <= %{version}
Obsoletes:     php53u-pecl-mysqlnd-ms <= %{version}
Obsoletes:     php54-pecl-mysqlnd-ms  <= %{version}
Obsoletes:     php54w-pecl-mysqlnd-ms <= %{version}
%if "%{php_version}" > "5.5"
Obsoletes:     php55u-pecl-mysqlnd-ms <= %{version}
Obsoletes:     php55w-pecl-mysqlnd-ms <= %{version}
%endif
%if "%{php_version}" > "5.6"
Obsoletes:     php56u-pecl-mysqlnd-ms <= %{version}
Obsoletes:     php56w-pecl-mysqlnd-ms <= %{version}
%endif
%endif

%if 0%{?fedora} < 20 && 0%{?rhel} < 7
# Filter private shared
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}
%endif


%description
The replication and load balancing plugin is a plugin for the mysqlnd library.
It can be used with PHP MySQL extensions (ext/mysql, ext/mysqli, PDO_MySQL),
if they are compiled to use mysqlnd. The plugin inspects queries to do
read-write splitting. Read-only queries are send to configured MySQL
replication slave servers all other queries are redirected to the MySQL
replication master server. Very little, if any, application changes required,
dependent on the usage scenario required.

Documentation : http://www.php.net/mysqlnd_ms

Package built for PHP %(%{__php} -r 'echo PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')%{?scl: as Software Collection (%{scl} by %{?scl_vendor}%{!?scl_vendor:rh})}.


%package devel
Summary:       Mysqlnd_ms developer files (header)
Group:         Development/Libraries
Requires:      %{name}%{?_isa} = %{version}-%{release}
Requires:      %{?scl_prefix}php-devel%{?_isa}

%description devel
These are the files needed to compile programs using mysqlnd_ms extension.


%prep
%setup -c -q

cp %{SOURCE1} %{ini_name}

%{?_licensedir:sed -e '/LICENSE/s/role="doc"/role="src"/' -i package.xml}

mv %{pecl_name}-%{version} NTS

# check version, so often broken
grep MYSQLND_MS_VERSION NTS/mysqlnd_ms.h
extver=$(sed -n '/PHP_MYSQLND_MS_VERSION /{s/.* "//;s/".*$//;p}' NTS/mysqlnd_ms.h)
if test "x${extver}" != "x%{version}%{?versufix}"; then
   : Error: Upstream version is ${extver}, expecting %{version}%{?versufix}.
   exit 1
fi

%if %{with_zts}
# Build ZTS extension if ZTS devel available (fedora >= 17)
cp -r NTS ZTS
%endif


%build
# EXPERIMENTAL options not used
# --enable-mysqlnd-ms-table-filter
#         Enable support for table filter in mysqlnd_ms
# --enable-mysqlnd-ms-cache-support
#         Enable query caching through mysqlnd_qc

cd NTS
%{_bindir}/phpize
%configure \
    --with-libdir=%{_lib} \
    --enable-mysqlnd-ms \
    --with-php-config=%{_bindir}/php-config
make %{?_smp_mflags}

%if %{with_zts}
cd ../ZTS
%{_bindir}/zts-phpize
%configure \
    --with-libdir=%{_lib} \
    --enable-mysqlnd-ms \
    --with-php-config=%{_bindir}/zts-php-config
make %{?_smp_mflags}
%endif


%install
rm -rf %{buildroot}

make install -C NTS INSTALL_ROOT=%{buildroot}

# Drop in the bit of configuration
install -D -m 644 %{ini_name} %{buildroot}%{php_inidir}/%{ini_name}

# Install XML package description
install -D -m 644 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml

%if %{with_zts}
make install -C ZTS INSTALL_ROOT=%{buildroot}
install -D -m 644 %{ini_name} %{buildroot}%{php_ztsinidir}/%{ini_name}
%endif

# Test & Documentation
for i in $(grep 'role="test"' package.xml | sed -e 's/^.*name="//;s/".*$//')
do install -Dpm 644 NTS/$i %{buildroot}%{pecl_testdir}/%{pecl_name}/$i
done
for i in $(grep 'role="doc"' package.xml | sed -e 's/^.*name="//;s/".*$//')
do install -Dpm 644 NTS/$i %{buildroot}%{pecl_docdir}/%{pecl_name}/$i
done


%clean
rm -rf %{buildroot}


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
cd NTS
# only check if build extension can be loaded
%{__php} -n -q \
    -d extension=json.so \
    -d extension=mysqlnd.so \
    -d extension=%{buildroot}%{php_extdir}/%{pecl_name}.so \
    --modules | grep %{pecl_name}

%if %{with_zts}
cd ../ZTS
# only check if build extension can be loaded
%{__ztsphp} -n -q \
    -d extension=json.so \
    -d extension=mysqlnd.so \
    -d extension=%{buildroot}%{php_ztsextdir}/%{pecl_name}.so \
    --modules | grep %{pecl_name}
%endif


%files
%defattr(-, root, root, -)
%{?_licensedir:%license NTS/LICENSE}
%doc %{pecl_docdir}/%{pecl_name}
#exclude %{pecl_docdir}/%{pecl_name}/examples
%{pecl_xmldir}/%{name}.xml

%config(noreplace) %{php_inidir}/%{ini_name}
%{php_extdir}/%{pecl_name}.so

%if %{with_zts}
%config(noreplace) %{php_ztsinidir}/%{ini_name}
%{php_ztsextdir}/%{pecl_name}.so
%endif


%files devel
%defattr(-,root,root,-)
#doc %{pecl_docdir}/%{pecl_name}/examples
%doc %{pecl_testdir}/%{pecl_name}
%{php_incldir}/ext/%{pecl_name}

%if %{with_zts}
%{php_ztsincldir}/ext/%{pecl_name}
%endif


%changelog
* Wed Mar  9 2016 Remi Collet <remi@fedoraproject.org> - 1.6.0-6.svn333506
- adapt for F24
- drop runtime dependency on pear, new scriptlets
- fix license management

* Wed Dec 24 2014 Remi Collet <remi@fedoraproject.org> - 1.6.0-5.svn333506
- Fedora 21 SCL mass rebuild

* Mon Aug 25 2014 Remi Collet <rcollet@redhat.com> - 1.6.0-4.svn333506
- improve SCL build

* Fri May  9 2014 Remi Collet <remi@fedoraproject.org> - 1.6.0-3.svn333506
- new snapshot

* Wed Apr 16 2014 Remi Collet <remi@fedoraproject.org> - 1.6.0-2.svn333055
- add numerical prefix to extension configuration file

* Sat Mar 22 2014 Remi Collet <remi@fedoraproject.org> - 1.6.0-1.svn333055
- Update to 1.6.0 (alpha) svn snapshot for php 5.6

* Sat Mar 22 2014 Remi Collet <remi@fedoraproject.org> - 1.5.2-2
- allow SCL build
- install doc in pecl_docdir
- install tests in pecl_testdir (devel)

* Fri Jun 21 2013 Remi Collet <remi@fedoraproject.org> - 1.5.2-1
- Update to 1.5.2

* Wed Jun 19 2013 Remi Collet <remi@fedoraproject.org> - 1.5.1-1
- Update to 1.5.1

* Fri Nov 30 2012 Remi Collet <RPMS@FamilleCollet.com> - 1.4.2-2.1
- also provides php-mysqlnd_ms

* Sun Sep  9 2012 Remi Collet <RPMS@FamilleCollet.com> - 1.4.2-2
- obsoletes php53*, php54*
- cleanups

* Wed Aug 22 2012 Remi Collet <remi@fedoraproject.org> - 1.4.2-1
- update to 1.4.2 (stable)
- add -devel sub package

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Apr 30 2012 Remi Collet <remi@fedoraproject.org> - 1.3.2-2
- rebuild for EL and PHP 5.4

* Mon Apr 30 2012 Remi Collet <remi@fedoraproject.org> - 1.3.2-1
- update to 1.2.3 (stable)
- add version check
- add devel sub-package

* Thu Feb 02 2012 Remi Collet <remi@fedoraproject.org> - 1.2.2-2
- build against php 5.4

* Thu Feb 02 2012 Remi Collet <remi@fedoraproject.org> - 1.2.2-1
- update to 1.2.2 (stable)

* Wed Jan 25 2012 Remi Collet <remi@fedoraproject.org> - 1.1.2-5
- zts binary in /usr/bin with zts prefix

* Sat Jan 21 2012 Remi Collet <remi@fedoraproject.org> - 1.1.2-4
- merge ZTS change for fedora 17
- filter_setup is enough

* Sun Nov 13 2011 Remi Collet <remi@fedoraproject.org> - 1.1.2-3
- build against php 5.4

* Mon Nov 07 2011 Remi Collet <remi@fedoraproject.org> - 1.1.2-2
- update to 1.1.2 (stable) with zts extension

* Mon Nov 07 2011 Remi Collet <remi@fedoraproject.org> - 1.1.2-1
- update to 1.1.2 (stable)

* Fri Oct 14 2011 Remi Collet <remi@fedoraproject.org> - 1.1.1-1
- update to 1.1.1

* Sun Oct 02 2011 Remi Collet <remi@fedoraproject.org> - 1.1.0-1
- Initial RPM
