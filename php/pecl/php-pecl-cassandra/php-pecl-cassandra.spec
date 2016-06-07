# remirepo spec file for php-pecl-cassandra
#
# Copyright (c) 2015-2016 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please preserve changelog entries
#
%if 0%{?scl:1}
%if "%{scl}" == "rh-php56"
%global sub_prefix more-php56-
%else
%global sub_prefix %{scl_prefix}
%endif
%endif

%{?scl:          %scl_package        php-pecl-cassandra}

%global pecl_name   cassandra
%global with_zts    0%{!?_without_zts:%{?__ztsphp:1}}
#global prever      RC
# see https://github.com/datastax/php-driver/releases
#global gh_commit   2b0642b1d6fc451f0481edaf0163e3e5bbf896ec
#global gh_short    %%(c=%%{gh_commit}; echo ${c:0:7})
%global gh_owner    datastax
%global gh_project  php-driver
%global with_tests  0%{!?_without_zts:%{?__ztsphp:1}}
%if "%{php_version}" < "5.6"
%global ini_name    %{pecl_name}.ini
%else
%global ini_name    40-%{pecl_name}.ini
%endif

# We don't really rely on upstream ABI
%global buildver %(pkg-config --silence-errors --modversion cassandra 2>/dev/null || echo 65536)

Summary:      DataStax PHP Driver for Apache Cassandra
Name:         %{?sub_prefix}php-pecl-%{pecl_name}
Version:      1.1.0
Release:      1%{?dist}%{!?scl:%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}}
License:      ASL 2.0
Group:        Development/Languages
URL:          http://pecl.php.net/package/%{pecl_name}

# Pull sources from github to get tests
%if 0%{?gh_commit:1}
Source0:      https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}%{?prever}.tar.gz
%else
Source:       http://pecl.php.net/get/%{pecl_name}-%{version}%{?prever}.tgz
%endif

BuildRoot:    %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
# Upstream recommends php >= 5.5
BuildRequires: %{?scl_prefix}php-devel
BuildRequires: %{?scl_prefix}php-pear
BuildRequires: cassandra-cpp-driver-devel
BuildRequires: libuv-devel
BuildRequires: gmp-devel

Requires:     cassandra-cpp-driver-devel%{?_isa}  >= %{buildver}
Requires:     %{?scl_prefix}php(zend-abi) = %{php_zend_api}
Requires:     %{?scl_prefix}php(api) = %{php_core_api}
%{?_sclreq:Requires: %{?scl_prefix}runtime%{?_sclreq}%{?_isa}}

Provides:     %{?scl_prefix}php-%{pecl_name} = %{version}
Provides:     %{?scl_prefix}php-%{pecl_name}%{?_isa} = %{version}
Provides:     %{?scl_prefix}php-pecl(%{pecl_name}) = %{version}
Provides:     %{?scl_prefix}php-pecl(%{pecl_name})%{?_isa} = %{version}
Provides:     %{?scl_prefix}php-pecl-%{pecl_name} = %{version}-%{release}
Provides:     %{?scl_prefix}php-pecl-%{pecl_name}%{?_isa} = %{version}-%{release}

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
%if "%{php_version}" > "7.0"
Obsoletes:     php70u-pecl-%{pecl_name} <= %{version}
Obsoletes:     php70w-pecl-%{pecl_name} <= %{version}
%endif
%endif

%if 0%{?fedora} < 20 && 0%{?rhel} < 7
# Filter private shared provides
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}
%endif


%description
A modern, feature-rich and highly tunable PHP client library for Apache
Cassandra and DataStax Enterprise using exclusively Cassandra's binary
protocol and Cassandra Query Language v3.

Package built for PHP %(%{__php} -r 'echo PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')%{?scl: as Software Collection (%{scl} by %{?scl_vendor}%{!?scl_vendor:rh})}.


%prep
%setup -c -q
%if 0%{?gh_commit:1}
mv %{gh_project}-%{gh_commit}/ext NTS
mv NTS/package.xml .
%else
mv %{pecl_name}-%{version}%{?prever} NTS
%endif

