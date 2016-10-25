# remirepo spec file for php-phpseclib-net-ssh2, from:
#
# Fedora spec file for php-phpseclib-net-ssh2
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#
%{!?__pear:       %global __pear %{_bindir}/pear}
%global pear_name Net_SSH2

Name:           php-phpseclib-net-ssh2
Version:        1.0.5
Release:        1%{?dist}
Summary:        Pure-PHP implementation of SSHv2

Group:          Development/Libraries
License:        MIT
URL:            http://phpseclib.sourceforge.net/
Source0:        http://phpseclib.sourceforge.net/get/%{pear_name}-%{version}.tgz
# From Debian, thanks to David Prévot, adjust for rename of Blowfish
# library to avoid conflict with php-pear-Crypt-Blowfish
Patch0:         php-phpseclib-Net-SSH2-Crypt_Blowfish_conflict.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php-pear(PEAR)
BuildRequires:  php-channel(phpseclib.sourceforge.net)

Requires(post): %{__pear}
Requires(postun): %{__pear}
Requires:       php-pear(PEAR)
Requires:       php-channel(phpseclib.sourceforge.net)
Requires:       php-pear(phpseclib.sourceforge.net/Math_BigInteger) >= 0.3.0
Requires:       php-pear(phpseclib.sourceforge.net/Crypt_Random) >= 0.3.0
Requires:       php-pear(phpseclib.sourceforge.net/Crypt_Hash) >= 0.3.0
Requires:       php-pear(phpseclib.sourceforge.net/Crypt_TripleDES) >= 0.3.0
Requires:       php-pear(phpseclib.sourceforge.net/Crypt_RC4) >= 0.3.0
Requires:       php-pear(phpseclib.sourceforge.net/Crypt_AES) >= 0.3.0
Requires:       php-pear(phpseclib.sourceforge.net/Crypt_Twofish) >= 0.3.0
Requires:       php-pear(phpseclib.sourceforge.net/Crypt_Blowfish) >= 0.3.0
# phpcompatinfo, generated from 0.3.5
Requires:       php-pcre
Requires:       php-xml

Provides:       php-pear(phpseclib.sourceforge.net/Net_SSH2) = %{version}


%description
Pure-PHP implementation of SSHv2.

%prep
%setup -q -c
cd %{pear_name}-%{version}
# Fix line endings of file we're about to patch
sed -e 's/\r//' -i SSH2.php
%patch0 -p1
# Drop md5sum of patched file from the PEAR manifest (or else it'll complain)
sed -e '/SSH2.php/s/md5sum="[^"]*"//' \
    ../package.xml >%{name}.xml
touch -r ../package.xml %{name}.xml


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
%{pear_phpdir}/Net


%changelog
* Tue Oct 25 2016 Remi Collet <remi@fedoraproject.org> - 1.0.5-1
- Update to 1.0.5 (no change)

* Tue Oct 04 2016 Remi Collet <remi@fedoraproject.org> - 1.0.4-1
- Update to 1.0.4

* Fri Sep 02 2016 Remi Collet <remi@fedoraproject.org> - 1.0.3-1
- Update to 1.0.3

* Wed May 11 2016 Remi Collet <remi@fedoraproject.org> - 1.0.2-1
- Update to 1.0.2

* Tue Jan 19 2016 Remi Collet <remi@fedoraproject.org> - 1.0.1-1
- Update to 1.0.1

* Mon Aug 03 2015 Remi Collet <remi@fedoraproject.org> - 1.0.0-1
- Update to 1.0.0

* Tue Feb 10 2015 Remi Collet <remi@fedoraproject.org> - 0.3.10-1
- Update to 0.3.10

* Mon Nov 10 2014 Remi Collet <remi@fedoraproject.org> - 0.3.9-1
- Update to 0.3.9

* Sat Sep 13 2014 Remi Collet <remi@fedoraproject.org> - 0.3.8-1
- Update to 0.3.8

* Mon Jul 07 2014 Remi Collet <remi@fedoraproject.org> - 0.3.7-1
- Update to 0.3.7

* Wed Feb 26 2014 Remi Collet <remi@fedoraproject.org> - 0.3.6-1
- Update to 0.3.6

* Sat Jan 25 2014 Remi Collet <rpms@famillecollet.com> - 0.3.5-3
- backport for remi repo

* Thu Jan 16 2014 Adam Williamson <awilliam@redhat.com> - 0.3.5-3
- fix up the patch for crypt_blowfish rename per review

* Sat Jan  4 2014 Adam Williamson <awilliam@redhat.com> - 0.3.5-2
- various review style cleanups

* Tue Dec 31 2013 Adam Williamson <awilliam@redhat.com> - 0.3.5-1
- initial package (generated with pear make-rpm-spec)
