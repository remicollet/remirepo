# remirepo spec file for php-pecl-mongo
# with SCL compatibility, from:
#
# Fedora spec file for php-pecl-mongo
#
# Copyright (c) 2014-2016 Remi Collet
# Copyright (c) 2010-2013 Christof Damian
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#
%{?scl:          %scl_package        php-pecl-mongo}

%global pecl_name   mongo
%global with_zts    0%{?__ztsphp:1}
#global prever      RC3
# see https://github.com/mongodb/mongo-php-driver-legacy/releases
%global gh_commit   0b2945e4d96ad9407b68cd9ac403e5824b3f364e
%global gh_short    %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner    mongodb
%global gh_project  mongo-php-driver-legacy
%global with_tests  %{?_with_tests:1}%{!?_with_tests:0}
%if "%{php_version}" < "5.6"
# After json
%global ini_name    %{pecl_name}.ini
%else
# After 40-json
%global ini_name    50-%{pecl_name}.ini
%endif

Summary:      PHP MongoDB database driver
Name:         %{?scl_prefix}php-pecl-mongo
Version:      1.6.14
Release:      1%{?dist}%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}
License:      ASL 2.0
Group:        Development/Languages
URL:          http://pecl.php.net/package/%{pecl_name}

# Pull sources from github to get tests
Source0:      https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}%{?prever}.tar.gz
Source1:      %{pecl_name}.ini

BuildRoot:    %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: %{?scl_prefix}php-devel >= 5.2.6
BuildRequires: %{?scl_prefix}php-pear
BuildRequires: cyrus-sasl-devel
BuildRequires: openssl-devel
%if %{with_tests}
BuildRequires: %{?scl_prefix}php-json
BuildRequires: mongodb
BuildRequires: mongodb-server
%endif

Requires:     %{?scl_prefix}php(zend-abi) = %{php_zend_api}
Requires:     %{?scl_prefix}php(api) = %{php_core_api}
%{?_sclreq:Requires: %{?scl_prefix}runtime%{?_sclreq}%{?_isa}}

Provides:     %{?scl_prefix}php-%{pecl_name}               = %{version}
Provides:     %{?scl_prefix}php-%{pecl_name}%{?_isa}       = %{version}
Provides:     %{?scl_prefix}php-pecl(%{pecl_name})         = %{version}
Provides:     %{?scl_prefix}php-pecl(%{pecl_name})%{?_isa} = %{version}
%if "%{?scl_prefix}" != "%{?sub_prefix}"
Provides:     %{?scl_prefix}php-pecl-%{pecl_name}          = %{version}-%{release}
Provides:     %{?scl_prefix}php-pecl-%{pecl_name}%{?_isa}  = %{version}-%{release}
%endif

%if "%{?vendor}" == "Remi Collet" && 0%{!?scl:1} && 0%{?rhel}
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
%endif

%if 0%{?fedora} < 20 && 0%{?rhel} < 7
# Filter private shared provides
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}
%endif


%description
This package provides an interface for communicating with the
MongoDB database in PHP.

Documentation: http://php.net/mongo

Package built for PHP %(%{__php} -r 'echo PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')%{?scl: as Software Collection (%{scl} by %{?scl_vendor}%{!?scl_vendor:rh})}.


%prep
%setup -c -q

mv %{gh_project}-%{gh_commit} NTS
cp %{SOURCE1} %{ini_name}
mv NTS/package.xml .

%{?_licensedir:sed -e '/LICENSE/s/role="doc"/role="src"/' -i package.xml}

cd NTS
# Sanity check, really often broken
extver=$(sed -n '/#define PHP_MONGO_VERSION/{s/.* "//;s/".*$//;p}' php_mongo.h)
if test "x${extver}" != "x%{version}%{?prever}"; then
   : Error: Upstream extension version is ${extver}, expecting %{version}%{?prever}.
   exit 1
fi
cd ..

%if %{with_zts}
cp -pr NTS ZTS
%endif


%build
cd NTS
%{_bindir}/phpize
%configure  \
  --with-mongo-sasl \
  --with-php-config=%{_bindir}/php-config
make %{?_smp_mflags}

%if %{with_zts}
cd ../ZTS
%{_bindir}/zts-phpize
%configure  \
  --with-mongo-sasl \
  --with-php-config=%{_bindir}/zts-php-config
