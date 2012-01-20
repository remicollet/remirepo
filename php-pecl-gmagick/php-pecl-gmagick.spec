%{!?__pecl: %{expand: %%global __pecl %{_bindir}/pecl}}

%global pecl_name  gmagick
%global prever     RC2

Summary:        Provides a wrapper to the GraphicsMagick library
Name:           php-pecl-%{pecl_name}
Version:        1.1.0
Release:        0.2.%{prever}%{?dist}
License:        PHP
Group:          Development/Libraries
URL:            http://pecl.php.net/package/gmagick
Source0:        http://pecl.php.net/get/gmagick-%{version}%{?prever}.tgz

BuildRoot:      %{_tmppath}/%{name}-%{version}-root-%(%{__id_u} -n)
BuildRequires:  php-pear >= 1.4.7
BuildRequires:  php-devel >= 5.1.3, GraphicsMagick-devel >= 1.2.6

Requires(post): %{__pecl}
Requires(postun): %{__pecl}
Requires:       php(zend-abi) = %{php_zend_api}
Requires:       php(api) = %{php_core_api}

Provides:       php-pecl(%{pecl_name}) = %{version}%{?prever}

Conflicts:      php-pecl-imagick
Conflicts:      php-magickwand


# RPM 4.8
%{?filter_provides_in: %filter_provides_in %{php_extdir}/.*\.so$}
%{?filter_provides_in: %filter_provides_in %{php_ztsextdir}/.*\.so$}
%{?filter_setup}
# RPM 4.9
%global __provides_exclude_from %{?__provides_exclude_from:%__provides_exclude_from|}%{php_extdir}/.*\\.so$
%global __provides_exclude_from %__provides_exclude_from|%{php_ztsextdir}/.*\\.so$


%description
%{pecl_name} is a php extension to create, modify and obtain meta information
of images using the GraphicsMagick API.


%prep
%setup -qc

# Create configuration file
cat >%{pecl_name}.ini << 'EOF'
; Enable %{pecl_name} extension module
extension=%{pecl_name}.so
EOF

# Check extension version
extver=$(sed -n '/#define PHP_GMAGICK_VERSION/{s/.* "//;s/".*$//;p}' %{pecl_name}-%{version}%{?prever}/php_gmagick.h)
if test "x${extver}" != "x%{version}%{?prever}"; then
   : Error: Upstream extension version is ${extver}, expecting %{version}%{?prever}.
   exit 1
fi

# Duplicate build tree for nts/zts
cp -r %{pecl_name}-%{version}%{?prever} %{pecl_name}-zts


%build
cd %{pecl_name}-%{version}%{?prever}
%{php_bindir}/phpize
%{configure} --with-%{pecl_name}  --with-php-config=%{php_bindir}/php-config
make %{?_smp_mflags}

cd ../%{pecl_name}-zts
%{php_ztsbindir}/phpize
%{configure} --with-%{pecl_name}  --with-php-config=%{php_ztsbindir}/php-config
make %{?_smp_mflags}


%install
rm -rf %{buildroot}

make -C %{pecl_name}-%{version}%{?prever} \
     install INSTALL_ROOT=%{buildroot}

make -C %{pecl_name}-zts \
     install INSTALL_ROOT=%{buildroot}

# Install XML package description
install -D -m 664 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml

# Drop in the bit of configuration
install -D -m 664 %{pecl_name}.ini %{buildroot}%{php_inidir}/%{pecl_name}.ini
install -D -m 664 %{pecl_name}.ini %{buildroot}%{php_ztsinidir}/%{pecl_name}.ini


%clean
rm -rf %{buildroot}


%post
%{pecl_install} %{pecl_xmldir}/%{name}.xml  >/dev/null || :


%postun
if [ "$1" -eq "0" ]; then
   %{pecl_uninstall} %{pecl_name} >/dev/null || :
fi

%check
cd %{pecl_name}-%{version}%{?prever}

# simple module load test
%{__php} --no-php-ini \
    --define extension_dir=modules \
    --define extension=%{pecl_name}.so \
    --modules | grep %{pecl_name}

# Remove know to fail tests (font issue)
rm -f tests/gmagick-006-annotateimage.phpt

# Still ignore test result as some fail on old version
TEST_PHP_EXECUTABLE=%{__php} \
REPORT_EXIT_STATUS=0 \
NO_INTERACTION=1 \
%{__php} run-tests.php \
    -n -q \
    -d extension_dir=modules \
    -d extension=%{pecl_name}.so

cd ../%{pecl_name}-zts

if [ -f %{php_ztsbindir}/php ]; then
# simple module load test
%{php_ztsbindir}/php --no-php-ini \
    --define extension_dir=modules \
    --define extension=%{pecl_name}.so \
    --modules | grep %{pecl_name}

# Remove know to fail tests (font issue)
rm -f tests/gmagick-006-annotateimage.phpt

# Still ignore test result as some fail on old version
TEST_PHP_EXECUTABLE=%{php_ztsbindir}/php \
REPORT_EXIT_STATUS=0 \
NO_INTERACTION=1 \
%{php_ztsbindir}/php run-tests.php \
    -n -q \
    -d extension_dir=modules \
    -d extension=%{pecl_name}.so
fi


%files
%defattr(-,root,root,-)
%doc %{pecl_name}-%{version}%{?prever}/{README,LICENSE}
%config(noreplace) %{php_inidir}/%{pecl_name}.ini
%config(noreplace) %{php_ztsinidir}/%{pecl_name}.ini
%{php_extdir}/%{pecl_name}.so
%{php_ztsextdir}/%{pecl_name}.so
%{pecl_xmldir}/%{name}.xml


%changelog
* Fri Jan 20 2012 Remi Collet <remi@fedoraproject.org> - 1.1.0-0.2.RC2
- Update to 1.1.0RC2
  fix https://bugs.php.net/60807

* Thu Jan 19 2012 Remi Collet <remi@fedoraproject.org> - 1.1.0-0.1.RC1
- Update to 1.1.0RC1

* Mon Dec 05 2011 Remi Collet <remi@fedoraproject.org> - 1.0.10-0.2.b1
- build against php 5.4

* Mon Dec 05 2011 Remi Collet <remi@fedoraproject.org> - 1.0.10-0.1.b1
- Update to 1.0.10b1
- run tests

* Tue Nov 15 2011 Remi Collet <remi@fedoraproject.org> - 1.0.9-0.2.b1
- build against php 5.4
- add patch for php 5.4, see https://bugs.php.net/60308

* Sun Oct 02 2011 Remi Collet <rpms@famillecollet.com> 1.0.9-0.1.b1
- Update to 1.0.9b1
- build zts extension
- clean spec

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
