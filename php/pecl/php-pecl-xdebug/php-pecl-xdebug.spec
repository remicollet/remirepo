# remirepo spec file for php-pecl-xdebug
# with SCL compatibility, from:
#
# Fedora spec file for php-pecl-xdebug
#
# Copyright (c) 2010-2016 Remi Collet
# Copyright (c) 2006-2009 Christopher Stone
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please, preserve the changelog entries
#

%{?scl:          %scl_package         php-pecl-xdebug}
%{!?php_inidir:  %global php_inidir   %{_sysconfdir}/php.d}
%{!?__pecl:      %global __pecl       %{_bindir}/pecl}
%{!?__php:       %global __php        %{_bindir}/php}

%global pecl_name   xdebug
%global with_zts    0%{?__ztsphp:1}
%global gh_commit   2d2bdbc7948aa72143df0c5fc0eb684078732bf9
%global gh_short    %(c=%{gh_commit}; echo ${c:0:7})
%global with_tests  0%{?_with_tests:1}

# XDebug should be loaded after opcache
%if "%{php_version}" < "5.6"
%global ini_name  %{pecl_name}.ini
%else
%global ini_name  15-%{pecl_name}.ini
%endif

Name:           %{?scl_prefix}php-pecl-xdebug
Summary:        PECL package for debugging PHP scripts
Version:        2.3.3
Release:        1%{?dist}%{!?scl:%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}}
Source0:        https://github.com/%{pecl_name}/%{pecl_name}/archive/%{gh_commit}/%{pecl_name}-%{version}-%{gh_short}.tar.gz

# The Xdebug License, version 1.01
# (Based on "The PHP License", version 3.0)
License:        PHP
Group:          Development/Languages
URL:            http://xdebug.org/

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  %{?scl_prefix}php-pear  > 1.9.1
BuildRequires:  %{?scl_prefix}php-devel > 5.4
BuildRequires:  libedit-devel
BuildRequires:  libtool
%if %{with_tests}
BuildRequires:  php-soap
%endif

Requires:       %{?scl_prefix}php(zend-abi) = %{php_zend_api}
Requires:       %{?scl_prefix}php(api) = %{php_core_api}
%{?_sclreq:Requires: %{?scl_prefix}runtime%{?_sclreq}%{?_isa}}

Provides:       %{?scl_prefix}php-%{pecl_name} = %{version}
Provides:       %{?scl_prefix}php-%{pecl_name}%{?_isa} = %{version}
Provides:       %{?scl_prefix}php-pecl(Xdebug) = %{version}
Provides:       %{?scl_prefix}php-pecl(Xdebug)%{?_isa} = %{version}

%if "%{?vendor}" == "Remi Collet" && 0%{!?scl:1}
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
# Filter private shared
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}
%endif


%description
The Xdebug extension helps you debugging your script by providing a lot of
valuable debug information. The debug information that Xdebug can provide
includes the following:

* stack and function traces in error messages with:
  o full parameter display for user defined functions
  o function name, file name and line indications
  o support for member functions
* memory allocation
* protection for infinite recursions

Xdebug also provides:

* profiling information for PHP scripts
* code coverage analysis
* capabilities to debug your scripts interactively with a debug client

Package built for PHP %(%{__php} -r 'echo PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')%{?scl: as Software Collection (%{scl} by %{?scl_vendor}%{!?scl_vendor:rh})}.


%prep
%setup -qc
mv %{pecl_name}-%{gh_commit} NTS
mv NTS/package.xml .

cd NTS

# Check extension version
ver=$(sed -n '/XDEBUG_VERSION/{s/.* "//;s/".*$//;p}' php_xdebug.h)
if test "$ver" != "%{version}%{?prever}"; then
   : Error: Upstream XDEBUG_VERSION version is ${ver}, expecting %{version}%{?prever}.
   exit 1
fi

cd ..

%if %{with_zts}
# Duplicate source tree for NTS / ZTS build
cp -pr NTS ZTS
%endif


%build
cd NTS
%{_bindir}/phpize
%configure \
    --enable-xdebug  \
    --with-php-config=%{_bindir}/php-config
make %{?_smp_mflags}

# Build debugclient
pushd debugclient
# buildconf required for aarch64 support
./buildconf
%configure --with-libedit
make %{?_smp_mflags}
popd

%if %{with_zts}
cd ../ZTS
%{_bindir}/zts-phpize
%configure \
    --enable-xdebug  \
    --with-php-config=%{_bindir}/zts-php-config