make %{?_smp_mflags}
%endif


%install
rm -rf %{buildroot}

make -C NTS install INSTALL_ROOT=%{buildroot}

# Drop in the bit of configuration
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
: Minimal load test for NTS extension
%{__php} -n \
    -d extension=%{buildroot}%{php_extdir}/%{pecl_name}.so \
    -i | grep "MongoDB Support => enabled"

%if %{with_tests}
cd NTS

: Create the configuration file
mkdir data
sed -e "/DBDIR/s:/data:$PWD/data:" \
    tests/utils/cfg.inc.template   \
    >tests/utils/cfg.inc

: Launch the test servers
MONGO_SERVER_STANDALONE=yes \
MONGO_SERVER_STANDALONE_AUTH=yes \
MONGO_SERVER_REPLICASET=yes \
MONGO_SERVER_REPLICASET_AUTH=yes \
make servers

: Ignore 2 tests
# need investigation (pass in local build)
rm tests/generic/bug00667.phpt
# fails with "hmh. you have to fast server!"
rm tests/standalone/bug01036-001.phpt

: Upstream test suite NTS extension
ret=0
TEST_PHP_EXECUTABLE=/usr/bin/php \
TEST_PHP_ARGS="-n -d extension=json.so -d extension=$PWD/modules/mongo.so" \
NO_INTERACTION=1 \
REPORT_EXIT_STATUS=1 \
%{__php} -n run-tests.php --show-diff || ret=1

: Cleanups
make stop-servers
rm -rf data

[ $ret -eq 0 ] || exit $ret
%endif

%if %{with_zts}
: Minimal load test for ZTS extension
%{__ztsphp} -n \
    -d extension=%{buildroot}%{php_ztsextdir}/%{pecl_name}.so \
    -i | grep "MongoDB Support => enabled"
%endif


%files
%defattr(-, root, root, -)
%{?_licensedir:%license NTS/LICENSE.md}
%doc %{pecl_docdir}/%{pecl_name}
%{pecl_xmldir}/%{name}.xml

%config(noreplace) %{php_inidir}/%{ini_name}
%{php_extdir}/%{pecl_name}.so

%if %{with_zts}
%config(noreplace) %{php_ztsinidir}/%{ini_name}
%{php_ztsextdir}/%{pecl_name}.so
%endif


%changelog
* Tue Apr 26 2016 Remi Collet <remi@fedoraproject.org> - 1.6.14-1
- update to 1.6.14 (stable)

* Fri Mar 18 2016 Remi Collet <remi@fedoraproject.org> - 1.6.13-1
- update to 1.6.13 (stable)

* Tue Mar  8 2016 Remi Collet <remi@fedoraproject.org> - 1.6.12-2
- adapt for F24
- fix license management

* Wed Nov 25 2015 Remi Collet <remi@fedoraproject.org> - 1.6.12-1
- update to 1.6.12 (stable)

* Tue Aug 25 2015 Remi Collet <remi@fedoraproject.org> - 1.6.11-1
- update to 1.6.11 (stable)

* Fri Jul  3 2015 Remi Collet <remi@fedoraproject.org> - 1.6.10-1
- update to 1.6.10 (stable)

* Wed Jun 10 2015 Remi Collet <remi@fedoraproject.org> - 1.6.9-1
- update to 1.6.9 (stable)

* Wed May 13 2015 Remi Collet <remi@fedoraproject.org> - 1.6.8-1
- update to 1.6.8 (stable)

* Tue Apr 28 2015 Remi Collet <remi@fedoraproject.org> - 1.6.7-1
- update to 1.6.7 (stable)

* Tue Mar 24 2015 Remi Collet <remi@fedoraproject.org> - 1.6.6-1
- update to 1.6.6 (stable)

* Sat Mar 14 2015 Remi Collet <remi@fedoraproject.org> - 1.6.5-1
- update to 1.6.5 (stable)
- openssl-devel required for build

* Tue Mar  3 2015 Remi Collet <remi@fedoraproject.org> - 1.6.4-1
- update to 1.6.4 (stable)

* Wed Feb 18 2015 Remi Collet <remi@fedoraproject.org> - 1.6.3-1
- update to 1.6.3 (stable)

* Wed Feb 11 2015 Remi Collet <remi@fedoraproject.org> - 1.6.2-1
- update to 1.6.2 (stable)

