# remirepo/fedora spec file for php-horde-Horde-Timezone
#
# Copyright (c) 2013-2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%{!?__pear:       %global __pear       %{_bindir}/pear}
%global pear_name    Horde_Timezone
%global pear_channel pear.horde.org

Name:           php-horde-Horde-Timezone
Version:        1.1.0
Release:        1%{?dist}
Summary:        Timezone library

Group:          Development/Libraries
License:        LGPLv2
URL:            http://%{pear_channel}
Source0:        http://%{pear_channel}/get/%{pear_name}-%{version}.tgz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php(language) >= 5.3.0
BuildRequires:  php-pear(PEAR) >= 1.7.0
BuildRequires:  php-channel(%{pear_channel})
# To run unit tests
BuildRequires:  php-pear(%{pear_channel}/Horde_Test) >= 2.1.0
BuildRequires:  php-pear(%{pear_channel}/Horde_Date) >= 2.3.0
BuildRequires:  php-pear(%{pear_channel}/Horde_Icalendar) >= 2.0.0

Requires(post): %{__pear}
Requires(postun): %{__pear}
Requires:       php(language) >= 5.3.0
Requires:       php-pcre
Requires:       php-pear(PEAR) >= 1.7.0
Requires:       php-channel(%{pear_channel})
Requires:       php-pear(%{pear_channel}/Horde_Date) >= 2.3.0
Requires:       php-pear(%{pear_channel}/Horde_Date) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Icalendar) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Icalendar) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Vfs) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Vfs) < 3.0.0

Provides:       php-pear(%{pear_channel}/%{pear_name}) = %{version}
Provides:       php-composer(horde/horde-timezone) = %{version}


%description
Library for parsing timezone databases and generating VTIMEZONE iCalendar
components.


%prep
%setup -q -c

cd %{pear_name}-%{version}
cp ../package.xml %{name}.xml


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
ret=0
for cmd in php56 php70 php71 php; do
  if which $cmd; then
    $cmd %{_bindir}/phpunit --verbose . || ret=1
  fi
done
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
%{pear_phpdir}/Horde/Timezone
%{pear_phpdir}/Horde/Timezone.php
%{pear_testdir}/%{pear_name}


%changelog
* Sat Feb 11 2017 Remi Collet <remi@fedoraproject.org> - 1.1.0-1
- Update to 1.1.0

* Mon Mar 21 2016 Remi Collet <remi@fedoraproject.org> - 1.0.11-1
- Update to 1.0.11
- raise dependency on Horde_Date >= 2.3.0

* Tue Feb 02 2016 Remi Collet <remi@fedoraproject.org> - 1.0.10-1
- Update to 1.0.10
- PHP 7 compatible version
- run test suite with both PHP 5 and 7 when available

* Fri Jan 09 2015 Remi Collet <remi@fedoraproject.org> - 1.0.9-1
- Update to 1.0.9
- add provides php-composer(horde/horde-timezone)

* Tue Oct 07 2014 Remi Collet <remi@fedoraproject.org> - 1.0.8-1
- Update to 1.0.8

* Sat Aug 30 2014 Remi Collet <remi@fedoraproject.org> - 1.0.7-1
- Update to 1.0.7

* Fri Apr 04 2014 Remi Collet <remi@fedoraproject.org> - 1.0.6-1
- Update to 1.0.6

* Mon Mar 10 2014 Remi Collet <remi@fedoraproject.org> - 1.0.5-1
- Update to 1.0.5

* Mon Oct 28 2013 Remi Collet <remi@fedoraproject.org> - 1.0.4-1
- Update to 1.0.4

* Fri Jun 07 2013 Remi Collet <remi@fedoraproject.org> - 1.0.3-2
- BR Horde_Icalendar for test

* Tue May 07 2013 Remi Collet <remi@fedoraproject.org> - 1.0.3-1
- Update to 1.0.3

* Tue Jan 29 2013 Remi Collet <remi@fedoraproject.org> - 1.0.2-1
- Update to 1.0.2
- license now provided http://bugs.horde.org/ticket/11967
- new test layout

* Thu Nov 22 2012 Remi Collet <remi@fedoraproject.org> - 1.0.1-1
- Initial package
