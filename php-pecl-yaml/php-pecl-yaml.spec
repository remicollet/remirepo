%{!?__pecl: %{expand: %%global __pecl %{_bindir}/pecl}}
%{!?php_extdir: %{expand: %%global php_extdir %(php-config --extension-dir)}}

%global pecl_name yaml

Summary: PHP Bindings for yaml
Name: php-pecl-yaml
Version: 1.0.1
Release: 1%{?dist}
License: PHP
Group: Development/Languages
URL: http://pecl.php.net/package/yaml

Source: http://pecl.php.net/get/%{pecl_name}-%{version}.tgz

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: php-devel >= 5.3.2
BuildRequires: php-pear
BuildRequires: libyaml-devel

Requires(post): %{__pecl}
Requires(postun): %{__pecl}
Provides: php-pecl(%{pecl_name}) = %{version}
Requires: php(zend-abi) = %{php_zend_api}
Requires: php(api) = %{php_core_api}
Requires: libyaml

%{?filter_setup:
%filter_provides_in %{php_extdir}/.*\.so$
%filter_setup
}


%description
Support for YAML 1.1 (YAML Ain't Markup Language) serialization using the LibYAML library.

%prep
%setup -c -q


%build
cd %{pecl_name}-%{version}
phpize
%configure

make %{?_smp_mflags}


%install
cd %{pecl_name}-%{version}
rm -rf %{buildroot}
make install INSTALL_ROOT=%{buildroot}

# Drop in the bit of configuration
mkdir -p %{buildroot}%{_sysconfdir}/php.d
cat > %{buildroot}%{_sysconfdir}/php.d/%{pecl_name}.ini << 'EOF'
; Enable %{pecl_name} extension module
extension=%{pecl_name}.so
EOF

# Install XML package description
mkdir -p %{buildroot}%{pecl_xmldir}
install -m 644 ../package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml


%check
cd %{pecl_name}-%{version}
php --no-php-ini \
    --define extension_dir=modules \
    --define extension=%{pecl_name}.so \
    --modules | grep %{pecl_name}


make test NO_INTERACTION=1 | tee rpmtests.log

if grep -q "FAILED TEST" rpmtests.log; then
  for t in tests/*diff; do
     echo "*** FAILED: $(basename $t .diff)"
     diff -u tests/$(basename $t .diff).exp tests/$(basename $t .diff).out || :
  done
%if 0%{?fedora} >= 14
  # tests only succeed with rrdtool 1.4.x
  # http://pecl.php.net/bugs/22642
  exit 1
%endif
fi

%clean
rm -rf %{buildroot}


%if 0%{?pecl_install:1}
%post
%{pecl_install} %{pecl_xmldir}/%{name}.xml >/dev/null || :
%endif


%if 0%{?pecl_uninstall:1}
%postun
if [ $1 -eq 0 ] ; then
    %{pecl_uninstall} %{pecl_name} >/dev/null || :
fi
%endif


%files
%defattr(-, root, root, -)
%doc %{pecl_name}-%{version}/CREDITS %{pecl_name}-%{version}/LICENSE
%config(noreplace) %{_sysconfdir}/php.d/%{pecl_name}.ini
%{php_extdir}/%{pecl_name}.so
%{pecl_xmldir}/%{name}.xml


%changelog
* Wed May 05 2011 Thomas Morse <tmorse@empowercampaigns.com> 1.0.1-1
- Version 1.0.1
- initial RPM
