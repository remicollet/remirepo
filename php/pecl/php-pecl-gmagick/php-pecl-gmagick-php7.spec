# spec file for php-pecl-gmagick
#
# Copyright (c) 2010-2016 Remi Collet
# Copyright (c) 2009-2010 Pavel Alexeev
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please, preserve the changelog entries
#
%if 0%{?scl:1}
%global sub_prefix %{scl_prefix}
%scl_package       php-pecl-gmagick
%endif

%global pecl_name  gmagick
%global prever     RC1
%global with_zts   0%{!?_without_zts:%{?__ztsphp:1}}
%global ini_name   40-%{pecl_name}.ini

Summary:        Provides a wrapper to the GraphicsMagick library
Name:           %{?sub_prefix}php-pecl-%{pecl_name}
Version:        2.0.4
Release:        0.3.%{prever}%{?dist}%{!?scl:%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}}
License:        PHP
Group:          Development/Libraries
URL:            http://pecl.php.net/package/%{pecl_name}
Source0:        http://pecl.php.net/get/%{pecl_name}-%{version}%{?prever}.tgz

BuildRoot:      %{_tmppath}/%{name}-%{version}-root-%(%{__id_u} -n)
BuildRequires:  %{?scl_prefix}php-pear
BuildRequires:  %{?scl_prefix}php-devel >= 7.0.1
BuildRequires:  GraphicsMagick-devel >= 1.3.17

Requires:       %{?scl_prefix}php(zend-abi) = %{php_zend_api}
Requires:       %{?scl_prefix}php(api) = %{php_core_api}
%{?_sclreq:Requires: %{?scl_prefix}runtime%{?_sclreq}%{?_isa}}

Provides:       %{?scl_prefix}php-%{pecl_name}               = %{version}
Provides:       %{?scl_prefix}php-%{pecl_name}%{?_isa}       = %{version}
Provides:       %{?scl_prefix}php-pecl(%{pecl_name})         = %{version}
Provides:       %{?scl_prefix}php-pecl(%{pecl_name})%{?_isa} = %{version}
%if "%{?scl_prefix}" != "%{?sub_prefix}"
Provides:       %{?scl_prefix}php-pecl-%{pecl_name}          = %{version}-%{release}
Provides:       %{?scl_prefix}php-pecl-%{pecl_name}%{?_isa}  = %{version}-%{release}
%endif

Conflicts:      %{?scl_prefix}php-pecl-imagick
Conflicts:      %{?scl_prefix}php-magickwand

%if "%{?vendor}" == "Remi Collet" && 0%{!?scl:1} && 0%{?rhel}
# Other third party repo stuff
Obsoletes:     php53-pecl-%{pecl_name}  <= %{version}
Obsoletes:     php53u-pecl-%{pecl_name} <= %{version}
Obsoletes:     php54-pecl-%{pecl_name}  <= %{version}
Obsoletes:     php54w-pecl-%{pecl_name} <= %{version}
Obsoletes:     php55u-pecl-%{pecl_name} <= %{version}
Obsoletes:     php55w-pecl-%{pecl_name} <= %{version}
Obsoletes:     php56u-pecl-%{pecl_name} <= %{version}
Obsoletes:     php56w-pecl-%{pecl_name} <= %{version}
Obsoletes:     php70u-pecl-%{pecl_name} <= %{version}
Obsoletes:     php70w-pecl-%{pecl_name} <= %{version}
%if "%{php_version}" > "7.1"
Obsoletes:     php71u-pecl-%{pecl_name} <= %{version}
Obsoletes:     php71w-pecl-%{pecl_name} <= %{version}
%endif
%endif

%if 0%{?fedora} < 20 && 0%{?rhel} < 7
# Filter private shared
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}
%endif


%description
%{pecl_name} is a php extension to create, modify and obtain meta information
of images using the GraphicsMagick API.

Package built for PHP %(%{__php} -r 'echo PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')%{?scl: as Software Collection (%{scl} by %{?scl_vendor}%{!?scl_vendor:rh})}.


