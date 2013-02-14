%global owner      zend-dev
%global extname    ZendOptimizerPlus
%global commit     afb43f5650da2d24f03ce893bcd5123c12aba3fd
%global short      %(c=%{commit}; echo ${c:0:7})
%global prever     -dev

Name:          php-ZendOptimizerPlus
Version:       7.0.0
Release:       0.2.git%{short}%{?dist}.1
Summary:       The Zend Optimizer+

Group:         Development/Libraries
License:       PHP
URL:           https://github.com/%{owner}/%{extname}
Source0:       %{url}/archive/%{commit}/%{extname}-%{version}-%{short}.tar.gz
Source1:       %{extname}.ini

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: php-devel

Requires:      php(zend-abi) = %{php_zend_api}
Requires:      php(api) = %{php_core_api}

# Only one opcode cache could be enabled
Conflicts:     php-eaccelerator
Conflicts:     php-xcache
Conflicts:     php-pecl-apc

# Filter private shared
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}


%description
The Zend Optimizer+ provides faster PHP execution through opcode caching and
optimization. It improves PHP performance by storing precompiled script
bytecode in the shared memory. This eliminates the stages of reading code from
the disk and compiling it on future access. In addition, it applies a few
bytecode optimization patterns that make code execution faster.


%prep
%setup -q -c

mv %{extname}-%{commit} NTS

# Sanity check, really often broken
extver=$(sed -n '/#define ACCELERATOR_VERSION/{s/.* "//;s/".*$//;p}' NTS/ZendAccelerator.h)
if test "x${extver}" != "x%{version}%{?prever}"; then
   : Error: Upstream extension version is ${extver}, expecting %{version}%{?prever}.
   exit 1
fi

cp %{SOURCE1} %{extname}.ini

# Duplicate source tree for NTS / ZTS build
cp -pr NTS ZTS


%build
cd NTS
%{_bindir}/phpize
%configure \
    --enable-optimizer-plus \
    --with-php-config=%{_bindir}/php-config
make %{?_smp_mflags}

cd ../ZTS
%{_bindir}/zts-phpize
%configure \
    --enable-optimizer-plus \
    --with-php-config=%{_bindir}/zts-php-config
make %{?_smp_mflags}


%install
rm -rf %{buildroot}

install -d -m 755 %{buildroot}%{php_inidir}
sed -e 's:@EXTPATH@:%{php_extdir}:' \
    %{extname}.ini >%{buildroot}%{php_inidir}/%{extname}.ini

install -d -m 755 %{buildroot}%{php_ztsinidir}
sed -e 's:@EXTPATH@:%{php_ztsextdir}:' \
    %{extname}.ini >%{buildroot}%{php_ztsinidir}/%{extname}.ini

make -C NTS install INSTALL_ROOT=%{buildroot}
make -C ZTS install INSTALL_ROOT=%{buildroot}


%clean
rm -rf %{buildroot}


%check
: Minimal load test of the built extensions

%{__php} \
    -n -d zend_extension=%{buildroot}%{php_extdir}/%{extname}.so \
    -m | grep "Zend Optimizer+"

%{__ztsphp} \
    -n -d zend_extension=%{buildroot}%{php_ztsextdir}/%{extname}.so \
    -m | grep "Zend Optimizer+"


%files
%defattr(-,root,root,-)
%doc NTS/{LICENSE,README}
%config(noreplace) %{php_inidir}/%{extname}.ini
%config(noreplace) %{php_ztsinidir}/%{extname}.ini
%{php_extdir}/%{extname}.so
%{php_ztsextdir}/%{extname}.so


%changelog
* Thu Feb 14 2013 Remi Collet <remi@fedoraproject.org> - 7.0.0-0.2.gitafb43f5
- new snapshot
- better default configuration file (new upstream recommendation)
- License file now provided by upstream

* Wed Feb 13 2013 Remi Collet <remi@fedoraproject.org> - 7.0.0-0.1.gitaafc145
- initial package
