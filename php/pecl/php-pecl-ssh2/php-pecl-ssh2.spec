%{!?__pecl:     %{expand: %%global __pecl     %{_bindir}/pecl}}

%global pecl_name ssh2

Name:           php-pecl-ssh2
Version:        0.12
Release:        1%{?dist}
Summary:        Bindings for the libssh2 library

# http://pecl.php.net/bugs/bug.php?id=24364
License:        PHP
Group:          Development/Languages
URL:            http://pecl.php.net/package/ssh2
Source0:        http://pecl.php.net/get/ssh2-%{version}.tgz
Source2:        php-pecl-ssh2-0.10-README

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  libssh2-devel >= 1.2
BuildRequires:  php-devel
BuildRequires:  php-pear

Requires(post): %{__pecl}
Requires(postun): %{__pecl}
Provides:       php-pecl(%{pecl_name}) = %{version}
Provides:       php-pecl(%{pecl_name})%{?_isa} = %{version}
Requires:       php(zend-abi) = %{php_zend_api}
Requires:       php(api) = %{php_core_api}

# Other third party repo stuff
Obsoletes:     php53-pecl-%{pecl_name}
Obsoletes:     php53u-pecl-%{pecl_name}
%if "%{php_version}" > "5.4"
Obsoletes:     php54-pecl-%{pecl_name}
%endif

# Filter private shared
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}


%description
Bindings to the libssh2 library which provide access to resources
(shell, remote exec, tunneling, file transfer) on a remote machine using
a secure cryptographic transport.

Documentation : http://php.net/ssh2


%prep
%setup -c -q 

extver=$(sed -n '/#define PHP_SSH2_VERSION/{s/.* "//;s/".*$//;p}' %{pecl_name}-%{version}/php_ssh2.h)
if test "x${extver}" != "x%{version}"; then
   : Error: Upstream PDO ABI version is now ${extver}, expecting %{version}.
   : Update the pdover macro and rebuild.
   exit 1
fi

cp %{SOURCE2} README

cat > ssh2.ini << 'EOF'
; Enable ssh2 extension module
extension=ssh2.so
EOF

cp -pr %{pecl_name}-%{version} %{pecl_name}-%{version}-zts


%build
cd %{pecl_name}-%{version}
%{_bindir}/phpize
%configure  --with-php-config=%{_bindir}/php-config
make %{?_smp_mflags}

cd ../%{pecl_name}-%{version}-zts
%{_bindir}/zts-phpize
%configure  --with-php-config=%{_bindir}/zts-php-config
make %{?_smp_mflags}


%install
rm -rf %{buildroot}

make -C %{pecl_name}-%{version} \
     install INSTALL_ROOT=%{buildroot}

make -C %{pecl_name}-%{version}-zts \
     install INSTALL_ROOT=%{buildroot}

# Install XML package description
install -Dpm 644 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml

# install config file
install -Dpm644 ssh2.ini %{buildroot}%{php_inidir}/ssh2.ini
install -Dpm644 ssh2.ini %{buildroot}%{php_ztsinidir}/ssh2.ini


%check
# Minimal load test for NTS extension
%{__php} --no-php-ini \
    --define extension_dir=%{pecl_name}-%{version}/modules \
    --define extension=%{pecl_name}.so \
    --modules | grep %{pecl_name}

# Minimal load test for ZTS extension
%{__ztsphp} --no-php-ini \
    --define extension_dir=%{pecl_name}-%{version}-zts/modules \
    --define extension=%{pecl_name}.so \
    --modules | grep %{pecl_name}


%post
%{pecl_install} %{pecl_xmldir}/%{name}.xml >/dev/null || :


%postun
if [ $1 -eq 0 ] ; then
    %{pecl_uninstall} %{pecl_name} >/dev/null || :
fi


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc README
%config(noreplace) %{php_inidir}/ssh2.ini
%config(noreplace) %{php_ztsinidir}/ssh2.ini
%{php_extdir}/ssh2.so
%{php_ztsextdir}/ssh2.so
%{pecl_xmldir}/%{name}.xml


%changelog
* Thu Oct 18 2012 Remi Collet <RPMS@FamilleCollet.com> - 0.12-1
- update to 0.12
- raise dependency on libssh2 >= 1.2

* Sun Nov 13 2011 Remi Collet <remi@fedoraproject.org> - 0.11.3-2
- build against php 5.4

* Sat Oct 04 2011 Remi Collet <RPMS@FamilleCollet.com> - 0.11.3-1
- update to 0.11.3
- zts extension

* Tue Aug 16 2011 Remi Collet <RPMS@FamilleCollet.com> - 0.11.2-1.1
- EL-5 rebuild for libssh2
- add filter

* Sat Apr 16 2011 Remi Collet <RPMS@FamilleCollet.com> - 0.11.2-1
- update to 0.11.2
- add minimal %%check

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan 14 2010 Chris Weyl <cweyl@alumni.drew.edu> 0.11.0-6
- bump for libssh2 rebuild


* Mon Sep 21 2009 Chris Weyl <cweyl@alumni.drew.edu> - 0.11.0-5
- rebuild for libssh2 1.2

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Jul 12 2009 Remi Collet <Fedora@FamilleCollet.com> - 0.11.0-3
- add ssh2-php53.patch
- rebuild for new PHP 5.3.0 ABI (20090626)

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Dec 20 2008 Itamar Reis Peixoto <itamar@ispbrasil.com.br> 0.11.0-1
- convert package.xml to V2 format, update to 0.11.0 #BZ 476405

* Sat Nov 15 2008 Itamar Reis Peixoto <itamar@ispbrasil.com.br> 0.10-2
- Install pecl xml, license and readme files

* Wed Jul 16 2008 Itamar Reis Peixoto <itamar@ispbrasil.com.br> 0.10-1
- Initial release
