# remirepo spec file for php-phpseclib-crypt-blowfish, from:
#
# Fedora spec file for php-phpseclib-crypt-blowfish
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#
%{!?__pear:       %global __pear %{_bindir}/pear}
%global pear_name Crypt_Blowfish

Name:           php-phpseclib-crypt-blowfish
Version:        1.0.4
Release:        1%{?dist}
Summary:        Pure-PHP implementation of Blowfish

Group:          Development/Libraries
License:        MIT
URL:            http://phpseclib.sourceforge.net/
Source0:        http://phpseclib.sourceforge.net/get/%{pear_name}-%{version}.tgz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php-pear(PEAR)
BuildRequires:  php-channel(phpseclib.sourceforge.net)

Requires(post): %{__pear}
Requires(postun): %{__pear}
Requires:       php-pear(PEAR)
Requires:       php-channel(phpseclib.sourceforge.net)
Requires:       php-pear(phpseclib.sourceforge.net/Crypt_Hash)
Requires:       php-pear(phpseclib.sourceforge.net/Crypt_Base)

Provides:       php-pear(phpseclib.sourceforge.net/Crypt_Blowfish) = %{version}


%description
Uses mcrypt, if available, and an internal implementation, otherwise.
Incompatible with php-pear-Crypt-Blowfish.

%prep
%setup -q -c
# Rename to avoid conflict with php-pear-Crypt-Blowfish
sed -i -e 's,Blowfish.php" role="php" md5sum=".*",Blowfish-phpseclib.php" role="php",' package.xml
sed -i -e 's,Blowfish.php,Blowfish-phpseclib.php,g' %{pear_name}-%{version}/Blowfish.php
mv %{pear_name}-%{version}/Blowfish.php %{pear_name}-%{version}/Blowfish-phpseclib.php

mv package.xml %{pear_name}-%{version}/%{name}.xml

cd %{pear_name}-%{version}


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
        phpseclib.sourceforge.net/%{pear_name} >/dev/null || :
fi


%files
%defattr(-, root, root, -)
%{pear_xmldir}/%{name}.xml
%{pear_phpdir}/Crypt/Blowfish-phpseclib.php


%changelog
* Tue Oct 04 2016 Remi Collet <remi@fedoraproject.org> - 1.0.4-1
- Update to 1.0.4

* Fri Sep 02 2016 Remi Collet <remi@fedoraproject.org> - 1.0.3-1
- Update to 1.0.3 (no change)

* Wed May 11 2016 Remi Collet <remi@fedoraproject.org> - 1.0.2-1
- Update to 1.0.2 (no change)

* Tue Jan 19 2016 Remi Collet <remi@fedoraproject.org> - 1.0.1-1
- Update to 1.0.1

* Mon Aug 03 2015 Remi Collet <remi@fedoraproject.org> - 1.0.0-1
- Update to 1.0.0

* Tue Feb 10 2015 Remi Collet <remi@fedoraproject.org> - 0.3.10-1
- Update to 0.3.10

* Mon Nov 10 2014 Remi Collet <remi@fedoraproject.org> - 0.3.9-1
- Update to 0.3.9 (no change)

* Sat Sep 13 2014 Remi Collet <remi@fedoraproject.org> - 0.3.8-1
- Update to 0.3.8 (no change)

* Mon Jul 07 2014 Remi Collet <remi@fedoraproject.org> - 0.3.7-1
- Update to 0.3.7

* Wed Feb 26 2014 Remi Collet <remi@fedoraproject.org> - 0.3.6-1
- Update to 0.3.6

* Wed Jan 15 2014 Remi Collet <rpms@famillecollet.com> - 0.3.5-4
- backport for remi repo

* Fri Jan 10 2014 Adam Williamson <awilliam@redhat.com> - 0.3.5-4
- requires crypt-hash, drop ownership of Crypt dir

* Thu Jan 09 2014 Adam Williamson <awilliam@redhat.com> - 0.3.5-3
- improve the rename again

* Sat Jan 04 2014 Adam Williamson <awilliam@redhat.com> - 0.3.5-2
- various review style cleanups
- do the rename better

* Tue Dec 31 2013 Adam Williamson <awilliam@redhat.com> - 0.3.5-1
- initial package (generated with pear make-rpm-spec)
