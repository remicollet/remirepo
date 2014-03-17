%{!?php_inidir:  %global php_inidir  %{_sysconfdir}/php.d}
%{!?__pecl:      %global __pecl      %{_bindir}/pecl}
%{!?__php:       %global __php       %{_bindir}/php}

%global pecl_name   mongo
%global with_zts    0%{?__ztsphp:1}

Summary:      PHP MongoDB database driver
Name:         php-pecl-mongo
Version:      1.4.5
Release:      1%{?dist}%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}
License:      ASL 2.0
Group:        Development/Languages
URL:          http://pecl.php.net/package/%{pecl_name}

Source0:      http://pecl.php.net/get/%{pecl_name}-%{version}.tgz
Source1:      %{pecl_name}.ini

BuildRoot:    %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: php-devel >= 5.2.6
BuildRequires: php-pear

Requires(post): %{__pecl}
Requires(postun): %{__pecl}
Requires:     php(zend-abi) = %{php_zend_api}
Requires:     php(api) = %{php_core_api}

Provides:     php-%{pecl_name} = %{version}
Provides:     php-%{pecl_name}%{?_isa} = %{version}
Provides:     php-pecl(%{pecl_name}) = %{version}
Provides:     php-pecl(%{pecl_name})%{?_isa} = %{version}

# Other third party repo stuff
%if "%{php_version}" > "5.4"
Obsoletes:     php53-pecl-%{pecl_name}
Obsoletes:     php53u-pecl-%{pecl_name}
Obsoletes:     php54-pecl-%{pecl_name}
%endif
%if "%{php_version}" > "5.5"
Obsoletes:     php55u-pecl-%{pecl_name}
%endif

%if 0%{?fedora} < 20 && 0%{?rhel} < 7
# Filter private shared provides
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}
%endif


%description
This package provides an interface for communicating with the
MongoDB database in PHP.


%prep 
%setup -c -q

mv %{pecl_name}-%{version} NTS
cd NTS

extver=$(sed -n '/#define PHP_MONGO_VERSION/{s/.* "//;s/".*$//;p}' php_mongo.h)
if test "x${extver}" != "x%{version}%{?pre}"; then
   : Error: Upstream version is ${extver}, expecting %{version}.
   exit 1
fi
cd ..

cp %{SOURCE1} .

%if %{with_zts}
cp -pr NTS ZTS
%endif


%build
cd NTS
%{_bindir}/phpize
%configure  --with-php-config=%{_bindir}/php-config
make %{?_smp_mflags}

%if %{with_zts}
cd ../ZTS
%{_bindir}/zts-phpize
%configure  --with-php-config=%{_bindir}/zts-php-config
make %{?_smp_mflags}
%endif

%install
rm -rf %{buildroot}

make -C NTS install INSTALL_ROOT=%{buildroot}

# Drop in the bit of configuration
install -D -m 644 %{pecl_name}.ini %{buildroot}%{php_inidir}/%{pecl_name}.ini

# Install XML package description
install -D -m 644 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml

%if %{with_zts}
make -C ZTS install INSTALL_ROOT=%{buildroot}
install -D -m 644 %{pecl_name}.ini %{buildroot}%{php_ztsinidir}/%{pecl_name}.ini
%endif

# Documentation
for i in $(grep 'role="doc"' package.xml | sed -e 's/^.*name="//;s/".*$//')
do install -Dpm 644 NTS/$i %{buildroot}%{pecl_docdir}/%{pecl_name}/$i
done


%clean
rm -rf %{buildroot}


%post
%{pecl_install} %{pecl_xmldir}/%{name}.xml >/dev/null || :


%postun
if [ "$1" -eq "0" ]; then
   %{pecl_uninstall} %{pecl_name} >/dev/null || :
fi


%check
: Minimal load test for NTS extension
%{__php} -n \
    -d extension=%{buildroot}%{php_extdir}/%{pecl_name}.so \
    -i | grep "MongoDB Support => enabled"

%if %{with_zts}
: Minimal load test for ZTS extension
%{__ztsphp} -n \
    -d extension=%{buildroot}%{php_ztsextdir}/%{pecl_name}.so \
    -i | grep "MongoDB Support => enabled"
%endif


%files
%defattr(-, root, root, -)
%doc %{pecl_docdir}/%{pecl_name}
%config(noreplace) %{php_inidir}/%{pecl_name}.ini
%{php_extdir}/%{pecl_name}.so
%{pecl_xmldir}/%{name}.xml

%if %{with_zts}
%config(noreplace) %{php_ztsinidir}/%{pecl_name}.ini
%{php_ztsextdir}/%{pecl_name}.so
%endif


%changelog
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