%prep
%setup -qc

# Don't install/register tests
sed -e 's/role="test"/role="src"/' \
    %{?_licensedir:-e '/LICENSE/s/role="doc"/role="src"/' } \
    -i package.xml

mv %{pecl_name}-%{version}%{?prever} NTS
cd NTS

extver=$(sed -n '/#define PHP_GMAGICK_VERSION/{s/.* "//;s/".*$//;p}' php_gmagick.h)
if test "x${extver}" != "x%{version}%{?prever}"; then
   : Error: Upstream version is ${extver}, expecting %{version}%{?prever}.
   exit 1
fi
cd ..

# Create configuration file
cat >%{ini_name} << 'EOF'
; Enable %{pecl_name} extension module
extension=%{pecl_name}.so
EOF

%if %{with_zts}
# Duplicate build tree for nts/zts
cp -r NTS ZTS
%endif


%build
cd NTS
%{_bindir}/phpize
%{configure} --with-%{pecl_name}  --with-php-config=%{_bindir}/php-config
make %{?_smp_mflags}

%if %{with_zts}
cd ../ZTS
%{_bindir}/zts-phpize
%{configure} --with-%{pecl_name}  --with-php-config=%{_bindir}/zts-php-config
make %{?_smp_mflags}
%endif


%install
rm -rf %{buildroot}

make -C NTS install INSTALL_ROOT=%{buildroot}

# Install XML package description
install -D -m 664 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml

# Drop in the bit of configuration
install -D -m 664 %{ini_name} %{buildroot}%{php_inidir}/%{ini_name}

%if %{with_zts}
make -C ZTS install INSTALL_ROOT=%{buildroot}
install -D -m 664 %{ini_name} %{buildroot}%{php_ztsinidir}/%{ini_name}
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
: simple module load test for NTS extension
cd NTS
%{__php} --no-php-ini \
    --define extension=%{buildroot}%{php_extdir}/%{pecl_name}.so \
    --modules | grep %{pecl_name}

: upstream test suite for NTS extension
export TEST_PHP_EXECUTABLE=%{__php}
export REPORT_EXIT_STATUS=1
export NO_INTERACTION=1
export TEST_PHP_ARGS="-n -d extension=$PWD/modules/%{pecl_name}.so"
%{__php} -n run-tests.php --show-diff

%if %{with_zts}
: simple module load test for ZTS extension
cd ../ZTS
%{__ztsphp} --no-php-ini \
    --define extension=%{buildroot}%{php_ztsextdir}/%{pecl_name}.so \
    --modules | grep %{pecl_name}

: upstream test suite for ZTS extension
export TEST_PHP_EXECUTABLE=%{__ztsphp}
export TEST_PHP_ARGS="-n -d extension=$PWD/modules/%{pecl_name}.so"
%{__ztsphp} -n run-tests.php --show-diff
%endif


%files
%defattr(-,root,root,-)
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
* Thu Dec  1 2016 Remi Collet <remi@fedoraproject.org> - 2.0.4-0.3.RC1
- rebuild with PHP 7.1.0 GA

* Wed Sep 14 2016 Remi Collet <remi@fedoraproject.org> - 2.0.4-0.2.RC1
- rebuild for PHP 7.1 new API version

* Mon Jun 27 2016 Remi Collet <remi@fedoraproject.org> - 2.0.4-0.1.RC1
- Update to 2.0.4RC1 (php 7, beta)

* Sun Jun 26 2016 Remi Collet <remi@fedoraproject.org> - 2.0.3-0.1.RC1
- Update to 2.0.3RC1 (php 7, beta)

* Fri Jun 24 2016 Remi Collet <remi@fedoraproject.org> - 2.0.2-0.4.RC2
- add patch for PHP 7.1, https://github.com/vitoc/gmagick/pull/41

