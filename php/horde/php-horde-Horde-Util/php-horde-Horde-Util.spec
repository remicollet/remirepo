# remirepo/fedora spec file for php-horde-Horde-Util
#
# Copyright (c) 2012-2016 Nick Bebout, Remi Collet
#
# License: MIT
# https://fedoraproject.org/wiki/Licensing:MIT#Modern_Style_with_sublicense
#
# Please, preserve the changelog entries
#
%{!?__pear:       %global __pear       %{_bindir}/pear}
%global bootstrap    0
%global pear_name    Horde_Util
%global pear_channel pear.horde.org
%if %{bootstrap}
%global with_tests   %{?_with_tests:1}%{!?_with_tests:0}
%else
%global with_tests   %{?_without_tests:0}%{!?_without_tests:1}
%endif

Name:           php-horde-Horde-Util
Version:        2.5.8
Release:        1%{?dist}
Summary:        Horde Utility Libraries

Group:          Development/Libraries
License:        LGPLv2
URL:            http://%{pear_channel}
Source0:        http://%{pear_channel}/get/%{pear_name}-%{version}.tgz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch:      noarch
BuildRequires:  php(language) >= 5.3.0
BuildRequires:  php-pear(PEAR) >= 1.7.0
BuildRequires:  php-channel(%{pear_channel})
%if 0%{?fedora} >= 24
# Used as default LANG for the test suite
BuildRequires:  glibc-langpack-fr
# Used by some tests
BuildRequires:  glibc-langpack-tr
%endif
%if %{with_tests}
# To run unit tests
BuildRequires:  php-pear(%{pear_channel}/Horde_Test) >= 2.1.0
%endif

Requires(post): %{__pear}
Requires(postun): %{__pear}
# From package.xml
Requires:       php(language) >= 5.3.0
Requires:       php-pear(PEAR) >= 1.7.0
Requires:       php-channel(%{pear_channel})
# Optional
Requires:       php-ctype
Requires:       php-filter
Requires:       php-iconv
Requires:       php-intl
Requires:       php-json
Requires:       php-mbstring
Requires:       php-xml
# From phpcompatinfo report for version 2.4.0
Requires:       php-dom
Requires:       php-libxml
Requires:       php-pcre
Requires:       php-session
Requires:       php-spl
# Optional: Horde_Imap_Client not required to reduce build tree

Provides:       php-pear(%{pear_channel}/%{pear_name}) = %{version}
Provides:       php-composer(horde/horde-util) = %{version}


%description
These classes provide functionality useful for all kind of applications.

%prep
%setup -q -c

cd %{pear_name}-%{version}
mv ../package.xml %{name}.xml


%build
cd %{pear_name}-%{version}
# Empty build section, most likely nothing required.


%install
cd %{pear_name}-%{version}
%{__pear} install --nodeps --packagingroot %{buildroot} %{name}.xml

# Clean up unnecessary files
rm -rf %{buildroot}%{pear_metadir}/.??*

# Install XML package description
mkdir -p %{buildroot}%{pear_xmldir}
install -pm 644 %{name}.xml %{buildroot}%{pear_xmldir}


%check
%if %{with_tests}
export LANG=fr_FR.utf8
cd %{pear_name}-%{version}/test/$(echo %{pear_name} | sed -e s:_:/:g)
# remirepo:14
%if 0%{?rhel} == 5
phpunit . || : Test suite result ignored
%else
run=0
ret=0
if which php56; then
   php56 %{_bindir}/phpunit . || ret=1
   run=1
fi
if which php71; then
   php71 %{_bindir}/phpunit . || ret=1
   run=1
fi
if [ $run -eq 0 ]; then
%{_bindir}/phpunit --verbose .
# remirepo:3
fi
exit $ret
%endif
%else
: Test disabled, bootstrap build
%endif


%post
%{__pear} install --nodeps --soft --force --register-only \
    %{pear_xmldir}/%{name}.xml >/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    %{__pear} uninstall --nodeps --ignore-errors --register-only \
        %{pear_channel}/%{pear_name} >/dev/null || :
fi


%files
%defattr(-,root,root,-)
%doc %{pear_docdir}/%{pear_name}
%{pear_xmldir}/%{name}.xml
%{pear_phpdir}/Horde/Array
%{pear_phpdir}/Horde/Array.php
%{pear_phpdir}/Horde/Domhtml.php
%{pear_phpdir}/Horde/String.php
%{pear_phpdir}/Horde/String
%{pear_phpdir}/Horde/Util.php
%{pear_phpdir}/Horde/Variables.php
%{pear_testdir}/%{pear_name}


