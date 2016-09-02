# remirepo/fedora spec file for php-horde-Horde-Db
#
# Copyright (c) 2012-2016 Nick Bebout, Remi Collet
#
# License: MIT
# https://fedoraproject.org/wiki/Licensing:MIT#Modern_Style_with_sublicense
#
# Please, preserve the changelog entries
#
%{!?__pear:       %global __pear       %{_bindir}/pear}
%global pear_name    Horde_Db
%global pear_channel pear.horde.org

Name:           php-horde-Horde-Db
Version:        2.3.3
Release:        1%{?dist}
Summary:        Horde Database Libraries

Group:          Development/Libraries
License:        BSD
URL:            http://pear.horde.org
Source0:        http://%{pear_channel}/get/%{pear_name}-%{version}.tgz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch:      noarch
BuildRequires:  php(language) >= 5.3.0
BuildRequires:  php-pear(PEAR) >= 1.7.0
BuildRequires:  php-channel(%{pear_channel})
# To run unit tests
BuildRequires:  php-pear(%{pear_channel}/Horde_Test) >= 2.1.0
BuildRequires:  php-pear(%{pear_channel}/Horde_Cache) >= 2.0.0

Requires(post): %{__pear}
Requires(postun): %{__pear}
Requires:       php(language) >= 5.3.0
Requires:       php-pdo
Requires:       php-hash
Requires:       php-pcre
Requires:       php-spl
Requires:       php-pear(PEAR) >= 1.7.0
Requires:       php-channel(%{pear_channel})
Requires:       php-pear(%{pear_channel}/Horde_Date) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Date) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Exception) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Exception) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Support) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Support) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Util) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Util) <  3.0.0
# Optional
Requires:       php-pear(%{pear_channel}/Horde_Autoloader) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Autoloader) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Cache) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Cache) <  3.0.0

Provides:       php-pear(%{pear_channel}/%{pear_name}) = %{version}
Provides:       php-composer(horde/horde-db) = %{version}


%description
Horde database/SQL abstraction layer


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
cd %{pear_name}-%{version}/test/$(echo %{pear_name} | sed -e s:_:/:g)

# remirepo:11
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
# remirepo:2
fi
exit $ret


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
%{pear_phpdir}/Horde/Db
%{pear_phpdir}/Horde/Db.php
%{pear_testdir}/%{pear_name}
%{_bindir}/horde-db-migrate-component


%changelog
* Fri Sep 02 2016 Remi Collet <remi@fedoraproject.org> - 2.3.3-1
- Update to 2.3.3

* Sun Jul 03 2016 Remi Collet <remi@fedoraproject.org> - 2.3.2-1
- Update to 2.3.2
- drop patch merged upstream

* Mon Jun 27 2016 Remi Collet <remi@fedoraproject.org> - 2.3.1-2
- add patch to drop dependency on ereg

* Tue Feb 02 2016 Remi Collet <remi@fedoraproject.org> - 2.3.1-1
- Update to 2.3.1
- PHP 7 compatible version

* Wed Nov 18 2015 Remi Collet <remi@fedoraproject.org> - 2.3.0-1
- Update to 2.3.0

* Wed Apr 29 2015 Remi Collet <remi@fedoraproject.org> - 2.2.3-1
- Update to 2.2.3
- add provides php-composer(horde/horde-db)

* Tue Nov 18 2014 Remi Collet <remi@fedoraproject.org> - 2.2.2-1
- Update to 2.2.2

* Thu Nov 06 2014 Remi Collet <remi@fedoraproject.org> - 2.2.0-1
- Update to 2.2.0

* Sat Oct 25 2014 Remi Collet <remi@fedoraproject.org> - 2.1.5-1
- Update to 2.1.5

* Thu Oct 02 2014 Remi Collet <remi@fedoraproject.org> - 2.1.4-1
- Update to 2.1.4

* Tue Jun 17 2014 Remi Collet <remi@fedoraproject.org> - 2.1.3-1
- Update to 2.1.3

* Thu May 22 2014 Remi Collet <remi@fedoraproject.org> - 2.1.2-1
- Update to 2.1.2

* Tue Apr 01 2014 Remi Collet <remi@fedoraproject.org> - 2.1.1-1
- Update to 2.1.1

* Tue Mar 04 2014 Remi Collet <remi@fedoraproject.org> - 2.1.0-1
- Update to 2.1.0

* Fri Aug 23 2013 Remi Collet <remi@fedoraproject.org> - 2.0.4-1
- Update to 2.0.4

* Sat May 04 2013 Remi Collet <remi@fedoraproject.org> - 2.0.3-1
- Update to 2.0.3

* Wed Mar 06 2013 Remi Collet <remi@fedoraproject.org> - 2.0.2-1
- Update to 2.0.2
- enable tests during build

* Mon Nov 19 2012 Remi Collet <remi@fedoraproject.org> - 2.0.1-1
- Update to 2.0.1 for remi repo

* Fri Nov  2 2012 Remi Collet <remi@fedoraproject.org> - 2.0.0-1
- Update to 2.0.0 for remi repo

* Thu Jun 21 2012 Nick Bebout <nb@fedoraproject.org> - 1.2.1-1
- Upgrade to 1.2.1

* Sat Jan 28 2012 Nick Bebout <nb@fedoraproject.org> - 1.2.0-1
- Initial package
