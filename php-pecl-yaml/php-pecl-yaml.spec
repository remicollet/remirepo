%{!?__pecl: %{expand: %%global __pecl %{_bindir}/pecl}}

%global pecl_name yaml

Summary:       PHP Bindings for yaml
Name:          php-pecl-yaml
Version:       1.0.1
Release:       4%{?dist}
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
Provides:      php-pecl(%{pecl_name}) = %{version}
Requires:      php(zend-abi) = %{php_zend_api}
Requires:      php(api) = %{php_core_api}

# RPM 4.8
%{?filter_provides_in: %filter_provides_in %{php_extdir}/.*\.so$}
%{?filter_provides_in: %filter_provides_in %{php_ztsextdir}/.*\.so$}
%{?filter_setup}
# RPM 4.9
%global __provides_exclude_from %{?__provides_exclude_from:%__provides_exclude_from|}%{php_extdir}/.*\\.so$
%global __provides_exclude_from %__provides_exclude_from|%{php_ztsextdir}/.*\\.so$


%description
Support for YAML 1.1 (YAML Ain't Markup Language) serialization using the
LibYAML library.


%prep
%setup -c -q

extver=$(sed -n '/#define PHP_YAML_MODULE_VERSION/{s/.* "//;s/".*$//;p}' %{pecl_name}-%{version}/php_yaml.h)
if test "x${extver}" != "x%{version}"; then
   : Error: Upstream version is ${extver}, expecting %{version}.
   exit 1
fi

cat > %{pecl_name}.ini << 'EOF'
; Enable %{pecl_name} extension module
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

cp -pr %{pecl_name}-%{version} %{pecl_name}-%{version}-zts


%build
cd %{pecl_name}-%{version}
%{php_bindir}/phpize
%configure  --with-php-config=%{php_bindir}/php-config
make %{?_smp_mflags}

cd ../%{pecl_name}-%{version}-zts
%{php_ztsbindir}/phpize
%configure  --with-php-config=%{php_ztsbindir}/php-config
make %{?_smp_mflags}


%install
make -C %{pecl_name}-%{version} \
     install INSTALL_ROOT=%{buildroot}

make -C %{pecl_name}-%{version}-zts \
     install INSTALL_ROOT=%{buildroot}

# Install XML package description
install -Dpm 644 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml

# install config file
install -Dpm644 %{pecl_name}.ini %{buildroot}%{php_inidir}/%{pecl_name}.ini
install -Dpm644 %{pecl_name}.ini %{buildroot}%{php_ztsinidir}/%{pecl_name}.ini


%check
cd %{pecl_name}-%{version}
%{__php} --no-php-ini \
    --define extension_dir=modules \
    --define extension=%{pecl_name}.so \
    --modules | grep %{pecl_name}

make test NO_INTERACTION=1 | tee rpmtests.log

if grep -q "FAILED TEST" rpmtests.log; then
  for t in tests/*diff; do
     echo "*** FAILED: $(basename $t .diff)"
     diff -u tests/$(basename $t .diff).exp tests/$(basename $t .diff).out || :
  done
  exit 1
fi


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
%doc %{pecl_name}-%{version}/{CREDITS,LICENSE}
%config(noreplace) %{php_inidir}/%{pecl_name}.ini
%config(noreplace) %{php_ztsinidir}/%{pecl_name}.ini
%{php_extdir}/%{pecl_name}.so
%{php_ztsextdir}/%{pecl_name}.so
%{pecl_xmldir}/%{name}.xml


%changelog
* Wed Oct 05 2011 Remi Collet <Fedora@FamilleCollet.com> - 1.0.1-4
- ZTS extension
- spec cleanups

* Fri May 06 2011 Remi Collet <RPMS@FamilleCollet.com> - 1.0.1-2
- clean spec
- fix requirment, license, tests...

* Wed May 05 2011 Thomas Morse <tmorse@empowercampaigns.com> 1.0.1-1
- Version 1.0.1
- initial RPM
