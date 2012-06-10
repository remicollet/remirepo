%{!?__pecl:         %{expand: %%global __pecl %{_bindir}/pecl}}

%global pecl_name xhprof

Name:           php-pecl-xhprof
Version:        0.9.2
Release:        5%{?dist}.1
Summary:        PHP extension for XHProf, a Hierarchical Profiler
Group:          Development/Languages
License:        ASL 2.0
URL:            http://pecl.php.net/package/%{pecl_name}
Source0:        http://pecl.php.net/get/%{pecl_name}-%{version}.tgz

# From github
Patch0:         %{pecl_name}-arginfo.patch
Patch1:         %{pecl_name}-php54.patch

# https://bugs.php.net/61262
ExcludeArch:    ppc64

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  php-devel >= 5.2.0
BuildRequires:  php-pear >= 1:1.4.0

Requires:       php(zend-abi) = %{php_zend_api}
Requires:       php(api) = %{php_core_api}
Requires(post): %{__pecl}
Requires(postun): %{__pecl}
Provides:       php-pecl(%{pecl_name}) = %{version}

# RPM 4.8
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}
# RPM 4.9
%global __provides_exclude_from %{?__provides_exclude_from:%__provides_exclude_from|}%{_libdir}/.*\\.so$


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
extension = xhprof.so

; You can either pass the directory location as an argument to the constructor
; for XHProfRuns_Default() or set xhprof.output_dir ini param.
xhprof.output_dir = /tmp
EOF

# Apache configuration file
cat >httpd.conf <<EOF
Alias /xhprof /usr/share/xhprof/xhprof_html

<Directory /usr/share/xhprof/xhprof_html>
   <IfModule mod_authz_core.c>
      # Apache 2.4
      <RequireAny>
         Require ip 127.0.0.1
         Require ip ::1
      </RequireAny>
   </IfModule>
   <IfModule !mod_authz_core.c>
      # Apache 2.2
      Order Deny,Allow
      Deny from All
      Allow from 127.0.0.1
      Allow from ::1
   </IfModule>
</Directory>
EOF

cd %{pecl_name}-%{version}
%patch0 -p1 -b .refl
%patch1 -p1 -b .php54

%if 0%{?__ztsphp:1}
# duplicate for ZTS build
cp -r extension ext-zts
%endif

# not to be installed
mv xhprof_html/docs ../docs


%build
cd %{pecl_name}-%{version}/extension
%{_bindir}/phpize
%configure \
    --with-php-config=%{_bindir}/php-config
make %{?_smp_mflags}

%if 0%{?__ztsphp:1}
cd ../ext-zts
%{_bindir}/zts-phpize
%configure \
    --with-php-config=%{_bindir}/zts-php-config
make %{?_smp_mflags}
%endif


%install
rm -rf %{buildroot}
make install -C %{pecl_name}-%{version}/extension  INSTALL_ROOT=%{buildroot}
install -D -m 644 %{pecl_name}.ini %{buildroot}%{_sysconfdir}/php.d/%{pecl_name}.ini

%if 0%{?__ztsphp:1}
make install -C %{pecl_name}-%{version}/ext-zts    INSTALL_ROOT=%{buildroot}
install -D -m 644 %{pecl_name}.ini %{buildroot}%{php_ztsinidir}/%{pecl_name}.ini
%endif

# Install XML package description
install -D -m 644 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml

# Install the web interface
install -D -m 644 httpd.conf %{buildroot}%{_sysconfdir}/httpd/conf.d/xhprof.conf

mkdir -p %{buildroot}%{_datadir}/xhprof
cp -pr %{pecl_name}-%{version}/xhprof_html %{buildroot}%{_datadir}/xhprof/xhprof_html
cp -pr %{pecl_name}-%{version}/xhprof_lib  %{buildroot}%{_datadir}/xhprof/xhprof_lib


%check
# simple module load test
php --no-php-ini \
    --define extension_dir=%{pecl_name}-%{version}/extension/modules \
    --define extension=%{pecl_name}.so \
    --modules | grep %{pecl_name}

%if 0%{?__ztsphp:1}
%{__ztsphp} --no-php-ini \
    --define extension_dir=%{pecl_name}-%{version}/ext-zts/modules \
    --define extension=%{pecl_name}.so \
    --modules | grep %{pecl_name}
%endif


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
%config(noreplace) %{_sysconfdir}/php.d/%{pecl_name}.ini
%{php_extdir}/%{pecl_name}.so
%{pecl_xmldir}/%{name}.xml

%if 0%{?__ztsphp:1}
%config(noreplace) %{php_ztsinidir}/%{pecl_name}.ini
%{php_ztsextdir}/%{pecl_name}.so
%endif


%files -n xhprof
%defattr(-,root,root,-)
%doc docs
%config(noreplace) %{_sysconfdir}/httpd/conf.d/xhprof.conf
%{_datadir}/xhprof


%changelog
* Sun May 06 2012 Remi Collet <remi@fedoraproject.org> - 0.9.2-5
- make configuration file compatible with apache 2.2 / 2.4

* Mon Mar 05 2012 Remi Collet <remi@fedoraproject.org> - 0.9.2-4
- rename patches
- install html and lib under /usr/share/xhprof

* Sat Mar 03 2012 Remi Collet <remi@fedoraproject.org> - 0.9.2-3
- prepare for review
- make ZTS build conditionnal (for PHP 5.3)
- add xhprof.output_dir in configuration file
- open https://bugs.php.net/61262 for ppc64

* Thu Mar 01 2012 Remi Collet <RPMS@FamilleCollet.com> - 0.9.2-2
- split web interace in xhprof sub-package

* Thu Mar 01 2012 Remi Collet <RPMS@FamilleCollet.com> - 0.9.2-1
- Initial RPM package

