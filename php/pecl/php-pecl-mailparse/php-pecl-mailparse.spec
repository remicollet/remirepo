%{!?php_inidir:  %global php_inidir   %{_sysconfdir}/php.d}
%{!?__pecl:      %global __pecl       %{_bindir}/pecl}
%{!?__php:       %global __php        %{_bindir}/php}

%global pecl_name mailparse
%global with_zts  0%{?__ztsphp:1}

Summary:   PHP PECL package for parsing and working with email messages
Name:      php-pecl-mailparse
Version:   2.1.6
Release:   5%{?dist}%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}
License:   PHP
Group:     Development/Languages
URL:       http://pecl.php.net/package/mailparse
Source0:   http://pecl.php.net/get/mailparse-%{version}.tgz

# https://bugs.php.net/65861 - Please Provides LICENSE file
# URL from mailparse.c header
Source1:   http://www.php.net/license/2_02.txt

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: php-devel, php-pear
# mbstring need for tests
BuildRequires: php-mbstring
# Required by phpize
BuildRequires: autoconf, automake, libtool

Requires: php-mbstring%{?_isa}
Requires: php(zend-abi) = %{php_zend_api}
Requires: php(api) = %{php_core_api}
Requires(post): %{__pecl}
Requires(postun): %{__pecl}

Provides: php-%{pecl_name} = %{version}
Provides: php-%{pecl_name}%{?_isa} = %{version}
Provides: php-pecl(%{pecl_name}) = %{version}
Provides: php-pecl(%{pecl_name})%{?_isa} = %{version}

%if "%{?vendor}" == "Remi Collet"
%if "%{php_version}" > "5.4"
# Other third party repo stuff
Obsoletes:     php53-pecl-%{pecl_name}
Obsoletes:     php53u-pecl-%{pecl_name}
Obsoletes:     php54-pecl-%{pecl_name}
%endif
%if "%{php_version}" > "5.5"
Obsoletes:     php55u-pecl-%{pecl_name}
%endif
%if "%{php_version}" > "5.6"
Obsoletes:     php56u-pecl-%{pecl_name}
%endif
%endif

%if 0%{?fedora} < 20
# Filter shared private
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}
%endif


%description
Mailparse is an extension for parsing and working with email messages.
It can deal with rfc822 and rfc2045 (MIME) compliant messages.


%prep
%setup -q -c

mv %{pecl_name}-%{version} NTS

cd NTS
cp %{SOURCE1} LICENSE
extver=$(sed -n '/#define PHP_MAILPARSE_VERSION/{s/.* "//;s/".*$//;p}' php_mailparse.h)
if test "x${extver}" != "x%{version}"; then
   : Error: Upstream version is ${extver}, expecting %{version}.
   exit 1
fi
cd ..

cat > %{pecl_name}.ini << 'EOF'
; Enable mailparse extension module
extension = mailparse.so

; Set the default charset
;mailparse.def_charset = us-ascii
EOF