* Mon Feb  9 2015 Remi Collet <remi@fedoraproject.org> - 1.6.1-1
- update to 1.6.1 (stable)

* Thu Jan 29 2015 Remi Collet <remi@fedoraproject.org> - 1.6.0-1
- update to 1.6.0 (stable)
- drop runtime dependency on pear, new scriptlets

* Wed Dec 24 2014 Remi Collet <remi@fedoraproject.org> - 1.6.0-0.4.RC3
- Fedora 21 SCL mass rebuild

* Fri Dec 19 2014 Remi Collet <remi@fedoraproject.org> - 1.6.0-0.3.RC3
- Update to 1.6.0RC3 (beta)

* Wed Nov 19 2014 Remi Collet <remi@fedoraproject.org> - 1.6.0-0.2.RC2
- Update to 1.6.0RC2 (beta)

* Wed Nov 12 2014 Remi Collet <remi@fedoraproject.org> - 1.6.0-0.1.RC1
- Update to 1.6.0RC1 (beta)

* Wed Nov 12 2014 Remi Collet <remi@fedoraproject.org> - 1.5.8-1
- Update to 1.5.8 (stable)

* Tue Sep 16 2014 Remi Collet <remi@fedoraproject.org> - 1.5.7-1
- Update to 1.5.7 (stable)

* Tue Sep 16 2014 Remi Collet <remi@fedoraproject.org> - 1.5.6-1
- Update to 1.5.6 (stable)

* Mon Aug 25 2014 Remi Collet <rcollet@redhat.com> - 1.5.5-2
- allow SCL build

* Wed Jul 30 2014 Remi Collet <remi@fedoraproject.org> - 1.5.5-1
- Update to 1.5.5 (stable)

* Tue Jun 17 2014 Remi Collet <remi@fedoraproject.org> - 1.5.4-1
- Update to 1.5.4 (stable)

* Fri Jun 06 2014 Remi Collet <remi@fedoraproject.org> - 1.5.3-1
- Update to 1.5.3 (stable)
- drop dependency on php-json

* Tue May 06 2014 Remi Collet <remi@fedoraproject.org> - 1.5.2-1
- Update to 1.5.2 (stable)

* Thu Apr 10 2014 Remi Collet <remi@fedoraproject.org> - 1.5.1-2
- add numerical prefix to extension configuration file

* Sat Apr 05 2014 Remi Collet <remi@fedoraproject.org> - 1.5.1-1
- Update to 1.5.1 (stable)
- mongo.native_long not allowed on 32bits

* Fri Apr  4 2014 Remi Collet <remi@fedoraproject.org> - 1.5.0-1
- Update to 1.5.0 (no change since RC2)

* Tue Apr  1 2014 Remi Collet <remi@fedoraproject.org> - 1.5.0-0.3-RC2
- Update to 1.5.0RC2

* Tue Mar 11 2014 Remi Collet <remi@fedoraproject.org> - 1.5.0-0.2-RC1
- Update to 1.5.0RC1
- open https://jira.mongodb.org/browse/PHP-1009
  JSON is optional at buildtime but required at runtime
- always enable SASL support

* Wed Feb 26 2014 Remi Collet <remi@fedoraproject.org> - 1.5.0-0.1.alpha1
- Update to 1.5.0alpha1
- use sources from github for tests
- cleanup mongo.ini
- enable SASL support (Fedora >= 19, RHEL-7)
  https://jira.mongodb.org/browse/PHP-996
- add patch for JSON detection
  https://jira.mongodb.org/browse/PHP-995

* Tue Nov 05 2013 Remi Collet <remi@fedoraproject.org> - 1.4.5-1
- Update to 1.4.5
- install doc in pecl doc_dir
- cleanups for Copr

* Wed Sep 25 2013 Remi Collet <remi@fedoraproject.org> - 1.4.4-1
- Update to 1.4.4

* Mon Aug 19 2013 Remi Collet <remi@fedoraproject.org> - 1.4.3-1
- Update to 1.4.3

* Wed Jul 24 2013 Remi Collet <remi@fedoraproject.org> - 1.4.2-1
- Update to 1.4.2

* Mon Jun 03 2013 Remi Collet <remi@fedoraproject.org> - 1.4.1-1
- Update to 1.4.1

* Tue May 21 2013 Remi Collet <remi@fedoraproject.org> - 1.4.0-1
- Update to 1.4.0

