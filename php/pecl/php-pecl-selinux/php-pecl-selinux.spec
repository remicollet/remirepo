# PECL(PHP Extension Community Library) related definitions
%{!?__pecl:     %{expand: %%global __pecl     %{_bindir}/pecl}}
%define pecl_name selinux

Summary: SELinux binding for PHP scripting language
Name: php-pecl-selinux
Version: 0.3.1
Release: 7%{?dist}.1
License: PHP
Group: Development/Languages
URL: http://pecl.php.net/package/%{pecl_name}
Source: http://pecl.php.net/get/%{pecl_name}-%{version}.tgz

BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildRequires: php-devel >= 5.2.0, php-pear, libselinux-devel >= 2.0.80
Requires: php >= 5.2.0, libselinux >= 2.0.80

Requires(post): %{__pecl}
Requires(postun): %{__pecl}
Requires: php(zend-abi) = %{php_zend_api}
Requires: php(api) = %{php_core_api}
Provides: php-pecl(%{pecl_name}) = %{version}-%{release}

# RPM 4.8
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}
# RPM 4.9
%global __provides_exclude_from %{?__provides_exclude_from:%__provides_exclude_from|}%{_dir}/.*\\.so$


%description
This package is an extension to the PHP Hypertext Preprocessor.
It wraps the libselinux library and provides a set of interfaces
to the PHP runtime engine.
The libselinux is a set of application program interfaces towards in-kernel
SELinux, contains get/set security context, communicate security server,
translate between raw and readable format and so on.

%prep
%setup -c -q

cp -pr %{pecl_name}-%{version} %{pecl_name}-zts 
(echo "; Enable SELinux extension module"
 echo "extension=%{pecl_name}.so") > %{pecl_name}.ini
 

%build
cd %{pecl_name}-%{version}
%{_bindir}/phpize
%configure \
    --with-php-config=%{_bindir}/php-config
make %{?_smp_mflags}

cd ../%{pecl_name}-zts
%{_bindir}/zts-phpize
%configure \
    --with-php-config=%{_bindir}/zts-php-config
make %{?_smp_mflags}


%install
rm -rf %{buildroot}
install -D -p -m 0755 %{pecl_name}-%{version}/modules/%{pecl_name}.so \
        %{buildroot}%{php_extdir}/%{pecl_name}.so
install -D -p -m 0755 %{pecl_name}-zts/modules/%{pecl_name}.so \
        %{buildroot}%{php_ztsextdir}/%{pecl_name}.so

# Drop in the bit of configuration
install -D -m 644 %{pecl_name}.ini %{buildroot}%{php_inidir}/%{pecl_name}.ini
install -D -m 644 %{pecl_name}.ini %{buildroot}%{php_ztsinidir}/%{pecl_name}.ini

# Install XML package description
install -D -m 644 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml


%check
# simple module load test
%{__php} --no-php-ini \
    --define extension_dir=%{pecl_name}-%{version}/modules \
    --define extension=%{pecl_name}.so \
    --modules | grep %{pecl_name}

%{__ztsphp} --no-php-ini \
    --define extension_dir=%{pecl_name}-zts/modules \
    --define extension=%{pecl_name}.so \
    --modules | grep %{pecl_name}


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
%doc %{pecl_name}-%{version}/{LICENSE,README}
%config(noreplace) %{php_inidir}/%{pecl_name}.ini
%config(noreplace) %{php_ztsinidir}/%{pecl_name}.ini
%{php_extdir}/%{pecl_name}.so
%{php_ztsextdir}/%{pecl_name}.so
%{pecl_xmldir}/%{name}.xml


%changelog
* Mon Dec 12 2011 Remi Collet <RPMS@FamilleCollet.com> - 0.3.1-7.1
- bump release (f16 rebuild)

* Sun Nov 27 2011 Remi Collet <RPMS@FamilleCollet.com> - 0.3.1-7
- php 5.4 and ZTS build

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Mar  3 2010 KaiGai Kohei <kaigai@kaigai.gr.jp> - 0.3.1-5
- Rebuilt for package 

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jul 13 2009 Remi Collet <Fedora@FamilleCollet.com> - 0.3.1-2
- rebuild for new PHP 5.3.0 ABI (20090626)

* Thu Apr 16 2009 KaiGai Kohei <kaigai@kaigai.gr.jp> - 0.3.1-1
- The "permissive" tag was added to selinux_compute_av
- The selinux_deny_unknown() was added
- README is updated for the new features

* Thu Mar 12 2009 KaiGai Kohei <kaigai@kaigai.gr.jp> - 0.2.1-1
- Specfile to build RPM package is added.

* Thu Mar  5 2009 KaiGai Kohei <kaigai@kaigai.gr.jp> - 0.1.2-1
- The initial release of SELinux binding for PHP script language.