chmod -x NTS/*.{php,c,h}

%if %{with_zts}
cp -pr NTS ZTS
%endif


%build
cd NTS
phpize
%configure --with-php-config=%{_bindir}/php-config
make %{?_smp_mflags}

%if %{with_zts}
cd ../ZTS
zts-phpize
%configure --with-php-config=%{_bindir}/zts-php-config
make %{?_smp_mflags}
%endif


%install
rm -rf %{buildroot}
make -C NTS install INSTALL_ROOT=%{buildroot}
# Drop in the bit of configuration
install -Dpm 644 %{pecl_name}.ini %{buildroot}%{php_inidir}/z-%{pecl_name}.ini

%if %{with_zts}
make -C ZTS install INSTALL_ROOT=%{buildroot}
# Drop in the bit of configuration
install -Dpm 644 %{pecl_name}.ini %{buildroot}%{php_ztsinidir}/z-%{pecl_name}.ini
%endif

# Install XML package description
install -Dpm 644 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml

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
    --define extension=mbstring.so \
    --define extension=%{buildroot}%{php_extdir}/%{pecl_name}.so \
    --modules | grep %{pecl_name}

: Upstream test suite for NTS extension
cd NTS
TEST_PHP_EXECUTABLE=%{__php} \
NO_INTERACTION=1 \
%{__php} run-tests.php \
    -n -q \
    -d extension=mbstring.so \
    -d extension=$PWD/modules/%{pecl_name}.so

%if %{with_zts}
: Minimal load test for ZTS extension
%{__ztsphp} --no-php-ini \
    --define extension=mbstring.so \
    --define extension=%{buildroot}%{php_ztsextdir}/%{pecl_name}.so \
    --modules | grep %{pecl_name}

: Upstream test suite for ZTS extension
cd ../ZTS
TEST_PHP_EXECUTABLE=%{__ztsphp} \
NO_INTERACTION=1 \
php run-tests.php \
    -n -q \
    -d extension=mbstring.so \
    -d extension=$PWD/modules/%{pecl_name}.so
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
# We prefix the config file with "z-" so that it loads after mbstring.ini
%config(noreplace) %{php_inidir}/z-%{pecl_name}.ini
%{php_extdir}/%{pecl_name}.so
%{pecl_xmldir}/%{name}.xml

%if %{with_zts}
%config(noreplace) %{php_ztsinidir}/z-%{pecl_name}.ini
%{php_ztsextdir}/%{pecl_name}.so
%endif


%changelog
* Sun Feb  2 2014 Remi Collet <remi@fedoraproject.org> - 2.1.6-5
- cleanups
- install documentation in pecl_docdir
- install tests in pecl_testdir
- add missing License file

* Fri Nov 30 2012 Remi Collet <remi@fedoraproject.org> - 2.1.6-3.1
- also provides php-mailparse

* Sun Oct 21 2012 Remi Collet <remi@fedoraproject.org> - 2.1.6-3
- rebuild

* Sat Mar 10 2012 Remi Collet <remi@fedoraproject.org> - 2.1.6-2
- rebuild for PHP 5.4

* Sat Mar 10 2012 Remi Collet <remi@fedoraproject.org> - 2.1.6-1
- update to 2.1.6
- enable ZTS build

* Thu Jan 19 2012 Remi Collet <remi@fedoraproject.org> - 2.1.5-6
- rebuild against PHP 5.4, with patch
- fix filters

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Oct 23 2010  Remi Collet <Fedora@FamilleCollet.com> 2.1.5-3
- add filter_provides to avoid private-shared-object-provides mailparse.so
- spec cleanup

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Jul 12 2009  Remi Collet <Fedora@FamilleCollet.com> 2.1.5-1
- update to 2.1.5 (bugfix + php 5.3.0 compatibility)

* Mon Apr 14 2008  Remi Collet <Fedora@FamilleCollet.com> 2.1.4-1
- update to 2.1.4 (bugfix)
- package2.xml is now provided

* Sun Feb 24 2008  Remi Collet <Fedora@FamilleCollet.com> 2.1.3-1
- update to 2.1.3
- add post(un) scriplet
- add check

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.1.1-9
- Autorebuild for GCC 4.3

* Wed Aug 22 2007 Matthias Saou <http://freshrpms.net/> 2.1.1-8
- Rebuild for new BuildID feature.

* Mon Aug  6 2007 Matthias Saou <http://freshrpms.net/> 2.1.1-7
- Update License field.
- Remove dist tag, since the package will seldom change.

* Tue Jun 19 2007 Matthias Saou <http://freshrpms.net/> 2.1.1-6
- Fix package requirements by adding build-time zend-abi version.
- Clean up spec to conform to current PHP packaging rules.
- No longer bundle part of mbstring (mbfl), at last! (makes spec F7+ specific)

* Mon Aug 28 2006 Matthias Saou <http://freshrpms.net/> 2.1.1-5
- FC6 rebuild.
- Add php-api requirement and php-pecl(mailparse) provides.

* Mon Mar  6 2006 Matthias Saou <http://freshrpms.net/> 2.1.1-4
- Add missing php-mbstring requirement (#197410).

* Mon Mar  6 2006 Matthias Saou <http://freshrpms.net/> 2.1.1-3
- FC5 rebuild.

* Thu Feb  9 2006 Matthias Saou <http://freshrpms.net/> 2.1.1-2
- Rebuild for new gcc/glibc and FC5's PHP 5.1.

* Wed Jul 20 2005 Matthias Saou <http://freshrpms.net/> 2.1.1-1
- Update to 2.1.1.
- Update mbfl tarball to 4.4.0 PHP sources.
- Rename .ini file to "z-<name>" to have it load after mbstring.so.

* Thu Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Wed Feb 16 2005 Matthias Saou <http://freshrpms.net/> 2.1-1
- Update to 2.1.

* Thu Jan 13 2005 Matthias Saou <http://freshrpms.net/> 2.0b-5
- Bump release.

* Tue Jul 27 2004 Matthias Saou <http://freshrpms.net/> 2.0b-4
- Update included mbfl source to 4.3.8 as the current 4.3.4 doesn't work
  anymore.

* Fri May 21 2004 Matthias Saou <http://freshrpms.net/> 2.0b-3
- Rebuild for Fedora Core 2.
- No need for a strict dependency on this package, it works fine with
  php 4.3.6 when compiled against 4.3.4.

* Fri May  7 2004 Matthias Saou <http://freshrpms.net/> 2.0b-2
- Added php.d entry to auto-load the module with recent php packages.
- Added more macros to the spec file.

* Mon Apr 26 2004 Matthias Saou <http://freshrpms.net/> 2.0b-1
- Initial RPM release.
- Included part of php-4.3.4's mbfl includes, ugly.

