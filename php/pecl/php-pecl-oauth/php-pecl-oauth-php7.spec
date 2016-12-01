# remirepo spec file for php-pecl-oauth
# with SCL compatibility, from Fedora:
#
# Fedora spec file for php-pecl-oauth
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please, preserve the changelog entries
#
%if 0%{?scl:1}
%global sub_prefix %{scl_prefix}
%scl_package       php-pecl-oauth
%endif

%global pecl_name   oauth
%global with_zts    0%{!?_without_zts:%{?__ztsphp:1}}
%global ini_name    40-%{pecl_name}.ini

Name:           %{?sub_prefix}php-pecl-oauth
Version:        2.0.2
Release:        3%{?dist}%{!?scl:%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}}
Summary:        PHP OAuth consumer extension
Group:          Development/Languages
License:        BSD
URL:            http://pecl.php.net/package/oauth
Source0:        http://pecl.php.net/get/%{pecl_name}-%{version}.tgz

BuildRequires:  %{?scl_prefix}php-devel >= 7
BuildRequires:  %{?scl_prefix}php-pear
BuildRequires:  pcre-devel
BuildRequires:  libcurl-devel

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

%if "%{?vendor}" == "Remi Collet" && 0%{!?scl:1}
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
# Filter shared private
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}
%endif


%description
OAuth is an authorization protocol built on top of HTTP which allows 
applications to securely access data without having to store
user names and passwords.

Documentation: http://php.net/oauth

Package built for PHP %(%{__php} -r 'echo PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')%{?scl: as Software Collection (%{scl} by %{?scl_vendor}%{!?scl_vendor:rh})}.


%prep
%setup -q -c

mv %{pecl_name}-%{version} NTS

# Don't install/register tests
sed -e 's/role="test"/role="src"/' \
    %{?_licensedir:-e '/LICENSE/s/role="doc"/role="src"/' } \
    -i package.xml

# Sanity check, really often broken
extver=$(sed -n '/#define PHP_OAUTH_VERSION/{s/.* //;s/".*$//;p}' NTS/php_oauth.h)
if test "x${extver}" != "x%{version}"; then
   : Error: Upstream extension version is ${extver}, expecting %{version}.
   exit 1
fi

cat >%{ini_name} << 'EOF'
; Enable %{pecl_name} extension module
extension=%{pecl_name}.so
EOF

%if %{with_zts}
# duplicate for ZTS build
cp -pr NTS ZTS
%endif


%build
cd NTS
%{_bindir}/phpize
%configure --with-php-config=%{_bindir}/php-config
make %{?_smp_mflags}

%if %{with_zts}
cd ../ZTS
%{_bindir}/zts-phpize
%configure --with-php-config=%{_bindir}/zts-php-config
make %{?_smp_mflags}
%endif


%install
make install -C NTS INSTALL_ROOT=%{buildroot}

# Drop in the bit of configuration
install -D -m 644 %{ini_name} %{buildroot}%{php_inidir}/%{ini_name}

# Install XML package description
install -D -m 644 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml

%if %{with_zts}
make install -C ZTS INSTALL_ROOT=%{buildroot}
install -D -m 644 %{ini_name} %{buildroot}%{php_ztsinidir}/%{ini_name}
%endif

# Documentation
cd NTS
for i in $(grep 'role="doc"' ../package.xml | sed -e 's/^.*name="//;s/".*$//')
do install -Dpm 644 $i %{buildroot}%{pecl_docdir}/%{pecl_name}/$i
done


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
: Minimal load test for NTS extension
%{__php} -n \
    -d extension=%{buildroot}%{php_extdir}/%{pecl_name}.so \
    --modules | grep OAuth

%if %{with_zts}
: Minimal load test for ZTS extension
%{__ztsphp} -n \
    -d extension=%{buildroot}%{php_ztsextdir}/%{pecl_name}.so \
    --modules | grep OAuth
%endif


%files
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
* Thu Dec  1 2016 Remi Collet <remi@fedoraproject.org> - 2.0.2-3
- rebuild with PHP 7.1.0 GA

* Wed Sep 14 2016 Remi Collet <remi@fedoraproject.org> - 2.0.2-2
- rebuild for PHP 7.1 new API version

