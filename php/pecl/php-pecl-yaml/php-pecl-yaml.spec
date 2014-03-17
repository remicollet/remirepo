%{!?php_inidir:  %global php_inidir  %{_sysconfdir}/php.d}
%{!?__pecl:      %global __pecl      %{_bindir}/pecl}
%{!?__php:       %global __php       %{_bindir}/php}

%global with_zts   0%{?__ztsphp:1}
%global pecl_name  yaml

Summary:       PHP Bindings for yaml
Name:          php-pecl-yaml
Version:       1.1.1
Release:       1%{?dist}%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}
License:       MIT
Group:         Development/Languages
URL:           http://pecl.php.net/package/yaml

Source:        http://pecl.php.net/get/%{pecl_name}-%{version}.tgz

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: php-devel >= 5.2.0
BuildRequires: php-pear
BuildRequires: libyaml-devel

Requires(post): %{__pecl}
Requires(postun): %{__pecl}
Requires:      php(zend-abi) = %{php_zend_api}
Requires:      php(api) = %{php_core_api}

Provides:      php-%{pecl_name} = %{version}
Provides:      php-%{pecl_name}%{?_isa} = %{version}
Provides:      php-pecl(%{pecl_name}) = %{version}
Provides:      php-pecl(%{pecl_name})%{?_isa} = %{version}

# Other third party repo stuff
Obsoletes:     php53-pecl-%{pecl_name}
Obsoletes:     php53u-pecl-%{pecl_name}
Obsoletes:     php54-pecl-%{pecl_name}
%if "%{php_version}" > "5.5"
Obsoletes:     php55u-pecl-%{pecl_name}
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


%prep
%setup -c -q
mv %{pecl_name}-%{version} NTS

cd NTS
# honour --with-libdir option
# http://git.php.net/?p=pecl/file_formats/yaml.git;a=commitdiff;h=e1b40c36a8f0ba42a90c655ab3fc21bf4fb7d163
sed -e 's:/lib:/$PHP_LIBDIR:' -i config.m4

# Check upstream version (often broken)
extver=$(sed -n '/#define PHP_YAML_VERSION/{s/.* "//;s/".*$//;p}' php_yaml.h)
if test "x${extver}" != "x%{version}"; then
   : Error: Upstream version is ${extver}, expecting %{version}.
   exit 1
fi
cd ..

cat << 'EOF' | tee %{pecl_name}.ini
; Enable %{summary} extension module
extension=%{pecl_name}.so

; %{pecl_name} extension configuration
; see http://www.php.net/manual/en/yaml.configuration.php

; Decode entities which have the explicit tag "tag:yaml.org,2002:binary"
yaml.decode_binary = 0

; Controls the decoding of "tag:yaml.org,2002:timestamp"
; 0 will not apply any decoding, 1 will use strtotime() 2 will use date_create().
yaml.decode_timestamp = 0

; Cause canonical form output.
yaml.output_canonical = 0

; Number of spaces to indent sections. Value should be between 1 and 10.
yaml.output_indent = 2

; Set the preferred line width. -1 means unlimited.
yaml.output_width = 80
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
install -Dpm644 %{pecl_name}.ini %{buildroot}%{php_inidir}/%{pecl_name}.ini

%if %{with_zts}
make -C ZTS install INSTALL_ROOT=%{buildroot}
install -Dpm644 %{pecl_name}.ini %{buildroot}%{php_ztsinidir}/%{pecl_name}.ini
%endif

# Test & Documentation
cd NTS
for i in $(grep 'role="test"' ../package.xml | sed -e 's/^.*name="//;s/".*$//')
do install -Dpm 644 $i %{buildroot}%{pecl_testdir}/%{pecl_name}/$i
done
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
%{__php} -n run-tests.php

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
%{__ztsphp} -n run-tests.php

%endif


%clean
rm -rf %{buildroot}


%post
%{pecl_install} %{pecl_xmldir}/%{name}.xml >/dev/null || :


%postun
if [ $1 -eq 0 ] ; then
    %{pecl_uninstall} %{pecl_name} >/dev/null || :
fi


%files
%defattr(-, root, root, -)
%doc %{pecl_docdir}/%{pecl_name}
%doc %{pecl_testdir}/%{pecl_name}
%{pecl_xmldir}/%{name}.xml
%config(noreplace) %{php_inidir}/%{pecl_name}.ini
%{php_extdir}/%{pecl_name}.so

%if %{with_zts}
%config(noreplace) %{php_ztsinidir}/%{pecl_name}.ini
%{php_ztsextdir}/%{pecl_name}.so
%endif


%changelog
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
