# remirepo spec file for php-phalcon3
#
# Copyright (c) 2014-2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%if 0%{?scl:1}
%global sub_prefix %{scl_prefix}
%scl_package       php-phalcon3
%else
%global pkg_name   %{name}
%endif

%global gh_commit    2f52d45cdc1dfb9d9dac40a63a7ca333d785e68c
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     phalcon
%global gh_project   cphalcon
%global with_zts     0%{!?_without_zts:%{?__ztsphp:1}}
%global with_tests   0%{?_with_tests:1}
%global ext_name     phalcon
%if "%{php_version}" < "5.6"
# after pdo.ini, json.ini, igbinary.ini
%global ini_name  z-%{ext_name}.ini
%else
# after 40-json.ini, 20-pdo.ini, 40-igbinary.ini
%global ini_name  50-%{ext_name}.ini
%endif

Name:           %{?sub_prefix}php-phalcon3
Version:        3.0.4
Release:        1%{?dist}%{!?scl:%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}}
Summary:        Phalcon Framework

Group:          Development/Libraries
License:        MIT
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        %{gh_project}-%{version}-strip.tar.xz
# Script to generate the stripped archive from a git clone
Source1:        strip.sh
# Fake minifiers
Source2:        cssminifier.c
Source3:        cssminifier.h
Source4:        jsminifier.c
Source5:        jsminifier.h

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: %{?scl_prefix}php-devel > 5.5
BuildRequires: %{?scl_prefix}php-json
BuildRequires: %{?scl_prefix}php-pdo
# For sources generation
BuildRequires: %{?scl_prefix}zephir >= 0.9.6
BuildRequires: %{?scl_prefix}php-gd
BuildRequires: %{?scl_prefix}php-libsodium
BuildRequires: %{?scl_prefix}php-mbstring
BuildRequires: %{?scl_prefix}php-msgpack
BuildRequires: %{?scl_prefix}php-imagick

Requires:      %{?scl_prefix}php(zend-abi) = %{php_zend_api}
Requires:      %{?scl_prefix}php(api) = %{php_core_api}
Requires:      %{?scl_prefix}php-json%{?_isa}
Requires:      %{?scl_prefix}php-pdo%{?_isa}
%{?_sclreq:Requires: %{?scl_prefix}runtime%{?_sclreq}%{?_isa}}

Provides:      %{?scl_prefix}php-phalcon          = %{version}-%{release}
Provides:      %{?scl_prefix}php-phalcon%{?_isa}  = %{version}-%{release}
%if "%{?scl_prefix}" != "%{?sub_prefix}"
Provides:      %{?scl_prefix}php-phalcon3         = %{version}-%{release}
Provides:      %{?scl_prefix}php-phalcon3%{?_isa} = %{version}-%{release}
%endif
%if "%{php_version}" > "7"
Obsoletes:     %{?scl_prefix}php-phalcon  < 3
Obsoletes:     %{?scl_prefix}php-phalcon2 < 3
%else
# Only one version can be installed
Conflicts:     %{?scl_prefix}php-phalcon  < 3
Conflicts:     %{?scl_prefix}php-phalcon2 < 3
%endif

# Don't provides php-composer(phalcon/cphalcon), not registered on packagist

%if 0%{?fedora} < 20 && 0%{?rhel} < 7
# Filter shared private
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%endif
%{?filter_setup}


%description
Phalcon is a web framework implemented as a C extension offering
high performance and lower resource consumption.

Notice: non-free JS and CSS minifiers are disabled.

Documentation: http://docs.phalconphp.com

Package built for PHP %(%{__php} -r 'echo PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')%{?scl: as Software Collection (%{scl} by %{?scl_vendor}%{!?scl_vendor:rh})}.


%prep
%setup -q -n %{gh_project}-%{gh_commit}

cp %{SOURCE2} %{SOURCE3} %{SOURCE4} %{SOURCE5} \
   ext/phalcon/assets/filters/

