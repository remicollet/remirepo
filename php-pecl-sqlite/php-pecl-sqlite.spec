%{!?__pecl:  %{expand: %%global __pecl     %{_bindir}/pecl}}

%global pecl_name   sqlite
%global svnver      313074
%global extver      2.0-dev

Name:           php-pecl-sqlite
Version:        2.0.0
Release:        0.1.svn%{svnver}%{?dist}
Summary:        Extension for the SQLite V2 Embeddable SQL Database Engine
Group:          Development/Languages
License:        PHP
URL:            http://pecl.php.net/package/%{pecl_name}
%if 0%{?svnver}
# svn export -r 313074 https://svn.php.net/repository/pecl/sqlite/trunk sqlite
# tar czf sqlite-svn313074.tgz sqlite
Source0:        sqlite-svn%{svnver}.tgz
%else
Source0:        http://pecl.php.net/get/%{pecl_name}-%{version}.tgz
%endif

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  php-devel >= 5.4.0
BuildRequires:  php-pear >= 1:1.4.0

Requires:       php(zend-abi) = %{php_zend_api}
Requires:       php(api) = %{php_core_api}
Requires(post): %{__pecl}
Requires(postun): %{__pecl}
Provides: php-pecl(%{pecl_name}) = %{extver}
# Was provided by php until 5.4.0
Obsoletes:      php-sqlite < 5.4.0
Provides:       php-sqlite = 5.4.0
Provides:       php-sqlite%{?_isa} = 5.4.0
Obsoletes:      php-sqlite2 < 5.4.0
Provides:       php-sqlite2 = 5.4.0
Provides:       php-sqlite2%{?_isa} = 5.4.0

# RPM 4.8
%{?filter_provides_in: %filter_provides_in %{php_extdir}/.*\.so$}
%{?filter_provides_in: %filter_provides_in %{php_ztsextdir}/.*\.so$}
%{?filter_setup}
# RPM 4.9
%global __provides_exclude_from %{?__provides_exclude_from:%__provides_exclude_from|}%{php_extdir}/.*\\.so$
%global __provides_exclude_from %__provides_exclude_from|%{php_ztsextdir}/.*\\.so$


%description
This is an extension for the SQLite 2 Embeddable SQL Database Engine.
http://www.sqlite.org/

SQLite is a C library that implements an embeddable SQL database engine.
Programs that link with the SQLite library can have SQL database access
without running a separate RDBMS process.

SQLite is not a client library used to connect to a big database server.
SQLite is the server. The SQLite library reads and writes directly to and from
the database files on disk


%package devel
Summary:       PHP SQLite V2 developer files (header)
Group:         Development/Libraries
Requires:      php-pecl-sqlite%{?_isa} = %{version}-%{release}
Requires:      php-devel%{?_isa} >= 5.4.0

%description devel
These are the files needed to compile programs using PHP SQLite V2.


%prep
%setup -c -q

%if 0%{?svnver}
mv %{pecl_name}/package.xml .
mv %{pecl_name} %{pecl_name}-%{version}
# fix package release state (stability)
sed -i \
 -e '/<release>stable/s/stable/beta/' \
 package.xml
%endif

# Check version
extver=$(sed -n '/#define PHP_SQLITE_MODULE_VERSION/{s/.*\t"//;s/".*$//;p}' %{pecl_name}-%{version}/sqlite.c)
if test "x${extver}" != "x%{extver}"; then
   : Error: Upstream version is ${extver}, expecting %{version}.
   exit 1
fi

cat >%{pecl_name}.ini << 'EOF'
; Enable %{pecl_name} extension module
extension=%{pecl_name}.so
EOF

cp -pr %{pecl_name}-%{version} %{pecl_name}-zts


%build
cd %{pecl_name}-%{version}
%{php_bindir}/phpize
%configure \
    --with-php-config=%{php_bindir}/php-config
make %{?_smp_mflags}

cd ../%{pecl_name}-zts
%{php_ztsbindir}/phpize
%configure \
    --with-php-config=%{php_ztsbindir}/php-config
make %{?_smp_mflags}


%install
rm -rf %{buildroot}
make install -C %{pecl_name}-%{version} INSTALL_ROOT=%{buildroot}
make install -C %{pecl_name}-zts        INSTALL_ROOT=%{buildroot}

# Drop in the bit of configuration
install -D -m 644 %{pecl_name}.ini %{buildroot}%{php_inidir}/%{pecl_name}.ini
install -D -m 644 %{pecl_name}.ini %{buildroot}%{php_ztsinidir}/%{pecl_name}.ini

# Install XML package description
install -D -m 644 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml

%check
cd %{pecl_name}-%{version}

TEST_PHP_EXECUTABLE=%{__php} \
REPORT_EXIT_STATUS=1 \
NO_INTERACTION=1 \
%{__php} run-tests.php \
    -n -q \
    -d extension_dir=modules \
    -d extension=%{pecl_name}.so \


%clean
rm -rf %{buildroot}


%post
%{pecl_install} %{pecl_xmldir}/%{name}.xml >/dev/null || :


%postun
if [ $1 -eq 0 ]  ; then
   %{pecl_uninstall} %{pecl_name} >/dev/null || :
fi


%files
%defattr(-,root,root,-)
%doc %{pecl_name}-%{version}/CREDITS
%config(noreplace) %{php_inidir}/%{pecl_name}.ini
%config(noreplace) %{php_ztsinidir}/%{pecl_name}.ini
%{php_extdir}/%{pecl_name}.so
%{php_ztsextdir}/%{pecl_name}.so
%{pecl_xmldir}/%{name}.xml

%files devel
%defattr(-,root,root,-)
%{php_incldir}/libsqlite
%{php_ztsincldir}/libsqlite


%changelog
* Sun Nov 27 2011 Remi Collet <RPMS@FamilleCollet.com> - 2.0.0-0.1.svn313074
- initial RPM as pecl extension
