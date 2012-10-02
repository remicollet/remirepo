%{!?__pecl:     %{expand: %%global __pecl     %{_bindir}/pecl}}
%{!?php_extdir: %{expand: %%global php_extdir %(php-config --extension-dir)}}

%global pecl_name oauth

Name:           php-pecl-oauth
Version:        1.2.3
Release:        1%{?dist}
Summary:        PHP OAuth consumer extension
Group:          Development/Languages
License:        BSD
URL:            http://pecl.php.net/package/oauth
Source0:        http://pecl.php.net/get/%{pecl_name}-%{version}.tgz

BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildRequires:  php-devel
BuildRequires:  php-pear
# curl instead of libcurl for old release
BuildRequires:  curl-devel

Requires:       php(zend-abi) = %{php_zend_api}
Requires:       php(api) = %{php_core_api}
Requires(post): %{__pecl}
Requires(postun): %{__pecl}

Provides: php-pecl(%{pecl_name}) = %{version}

# Other third party repo stuff
Obsoletes:     php53-pecl-oauth
Obsoletes:     php53u-pecl-oauth
%if "%{php_version}" > "5.4"
Obsoletes:     php54-pecl-oauth
%endif

# Filter private shared
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}


%description
OAuth is an authorization protocol built on top of HTTP which allows 
applications to securely access data without having to store
user names and passwords.

%prep
%setup -q -c

cp -r %{pecl_name}-%{version} %{pecl_name}-%{version}-zts

cat >%{pecl_name}.ini << 'EOF'
; Enable %{pecl_name} extension module
extension=%{pecl_name}.so
EOF


%build
cd %{pecl_name}-%{version}
%{_bindir}/phpize
%configure --with-php-config=%{_bindir}/php-config
make %{?_smp_mflags}

cd ../%{pecl_name}-%{version}-zts
%{_bindir}/zts-phpize
%configure --with-php-config=%{_bindir}/zts-php-config
make %{?_smp_mflags}


%install
rm -rf %{buildroot}

make install -C %{pecl_name}-%{version}     INSTALL_ROOT=%{buildroot}
make install -C %{pecl_name}-%{version}-zts INSTALL_ROOT=%{buildroot}

# Drop in the bit of configuration
install -D -m 644 %{pecl_name}.ini %{buildroot}%{php_inidir}/%{pecl_name}.ini
install -D -m 644 %{pecl_name}.ini %{buildroot}%{php_ztsinidir}/%{pecl_name}.ini

# Install XML package description
install -D -m 644 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml


%clean
rm -rf %{buildroot}


%post
%{pecl_install} %{pecl_xmldir}/%{name}.xml >/dev/null || :


%postun
if [ $1 -eq 0 ]; then
%{pecl_uninstall} %{pecl_name} >/dev/null || :
fi


%check
%{__php} -n \
    -d extension_dir=%{pecl_name}-%{version}/modules \
    -d extension=%{pecl_name}.so \
    --modules | grep OAuth

%{__ztsphp} -n \
    -d extension_dir=%{pecl_name}-%{version}-zts/modules \
    -d extension=%{pecl_name}.so \
    --modules | grep OAuth


%files
%defattr(-,root,root,-)
%doc %{pecl_name}-%{version}/LICENSE %{pecl_name}-%{version}/examples
%config(noreplace) %{php_inidir}/%{pecl_name}.ini
%config(noreplace) %{php_ztsinidir}/%{pecl_name}.ini
%{php_extdir}/%{pecl_name}.so
%{php_ztsextdir}/%{pecl_name}.so
%{pecl_xmldir}/%{name}.xml


%changelog
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