* Fri Mar 11 2016 Remi Collet <remi@fedoraproject.org> - 2.0.2-0.3.RC2
- Update to 2.0.2RC2 (php 7, beta)

* Sat Mar  5 2016 Remi Collet <remi@fedoraproject.org> - 2.0.2-0.2.RC1
- adapt for F24

* Sat Feb 20 2016 Remi Collet <remi@fedoraproject.org> - 2.0.2-0.1.RC1
- Update to 2.0.2RC1 (php 7, beta)

* Thu Feb  4 2016 Remi Collet <remi@fedoraproject.org> - 2.0.1-0.3.RC3
- Update to 2.0.1RC3 (php 7, beta)

* Sun Jan 31 2016 Remi Collet <remi@fedoraproject.org> - 2.0.1-0.2.RC2
- Update to 2.0.1RC2 (php 7, beta)
- lower dependency on GraphicsMagick >= 1.3.17
- open https://github.com/vitoc/gmagick/issues/25
- open https://github.com/vitoc/gmagick/issues/26

* Tue Dec 29 2015 Remi Collet <remi@fedoraproject.org> - 2.0.1-0.1.RC1
- Update to 2.0.1RC1 (php 7, beta)
- lower dependency on GraphicsMagick >= 1.3.20

* Tue Dec 29 2015 Remi Collet <remi@fedoraproject.org> - 2.0.0-0.1.RC1
- Update to 2.0.0RC1 (php 7, beta)
- raise dependency on GraphicsMagick >= 1.3.22

* Fri Apr 24 2015 Remi Collet <remi@fedoraproject.org> - 1.1.7-0.6.RC3
- Update to 1.1.7RC3 (beta)
- don't install/register tests
- drop runtime dependency on pear, new scriptlets

* Wed Dec 24 2014 Remi Collet <remi@fedoraproject.org> - 1.1.7-0.5.RC2
- Fedora 21 SCL mass rebuild

* Mon Aug 25 2014 Remi Collet <rcollet@redhat.com> - 1.1.7-0.4.RC2
- improve SCL build

* Mon Mar 17 2014 Remi Collet <remi@fedoraproject.org> - 1.1.7-0.3.RC2
- Update to 1.1.7RC2 (beta)

* Mon Mar  3 2014 Remi Collet <remi@fedoraproject.org> - 1.1.7-0.2.RC1
- add upstream patch for PHP 5.6

* Fri Feb 14 2014 Remi Collet <remi@fedoraproject.org> - 1.1.7-0.1.RC1
- Update to 1.1.7RC1 (beta)

* Thu Jan 30 2014 Remi Collet <remi@fedoraproject.org> - 1.1.6-0.3.RC3
- Update to 1.1.6RC3 (beta)

* Sat Dec 14 2013 Remi Collet <remi@fedoraproject.org> - 1.1.6-0.2.RC2
- Update to 1.1.6RC2 (beta)

* Sat Dec 14 2013 Remi Collet <remi@fedoraproject.org> - 1.1.6-0.1.RC1
- Update to 1.1.6RC1 (beta)
- adapt for SCL
- add patch for setStrokeDashArray / getStrokeDashArray

* Tue Nov  5 2013 Remi Collet <RPMS@FamilleCollet.com> - 1.1.5-0.1.RC1
- Update to 1.1.5RC1
- cleanups for Copr

* Sun Oct 20 2013 Remi Collet <RPMS@FamilleCollet.com> - 1.1.4-0.1.RC1
- Update to 1.1.4RC1
- drop merged patches

* Sun Oct 20 2013 Remi Collet <RPMS@FamilleCollet.com> - 1.1.3-0.1.RC1
- Update to 1.1.3RC1
- install doc in pecl doc_dir
- install tests in pecl test_dir
- take care of test results

* Fri Dec 28 2012 Remi Collet <RPMS@FamilleCollet.com> - 1.1.2-0.1.RC1
- Update to 1.1.2RC1
- also provides php-gmagick

