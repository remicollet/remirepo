# remirepo spec file for php-pecl-runkit
# with SCL compatibility from:

# Fedora spec file for php-pecl-runkit
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
%endif

%{?scl:          %scl_package         php-pecl-runkit}

#global gh_owner    zenovich
#global gh_commit   80160a2cf94b0377924a7d08f9318bef0c225214
#global gh_short    %(c=%{gh_commit}; echo ${c:0:7})
%global pecl_name   runkit
%global with_zts    0%{?__ztsphp:1}
%if "%{php_version}" < "5.6"
%global ini_name    %{pecl_name}.ini
%else
%global ini_name    40-%{pecl_name}.ini
%endif
%global channel     zenovich.github.io/pear

Summary:          Mangle with user defined functions and classes
Name:             %{?sub_prefix}php-pecl-%{pecl_name}
Version:          1.0.4
Release:          3%{?dist}%{!?scl:%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}}
License:          PHP
Group:            Development/Libraries
# URL:            http://pecl.php.net/package/runkit/
# New upstream URL - https://bugs.php.net/bug.php?id=61189
URL:              https://github.com/zenovich/runkit

%if 0%{?gh_short:1}
Source0:          https://github.com/%{gh_owner}/%{pecl_name}/archive/%{gh_commit}/%{pecl_name}-%{version}-%{gh_short}.tar.gz
%else
Source0:          http://pecl.php.net/get/%{pecl_name}-%{version}.tgz
%endif

BuildRoot:        %{_tmppath}/%{name}-%{version}-root-%(id -u -n)
BuildRequires:    %{?scl_prefix}php-pear
BuildRequires:    %{?scl_prefix}php-devel

Requires:         %{?scl_prefix}php(zend-abi) = %{php_zend_api}
Requires:         %{?scl_prefix}php(api) = %{php_core_api}
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
# filter private shared
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}
%endif


%description
Replace, rename, and remove user defined functions and classes. Define
customized superglobal variables for general purpose use. Execute code
in restricted environment (sandboxing).

Package built for PHP %(%{__php} -r 'echo PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')%{?scl: as Software Collection (%{scl} by %{?scl_vendor}%{!?scl_vendor:rh})}.


%prep
%if 0%{?gh_short:1}
%setup -q -c
mv runkit-%{gh_commit} NTS
mv NTS/package.xml .
sed -e '/<channel>/s:%{channel}:pecl.php.net:' -i package.xml
%else
%setup -q -c
mv runkit-%{version} NTS
%endif

# Don't install/register tests
sed -e 's/role="test"/role="src"/' \
    %{?_licensedir:-e '/LICENSE/s/role="doc"/role="src"/' } \
    -i package.xml

cd NTS
sed -e 's/-Werror//' -i config.m4

extver=$(sed -n '/#define PHP_RUNKIT_VERSION/{s/.*\t"//;s/".*$//;p}' php_runkit.h)
if test "x${extver}" != "x%{version}%{?prever}"; then
   : Error: Upstream version is ${extver}, expecting %{version}%{?prever}.
   exit 1
fi
cd ..

%if %{with_zts}
# duplicate for ZTS build
cp -pr NTS ZTS
%endif

# Create the configuration file
cat <<'EOF' > %{ini_name}
; Enable %{pecl_name} extension module
extension=%{pecl_name}.so
EOF


%build
cd NTS
%{_bindir}/phpize
%configure \
    --with-%{pecl_name}\
    --with-php-config=%{_bindir}/php-config
make %{?_smp_mflags}

%if %{with_zts}
cd ../ZTS
%{_bindir}/zts-phpize
%configure \
    --with-%{pecl_name}\
    --with-php-config=%{_bindir}/zts-php-config
make %{?_smp_mflags}
%endif


%install
rm -rf %{buildroot}

make install -C NTS install INSTALL_ROOT=%{buildroot}

# Drop in the bit of configuration
install -Dpm 644 %{ini_name} %{buildroot}%{php_inidir}/%{ini_name}

# Install XML package description
install -Dpm 0664 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml

%if %{with_zts}
make install -C ZTS install INSTALL_ROOT=%{buildroot}
install -Dpm 644 %{ini_name} %{buildroot}%{php_ztsinidir}/%{ini_name}
%endif

# Documentation
cd NTS
for i in $(grep 'role="doc"' ../package.xml | sed -e 's/^.*name="//;s/".*$//')
do install -Dpm 644 $i %{buildroot}%{pecl_docdir}/%{pecl_name}/$i
done


%check
# See https://github.com/zenovich/runkit/pull/93
rm ?TS/tests/runkit_fpm_internal_function_restore.phpt

# Minimal load test
%{__php} --no-php-ini \
    --define extension=%{buildroot}%{php_extdir}/%{pecl_name}.so \
    -m | grep %{pecl_name}

# Provided test suite
cd NTS
TEST_PHP_EXECUTABLE=%{__php} \
TEST_PHP_ARGS="-n -d extension_dir=%{buildroot}%{php_extdir} -d extension=%{pecl_name}.so" \
NO_INTERACTION=1 \
REPORT_EXIT_STATUS=1 \
%{_bindir}/php -n run-tests.php --show-diff

%if %{with_zts}
%{__ztsphp} --no-php-ini \
    --define extension=%{buildroot}%{php_ztsextdir}/%{pecl_name}.so \
    -m | grep %{pecl_name}

cd ../ZTS
TEST_PHP_EXECUTABLE=%{__ztsphp} \
TEST_PHP_ARGS="-n -d extension_dir=%{buildroot}%{php_ztsextdir} -d extension=%{pecl_name}.so" \
NO_INTERACTION=1 \
REPORT_EXIT_STATUS=1 \
%{_bindir}/php -n run-tests.php --show-diff
%endif


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


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{?_licensedir:%license NTS/LICENSE}
%doc %{pecl_docdir}/%{pecl_name}
%{pecl_xmldir}/%{name}.xml

%{php_extdir}/%{pecl_name}.so
%config(noreplace) %{php_inidir}/%{ini_name}

%if %{with_zts}
%{php_ztsextdir}/%{pecl_name}.so
%config(noreplace) %{php_ztsinidir}/%{ini_name}
%endif


%changelog
* Tue Mar  8 2016 Remi Collet <remi@fedoraproject.org> - 1.0.4-3
- adapt for F24
- fix license management

* Mon Oct 19 2015 Remi Collet <remi@fedoraproject.org> - 1.0.4-2
- switch to pecl sources

* Tue Oct 13 2015 Remi Collet <remi@fedoraproject.org> - 1.0.4-1
- update to 1.0.4
- drop runtime dependency on pear, new scriptlets
- don't install/register tests
- add virtual provides for php-zenovich-runkit and
  php-pecl(zenovich.github.io/pear/runkit)

* Wed Dec 24 2014 Remi Collet <remi@fedoraproject.org> - 1.0.4-0.9.git5e179e9
- Fedora 21 SCL mass rebuild

* Mon Aug 25 2014 Remi Collet <rcollet@redhat.com> - 1.0.4-0.8.git5e179e9
- improve SCL build

* Wed Apr 16 2014 Remi Collet <remi@fedoraproject.org> - 1.0.4-0.7.git5e179e9
- add numerical prefix to extension configuration file (php 5.6)

* Wed Mar 19 2014 Remi Collet <rcollet@redhat.com> - 1.0.4-0.6.git5e179e9
- allow SCL build

* Tue Mar 18 2014 Remi Collet <remi@fedoraproject.org> - 1.0.4-0.5.git5e179e9
- cleanups
- install doc in pecl_docdir
- install tests in pecl_testdir
- make ZTS build optional

* Thu Jul 18 2013 Remi Collet <remi@fedoraproject.org> - 1.0.4-0.4.git5e179e9
- update to latest master snapshot
- fix Source0 URL

* Fri Dec  7 2012 Remi Collet <remi@fedoraproject.org> - 1.0.4-0.3.gitd069e23
- update to latest master snapshot
- also provides php-runkit
- run tests during build
- cleanups

* Wed Sep 12 2012 Remi Collet <remi@fedoraproject.org> - 1.0.4-0.2.gita079457
- standardize for remi repo, lot of cleanups
- add ZTS extension
- add %%check section: minimal load test
- update to latest master snapshot