# Sanity check, really often broken
extver=$(sed -n '/#define PHP_PHALCON_VERSION/{s/.* "//;s/".*$//;p}' ext/php_phalcon.h)
if test "x${extver}" != "x%{version}%{?prever:-%{prever}}"; then
   : Error: Upstream extension version is ${extver}, expecting %{version}%{?prever:-%{prever}}.
   exit 1
fi

# Create configuration file
cat << 'EOF' | tee %{ini_name}
; Enable '%{summary}' extension module
extension=%{ext_name}.so

; Configuration
;phalcon.db.escape_identifiers = '1'
;phalcon.db.force_casting = '0'
;phalcon.orm.events = '1'
;phalcon.orm.virtual_foreign_keys = '1'
;phalcon.orm.column_renaming = '1'
;phalcon.orm.not_null_validations = '1'
;phalcon.orm.exception_on_failed_save = '0'
;phalcon.orm.enable_literals = '1'
;phalcon.orm.late_state_binding = '0'
;phalcon.orm.enable_implicit_joins = '1'
;phalcon.orm.cast_on_hydrate = '0'
;phalcon.orm.ignore_unknown_columns = '0'

EOF


%build
peclconf() {
%configure \
  --enable-phalcon \
  --with-libdir=%{_lib} \
  --with-php-config=$1
}

: Generate the SAFE sources - optimization seems no more needed

%if "%{php_version}" > "7.0"
%{_bindir}/zephir generate --backend=ZendEngine3
%{__php} build/gen-build.php
mv build/php7/safe build/NTS
%else
%{_bindir}/zephir generate --backend=ZendEngine2
%{__php} build/gen-build.php
mv build/php5/safe build/NTS
%endif

%if %{with_zts}
: Duplicate source tree for NTS / ZTS build
cp -r build/NTS build/ZTS
%endif

: Build NTS extension
cd build/NTS
%{_bindir}/phpize
peclconf %{_bindir}/php-config
make %{?_smp_mflags}

%if %{with_zts}
: Build ZTS extension
cd ../ZTS
%{_bindir}/zts-phpize
peclconf %{_bindir}/zts-php-config
make %{?_smp_mflags}
%endif


%install
rm -rf %{buildroot}

make -C build/NTS install INSTALL_ROOT=%{buildroot}

# install config file
install -Dpm644 %{ini_name} %{buildroot}%{php_inidir}/%{ini_name}

%if %{with_zts}
make -C build/ZTS install INSTALL_ROOT=%{buildroot}
install -Dpm644 %{ini_name} %{buildroot}%{php_ztsinidir}/%{ini_name}
%endif


%check
# Shared needed extensions
modules=""
for mod in json pdo; do
  if [ -f %{php_extdir}/${mod}.so ]; then
    modules="$modules -d extension=${mod}.so"
  fi
done

: Minimal load test for NTS extension
%{__php} --no-php-ini \
    $modules \
    --define extension=%{buildroot}%{php_extdir}/%{ext_name}.so \
    --modules | grep -i %{ext_name}

%if %{with_tests}
: Upstream test suite NTS extension
cd build/NTS
SKIP_ONLINE_TESTS=1 \
TEST_PHP_EXECUTABLE=%{__php} \
TEST_PHP_ARGS="-n $modules -d extension=$PWD/modules/%{ext_name}.so" \
NO_INTERACTION=1 \
REPORT_EXIT_STATUS=1 \
%{__php} -n run-tests.php --show-diff
%endif

%if %{with_zts}
: Minimal load test for ZTS extension
%{__ztsphp} --no-php-ini \
    $modules \
    --define extension=%{buildroot}%{php_ztsextdir}/%{ext_name}.so \
    --modules | grep -i %{ext_name}
%endif


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license docs/LICENSE.md
%doc CHANGELOG.md
%doc CONTRIBUTING.md
%doc docs/DOCUMENTATION.md

%config(noreplace) %{php_inidir}/%{ini_name}
%{php_extdir}/%{ext_name}.so
%exclude %{php_incldir}/ext/%{ext_name}/php_phalcon.h

