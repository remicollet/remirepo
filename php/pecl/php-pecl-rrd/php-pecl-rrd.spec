# spec file for php-pecl-rrd
#
# Copyright (c) 2011-2014 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/3.0/
#
# Please, preserve the changelog entries
#
%{?scl:          %scl_package        php-pecl-rrd}
%{!?php_inidir:  %global php_inidir  %{_sysconfdir}/php.d}
%{!?__pecl:      %global __pecl      %{_bindir}/pecl}
%{!?__php:       %global __php       %{_bindir}/php}

%global with_zts  0%{?__ztsphp:1}
%global pecl_name rrd


Summary:      PHP Bindings for rrdtool
Name:         %{?scl_prefix}php-pecl-rrd
Version:      1.1.3
Release:      1%{?dist}%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}
License:      BSD
Group:        Development/Languages
URL:          http://pecl.php.net/package/rrd

Source:       http://pecl.php.net/get/%{pecl_name}-%{version}%{?pre}.tgz

BuildRoot:    %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: %{?scl_prefix}php-devel >= 5.3.2
BuildRequires: rrdtool
BuildRequires: rrdtool-devel >= 1.3.0
BuildRequires: %{?scl_prefix}php-pear

Requires(post): %{__pecl}
Requires(postun): %{__pecl}
Requires:     %{?scl_prefix}php(zend-abi) = %{php_zend_api}
Requires:     %{?scl_prefix}php(api) = %{php_core_api}

Conflicts:    %{?scl_prefix}rrdtool-php
Provides:     %{?scl_prefix}php-pecl(%{pecl_name}) = %{version}%{?pre}
Provides:     %{?scl_prefix}php-pecl(%{pecl_name})%{?_isa} = %{version}%{?pre}
Provides:     %{?scl_prefix}php-%{pecl_name} = %{version}%{?pre}
Provides:     %{?scl_prefix}php-%{pecl_name}%{?_isa} = %{version}%{?pre}


%if 0%{!?scl:1}
# Other third party repo stuff
%if "%{php_version}" > "5.4"
Obsoletes:     php53-pecl-%{pecl_name}
Obsoletes:     php53u-pecl-%{pecl_name}
Obsoletes:     php54-pecl-%{pecl_name}
%endif
%if "%{php_version}" > "5.5"
Obsoletes:     php55u-pecl-%{pecl_name}
%endif
%endif

%if 0%{?fedora} < 20
# Filter shared private
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}
%endif


%description
Procedural and simple OO wrapper for rrdtool - data logging and graphing
system for time series data.


%prep 
%setup -c -q

mv %{pecl_name}-%{version} NTS

cat > %{pecl_name}.ini << 'EOF'
; Enable %{pecl_name} extension module
extension=%{pecl_name}.so
EOF

%if %{with_zts}
cp -r  NTS ZTS
%endif


%build
cd NTS
%{_bindir}/phpize
%configure --with-php-config=%{_bindir}/php-config
make %{?_smp_mflags}

%if %{with_zts}
cd ../ZTS
%{_bindir}/zts-phpize
%configure --with-php-config=%{_bindir}/zts-php-config
make %{?_smp_mflags}
%endif


%install
rm -rf %{buildroot}
make install -C NTS INSTALL_ROOT=%{buildroot}

# Drop in the bit of configuration
install -D -m 644 %{pecl_name}.ini %{buildroot}%{php_inidir}/%{pecl_name}.ini

# Install XML package description
install -D -m 644 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml

%if %{with_zts}
make install -C ZTS INSTALL_ROOT=%{buildroot}
install -D -m 644 %{pecl_name}.ini %{buildroot}%{php_ztsinidir}/%{pecl_name}.ini
%endif

# Test & Documentation
for i in $(grep 'role="test"' package.xml | sed -e 's/^.*name="//;s/".*$//')
do install -Dpm 644 NTS/$i %{buildroot}%{pecl_testdir}/%{pecl_name}/$i
done
for i in $(grep 'role="doc"' package.xml | sed -e 's/^.*name="//;s/".*$//')
do install -Dpm 644 NTS/$i %{buildroot}%{pecl_docdir}/%{pecl_name}/$i
done


%check
%if %{with_zts}
%{__ztsphp} --no-php-ini \
    --define extension=ZTS/modules/%{pecl_name}.so \
    --modules | grep %{pecl_name}
%endif

cd NTS
%{__php} --no-php-ini \
    --define extension=modules/%{pecl_name}.so \
    --modules | grep %{pecl_name}


%if 0%{?fedora} < 14 && 0%{?rhel} < 7
  # skip tests which only succeed with rrdtool > 1.4.0
  rm tests/rrd_012.phpt \
     tests/rrd_017.phpt
%endif

make -C tests/data clean
make -C tests/data all
make test NO_INTERACTION=1 | tee rpmtests.log

if  grep -q "FAILED TEST" rpmtests.log; then
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
* Wed Jan 15 2014 Remi Collet <remi@fedoraproject.org> - 1.1.3-1
- Update to 1.1.3 (stable)

* Tue Jan 14 2014 Remi Collet <remi@fedoraproject.org> - 1.1.2-2
- fix upstream patch

* Tue Jan 14 2014 Remi Collet <remi@fedoraproject.org> - 1.1.2-1
- Update to 1.1.2 (stable)
- install doc in pecl doc_dir
- install tests in pecl test_dir
- adapt for SCL

* Mon Sep 09 2013 Remi Collet <remi@fedoraproject.org> - 1.1.1-1
- Update to 1.1.1

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

