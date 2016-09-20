# remirepo spec file for php-pecl-gearman
# with SCL compatibility, from:
#
# Fedora spec file for php-pecl-gearman
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please, preserve the changelog entries
#
%if 0%{?scl:1}
%if "%{scl}" == "rh-php56"
%global sub_prefix more-php56-
%else
%global sub_prefix %{scl_prefix}
%endif
%scl_package         php-pecl-gearman
%endif

%global gh_commit   f7ec3cf044f654a3db4c415658941898a6e4d42f
%global gh_short    %(c=%{gh_commit}; echo ${c:0:7})
%global gh_date     20160816
%global gh_owner    wcgallego
%global gh_project  pecl-gearman
%global with_tests  0%{?_with_tests:1}
%global with_zts    0%{!?_without_zts:%{?__ztsphp:1}}
%global pecl_name   gearman
%if "%{php_version}" < "5.6"
%global ini_name  %{pecl_name}.ini
%else
%global ini_name  40-%{pecl_name}.ini
%endif

%global extver 2.0.1
%global libver 1.1.0


Name:           %{?sub_prefix}php-pecl-gearman
Version:        %{extver}
Release:        1%{?dist}%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}
Summary:        PHP wrapper to libgearman

Group:          Development/Tools
License:        PHP
URL:            http://gearman.org
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{pecl_name}-%{version}%{?prever}-%{gh_short}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  libgearman-devel > %{libver}
BuildRequires:  %{?scl_prefix}php-devel
BuildRequires:  %{?scl_prefix}php-pear
# Required by phpize
BuildRequires:  autoconf, automake, libtool

Requires:       %{?scl_prefix}php(zend-abi) = %{php_zend_api}
Requires:       %{?scl_prefix}php(api) = %{php_core_api}
%{?_sclreq:Requires: %{?scl_prefix}runtime%{?_sclreq}%{?_isa}}

Provides:       %{?scl_prefix}php-%{pecl_name}               = %{version}
Provides:       %{?scl_prefix}php-%{pecl_name}%{?_isa}       = %{version}
Provides:       %{?scl_prefix}php-pecl(%{pecl_name})         = %{version}
Provides:       %{?scl_prefix}php-pecl(%{pecl_name})%{?_isa} = %{version}
Provides:       %{?scl_prefix}php-pecl-%{pecl_name}          = %{version}-%{release}
Provides:       %{?scl_prefix}php-pecl-%{pecl_name}%{?_isa}  = %{version}-%{release}

%if "%{?vendor}" == "Remi Collet" && 0%{!?scl:1}
# Other third party repo stuff
Obsoletes:      php53-pecl-%{pecl_name}  <= %{version}
Obsoletes:      php53u-pecl-%{pecl_name} <= %{version}
Obsoletes:      php54-pecl-%{pecl_name}  <= %{version}
Obsoletes:      php54w-pecl-%{pecl_name} <= %{version}
%if "%{php_version}" > "5.5"
Obsoletes:      php55u-pecl-%{pecl_name} <= %{version}
Obsoletes:      php55w-pecl-%{pecl_name} <= %{version}
%endif
%if "%{php_version}" > "5.6"
Obsoletes:      php56u-pecl-%{pecl_name} <= %{version}
Obsoletes:      php56w-pecl-%{pecl_name} <= %{version}
%endif
%if "%{php_version}" > "7.0"
Obsoletes:      php70u-pecl-%{pecl_name} <= %{version}
Obsoletes:      php70w-pecl-%{pecl_name} <= %{version}
%endif
%if "%{php_version}" > "7.1"
Obsoletes:      php71u-pecl-%{pecl_name} <= %{version}
Obsoletes:      php71w-pecl-%{pecl_name} <= %{version}
%endif
%endif

%if 0%{?fedora} < 20 && 0%{?rhel} < 7
# Filter shared private
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}
%endif


%description
This extension uses libgearman library to provide API for
communicating with gearmand, and writing clients and workers

Documentation: http://php.net/gearman

Package built for PHP %(%{__php} -r 'echo PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')%{?scl: as Software Collection (%{scl} by %{?scl_vendor}%{!?scl_vendor:rh})}.


%prep
%setup -q -c
mv %{gh_project}-%{gh_commit} NTS
%{__php} -r '
  $pkg = simplexml_load_file("NTS/package.xml");
  $pkg->date = substr("%{gh_date}",0,4)."-".substr("%{gh_date}",4,2)."-".substr("%{gh_date}",6,2);
  $pkg->version->release = "%{version}";
  $pkg->asXML("package.xml");
'

# Dont register tests on install
sed -e 's/role="test"/role="src"/' \
    %{?_licensedir:-e '/LICENSE/s/role="doc"/role="src"/' } \
    -i package.xml


extver=$(sed -n '/#define PHP_GEARMAN_VERSION/{s/.* "//;s/".*$//;p}' NTS/php_gearman.h)
if test "x${extver}" != "x%{version}"; then
   : Error: Upstream version is ${extver}, expecting %{version}.
   exit 1
fi

cat >%{ini_name} <<EOF
; enable %{pecl_name} extension
extension=%{pecl_name}.so
EOF

find NTS -type f -exec chmod -x {} \;

%if %{with_zts}
cp -pr NTS ZTS
%endif


%build
cd NTS
%{_bindir}/phpize
%configure  --with-php-config=%{_bindir}/php-config
make %{?_smp_mflags}

%if %{with_zts}
cd ../ZTS
%{_bindir}/zts-phpize
%configure  --with-php-config=%{_bindir}/zts-php-config
make %{?_smp_mflags}
%endif


%install
rm -rf %{buildroot}