# Don't install/register tests
sed -e 's/role="test"/role="src"/' \
    %{?_licensedir:-e '/LICENSE/s/role="doc"/role="src"/' } \
    -i package.xml

cd NTS
# Sanity check, really often broken
extver=$(sed -n '/#define PHP_CASSANDRA_VERSION /{s/.* "//;s/".*$//;p}' version.h)
if test "x${extver}" != "x%{version}%{?prever}"; then
   : Error: Upstream extension version is ${extver}, expecting %{version}%{?prever}.
   exit 1
fi
cd ..

cat << 'EOF' | tee %{ini_name}
; Enable '%{summary}' extension module
extension=%{pecl_name}.so

; Configuration
;cassandra.log = 'cassandra.log'
;cassandra.log_level = 'ERROR'
EOF

%if %{with_zts}
cp -pr NTS ZTS
%endif


%build
cd NTS
%{_bindir}/phpize
%configure  \
  --with-cassandra \
  --with-php-config=%{_bindir}/php-config
make %{?_smp_mflags}

%if %{with_zts}
cd ../ZTS
%{_bindir}/zts-phpize
%configure  \
  --with-cassandra \
  --with-php-config=%{_bindir}/zts-php-config
make %{?_smp_mflags}
%endif


%install
rm -rf %{buildroot}

make -C NTS install INSTALL_ROOT=%{buildroot}

# Drop in the bit of configuration
install -D -m 644 %{ini_name} %{buildroot}%{php_inidir}/%{ini_name}

# Install XML package description
install -D -m 644 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml

%if %{with_zts}
make -C ZTS install INSTALL_ROOT=%{buildroot}
install -D -m 644 %{ini_name} %{buildroot}%{php_ztsinidir}/%{ini_name}
%endif

# Documentation
for i in $(grep 'role="doc"' package.xml | sed -e 's/^.*name="//;s/".*$//')
do install -Dpm 644 NTS/$i %{buildroot}%{pecl_docdir}/%{pecl_name}/$i
done


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


%check
: Minimal load test for NTS extension
%{__php} -n \
    -d extension=%{buildroot}%{php_extdir}/%{pecl_name}.so \
    -m | grep %{pecl_name}

%if %{with_tests}
cd NTS
: Upstream test suite NTS extension
TEST_PHP_EXECUTABLE=%{__php} \
TEST_PHP_ARGS="-n -d extension=$PWD/modules/%{pecl_name}.so" \
NO_INTERACTION=1 \
REPORT_EXIT_STATUS=1 \
%{__php} -n run-tests.php --show-diff
%endif

%if %{with_zts}
: Minimal load test for ZTS extension
%{__ztsphp} -n \
    -d extension=%{buildroot}%{php_ztsextdir}/%{pecl_name}.so \
    -m | grep %{pecl_name}

%if %{with_tests}
cd ../ZTS
: Upstream test suite ZTS extension
TEST_PHP_EXECUTABLE=%{__ztsphp} \
TEST_PHP_ARGS="-n -d extension=$PWD/modules/%{pecl_name}.so" \
NO_INTERACTION=1 \
REPORT_EXIT_STATUS=1 \
%{__ztsphp} -n run-tests.php --show-diff
%endif
%endif


%files
%defattr(-, root, root, -)
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
* Fri Feb 12 2016 Remi Collet <remi@fedoraproject.org> - 1.1.0-1
- Update to 1.1.0

* Thu Nov 26 2015 Remi Collet <remi@fedoraproject.org> - 1.0.1-1
- Update to 1.0.1

* Tue Sep 15 2015 Remi Collet <remi@fedoraproject.org> - 1.0.0-1
- update to 1.0.0 (stable)

* Thu Aug 13 2015 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.2.RC
- fix package name for more-php56

* Thu Aug 13 2015 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.1.RC
- Initial package, version 1.0.0RC
