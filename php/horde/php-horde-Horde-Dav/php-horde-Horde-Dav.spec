# spec file for php-horde-Horde-Dav
#
# Copyright (c) 2013-2014 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/3.0/
#
# Please, preserve the changelog entries
#
%{!?pear_metadir: %global pear_metadir %{pear_phpdir}}
%{!?__pear:       %global __pear       %{_bindir}/pear}
%global pear_name    Horde_Dav
%global pear_channel pear.horde.org

Name:           php-horde-Horde-Dav
Version:        1.0.3
Release:        2%{?dist}
Summary:        Horde library for WebDAV, CalDAV, CardDAV

Group:          Development/Libraries
License:        BSD
URL:            http://%{pear_channel}
Source0:        http://%{pear_channel}/get/%{pear_name}-%{version}.tgz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php(language) >= 5.3.0
BuildRequires:  php-pear(PEAR) >= 1.7.0
BuildRequires:  php-channel(%{pear_channel})

Requires(post): %{__pear}
Requires(postun): %{__pear}
Requires:       php(language) >= 5.3.0
Requires:       php-spl
Requires:       php-pear(PEAR) >= 1.7.0
Requires:       php-channel(%{pear_channel})
Requires:       php-pear(%{pear_channel}/Horde_Auth) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Auth) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Core) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Core) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Stream) >= 1.2.0
Requires:       php-pear(%{pear_channel}/Horde_Stream) <  2.0.0
Requires:       php-sabre-dav  >= 1.8.7
Requires:       php-sabre-vobject >= 2.1.3

Provides:       php-pear(%{pear_channel}/%{pear_name}) = %{version}


%description
This package contains all Horde-specific wrapper classes for the Sabre DAV
library.

%prep
%setup -q -c
cd %{pear_name}-%{version}

# Don't use bunled Sabre library
sed -e '/sabre/d' \
    ../package.xml >%{name}.xml


%build
cd %{pear_name}-%{version}
# Empty build section, most likely nothing required.


%install
rm -rf %{buildroot}
cd %{pear_name}-%{version}
%{__pear} install --nodeps --packagingroot %{buildroot} %{name}.xml

# Clean up unnecessary files
rm -rf %{buildroot}%{pear_metadir}/.??*

# Install XML package description
mkdir -p %{buildroot}%{pear_xmldir}
install -pm 644 %{name}.xml %{buildroot}%{pear_xmldir}


%clean
rm -rf %{buildroot}


%post
%{__pear} install --nodeps --soft --force --register-only \
    %{pear_xmldir}/%{name}.xml >/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    %{__pear} uninstall --nodeps --ignore-errors --register-only \
        %{pear_name}/%{pear_name} >/dev/null || :
fi


%files
%defattr(-,root,root,-)
%doc %{pear_docdir}/%{pear_name}
%{pear_xmldir}/%{name}.xml
%{pear_phpdir}/Horde/Dav
%{pear_datadir}/%{pear_name}



%changelog
* Fri Jan  3 2014 Remi Collet <remi@fedoraproject.org> - 1.0.3-2
- requires php-sabre-dav and php-sabre-vobject

* Tue Nov 12 2013 Remi Collet <remi@fedoraproject.org> - 1.0.3-1
- Update to 1.0.3

* Wed Jul 17 2013 Remi Collet <remi@fedoraproject.org> - 1.0.2-1
- Update to 1.0.2

* Wed Jul 17 2013 Remi Collet <remi@fedoraproject.org> - 1.0.1-1
- Update to 1.0.1
- raise dependencies for SabreDAV 1.8.6

* Wed Jun  5 2013 Remi Collet <remi@fedoraproject.org> - 1.0.0-1
- update to 1.0.0
- switch from Conflicts to Requires

* Thu May 30 2013 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.3.RC1
- update to 1.0.0RC1

* Tue May  7 2013 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.2.beta1
- fix versions required in sabredav channel

* Tue May  7 2013 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.1.beta1
- initial package