* Wed Sep 12 2012 Remi Collet <RPMS@FamilleCollet.com> - 1.1.1-0.1.RC1
- Update to 1.1.1RC1

* Sat Jun 02 2012 Remi Collet <remi@fedoraproject.org> - 1.1.0-0.5.RC3
- Update to 1.1.0RC3

* Sat Jan 21 2012 Remi Collet <remi@fedoraproject.org> - 1.1.0-0.4.RC2
- add patch for getColor options https://bugs.php.net/60829

* Fri Jan 20 2012 Remi Collet <remi@fedoraproject.org> - 1.1.0-0.3.RC2
- build against php 5.4

* Fri Jan 20 2012 Remi Collet <remi@fedoraproject.org> - 1.1.0-0.2.RC2
- Update to 1.1.0RC2
  fix https://bugs.php.net/60807

* Thu Jan 19 2012 Remi Collet <remi@fedoraproject.org> - 1.1.0-0.1.RC1
- Update to 1.1.0RC1

* Mon Dec 05 2011 Remi Collet <remi@fedoraproject.org> - 1.0.10-0.2.b1
- build against php 5.4

* Mon Dec 05 2011 Remi Collet <remi@fedoraproject.org> - 1.0.10-0.1.b1
- Update to 1.0.10b1
- run tests

* Tue Nov 15 2011 Remi Collet <remi@fedoraproject.org> - 1.0.9-0.2.b1
- build against php 5.4
- add patch for php 5.4, see https://bugs.php.net/60308

* Sun Oct 02 2011 Remi Collet <rpms@famillecollet.com> 1.0.9-0.1.b1
- Update to 1.0.9b1
- build zts extension
- clean spec

* Thu May 05 2011 Remi Collet <rpms@famillecollet.com> 1.0.8-0.4.b2
- Update to 1.0.8b2

* Sat Apr 16 2011 Remi Collet <rpms@famillecollet.com> 1.0.8-0.3.b1
- fix build against latest php

* Sun Oct 17 2010 Remi Collet <rpms@famillecollet.com> 1.0.8-0.2.b1
- F-14 build + add Conflicts php-magickwand

* Mon Sep 13 2010 Remi Collet <rpms@famillecollet.com> 1.0.8-0.1.b1
- Update to 1.0.8b1 for remi repo

* Sun Aug 08 2010 Remi Collet <rpms@famillecollet.com> 1.0.7-0.1.b1
- Update to 1.0.7b1 for remi repo
- remove patch for http://pecl.php.net/bugs/17991
- add fix for http://pecl.php.net/bugs/18002

* Sat Aug 07 2010 Remi Collet <rpms@famillecollet.com> 1.0.6-0.1.b1
- Update to 1.0.6b1 for remi repo
- add patch for http://pecl.php.net/bugs/17991

* Mon Jul 26 2010 Remi Collet <rpms@famillecollet.com> 1.0.5-0.1.b1
- Update to 1.0.5b1 for remi repo

* Mon Jul 26 2010 Pavel Alexeev <Pahan@Hubbitus.info> - 1.0.5b1-5
- Update to 1.0.5b1
- Add Conflicts: php-pecl-imagick - BZ#559675

* Sun Jan 31 2010 Pavel Alexeev <Pahan@Hubbitus.info> - 1.0.3b3-4
- Update to 1.0.3b3

* Fri Jan 29 2010 Remi Collet <rpms@famillecollet.com> 1.0.3-0.1.b3
- update to 1.0.3b3

* Tue Nov  3 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 1.0.2b1-3
- Fedora Review started, thanks to Andrew Colin Kissa.
- Remove macros %%{__make} in favour to plain make.
- Add %%{?_smp_mflags} to make.

* Mon Oct 12 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 1.0.2b1-2
- New version 1.0.2b1 - author include license text by my request. Thank you Vito Chin.
- Include LICENSE.

* Fri Oct  2 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 1.0.1b1-1
- Initial release.
- License text absent, but I ask Vito Chin by email to add it into tarball.
