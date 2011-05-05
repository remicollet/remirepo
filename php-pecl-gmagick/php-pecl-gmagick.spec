%global	php_apiver  %((echo 0; php -i 2>/dev/null | sed -n 's/^PHP API => //p') | tail -1)
%{!?__pecl: %{expand: %%global __pecl	%{_bindir}/pecl}}
%{!?php_extdir: %{expand: %%global php_extdir	%(php-config --extension-dir)}}

%global	pecl_name	gmagick
%global prever 		b2

Summary:	Provides a wrapper to the GraphicsMagick library
Name:		php-pecl-%{pecl_name}
Version:	1.0.8
Release:	0.4.%{prever}%{?dist}
License:	PHP
Group:		Development/Libraries
URL:		http://pecl.php.net/package/gmagick
Source0:	http://pecl.php.net/get/gmagick-%{version}%{?prever}.tgz


BuildRoot:	%{_tmppath}/%{name}-%{version}-root-%(%{__id_u} -n)
BuildRequires:	php-pear >= 1.4.7
BuildRequires: 	php-devel >= 5.1.3, GraphicsMagick-devel >= 1.2.6

Requires(post):	%{__pecl}
Requires(postun): %{__pecl}
%if %{?php_zend_api:1}0
Requires:	php(zend-abi) = %{php_zend_api}
Requires:	php(api) = %{php_core_api}
%else
Requires:	php-api = %{php_apiver}
%endif
Provides:	php-pecl(%{pecl_name}) = %{version}%{?prever}

Conflicts:	php-pecl-imagick
Conflicts:	php-magickwand


%description
%{pecl_name} is a php extension to create, modify and obtain meta information of
images using the GraphicsMagick API.


%prep
%setup -qc
cd %{pecl_name}-%{version}%{?prever}

chmod 0644 README

# Check to avoid See : http://pecl.php.net/bugs/18002
grep '"%{version}%{?prever}"' php_gmagick.h || exit1


%build
cd %{pecl_name}-%{version}%{?prever}
phpize
%{configure} --with-%{pecl_name}
make %{?_smp_mflags}


%install
rm -rf %{buildroot}

cd %{pecl_name}-%{version}%{?prever}

make install \
	INSTALL_ROOT=%{buildroot}

# Install XML package description
install -m 0755 -d %{buildroot}%{pecl_xmldir}
install -m 0664 ../package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml
install -d %{buildroot}%{_sysconfdir}/php.d/
%{__cat} > %{buildroot}%{_sysconfdir}/php.d/%{pecl_name}.ini << 'EOF'
; Enable %{pecl_name} extension module
extension=%{pecl_name}.so
EOF


%clean
rm -rf %{buildroot}


%post
%if 0%{?pecl_install:1}
%{pecl_install} %{pecl_xmldir}/%{name}.xml  >/dev/null || :
%endif


%postun
%if 0%{?pecl_uninstall:1}
if [ "$1" -eq "0" ]; then
	%{pecl_uninstall} %{pecl_name} >/dev/null || :
fi
%endif

%check
cd %{pecl_name}-%{version}%{?prever}

# simple module load test
php --no-php-ini \
    --define extension_dir=modules \
    --define extension=%{pecl_name}.so \
    --modules | grep %{pecl_name}


%files
%defattr(-,root,root,-)
%doc %{pecl_name}-%{version}%{?prever}/{README,LICENSE}
%config(noreplace) %{_sysconfdir}/php.d/%{pecl_name}.ini
%{_libdir}/php/modules/%{pecl_name}.so
%{pecl_xmldir}/%{name}.xml


%changelog
* Thu May 05 2011 Remi Collet <rpms@famillecollet.com> 1.0.8-0.4.b2
- Update to 1.0.8b2

* Sat Apr 16 2011 Remi Collet <rpms@famillecollet.com> 1.0.8-0.3.b1
- fix build against latest php

* Sun Oct 17 2010 Remi Collet <rpms@famillecollet.com> 1.0.8-0.2.b1
- F-14 build + add Conflicts php-magickwand

* Mon Sep 13 2010 Remi Collet <rpms@famillecollet.com> 1.0.8-0.1.b1
- Update to 1.0.8b1 for remi repo

* Sun Aug 08 2010 Remi Collet <rpms@famillecollet.com> 1.0.7-0.1.b1
- Update to 1.0.7b1 for remi repo
- remove patch for http://pecl.php.net/bugs/17991
- add fix for http://pecl.php.net/bugs/18002

* Sat Aug 07 2010 Remi Collet <rpms@famillecollet.com> 1.0.6-0.1.b1
- Update to 1.0.6b1 for remi repo
- add patch for http://pecl.php.net/bugs/17991

* Mon Jul 26 2010 Remi Collet <rpms@famillecollet.com> 1.0.5-0.1.b1
- Update to 1.0.5b1 for remi repo

* Mon Jul 26 2010 Pavel Alexeev <Pahan@Hubbitus.info> - 1.0.5b1-5
- Update to 1.0.5b1
- Add Conflicts: php-pecl-imagick - BZ#559675

* Sun Jan 31 2010 Pavel Alexeev <Pahan@Hubbitus.info> - 1.0.3b3-4
- Update to 1.0.3b3

* Fri Jan 29 2010 Remi Collet <rpms@famillecollet.com> 1.0.3-0.1.b3
- update to 1.0.3b3

* Tue Nov 3 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 1.0.2b1-3
- Fedora Review started, thanks to Andrew Colin Kissa.
- Remove macros %%{__make} in favour to plain make.
- Add %%{?_smp_mflags} to make.

* Mon Oct 12 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 1.0.2b1-2
- New version 1.0.2b1 - author include license text by my request. Thank you Vito Chin.
- Include LICENSE.

* Fri Oct 2 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 1.0.1b1-1
- Initial release.
- License text absent, but I ask Vito Chin by email to add it into tarball.