%changelog
* Sat Jul 02 2016 Remi Collet <remi@fedoraproject.org> - 2.5.8-1
- Update to 2.5.8

* Mon Feb 29 2016 Remi Collet <remi@fedoraproject.org> - 2.5.7-2
- add BR on glibc-langpack-fr, glibc-langpack-tr (F25+)

* Tue Feb 02 2016 Remi Collet <remi@fedoraproject.org> - 2.5.7-1
- Update to 2.5.7
- PHP 7 compatible version
- run test suite with both PHP 5 and 7 when available

* Fri Jul 31 2015 Remi Collet <remi@fedoraproject.org> - 2.5.6-1
- Update to 2.5.6

* Tue Apr 14 2015 Remi Collet <remi@fedoraproject.org> - 2.5.5-1
- Update to 2.5.5

* Tue Mar 03 2015 Remi Collet <remi@fedoraproject.org> - 2.5.4-1
- Update to 2.5.4
- enable the test suite during build

* Wed Feb 11 2015 Remi Collet <remi@fedoraproject.org> - 2.5.3-1
- Update to 2.5.3
- add provides php-composer(horde/horde-util)

* Mon Dec 29 2014 Remi Collet <remi@fedoraproject.org> - 2.5.2-1
- Update to 2.5.2

* Sat Aug 16 2014 Remi Collet <remi@fedoraproject.org> - 2.5.1-1
- Update to 2.5.1

* Mon Aug 11 2014 Remi Collet <remi@fedoraproject.org> - 2.5.0-1
- Update to 2.5.0

* Sat May 03 2014 Remi Collet <remi@fedoraproject.org> - 2.4.0-1
- Update to 2.4.0

* Fri Jun 28 2013 Remi Collet <remi@fedoraproject.org> - 2.3.0-1
- Update to 2.3.0
- requires php-json

* Tue May 07 2013 Remi Collet <remi@fedoraproject.org> - 2.2.2-1
- Update to 2.2.2

* Wed Mar 06 2013 Remi Collet <remi@fedoraproject.org> - 2.2.1-1
- Update to 2.2.1

* Tue Feb 26 2013 Remi Collet <remi@fedoraproject.org> - 2.2.0-1
- Update to 2.2.0

* Tue Feb 12 2013 Remi Collet <remi@fedoraproject.org> - 2.1.0-1
- Update to 2.1.0

* Wed Jan  9 2013 Remi Collet <RPMS@FamilleCollet.com> - 2.0.3-1
- Update to 2.0.3 for remi repo

* Fri Dec 21 2012 Remi Collet <RPMS@FamilleCollet.com> - 2.0.2-1
- Update to 2.0.2 for remi repo

* Sun Dec 16 2012 Remi Collet <RPMS@FamilleCollet.com> - 2.0.1-2
- drop optional dep on Horde_Imap_Client to
  minimize build dependencies (of Horde_Test)

* Mon Nov 19 2012 Remi Collet <RPMS@FamilleCollet.com> - 2.0.1-1
- Update to 2.0.1 for remi repo

* Mon Nov  5 2012 Remi Collet <RPMS@FamilleCollet.com> - 2.0.0-4
- make test optional

* Thu Nov  1 2012 Remi Collet <RPMS@FamilleCollet.com> - 2.0.0-3
- Update to 2.0.0 for remi repo

* Tue Aug 14 2012 Remi Collet <remi@fedoraproject.org> - 1.4.0-3
- rebuilt for new pear_testdir

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 17 2012 Remi Collet <RPMS@FamilleCollet.com> - 1.4.0-1
- Upgrade to 1.4.0, backport for remi repo

* Thu Jul 12 2012 Nick Bebout <nb@fedoraproject.org> - 1.4.0-1
- Update to 1.4.0

* Sat Jun 16 2012 Remi Collet <RPMS@FamilleCollet.com> - 1.3.1-1
- Upgrade to 1.3.1, backport for remi repo

* Thu Jun 14 2012 Nick Bebout <nb@fedoraproject.org> - 1.3.1-1
- Update to 1.3.1

* Thu Mar 22 2012 Remi Collet <RPMS@FamilleCollet.com> - 1.3.0-1
- update to 1.3.0, backport for remi repo

* Wed Mar 21 2012 Nick Bebout <nb@fedoraproject.org> - 1.3.0-1
- Update to 1.3.0

* Mon Feb 20 2012 Remi Collet <RPMS@FamilleCollet.com> - 1.2.0-1
- backport for remi repo

* Sat Jan 28 2012 Nick Bebout <nb@fedoraproject.org> - 1.2.0-1
- Initial package