%if %{with_zts}
%config(noreplace) %{php_ztsinidir}/%{ini_name}
%{php_ztsextdir}/%{ext_name}.so
%exclude %{php_ztsincldir}/ext/%{ext_name}/php_phalcon.h
%endif


%changelog
* Tue Feb 21 2017 Remi Collet <remi@fedoraproject.org> - 3.0.4-1
- update to 3.0.4

* Sun Dec 25 2016 Remi Collet <remi@fedoraproject.org> - 3.0.3-1
- update to 3.0.3

* Sun Nov 27 2016 Remi Collet <remi@fedoraproject.org> - 3.0.2-1
- update to 3.0.2

* Fri Sep  2 2016 Remi Collet <remi@fedoraproject.org> - 3.0.1-1
- update to 3.0.1

* Sat Jul 30 2016 Remi Collet <remi@fedoraproject.org> - 3.0.0-2
- generate sources using zephir

* Sat Jul 30 2016 Remi Collet <remi@fedoraproject.org> - 3.0.0-1
- update to 3.0.0
- rename to php-phalcon3
- PHP 7 build is broken for now
  open https://github.com/phalcon/cphalcon/issues/12054

* Fri May 20 2016 Remi Collet <remi@fedoraproject.org> - 2.0.13-1
- update to 2.0.13

* Tue May 17 2016 Remi Collet <remi@fedoraproject.org> - 2.0.12-1
- update to 2.0.12

* Thu May  5 2016 Remi Collet <remi@fedoraproject.org> - 2.0.11-1
- update to 2.0.11

* Sun Feb  7 2016 Remi Collet <remi@fedoraproject.org> - 2.0.10-1
- update to 2.0.10

* Wed Nov 25 2015 Remi Collet <remi@fedoraproject.org> - 2.0.9-1
- update to 2.0.9

* Sat Sep 26 2015 Remi Collet <remi@fedoraproject.org> - 2.0.8-1
- update to 2.0.8
- allow build against rh-php56 (as more-php56)

* Fri Aug 21 2015 Remi Collet <remi@fedoraproject.org> - 2.0.7-1
- update to 2.0.7

* Wed Jul 22 2015 Remi Collet <remi@fedoraproject.org> - 2.0.6-1
- update to 2.0.6

* Wed Jul 15 2015 Remi Collet <remi@fedoraproject.org> - 2.0.5-1
- update to 2.0.5

* Mon Jul 13 2015 Remi Collet <remi@fedoraproject.org> - 2.0.4-1
- update to 2.0.4

* Thu Jun 11 2015 Remi Collet <remi@fedoraproject.org> - 2.0.3-1
- update to 2.0.3

* Tue May 26 2015 Remi Collet <remi@fedoraproject.org> - 2.0.2-1
- update to 2.0.2

* Thu May 14 2015 Remi Collet <remi@fedoraproject.org> - 2.0.1-1
- update to 2.0.1

* Tue Apr 21 2015 Remi Collet <remi@fedoraproject.org> - 2.0.0-1
- update to 2.0.0
- rename to php-phalcon2

* Wed Dec 24 2014 Remi Collet <remi@fedoraproject.org> - 1.3.4-1.1
- Fedora 21 SCL mass rebuild

* Sat Nov 15 2014 Remi Collet <remi@fedoraproject.org> - 1.3.4-1
- update to 1.3.4

* Mon Sep 29 2014 Remi Collet <remi@fedoraproject.org> - 1.3.3-1
- update to 1.3.3
- drop all patches merged upstream

* Sun Sep  7 2014 Remi Collet <remi@fedoraproject.org> - 1.3.2-2
- use striped archive, without non-free sources
- generate and use optimized sources
- open https://github.com/phalcon/cphalcon/pull/2793

* Thu Sep  4 2014 Remi Collet <remi@fedoraproject.org> - 1.3.2-1
- initial package, version 1.3.2
- open https://github.com/phalcon/cphalcon/pull/2772 (merged)
- open https://github.com/phalcon/cphalcon/pull/2774
- open https://github.com/phalcon/cphalcon/pull/2775
