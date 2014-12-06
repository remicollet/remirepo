# spec file for php-pecl-graphdat
#
# Copyright (c) 2014 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/3.0/
#
# Please, preserve the changelog entries
#
%{?scl:          %scl_package         php-pecl-graphdat}
%{!?php_inidir:  %global php_inidir   %{_sysconfdir}/php.d}
%{!?__pecl:      %global __pecl       %{_bindir}/pecl}
%{!?__php:       %global __php        %{_bindir}/php}

%global pecl_name    graphdat
%global with_zts     0%{?__ztsphp:1}
%if "%{php_version}" < "5.6"
%global ini_name     %{pecl_name}.ini
%else
%global ini_name     40-%{pecl_name}.ini
%endif
%if 0%{?fedora} > 15 || 0%{?rhel} > 6
%global with_msgpack 1
%else
%global with_msgpack 0
%endif

Summary:       Troubleshoot application and server performance
Name:          %{?scl_prefix}php-pecl-graphdat
Version:       1.0.4
Release:       1%{?dist}%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}
# https://github.com/alphashack/graphdat-sdk-php/issues/6
License:       ASL 2.0
Group:         Development/Languages
URL:           http://pecl.php.net/package/%{pecl_name}
Source:        http://pecl.php.net/get/%{pecl_name}-%{version}.tgz

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: %{?scl_prefix}php-devel
BuildRequires: %{?scl_prefix}php-pear
%if %{with_msgpack}
BuildRequires: msgpack-devel
%endif

Requires(post): %{__pecl}
Requires(postun): %{__pecl}
Requires:      %{?scl_prefix}php(zend-abi) = %{php_zend_api}
Requires:      %{?scl_prefix}php(api) = %{php_core_api}
%{?_sclreq:Requires: %{?scl_prefix}runtime%{?_sclreq}%{?_isa}}

Provides:      %{?scl_prefix}php-%{pecl_name} = %{version}
Provides:      %{?scl_prefix}php-%{pecl_name}%{?_isa} = %{version}
Provides:      %{?scl_prefix}php-pecl(%{pecl_name}) = %{version}
Provides:      %{?scl_prefix}php-pecl(%{pecl_name})%{?_isa} = %{version}

%if "%{?vendor}" == "Remi Collet" && 0%{!?scl:1}
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
# Filter shared private
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}
%endif


%description
Graphdat is a real time performance monitoring tool for websites.
Graphdat graphs system metrics along side request counts and response
time data. The purpose of the extension is report request counts and
response time information to our agent (installed on the box) which
forwards that along to our servers. The data is then presented in a
graph so that you can see performance spikes as they happen, and
trends over time.

Package built for PHP %(%{__php} -r 'echo PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')%{?scl: as Software Collection}.


%prep
%setup -q -c 

# Don't install/register tests
sed -e 's/role="test"/role="src"/' \
%if %{with_msgpack}
    -e '\:name="src/msgpack:d' \
%endif
    -i package.xml

mv %{pecl_name}-%{version} NTS
cd NTS

%if %{with_msgpack}
# use system library
rm -rf src/msgpack
%endif

# Sanity check, really often broken
extver=$(sed -n '/#define PHP_GRAPHDAT_VERSION/{s/.* "//;s/".*$//;p}' php_graphdat.h)
if test "x${extver}" != "x%{version}"; then
   : Error: Upstream extension version is ${extver}, expecting %{version}.
   exit 1
fi
cd ..

%if %{with_zts}
# duplicate for ZTS build
cp -pr NTS ZTS
%endif

# Drop in the bit of configuration
cat << 'EOF' | tee %{ini_name}
; Enable '%{pecl_name}' extension module
extension = %{pecl_name}.so

; Configuration options
;graphdat.socketFile = /tmp/gd.agent.sock
;graphdat.socketPort = 26873
;graphdat.debug = false
;graphdat.enable_joomla  = false
;graphdat.enable_drupal  = false
;graphdat.enable_magento = false
;graphdat.enable_cakephp = false
EOF


%build
%ifarch i386 i686
CFLAGS=$(echo %{optflags} | sed -e "s|i386|i686|g")
export CFLAGS
%endif

cd NTS
%{_bindir}/phpize
%configure \
%if %{with_msgpack}
    --with-libmsgpack \
%endif
    --with-php-config=%{_bindir}/php-config
make %{?_smp_mflags}

%if %{with_zts}
cd ../ZTS
%{_bindir}/zts-phpize
%configure \
%if %{with_msgpack}
    --with-libmsgpack \
%endif
    --with-php-config=%{_bindir}/zts-php-config
make %{?_smp_mflags}
%endif


%install
rm -rf %{buildroot}
# Install the NTS stuff
make -C NTS install INSTALL_ROOT=%{buildroot}
install -D -m 644 %{ini_name} %{buildroot}%{php_inidir}/%{ini_name}

%if %{with_zts}
# Install the ZTS stuff
make -C ZTS install INSTALL_ROOT=%{buildroot}
install -D -m 644 %{ini_name} %{buildroot}%{php_ztsinidir}/%{ini_name}
%endif

# Install the package XML file
install -D -m 644 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml

# Documentation
cd NTS
for i in $(grep 'role="doc"' ../package.xml | sed -e 's/^.*name="//;s/".*$//')
do install -Dpm 644 $i %{buildroot}%{pecl_docdir}/%{pecl_name}/$i
done


%check
: Minimal load test for NTS extension
%{__php} --no-php-ini \
    --define extension=%{buildroot}%{php_extdir}/%{pecl_name}.so \
    --modules | grep %{pecl_name}

%if %{with_zts}
: Minimal load test for ZTS extension
%{__ztsphp} --no-php-ini \
    --define extension=%{buildroot}%{php_ztsextdir}/%{pecl_name}.so \
    --modules | grep %{pecl_name}
%endif


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
%{?_licensedir:%license NTS/LICENSE}
%doc %{pecl_docdir}/%{pecl_name}
%{pecl_xmldir}/%{name}.xml

%config(noreplace) %{php_inidir}/%{ini_name}
%{php_extdir}/%{pecl_name}.so

%if %{with_zts}
%config(noreplace) %{php_ztsinidir}/%{ini_name}
%{php_ztsextdir}/%{pecl_name}.so
%endif


%changelog
* Sat Dec 06 2014 Remi Collet <remi@fedoraproject.org> - 1.0.4-1
- Update to 1.0.4

* Fri Sep 19 2014 Remi Collet <remi@fedoraproject.org> - 1.0.3-1
- initial package, version 1.0.3 (stable)
- open https://github.com/alphashack/graphdat-sdk-php/pull/5
- open https://github.com/alphashack/graphdat-sdk-php/issues/6