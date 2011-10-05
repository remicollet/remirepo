%{!?__pecl:     %{expand: %%global __pecl     %{_bindir}/pecl}}

%global pecl_name rrd
%global pre       RC1

Summary:      PHP Bindings for rrdtool
Name:         php-pecl-rrd
Version:      1.0.5
Release:      0.1.%{pre}%{?dist}
License:      PHP
Group:        Development/Languages
URL:          http://pecl.php.net/package/rrd

Source:       http://pecl.php.net/get/%{pecl_name}-%{version}%{?pre}.tgz

# http://pecl.php.net/bugs/bug.php?id=24401
Patch0:       rrd-zts.patch


BuildRoot:    %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: php-devel >= 5.3.2
BuildRequires: rrdtool
BuildRequires: rrdtool-devel >= 1.3.0
BuildRequires: php-pear

Requires(post): %{__pecl}
Requires(postun): %{__pecl}
Conflicts:    rrdtool-php
Provides:     php-pecl(%{pecl_name}) = %{version}%{?pre}
Requires:     php(zend-abi) = %{php_zend_api}
Requires:     php(api) = %{php_core_api}


# RPM 4.8
%{?filter_provides_in: %filter_provides_in %{php_extdir}/.*\.so$}
%{?filter_provides_in: %filter_provides_in %{php_ztsextdir}/.*\.so$}
%{?filter_setup}
# RPM 4.9
%global __provides_exclude_from %{?__provides_exclude_from:%__provides_exclude_from|}%{php_extdir}/.*\\.so$
%global __provides_exclude_from %__provides_exclude_from|%{php_ztsextdir}/.*\\.so$


%description
Procedural and simple OO wrapper for rrdtool - data logging and graphing
system for time series data.


%prep 
%setup -c -q

cd %{pecl_name}-%{version}%{?pre}
%patch0 -p 1 -b .zts
cd ..

cp -r %{pecl_name}-%{version}%{?pre} %{pecl_name}-%{version}-zts

cat > %{pecl_name}.ini << 'EOF'
; Enable %{pecl_name} extension module
extension=%{pecl_name}.so
EOF


%build
cd %{pecl_name}-%{version}%{?pre}
%{php_bindir}/phpize
%configure --with-php-config=%{php_bindir}/php-config
make %{?_smp_mflags}

cd ../%{pecl_name}-%{version}-zts
%{php_ztsbindir}/phpize
%configure --with-php-config=%{php_ztsbindir}/php-config
make %{?_smp_mflags}


%install
rm -rf %{buildroot}
make install -C %{pecl_name}-%{version}%{?pre} INSTALL_ROOT=%{buildroot}
make install -C %{pecl_name}-%{version}-zts    INSTALL_ROOT=%{buildroot}

# Drop in the bit of configuration
install -D -m 644 %{pecl_name}.ini %{buildroot}%{php_inidir}/%{pecl_name}.ini
install -D -m 644 %{pecl_name}.ini %{buildroot}%{php_ztsinidir}/%{pecl_name}.ini

# Install XML package description
install -D -m 644 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml


%check
cd %{pecl_name}-%{version}%{?pre}
%{__php} --no-php-ini \
    --define extension_dir=modules \
    --define extension=%{pecl_name}.so \
    --modules | grep %{pecl_name}


make -C tests/data clean
make -C tests/data all
make test NO_INTERACTION=1 | tee rpmtests.log

if  grep -q "FAILED TEST" rpmtests.log; then
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


%post
%{pecl_install} %{pecl_xmldir}/%{name}.xml >/dev/null || :


%postun
if [ $1 -eq 0 ] ; then
    %{pecl_uninstall} %{pecl_name} >/dev/null || :
fi


%files
%defattr(-, root, root, -)
%doc %{pecl_name}-%{version}%{?pre}/{CREDITS,LICENSE}
%config(noreplace) %{php_inidir}/%{pecl_name}.ini
%config(noreplace) %{php_ztsinidir}/%{pecl_name}.ini
%{php_extdir}/%{pecl_name}.so
%{php_ztsextdir}/%{pecl_name}.so
%{pecl_xmldir}/%{name}.xml


%changelog
* Wed Oct 05 2011 Remi Collet <Fedora@FamilleCollet.com> 1.0.5-0.1.RC1
- update to 1.0.5RC1
- build ZTS extension

* Tue Aug 16 2011 Remi Collet <Fedora@FamilleCollet.com> 1.0.4-1
- Version 1.0.4 (stable) - API 1.0.4 (stable)
- fix filters

* Fri Apr 29 2011 Remi Collet <Fedora@FamilleCollet.com> 1.0.3-1
- Version 1.0.3 (stable) - API 1.0.3 (stable)
- no change in sources

* Wed Apr 20 2011 Remi Collet <Fedora@FamilleCollet.com> 1.0.2-1
- Version 1.0.2 (stable) - API 1.0.2 (stable)
- no change in sources

* Sat Apr 16 2011 Remi Collet <Fedora@FamilleCollet.com> 1.0.1-1
- Version 1.0.1 (stable) - API 1.0.1 (stable)
- no change in sources
- remove generated Changelog (only latest version, no real value)

* Tue Apr 12 2011 Remi Collet <Fedora@FamilleCollet.com> 1.0.0-1
- Version 1.0.0 (stable) - API 1.0.0 (stable)
- remove all patches merged by upstream

* Sat Mar 05 2011 Remi Collet <Fedora@FamilleCollet.com> 0.10.0-2
- improved patches
- implement rrd_strversion

* Fri Mar 04 2011 Remi Collet <Fedora@FamilleCollet.com> 0.10.0-1
- Version 0.10.0 (stable) - API 0.10.0 (beta)
- remove patches, merged upstream
- add links to 5 new upstream bugs

* Mon Jan 03 2011 Remi Collet <Fedora@FamilleCollet.com> 0.9.0-1
- Version 0.9.0 (beta) - API 0.9.0 (beta)
- initial RPM