* Mon Jun 20 2016 Remi Collet <rcollet@redhat.com> - 2.0.2-1
- update to 2.0.2

* Fri Mar 11 2016 Remi Collet <rcollet@redhat.com> - 2.0.1-1
- update to 2.0.1

* Sun Mar  6 2016 Remi Collet <rcollet@redhat.com> - 2.0.0-2
- adapt for F24

* Sun Jan  3 2016 Remi Collet <rcollet@redhat.com> - 2.0.0-1
- update to 2.0.0 (php 7, stable)

* Tue Jun 23 2015 Remi Collet <rcollet@redhat.com> - 1.2.3-10
- allow build against rh-php56 (as more-php56)

* Fri Jan 23 2015 Remi Collet <remi@fedoraproject.org> - 1.2.3-9
- fix %%postun scriplet

* Thu Jan 22 2015 Remi Collet <remi@fedoraproject.org> - 1.2.3-8
- bump release
- drop runtime dependency on pear, new scriptlets

* Wed Dec 24 2014 Remi Collet <remi@fedoraproject.org> - 1.2.3-7.1
- Fedora 21 SCL mass rebuild

* Mon Aug 25 2014 Remi Collet <rcollet@redhat.com> - 1.2.3-7
- improve SCL build

* Wed Apr 16 2014 Remi Collet <remi@fedoraproject.org> - 1.2.3-6
- add numerical prefix to extension configuration file (php 5.6)

* Wed Mar 19 2014 Remi Collet <rcollet@redhat.com> - 1.2.3-5
- allow SCL build

* Wed Mar 12 2014 Remi Collet <remi@fedoraproject.org> - 1.2.3-4
- cleanups
- move doc in pecl_docdir

* Fri Nov 30 2012 Remi Collet <remi@fedoraproject.org> - 1.2.3-1.1
- also provides php-oauth

* Tue Oct  2 2012 Remi Collet <remi@fedoraproject.org> - 1.2.3-1
- update to 1.2.3

* Tue Sep  4 2012 Remi Collet <remi@fedoraproject.org> - 1.2.2-4
- EL rebuild

* Sun Nov 13 2011 Remi Collet <remi@fedoraproject.org> - 1.2.2-3
- build against php 5.4

* Tue Oct 04 2011 Remi Collet <RPMS@FamilleCollet.com> - 1.2.2-2
- ZTS extension

* Fri Jul 22 2011 Remi Collet <RPMS@FamilleCollet.com> - 1.2.2-1
- update to 1.2.2

* Fri Jul 22 2011 Remi Collet <RPMS@FamilleCollet.com> - 1.2.1-1
- rebuild for remi repo

* Fri Jul 22 2011 F. Kooman <fkooman@tuxed.net> - 1.2.1-1
- update to 1.2.1 (RHBZ #724872). See
  http://pecl.php.net/package-changelog.php?package=oauth&release=1.2.1

* Mon Jul 04 2011 Remi Collet <RPMS@FamilleCollet.com> - 1.2-1
- rebuild for remi repo

* Sun Jul 03 2011 F. Kooman <fkooman@tuxed.net> - 1.2-1
- upgrade to 1.2

* Sat Jun 25 2011 Remi Collet <RPMS@FamilleCollet.com> - 1.1.0-6
- rebuild for remi repo

* Sun Jun 19 2011 F. Kooman <fkooman@tuxed.net> - 1.1.0-6
- add fix for http://pecl.php.net/bugs/bug.php?id=22337

* Tue Jun 14 2011 Remi Collet <RPMS@FamilleCollet.com> - 1.1.0-5
- rebuild for remi repo

* Mon Jun 13 2011 F. Kooman <fkooman@tuxed.net> - 1.1.0-5
- remove php_apiver marco, was not used

* Mon Jun 13 2011 F. Kooman <fkooman@tuxed.net> - 1.1.0-4
- add minimal check to see if module loads
- fix private-shared-object-provides rpmlint warning

* Sat Jun 11 2011 F. Kooman - 1.1.0-3
- BR pcre-devel

* Sat May 28 2011 F. Kooman - 1.1.0-2
- require libcurl for cURL request engine support 

* Sat May 28 2011 F. Kooman - 1.1.0-1
- initial package 
