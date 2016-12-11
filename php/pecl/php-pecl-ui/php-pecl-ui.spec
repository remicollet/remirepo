# remirepo spec file for php-pecl-ui
#
# Copyright (c) 2016 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%if 0%{?scl:1}
%global sub_prefix %{scl_prefix}
%scl_package       php-pecl-ui
%else
%global _root_prefix %{_prefix}
%endif


# The project is UI but the extension is ui
%global proj_name UI
%global pecl_name ui
%global with_zts  0%{!?_without_zts:%{?__ztsphp:1}}
%global ini_name  40-%{pecl_name}.ini

Name:           %{?sub_prefix}php-pecl-ui
Version:        2.0.0
Release:        2%{?dist}%{!?scl:%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}}
Summary:        UI API

License:        PHP
Group:          Development/Languages
URL:            http://pecl.php.net/package/%{proj_name}
Source0:        http://pecl.php.net/get/%{proj_name}-%{version}%{?prever}.tgz

BuildRequires:  %{?scl_prefix}php-devel >= 7
BuildRequires:  %{?scl_prefix}php-pear
BuildRequires:  libui-devel

Requires:       %{?scl_prefix}php(zend-abi) = %{php_zend_api}
Requires:       %{?scl_prefix}php(api) = %{php_core_api}
%{?_sclreq:Requires: %{?scl_prefix}runtime%{?_sclreq}%{?_isa}}

Provides:       %{?scl_prefix}php-pecl(%{proj_name})         = %{version}
Provides:       %{?scl_prefix}php-pecl(%{proj_name})%{?_isa} = %{version}
%if "%{?scl_prefix}" != "%{?sub_prefix}"
Provides:       %{?scl_prefix}php-pecl-%{pecl_name}          = %{version}-%{release}
Provides:       %{?scl_prefix}php-pecl-%{pecl_name}%{?_isa}  = %{version}-%{release}
%endif
Provides:       %{?scl_prefix}php-pecl(%{pecl_name})         = %{version}
Provides:       %{?scl_prefix}php-pecl(%{pecl_name})%{?_isa} = %{version}
Provides:       %{?scl_prefix}php-%{pecl_name}               = %{version}
Provides:       %{?scl_prefix}php-%{pecl_name}%{?_isa}       = %{version}

%if "%{?vendor}" == "Remi Collet" && 0%{!?scl:1} && 0%{?rhel}
# Other third party repo stuff
Obsoletes:     php70u-pecl-ui <= %{version}
Obsoletes:     php70w-pecl-ui <= %{version}
%if "%{php_version}" > "7.1"
Obsoletes:     php71u-pecl-ui <= %{version}
Obsoletes:     php71w-pecl-ui <= %{version}
%endif
%endif

%if 0%{?fedora} < 20 && 0%{?rhel} < 7
# Filter shared private
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%endif
%{?filter_setup}


%description
An OO wrapper around libui.

Documentation : http://php.net/ui

Use the phpui command to launch applications.

Package built for PHP %(%{__php} -r 'echo PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')%{?scl: as Software Collection (%{scl} by %{?scl_vendor}%{!?scl_vendor:rh})}.


%prep
%setup -c -q 
mv %{proj_name}-%{version}%{?prever} NTS

%{?_licensedir:sed -e '/LICENSE/s/role="doc"/role="src"/' -i package.xml}

cd NTS

extver=$(sed -n '/#define PHP_UI_VERSION/{s/.* "//;s/".*$//;p}' php_ui.h)
if test "x${extver}" != "x%{version}%{?prever}%{?gh_date:dev}"; then
   : Error: Upstream HTTP version is now ${extver}, expecting %{version}%{?prever}%{?gh_date:dev}.
   : Update the pdover macro and rebuild.
   exit 1
fi
cd ..

cat << 'EOF' | tee NTS/phpui
#!/bin/sh
exec %{__php} -d extension=%{pecl_name}.so "$@"
EOF

%if %{with_zts}
cp -r NTS ZTS

cat << 'EOF' | tee ZTS/phpui
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
  --with-ui \
  --with-libdir=%{_lib} \
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
make -C NTS install INSTALL_ROOT=%{buildroot}

# Install XML package description
install -Dpm 644 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml

# Install the command wrapper
install -Dpm 755 NTS/phpui %{buildroot}%{_bindir}/phpui

%if %{with_zts}
make -C ZTS install INSTALL_ROOT=%{buildroot}
install -Dpm 755 ZTS/phpui %{buildroot}%{_bindir}/zts-phpui
%endif

# Documentation
cd NTS
for i in $(grep 'role="doc"' ../package.xml | sed -e 's/^.*name="//;s/".*$//')
do install -Dpm 644 $i %{buildroot}%{pecl_docdir}/%{proj_name}/$i
done

# make the cli commands available in standard root for SCL build
%if 0%{?scl:1}
install -m 755 -d %{buildroot}%{_root_bindir}
ln -s %{_bindir}/phpui      %{buildroot}%{_root_bindir}/%{scl_prefix}phpui
%endif


%check
if [ -z "$DISPLAY"]; then
   : skip test which requires a display
   exit 0
fi

: Minimal load test for NTS extension
%{__php} --no-php-ini \
    $modules \
    --define extension=modules/%{pecl_name}.so \
    --modules | grep %{pecl_name}

%if %{with_zts}
cd ../ZTS
: Minimal load test for ZTS extension
%{__ztsphp} --no-php-ini \
    $modules \
    --define extension=modules/%{pecl_name}.so \
    --modules | grep %{pecl_name}
%endif


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
    %{pecl_uninstall} %{proj_name} >/dev/null || :
fi
%endif


%files
%{?_licensedir:%license NTS/LICENSE}
%doc %{pecl_docdir}/%{proj_name}
%{pecl_xmldir}/%{name}.xml
%{php_extdir}/%{pecl_name}.so
%{_bindir}/phpui

%if %{with_zts}
%{php_ztsextdir}/%{pecl_name}.so
%{_bindir}/zts-phpui
%endif

%if 0%{?scl:1}
%{_root_bindir}/%{scl_prefix}phpui
%endif


%changelog
* Thu Dec  1 2016 Remi Collet <remi@fedoraproject.org> - 2.0.0-2
- rebuild with PHP 7.1.0 GA

* Wed Nov 02 2016 Remi Collet <remi@fedoraproject.org> - 2.0.0-1
- Update to 2.0.0

* Sun Oct 30 2016 Remi Collet <remi@fedoraproject.org> - 1.0.3-1
- Update to 1.0.3

* Fri Oct 28 2016 Remi Collet <remi@fedoraproject.org> - 1.0.2-1
- Update to 1.0.2

* Wed Oct 26 2016 Remi Collet <remi@fedoraproject.org> - 1.0.1-1
- Update to 1.0.1

* Tue Oct 25 2016 Remi Collet <remi@fedoraproject.org> - 1.0.0-1
- initial package

