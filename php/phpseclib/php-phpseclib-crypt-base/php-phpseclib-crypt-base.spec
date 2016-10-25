# remirepo spec file for php-phpseclib-crypt-base, from:
#
# Fedora spec file for php-phpseclib-crypt-base
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#
%{!?__pear:       %global __pear %{_bindir}/pear}
%global pear_name Crypt_Base

Name:           php-phpseclib-crypt-base
Version:        1.0.5
Release:        1%{?dist}
Summary:        Base class for symmetric key cryptographic algorithms

Group:          Development/Libraries
License:        MIT License
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
# optional
Requires:       php-mhash
Requires:       php-mcrypt

Provides:       php-pear(phpseclib.sourceforge.net/Crypt_Base) = %{version}


%description
This file is a common dependency required for multiple Crypt_* classes.


%prep
%setup -q -c

cd %{pear_name}-%{version}
mv ../package.xml %{name}.xml


%build
cd %{pear_name}-%{version}
# Empty build section, most likely nothing required.


%install
cd %{pear_name}-%{version}
rm -rf %{buildroot}
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
%defattr(-,root,root,-)
%{pear_xmldir}/%{name}.xml
%{pear_phpdir}/Crypt


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
- Update to 0.3.8 (no change)

* Mon Jul 07 2014 Remi Collet <remi@fedoraproject.org> - 0.3.7-1
- Initial packaging, version 0.3.7
