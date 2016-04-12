# remirepo spec file for php-pecl-memcached
# With SCL compatibility, from:
#
# Fedora spec file for php-pecl-memcached
#
# Copyright (c) 2009-2016 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%if 0%{?scl:1}
%if "%{scl}" == "rh-php56"
%global sub_prefix more-php56-
%else
%global sub_prefix %{scl_prefix}
%endif
%scl_package         php-pecl-memcached
%else
%global _root_prefix %{_prefix}
%endif

%global with_fastlz 1
%global with_igbin  1
%global with_zts    0%{!?_without_zts:%{?__ztsphp:1}}
%global with_tests  %{?_with_tests:1}%{!?_with_tests:0}
%global pecl_name   memcached
# https://github.com/php-memcached-dev/php-memcached/commits/php7
%global gh_commit   6ace07da69a5ebc021e56a9d2f52cdc8897b4f23
%global gh_short    %(c=%{gh_commit}; echo ${c:0:7})
%global gh_date     20160217
%global gh_owner    php-memcached-dev
%global gh_project  php-memcached
#global prever      RC1
#global intver      rc1
%if "%{php_version}" < "5.6"
# After igbinary, json, msgpack
%global ini_name  z-%{pecl_name}.ini
%else
# After 40-igbinary, 40-json, 40-msgpack
%global ini_name  50-%{pecl_name}.ini
%endif

Summary:      Extension to work with the Memcached caching daemon
Name:         %{?sub_prefix}php-pecl-memcached
Version:      3.0.0
Release:      0.1.%{gh_date}git%{gh_short}%{?dist}%{!?scl:%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}}
License:      PHP
Group:        Development/Languages
URL:          http://pecl.php.net/package/%{pecl_name}

Source0:      https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}%{?prever}-%{gh_short}.tar.gz

BuildRoot:    %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
# 5.2.10 required to HAVE_JSON enabled
BuildRequires: %{?scl_prefix}php-devel >= 5.2.10
BuildRequires: %{?scl_prefix}php-pear
BuildRequires: %{?scl_prefix}php-json
%if %{with_igbin}
BuildRequires: %{?sub_prefix}php-pecl-igbinary-devel
%endif
%ifnarch ppc64
BuildRequires: %{?sub_prefix}php-pecl-msgpack-devel
%endif
BuildRequires: zlib-devel
BuildRequires: cyrus-sasl-devel
%if %{with_fastlz}
BuildRequires: fastlz-devel
%endif
%if %{with_tests}
BuildRequires: memcached
%endif

%if 0%{?scl:1} && 0%{?fedora} < 15 && 0%{?rhel} < 7 && "%{?scl_vendor}" != "remi"
# Filter in the SCL collection
%{?filter_requires_in: %filter_requires_in %{_libdir}/.*\.so}
# libvent from SCL as not available in system
BuildRequires: %{?sub_prefix}libevent-devel  > 2
Requires:      %{?sub_prefix}libevent%{_isa} > 2
BuildRequires: %{?sub_prefix}libmemcached-devel  > 1
Requires:      %{?sub_prefix}libmemcached-libs%{_isa} > 1
%if %{with_fastlz}
Requires:      fastlz%{_isa}
%endif
Requires:      cyrus-sasl-lib%{_isa}
%else
BuildRequires: libevent-devel >= 2.0.2
%if 0%{?rhel} == 5
BuildRequires: libmemcached-devel  > 1
%else
# To ensure use of libmemcached-last for --enable-memcached-protocol
BuildRequires: libmemcached-devel  >= 1.0.16
%endif
%endif

Requires:     %{?scl_prefix}php(zend-abi) = %{php_zend_api}
Requires:     %{?scl_prefix}php(api) = %{php_core_api}
Requires:     %{?scl_prefix}php-json%{?_isa}
%if %{with_igbin}
Requires:     %{?sub_prefix}php-pecl-igbinary%{?_isa}
%endif
%ifnarch ppc64
Requires:     %{?sub_prefix}php-pecl-msgpack%{?_isa}
%endif
%{?_sclreq:Requires: %{?scl_prefix}runtime%{?_sclreq}%{?_isa}}

