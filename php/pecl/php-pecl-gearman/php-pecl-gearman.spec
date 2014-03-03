# spec file for php-pecl-gearman
#
# Copyright (c) 2011-2014 Remi Collet
# Copyright (c) 2011 Paul Whalen
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please, preserve the changelog entries
#
%{!?php_inidir:  %global php_inidir   %{_sysconfdir}/php.d}
%{!?__pecl:      %global __pecl       %{_bindir}/pecl}
%{!?__php:       %global __php        %{_bindir}/php}

%global pecl_name gearman
%global with_zts  0%{?__ztsphp:1}

%if 0%{?fedora} >= 12 && 0%{?fedora} <= 15
%global extver 0.8.3
%global libver 0.10
%endif
%if 0%{?fedora} >= 16 && 0%{?fedora} <= 18
%global extver 1.0.3
%global libver 0.21
%endif
%if 0%{?fedora} >= 19 || 0%{?rhel} >= 5
%global extver 1.1.2
%global libver 1.1.0
%endif


Name:           php-pecl-gearman
Version:        %{extver}
Release:        2%{?dist}%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}
Summary:        PHP wrapper to libgearman

Group:          Development/Tools
License:        PHP
URL:            http://gearman.org
Source0:        http://pecl.php.net/get/%{pecl_name}-%{version}.tgz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  libgearman-devel > %{libver}
BuildRequires:  php-devel
BuildRequires:  php-pear
# Required by phpize
BuildRequires:  autoconf, automake, libtool

Requires:       php(zend-abi) = %{php_zend_api}
Requires:       php(api) = %{php_core_api}
Requires(post): %{__pecl}
Requires(postun): %{__pecl}

Provides:       php-%{pecl_name} = %{version}
Provides:       php-%{pecl_name}%{?_isa} = %{version}
Provides:       php-pecl(%{pecl_name}) = %{version}
Provides:       php-pecl(%{pecl_name})%{?_isa} = %{version}

# Other third party repo stuff
Obsoletes:      php53-pecl-%{pecl_name}
Obsoletes:      php53u-pecl-%{pecl_name}
%if "%{php_version}" > "5.4"
Obsoletes:      php54-pecl-%{pecl_name}
%endif
%if "%{php_version}" > "5.5"
Obsoletes:      php55u-pecl-%{pecl_name}
%endif
%if "%{php_version}" > "5.6"
Obsoletes:      php56u-pecl-%{pecl_name}
%endif

%if 0%{?fedora} < 20
# Filter shared private
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}
%endif


%description
This extension uses libgearman library to provide API for
communicating with gearmand, and writing clients and workers

Documentation: http://php.net/gearman


%prep
%setup -q -c
mv %{pecl_name}-%{version} NTS

extver=$(sed -n '/#define PHP_GEARMAN_VERSION/{s/.* "//;s/".*$//;p}' NTS/php_gearman.h)
if test "x${extver}" != "x%{version}"; then
   : Error: Upstream version is ${extver}, expecting %{version}.
   exit 1
fi

cat >%{pecl_name}.ini <<EOF
; enable %{pecl_name} extension
extension=%{pecl_name}.so
EOF

find NTS -type f -exec chmod -x {} \;

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

# Install XML package description
install -Dpm 644 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml

# install config file
install -Dpm644 %{pecl_name}.ini %{buildroot}%{php_inidir}/%{pecl_name}.ini

%if %{with_zts}
make -C ZTS install INSTALL_ROOT=%{buildroot}
install -Dpm644 %{pecl_name}.ini %{buildroot}%{php_ztsinidir}/%{pecl_name}.ini
%endif

# Test & Documentation
for i in $(grep 'role="test"' package.xml | sed -e 's/^.*name="//;s/".*$//')
do install -Dpm 644 NTS/$i %{buildroot}%{pecl_testdir}/%{pecl_name}/$i
done
for i in LICENSE $(grep 'role="doc"' package.xml | sed -e 's/^.*name="//;s/".*$//')
do install -Dpm 644 NTS/$i %{buildroot}%{pecl_docdir}/%{pecl_name}/$i
done


%check
: Minimal load test for NTS extension
%{__php} --no-php-ini \
    --define extension=%{buildroot}%{php_extdir}/%{pecl_name}.so \
    --modules | grep %{pecl_name}

