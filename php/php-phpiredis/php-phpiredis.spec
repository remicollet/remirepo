# Fedora spec file for php-phpiredis
# Without SCL compatibility stuff, from:
#
# remirepo spec file for php-phpiredis
#
# Copyright (c) 2016 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global gh_commit  981d455034a48bb19db39c578e9c16d889289b99
%global gh_short   %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner   nrk
%global gh_project phpiredis

%global pecl_name  phpiredis
%global with_zts   0%{!?_without_zts:%{?__ztsphp:1}}
%if "%{php_version}" < "5.6"
%global ini_name   %{pecl_name}.ini
%else
%global ini_name   40-%{pecl_name}.ini
%endif
%global with_tests 0%{!?_without_tests:1}

Name:           php-%{pecl_name}
Version:        1.0.0
Release:        2%{?dist}

Summary:        Client extension for Redis

Group:          Development/Languages
License:        BSD
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{pecl_name}-%{version}-%{gh_short}.tar.gz

BuildRequires:  php-devel
BuildRequires:  php-pear
BuildRequires:  hiredis-devel
%if %{with_tests}
BuildRequires:  redis
%endif

Requires:       php(zend-abi) = %{php_zend_api}
Requires:       php(api) = %{php_core_api}

%if 0%{?fedora} < 20 && 0%{?rhel} < 7
# Filter private shared
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}
%endif


%description
Phpiredis is an extension for PHP 5.x and 7.x based on hiredis
that provides a simple and efficient client for Redis and a fast
incremental parser / serializer for the RESP protocol.


%prep
%setup -q -c
mv %{gh_project}-%{gh_commit} NTS

cd NTS
# Check extension version
ver=$(sed -n '/define PHP_PHPIREDIS_VERSION/{s/.* "//;s/".*$//;p}' php_phpiredis.h)
if test "$ver" != "%{version}%{?prever}%{?gh_date:-dev}"; then
   : Error: Upstream VERSION version is ${ver}, expecting %{version}%{?prever}%{?gh_date:-dev}.
   exit 1
fi
cd ..

cat  << 'EOF' | tee %{ini_name}
; Enable %{pecl_name} extension module
extension=%{pecl_name}.so
EOF


%if %{with_zts}
# Duplicate source tree for NTS / ZTS build
cp -pr NTS ZTS
%endif


%build
cd NTS
%{_bindir}/phpize
%configure --with-php-config=%{_bindir}/php-config
make %{?_smp_mflags}

%if %{with_zts}
cd ../ZTS
%{_bindir}/zts-phpize
%configure --with-php-config=%{_bindir}/zts-php-config
make %{?_smp_mflags}
%endif


%install
make -C NTS install INSTALL_ROOT=%{buildroot}

# install configuration
install -Dpm 644 %{ini_name} %{buildroot}%{php_inidir}/%{ini_name}

%if %{with_zts}
make -C ZTS install INSTALL_ROOT=%{buildroot}
install -Dpm 644 %{ini_name} %{buildroot}%{php_ztsinidir}/%{ini_name}
%endif


%check
: Minimal load test for NTS extension
%{__php} --no-php-ini \
    --define extension=%{buildroot}%{php_extdir}/%{pecl_name}.so \
    --modules | grep %{pecl_name}

%if %{with_zts}
: Minimal load test for NTS extension
%{__ztsphp} --no-php-ini \
    --define extension=%{buildroot}%{php_ztsextdir}/%{pecl_name}.so \
    --modules | grep %{pecl_name}
%endif

%if %{with_tests}
: Upstream test suite for NTS extension
pidfile=$PWD/redis.pid
port=$(%{__php} -r 'echo 9000 + PHP_MAJOR_VERSION*100 + PHP_MINOR_VERSION*10 + PHP_INT_SIZE;')
sed -e "/REDIS_PORT/s/6379/$port/" -i ?TS/tests/testsuite_configuration.inc
mkdir -p data

redis-server                   \
    --bind      127.0.0.1      \
    --port      $port          \
    --daemonize yes            \
    --logfile   $PWD/redis.log \
    --dir       $PWD/data      \
    --pidfile   $pidfile

cd NTS
: Upstream test suite for NTS extension
TEST_PHP_EXECUTABLE=%{__php} \
TEST_PHP_ARGS="-n -d extension=%{buildroot}%{php_extdir}/%{pecl_name}.so" \
NO_INTERACTION=1 \
REPORT_EXIT_STATUS=1 \
%{__php} -n run-tests.php --show-diff || ret=1

%if %{with_zts}
cd ../ZTS
: Upstream test suite for ZTS extension
TEST_PHP_EXECUTABLE=%{__ztsphp} \
TEST_PHP_ARGS="-n -d extension=%{buildroot}%{php_ztsextdir}/%{pecl_name}.so" \
NO_INTERACTION=1 \
REPORT_EXIT_STATUS=1 \
%{__ztsphp} -n run-tests.php --show-diff || ret=1
%endif

: Cleanup
if [ -s $pidfile ]; then
   kill $(cat $pidfile)
   sleep 1
fi

exit $ret
%endif


%files
%license NTS/LICENSE
%doc NTS/README.md

%config(noreplace) %{php_inidir}/%{ini_name}
%{php_extdir}/%{pecl_name}.so

%if %{with_zts}
%config(noreplace) %{php_ztsinidir}/%{ini_name}
%{php_ztsextdir}/%{pecl_name}.so
%endif


%changelog
* Sat Nov 26 2016 Remi Collet <remi@fedoraproject.org> - 1.0.0-2
- cleanup for fedora review

* Thu Nov 24 2016 Remi Collet <remi@fedoraproject.org> - 1.0.0-1
- update to 1.0.0 release

* Sun Nov 13 2016 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.2.20160715gita64e3bf
- add minor fix for portability
- add full reflection for all functions
- open https://github.com/nrk/phpiredis/pull/53

* Sat Nov 12 2016 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.1.20160715gita64e3bf
- Initial packaging of 1.0.0-dev