Provides:     %{?scl_prefix}php-%{pecl_name} = %{version}
Provides:     %{?scl_prefix}php-%{pecl_name}%{?_isa} = %{version}
Provides:     %{?scl_prefix}php-pecl(%{pecl_name}) = %{version}
Provides:     %{?scl_prefix}php-pecl(%{pecl_name})%{?_isa} = %{version}
%if "%{?scl_prefix}" != "%{?sub_prefix}"
Provides:     %{?scl_prefix}php-pecl-%{pecl_name}          = %{version}-%{release}
Provides:     %{?scl_prefix}php-pecl-%{pecl_name}%{?_isa}  = %{version}-%{release}
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
%endif

%if 0%{?fedora} < 20 && 0%{?rhel} < 7
# Filter private shared
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}
%endif


%description
This extension uses libmemcached library to provide API for communicating
with memcached servers.

memcached is a high-performance, distributed memory object caching system,
generic in nature, but intended for use in speeding up dynamic web 
applications by alleviating database load.

It also provides a session handler (memcached). 

Package built for PHP %(%{__php} -r 'echo PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')%{?scl: as Software Collection (%{scl} by %{?scl_vendor}%{!?scl_vendor:rh})}.


%prep 
%setup -c -q
mv %{gh_project}-%{gh_commit} NTS
sed -e '/PHP_MEMCACHED_VERSION/s/3.0.0b1/%{version}-dev/' -i NTS/php_memcached.h
%{__php} -r '
  $pkg = simplexml_load_file("NTS/package.xml");
  $pkg->date = substr("%{gh_date}",0,4)."-".substr("%{gh_date}",4,2)."-".substr("%{gh_date}",6,2);
  $pkg->version->release = "%{version}dev";
  $pkg->stability->release = "devel";
  $pkg->asXML("package.xml");
'

# Don't install/register tests
sed -e 's/role="test"/role="src"/' \
    %{?_licensedir:-e '/LICENSE/s/role="doc"/role="src"/' } \
    -i package.xml

cd NTS
%if %{with_fastlz}
rm -r fastlz
sed -e '/name=.fastlz/d' -i ../package.xml
%endif

# Check version as upstream often forget to update this
extver=$(sed -n '/#define PHP_MEMCACHED_VERSION/{s/.* "//;s/".*$//;p}' php_memcached.h)
if test "x${extver}" != "x%{version}%{?gh_date:-dev}%{?intver}"; then
   : Error: Upstream HTTP version is now ${extver}, expecting %{version}%{?prever}%{?gh_date:-dev}.
   : Update the pdover macro and rebuild.
   exit 1
fi
cd ..

cat > %{ini_name} << 'EOF'
; Enable %{pecl_name} extension module
extension=%{pecl_name}.so

; ----- Options to use the memcached session handler

