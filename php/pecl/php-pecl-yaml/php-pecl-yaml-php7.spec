# remirepo spec file for php-pecl-yaml
#
# Copyright (c) 2012-2016 Remi Collet

# Fedora spec file for php-pecl-yaml
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please, preserve the changelog entries
#
%if 0%{?scl:1}
%global sub_prefix %{scl_prefix}
%scl_package       php-pecl-yaml
%endif

%global with_zts   0%{!?_without_zts:%{?__ztsphp:1}}
%global pecl_name  yaml
%global ini_name   40-%{pecl_name}.ini
%global prever     RC8

Summary:       PHP Bindings for yaml
Name:          %{?sub_prefix}php-pecl-yaml
Version:       2.0.0
Release:       0.10.%{prever}%{?dist}%{!?scl:%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}}
License:       MIT
Group:         Development/Languages
URL:           http://pecl.php.net/package/yaml

Source:        http://pecl.php.net/get/%{pecl_name}-%{version}%{?prever}.tgz

BuildRequires: %{?scl_prefix}php-devel >= 7
BuildRequires: %{?scl_prefix}php-pear
BuildRequires: libyaml-devel

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
# Filter private shared
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}
%endif


%description
Support for YAML 1.1 (YAML Ain't Markup Language) serialization using the
LibYAML library.

Documentation: http://php.net/yaml

Package built for PHP %(%{__php} -r 'echo PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')%{?scl: as Software Collection (%{scl} by %{?scl_vendor}%{!?scl_vendor:rh})}.


%prep
%setup -c -q
mv %{pecl_name}-%{version}%{?prever} NTS

# Remove test file to avoid regsitration
sed -e 's/role="test"/role="src"/' \
    %{?_licensedir:-e '/LICENSE/s/role="doc"/role="src"/' } \
    -i package.xml

cd NTS
# Check upstream version (often broken)
extver=$(sed -n '/#define PHP_YAML_VERSION/{s/.* "//;s/".*$//;p}' php_yaml.h)
if test "x${extver}" != "x%{version}%{?prever}"; then
   : Error: Upstream version is ${extver}, expecting %{version}%{?prever}.
   exit 1
fi
cd ..

cat << 'EOF' | tee %{ini_name}
; Enable %{summary} extension module
extension=%{pecl_name}.so

; %{pecl_name} extension configuration
; see http://www.php.net/manual/en/yaml.configuration.php

; Decode entities which have the explicit tag "tag:yaml.org,2002:binary"
;yaml.decode_binary = 0

; Controls the decoding of "tag:yaml.org,2002:timestamp"
; 0 will not apply any decoding, 1 will use strtotime() 2 will use date_create().
;yaml.decode_timestamp = 0

; Cause canonical form output.
;yaml.output_canonical = 0

; Number of spaces to indent sections. Value should be between 1 and 10.
;yaml.output_indent = 2

; Set the preferred line width. -1 means unlimited.
;yaml.output_width = 80

; Enable/disable serialized php object processing.
;yaml.decode_php = 0
EOF

cp -pr NTS ZTS


%build
cd NTS

%{_bindir}/phpize
%configure \
    --with-libdir=%{_lib} \
    --with-php-config=%{_bindir}/php-config
make %{?_smp_mflags}

%if %{with_zts}
cd ../ZTS
%{_bindir}/zts-phpize
%configure \
    --with-libdir=%{_lib} \
    --with-php-config=%{_bindir}/zts-php-config
make %{?_smp_mflags}
%endif


%install
make -C NTS install INSTALL_ROOT=%{buildroot}

# Install XML package description
install -Dpm 644 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml

# install config file
install -Dpm644 %{ini_name} %{buildroot}%{php_inidir}/%{ini_name}

%if %{with_zts}
make -C ZTS install INSTALL_ROOT=%{buildroot}
install -Dpm644 %{ini_name} %{buildroot}%{php_ztsinidir}/%{ini_name}
%endif

# Documentation
cd NTS
for i in $(grep 'role="doc"' ../package.xml | sed -e 's/^.*name="//;s/".*$//')
do install -Dpm 644 $i %{buildroot}%{pecl_docdir}/%{pecl_name}/$i
done


%check
cd NTS
: Minimal load test for NTS extension
%{__php} --no-php-ini \
    --define extension=modules/%{pecl_name}.so \
    --modules | grep %{pecl_name}

: Upstream test suite for NTS extension
TEST_PHP_EXECUTABLE=%{__php} \
TEST_PHP_ARGS="-n -d extension=$PWD/modules/%{pecl_name}.so" \
NO_INTERACTION=1 \
REPORT_EXIT_STATUS=1 \
%{__php} -n run-tests.php --show-diff

%if %{with_zts}
cd ../ZTS
: Minimal load test for ZTS extension
%{__ztsphp} --no-php-ini \
    --define extension=modules/%{pecl_name}.so \
    --modules | grep %{pecl_name}

: Upstream test suite for ZTS extension
TEST_PHP_EXECUTABLE=%{__ztsphp} \
TEST_PHP_ARGS="-n -d extension=$PWD/modules/%{pecl_name}.so" \
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
%config(noreplace) %{php_ztsinidir}/%{ini_name}
%{php_ztsextdir}/%{pecl_name}.so
%endif


%changelog
* Wed Sep 14 2016 Remi Collet <remi@fedoraproject.org> - 2.0.0-0.10.RC8
- rebuild for PHP 7.1 new API version

* Mon Jun  6 2016 Remi Collet <remi@fedoraproject.org> - 2.0.0-0.9.RC8
- update to 2.0.0RC8

* Sun Mar  6 2016 Remi Collet <remi@fedoraproject.org> - 2.0.0-0.8.RC7
- adapt for F24

* Tue Mar  1 2016 Remi Collet <remi@fedoraproject.org> - 2.0.0-0.7.RC7
- skip yaml_002.phpt, see https://bugs.php.net/71696

* Thu Dec 31 2015 Remi Collet <remi@fedoraproject.org> - 2.0.0-0.6.RC7
- update to 2.0.0RC7

* Tue Dec  8 2015 Remi Collet <remi@fedoraproject.org> - 2.0.0-0.5.RC6
- update to 2.0.0RC6

* Sun Oct 18 2015 Remi Collet <remi@fedoraproject.org> - 2.0.0-0.4.RC5
- update to 2.0.0RC5

* Sat Oct 17 2015 Remi Collet <remi@fedoraproject.org> - 2.0.0-0.3.RC4
- update to 2.0.0RC4

* Sat Oct 17 2015 Remi Collet <remi@fedoraproject.org> - 2.0.0-0.2.RC2
- add uptream patches, fix segfault and test suite

* Sat Oct 17 2015 Remi Collet <remi@fedoraproject.org> - 2.0.0-0.1.RC2
- update to 2.0.0RC2 for PHP 7
- 2 failed tests, so ignore test suite results for now

* Sat Oct 17 2015 Remi Collet <remi@fedoraproject.org> - 2.0.0-0.1.RC1
- update to 2.0.0RC1 for PHP 7

* Tue Jun 23 2015 Remi Collet <remi@fedoraproject.org> - 1.2.0-2
- allow build against rh-php56 (as more-php56)

* Mon May 18 2015 Remi Collet <remi@fedoraproject.org> - 1.2.0-1
- Update to 1.2.0 (stable)

* Mon May  4 2015 Remi Collet <remi@fedoraproject.org> - 1.1.1-6
- drop runtime dependency on pear, new scriptlets

* Wed Dec 24 2014 Remi Collet <remi@fedoraproject.org> - 1.1.1-5.1
- Fedora 21 SCL mass rebuild

* Fri Aug 29 2014 Remi Collet <rcollet@redhat.com> - 1.1.1-5
- don't install tests

* Mon Aug 25 2014 Remi Collet <rcollet@redhat.com> - 1.1.1-4
- improve SCL build

* Thu Apr 17 2014 Remi Collet <remi@fedoraproject.org> - 1.1.1-3
- add numerical prefix to extension configuration file (php 5.6)

* Wed Mar 19 2014 Remi Collet <rcollet@redhat.com> - 1.1.1-2
- allow SCL build

* Tue Nov 19 2013 Remi Collet <remi@fedoraproject.org> - 1.1.1-1
- Update to 1.1.1 (stable)
- install doc in pecl doc_dir
- install tests in pecl test_dir

* Fri Nov 30 2012 Remi Collet <RPMS@FamilleCollet.com> - 1.1.0-2.1
- also provides php-yaml

* Fri Apr 20 2012 Remi Collet <RPMS@FamilleCollet.com> - 1.1.0-2
- update to 1.0.1 for php 5.4

* Fri Apr 20 2012 Remi Collet <RPMS@FamilleCollet.com> - 1.1.0-1
- update to 1.0.1 for php 5.3

* Fri Apr 20 2012 Theodore Lee <theo148@gmail.com> - 1.1.0-1
- Update to upstream 1.1.0 release
- Drop upstreamed cflags patch

* Sun Nov 13 2011 Remi Collet <remi@fedoraproject.org> - 1.0.1-5
- build against php 5.4

* Wed Oct 05 2011 Remi Collet <Fedora@FamilleCollet.com> - 1.0.1-4
- ZTS extension
- spec cleanups

* Fri May 06 2011 Remi Collet <RPMS@FamilleCollet.com> - 1.0.1-2
- clean spec
- fix requirment, license, tests...

* Thu May 05 2011 Thomas Morse <tmorse@empowercampaigns.com> 1.0.1-1
- Version 1.0.1
- initial RPM