* Wed Apr 10 2013 Remi Collet <remi@fedoraproject.org> - 1.3.7-1
- Update to 1.3.7

* Tue Mar 26 2013 Remi Collet <remi@fedoraproject.org> - 1.3.6-1
- Update to 1.3.6

* Fri Mar 15 2013 Remi Collet <remi@fedoraproject.org> - 1.3.5-1
- Update to 1.3.5

* Thu Jan 31 2013 Remi Collet <RPMS@FamilleCollet.com> - 1.3.4-1
- update to 1.3.4

* Wed Jan 16 2013 Remi Collet <RPMS@FamilleCollet.com> - 1.3.3-1
- update to 1.3.3

* Wed Dec 19 2012 Remi Collet <RPMS@FamilleCollet.com> - 1.3.2-1
- update to 1.3.2

* Tue Dec  4 2012 Remi Collet <RPMS@FamilleCollet.com> - 1.3.1-1
- update to 1.3.1

* Tue Nov 27 2012 Remi Collet <RPMS@FamilleCollet.com> - 1.3.0-1
- update to 1.3.0
- add new options allow_empty_keys, is_master_interval, ping_interval
- remove old option auto_reconnect
- add LICENSE from upstream github

* Wed Aug 01 2012 Remi Collet <RPMS@FamilleCollet.com> - 1.2.12-1
- update to 1.2.12

* Tue Apr 10 2012 Remi Collet <RPMS@FamilleCollet.com> - 1.2.10-2
- update to 1.2.10, php 5.4 build

* Tue Apr 10 2012 Remi Collet <RPMS@FamilleCollet.com> - 1.2.10-1
- update to 1.2.10, php 5.3 build

* Thu Feb 23 2012 Remi Collet <RPMS@FamilleCollet.com> - 1.2.9-2
- update to 1.2.9, php 5.4 build

* Thu Feb 23 2012 Remi Collet <RPMS@FamilleCollet.com> - 1.2.9-1
- update to 1.2.9, php 5.3 build

* Wed Feb 22 2012 Remi Collet <RPMS@FamilleCollet.com> - 1.2.8-2
- update to 1.2.8, php 5.4 build

* Wed Feb 22 2012 Remi Collet <RPMS@FamilleCollet.com> - 1.2.8-1
- update to 1.2.8, php 5.3 build

* Thu Jan 05 2012 Remi Collet <RPMS@FamilleCollet.com> - 1.2.7-2
- php 5.4 build

* Thu Jan 05 2012 Remi Collet <RPMS@FamilleCollet.com> - 1.2.7-1
- update to 1.2.7

* Fri Nov 18 2011 Remi Collet <RPMS@FamilleCollet.com> - 1.2.6-2
- php 5.4 build

* Sun Oct 02 2011 Remi Collet <RPMS@FamilleCollet.com> - 1.2.6-1
- update to 1.2.6

* Fri Sep 16 2011 Remi Collet <RPMS@FamilleCollet.com> - 1.2.5-1
- update to 1.2.5
- clean spec
- allow relocation
- build zts extension

* Sat Aug 27 2011 Remi Collet <RPMS@FamilleCollet.com> - 1.2.4-1
- update to 1.2.4

* Fri Aug 19 2011 Remi Collet <RPMS@FamilleCollet.com> - 1.2.3-1
- update to 1.2.3

* Sun Jul 17 2011 Remi Collet <RPMS@FamilleCollet.com> - 1.2.1-1
- rebuild for remi repo

* Sun Jul 17 2011 Christof Damian <christof@damian.net> - 1.2.1-1
- upstream 1.2.1

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.10-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Oct 26 2010 Remi Collet <RPMS@FamilleCollet.com> - 1.0.10-4
- rebuild for remi repo

* Mon Oct 25 2010 Christof Damian <christof@damian.net> - 1.0.10-4
- added link to option docs

* Sat Oct 23 2010 Christof Damian <christof@damian.net> - 1.0.10-3
- fix post
- add example config with sensible defaults
- add conditionals for EPEL + fix for check

* Fri Oct 22 2010 Christof Damian <christof@damian.net> - 1.0.10-2
- fixes for package review: requires and warnings

* Wed Oct 20 2010 Christof Damian <christof@damian.net> - 1.0.10-1
- Initial RPM
