# remirepo spec file for php-pecl-xhprof
# with SCL compatibility
#
# Fedora spec file for php-pecl-xhprof
#
# Copyright (c) 2012-2016 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%if 0%{?scl:1}
%if "%{scl}" == "rh-php56"
%global sub_prefix more-php56-
%else
%global sub_prefix %{scl_prefix}
%endif
%endif

%{?scl:          %scl_package             php-pecl-xhprof}
%{!?scl:         %global _root_bindir     %{_bindir}}
%{!?scl:         %global _root_sysconfdir %{_sysconfdir}}

%global pecl_name xhprof
%global with_zts  0%{?__ztsphp:1}
%if "%{php_version}" < "5.6"
%global ini_name  %{pecl_name}.ini
%else
%global ini_name  40-%{pecl_name}.ini
%endif

Name:           %{?sub_prefix}php-pecl-xhprof
Version:        0.9.4
Release:        7%{?dist}%{!?scl:%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}}

Summary:        PHP extension for XHProf, a Hierarchical Profiler
Group:          Development/Languages
License:        ASL 2.0
URL:            http://pecl.php.net/package/%{pecl_name}
Source0:        http://pecl.php.net/get/%{pecl_name}-%{version}.tgz

# https://bugs.php.net/61262
ExclusiveArch:  %{ix86} x86_64

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  %{?scl_prefix}php-devel >= 5.2.0
BuildRequires:  %{?scl_prefix}php-pear

Requires:       %{?scl_prefix}php(zend-abi) = %{php_zend_api}
Requires:       %{?scl_prefix}php(api) = %{php_core_api}
%{?_sclreq:Requires: %{?scl_prefix}runtime%{?_sclreq}%{?_isa}}

Provides:       %{?scl_prefix}php-%{pecl_name}               = %{version}
Provides:       %{?scl_prefix}php-%{pecl_name}%{?_isa}       = %{version}
Provides:       %{?scl_prefix}php-pecl(%{pecl_name})         = %{version}
Provides:       %{?scl_prefix}php-pecl(%{pecl_name})%{?_isa} = %{version}
Provides:       %{?scl_prefix}php-pecl-%{pecl_name}          = %{version}-%{release}
Provides:       %{?scl_prefix}php-pecl-%{pecl_name}%{?_isa}  = %{version}-%{release}

%if "%{?vendor}" == "Remi Collet" && 0%{!?scl:1} && 0%{?rhel}
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
# Filter private shared object
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}
%endif


%description
XHProf is a function-level hierarchical profiler for PHP.

This package provides the raw data collection component,
implemented in C (as a PHP extension).

The HTML based navigational interface is provided in the "xhprof" package.

Package built for PHP %(%{__php} -r 'echo PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')%{?scl: as Software Collection (%{scl} by %{?scl_vendor}%{!?scl_vendor:rh})}.


%package -n %{?sub_prefix}xhprof
Summary:       A Hierarchical Profiler for PHP - Web interface
Group:         Development/Tools
%if 0%{?fedora} > 11 || 0%{?rhel} > 5
BuildArch:     noarch
%endif

Requires:      %{name} = %{version}-%{release}
Requires:      %{?scl_prefix}mod_php >= 5.2.0
Requires:      %{_root_bindir}/dot

%description -n %{?sub_prefix}xhprof
XHProf is a function-level hierarchical profiler for PHP and has a simple HTML
based navigational interface.

The raw data collection component, implemented in C (as a PHP extension,
provided by the "php-pecl-xhprof" package).

The reporting/UI layer is all in PHP. It is capable of reporting function-level
inclusive and exclusive wall times, memory usage, CPU times and number of calls
for each function.

Additionally, it supports ability to compare two runs (hierarchical DIFF
reports), or aggregate results from multiple runs.

Documentation: %{pecl_docdir}/%{pecl_name}/xhprof_html/docs/index.html


%prep
%setup -c -q

# Mark "php" files as "src" to avoid registration in pear file list
# xhprof_html should be web, but www_dir is /var/www/html
# xhprof_lib  should be php, really a lib
sed -e 's/role="php"/role="src"/' \
    %{?_licensedir:-e '/LICENSE/s/role="doc"/role="src"/' } \
    -i package.xml

# Extension configuration file
cat >%{ini_name} <<EOF
; Enable %{pecl_name} extension module
extension = xhprof.so

; You can either pass the directory location as an argument to the constructor
; for XHProfRuns_Default() or set xhprof.output_dir ini param.
xhprof.output_dir = /tmp
EOF

# Apache configuration file
cat >httpd.conf <<EOF
Alias /xhprof %{_datadir}/xhprof/xhprof_html

<Directory %{_datadir}/xhprof/xhprof_html>
   # For security reason, the web interface
   # is only allowed from the server
   <IfModule mod_authz_core.c>
      # Apache 2.4
      Require local
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

%if %{with_zts}
# duplicate for ZTS build
cp -r extension ext-zts
%endif


%build
cd %{pecl_name}-%{version}/extension
%{_bindir}/phpize
%configure \
    --with-php-config=%{_bindir}/php-config
make %{?_smp_mflags}

%if %{with_zts}
cd ../ext-zts
%{_bindir}/zts-phpize
%configure \
    --with-php-config=%{_bindir}/zts-php-config
