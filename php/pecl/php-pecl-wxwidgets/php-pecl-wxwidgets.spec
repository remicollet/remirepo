# remirepo spec file for php-pecl-wxwidgets
#
# Copyright (c) 2014-2016 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%{?scl:          %scl_package         php-pecl-wxwidgets}
%{!?scl:         %global _root_prefix %{_prefix}}
%{!?__php:       %global __php        %{_bindir}/php}

%global with_zts    0%{?__ztsphp:1}
%global pecl_name   wxwidgets

Summary:       Cross-platform widget toolkit
Name:          %{?scl_prefix}php-pecl-wxwidgets
Version:       3.0.2.0
Release:       2%{?dist}%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}
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

Requires:         %{?scl_prefix}php(zend-abi) = %{php_zend_api}
Requires:         %{?scl_prefix}php(api) = %{php_core_api}
Requires:         %{__php}

Provides:         %{?scl_prefix}php-%{pecl_name}               = %{version}
Provides:         %{?scl_prefix}php-%{pecl_name}%{?_isa}       = %{version}
Provides:         %{?scl_prefix}php-pecl(%{pecl_name})         = %{version}
Provides:         %{?scl_prefix}php-pecl(%{pecl_name})%{?_isa} = %{version}
Provides:         %{?scl_prefix}php-pecl-%{pecl_name}          = %{version}-%{release}
Provides:         %{?scl_prefix}php-pecl-%{pecl_name}%{?_isa}  = %{version}-%{release}

%if "%{?vendor}" == "Remi Collet" && 0%{!?scl:1} && 0%{?rhel}
# Other third party repo stuff
Obsoletes:     php53-pecl-%{pecl_name}  <= %{version}
Obsoletes:     php53u-pecl-%{pecl_name} <= %{version}
Obsoletes:     php54-pecl-%{pecl_name}  <= %{version}
Obsoletes:     php54w-pecl-%{pecl_name} <= %{version}
%if "%{php_version}" > "5.5"
Obsoletes:     php55u-pecl-%{pecl_name} <= %{version}
Obsoletes:     php55w-pecl-%{pecl_name} <= %{version}
%endif
%if "%{php_version}" > "5.6"
Obsoletes:     php56u-pecl-%{pecl_name} <= %{version}
Obsoletes:     php56w-pecl-%{pecl_name} <= %{version}
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

Package built for PHP %(%{__php} -r 'echo PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')%{?scl: as Software Collection (%{scl} by %{?scl_vendor}%{!?scl_vendor:rh})}.


%prep
%setup -q -c
mv %{pecl_name}-%{version} NTS

%{?_licensedir:sed -e '/LICENSE/s/role="doc"/role="src"/' -i package.xml}

cd NTS
# Ensure no download will be done
sed -e '/Downloading/s/$/; exit 1/' -i config.m4

# Sanity check, really often broken
extver=$(sed -n '/#define PHP_WXWIDGETS_EXTVER/{s/.* "//;s/".*$//;p}' php_wxwidgets.h)
if test "x${extver}" != "x%{version}"; then
   : Error: Upstream extension version is ${extver}, expecting %{version}.
   exit 1
fi
cd ..

cat << 'EOF' | tee NTS/wxphp
#!/bin/sh
exec %{__php} -d extension=%{pecl_name}.so "$@"
EOF

%if %{with_zts}
cp -r NTS ZTS

cat << 'EOF' | tee ZTS/wxphp
#!/bin/sh
if [ -x %{__ztsphp} ]
then exec %{__ztsphp} -d extension=%{pecl_name}.so "$@"
else echo "zts-php not available on this system"
fi
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


%if 0%{?fedora} < 24
# when pear installed alone, after us
%triggerin -- %{?scl_prefix}php-pear
if [ -x %{__pecl} ] ; then
    %{pecl_install} %{pecl_xmldir}/%{name}.xml >/dev/null || :
fi

# posttrans as pear can be installed after us
%posttrans
if [ -x %{__pecl} ] ; then
    %{pecl_install} %{pecl_xmldir}/%{name}.xml >/dev/null || :
fi

%postun
if [ $1 -eq 0 -a -x %{__pecl} ] ; then
    %{pecl_uninstall} %{pecl_name} >/dev/null || :
fi
%endif


%files
%defattr(-,root,root,-)
%{?_licensedir:%license NTS/LICENSE}
%doc %{pecl_docdir}/%{pecl_name}
%{pecl_xmldir}/%{name}.xml

%{_bindir}/wxphp
%{php_extdir}/%{pecl_name}.so

%if %{with_zts}
%{_bindir}/zts-wxphp
%{php_ztsextdir}/%{pecl_name}.so
%endif


%changelog
* Tue Mar  8 2016 Remi Collet <remi@fedoraproject.org> - 3.0.2.0-2
- adapt for F24
- fix license management

* Tue Jun 09 2015 Remi Collet <remi@fedoraproject.org> - 3.0.2.0-1
- Update to 3.0.2.0
- drop runtime dependency on pear, new scriptlets
- drop dependency on zts-php, checked on runtime

* Fri Apr 25 2014  Remi Collet <remi@fedoraproject.org> - 3.0.0.2-1
- initial package, version 3.0.0.2 (stable)
