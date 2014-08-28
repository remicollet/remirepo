#
# RPM spec file for php-twig
#
# Copyright (c) 2014 Shawn Iwinski <shawn.iwinski@gmail.com>
#                    Remi Collet <remi@fedoraproject.org>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%global github_owner     fabpot
%global github_name      Twig
%global github_version   1.16.0
%global github_commit    8ce37115802e257a984a82d38254884085060024

# Lib
%global composer_vendor  twig
%global composer_project twig

# Ext
%global ext_name twig
%global with_zts 0%{?__ztsphp:1}
%if "%{php_version}" < "5.6"
%global ini_name %{ext_name}.ini
%else
%global ini_name 40-%{ext_name}.ini
%endif

# "php": ">=5.2.4"
%global php_min_ver 5.2.4

# Build using "--without tests" to disable tests
%global with_tests %{?_without_tests:0}%{!?_without_tests:1}

%{!?php_inidir: %global php_inidir %{_sysconfdir}/php.d}
%{!?__php:      %global __php      %{_bindir}/php}
%{!?__phpunit:  %global __phpunit  %{_bindir}/phpunit}

Name:          php-%{composer_project}
Version:       %{github_version}
Release:       2%{?dist}
Summary:       The flexible, fast, and secure template engine for PHP

Group:         Development/Libraries
License:       BSD
URL:           http://twig.sensiolabs.org
Source0:       https://github.com/%{github_owner}/%{github_name}/archive/%{github_commit}/%{name}-%{github_version}-%{github_commit}.tar.gz

BuildRequires: php-devel >= %{php_min_ver}
%if %{with_tests}
# For tests
BuildRequires: php-phpunit-PHPUnit
# For tests: phpcompatinfo (computed from version 1.16.0)
BuildRequires: php-ctype
BuildRequires: php-date
BuildRequires: php-dom
BuildRequires: php-hash
BuildRequires: php-iconv
BuildRequires: php-json
BuildRequires: php-mbstring
BuildRequires: php-pcre
BuildRequires: php-reflection
BuildRequires: php-spl
%endif

# Lib
## composer.json
Requires:      php(language) >= %{php_min_ver}
## phpcompatinfo (computed from version 1.16.0)
Requires:      php-ctype
Requires:      php-date
Requires:      php-dom
Requires:      php-hash
Requires:      php-iconv
Requires:      php-json
Requires:      php-mbstring
Requires:      php-pcre
Requires:      php-reflection
Requires:      php-spl
# Ext
Requires:      php(zend-abi) = %{php_zend_api}
Requires:      php(api)      = %{php_core_api}

# Lib
## Composer
Provides:      php-composer(%{composer_vendor}/%{composer_project}) = %{version}
## Rename
Obsoletes:     php-twig-Twig < %{version}-%{release}
Provides:      php-twig-Twig = %{version}-%{release}
## PEAR
Provides:      php-pear(pear.twig-project.org/Twig) = %{version}
# Ext
## Rename
Obsoletes:     php-twig-ctwig         < %{version}-%{release}
Provides:      php-twig-ctwig         = %{version}-%{release}
Provides:      php-twig-ctwig%{?_isa} = %{version}-%{release}
## PECL
Provides:      php-pecl(pear.twig-project.org/CTwig)         = %{version}
Provides:      php-pecl(pear.twig-project.org/CTwig)%{?_isa} = %{version}

# This pkg was the only one in this channel so the channel is no longer needed
Obsoletes:     php-channel-twig

%if 0%{?fedora} < 20 && 0%{?rhel} < 7
# Filter shared private
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}
%endif

%description
%{summary}.

* Fast: Twig compiles templates down to plain optimized PHP code. The
  overhead compared to regular PHP code was reduced to the very minimum.

* Secure: Twig has a sandbox mode to evaluate untrusted template code. This
  allows Twig to be used as a template language for applications where users
  may modify the template design.

* Flexible: Twig is powered by a flexible lexer and parser. This allows the
  developer to define its own custom tags and filters, and create its own
  DSL.


%prep
%setup -qn %{github_name}-%{github_commit}

# Licenses
mv LICENSE LICENSE-lib
mv ext/twig/LICENSE LICENSE-ext

# Ext
## NTS
mv ext/%{ext_name} ext/NTS
## ZTS
%if %{with_zts}
cp -pr ext/NTS ext/ZTS
%endif

## Create configuration file
cat > %{ini_name} << 'INI'
; Enable %{ext_name} extension module
extension=%{ext_name}.so
INI


%build
# Ext
## NTS
pushd ext/NTS
%{_bindir}/phpize
%configure --with-php-config=%{_bindir}/php-config
make %{?_smp_mflags}
popd

## ZTS
%if %{with_zts}
pushd ext/ZTS
%{_bindir}/zts-phpize
%configure --with-php-config=%{_bindir}/zts-php-config
make %{?_smp_mflags}
popd
%endif


%install
# Lib
mkdir -p %{buildroot}/%{_datadir}/php
cp -rp lib/* %{buildroot}/%{_datadir}/php/

# Ext
## NTS
make -C ext/NTS install INSTALL_ROOT=%{buildroot}
install -D -m 0644 %{ini_name} %{buildroot}%{php_inidir}/%{ini_name}
## ZTS
%if %{with_zts}
make -C ext/ZTS install INSTALL_ROOT=%{buildroot}
install -D -m 0644 %{ini_name} %{buildroot}%{php_ztsinidir}/%{ini_name}
%endif


%check
# Ext
: Extension NTS minimal load test
%{__php} --no-php-ini \
    --define extension=ext/NTS/modules/%{ext_name}.so \
    --modules | grep %{ext_name}

%if %{with_zts}
: Extension ZTS minimal load test
%{__ztsphp} --no-php-ini \
    --define extension=ext/ZTS/modules/%{ext_name}.so \
    --modules | grep %{ext_name}
%endif

%if %{with_tests}
# Test suite
## Skip tests known to fail
%ifarch ppc64
sed 's/function testGetAttributeWithTemplateAsObject/function SKIP_testGetAttributeWithTemplateAsObject/' \
    -i test/Twig/Tests/TemplateTest.php
%endif

## Create PHPUnit config with colors turned off
sed 's/colors="true"/colors="false"/' phpunit.xml.dist > phpunit.xml

: Test suite without extension
%{__phpunit} --include-path ./lib -d date.timezone="UTC"

: Test suite with extension
%{__php} --define extension=ext/NTS/modules/%{ext_name}.so \
    %{__phpunit} --include-path ./lib -d date.timezone="UTC"
%else
: Tests skipped
%endif


%files
%{!?_licensedir:%global license %%doc}
%license LICENSE*
%doc CHANGELOG README.rst composer.json
# Lib
%{_datadir}/php/Twig
# Ext
## NTS
%config(noreplace) %{php_inidir}/%{ini_name}
%{php_extdir}/%{ext_name}.so
## ZTS
%if %{with_zts}
%config(noreplace) %{php_ztsinidir}/%{ini_name}
%{php_ztsextdir}/%{ext_name}.so
%endif


%changelog
* Mon Aug 25 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.16.0-2
- Removed obsolete and provide of php-twig-CTwig (never imported into Fedora/EPEL)
- Obsolete php-channel-twig
- Removed comment about optional Xdebug in description (does not provide any new feature)
- Always run extension minimal load test

* Tue Jul 29 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.16.0-1
- Initial package