make %{?_smp_mflags}
%endif


%install
rm -rf %{buildroot}

# install NTS extension
make -C NTS install INSTALL_ROOT=%{buildroot}

# install debugclient
install -Dpm 755 NTS/debugclient/debugclient \
        %{buildroot}%{_bindir}/debugclient

# install package registration file
install -Dpm 644 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml

# install config file
install -d %{buildroot}%{php_inidir}
cat << 'EOF' | tee %{buildroot}%{php_inidir}/%{ini_name}
; Enable xdebug extension module
%if "%{php_version}" > "5.5"
zend_extension=%{pecl_name}.so
%else
zend_extension=%{php_extdir}/%{pecl_name}.so
%endif

; see http://xdebug.org/docs/all_settings
EOF

%if %{with_zts}
# Install ZTS extension
make -C ZTS install INSTALL_ROOT=%{buildroot}

install -d %{buildroot}%{php_ztsinidir}
cat << 'EOF' | tee %{buildroot}%{php_ztsinidir}/%{ini_name}
; Enable xdebug extension module
%if "%{php_version}" > "5.5"
zend_extension=%{pecl_name}.so
%else
zend_extension=%{php_ztsextdir}/%{pecl_name}.so
%endif

; see http://xdebug.org/docs/all_settings
EOF
%endif

# Documentation
for i in $(grep 'role="doc"' package.xml | sed -e 's/^.*name="//;s/".*$//')
do
  [ -f NTS/contrib/$i ] && j=contrib/$i || j=$i
  install -Dpm 644 NTS/$j %{buildroot}%{pecl_docdir}/%{pecl_name}/$j
done


%check
# only check if build extension can be loaded
%{_bindir}/php \
    --no-php-ini \
    --define zend_extension=%{buildroot}%{php_extdir}/%{pecl_name}.so \
    --modules | grep Xdebug

%if %{with_zts}
%{_bindir}/zts-php \
    --no-php-ini \
    --define zend_extension=%{buildroot}%{php_ztsextdir}/%{pecl_name}.so \
    --modules | grep Xdebug
%endif

%if %{with_tests}
cd NTS
# ignore kwown failed tests
rm tests/bug00623.phpt
rm tests/bug00687.phpt
rm tests/bug00778.phpt
rm tests/bug00806.phpt
rm tests/bug00840.phpt
rm tests/bug00886.phpt
rm tests/bug00913.phpt
rm tests/bug01059.phpt
rm tests/bug01104.phpt
rm tests/dbgp-context-get.phpt
rm tests/dbgp-property-get-constants.phpt

: Upstream test suite NTS extension
TEST_PHP_EXECUTABLE=%{_bindir}/php \
TEST_PHP_ARGS="-n -d extension=soap.so -d zend_extension=$PWD/modules/%{pecl_name}.so" \
NO_INTERACTION=1 \
REPORT_EXIT_STATUS=1 \
%{__php} -n run-tests.php --show-diff
%else
: Test suite disabled
%endif


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


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{?_licensedir:%license NTS/LICENSE}
%doc %{pecl_docdir}/%{pecl_name}
%{_bindir}/debugclient
%{pecl_xmldir}/%{name}.xml

%config(noreplace) %{php_inidir}/%{ini_name}
%{php_extdir}/%{pecl_name}.so

%if %{with_zts}
%config(noreplace) %{php_ztsinidir}/%{ini_name}
%{php_ztsextdir}/%{pecl_name}.so
%endif


%changelog
* Fri Jun 19 2015 Remi Collet <remi@fedoraproject.org> - 2.3.3-1
- update to 2.3.3
- drop all patches, merged upstream

* Fri May 29 2015 Remi Collet <remi@fedoraproject.org> - 2.3.2-5
- sources from github, with test suite
- run test suite when build using "--with tests" option
- add upstream patch to fix crash when another extension calls
  call_user_function() during RINIT (e.g. phk)

* Fri May 29 2015 Remi Collet <remi@fedoraproject.org> - 2.3.2-4
- add patch for exception code change (for phpunit)

* Wed May 27 2015 Remi Collet <remi@fedoraproject.org> - 2.3.2-3
- add patch for efree/str_efree in php 5.6

* Wed Apr 22 2015 Remi Collet <remi@fedoraproject.org> - 2.3.2-2
- add patch for virtual_file_ex in 5.6 #1214111

