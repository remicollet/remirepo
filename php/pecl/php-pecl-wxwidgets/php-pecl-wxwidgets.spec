# spec file for php-pecl-wxwidgets
#
# Copyright (c) 2014 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/3.0/
#
# Please, preserve the changelog entries
#
%{?scl:          %scl_package         php-pecl-wxwidgets}
%{!?scl:         %global _root_prefix %{_prefix}}
%{!?php_inidir:  %global php_inidir   %{_sysconfdir}/php.d}
%{!?__pecl:      %global __pecl       %{_bindir}/pecl}
%{!?__php:       %global __php        %{_bindir}/php}

%global with_zts    0%{?__ztsphp:1}
%global pecl_name   wxwidgets

Summary:       Cross-platform widget toolkit
Name:          %{?scl_prefix}php-pecl-wxwidgets
Version:       3.0.0.2
Release:       1%{?dist}%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}
License:       PHP
Group:         Development/Languages
URL:           http://pecl.php.net/package/wxwidgets
Source0:       http://pecl.php.net/get/%{pecl_name}-%{version}.tgz

BuildRoot:        %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires:    %{?scl_prefix}php-devel > 5.3
BuildRequires:    %{?scl_prefix}php-pear
BuildRequires:    wxGTK3-devel
%if 0%{?rhel} == 6
# We need a recent g++ compiler
BuildRequires:    devtoolset-2-toolchain
%endif

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

%if "%{?vendor}" == "Remi Collet"
# Other third party repo stuff
Obsoletes:     php53-pecl-%{pecl_name}
Obsoletes:     php53u-pecl-%{pecl_name}
Obsoletes:     php54-pecl-%{pecl_name}
%if "%{php_version}" > "5.5"
Obsoletes:     php55u-pecl-%{pecl_name}
%endif
%if "%{php_version}" > "5.6"
Obsoletes:     php56u-pecl-%{pecl_name}
%endif
%endif

%if 0%{?fedora} < 20 && 0%{?rhel} < 7
# filter private shared
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}
%endif


%description
Wraps the wxWidgets library, which allows to write
multi-platform desktop applications that make use of the native
graphical components available to the different platforms.

Use the "wxphp" command to launch an application.


%prep
%setup -q -c
mv %{pecl_name}-%{version} NTS

cat << 'EOF' | tee NTS/wxphp
#!/bin/sh
exec %{__php} -d extension=%{pecl_name}.so "$@"
EOF

%if %{with_zts}
cp -r NTS ZTS

cat << 'EOF' | tee ZTS/wxphp
#!/bin/sh
exec %{__ztsphp} -d extension=%{pecl_name}.so "$@"
EOF
%endif


%build
peclconf() {
%configure \
    --with-wxwidgets=%{_root_prefix} \
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
install -Dpm 755 NTS/wxphp %{buildroot}%{_bindir}/wxphp

%if %{with_zts}
make -C ZTS install INSTALL_ROOT=%{buildroot}
install -Dpm 755 ZTS/wxphp %{buildroot}%{_bindir}/zts-wxphp
%endif

# Test & Documentation
cd NTS
for i in $(grep 'role="doc"' ../package.xml | sed -e 's/^.*name="//;s/".*$//')
do install -Dpm 644 $i %{buildroot}%{pecl_docdir}/%{pecl_name}/$i
done


%check
: no check, as this would require a DISPLAY.


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
%{pecl_xmldir}/%{name}.xml

%{_bindir}/wxphp
%{php_extdir}/%{pecl_name}.so

%if %{with_zts}
%{_bindir}/zts-wxphp
%{php_ztsextdir}/%{pecl_name}.so
%endif


%changelog
* Fri Apr 25 2014  Remi Collet <remi@fedoraproject.org> - 3.0.0.2-1
- initial package, version 3.0.0.2 (stable)