make %{?_smp_mflags}
%endif


%install
rm -rf %{buildroot}
make install -C %{pecl_name}-%{version}/extension  INSTALL_ROOT=%{buildroot}
install -D -m 644 %{ini_name} %{buildroot}%{php_inidir}/%{ini_name}

%if %{with_zts}
make install -C %{pecl_name}-%{version}/ext-zts    INSTALL_ROOT=%{buildroot}
install -D -m 644 %{ini_name} %{buildroot}%{php_ztsinidir}/%{ini_name}
%endif

# Install XML package description
install -D -m 644 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml

# Install the Apache configuration
install -D -m 644 httpd.conf %{buildroot}%{_root_sysconfdir}/httpd/conf.d/%{?scl_prefix}xhprof.conf

# Install the web interface
mkdir -p %{buildroot}%{_datadir}/xhprof
cp -pr %{pecl_name}-%{version}/xhprof_html %{buildroot}%{_datadir}/xhprof/xhprof_html
cp -pr %{pecl_name}-%{version}/xhprof_lib  %{buildroot}%{_datadir}/xhprof/xhprof_lib
rm -r %{buildroot}%{_datadir}/xhprof/xhprof_html/docs

# Test & Documentation
cd %{pecl_name}-%{version}
for i in $(grep 'role="test"' ../package.xml | sed -e 's/^.*name="//;s/".*$//')
do install -Dpm 644 $i %{buildroot}%{pecl_testdir}/%{pecl_name}/$i
done
for i in $(grep 'role="doc"' ../package.xml | sed -e 's/^.*name="//;s/".*$//')
do install -Dpm 644 $i %{buildroot}%{pecl_docdir}/%{pecl_name}/$i
done


%check
: simple module load TEST for NTS extension
%{__php} --no-php-ini \
    --define extension=%{buildroot}%{php_extdir}/%{pecl_name}.so \
    --modules | grep %{pecl_name}

%if %{with_zts}
: simple module load TEST for ZTS extension
%{__ztsphp} --no-php-ini \
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
    %{pecl_uninstall} %{pecl_name} >/dev/null || :
fi
%endif


%files
%defattr(-,root,root,-)
%{?_licensedir:%license %{pecl_name}-%{version}/LICENSE}
%doc %{pecl_docdir}/%{pecl_name}
%exclude %{pecl_docdir}/%{pecl_name}/examples
%exclude %{pecl_docdir}/%{pecl_name}/xhprof_html
%{pecl_xmldir}/%{name}.xml

%config(noreplace) %{php_inidir}/%{ini_name}
%{php_extdir}/%{pecl_name}.so

%if %{with_zts}
%config(noreplace) %{php_ztsinidir}/%{ini_name}
%{php_ztsextdir}/%{pecl_name}.so
%endif


%files -n %{?sub_prefix}xhprof
%defattr(-,root,root,-)
%doc %{pecl_docdir}/%{pecl_name}/examples
%doc %{pecl_docdir}/%{pecl_name}/xhprof_html
%doc %{pecl_testdir}/%{pecl_name}
%config(noreplace) %{_root_sysconfdir}/httpd/conf.d/%{?scl_prefix}xhprof.conf
%{_datadir}/xhprof


%changelog
* Wed Mar  9 2016 Remi Collet <remi@fedoraproject.org> - 0.9.4-7
- adapt for F24

* Tue Jun 23 2015 Remi Collet <remi@fedoraproject.org> - 0.9.4-6
- allow build against rh-php56 (as more-php56)
- drop runtime dependency on pear, new scriptlets

* Wed Dec 24 2014 Remi Collet <remi@fedoraproject.org> - 0.9.4-5.1
- Fedora 21 SCL mass rebuild

* Mon Aug 25 2014 Remi Collet <rcollet@redhat.com> - 0.9.4-5
- improve SCL build

* Thu Apr 17 2014 Remi Collet <remi@fedoraproject.org> - 0.9.4-4
- add numerical prefix to extension configuration file (php 5.6)

* Wed Mar 19 2014 Remi Collet <rcollet@redhat.com> - 0.9.4-3
- allow SCL build

* Sat Mar 15 2014 Remi Collet <remi@fedoraproject.org> - 0.9.4-2
- install doc in pecl_docdir
- install test in pecl_testdir

* Tue Oct  1 2013 Remi Collet <remi@fedoraproject.org> - 0.9.4-1
- update to 0.9.4

* Tue Aug 6 2013 Remi Collet <remi@fedoraproject.org> - 0.9.3-3
- fix doc path in package description #994038

* Mon May 20 2013 Remi Collet <remi@fedoraproject.org> - 0.9.3-1
- update to 0.9.3

* Fri Jan  4 2013 Remi Collet <remi@fedoraproject.org> - 0.9.2-8.gitb8c76ac5ab
- git snapshot + php 5.5 fix
  https://github.com/facebook/xhprof/pull/15
- also provides php-xhprof
- cleanups

* Tue May 22 2012 Remi Collet <remi@fedoraproject.org> - 0.9.2-6
- move from ExcludeArch: ppc64
  to ExclusiveArch: %%{ix86} x86_64 because of cycle_timer()

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