* Sun Mar 22 2015 Remi Collet <remi@fedoraproject.org> - 2.3.2-1
- Update to 2.3.2

* Wed Feb 25 2015 Remi Collet <remi@fedoraproject.org> - 2.3.1-1
- Update to 2.3.1

* Mon Feb 23 2015 Remi Collet <remi@fedoraproject.org> - 2.3.0-1
- Update to 2.3.0
- raise minimum php version to 5.4

* Fri Jan 23 2015 Remi Collet <remi@fedoraproject.org> - 2.2.7-2
- fix %%postun scriplet

* Thu Jan 22 2015 Remi Collet <remi@fedoraproject.org> - 2.2.7-1
- Update to 2.2.7
- drop runtime dependency on pear, new scriptlets

* Wed Dec 24 2014 Remi Collet <remi@fedoraproject.org> - 2.2.6-3.1
- Fedora 21 SCL mass rebuild

* Wed Dec  3 2014 Remi Collet <remi@fedoraproject.org> - 2.2.6-3
- more upstream patch

* Wed Dec  3 2014 Remi Collet <remi@fedoraproject.org> - 2.2.6-2
- add upstream patch for couchbase compatibility
  see http://bugs.xdebug.org/view.php?id=1087

* Sun Nov 16 2014 Remi Collet <remi@fedoraproject.org> - 2.2.6-1
- Update to 2.2.6 (stable)

* Mon Aug 25 2014 Remi Collet <rcollet@redhat.com> - 2.2.5-2
- improve SCL build

* Wed Apr 30 2014 Remi Collet <remi@fedoraproject.org> - 2.2.5-1
- Update to 2.2.5 (stable)

* Wed Apr  9 2014 Remi Collet <remi@fedoraproject.org> - 2.2.4-3
- add numerical prefix to extension configuration file
- drop uneeded full extension path

* Wed Mar 19 2014 Remi Collet <rcollet@redhat.com> - 2.2.4-2
- allow SCL build

* Sun Mar 02 2014 Remi Collet <remi@fedoraproject.org> - 2.2.4-1
- Update to 2.2.4 (stable)
- move documentation in pecl_docdir

* Wed May 22 2013 Remi Collet <remi@fedoraproject.org> - 2.2.3-1
- Update to 2.2.3

* Sun Mar 24 2013 Remi Collet <remi@fedoraproject.org> - 2.2.2-1
- update to 2.2.2 (stable)

* Mon Mar 18 2013 Remi Collet <remi@fedoraproject.org> - 2.2.2-0.5.gitb1ce1e3
- new snapshot

* Fri Jan 18 2013 Remi Collet <remi@fedoraproject.org> - 2.2.2-0.4.gitb44a72a
- new snapshot
- drop our patch, merged upstream

* Thu Jan  3 2013 Remi Collet <remi@fedoraproject.org> - 2.2.2-0.3.gite1b9127
- new snapshot
- add patch, see https://github.com/xdebug/xdebug/pull/51

* Fri Nov 30 2012 Remi Collet <remi@fedoraproject.org> - 2.2.2-0.2.gite773b090fc
- rebuild with new php 5.5 snaphost with zend_execute_ex

* Fri Nov 30 2012 Remi Collet <remi@fedoraproject.org> - 2.2.2-0.1.gite773b090fc
- update to git snapshot for php 5.5
- also provides php-xdebug

* Sun Sep  9 2012 Remi Collet <remi@fedoraproject.org> - 2.2.1-2
- sync with rawhide, cleanups
- obsoletes php53*, php54*

* Tue Jul 17 2012 Remi Collet <remi@fedoraproject.org> - 2.2.1-1
- Update to 2.2.1

* Fri Jun 22 2012 Remi Collet <remi@fedoraproject.org> - 2.2.0-2
- upstream patch for upstream bug #838/#839/#840

* Wed May 09 2012 Remi Collet <remi@fedoraproject.org> - 2.2.0-1
- Update to 2.2.0

* Sat Apr 28 2012 Remi Collet <remi@fedoraproject.org> - 2.2.0-0.7.RC2
- Update to 2.2.0RC2

* Wed Mar 14 2012 Remi Collet <remi@fedoraproject.org> - 2.2.0-0.6.RC1
- Update to 2.2.0RC1

* Sun Mar 11 2012 Remi Collet <remi@fedoraproject.org> - 2.2.0-0.5.git8d9993b
- new git snapshot

* Sat Jan 28 2012 Remi Collet <remi@fedoraproject.org> - 2.2.0-0.4.git7e971c4
- new git snapshot
- fix version reported by pecl list

