%{!?php_inidir:  %global php_inidir   %{_sysconfdir}/php.d}
%{!?__pecl:      %global __pecl       %{_bindir}/pecl}
%{!?__php:       %global __php        %{_bindir}/php}

%global pecl_name   oauth
%global with_zts    0%{?__ztsphp:1}

Name:           php-pecl-oauth
Version:        1.2.3
Release:        4%{?dist}%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}
Summary:        PHP OAuth consumer extension
Group:          Development/Languages
License:        BSD
URL:            http://pecl.php.net/package/oauth
Source0:        http://pecl.php.net/get/%{pecl_name}-%{version}.tgz

BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildRequires:  php-devel
BuildRequires:  php-pear
BuildRequires:  pcre-devel
# curl instead of libcurl for old release
BuildRequires:  curl-devel

Requires:       php(zend-abi) = %{php_zend_api}
Requires:       php(api) = %{php_core_api}
Requires(post): %{__pecl}
Requires(postun): %{__pecl}

Provides:       php-%{pecl_name} = %{version}
Provides:       php-%{pecl_name}%{?_isa} = %{version}
Provides:       php-pecl(%{pecl_name}) = %{version}
Provides:       php-pecl(%{pecl_name})%{?_isa} = %{version}

%if "%{?vendor}" == "Remi Collet"
# Other third party repo stuff
%if "%{php_version}" > "5.4"
# Other third party repo stuff
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
OAuth is an authorization protocol built on top of HTTP which allows 
applications to securely access data without having to store
user names and passwords.

%prep
%setup -q -c

mv %{pecl_name}-%{version} NTS

# Sanity check, really often broken
extver=$(sed -n '/#define PHP_OAUTH_VERSION/{s/.* //;s/".*$//;p}' NTS/php_oauth.h)
if test "x${extver}" != "x%{version}"; then
   : Error: Upstream extension version is ${extver}, expecting %{version}.
   exit 1
fi

cat >%{pecl_name}.ini << 'EOF'
; Enable %{pecl_name} extension module
extension=%{pecl_name}.so
EOF

%if %{with_zts}
# duplicate for ZTS build
cp -pr NTS ZTS
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
cd NTS
for i in $(grep 'role="doc"' ../package.xml | sed -e 's/^.*name="//;s/".*$//')
do install -Dpm 644 $i %{buildroot}%{pecl_docdir}/%{pecl_name}/$i
done


%clean
rm -rf %{buildroot}


%post
%{pecl_install} %{pecl_xmldir}/%{name}.xml >/dev/null || :


%postun
if [ $1 -eq 0 ]; then
%{pecl_uninstall} %{pecl_name} >/dev/null || :
fi


%check
: Minimal load test for NTS extension
%{__php} -n \
    -d extension=%{buildroot}%{php_extdir}/%{pecl_name}.so \
    --modules | grep OAuth

%if %{with_zts}
: Minimal load test for ZTS extension
%{__ztsphp} -n \
    -d extension=%{buildroot}%{php_ztsextdir}/%{pecl_name}.so \
    --modules | grep OAuth
%endif


%files
%defattr(-,root,root,-)
%doc %{pecl_docdir}/%{pecl_name}
%config(noreplace) %{php_inidir}/%{pecl_name}.ini
%{php_extdir}/%{pecl_name}.so
%{pecl_xmldir}/%{name}.xml

%if %{with_zts}
%config(noreplace) %{php_ztsinidir}/%{pecl_name}.ini
%{php_ztsextdir}/%{pecl_name}.so
%endif


%changelog
* Wed Mar 12 2014 Remi Collet <remi@fedoraproject.org> - 1.2.3-4
- cleanups
- move doc in pecl_docdir

* Fri Nov 30 2012 Remi Collet <remi@fedoraproject.org> - 1.2.3-1.1
- also provides php-oauth

* Tue Oct  2 2012 Remi Collet <remi@fedoraproject.org> - 1.2.3-1
- update to 1.2.3

* Tue Sep  4 2012 Remi Collet <remi@fedoraproject.org> - 1.2.2-4
- EL rebuild

* Sun Nov 13 2011 Remi Collet <remi@fedoraproject.org> - 1.2.2-3
- build against php 5.4

* Tue Oct 04 2011 Remi Collet <RPMS@FamilleCollet.com> - 1.2.2-2
- ZTS extension

* Fri Jul 22 2011 Remi Collet <RPMS@FamilleCollet.com> - 1.2.2-1
- update to 1.2.2

* Fri Jul 22 2011 Remi Collet <RPMS@FamilleCollet.com> - 1.2.1-1
- rebuild for remi repo

* Fri Jul 22 2011 F. Kooman <fkooman@tuxed.net> - 1.2.1-1
- update to 1.2.1 (RHBZ #724872). See
  http://pecl.php.net/package-changelog.php?package=oauth&release=1.2.1

* Mon Jul 04 2011 Remi Collet <RPMS@FamilleCollet.com> - 1.2-1
- rebuild for remi repo

* Sun Jul 03 2011 F. Kooman <fkooman@tuxed.net> - 1.2-1
- upgrade to 1.2

* Sat Jun 25 2011 Remi Collet <RPMS@FamilleCollet.com> - 1.1.0-6
- rebuild for remi repo

* Sun Jun 19 2011 F. Kooman <fkooman@tuxed.net> - 1.1.0-6
- add fix for http://pecl.php.net/bugs/bug.php?id=22337

* Wed Jun 14 2011 Remi Collet <RPMS@FamilleCollet.com> - 1.1.0-5
- rebuild for remi repo

* Mon Jun 13 2011 F. Kooman <fkooman@tuxed.net> - 1.1.0-5
- remove php_apiver marco, was not used

* Mon Jun 13 2011 F. Kooman <fkooman@tuxed.net> - 1.1.0-4
- add minimal check to see if module loads
- fix private-shared-object-provides rpmlint warning

* Sat Jun 11 2011 F. Kooman - 1.1.0-3
- BR pcre-devel

* Sat May 28 2011 F. Kooman - 1.1.0-2
- require libcurl for cURL request engine support 

* Sat May 28 2011 F. Kooman - 1.1.0-1
- initial package 
