# remirepo/fedora spec file for php-horde-Horde-Dav
#
# Copyright (c) 2013-2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%{!?__pear:       %global __pear       %{_bindir}/pear}
%global pear_name    Horde_Dav
%global pear_channel pear.horde.org
# See https://fedorahosted.org/fpc/ticket/571
# sabre/dav bundle temporary exception in Horde
%global with_sabre   0

Name:           php-horde-Horde-Dav
Version:        1.1.4
Release:        1%{?dist}
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
BuildRequires:  gettext

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
Requires:       php-pear(%{pear_channel}/Horde_Http) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Http) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Stream) >= 1.2.0
Requires:       php-pear(%{pear_channel}/Horde_Stream) <  2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Translation) >= 2.2.0
Requires:       php-pear(%{pear_channel}/Horde_Translation) <  3.0.0
%if %{with_sabre}
# php-sabredav-Sabre_DAV is 1.7, php-sabre-dav is 1.8
Requires:       php-sabre-dav  >= 1.8.10
%else
Obsoletes:      php-sabredav-Sabre_CalDAV                 < 1:1.8
Provides:       php-sabredav-Sabre_CalDAV                 = 1:1.8.7
Provides:       php-pear(pear.sabredav.org/Sabre_CalDAV)  =   1.8.7
Obsoletes:      php-sabredav-Sabre_CardDAV                < 1:1.8
Provides:       php-sabredav-Sabre_CardDAV                = 1:1.8.7
Provides:       php-pear(pear.sabredav.org/Sabre_CardDAV) =   1.8.7
Obsoletes:      php-sabredav-Sabre_DAV                    < 1:1.8
Provides:       php-sabredav-Sabre_DAV                    = 1:1.8.12
Provides:       php-pear(pear.sabredav.org/Sabre_DAV)     =   1.8.12
Obsoletes:      php-sabredav-Sabre_DAVACL                 < 1:1.8
Provides:       php-sabredav-Sabre_DAVACL                 = 1:1.8.7
Provides:       php-pear(ppear.sabredav.org/Sabre_HTTP)   =   1.8.7
Obsoletes:      php-sabredav-Sabre_HTTP                   < 1:1.8
Provides:       php-sabredav-Sabre_HTTP                   = 1:1.8.12
Provides:       php-pear(pear.sabredav.org/Sabre_HTTP)    =   1.8.12
%endif
# php-sabredav-Sabre_VObject is 2.1, php-sabre-vobject is  3.1
Requires:       php-pear(Sabre_VObject) >= 2.1.7
# For rpmclassmap
Requires:       php-horde-Horde-Autoloader >= 2.1.1-3

Provides:       php-pear(%{pear_channel}/%{pear_name}) = %{version}


%description
This package contains all Horde-specific wrapper classes for the Sabre DAV
library.

%prep
%setup -q -c
cd %{pear_name}-%{version}

# Don't use bunled Sabre library
# Don't install .po and .pot files
# Remove checksum for .mo, as we regenerate them

sed -e '/%{pear_name}.po/d' \
    -e '/%{pear_name}.mo/s/md5sum=.*name=/name=/' \
%if %{with_sabre}
    -e '/sabre/d' \
%else
    -e '/vobject/d' \
    -e '/LICENSE/s/role="php"/role="doc"/' \
%endif
    ../package.xml >%{name}.xml
touch -r ../package.xml %{name}.xml

cat << 'EOF' | tee rpmclassmap.php
<?php
return array(
%if %{with_sabre}
   '/^Sabre\\\\/'            => '%{_datadir}/php/Sabre',
%else
   '/^Sabre\\\\/'            => '%{pear_phpdir}/Sabre',
%endif
   '/^Sabre\\\\VObject\\\\/' => '%{pear_phpdir}/Sabre/VObject'
);
EOF


%build
cd %{pear_name}-%{version}

# Regenerate the locales
for po in $(find locale -name \*.po)
do
   msgfmt $po -o $(dirname $po)/$(basename $po .po).mo
done


%install
rm -rf %{buildroot}
cd %{pear_name}-%{version}
%{__pear} install --nodeps --packagingroot %{buildroot} %{name}.xml

# Clean up unnecessary files
rm -rf %{buildroot}%{pear_metadir}/.??*

# Install XML package description
mkdir -p %{buildroot}%{pear_xmldir}
install -pm 644 %{name}.xml %{buildroot}%{pear_xmldir}

# RPM classmap for Horde_Autoloader.php
install -pm 644 rpmclassmap.php %{buildroot}%{pear_phpdir}/Horde/Dav/rpmclassmap.php

for loc in locale/{??,??_??}
do
    lang=$(basename $loc)
    test -d %{buildroot}%{pear_datadir}/%{pear_name}/$loc \
         && echo "%%lang(${lang%_*}) %{pear_datadir}/%{pear_name}/$loc"
done | tee ../%{pear_name}.lang


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


%files -f %{pear_name}.lang
%defattr(-,root,root,-)
%doc %{pear_docdir}/%{pear_name}
%{pear_xmldir}/%{name}.xml
%if ! %{with_sabre}
%{pear_phpdir}/Sabre
%endif
%{pear_phpdir}/Horde/Dav
%dir %{pear_datadir}/%{pear_name}
%dir %{pear_datadir}/%{pear_name}/locale
%{pear_datadir}/%{pear_name}/migration



%changelog
* Thu Dec 15 2016 Remi Collet <remi@fedoraproject.org> - 1.1.4-1
- Update to 1.1.4
- Update bundled SabreDAV to 1.8.12

* Tue Apr 05 2016 Remi Collet <remi@fedoraproject.org> - 1.1.3-1
- Update to 1.1.3

* Thu Sep 24 2015 Remi Collet <remi@fedoraproject.org> - 1.1.2-3
- bundle sabre/dav libraries (not vobject)

* Wed Dec 03 2014 Remi Collet <remi@fedoraproject.org> - 1.1.2-1
- Update to 1.1.2
- add dependency on Horde_Translation

* Wed Oct 29 2014 Remi Collet <remi@fedoraproject.org> - 1.1.1-1
- Update to 1.1.1

* Thu Oct 02 2014 Remi Collet <remi@fedoraproject.org> - 1.1.0-1
- Update to 1.1.0

* Sat Jun  7 2014 Remi Collet <remi@fedoraproject.org> - 1.0.7-2
- requires Horde_Http

* Wed Jun 04 2014 Remi Collet <remi@fedoraproject.org> - 1.0.7-1
- Update to 1.0.7

* Mon May 26 2014 Remi Collet <remi@fedoraproject.org> - 1.0.6-1
- Update to 1.0.6

* Thu May 22 2014 Remi Collet <remi@fedoraproject.org> - 1.0.5-1
- Update to 1.0.5
- raise dependencies on SabreDAV 1.8.10, VObject 2.1.4
- generate local during build

* Tue Mar 04 2014 Remi Collet <remi@fedoraproject.org> - 1.0.4-1
- Update to 1.0.4
- raise dependency on sabre-dav 1.8.9

* Thu Feb 20 2014 Remi Collet <remi@fedoraproject.org> - 1.0.3-3
- requires php-pear(Sabre_VObject) (as php-sabre-vobject is 3.1)

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
