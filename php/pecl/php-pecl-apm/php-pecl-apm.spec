# remirepo spec file for php-pecl-apm
#
# Copyright (c) 2015-2016 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%if 0%{?scl:1}
%if "%{scl}" == "rh-php56"
%global sub_prefix  more-php56-
%else
%global sub_prefix  %{scl_prefix}
%endif
%scl_package        php-pecl-apm
%else
%global pkg_name    %{name}
%endif

%global gh_commit   c0bd339a94b7fe5da66c6b5ced286345a4b5410f
%global gh_short    %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner    patrickallaert
%global gh_project  php-apm
#global gh_date     20151117
%global pecl_name   apm
%global proj_name   APM
%global with_zts    0%{!?_without_zts:%{?__ztsphp:1}}
%if "%{php_version}" < "5.6"
# after json.ini
%global ini_name    z-%{pecl_name}.ini
%else
# after 40-json.ini
%global ini_name    50-%{pecl_name}.ini
%endif
%if 0%{?fedora} >= 11 || 0%{?rhel} >= 6
%global with_sqlite 1
%else
%global with_sqlite 0
%endif


Name:           %{?sub_prefix}php-pecl-apm
Summary:        Alternative PHP Monitor
Version:        2.1.1
%if 0%{?gh_date:1}
Release:        6.%{gh_date}git%{gh_short}%{?dist}%{!?scl:%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}}
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{pecl_name}-%{version}-%{gh_short}.tar.gz
%else
Release:        1%{?dist}%{!?scl:%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}}
Source0:        http://pecl.php.net/get/%{proj_name}-%{version}.tgz
%endif

# Disable the extension and drivers by default
Patch0:         %{proj_name}-config.patch

License:        PHP
Group:          Development/Languages
URL:            http://pecl.php.net/package/%{proj_name}

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  %{?scl_prefix}php-devel
BuildRequires:  %{?scl_prefix}php-pear
BuildRequires:  %{?scl_prefix}php-json
%if %{with_sqlite}
BuildRequires:  sqlite-devel >= 3.6
%endif
BuildRequires:  mysql-devel
BuildRequires:  zlib-devel

Requires:       %{?scl_prefix}php(zend-abi) = %{php_zend_api}
Requires:       %{?scl_prefix}php(api) = %{php_core_api}
Requires:       %{?scl_prefix}php-json%{?_isa}
%{?_sclreq:Requires: %{?scl_prefix}runtime%{?_sclreq}%{?_isa}}

Provides:       %{?scl_prefix}php-%{pecl_name}               = %{version}
Provides:       %{?scl_prefix}php-%{pecl_name}%{?_isa}       = %{version}
Provides:       %{?scl_prefix}php-pecl(%{proj_name})         = %{version}
Provides:       %{?scl_prefix}php-pecl(%{proj_name})%{?_isa} = %{version}
%if "%{?scl_prefix}" != "%{?sub_prefix}"
Provides:       %{?scl_prefix}php-pecl-%{pecl_name}          = %{version}-%{release}
Provides:       %{?scl_prefix}php-pecl-%{pecl_name}%{?_isa}  = %{version}-%{release}
%endif

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
# Filter shared private
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}
%endif


%description
Monitoring extension for PHP, collects error events and statistics and send
them to one of his drivers:

* StatsD driver sends them to StatsD using UDP.

* Socket driver sends them via UDP or TCP socket using its dedicated protocol.
%if %{with_sqlite}
* SQLite and MariaDB/MySQL drivers are storing those in a database.
%else
* MariaDB/MySQL drivers are storing those in a database.
%endif

NOTICE: the extension is disable, apm.ini configuration file needs to be edited.

The optional %{?scl_prefix}apm-web package provides the web application.

Package built for PHP %(%{__php} -r 'echo PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')%{?scl: as Software Collection (%{scl} by %{?scl_vendor}%{!?scl_vendor:rh})}.


%prep
%setup -qc
%if 0%{?gh_date:1}
mv %{gh_project}-%{gh_commit} NTS
mv NTS/package.xml .
%else
mv %{proj_name}-%{version} NTS
%endif

%{?_licensedir:sed -e '/LICENSE/s/role="doc"/role="src"/' -i package.xml}

cd NTS
%patch0 -p0 -b .rpm
sed -e 's:/var/php/apm/db:%{_localstatedir}/lib/php/apm/db:' -i apm.ini

: Sanity check, really often broken
extver=$(sed -n '/#define PHP_APM_VERSION/{s/.* "//;s/".*$//;p}' php_apm.h)
if test "x${extver}" != "x%{version}"; then
   : Error: Upstream extension version is ${extver}, expecting %{version}.
   exit 1
fi
cd ..

%if %{with_zts}
# duplicate for ZTS build
cp -pr NTS ZTS
%endif


