# remirepo spec file for php-phpseclib-crypt-rsa, from:
#
# Fedora spec file for php-phpseclib-crypt-rsa
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#
%{!?__pear:       %global __pear %{_bindir}/pear}
%global pear_name Crypt_RSA

Name:           php-phpseclib-crypt-rsa
Version:        1.0.5
Release:        1%{?dist}
Summary:        Pure-PHP PKCS#1 (v2.1) compliant implementation of RSA

Group:          Development/Libraries
License:        MIT
URL:            http://phpseclib.sourceforge.net/
Source0:        http://phpseclib.sourceforge.net/get/%{pear_name}-%{version}.tgz

# https://sourceforge.net/p/phpseclib/bugs/4/
Patch0:         %{pear_name}-role.patch

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
# phpcompatinfo, generated from 0.3.5
Requires:       php-date
Requires:       php-pcre
Requires:       php-xml

Provides:       php-pear(phpseclib.sourceforge.net/Crypt_RSA) = %{version}


%description
Pure-PHP PKCS#1 (v2.1) compliant implementation of RSA. Optionally uses
openssl.

%prep
%setup -q -c

cd %{pear_name}-%{version}
sed -e 's/\r//' -i RSA.php
%patch0 -p1 -b .role
sed -e '/RSA.php/s/md5sum="[^"]*"//' \
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
%{pear_phpdir}/Crypt/RSA.php
%dir %{pear_cfgdir}/%{pear_name}
%config(noreplace) %{pear_cfgdir}/%{pear_name}/openssl.cnf


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
- Update to 0.3.9 (no change)

* Sat Sep 13 2014 Remi Collet <remi@fedoraproject.org> - 0.3.8-1
- Update to 0.3.8

* Mon Jul 07 2014 Remi Collet <remi@fedoraproject.org> - 0.3.7-1
- Update to 0.3.7

* Wed Feb 26 2014 Remi Collet <remi@fedoraproject.org> - 0.3.6-1
- Update to 0.3.6

* Fri Jan 24 2014 Remi Collet <rpms@famillecollet.com> - 0.3.5-3
- backport for remi repo

* Thu Jan 09 2014 Adam Williamson <awilliam@redhat.com> - 0.3.5-3
- fix up config file install and use (from Remi Collet)

* Sat Jan  4 2014 Adam Williamson <awilliam@redhat.com> - 0.3.5-2
- various review style cleanups

* Tue Dec 31 2013 Adam Williamson <awilliam@redhat.com> - 0.3.5-1
- initial package (generated with pear make-rpm-spec)
