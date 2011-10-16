%{!?__pecl:     %{expand: %%global __pecl     %{_bindir}/pecl}}

%global pecl_name mailparse

Summary:   PHP PECL package for parsing and working with email messages
Name:      php-pecl-mailparse
Version:   2.1.5
Release:   4%{?dist}
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
Provides: php-pecl(%{pecl_name}) = %{version}-%{release}

# RPM 4.8
%{?filter_provides_in: %filter_provides_in %{php_extdir}/.*\.so$}
%{?filter_provides_in: %filter_provides_in %{php_ztsextdir}/.*\.so$}
%{?filter_setup}
# RPM 4.9
%global __provides_exclude_from %{?__provides_exclude_from:%__provides_exclude_from|}%{php_extdir}/.*\\.so$
%global __provides_exclude_from %__provides_exclude_from|%{php_ztsextdir}/.*\\.so$


%description
Mailparse is an extension for parsing and working with email messages.
It can deal with rfc822 and rfc2045 (MIME) compliant messages.


%prep
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
rm -rf %{buildroot}

make -C %{pecl_name}-%{version} \
     install INSTALL_ROOT=%{buildroot}

make -C %{pecl_name}-%{version}-zts \
     install INSTALL_ROOT=%{buildroot}

# Install XML package description
install -Dpm 644 package2.xml %{buildroot}%{pecl_xmldir}/%{name}.xml

# install config file
install -Dpm644 %{pecl_name}.ini %{buildroot}%{php_inidir}/z-%{pecl_name}.ini
install -Dpm644 %{pecl_name}.ini %{buildroot}%{php_ztsinidir}/z-%{pecl_name}.ini


%check
cd %{pecl_name}-%{version}
ln -s %{php_extdir}/mbstring.so modules

TEST_PHP_EXECUTABLE=%{__php} \
REPORT_EXIT_STATUS=1 \
NO_INTERACTION=1 \
%{__php} run-tests.php \
    -n -q -d extension_dir=modules \
    -d extension=mbstring.so \
    -d extension=%{pecl_name}.so \


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
%doc %{pecl_name}-%{version}/{README,CREDITS,try.php}
# We prefix the config file with "z-" so that it loads after mbstring.ini
%config(noreplace) %{php_inidir}/z-%{pecl_name}.ini
%config(noreplace) %{php_ztsinidir}/z-%{pecl_name}.ini
%{php_extdir}/%{pecl_name}.so
%{php_ztsextdir}/%{pecl_name}.so
%{pecl_xmldir}/%{name}.xml


%changelog
* Sun Oct 16 2011 Remi Collet <Fedora@FamilleCollet.com> - 2.1.5-4
- ZTS extension
- spec cleanups

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

