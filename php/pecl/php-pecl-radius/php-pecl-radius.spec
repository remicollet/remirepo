%{!?__pecl:     %{expand: %%global __pecl     %{_bindir}/pecl}}

%global pecl_name radius

Name:           php-pecl-radius
Version:        1.2.5
Release:        14%{?dist}
Summary:        Radius client library

License:        BSD
Group:          Development/Languages
URL:            http://pecl.php.net/package/radius
Source0:        http://pecl.php.net/get/radius-%{version}.tgz

# http://svn.php.net/viewvc/pecl/radius/trunk/radius.c?r1=256497&r2=297236&sortby=date
Patch0:         radius-php54.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  php-devel
BuildRequires:  php-pear

Requires(post): %{__pecl}
Requires(postun): %{__pecl}
Requires:       php(zend-abi) = %{php_zend_api}
Requires:       php(api) = %{php_core_api}

Provides:       php-%{pecl_name} = %{version}
Provides:       php-%{pecl_name}%{?_isa} = %{version}
Provides:       php-pecl(%{pecl_name}) = %{version}
Provides:       php-pecl(%{pecl_name})%{?_isa} = %{version}

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
This package is based on the libradius of FreeBSD, with some modifications
and extensions.  This PECL provides full support for RADIUS authentication
(RFC 2865) and RADIUS accounting (RFC 2866), works on Unix and on Windows.
Its an easy way to authenticate your users against the user-database of your
OS (for example against Windows Active-Directory via IAS).


%prep
%setup -qc

cd %{pecl_name}-%{version}
%patch0 -p3 -b .php54
cd ..

cat > %{pecl_name}.ini << 'EOF'
; Enable %{pecl_name} extension module
extension=%{pecl_name}.so
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
install -Dpm644 %{pecl_name}.ini %{buildroot}%{php_inidir}/%{pecl_name}.ini
install -Dpm644 %{pecl_name}.ini %{buildroot}%{php_ztsinidir}/%{pecl_name}.ini


%check
# simple module load test
%{__php} --no-php-ini \
    --define extension_dir=%{pecl_name}-%{version}/modules \
    --define extension=%{pecl_name}.so \
    --modules | grep %{pecl_name}

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
%doc %{pecl_name}-%{version}/{CREDITS,examples}
%config(noreplace) %{php_inidir}/%{pecl_name}.ini
%config(noreplace) %{php_ztsinidir}/%{pecl_name}.ini
%{php_extdir}/%{pecl_name}.so
%{php_ztsextdir}/%{pecl_name}.so
%{pecl_xmldir}/%{name}.xml


%changelog
* Fri Nov 18 2011 Remi Collet <rpms@famillecollet.com> 1.2.5-14
- also provides php-radius

* Fri Nov 18 2011 Remi Collet <rpms@famillecollet.com> 1.2.5-12
- php 5.4 build

* Thu Oct 06 2011 Remi Collet <rpms@famillecollet.com> 1.2.5-11
- ZTS extension
- spec cleanups

* Wed Jul  6 2011  Remi Collet <Fedora@FamilleCollet.com> - 1.2.5-11
- fix php_zend_api usage, fix FTBFS #715846

* Sat Oct 23 2010  Remi Collet <Fedora@FamilleCollet.com> - 1.2.5-10
- add filter_provides to avoid private-shared-object-provides ncurses.so

* Sat Aug 28 2010 Remi Collet <Fedora@FamilleCollet.com> - 1.2.5-9
- clean define
- use more macros
- add simple load test in %%check

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.5-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Jul 12 2009 Remi Collet <Fedora@FamilleCollet.com> - 1.2.5-7
- rebuild for new PHP 5.3.0 ABI (20090626)

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Apr 19 2008 Christopher Stone <chris.stone@gmail.com> 1.2.5-5
- Fix Requires for post/postun sections (bz #442699)

* Fri Feb 22 2008 Christopher Stone <chris.stone@gmail.com> 1.2.5-4
- Properly register package

* Wed Feb 20 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.2.5-3
- Autorebuild for GCC 4.3

* Sun Sep 30 2007 Christopher Stone <chris.stone@gmail.com> 1.2.5-2
- Update to new standards

* Sat Sep 08 2007 Christopher Stone <chris.stone@gmail.com> 1.2.5-1
- Upstream sync

* Sun Mar 11 2007 Christopher Stone <chris.stone@gmail.com> 1.2.4-2
- Use new ABI check for FC-6
- Create directory to untar sources
- Remove %%{release} from Provides

* Sat Jul 01 2006 Christopher Stone <chris.stone@gmail.com> 1.2.4-1
- Initial release
