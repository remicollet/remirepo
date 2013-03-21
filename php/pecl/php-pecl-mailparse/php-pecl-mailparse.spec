%{!?__pecl:     %{expand: %%global __pecl     %{_bindir}/pecl}}

%global pecl_name mailparse

Summary:   PHP PECL package for parsing and working with email messages
Name:      php-pecl-mailparse
Version:   2.1.6
Release:   3%{?dist}.5
License:   PHP
Group:     Development/Languages
URL:       http://pecl.php.net/package/mailparse
Source0:   http://pecl.php.net/get/mailparse-%{version}.tgz


BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: php-devel, php-pear
# mbstring need for tests
BuildRequires: php-mbstring
# Required by phpize
BuildRequires: autoconf, automake, libtool

Requires: php-mbstring
Requires: php(zend-abi) = %{php_zend_api}
Requires: php(api) = %{php_core_api}
Requires(post): %{__pecl}
Requires(postun): %{__pecl}

Provides: php-%{pecl_name} = %{version}
Provides: php-%{pecl_name}%{?_isa} = %{version}
Provides: php-pecl(%{pecl_name}) = %{version}
Provides: php-pecl(%{pecl_name})%{?_isa} = %{version}

# Other third party repo stuff
Obsoletes:     php53-pecl-%{pecl_name}
Obsoletes:     php53u-pecl-%{pecl_name}
%if "%{php_version}" > "5.4"
Obsoletes:     php54-pecl-%{pecl_name}
%endif
%if "%{php_version}" > "5.5"
Obsoletes:     php55-pecl-%{pecl_name}
%endif

# Filter private shared
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}


%description
Mailparse is an extension for parsing and working with email messages.
It can deal with rfc822 and rfc2045 (MIME) compliant messages.


%prep
# We need to create our working directory since the package*.xml files from
# the sources extract straight to it
%setup -q -c

extver=$(sed -n '/#define PHP_MAILPARSE_VERSION/{s/.* "//;s/".*$//;p}' %{pecl_name}-%{version}/php_mailparse.h)
if test "x${extver}" != "x%{version}"; then
   : Error: Upstream version is ${extver}, expecting %{version}.
   exit 1
fi

cat > %{pecl_name}.ini << 'EOF'
; Enable mailparse extension module
extension = mailparse.so

; Set the default charset
;mailparse.def_charset = us-ascii
EOF

chmod -x %{pecl_name}-%{version}/*.{php,c,h}

%if 0%{?__ztsphp:1}
cp -pr %{pecl_name}-%{version} %{pecl_name}-%{version}-zts
%endif


%build
cd %{pecl_name}-%{version}
phpize
%configure --with-php-config=%{_bindir}/php-config
make %{?_smp_mflags}

%if 0%{?__ztsphp:1}
cd ../%{pecl_name}-%{version}-zts
zts-phpize
%configure --with-php-config=%{_bindir}/zts-php-config
make %{?_smp_mflags}
%endif


%install
rm -rf %{buildroot}
make -C %{pecl_name}-%{version} \
     install INSTALL_ROOT=%{buildroot}
# Drop in the bit of configuration
install -Dpm 644 %{pecl_name}.ini %{buildroot}%{_sysconfdir}/php.d/z-%{pecl_name}.ini

%if 0%{?__ztsphp:1}
make -C %{pecl_name}-%{version}-zts \
     install INSTALL_ROOT=%{buildroot}
# Drop in the bit of configuration
install -Dpm 644 %{pecl_name}.ini %{buildroot}%{php_ztsinidir}/z-%{pecl_name}.ini
%endif

# Install XML package description
install -Dpm 644 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml


%check
cd %{pecl_name}-%{version}
ln -s %{php_extdir}/mbstring.so modules

TEST_PHP_EXECUTABLE=$(which php) \
NO_INTERACTION=1 \
php run-tests.php \
    -n -q -d extension_dir=modules \
    -d extension=mbstring.so \
    -d extension=%{pecl_name}.so \

%if 0%{?__ztsphp:1}
cd ../%{pecl_name}-%{version}-zts
ln -s %{php_ztsextdir}/mbstring.so modules

TEST_PHP_EXECUTABLE=%{__ztsphp} \
NO_INTERACTION=1 \
php run-tests.php \
    -n -q -d extension_dir=modules \
    -d extension=mbstring.so \
    -d extension=%{pecl_name}.so \
%endif


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
%defattr(-,root,root,-)
%doc %{pecl_name}-%{version}/{README,CREDITS,try.php}
# We prefix the config file with "z-" so that it loads after mbstring.ini
%config(noreplace) %{_sysconfdir}/php.d/z-mailparse.ini
%{php_extdir}/mailparse.so
%{pecl_xmldir}/%{name}.xml

%if 0%{?__ztsphp:1}
%config(noreplace) %{php_ztsinidir}/z-mailparse.ini
%{php_ztsextdir}/mailparse.so
%endif

%changelog
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

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
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

