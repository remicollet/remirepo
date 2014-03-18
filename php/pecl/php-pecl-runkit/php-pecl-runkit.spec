%{!?php_inidir:  %global php_inidir   %{_sysconfdir}/php.d}
%{!?__pecl:      %global __pecl       %{_bindir}/pecl}
%{!?__php:       %global __php        %{_bindir}/php}

%global gh_owner    zenovich
%global gh_commit   5e179e978af79444d3c877d5681ea91d15134a01
%global gh_short    %(c=%{gh_commit}; echo ${c:0:7})
%global pecl_name   runkit
%global with_zts    0%{?__ztsphp:1}

Summary:          Mangle with user defined functions and classes
Summary(ru):      Манипулирование пользовательскими функциями и классами
Summary(pl):      Obróbka zdefiniowanych przez użytkownika funkcji i klas
Name:             php-pecl-%{pecl_name}
Version:          1.0.4
Release:          0.5%{?gh_short:.git%{gh_short}}%{?dist}%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}
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

BuildRoot:    %{_tmppath}/%{name}-%{version}-root-%(id -u -n)
BuildRequires:    php-pear
BuildRequires:    php-devel

Requires(post):   %{__pecl}
Requires(postun): %{__pecl}
Requires:         php(zend-abi) = %{php_zend_api}
Requires:         php(api) = %{php_core_api}

Provides:         php-%{pecl_name} = %{version}
Provides:         php-%{pecl_name}%{?_isa} = %{version}
Provides:         php-pecl(%{pecl_name}) = %{version}
Provides:         php-pecl(%{pecl_name})%{?_isa} = %{version}

%if "%{?vendor}" == "Remi Collet"
# Other third party repo stuff
Obsoletes:        php53-pecl-%{pecl_name}
Obsoletes:        php53u-pecl-%{pecl_name}
Obsoletes:        php54-pecl-%{pecl_name}
%if "%{php_version}" > "5.5"
Obsoletes:        php55u-pecl-%{pecl_name}
%endif
%if "%{php_version}" > "5.6"
Obsoletes:        php56u-pecl-%{pecl_name}
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

%description -l ru
Замещение, переименование и удаление оперделенных пользователем функций
и классов. Определение собственных суперглобальных переменных. Выполнение
кода в ограниченной среде (песочнице)

%description -l pl
Zastępowanie, zmiana nazwy lub usuwanie zdefiniowanych przez
użytkownika funkcji i klas. Definiowanie zmiennych superglobalnych do
ogólnego użytku. Wykonywanie danego kodu w ograniczonym środowisku
(sandbox).


%prep
%setup -q -c

mv runkit-%{gh_commit} NTS
mv NTS/package.xml .

%if 0%{?rhel} == 5
sed -e 's/-Werror//' -i NTS/config.m4
%endif

%if %{with_zts}
# duplicate for ZTS build
cp -pr NTS ZTS
%endif

# Create the configuration file
cat <<'EOF' > %{pecl_name}.ini
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
install -Dpm 644 %{pecl_name}.ini %{buildroot}%{php_inidir}/%{pecl_name}.ini

# Install XML package description
install -Dpm 0664 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml

%if %{with_zts}
make install -C ZTS install INSTALL_ROOT=%{buildroot}
install -Dpm 644 %{pecl_name}.ini %{buildroot}%{php_ztsinidir}/%{pecl_name}.ini
%endif

# Test & Documentation
cd NTS
for i in $(grep 'role="test"' ../package.xml | sed -e 's/^.*name="//;s/".*$//')
do install -Dpm 644 tests/$i %{buildroot}%{pecl_testdir}/%{pecl_name}/$i
done
for i in $(grep 'role="doc"' ../package.xml | sed -e 's/^.*name="//;s/".*$//')
do install -Dpm 644 $i %{buildroot}%{pecl_docdir}/%{pecl_name}/$i
done


%check
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
%{_bindir}/php -n run-tests.php

%if %{with_zts}
%{__ztsphp} --no-php-ini \
    --define extension=%{buildroot}%{php_ztsextdir}/%{pecl_name}.so \
    -m | grep %{pecl_name}

cd ../ZTS
TEST_PHP_EXECUTABLE=%{__ztsphp} \
TEST_PHP_ARGS="-n -d extension_dir=%{buildroot}%{php_ztsextdir} -d extension=%{pecl_name}.so" \
NO_INTERACTION=1 \
REPORT_EXIT_STATUS=1 \
%{_bindir}/php -n run-tests.php
%endif


%post
%{pecl_install} %{pecl_xmldir}/%{name}.xml >/dev/null || :

%postun
if [ "$1" -eq "0" ]; then
    %{pecl_uninstall} %{pecl_name} >/dev/null || :
fi


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc %{pecl_docdir}/%{pecl_name}
%doc %{pecl_testdir}/%{pecl_name}
%{pecl_xmldir}/%{name}.xml

%{php_extdir}/%{pecl_name}.so
%config(noreplace) %{php_inidir}/%{pecl_name}.ini

%if %{with_zts}
%{php_ztsextdir}/%{pecl_name}.so
%config(noreplace) %{php_ztsinidir}/%{pecl_name}.ini
%endif


%changelog
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

