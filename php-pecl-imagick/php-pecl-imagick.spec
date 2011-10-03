%{!?__pecl:  %{expand: %%global __pecl %{_bindir}/pecl}}
%{!?phpname: %{expand: %%global phpname php}}

%global pecl_name imagick

Summary:       Extension to create and modify images using ImageMagick
Name:          %{phpname}-pecl-imagick
Version:       3.0.1
Release:       3%{?dist}.1
License:       PHP
Group:         Development/Languages
URL:           http://pecl.php.net/package/imagick
Source:        http://pecl.php.net/get/imagick-%{version}.tgz


BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: %{phpname}-devel >= 5.1.3, %{phpname}-pear
%if 0%{?fedora} >= 14 || 0%{?rhel} >= 7
BuildRequires: ImageMagick-devel >= 6.6.0
%else
BuildRequires: ImageMagick2-devel >= 6.6.0
%endif
Requires(post): %{__pecl}
Requires(postun): %{__pecl}
Provides:      %{phpname}-pecl(%{pecl_name}) = %{version}

Conflicts:     %{phpname}-pecl-gmagick

Requires:       %{phpname}(zend-abi) = %{php_zend_api}
Requires:       %{phpname}(api) = %{php_core_api}


# RPM 4.8
%{?filter_provides_in: %filter_provides_in %{php_extdir}/.*\.so$}
%{?filter_provides_in: %filter_provides_in %{php_ztsextdir}/.*\.so$}
%{?filter_setup}
# RPM 4.9
%global __provides_exclude_from %{?__provides_exclude_from:%__provides_exclude_from|}%{php_extdir}/.*\\.so$
%global __provides_exclude_from %__provides_exclude_from|%{php_ztsextdir}/.*\\.so$


%description
Imagick is a native php extension to create and modify images
using the ImageMagick API.


%prep
echo TARGET is %{name}-%{version}-%{release}
%setup -q -c 

cat > %{pecl_name}.ini << 'EOF'
; Enable %{pecl_name} extension module
extension = %{pecl_name}.so

; Options not documented
;imagick.locale_fix=0
;imagick.progress_monitor=0
EOF

cp -r %{pecl_name}-%{version} %{pecl_name}-%{version}-zts


%build
cd %{pecl_name}-%{version}-zts
# ZTS build
%{php_ztsbindir}/phpize
%configure --with-imagick=%{prefix} --with-php-config=%{php_ztsbindir}/php-config
make %{?_smp_mflags}

# Standard build
cd ../%{pecl_name}-%{version}
%{php_bindir}/phpize
%configure --with-imagick=%{prefix} --with-php-config=%{php_bindir}/php-config
make %{?_smp_mflags}


%install
rm -rf %{buildroot}

make install INSTALL_ROOT=%{buildroot} -C %{pecl_name}-%{version}-zts
make install INSTALL_ROOT=%{buildroot} -C %{pecl_name}-%{version}

# Drop in the bit of configuration
install -D -m 644 %{pecl_name}.ini %{buildroot}%{php_ztsinidir}/%{pecl_name}.ini
install -D -m 644 %{pecl_name}.ini %{buildroot}%{php_inidir}/%{pecl_name}.ini

# Install XML package description
mkdir -p %{buildroot}%{pecl_xmldir}
install -pm 644 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml


%post
%{pecl_install} %{pecl_xmldir}/%{name}.xml >/dev/null || :


%postun
if [ $1 -eq 0 ] ; then
    %{pecl_uninstall} %{pecl_name} >/dev/null || :
fi


%check
# simple module load test
pushd %{pecl_name}-%{version}
%{__php} --no-php-ini \
    --define extension_dir=modules \
    --define extension=%{pecl_name}.so \
    --modules | grep %{pecl_name}


%clean
rm -rf %{buildroot}


%files
%defattr(-, root, root, 0755)
%doc %{pecl_name}-%{version}/{CREDITS,ChangeLog,examples}
%config(noreplace) %{php_inidir}/%{pecl_name}.ini
%config(noreplace) %{php_ztsinidir}/%{pecl_name}.ini
%{php_extdir}/%{pecl_name}.so
%{php_ztsextdir}/%{pecl_name}.so
%{pecl_xmldir}/%{name}.xml
%{php_incldir}/ext/%{pecl_name}
%{php_ztsincldir}/ext/%{pecl_name}


%changelog
* Mon Oct 03 2011 Remi Collet <Fedora@FamilleCollet.com> - 3.0.1-3.1
- spec cleanup

* Tue Aug 24 2011 Remi Collet <Fedora@FamilleCollet.com> - 3.0.1-3
- build zts extension

* Sun Dec 27 2010 Remi Collet <rpms@famillecollet.com> 3.0.1-2
- relocate using phpname macro

* Fri Nov 26 2010 Remi Collet <rpms@famillecollet.com> 3.0.1-1.1
- rebuild against latest ImageMagick 6.6.5.10

* Thu Nov 25 2010 Remi Collet <rpms@famillecollet.com> 3.0.1-1
- update to 3.0.1

* Mon Jul 26 2010 Remi Collet <rpms@famillecollet.com> 3.0.0-1
- update to 3.0.0

* Wed Aug 26 2009 Remi Collet <rpms@famillecollet.com> 2.3.0-2
- build against ImageMagick2 6.5.x

* Mon Aug 24 2009 Remi Collet <rpms@famillecollet.com> 2.3.0-1
- update to 2.3.0

* Wed Jun 30 2009 Remi Collet <rpms@famillecollet.com> 2.2.2-3.###.remi
- rebuild for PHP 5.3.0 (API = 20090626)

* Thu Apr 25 2009 Remi Collet <rpms@famillecollet.com> 2.2.2-2.fc11.remi
- F11 rebuild for PHP 5.3.0RC1

* Wed Feb 25 2009 Remi Collet <rpms@famillecollet.com> 2.2.2-1.fc10.remi
- update to 2.2.2 for php 5.3.0beta1

* Thu Jan 29 2009 Remi Collet <rpms@famillecollet.com> 2.2.1-1.fc10.remi.2
- rebuild for php 5.3.0beta1

* Sat Dec 13 2008 Remi Collet <rpms@famillecollet.com> 2.2.1-1.fc#.remi.1
- rebuild with php 5.3.0-dev
- add imagick-2.2.1-php53.patch

* Sat Dec 13 2008 Remi Collet <rpms@famillecollet.com> 2.2.1-1
- update to 2.2.1

* Sat Jul 19 2008 Remi Collet <rpms@famillecollet.com> 2.2.0-1.fc9.remi.1
- rebuild with php 5.3.0-dev

* Sat Jul 19 2008 Remi Collet <rpms@famillecollet.com> 2.2.0-1
- update to 2.2.0

* Thu Apr 24 2008 Remi Collet <rpms@famillecollet.com> 2.1.1-1
- Initial package