* Mon Sep  3 2012 Pavel Alexeev <Pahan@Hubbitus.info> - 1.0.4-0.1.GIT8c73eaf
- New upstream url - https://bugs.php.net/bug.php?id=61189, continue developing, new version, switch to git SCM.
- Fix compilation error: https://github.com/zenovich/runkit/issues/26#issuecomment-8268795

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-16.CVS20090215
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-15.CVS20090215
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Aug  2 2011 Pavel Alexeev <Pahan@Hubbitus.info> - 0.9-14.CVS20090215
- Fix FBFS on Fedora 16(17 rawhide) and rpm 4.9 - bz#715709

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-13.CVS20090215
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jul 30 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 0.9-12.CVS20090215
- Apply patches only on PHP>=5.3.0. (Bug: https://bugzilla.redhat.com/show_bug.cgi?id=513096 )

* Sun Apr  5 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 0.9-11.CVS20090215
- By suggestion in the bug https://fedorahosted.org/fedora-infrastructure/ticket/1298 try remove version specifications in requires:
    Turn BuildRequires: php-pear >= 1.4.7, php-devel >= 5.0.0 to just BuildRequires: php-pear, php-devel
- Add more magick in Release tag: 11%%{?CVS:.CVS%%{CVS}}%%{?dist}

* Tue Mar 17 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 0.9-10.CVS20090215
- Remi Collet notes in Fedora review:
- Rename back %%{peclName}.xml to %%{name}.xml :)
- Set %%defattr(-,root,root,-) (was %%defattr(644,root,root,755))
- Make the %%post/%%postun scriptlets silent

* Mon Mar  9 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 0.9-9.CVS20090215
- In rename %%{name}.xml to %%{peclName}.xml
- Add BR php-pear >= 1.4.7

* Wed Feb 25 2009 Pavel Alexeev <Pahan [ at ] Hubbitus [ DOT ] spb [ dOt.] su> - 0.9-8.CVS20090215
- All changes inspired by Fedora package review by Remi Collet.
- From summary deleted name.
- Readmy path fixed(replaced %%{peclName}-%%{version}/README to %%{peclName}/README)
- Group changed to Development/Libraries (was: Development/Languages/PHP)
- Removed Obsoletes: php-pear-%%{peclName} it was unnecessary.

