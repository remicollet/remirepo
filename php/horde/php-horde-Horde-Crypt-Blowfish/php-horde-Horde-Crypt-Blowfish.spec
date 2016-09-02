# remirepo/fedora spec file for php-horde-Horde-Crypt-Blowfish
#
# Copyright (c) 2013-2016 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%{!?__pear:       %global __pear       %{_bindir}/pear}
%global pear_name    Horde_Crypt_Blowfish
%global pear_channel pear.horde.org

Name:           php-horde-Horde-Crypt-Blowfish
Version:        1.1.2
Release:        1%{?dist}
Summary:        Blowfish Encryption Library

Group:          Development/Libraries
License:        LGPLv2
URL:            http://pear.horde.org
Source0:        http://%{pear_channel}/get/%{pear_name}-%{version}.tgz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php(language) >= 5.3.0
BuildRequires:  php-pear(PEAR) >= 1.7.0
BuildRequires:  php-hash
BuildRequires:  php-mcrypt
BuildRequires:  php-channel(%{pear_channel})
# To run unit tests
BuildRequires:  php-pear(%{pear_channel}/Horde_Test) >= 2.1.0

Requires(post): %{__pear}
Requires(postun): %{__pear}
Requires:       php(language) >= 5.3.0
Requires:       php-hash
Requires:       php-mcrypt
Requires:       php-openssl
Requires:       php-channel(%{pear_channel})
Requires:       php-pear(PEAR) >= 1.7.0
Requires:       php-pear(%{pear_channel}/Horde_Exception) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Exception) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Support) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Support) <  3.0.0

Provides:       php-pear(%{pear_channel}/%{pear_name}) = %{version}
Provides:       php-composer(horde/horde-crypt-blowfish) = %{version}


%description
Provides blowfish encryption/decryption for PHP string data.

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
# remirepo:14
%if 0%{?rhel} == 5
phpunit . || exit 0
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
# dir also owned by Horde_Crypt which is not required
%dir %{pear_phpdir}/Horde/Crypt
%{pear_phpdir}/Horde/Crypt/Blowfish
%{pear_phpdir}/Horde/Crypt/Blowfish.php
%{pear_testdir}/%{pear_name}


%changelog
* Fri Sep 02 2016 Remi Collet <remi@fedoraproject.org> - 1.1.2-1
- Update to 1.1.2

* Tue Feb 02 2016 Remi Collet <remi@fedoraproject.org> - 1.1.1-1
- Update to 1.1.1
- PHP 7 compatible version
- run test suite with both PHP 5 and 7 when available

* Fri May 22 2015 Remi Collet <remi@fedoraproject.org> - 1.1.0-1
- Update to 1.1.0

* Thu Jan 08 2015 Remi Collet <remi@fedoraproject.org> - 1.0.3-1
- Update to 1.0.3
- add provides php-composer(horde/horde-crypt-blowfish)

* Wed Jan  9 2013 Remi Collet <RPMS@FamilleCollet.com> - 1.0.2-1
- Update to 1.0.2 for remi repo
- skip test in EL-5

* Thu Nov 22 2012 Remi Collet <remi@fedoraproject.org> - 1.0.1-1
- Update to 1.0.1 for remi repo (no change)

* Mon Nov 19 2012 Remi Collet <remi@fedoraproject.org> - 1.0.0-1
- Initial package
