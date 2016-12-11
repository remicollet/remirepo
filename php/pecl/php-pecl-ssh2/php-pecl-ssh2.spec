# remirepo spec file for php-pecl-ssh2
# with SCL compatibility
#
# Copyright (c) 2011-2016 Remi Collet
#
# Fedora spec file for php-pecl-ssh2
#
# License: MIT
#
# Please, preserve the changelog entries
#
%if 0%{?scl:1}
%if "%{scl}" == "rh-php56"
%global sub_prefix more-php56-
%else
%global sub_prefix %{scl_prefix}
%endif
%scl_package       php-pecl-ssh2
%endif

%global with_zts  0%{!?_without_zts:%{?__ztsphp:1}}
%global pecl_name ssh2
%if "%{php_version}" < "5.6"
%global ini_name  %{pecl_name}.ini
%else
%global ini_name  40-%{pecl_name}.ini
%endif

Name:           %{?sub_prefix}php-pecl-ssh2
Version:        0.13
Release:        3%{?dist}%{!?scl:%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}}
Summary:        Bindings for the libssh2 library

%global buildver %(pkg-config --silence-errors --modversion libssh2  2>/dev/null || echo 65536)

License:        PHP
Group:          Development/Languages
URL:            http://pecl.php.net/package/ssh2
Source0:        http://pecl.php.net/get/ssh2-%{version}.tgz
Source2:        php-pecl-ssh2-0.10-README

Patch0:         %{pecl_name}-php5628.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  libssh2-devel >= 1.2
BuildRequires:  %{?scl_prefix}php-devel < 7
BuildRequires:  %{?scl_prefix}php-pear

Requires:       %{?scl_prefix}php(zend-abi) = %{php_zend_api}
Requires:       %{?scl_prefix}php(api) = %{php_core_api}
Requires:       libssh2%{?_isa}  >= %{buildver}
%{?_sclreq:Requires: %{?scl_prefix}runtime%{?_sclreq}%{?_isa}}

Provides:       %{?scl_prefix}php-%{pecl_name}               = %{version}
Provides:       %{?scl_prefix}php-%{pecl_name}%{?_isa}       = %{version}
Provides:       %{?scl_prefix}php-pecl(%{pecl_name})         = %{version}
Provides:       %{?scl_prefix}php-pecl(%{pecl_name})%{?_isa} = %{version}
%if "%{?scl_prefix}" != "%{?sub_prefix}"
Provides:       %{?scl_prefix}php-pecl-%{pecl_name}          = %{version}-%{release}
Provides:       %{?scl_prefix}php-pecl-%{pecl_name}%{?_isa}  = %{version}-%{release}
%endif

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
%endif

%if 0%{?fedora} < 20 && 0%{?rhel} < 7
# Filter private shared
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}
%endif


%description
Bindings to the libssh2 library which provide access to resources
(shell, remote exec, tunneling, file transfer) on a remote machine using
a secure cryptographic transport.

Documentation: http://php.net/ssh2

Package built for PHP %(%{__php} -r 'echo PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')%{?scl: as Software Collection (%{scl} by %{?scl_vendor}%{!?scl_vendor:rh})}.


%prep
%setup -c -q

# Don't install/register tests
sed -e 's/role="test"/role="src"/' \
    %{?_licensedir:-e '/LICENSE/s/role="doc"/role="src"/' } \
    -i package.xml

mv %{pecl_name}-%{version} NTS
cd NTS
%patch0 -p1 -b .php7013

extver=$(sed -n '/#define PHP_SSH2_VERSION/{s/.* "//;s/".*$//;p}' php_ssh2.h)
if test "x${extver}" != "x%{version}"; then
   : Error: Upstream version is now ${extver}, expecting %{version}.
   : Update the pdover macro and rebuild.
   exit 1
fi
cd ..

cp %{SOURCE2} README

cat > %{ini_name} << 'EOF'
; Enable ssh2 extension module
extension=ssh2.so
EOF

%if %{with_zts}
: Duplicate source tree for NTS / ZTS build
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
install -Dpm 644 README %{buildroot}%{pecl_docdir}/%{pecl_name}/README