; RPM note : save_handler and save_path are defined
; for mod_php, in /etc/httpd/conf.d/php.conf
; for php-fpm, in %{_sysconfdir}/php-fpm.d/*conf

;  Use memcache as a session handler
;session.save_handler=memcached
;  Defines a comma separated list of server urls to use for session storage
;session.save_path="localhost:11211"

; ----- Configuration options
; http://php.net/manual/en/memcached.configuration.php

EOF

# default options with description from upstream
cat NTS/memcached.ini >>%{ini_name}

%if %{with_zts}
cp -r NTS ZTS
%endif


%build
# only needed for SCL
export PKG_CONFIG_PATH=%{_libdir}/pkgconfig

peclconf() {
%configure \
%if %{with_igbin}
           --enable-memcached-igbinary \
%endif
           --enable-memcached-json \
           --enable-memcached-sasl \
%ifnarch ppc64
           --enable-memcached-msgpack \
%endif
%if 1
           --disable-memcached-protocol \
%else
           --enable-memcached-protocol \
%endif
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
# Install the NTS extension
make install -C NTS INSTALL_ROOT=%{buildroot}

# Drop in the bit of configuration
# rename to z-memcached to be load after msgpack
install -D -m 644 %{ini_name} %{buildroot}%{php_inidir}/%{ini_name}

# Install XML package description
install -D -m 644 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml

# Install the ZTS extension
%if %{with_zts}
make install -C ZTS INSTALL_ROOT=%{buildroot}
install -D -m 644 %{ini_name} %{buildroot}%{php_ztsinidir}/%{ini_name}
%endif

# Documentation
cd NTS
for i in $(grep 'role="doc"' ../package.xml | sed -e 's/^.*name="//;s/".*$//')
do install -Dpm 644 $i %{buildroot}%{pecl_docdir}/%{pecl_name}/$i
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
OPT="-n"
[ -f %{php_extdir}/igbinary.so ] && OPT="$OPT -d extension=igbinary.so"
[ -f %{php_extdir}/json.so ]     && OPT="$OPT -d extension=json.so"
[ -f %{php_extdir}/msgpack.so ]  && OPT="$OPT -d extension=msgpack.so"

: Minimal load test for NTS extension
%{__php} $OPT \
    -d extension=%{buildroot}%{php_extdir}/%{pecl_name}.so \
    --modules | grep %{pecl_name}

%if %{with_zts}
: Minimal load test for ZTS extension
%{__ztsphp} $OPT \
    -d extension=%{buildroot}%{php_ztsextdir}/%{pecl_name}.so \
    --modules | grep %{pecl_name}
%endif

%if %{with_tests}
ret=0

: Launch the Memcached service
memcached -p 11211 -U 11211      -d -P $PWD/memcached.pid

: Run the upstream test Suite for NTS extension
pushd NTS
rm tests/flush_buffers.phpt tests/touch_binary.phpt
TEST_PHP_EXECUTABLE=%{__php} \
TEST_PHP_ARGS="$OPT -d extension=$PWD/modules/%{pecl_name}.so" \
NO_INTERACTION=1 \
REPORT_EXIT_STATUS=1 \
%{__php} -n run-tests.php --show-diff tests/*phpt || ret=1
popd

%if %{with_zts}
: Run the upstream test Suite for ZTS extension
pushd ZTS
rm tests/flush_buffers.phpt tests/touch_binary.phpt
TEST_PHP_EXECUTABLE=%{__ztsphp} \
TEST_PHP_ARGS="$OPT -d extension=$PWD/modules/%{pecl_name}.so" \
NO_INTERACTION=1 \
REPORT_EXIT_STATUS=1 \
%{__ztsphp} -n run-tests.php --show-diff tests/*phpt  || ret=1
popd
%endif

# Cleanup
if [ -f memcached.pid ]; then
   kill $(cat memcached.pid)
fi

exit $ret
%endif


%files
%defattr(-,root,root,-)
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
* Thu Mar  3 2016 Remi Collet <remi@fedoraproject.org> - 3.0.0-0.1.20160217git6ace07d
- update to 3.0.0-dev
- switch back to php-memcached-dev sources

* Wed Mar  2 2016 Remi Collet <remi@fedoraproject.org> - 2.2.1-0.2.20150628git3c79a97
- add patch for igbinary, see
  https://github.com/rlerdorf/php-memcached/pull/3

* Sun Jan 10 2016 Remi Collet <remi@fedoraproject.org> - 2.2.1-0.1.20150628git3c79a97
- bump version to 2.2.1-dev, stability=devel

* Tue Oct 13 2015 Remi Collet <remi@fedoraproject.org> - 2.2.0-11.20150628git3c79a97
- rebuild for PHP 7.0.0RC5 new API version

* Fri Sep 18 2015 Remi Collet <remi@fedoraproject.org> - 2.2.0-10.20150628git3c79a97
- F23 rebuild with rh_layout

* Wed Jul 22 2015 Remi Collet <rcollet@redhat.com> - 2.2.0-9.20150628git3c79a97
- rebuild against php 7.0.0beta2

* Wed Jul  8 2015 Remi Collet <rcollet@redhat.com> - 2.2.0-8.20150628git3c79a97
- new snapshot

* Sat Jun 27 2015 Remi Collet <rcollet@redhat.com> - 2.2.0-7.20150423git4187e22
- switch sources from pecl to github
- temporarily use rlerdorf fork (php7 compatibility)
- disable igbinary
- open https://github.com/rlerdorf/php-memcached/pull/2 - msgpack

* Tue Jun 23 2015 Remi Collet <rcollet@redhat.com> - 2.2.0-6
- allow build against rh-php56 (as more-php56)
- don't install/register tests
- drop runtime dependency on pear, new scriptlets

* Wed Dec 24 2014 Remi Collet <remi@fedoraproject.org> - 2.2.0-5.1
- Fedora 21 SCL mass rebuild

* Fri Aug 29 2014 Remi Collet <rcollet@redhat.com> - 2.2.0-5
- test build with system fastlz

* Fri Aug 29 2014 Remi Collet <rcollet@redhat.com> - 2.2.0-4
- improve SCL build

* Wed Apr  9 2014 Remi Collet <remi@fedoraproject.org> - 2.2.0-3
- add numerical prefix to extension configuration file

* Wed Apr  2 2014  Remi Collet <remi@fedoraproject.org> - 2.2.0-2
- add all ini options in configuration file (comments)

* Wed Apr  2 2014  Remi Collet <remi@fedoraproject.org> - 2.2.0-1
- update to 2.2.0 (stable)
- msgpack not available for ppc64

* Wed Mar 19 2014 Remi Collet <rcollet@redhat.com> - 2.2.0-0.3.RC1
- allow SCL build

* Thu Mar 13 2014  Remi Collet <remi@fedoraproject.org> - 2.2.0-0.2.RC1
- update to 2.2.0RC1 (beta)

* Mon Nov 25 2013  Remi Collet <remi@fedoraproject.org> - 2.2.0-0.1.b1
- update to 2.2.0b1 (beta)
- cleanups for Copr
- install doc in pecl doc_dir
- install tests in pecl test_dir (in devel)
- add dependency on pecl/msgpack
- add --with tests option to run upstream test suite during build

* Fri Nov 15 2013  Remi Collet <remi@fedoraproject.org> - 2.1.0-7
- drop requires libmemcached >= build version
  as this can also be libmemcached-last

* Mon Nov 19 2012  Remi Collet <remi@fedoraproject.org> - 2.1.0-6
- requires libmemcached >= build version

* Sat Nov 17 2012  Remi Collet <remi@fedoraproject.org> - 2.1.0-5
- rebuild for libmemcached 1.0.14 (with SASL)
- switch to upstream patch
- add patch to report about SASL support in phpinfo

* Fri Oct 19 2012 Remi Collet <remi@fedoraproject.org> - 2.1.0-4
- improve comment in configuration about session.

* Sat Sep 22 2012 Remi Collet <remi@fedoraproject.org> - 2.1.0-3
- rebuild for new libmemcached
- drop sasl support

* Sat Sep  8 2012 Remi Collet <remi@fedoraproject.org> - 2.1.0-2
- sync with rawhide, cleanups
- Obsoletes php53*, php54* on EL

* Tue Aug 07 2012 Remi Collet <remi@fedoraproject.org> - 2.1.0-1
- update to 2.1.0
- add patch to lower libmemcached required version

* Sun Apr 22 2012  Remi Collet <remi@fedoraproject.org> - 2.0.1-6
- rebuild for libmemcached 1.0.6 (with SASL) and php 5.4

* Sun Apr 22 2012  Remi Collet <remi@fedoraproject.org> - 2.0.1-5
- rebuild for libmemcached 1.0.6 (with SASL) and php 5.3

* Sat Apr 21 2012  Remi Collet <remi@fedoraproject.org> - 2.0.1-4
- rebuild for libmemcached 1.0.6 and php 5.4

* Sat Apr 21 2012  Remi Collet <remi@fedoraproject.org> - 2.0.1-3
- rebuild for libmemcached 1.0.6 and php 5.3

* Sat Mar 03 2012  Remi Collet <remi@fedoraproject.org> - 2.0.1-2
- update to 2.0.1 for PHP 5.4

* Sat Mar 03 2012  Remi Collet <remi@fedoraproject.org> - 2.0.1-1
- update to 2.0.1 for PHP 5.3

* Sat Mar 03 2012  Remi Collet <remi@fedoraproject.org> - 2.0.0-2
- update to 2.0.0 for PHP 5.4

* Sat Mar 03 2012  Remi Collet <remi@fedoraproject.org> - 2.0.0-1
- update to 2.0.0 for PHP 5.3

* Wed Nov 16 2011  Remi Collet <remi@fedoraproject.org> - 2.0.0-0.1.1736623
- update to git snapshot (post 2.0.0b2) for php 5.4 build

* Sun Oct 16 2011  Remi Collet <remi@fedoraproject.org> - 1.0.2-10
- rebuild against latest libmemcached (f16 only)

* Tue Oct 04 2011  Remi Collet <remi@fedoraproject.org> - 1.0.2-9
- ZTS extension

* Sat Sep 17 2011  Remi Collet <remi@fedoraproject.org> - 1.0.2-8
- allow relocation
- work for ZTS (not yet ok)

* Sat Sep 17 2011  Remi Collet <remi@fedoraproject.org> - 1.0.2-7
- rebuild against libmemcached 0.52
- adapted filter
- clean spec

* Thu Jun 02 2011  Remi Collet <Fedora@FamilleCollet.com> - 1.0.2-6
- rebuild against libmemcached 0.49

* Sat Feb 19 2011 Remi Collet <fedora@famillecollet.com> - 1.0.2-3.2
- rebuild for remi repo with SASL for fedora <= 10 and EL <= 5

* Sat Oct 02 2010 Remi Collet <fedora@famillecollet.com> - 1.0.2-3.1
- remove patch 

* Fri Oct 01 2010 Remi Collet <fedora@famillecollet.com> - 1.0.2-3
- rebuild against libmemcached 0.44 with SASL support

* Wed Sep 29 2010 Remi Collet <fedora@famillecollet.com> - 1.0.2-2
- rebuild with igbinary support

* Tue May 04 2010 Remi Collet <fedora@famillecollet.com> - 1.0.2-1
- update to 1.0.2 for libmemcached 0.40

* Sat Mar 13 2010 Remi Collet <fedora@famillecollet.com> - 1.0.1-1
- update to 1.0.1 for libmemcached 0.38

* Sun Feb 07 2010 Remi Collet <fedora@famillecollet.com> - 1.0.0-3.1
- bump release

* Sat Feb 06 2010 Remi Collet <fedora@famillecollet.com> - 1.0.0-3
- rebuilt against new libmemcached
- add minimal %%check

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Jul 12 2009 Remi Collet <fedora@famillecollet.com> - 1.0.0-1
- Update to 1.0.0 (First stable release)

* Sat Jun 27 2009 Remi Collet <fedora@famillecollet.com> - 0.2.0-1
- Update to 0.2.0 + Patch for HAVE_JSON constant

* Wed Apr 29 2009 Remi Collet <fedora@famillecollet.com> - 0.1.5-1
- Initial RPM

