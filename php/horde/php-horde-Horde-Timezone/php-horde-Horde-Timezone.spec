# spec file for php-horde-Horde-Timezone
#
# Copyright (c) 2013 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/3.0/
#
# Please, preserve the changelog entries
#
%{!?pear_metadir: %global pear_metadir %{pear_phpdir}}
%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name    Horde_Timezone
%global pear_channel pear.horde.org

Name:           php-horde-Horde-Timezone
Version:        1.0.4
Release:        1%{?dist}
Summary:        Timezone library

Group:          Development/Libraries
# missing COPYING file
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
BuildRequires:  php-pear(%{pear_channel}/Horde_Date) >= 2.0.0
BuildRequires:  php-pear(%{pear_channel}/Horde_Icalendar) >= 2.0.0

Requires(post): %{__pear}
Requires(postun): %{__pear}
Requires:       php(language) >= 5.3.0
Requires:       php-pcre
Requires:       php-pear(PEAR) >= 1.7.0
Requires:       php-channel(%{pear_channel})
Requires:       php-pear(%{pear_channel}/Horde_Date) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Date) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Icalendar) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Icalendar) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Vfs) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Vfs) < 3.0.0

Provides:       php-pear(%{pear_channel}/%{pear_name}) = %{version}


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
src=$(pwd)/%{pear_name}-%{version}
cd %{pear_name}-%{version}/test/$(echo %{pear_name} | sed -e s:_:/:g)
phpunit \
    -d include_path=$src/lib:.:%{pear_phpdir} \
    -d date.timezone=UTC \
    .


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
* Mon Oct 28 2013 Remi Collet <remi@fedoraproject.org> - 1.0.4-1
- Update to 1.0.4

* Fri Jun 07 2013 Remi Collet <remi@fedoraproject.org> - 1.0.3-2
- BR Horde_Icalendar for test

* Tue May 07 2013 Remi Collet <remi@fedoraproject.org> - 1.0.3-1
- Update to 1.0.3

* Tue Jan 29 2013 Remi Collet <remi@fedoraproject.org> - 1.0.2-1
- Update to 1.0.2 for remi repo
- license now provided http://bugs.horde.org/ticket/11967
- new test layout

* Thu Nov 22 2012 Remi Collet <remi@fedoraproject.org> - 1.0.1-1
- Initial package
