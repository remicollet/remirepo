# spec file for php-pecl-ncurses
#
# Copyright (c) 2007-2014 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/3.0/
#
# Please, preserve the changelog entries
#
%{!?php_inidir:  %global php_inidir   %{_sysconfdir}/php.d}
%{!?__pecl:      %global __pecl       %{_bindir}/pecl}
%{!?__php:       %global __php        %{_bindir}/php}

%global pecl_name ncurses
%global with_zts  0%{?__ztsphp:1}

Summary:      Terminal screen handling and optimization package
Name:         php-pecl-ncurses
Version:      1.0.2
Release:      5%{?dist}%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}
License:      PHP
Group:        Development/Languages
URL:          http://pecl.php.net/package/ncurses

Source:       http://pecl.php.net/get/%{pecl_name}-%{version}.tgz

# https://bugs.php.net/65862 - Please Provides LICENSE file
# URL from ncurses.c
Source1:      http://www.php.net/license/3_01.txt

BuildRoot:    %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: php-devel
BuildRequires: php-simplexml
BuildRequires: ncurses-devel
BuildRequires: php-pear

Requires(post): %{__pecl}
Requires(postun): %{__pecl}
Requires:     php(zend-abi) = %{php_zend_api}
Requires:     php(api) = %{php_core_api}

Obsoletes:    php-ncurses < 5.3.0
Provides:     php-ncurses = 5.3.0
Provides:     php-ncurses%{?_isa} = 5.3.0
Provides:     php-pecl(%{pecl_name}) = %{version}
Provides:     php-pecl(%{pecl_name})%{?_isa} = %{version}

# Other third party repo stuff
Obsoletes:     php53-pecl-%{pecl_name}
Obsoletes:     php53u-pecl-%{pecl_name}
%if "%{php_version}" > "5.4"
Obsoletes:     php54-pecl-%{pecl_name}
%endif
%if "%{php_version}" > "5.5"
Obsoletes:     php55u-pecl-%{pecl_name}
%endif
%if "%{php_version}" > "5.6"
Obsoletes:     php56u-pecl-%{pecl_name}
%endif

%if 0%{?fedora} < 20 && 0%{?rhel} < 7
# Filter shared private
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}
%endif


%description
ncurses (new curses) is a free software emulation of curses in
System V Rel 4.0 (and above). It uses terminfo format, supports
pads, colors, multiple highlights, form characters and function
key mapping. Because of the interactive nature of this library,
it will be of little use for writing Web applications, but may
be useful when writing scripts meant using PHP from the command
line.



%prep 
%setup -c -q

cat >%{pecl_name}.ini << 'EOF'
; Enable %{pecl_name} extension module
extension=%{pecl_name}.so
EOF

mv %{pecl_name}-%{version} NTS

cp %{SOURCE1} NTS/LICENSE

%if %{with_zts}
cp -r NTS ZTS
%endif


%build
cd NTS
%{_bindir}/phpize
%configure --enable-ncursesw \
           --with-php-config=%{_bindir}/php-config
make %{?_smp_mflags}

%if %{with_zts}
cd ../ZTS
%{_bindir}/zts-phpize
%configure --enable-ncursesw \
           --with-php-config=%{_bindir}/zts-php-config
make %{?_smp_mflags}
%endif


%install
rm -rf %{buildroot}

make -C NTS install INSTALL_ROOT=%{buildroot}

# Install XML package description
install -Dpm 644 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml

# install config file
install -Dpm 644 %{pecl_name}.ini %{buildroot}%{php_inidir}/%{pecl_name}.ini

%if %{with_zts}
make -C ZTS install INSTALL_ROOT=%{buildroot}
install -Dpm 644 %{pecl_name}.ini %{buildroot}%{php_ztsinidir}/%{pecl_name}.ini
%endif

# Test & Documentation
for i in $(grep 'role="test"' package.xml | sed -e 's/^.*name="//;s/".*$//')
do install -Dpm 644 NTS/$i %{buildroot}%{pecl_testdir}/%{pecl_name}/$i
done
for i in LICENSE $(grep 'role="doc"' package.xml | sed -e 's/^.*name="//;s/".*$//')
do install -Dpm 644 NTS/$i %{buildroot}%{pecl_docdir}/%{pecl_name}/$i
done


%check
cd NTS

TEST_PHP_EXECUTABLE=%{__php} \
REPORT_EXIT_STATUS=1 \
NO_INTERACTION=1 \
%{__php} run-tests.php \
    -n -q \
    -d extension_dir=modules \
    -d extension=%{pecl_name}.so \

%if %{with_zts}
cd ../ZTS

TEST_PHP_EXECUTABLE=%{__ztsphp} \
REPORT_EXIT_STATUS=1 \
NO_INTERACTION=1 \
%{__ztsphp} run-tests.php \
    -n -q \
    -d extension_dir=modules \
    -d extension=%{pecl_name}.so \
%endif


%clean
rm -rf %{buildroot}


%post
%{pecl_install} %{pecl_xmldir}/%{name}.xml >/dev/null || :


%postun
if [ $1 -eq 0 ] ; then
    %{pecl_uninstall} %{pecl_name} >/dev/null || :
fi


%files
%defattr(-, root, root, -)
%doc %{pecl_docdir}/%{pecl_name}
%doc %{pecl_testdir}/%{pecl_name}
%config(noreplace) %{php_inidir}/%{pecl_name}.ini
%{php_extdir}/%{pecl_name}.so
%{pecl_xmldir}/%{name}.xml
%if %{with_zts}
%config(noreplace) %{php_ztsinidir}/%{pecl_name}.ini
%{php_ztsextdir}/%{pecl_name}.so
%endif


%changelog
* Sat Mar  8 2014 Remi Collet <remi@fedoraproject.org> - 1.0.2-2
- cleanups
- install doc in pecl_docdir
- install tests in pecl_testdir

* Fri Nov 30 2012 Remi Collet <remi@fedoraproject.org> - 1.0.2-1.1
- rebuild

* Sun Jun 24 2012 Remi Collet <remi@fedoraproject.org> - 1.0.2-1
- update to 1.0.2

* Sun Nov 13 2011 Remi Collet <remi@fedoraproject.org> - 1.0.1-4
- build against php 5.4

* Thu Oct 06 2011 Remi Collet <Fedora@FamilleCollet.com> - 1.0.1-3
- ZTS extension
- spec cleanups

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Oct 23 2010  Remi Collet <Fedora@FamilleCollet.com> - 1.0.1-2
- add filter_provides to avoid private-shared-object-provides ncurses.so

* Sat Dec 19 2009 Remi Collet <Fedora@FamilleCollet.com> 1.0.1-1
- update to 1.0.1
- enable wide char support

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Jul 12 2009 Remi Collet <Fedora@FamilleCollet.com> 1.0.0-2
- add %%check for minimal test.

* Sun Jul 12 2009 Remi Collet <Fedora@FamilleCollet.com> 1.0.0-1
- initial RPM (for php 5.3.0)
- ncurses-1.0.0-php53.patch 

