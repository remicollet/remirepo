%{!?__pecl:     %{expand: %%global __pecl     %{_bindir}/pecl}}

%global pecl_name rrd


Summary:      PHP Bindings for rrdtool
Name:         php-pecl-rrd
Version:      1.1.0
Release:      1%{?dist}.1
License:      BSD
Group:        Development/Languages
URL:          http://pecl.php.net/package/rrd

Source:       http://pecl.php.net/get/%{pecl_name}-%{version}%{?pre}.tgz

BuildRoot:    %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: php-devel >= 5.3.2
BuildRequires: rrdtool
BuildRequires: rrdtool-devel >= 1.3.0
BuildRequires: php-pear

Requires(post): %{__pecl}
Requires(postun): %{__pecl}
Requires:     php(zend-abi) = %{php_zend_api}
Requires:     php(api) = %{php_core_api}

Conflicts:    rrdtool-php
Provides:     php-pecl(%{pecl_name}) = %{version}%{?pre}
Provides:     php-pecl(%{pecl_name})%{?_isa} = %{version}%{?pre}
Provides:     php-%{pecl_name} = %{version}%{?pre}
Provides:     php-%{pecl_name}%{?_isa} = %{version}%{?pre}


# Filter private shared object
%{?filter_provides_in: %filter_provides_in %{_dir}/.*\.so$}
%{?filter_setup}


%description
Procedural and simple OO wrapper for rrdtool - data logging and graphing
system for time series data.


%prep 
%setup -c -q

cp -r %{pecl_name}-%{version}%{?pre} %{pecl_name}-%{version}-zts

extver=$(sed -n '/#define PHP_RRD_VERSION/{s/.* "//;s/".*$//;p}' %{pecl_name}-%{version}%{?pre}/php_rrd.h)
if test "x${extver}" != "x%{version}%{?pre}"; then
   : Error: Upstream version is ${extver}, expecting %{version}.
   exit 1
fi

cat > %{pecl_name}.ini << 'EOF'
; Enable %{pecl_name} extension module
extension=%{pecl_name}.so
EOF


%build
cd %{pecl_name}-%{version}%{?pre}
%{_bindir}/phpize
%configure --with-php-config=%{_bindir}/php-config
make %{?_smp_mflags}

cd ../%{pecl_name}-%{version}-zts
%{_bindir}/zts-phpize
%configure --with-php-config=%{_bindir}/zts-php-config
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
%{__ztsphp} --no-php-ini \
    --define extension_dir=%{pecl_name}-%{version}-zts/modules \
    --define extension=%{pecl_name}.so \
    --modules | grep %{pecl_name}

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

  # tests only succeed with some rrdtool version (> 1.4.0 but < 1.4.7)
  # because of difference between image size / position
  # http://pecl.php.net/bugs/22642

  # only consider result of rrd_version test
  [ -f tests/rrd_020.diff ] && exit 1
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
* Thu Jan 24 2013 Remi Collet <remi@fedoraproject.org> - 1.1.0-1.1
- also provides php-rrd

* Sun Aug 12 2012 Remi Collet <remi@fedoraproject.org> - 1.1.0-1
- Version 1.1.0 (stable), api 1.1.0 (stable)

* Tue Jul 31 2012 Remi Collet <remi@fedoraproject.org> - 1.0.5-4
- ignore test results (fails with rrdtool 1.4.7)

* Fri Nov 18 2011 Remi Collet <Fedora@FamilleCollet.com> 1.0.5-2
- build against php 5.4

* Fri Nov 18 2011 Remi Collet <Fedora@FamilleCollet.com> 1.0.5-1
- update to 1.0.5
- change license from PHP to BSD

* Sun Nov 13 2011 Remi Collet <remi@fedoraproject.org> - 1.0.5-0.3.RC2
- build against php 5.4

* Mon Oct 17 2011 Remi Collet <Fedora@FamilleCollet.com> 1.0.5-0.2.RC2
- update to 1.0.5RC2
- drop patch merged upstream

* Wed Oct 05 2011 Remi Collet <Fedora@FamilleCollet.com> 1.0.5-0.1.RC1
- update to 1.0.5RC1
- build ZTS extension
- patch for https://bugs.php.net/bug.php?id=59992

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