%build
peclconf() {
%configure \
  --enable-apm \
%if %{with_sqlite}
  --with-sqlite3 \
%else
  --without-sqlite3 \
%endif
  --with-mysql \
  --enable-statsd \
  --enable-socket \
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
rm -rf %{buildroot}

# Install the NTS stuff
make -C NTS install INSTALL_ROOT=%{buildroot}
install -D -m 644 NTS/apm.ini %{buildroot}%{php_inidir}/%{ini_name}

%if %{with_zts}
# Install the ZTS stuff
make -C ZTS install INSTALL_ROOT=%{buildroot}
install -D -m 644 ZTS/apm.ini %{buildroot}%{php_ztsinidir}/%{ini_name}
%endif

# Install the package XML file
install -D -m 644 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml

# Default database dir
install -m 700 -d %{buildroot}%{_localstatedir}/lib/php/apm/db

cd NTS
for i in $(grep 'role="doc"' ../package.xml | sed -e 's/^.*name="//;s/".*$//')
do install -Dpm 644 $i %{buildroot}%{pecl_docdir}/%{proj_name}/$i
done


%check
cd NTS

opt="--no-php-ini --define apm.enabled=0"
if [ -f %{php_extdir}/json.so ]; then
  opt="$opt --define extension=json.so"
fi

: Minimal load test for NTS extension
%{__php} $opt \
    --define extension=%{buildroot}%{php_extdir}/%{pecl_name}.so \
    --modules | grep %{pecl_name}

%if %{with_zts}
cd ../ZTS
: Minimal load test for ZTS extension
%{__ztsphp} $opt \
    $dep \
    --define extension=%{buildroot}%{php_ztsextdir}/%{pecl_name}.so \
    --modules | grep %{pecl_name}
%endif


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
    %{pecl_uninstall} %{proj_name} >/dev/null || :
fi
%endif


%files
%defattr(-,root,root,-)
%{?_licensedir:%license NTS/LICENSE}
%doc %{pecl_docdir}/%{proj_name}
%{pecl_xmldir}/%{name}.xml
%dir %attr(0770,root,apache) %dir %{_localstatedir}/lib/php/apm
%dir %attr(0770,root,apache) %dir %{_localstatedir}/lib/php/apm/db

%config(noreplace) %{php_inidir}/%{ini_name}
%{php_extdir}/%{pecl_name}.so

%if %{with_zts}
%{php_ztsextdir}/%{pecl_name}.so
%config(noreplace) %{php_ztsinidir}/%{ini_name}
%endif


%changelog
* Tue Mar 29 2016 Remi Collet <remi@fedoraproject.org> - 2.1.1-1
- Update to 2.1.1 (no change, only patch merged upstream)

* Tue Mar 29 2016 Remi Collet <remi@fedoraproject.org> - 2.1.0-1
- Update to 2.1.0
- add patch to fix ZTS build
  open https://github.com/patrickallaert/php-apm/pull/38

* Sat Mar  5 2016 Remi Collet <remi@fedoraproject.org> - 2.0.5-6.20151117gitc0bd339
- refresh and adapt for F24

* Tue Oct 13 2015 Remi Collet <remi@fedoraproject.org> - 2.0.5-5.20150807gitd08a589
- rebuild for PHP 7.0.0RC5 new API version

* Fri Sep 18 2015 Remi Collet <remi@fedoraproject.org> - 2.0.5-4.20150807gitd08a589
- F23 rebuild with rh_layout

* Fri Aug  7 2015 Remi Collet <rcollet@redhat.com> - 2.0.5-3.20150807gitd08a589
- sources from github
- git snapshot for php 7

* Tue Jun 23 2015 Remi Collet <rcollet@redhat.com> - 2.0.5-2
- allow build against rh-php56 (as more-php56)

* Wed Jun 17 2015 Remi Collet <remi@fedoraproject.org> - 2.0.5-1
- Update to 2.0.5 (stable)

* Tue Jun 02 2015 Remi Collet <remi@fedoraproject.org> - 2.0.4-1
- Update to 2.0.4 (stable)

* Mon May 18 2015 Remi Collet <remi@fedoraproject.org> - 2.0.3-1
- Update to 2.0.3 (stable)
- drop runtime dependency on pear, new scriptlets
- provide /var/lib/php/apm/db directory

* Tue Mar 10 2015 Remi Collet <remi@fedoraproject.org> - 2.0.2-2
- upstream patches
- fix provided configuration

* Tue Mar 10 2015 Remi Collet <remi@fedoraproject.org> - 2.0.2-1
- Update to 2.0.2 (stable)
- drop sub package, apm-web is now a separate project
- enable ZTS extension

* Sat Feb 21 2015 Remi Collet <remi@fedoraproject.org> - 2.0.0-2
- add missing dependencies
- drop dependency between extension and webapp
- move configuration to /etc/apm-web
- fix permission of configuration file

* Sat Feb 21 2015 Remi Collet <remi@fedoraproject.org> - 2.0.0-1
- initial package, version 2.0.0 (stable)
- open upstream bugs:
  https://github.com/patrickallaert/php-apm/issues/10 - configure
  https://github.com/patrickallaert/php-apm/issues/11 - bad version
  https://github.com/patrickallaert/php-apm/issues/12 - bad roles
  https://github.com/patrickallaert/php-apm/issues/13 - zts broken

