# remirepo/fedora spec file for zephir and zephir-parser
#
# Copyright (c) 2016 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#

%if 0%{?scl:1}
%global with_tests   0
%scl_package zephyr-parser
%else
%if "%{php_version}" > "5.6"
%global with_tests   0%{!?_without_tests:1}
%else
%global with_tests   0%{?_with_tests:1}
%endif
%endif

# Get commit from PHP_PHALCON_ZEPVERSION in 
# https://github.com/phalcon/cphalcon/blob/master/ext/php_phalcon.h
%global gh_commit    cae68c4205a93a7a1ea6165bcd5ce5cb470f5bdd
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
#global gh_date      20161126
%global gh_owner     phalcon
%global gh_project   zephir
%global ext_name     zephir_parser

Name:           %{?scl_prefix}%{gh_project}-parser
Version:        0.9.5
Release:        1%{?gh_date:.%{gh_date}git%{gh_short}}%{?dist}%{!?scl:%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}}
Summary:        Zephir parser extension

Group:          Development/Libraries
License:        MIT
URL:            https://getcomposer.org/
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}-%{gh_short}.tar.gz

# Adapt path used in RPM
Patch0:         %{gh_project}-rpm.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  %{?scl_prefix}php-devel > 5.4
BuildRequires:  re2c
%if %{with_tests}
BuildRequires:  %{?scl_prefix}php-json
BuildRequires:  %{?scl_prefix}php-hash
BuildRequires:  %{?scl_prefix}php-ctype
# From composer.json, "require-dev"
#        "squizlabs/php_codesniffer": "~2.6",
#        "phpunit/phpunit": "3.7.*",
#        "ext-gmp": "*",
#        "ext-pdo": "*",
#        "ext-pdo_sqlite": "*"
BuildRequires:  %{?scl_prefix}php-gmp
BuildRequires:  %{?scl_prefix}php-pdo
BuildRequires:  %{?scl_prefix}php-pdo_sqlite
BuildRequires:  %{?scl_prefix}php-composer(phpunit/phpunit)    >= 3.7
%endif

Requires:     %{?scl_prefix}php(zend-abi) = %{php_zend_api}
Requires:     %{?scl_prefix}php(api) = %{php_core_api}
%{?_sclreq:Requires: %{?scl_prefix}runtime%{?_sclreq}%{?_isa}}

%description
Parser extension used by %{gh_project}


%package -n %{?scl_prefix}%{gh_project}
Summary:       Zephir language for creation of extensions for PHP.
Group:         Development/Languages
%if 0%{?fedora} >= 12 || 0%{?rhel} >= 6
BuildArch:     noarch
%endif

Requires:       %{?scl_prefix}php-cli
Requires:       %{name} = %{version}-%{release}
# From composer.json, "require"
#        "php": ">=5.4",
#        "ext-json": "*",
#        "ext-hash": "*",
#        "ext-ctype": "*",
#        "ext-xml": "*"
Requires:       %{?scl_prefix}php(language)                    >= 5.4
Requires:       %{?scl_prefix}php-json
Requires:       %{?scl_prefix}php-hash
Requires:       %{?scl_prefix}php-ctype
Requires:       %{?scl_prefix}php-xml
# From phpcompatinfo
Requires:       %{?scl_prefix}php-reflection
Requires:       %{?scl_prefix}php-date
Requires:       %{?scl_prefix}php-gmp
Requires:       %{?scl_prefix}php-pcre
Requires:       %{?scl_prefix}php-pdo
Requires:       %{?scl_prefix}php-spl

Provides:       %{?scl_prefix}php-composer(%{gh_owner}/%{gh_project}) = %{version}

%description  -n %{?scl_prefix}%{gh_project}
Zephir - Ze(nd Engine) Ph(p) I(nt)r(mediate) - is a high level language
that eases the creation and maintainability of extensions for PHP.
Zephir extensions are exported to C code that can be compiled and
optimized by major C compilers such as gcc/clang/vc++. Functionality
is exposed to the PHP language.

Main features:
* Both dynamic/static typing
* Reduced execution overhead compared with full interpretation
* Restricted procedural programming, promoting OOP
* Memory safety
* Ahead-of-time (AOT) compiler to provide predictable performance

Compiler design goals:
* Multi-pass compilation
* Type speculation/inference
* Allow runtime profile-guided optimizations, pseudo-constant propagation
  and indirect/virtual function inlining


%prep
%setup -q -n %{gh_project}-%{gh_commit}

: Fix versions
sed -e 's/0.9.4a-dev/%{version}/' -i Library/Compiler.php
sed -e '/PHP_ZEPHIR_PARSER_VERSION/s/0.1.0/%{version}/' -i parser/php_zephir_parser.h

%patch0 -p0 -b .rpm
sed -e 's:@DATADIR@:%{_datadir}:;s:@BINDIR@:%{_bindir}:' \
    -i bin/%{gh_project}

find . -name \*.php -exec chmod -x {} \;


%build
cd parser/parser
./build_linux.sh
cd ..
%{_bindir}/phpize
%configure \
    --with-php-config=%{_bindir}/php-config
make



%install
rm -rf       %{buildroot}

: Library and resources
mkdir -p     %{buildroot}%{_datadir}/%{gh_project}
for i in *php Library kernels prototypes templates
do
   cp -pr $i %{buildroot}%{_datadir}/%{gh_project}/$i
done

: Command
install -Dpm 755 bin/%{gh_project} %{buildroot}%{_bindir}/%{gh_project}

: Extension
make install -C parser INSTALL_ROOT=%{buildroot}


%check
sed -e 's:%ZEPHIRDIR%:%{buildroot}%{_datadir}/%{gh_project}:g' \
    -e 's: php:%{_bindir}/php:' \
     bin/%{gh_project}.rpm > bin/%{gh_project}.test
sh ./bin/%{gh_project}.test version
sh ./bin/%{gh_project}.test version | grep %{version}

: Check extension
%{_bindir}/php -n -d extension=parser/modules/%{ext_name}.so -m | grep %{ext_name}

%if %{with_tests}
: Run test suite
if %{_bindir}/phpunit --atleast-version 5; then
   %{_bindir}/phpunit unit-tests/Zephir --verbose
fi

%else
: Test suite disabled
%endif


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE
%{php_extdir}/%{ext_name}.so

%files  -n %{?scl_prefix}%{gh_project}
%defattr(-,root,root,-)
%doc *.md
%doc composer.json
%{_bindir}/%{gh_project}
%{_datadir}/%{gh_project}


%changelog
* Sun Nov 27 2016 Remi Collet <remi@fedoraproject.org> - 0.9.5-1
- version 0.9.5

* Fri Oct 14 2016 Remi Collet <remi@fedoraproject.org> - 0.9.4-2.20161014git23856e1
- new snapshot to fix PHP 7.1 compatibility of generated code

* Mon Oct 10 2016 Remi Collet <remi@fedoraproject.org> - 0.9.4-1.20160929git22f6632
- new snapshot to fix PHP 7.1 compatibility of generated code

* Wed Sep 14 2016 Remi Collet <remi@fedoraproject.org> - 0.9.3-2.20160728gite716dbe
- rebuild for PHP 7.1 new API version

* Sat Jul 30 2016 Remi Collet <remi@fedoraproject.org> - 0.9.0-1.20160728gite716dbe
- Initial package

