%{!?__pecl:  %{expand: %%global __pecl %{_bindir}/pecl}}

%define pecl_name xhprof

Name:           php-pecl-xhprof
Version:        0.9.2
Release:        2%{?dist}
Summary:        PHP extension for XHProf, a Hierarchical Profiler
Group:          Development/Languages
License:        ASL 2.0
URL:            http://pecl.php.net/package/%{pecl_name}
Source0:        http://pecl.php.net/get/%{pecl_name}-%{version}.tgz

# From github
Patch0:         0b3d4054d86b5a52d258623be1497c0c1c3f9a54.patch
Patch1:         a6bae51236677d95cb329d5b20806465c0260394.patch


BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  php-devel >= 5.2.0
BuildRequires:  php-pear >= 1:1.4.0

Requires:       php(zend-abi) = %{php_zend_api}
Requires:       php(api) = %{php_core_api}
Requires(post): %{__pecl}
Requires(postun): %{__pecl}
Provides:       php-pecl(%{pecl_name}) = %{version}

# RPM 4.8
%{?filter_provides_in: %filter_provides_in %{php_extdir}/.*\.so$}
%{?filter_provides_in: %filter_provides_in %{php_ztsextdir}/.*\.so$}
%{?filter_setup}
# RPM 4.9
%global __provides_exclude_from %{?__provides_exclude_from:%__provides_exclude_from|}%{php_extdir}/.*\\.so$
%global __provides_exclude_from %__provides_exclude_from|%{php_ztsextdir}/.*\\.so$


%description
XHProf is a function-level hierarchical profiler for PHP.

This package provides the raw data collection component,
implemented in C (as a PHP extension).

The HTML based navigational interface is provided in the "xhprof" package.


%package -n xhprof
Summary:       A Hierarchical Profiler for PHP - Web interface
Group:         Development/Tools
%if 0%{?fedora} > 11 || 0%{?rhel} > 5
BuildArch:     noarch
%endif

Requires:      php-pecl-xhprof = %{version}-%{release}
Requires:      php >= 5.2.0
Requires:      %{_bindir}/dot

%description -n xhprof
XHProf is a function-level hierarchical profiler for PHP and has a simple HTML
based navigational interface.

The raw data collection component, implemented in C (as a PHP extension,
provided by the "php-pecl-xhprof" package).

The reporting/UI layer is all in PHP. It is capable of reporting function-level
inclusive and exclusive wall times, memory usage, CPU times and number of calls
for each function.

Additionally, it supports ability to compare two runs (hierarchical DIFF
reports), or aggregate results from multiple runs.

Documentation : %{_datadir}/doc/%{name}-%{version}/docs/index.html


%prep
%setup -c -q

# Extension configuration file
cat >%{pecl_name}.ini <<EOF
; Enable %{pecl_name} extension module
extension=xhprof.so
EOF

# Apache configuration file
cat >httpd.conf <<EOF
Alias /xhprof /usr/share/xhprof_html
<Directory /usr/share/xhprof_html>
   order deny,allow
   deny from all
   allow from 127.0.0.1
   allow from ::1
</Directory>
EOF

cd %{pecl_name}-%{version}
%patch0 -p1 -b .refl
%patch1 -p1 -b .php54

# duplicate for ZTS build
cp -r extension ext-zts

# not to be installed
mv xhprof_html/docs ../docs


%build
cd %{pecl_name}-%{version}/extension
%{_bindir}/phpize
%configure \
    --with-php-config=%{_bindir}/php-config
make %{?_smp_mflags}

cd ../ext-zts
%{_bindir}/zts-phpize
%configure \
    --with-php-config=%{_bindir}/zts-php-config
make %{?_smp_mflags}


%install
rm -rf %{buildroot}
make install -C %{pecl_name}-%{version}/extension  INSTALL_ROOT=%{buildroot}
make install -C %{pecl_name}-%{version}/ext-zts    INSTALL_ROOT=%{buildroot}

# Drop in the bit of configuration
install -D -m 644 %{pecl_name}.ini %{buildroot}%{php_inidir}/%{pecl_name}.ini
install -D -m 644 %{pecl_name}.ini %{buildroot}%{php_ztsinidir}/%{pecl_name}.ini

# Install XML package description
install -D -m 644 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml

# Install the web interface
install -D -m 644 httpd.conf %{buildroot}%{_sysconfdir}/httpd/conf.d/xhprof.conf

mkdir -p %{buildroot}%{_datadir}
cp -pr %{pecl_name}-%{version}/xhprof_html %{buildroot}%{_datadir}/xhprof_html
cp -pr %{pecl_name}-%{version}/xhprof_lib  %{buildroot}%{_datadir}/xhprof_lib


%check
# simple module load test
%{__php} --no-php-ini \
    --define extension_dir=%{pecl_name}-%{version}/extension/modules \
    --define extension=%{pecl_name}.so \
    --modules | grep %{pecl_name}

%{__ztsphp} --no-php-ini \
    --define extension_dir=%{pecl_name}-%{version}/ext-zts/modules \
    --define extension=%{pecl_name}.so \
    --modules | grep %{pecl_name}


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
%doc %{pecl_name}-%{version}/{CHANGELOG,CREDITS,README,LICENSE,examples}
%config(noreplace) %{php_inidir}/%{pecl_name}.ini
%config(noreplace) %{php_ztsinidir}/%{pecl_name}.ini
%{php_extdir}/%{pecl_name}.so
%{php_ztsextdir}/%{pecl_name}.so
%{pecl_xmldir}/%{name}.xml

%files -n xhprof
%defattr(-,root,root,-)
%doc docs
%config(noreplace) %{_sysconfdir}/httpd/conf.d/xhprof.conf
%{_datadir}/xhprof_html
%{_datadir}/xhprof_lib


%changelog
* Thu Feb 01 2012 Remi Collet <RPMS@FamilleCollet.com> - 0.9.2-2
- split web interace in xhprof sub-package

* Thu Feb 01 2012 Remi Collet <RPMS@FamilleCollet.com> - 0.9.2-1
- Initial RPM package