make -C NTS install INSTALL_ROOT=%{buildroot}

# Install XML package description
install -Dpm 644 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml

# install config file
install -Dpm644 %{ini_name} %{buildroot}%{php_inidir}/%{ini_name}

%if %{with_zts}
make -C ZTS install INSTALL_ROOT=%{buildroot}
install -Dpm644 %{ini_name} %{buildroot}%{php_ztsinidir}/%{ini_name}
%endif

# Documentation
for i in $(grep 'role="doc"' package.xml | sed -e 's/^.*name="//;s/".*$//')
do install -Dpm 644 NTS/$i %{buildroot}%{pecl_docdir}/%{pecl_name}/$i
done


%check
: Minimal load test for NTS extension
%{__php} --no-php-ini \
    --define extension=%{buildroot}%{php_extdir}/%{pecl_name}.so \
    --modules | grep %{pecl_name}

%if %{with_zts}
: Minimal load test for ZTS extension
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
* Tue Sep 20 2016 Remi Collet <remi@fedoraproject.org> - 2.0.1-1
- update to 2.0.1 for PHP 7
- use sources from https://github.com/wcgallego/pecl-gearman fork

* Wed Mar  9 2016 Remi Collet <remi@fedoraproject.org> - 1.1.2-8
- adapt for F24

* Sat Jun 20 2015 Remi Collet <remi@fedoraproject.org> - 1.1.2-7
- allow build against rh-php56 (as more-php56)
- drop runtime dependency on pear, new scriptlets

* Wed Dec 24 2014 Remi Collet <remi@fedoraproject.org> - 1.1.2-6.1
- Fedora 21 SCL mass rebuild

* Tue Sep  9 2014 Remi Collet <remi@fedoraproject.org> - 1.1.2-6
- don't install tests
- fix license handling

* Mon Aug 25 2014 Remi Collet <rcollet@redhat.com> - 1.1.2-5
- improve SCL build

* Wed Apr  9 2014 Remi Collet <remi@fedoraproject.org> - 1.1.2-4
- add numerical prefix to extension configuration file

* Wed Mar 19 2014 Remi Collet <rcollet@redhat.com> - 1.1.2-3
- allow SCL build

* Mon Mar  3 2014 Remi Collet <remi@fedoraproject.org> - 1.1.2-2
- cleanups
- install documentation in pecl_docdir
- install tests in pecl_testdir

* Thu Aug 29 2013 Remi Collet <remi@fedoraproject.org> - 1.1.2-1
- update to 1.1.2

* Mon Aug 19 2013 Remi Collet <remi@fedoraproject.org> - 1.1.1-1
- single spec for 0.8.x / 1.0.x / 1.1.x
- update to 1.1.1, requires libgearman >= 1.1.0

* Fri Nov 30 2012 Remi Collet <remi@fedoraproject.org> - 1.0.3-1.1
- also provides php-gearman

* Sun Aug 05 2012 Remi Collet <remi@fedoraproject.org> - 1.0.3-1
- update to 1.0.3
- add missing provides php-pecl(gearman)

* Sun Aug 05 2012 Remi Collet <remi@fedoraproject.org> - 0.8.3-1
- update to 0.8.3
- add missing provides php-pecl(gearman)

* Sat May 05 2012 Remi Collet <remi@fedoraproject.org> - 1.0.2-3
- add BR libgearman-1.0 + libgearman-1.0-devel
  Workaround for https://bugzilla.redhat.com/819209

* Tue Mar 06 2012 Remi Collet <remi@fedoraproject.org> - 1.0.2-2
- update to 1.0.2 for PHP 5.4

* Tue Mar 06 2012 Remi Collet <remi@fedoraproject.org> - 1.0.2-1
- update to 1.0.2 for PHP 5.3
- spec clean up

* Fri Dec 09 2011 Remi Collet <remi@fedoraproject.org> - 1.0.1-2
- update to 1.0.1, build against php 5.4

* Fri Dec 09 2011 Remi Collet <remi@fedoraproject.org> - 1.0.1-1
- update to 1.0.1

* Fri Dec 09 2011 Remi Collet <remi@fedoraproject.org> - 0.8.1-2
- update to 0.8.1, build against php 5.4

* Fri Dec 09 2011 Remi Collet <remi@fedoraproject.org> - 0.8.1-1
- update to 0.8.1

* Mon Dec 05 2011 Remi Collet <remi@fedoraproject.org> - 1.0.0-2
- build against php 5.4

* Mon Dec 05 2011 Remi Collet <remi@fedoraproject.org> - 1.0.0-1
- update to 1.0.0
- raise dependency to libgearman 0.21 (si f16 only)

* Mon Nov 14 2011 Remi Collet <remi@fedoraproject.org> - 0.8.0-2
- build against php 5.4

* Sat Oct 15 2011 Remi Collet <Fedora@FamilleCollet.com> - 0.8.0-1
- update to 0.8.0
- ZTS extension
- spec cleanup and minimal %%check
- fix requires

* Fri Aug 12 2011 Jesse Keating <jkeating@redhat.com> - 0.7.0-5
- Rebuild for broken deps

* Mon Apr 11 2011 Paul Whalen <paul.whalen@senecac.on.ca> 0.7.0-4
- fix setup and package.xml install

* Mon Apr 11 2011 Paul Whalen <paul.whalen@senecac.on.ca> 0.7.0-3
- correct macros, add license to files

* Fri Apr 08 2011 Paul Whalen <paul.whalen@senecac.on.ca> 0.7.0-2
- correct package following pecl packaging guidelines

* Fri Mar 11 2011 Paul Whalen <paul.whalen@senecac.on.ca> 0.7.0-1
- Initial Packaging