%if %{with_zts}
: Minimal load test for ZTS extension
%{__ztsphp} --no-php-ini \
    --define extension=%{buildroot}%{php_ztsextdir}/%{pecl_name}.so \
    --modules | grep %{pecl_name}
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
%defattr(-,root,root,-)
%doc %{pecl_docdir}/%{pecl_name}
%doc %{pecl_testdir}/%{pecl_name}
%config(noreplace) %{php_inidir}/%{pecl_name}.ini
%{php_extdir}/%{pecl_name}.so
%{pecl_xmldir}/%{name}.xml
%if %{with_zts}
%{php_ztsextdir}/%{pecl_name}.so
%config(noreplace) %{php_ztsinidir}/%{pecl_name}.ini
%endif


%changelog
* Mon Mar  3 2014 Remi Collet <remi@fedoraproject.org> - 1.1.2-2
- cleanups
- install documentation in pecl_docdir
- install tests in pecl_testdir

* Thu Aug 29 2013 Remi Collet <remi@fedoraproject.org> - 1.1.2-1
- update to 1.1.2

* Mon Aug 19 2013 Remi Collet <remi@fedoraproject.org> - 1.1.1-1
- single spec for 0.8.x / 1.0.x / 1.1.x
- update to 1.1.1, requires libgearman >= 1.1.0

* Fri Nov 30 2012 Remi Collet <remi@fedoraproject.org> - 1.0.3-1.1
- also provides php-gearman

* Sun Aug 05 2012 Remi Collet <remi@fedoraproject.org> - 1.0.3-1
- update to 1.0.3
- add missing provides php-pecl(gearman)

* Sun Aug 05 2012 Remi Collet <remi@fedoraproject.org> - 0.8.3-1
- update to 0.8.3
- add missing provides php-pecl(gearman)

* Sat May 05 2012 Remi Collet <remi@fedoraproject.org> - 1.0.2-3
- add BR libgearman-1.0 + libgearman-1.0-devel
  Workaround for https://bugzilla.redhat.com/819209

* Tue Mar 06 2012 Remi Collet <remi@fedoraproject.org> - 1.0.2-2
- update to 1.0.2 for PHP 5.4

* Tue Mar 06 2012 Remi Collet <remi@fedoraproject.org> - 1.0.2-1
- update to 1.0.2 for PHP 5.3
- spec clean up

* Fri Dec 09 2011 Remi Collet <remi@fedoraproject.org> - 1.0.1-2
- update to 1.0.1, build against php 5.4

* Fri Dec 09 2011 Remi Collet <remi@fedoraproject.org> - 1.0.1-1
- update to 1.0.1

* Fri Dec 09 2011 Remi Collet <remi@fedoraproject.org> - 0.8.1-2
- update to 0.8.1, build against php 5.4

* Fri Dec 09 2011 Remi Collet <remi@fedoraproject.org> - 0.8.1-1
- update to 0.8.1

* Mon Dec 05 2011 Remi Collet <remi@fedoraproject.org> - 1.0.0-2
- build against php 5.4

* Mon Dec 05 2011 Remi Collet <remi@fedoraproject.org> - 1.0.0-1
- update to 1.0.0
- raise dependency to libgearman 0.21 (si f16 only)

* Mon Nov 14 2011 Remi Collet <remi@fedoraproject.org> - 0.8.0-2
- build against php 5.4

* Sat Oct 15 2011 Remi Collet <Fedora@FamilleCollet.com> - 0.8.0-1
- update to 0.8.0
- ZTS extension
- spec cleanup and minimal %%check
- fix requires

* Fri Aug 12 2011 Jesse Keating <jkeating@redhat.com> - 0.7.0-5
- Rebuild for broken deps

* Mon Apr 11 2011 Paul Whalen <paul.whalen@senecac.on.ca> 0.7.0-4
- fix setup and package.xml install

* Mon Apr 11 2011 Paul Whalen <paul.whalen@senecac.on.ca> 0.7.0-3
- correct macros, add license to files

* Fri Apr 08 2011 Paul Whalen <paul.whalen@senecac.on.ca> 0.7.0-2
- correct package following pecl packaging guidelines

* Fri Mar 11 2011 Paul Whalen <paul.whalen@senecac.on.ca> 0.7.0-1
- Initial Packaging