for i in $(grep 'role="doc"' package.xml | sed -e 's/^.*name="//;s/".*$//')
do install -Dpm 644 NTS/$i %{buildroot}%{pecl_docdir}/%{pecl_name}/$i
done



%check
: Minimal load test for NTS extension
%{__php} --no-php-ini \
    --define extension_dir=%{buildroot}%{php_extdir} \
    --define extension=%{pecl_name}.so \
    --modules | grep %{pecl_name}

%if %{with_zts}
: Minimal load test for ZTS extension
%{__ztsphp} --no-php-ini \
    --define extension_dir=%{buildroot}%{php_ztsextdir} \
    --define extension=%{pecl_name}.so \
    --modules | grep %{pecl_name}
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

%config(noreplace) %{php_inidir}/%{ini_name}
%{php_extdir}/ssh2.so

%if %{with_zts}
%config(noreplace) %{php_ztsinidir}/%{ini_name}
%{php_ztsextdir}/ssh2.so
%endif


%changelog
* Thu Nov 10 2016 Remi Collet <remi@fedoraproject.org> - 0.13-3
- add patch for parse_url change in PHP 5.6.28

* Sun Jun 12 2016 Remi Collet <remi@fedoraproject.org> - 0.13-1
- update to 0.13

* Tue Mar  8 2016 Remi Collet <remi@fedoraproject.org> - 0.12-7
- adapt for F24

* Tue Jun 23 2015 Remi Collet <remi@fedoraproject.org> - 0.12-6
- allow build against rh-php56 (as more-php56)
- drop runtime dependency on pear, new scriptlets

* Wed Dec 24 2014 Remi Collet <remi@fedoraproject.org> - 0.12-5.1
- Fedora 21 SCL mass rebuild

* Sat Dec 20 2014 Remi Collet <remi@fedoraproject.org> - 0.12-5
- rebuild for new libssh2 in EL-5
- ensure dependency on libssh2 used at buildtime

* Mon Aug 25 2014 Remi Collet <rcollet@redhat.com> - 0.12-4
- improve SCL build

* Thu Apr 17 2014 Remi Collet <remi@fedoraproject.org> - 0.12-3
- add numerical prefix to extension configuration file (php 5.6)

* Sat Nov 30 2013 Remi Collet <RPMS@FamilleCollet.com> - 0.12-2
- cleanups for Copr
- adap for SCL
- install doc in pecl doc_dir

* Fri Nov 30 2012 Remi Collet <RPMS@FamilleCollet.com> - 0.12-1.1
- also provides php-ssh2

* Thu Oct 18 2012 Remi Collet <RPMS@FamilleCollet.com> - 0.12-1
- update to 0.12
- raise dependency on libssh2 >= 1.2

* Sun Nov 13 2011 Remi Collet <remi@fedoraproject.org> - 0.11.3-2
- build against php 5.4

* Tue Oct 04 2011 Remi Collet <RPMS@FamilleCollet.com> - 0.11.3-1
- update to 0.11.3
- zts extension

* Tue Aug 16 2011 Remi Collet <RPMS@FamilleCollet.com> - 0.11.2-1.1
- EL-5 rebuild for libssh2
- add filter

* Sat Apr 16 2011 Remi Collet <RPMS@FamilleCollet.com> - 0.11.2-1
- update to 0.11.2
- add minimal %%check

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan 14 2010 Chris Weyl <cweyl@alumni.drew.edu> 0.11.0-6
- bump for libssh2 rebuild


* Mon Sep 21 2009 Chris Weyl <cweyl@alumni.drew.edu> - 0.11.0-5
- rebuild for libssh2 1.2

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Jul 12 2009 Remi Collet <Fedora@FamilleCollet.com> - 0.11.0-3
- add ssh2-php53.patch
- rebuild for new PHP 5.3.0 ABI (20090626)

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Dec 20 2008 Itamar Reis Peixoto <itamar@ispbrasil.com.br> 0.11.0-1
- convert package.xml to V2 format, update to 0.11.0 #BZ 476405

* Sat Nov 15 2008 Itamar Reis Peixoto <itamar@ispbrasil.com.br> 0.10-2
- Install pecl xml, license and readme files

* Wed Jul 16 2008 Itamar Reis Peixoto <itamar@ispbrasil.com.br> 0.10-1
- Initial release
