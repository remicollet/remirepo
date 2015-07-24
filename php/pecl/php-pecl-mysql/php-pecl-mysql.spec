# remirepo spec file for php-pecl-mysql
#
# Copyright (c) 2013-2015 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%if 0%{?scl:1}
%global sub_prefix %{scl_prefix}
%endif

%{?scl:          %scl_package        php-pecl-mysql}
%{!?php_inidir:  %global php_inidir  %{_sysconfdir}/php.d}
%{!?__pecl:      %global __pecl      %{_bindir}/pecl}
%{!?__php:       %global __php       %{_bindir}/php}

%global gh_commit   617e5103743d07435fdfe5cbbe6ad310e610c4b9
%global gh_short    %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner    php
%global gh_project  pecl-database-mysql
%global gh_date     20150703
%global with_zts    0%{?__ztsphp:1}
%global pecl_name   mysql
%global with_tests  %{!?_without_tests:1}%{?_without_tests:0}
# After 40-mysqlnd
%global ini_name    50-%{pecl_name}.ini
%global mysql_sock  %(mysql_config --socket 2>/dev/null || echo /var/lib/mysql/mysql.sock)

Summary:        MySQL database access functions
Name:           %{?sub_prefix}php-pecl-%{pecl_name}
Version:        1.0.0
%if 0%{?gh_date:1}
Release:        0.4.%{gh_date}git%{gh_short}%{?dist}%{!?scl:%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}}
%else
Release:        2%{?dist}%{!?scl:%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}}
%endif

License:        PHP
Group:          Development/Languages
URL:            http://pecl.php.net/package/%{pecl_name}
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{pecl_name}-%{version}-%{gh_short}.tar.gz

Source1:        %{pecl_name}.ini
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  %{?scl_prefix}php-devel > 7
BuildRequires:  %{?scl_prefix}php-mysqlnd
BuildRequires:  %{?scl_prefix}php-pear

Requires:       %{?scl_prefix}php(zend-abi) = %{php_zend_api}
Requires:       %{?scl_prefix}php(api) = %{php_core_api}
%{?_sclreq:Requires: %{?scl_prefix}runtime%{?_sclreq}%{?_isa}}

# Set epoch so provides is > 0:7.0.0 (obsoleted by php-mysqlnd)
Provides:       %{?scl_prefix}php-%{pecl_name} = 1:%{version}
Provides:       %{?scl_prefix}php-%{pecl_name}%{?_isa} = 1:%{version}
Provides:       %{?scl_prefix}php-pecl(%{pecl_name}) = %{version}
Provides:       %{?scl_prefix}php-pecl(%{pecl_name})%{?_isa} = %{version}

%if "%{?vendor}" == "Remi Collet" && 0%{!?scl:1}
# Other third party repo stuff
Obsoletes:     php70u-pecl-%{pecl_name} <= %{version}
Obsoletes:     php70w-pecl-%{pecl_name} <= %{version}
%endif

%if 0%{?fedora} < 20 && 0%{?rhel} < 7
# Filter private shared object
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}
%endif


%description
This extension provides the mysql family of functions that were provided
with PHP 3-5. These functions have been superseded by MySQLi and PDO_MySQL,
which continue to be bundled with PHP 7.

Although it should be possible to use this extension with PHP 7.0, you are
strongly encouraged to port your code to use either MySQLi or PDO_MySQL,
as this extension is not maintained and is available for historical reasons only.

Package built for PHP %(%{__php} -r 'echo PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')%{?scl: as Software Collection (%{scl})}.


%prep
%setup -qc
mv %{gh_project}-%{gh_commit} NTS
mv NTS/package.xml .

# Don't install (register) the tests
sed -e 's/role="test"/role="src"/' -i package.xml

#cd NTS
# Check version as upstream often forget to update this
#extver=$(sed -n '/#define PHP_YAC_VERSION/{s/.* "//;s/".*$//;p}' php_yac.h)
#if test "x${extver}" != "x%{version}%{?prever}%{?gh_date:-dev}"; then
#   : Error: Upstream YAC version is ${extver}, expecting %{version}%{?prever}%{?gh_date:-dev}.
#   exit 1
#fi
#cd ..


%if %{with_zts}
# duplicate for ZTS build
cp -pr NTS ZTS
%endif


%build
peclconf() {
%configure \
    --with-mysql=mysqlnd \
    --with-mysql-sock=%{mysql_sock} \
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
install -D -m 644 %{SOURCE1} %{buildroot}%{php_inidir}/%{ini_name}

# Install XML package description
install -D -m 644 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml

# Install the ZTS stuff
%if %{with_zts}
make -C ZTS install INSTALL_ROOT=%{buildroot}
install -D -m 644 %{SOURCE1} %{buildroot}%{php_ztsinidir}/%{ini_name}
%endif

# Documentation
for i in LICENSE $(grep 'role="doc"' package.xml | sed -e 's/^.*name="//;s/".*$//')
do [ -f NTS/$i ] &&  install -Dpm 644 NTS/$i %{buildroot}%{pecl_docdir}/%{pecl_name}/$i
done


%check
cd NTS

: Minimal load test for NTS extension
%{_bindir}/php --no-php-ini \
    --define extension=mysqlnd.so \
    --define extension=%{buildroot}%{php_extdir}/%{pecl_name}.so \
    --modules | grep '^%{pecl_name}$'

%if %{with_zts}
cd ../ZTS

: Minimal load test for ZTS extension
%{__ztsphp} --no-php-ini \
    --define extension=mysqlnd.so \
    --define extension=%{buildroot}%{php_ztsextdir}/%{pecl_name}.so \
    --modules | grep '^%{pecl_name}$'

%endif


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


%clean
rm -rf %{buildroot}


%files
%defattr(-, root, root, 0755)
%{?_licensedir:%license NTS/LICENSE}
%doc %{pecl_docdir}/%{pecl_name}
%{pecl_xmldir}/%{name}.xml

%config(noreplace) %{php_inidir}/%{ini_name}
%{php_extdir}/%{pecl_name}.so

%if %{with_zts}
%{php_ztsextdir}/%{pecl_name}.so
%config(noreplace) %{php_ztsinidir}/%{ini_name}
%endif


%changelog
* Fri Jul 24 2015 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.4.20150703git617e510
- provide php-mysql 1:1.0.0 > 0:7.0.0 which is obsoleted by php-mysqlnd

* Wed Jul 22 2015 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.3.20150703git617e510
- rebuild against php 7.0.0beta2

* Wed Jul  8 2015 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.2.20150703git617e510
- new snapshot, rebuild against php 7.0.0beta1

* Wed Jun 24 2015 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.1.20150305git01751ce
- initial package, version 1.0.0-dev