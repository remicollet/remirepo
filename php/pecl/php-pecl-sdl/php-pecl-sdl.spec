# spec file for php-pecl-sdl
#
# Copyright (c) 2013-2014 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/3.0/
#
# Please, preserve the changelog entries
#
%{?scl:          %scl_package        php-pecl-sdl}
%{!?php_inidir:  %global php_inidir  %{_sysconfdir}/php.d}
%{!?__pecl:      %global __pecl      %{_bindir}/pecl}
%{!?__php:       %global __php       %{_bindir}/php}

%global with_zts    0%{?__ztsphp:1}
%global with_tests  %{?_with_tests:1}%{!?_with_tests:0}
%global pecl_name   sdl

Summary:       Simple DirectMedia Layer for PHP
Name:          %{?scl_prefix}php-pecl-sdl
Version:       0.9.2
Release:       1%{?dist}%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}
License:       PHP
Group:         Development/Languages
URL:           http://pecl.php.net/package/sdl
Source0:       http://pecl.php.net/get/%{pecl_name}-%{version}.tgz

Patch0:           %{pecl_name}-nts.patch

BuildRoot:        %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires:    %{?scl_prefix}php-devel > 5.2.0
BuildRequires:    %{?scl_prefix}php-pear
BuildRequires:    SDL-devel

Requires(post):   %{__pecl}
Requires(postun): %{__pecl}
Requires:         %{?scl_prefix}php(zend-abi) = %{php_zend_api}
Requires:         %{?scl_prefix}php(api) = %{php_core_api}
Requires:         %{__php}
%if %{with_zts}
Requires:         %{__ztsphp}
%endif

Provides:         %{?scl_prefix}php-%{pecl_name} = %{version}
Provides:         %{?scl_prefix}php-%{pecl_name}%{?_isa} = %{version}
Provides:         %{?scl_prefix}php-pecl(%{pecl_name}) = %{version}
Provides:         %{?scl_prefix}php-pecl(%{pecl_name})%{?_isa} = %{version}

%if 0%{!?scl:1}
# Other third party repo stuff
%if "%{php_version}" > "5.4"
Obsoletes:     php53-pecl-%{pecl_name}
Obsoletes:     php53u-pecl-%{pecl_name}
Obsoletes:     php54-pecl-%{pecl_name}
%endif
%if "%{php_version}" > "5.5"
Obsoletes:     php55u-pecl-%{pecl_name}
%endif
%endif

%if 0%{?fedora} < 20 && 0%{?rhel} < 7
# filter private shared
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}
%endif


%description
This extension allows you to develop multimedia applications with PHP
using the complete SDL library API.

Use the "phpsdl" command to launch a SDL application.


%prep
%setup -q -c
mv %{pecl_name}-%{version} NTS

pushd NTS
%patch0 -p2 -b .nts
popd

cat << 'EOF' | tee phpsdl
#!/bin/sh
exec %{__php} -d extension=%{pecl_name}.so "$@"
EOF

%if %{with_zts}
cat << 'EOF' | tee zts-phpsdl
#!/bin/sh
exec %{__ztsphp} -d extension=%{pecl_name}.so "$@"
EOF

cp -r NTS ZTS
%endif

%build

peclconf() {
%configure \
    --with-sdl \
    --with-php-config=$1
}
cd NTS
%{_bindir}/phpize
peclconf %{_bindir}/php-config
make %{?_smp_mflags}

%if %{with_zts}
cd ../ZTS
%{_bindir}/zts-phpize
peclconf %{_bindir}/zts-php-config
make %{?_smp_mflags}
%endif


%install
rm -rf %{buildroot}
make -C NTS install INSTALL_ROOT=%{buildroot}

# Install XML package description
install -Dpm 644 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml

# Install the command wrapper
install -Dpm 755 phpsdl %{buildroot}%{_bindir}/phpsdl

%if %{with_zts}
make -C ZTS install INSTALL_ROOT=%{buildroot}
install -Dpm 755 zts-phpsdl %{buildroot}%{_bindir}/zts-phpsdl
%endif

# Test & Documentation
cd NTS
for i in $(grep 'role="test"' ../package.xml | sed -e 's/^.*name="//;s/".*$//')
do install -Dpm 644 $i %{buildroot}%{pecl_testdir}/%{pecl_name}/$i
done
for i in $(grep 'role="doc"' ../package.xml | sed -e 's/^.*name="//;s/".*$//')
do install -Dpm 644 $i %{buildroot}%{pecl_docdir}/%{pecl_name}/$i
done


%check
: Minimal load test for NTS extension
%{__php} -n -q \
    -d extension=NTS/modules/%{pecl_name}.so \
    --modules | grep -i %{pecl_name}

%if %{with_zts}
: Minimal load test for ZTS extension
%{__ztsphp} -n -q \
    -d extension=ZTS/modules/%{pecl_name}.so \
    --modules | grep -i %{pecl_name}
%endif


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
%doc %{pecl_docdir}/%{pecl_name}
%doc %{pecl_testdir}/%{pecl_name}
%{_bindir}/phpsdl
%{php_extdir}/%{pecl_name}.so
%{pecl_xmldir}/%{name}.xml

%if %{with_zts}
%{_bindir}/zts-phpsdl
%{php_ztsextdir}/%{pecl_name}.so
%endif


%changelog
* Tue Dec 03 2013 Remi Collet <remi@fedoraproject.org> - 0.9.2-1
- Update to 0.9.2 (beta)
- adapt for SCL
- add patch to fix NTS build

* Tue Nov 26 2013 Remi Collet <remi@fedoraproject.org> - 0.9.1-1
- Update to 0.9.1 (beta)
- drop build patch merged upstream

* Mon Nov 25 2013  Remi Collet <remi@fedoraproject.org> - 0.9.0-1
- initial package, 0.9.0 (beta)
