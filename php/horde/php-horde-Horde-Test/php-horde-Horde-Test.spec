# remirepo/fedora spec file for php-horde-Horde-Test
#
# Copyright (c) 2012-2017 Nick Bebout, Remi Collet
#
# License: MIT
# https://fedoraproject.org/wiki/Licensing:MIT#Modern_Style_with_sublicense
#
# Please, preserve the changelog entries
#
%{!?__pear:       %global __pear       %{_bindir}/pear}
%global pear_name    Horde_Test
%global pear_channel pear.horde.org

Name:           php-horde-Horde-Test
Version:        2.6.2
Release:        2%{?dist}
Summary:        Horde testing base classes

Group:          Development/Libraries
License:        LGPLv2
URL:            http://%{pear_channel}
Source0:        http://%{pear_channel}/get/%{pear_name}-%{version}.tgz

# Use unbundled PHPUnit
Patch0:         %{pear_name}-rpm.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch:      noarch
BuildRequires:  php(language) >= 5.3.0
BuildRequires:  php-pear(PEAR) >= 1.7.0
BuildRequires:  php-channel(%{pear_channel})

Requires(post): %{__pear}
Requires(postun): %{__pear}
# From package.xml, required
Requires:       php(language) >= 5.3.0
Requires:       php-dom
Requires:       php-json
Requires:       php-pear(PEAR) >= 1.7.0
Requires:       php-channel(%{pear_channel})
Requires:       php-pear(%{pear_channel}/Horde_Support) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Support) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Util) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Util) <  3.0.0
# From package.xml, optional
Requires:       php-pear(%{pear_channel}/Horde_Cli) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Cli) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Log) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Log) <  3.0.0
# From phpcompatinfo report for version 2.4.0
Requires:       php-pcre
Requires:       php-pdo
Requires:       php-spl
# Required as we drop bundled copy
Requires:       php-phpunit-PHPUnit >= 3.5.0

Provides:       php-pear(%{pear_channel}/%{pear_name}) = %{version}
Provides:       php-composer(horde/horde-test) = %{version}


%description
Horde-specific PHPUnit base classes.


%prep
%setup -q -c

cd %{pear_name}-%{version}
%patch0 -p1 -b .rpm

# Don't install bundled PHPUnit
# Don't check md5sum for patched files
sed -e '/bundle\/vendor/d' \
    -e '/Autoload.php/s/md5sum="[^"]*"//' \
    -e '/AllTests.php/s/md5sum="[^"]*"//' \
   ../package.xml >%{name}.xml
touch -r ../package.xml %{name}.xml


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
%{pear_phpdir}/Horde/Test


%changelog
* Mon Mar 20 2017 Remi Collet <remi@remirepo.net> - 2.6.2-2
- EL-6 rebuild

* Mon Feb 27 2017 Remi Collet <remi@fedoraproject.org> - 2.6.2-1
- Update to 2.6.2

* Wed Jul 13 2016 Remi Collet <remi@fedoraproject.org> - 2.6.1-1
- Update to 2.6.1

* Tue Feb 02 2016 Remi Collet <remi@fedoraproject.org> - 2.6.0-1
- Update to 2.6.0

* Tue Apr 14 2015 Remi Collet <remi@fedoraproject.org> - 2.5.1-1
- Update to 2.5.1 (no change)

* Wed Feb 11 2015 Remi Collet <remi@fedoraproject.org> - 2.5.0-1
- Update to 2.5.0

* Tue Jan 13 2015 Remi Collet <remi@fedoraproject.org> - 2.4.8-1
- Update to 2.4.8 (no change)
- add provides php-composer(horde/horde-test)

* Mon Dec 29 2014 Remi Collet <remi@fedoraproject.org> - 2.4.7-1
- Update to 2.4.7

* Tue Nov 18 2014 Remi Collet <remi@fedoraproject.org> - 2.4.6-1
- Update to 2.4.6

* Mon Nov 10 2014 Remi Collet <remi@fedoraproject.org> - 2.4.5-2
- add upstream patch to fix test failure in turba
  and kronolith, thanks to Koschei

* Tue Oct 28 2014 Remi Collet <remi@fedoraproject.org> - 2.4.5-1
- Update to 2.4.5

* Thu Oct 02 2014 Remi Collet <remi@fedoraproject.org> - 2.4.4-1
- Update to 2.4.4

* Sat Aug 30 2014 Remi Collet <remi@fedoraproject.org> - 2.4.3-1
- Update to 2.4.3

* Mon Jul 07 2014 Remi Collet <remi@fedoraproject.org> - 2.4.2-1
- Update to 2.4.2 (no change)

* Tue May 06 2014 Remi Collet <remi@fedoraproject.org> - 2.4.1-1
- Update to 2.4.1

* Tue May 06 2014 Remi Collet <remi@fedoraproject.org> - 2.4.0-1
- Update to 2.4.0
- drop bundled PHPUnit and use system one

* Sat May 03 2014 Remi Collet <remi@fedoraproject.org> - 2.3.1-1
- Update to 2.3.1

* Tue Mar 11 2014 Remi Collet <remi@fedoraproject.org> - 2.3.0-1
- Update to 2.3.0

* Sat Dec 07 2013 Remi Collet <remi@fedoraproject.org> - 2.2.6-1
- Update to 2.2.6 (stable)

* Tue Nov 12 2013 Remi Collet <remi@fedoraproject.org> - 2.2.5-1
- Update to 2.2.5

* Mon Oct 28 2013 Remi Collet <remi@fedoraproject.org> - 2.2.4-1
- Update to 2.2.4

* Tue Aug 27 2013 Remi Collet <remi@fedoraproject.org> - 2.2.3-1
- Update to 2.2.3

* Tue May 07 2013 Remi Collet <remi@fedoraproject.org> - 2.2.2-1
- Update to 2.2.2

* Wed Mar 06 2013 Remi Collet <remi@fedoraproject.org> - 2.2.1-1
- Update to 2.2.1

* Tue Feb 12 2013 Remi Collet <remi@fedoraproject.org> - 2.2.0-1
- Update to 2.2.0

* Sat Nov 17 2012 Remi Collet <RPMS@FamilleCollet.com> - 2.1.0-1
- Update to 2.1.0 for remi repo

* Thu Nov  1 2012 Remi Collet <RPMS@FamilleCollet.com> - 2.0.0-1
- Update to 2.0.0 for remi repo

* Mon Jun 25 2012 Nick Bebout <nb@fedoraproject.org> - 1.3.0-3
- Fix requires

* Wed Jun 20 2012 Nick Bebout <nb@fedoraproject.org> - 1.3.0-2
- Fix packaging issues

* Sat Jan 28 2012 Nick Bebout <nb@fedoraproject.org> - 1.3.0-1
- Initial package
