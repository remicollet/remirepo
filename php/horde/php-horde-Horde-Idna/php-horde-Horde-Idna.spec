# spec file for php-horde-Horde-Idna
#
# Copyright (c) 2015 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/3.0/
#
# Please, preserve the changelog entries
#
%{!?__pear:       %global __pear       %{_bindir}/pear}
%{!?pear_metadir: %global pear_metadir %{pear_phpdir}}
%global pear_name    Horde_Idna
%global pear_channel pear.horde.org

Name:           php-horde-Horde-Idna
Version:        1.0.1
Release:        1%{?dist}
Summary:        IDNA backend normalization package

Group:          Development/Libraries
License:        BSD
URL:            http://www.horde.org/
Source0:        http://%{pear_channel}/get/%{pear_name}-%{version}.tgz

# Use system true/punycode
Patch0:         %{pear_name}-rpm.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php(language) >= 5.3.0
BuildRequires:  php-pear(PEAR) >= 1.7.0
BuildRequires:  php-channel(%{pear_channel})

Requires(post): %{__pear}
Requires(postun): %{__pear}
Requires:       php(language) >= 5.3.0
Requires:       php-pear(PEAR) >= 1.7.0
Requires:       php-channel(%{pear_channel})
Requires:       php-pear(%{pear_channel}/Horde_Exception) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Exception) <  3.0.0
# optional, but not needed as true/punycode is prefered / mandatory:
#   Net_IDNA, Net_IDNA2, mbstring
# unbundled library:
Requires:       php-composer(true/punycode) >= 1.0.1

Provides:       php-pear(%{pear_channel}/%{pear_name}) = %{version}


%description
Normalized access to various backends providing IDNA (Internationalized
Domain Names in Applications) support.


%prep
%setup -q -c
cd %{pear_name}-%{version}

%patch0 -p1 -b .rpm

# don't install bundled library
# don't check checksum of patched file
sed -e '/bundle/d' \
    -e '/Idna.php/s/md5sum="[^"]*"//' \
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
        %{pear_channel}/%{pear_name} >/dev/null || :
fi


%files
%defattr(-,root,root,-)
%doc %{pear_docdir}/%{pear_name}
%{pear_xmldir}/%{name}.xml
%{pear_phpdir}/Horde/Idna/
%{pear_phpdir}/Horde/Idna.php


%changelog
* Wed Jan 07 2015 Remi Collet <remi@fedoraproject.org> - 1.0.1-1
- Update to 1.0.1

* Wed Jan  7 2015 Remi Collet <remi@fedoraproject.org> - 1.0.0-1
- New Package