* Mon Feb 23 2009 Pavel Alexeev <Pahan [ at ] Hubbitus [ DOT ] spb [ dOt.] su> - 0.9-7.CVS20090215
- Again change version enumeration (https://bugzilla.redhat.com/show_bug.cgi?id=455226#c9).
- %%{pecl_xmldir}/%%{peclName}2.xml changed to %%{pecl_xmldir}/%%{name}.xml
- Recode pl summary and description text from iso8859-2 to UTF-8.

* Sun Feb 15 2009 Pavel Alexeev <Pahan [ at ] Hubbitus [ DOT ] spb [ dOt.] su> - 0.9-0.6.CVS20090215
- Step to CVS build 20090215.
- Replace $RPM_BUILD_ROOT to %%{buildroot} to consistence usage.
- Strip some old comments.
- Add translated Summary(ru) and description.
- Remove legacy macros %%{?requires_php_extension}.
- All macroses %%peclName replaced to %{peclName} usages.
- Add file: %%{pecl_xmldir}/%%{peclName}2.xml
- All followed changes inspired by Fedora review by Remi Collet ( https://bugzilla.redhat.com/show_bug.cgi?id=455226 ).
- Change version enumeration, delete Hu-part.
- Modify Source0 for CVS build. Add comment about get it source.
- Spec-file renamed to php-pecl-runkit.spec.
- File BUG to upstream - http://pecl.php.net/bugs/bug.php?id=15969 .
- %%Post and %%postun scripts to restart apache removed.
- Register extension.
- Add PHP ABI provides/requires and Pre/post requires pecl.
- Defile some macroses from guidelines: php_apiver, __pecl, php_extdir.
- Replace %%extensionsdir by %%php_extdir.

* Mon May 12 2008 Pavel Alexeev <Pahan [ at ] Hubbitus [ DOT ] spb [ dOt.] su> - 0.9-0.CVS20080512.Hu.5
- Add Patch3: php-pecl-runkit-0.9.Z_NEW_REFCOUNT.patch to reflect new zend API

* Mon May 12 2008 Pavel Alexeev <Pahan [ at ] Hubbitus [ DOT ] spb [ dOt.] su> - 0.9-0.CVS20080512.Hu.3
- New CVS20080512 (cvs -d :pserver:cvsread@cvs.php.net/repository checkout pecl/runkit)
- Rename %%{_modname} to peclName to unify SPECs.
- Correct %%if 0%%{?CVS} to %%if 0%%{?CVS:1} - it is not integer!
- Rename pethces to:
    Patch0:        php-pecl-runkit-0.9-ZVAL_REFCOUNT.patch
    Patch1:        php-pecl-runkit-0.9-ZVAL_ADDREF.patch

* Mon Mar 10 2008 Pavel Alexeev <Pahan [ at ] Hubbitus [ DOT ] spb [ dOt.] su> - 0.9-0.CVS20080310.Hu.2
- CVS20080310 build. (cvs -d :pserver:cvsread@cvs.php.net:/repository checkout pecl/runkit)
- 0.9 stable are incompatible with php 5.3.0, build from CVS. Disable self patch0
- Enable patch0. Rewritten and rename to fix ZVAL_REFCOUNT.patch
    Hu.1
- Add patch1. Fix wrong call ZVAL_ADDREF.patch
    Hu.2

* Sun Mar  9 2008 Pavel Alexeev <Pahan [ at ] Hubbitus [ DOT ] info> - 0.9-0.Hu.3
- Add patch (self written) zval_ref.patch. It is allow build.
- Agjust built dir:
    BuildRoot:    %%{tmpdir}/%%{name}-%%{version}-root-%%(id -u -n)
    to
    BuildRoot:    %%{_tmppath}/%%{name}-%%{version}-root-%%(id -u -n)
- Fix Release:        0%%{?dist}.Hu.2 -> Release:        0%%{?dist}.Hu.2
    Hu.2
- Remove %%define _status beta and all apearance of %%{_status}
- Remove %%define _sysconfdir /etc/php (it's already defined in system wide)
- Remove Requires: %%{_sysconfdir}/conf.d
- Change path %%{_sysconfdir}/conf.d to %%{_sysconfdir}/php.d:
    Replace:
        install -d $RPM_BUILD_ROOT{%%{_sysconfdir}/conf.d,%%{extensionsdir}}
        to
        install -d $RPM_BUILD_ROOT{%%{_sysconfdir}/php.d,%%{extensionsdir}}

        %%config(noreplace) %%verify(not md5 mtime size) %%{_sysconfdir}/conf.d/%%{_modname}.ini
        to
        %%config(noreplace) %%verify(not md5 mtime size) %%{_sysconfdir}/php.d/%%{_modname}.ini

        cat <<'EOF' > $RPM_BUILD_ROOT%%{_sysconfdir}/conf.d/%%{_modname}.ini
        to
        cat <<'EOF' > $RPM_BUILD_ROOT%%{_sysconfdir}/php.d/%%{_modname}.ini
- Hu.3

* Wed Feb 27 2008 Pavel Alexeev <Pahan [ at ] Hubbitus [ DOT ] info> - 0.9-0.Hu.0
- Import from ftp://ftp.pld-linux.org/dists/2.0/PLD/SRPMS/SRPMS/php-pecl-runkit-0.4-5.src.rpm
- Step to version 0.9
    Release:        0{?dist}.Hu.0 (Was: Release:    0)
- Remove defining %%date and:
    * %%{date} PLD Team <feedback@pld-linux.org>
    All persons listed below can be reached at <cvs_login>@pld-linux.org
 due to error: ошибка: %%changelog не в нисходящем хронологическом порядке
- Small reformat of header spec
- Change BuildRequires:    php-devel >= 3:5.0.0 to php-devel >= 5.0.0
-Remove BuildRequires:    rpmbuild(macros) >= 1.254