* Fri Jan 20 2012 Remi Collet <remi@fedoraproject.org> - 2.2.0-0.3.git758d962
- new git snapshot

* Sun Dec 11 2011 Remi Collet <remi@fedoraproject.org> - 2.2.0-0.2.gitd076740
- new git snapshot

* Sun Nov 13 2011 Remi Collet <remi@fedoraproject.org> - 2.2.0-0.1.git535df90
- update to 2.2.0-dev, build against php 5.4

* Tue Oct 04 2011 Remi Collet <Fedora@FamilleCollet.com> - 2.1.2-2
- ZTS extension
- spec cleanups

* Thu Jul 28 2011 Remi Collet <Fedora@FamilleCollet.com> - 2.1.2-1
- update to 2.1.2
- fix provides filter for rpm 4.9
- improved description

* Wed Mar 30 2011 Remi Collet <RPMS@FamilleCollet.com> - 2.1.1-1
- allow relocation

* Wed Mar 30 2011 Remi Collet <Fedora@FamilleCollet.com> - 2.1.1-1
- update to 2.1.1
- patch reported version

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Oct 23 2010 Remi Collet <Fedora@FamilleCollet.com> - 2.1.0-2
- add filter_provides to avoid private-shared-object-provides xdebug.so
- add %%check section (minimal load test)
- always use libedit

* Tue Jun 29 2010 Remi Collet <Fedora@FamilleCollet.com> - 2.1.0-1
- update to 2.1.0

* Mon Sep 14 2009 Christopher Stone <chris.stone@gmail.com> 2.0.5-1
- Upstream sync

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Jul 12 2009 Remi Collet <Fedora@FamilleCollet.com> - 2.0.4-1
- update to 2.0.4 (bugfix + Basic PHP 5.3 support)

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Oct 09 2008 Christopher Stone <chris.stone@gmail.com> 2.0.3-4
- Add code coverage patch (bz #460348)
- http://bugs.xdebug.org/bug_view_page.php?bug_id=0000344

* Thu Oct 09 2008 Christopher Stone <chris.stone@gmail.com> 2.0.3-3
- Revert last change

* Thu Oct 09 2008 Christopher Stone <chris.stone@gmail.com> 2.0.3-2
- Add php-xml to Requires (bz #464758)

* Thu May 22 2008 Christopher Stone <chris.stone@gmail.com> 2.0.3-1
- Upstream sync
- Clean up libedit usage
- Minor rpmlint fix

* Sun Mar 02 2008 Christopher Stone <chris.stone@gmail.com> 2.0.2-4
- Add %%{__pecl} to post/postun Requires

* Fri Feb 22 2008 Christopher Stone <chris.stone@gmail.com> 2.0.2-3
- %%define %%pecl_name to properly register package
- Install xml package description
- Add debugclient
- Many thanks to Edward Rudd (eddie@omegaware.com) (bz #432681)

* Wed Feb 20 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.0.2-2
- Autorebuild for GCC 4.3

* Sun Nov 25 2007 Christopher Stone <chris.stone@gmail.com> 2.0.2-1
- Upstream sync

* Sun Sep 30 2007 Christopher Stone <chris.stone@gmail.com> 2.0.0-2
- Update to latest standards
- Fix encoding on Changelog

* Sat Sep 08 2007 Christopher Stone <chris.stone@gmail.com> 2.0.0-1
- Upstream sync
- Remove %%{?beta} tags

* Sun Mar 11 2007 Christopher Stone <chris.stone@gmail.com> 2.0.0-0.5.RC2
- Create directory to untar sources
- Use new ABI check for FC6
- Remove %%{release} from Provides

* Mon Jan 29 2007 Christopher Stone <chris.stone@gmail.com> 2.0.0-0.4.RC2
- Compile with $RPM_OPT_FLAGS
- Use %{buildroot} instead of %%{buildroot}
- Fix license tag

* Mon Jan 15 2007 Christopher Stone <chris.stone@gmail.com> 2.0.0-0.3.RC2
- Upstream sync

* Sun Oct 29 2006 Christopher Stone <chris.stone@gmail.com> 2.0.0-0.2.RC1
- Upstream sync

* Wed Sep 06 2006 Christopher Stone <chris.stone@gmail.com> 2.0.0-0.1.beta6
- Remove Provides php-xdebug
- Fix Release
- Remove prior changelog due to Release number change
