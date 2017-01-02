# remirepo/fedora spec file for php-horde-Horde-Compress-Fast
#
# Copyright (c) 2013-2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%{!?__pear:       %global __pear       %{_bindir}/pear}
%global pear_name    Horde_Compress_Fast
%global pear_channel pear.horde.org

Name:           php-horde-Horde-Compress-Fast
Version:        1.1.1
Release:        1%{?dist}
Summary:        Fast Compression Library

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

Requires(post): %{__pear}
Requires(postun): %{__pear}
Requires:       php(language) >= 5.3.0
Requires:       php-pear(PEAR) >= 1.7.0
Requires:       php-pear(%{pear_channel}/Horde_Exception) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Exception) <  3.0.0
Requires:       php-channel(%{pear_channel})
# Optional
Requires:       php-pecl(LZF)
Requires:       php-pecl(%{pear_channel}/horde_lz4)

Provides:       php-pear(%{pear_channel}/%{pear_name}) = %{version}
Provides:       php-composer(horde/horde-compress-fast) = %{version}


%description
Provides compression suitable for packing strings on-the-fly in PHP code
(as opposed to more resource-intensive compression algorithms such as
DEFLATE).


%prep
%setup -q -c
cd %{pear_name}-%{version}
mv ../package.xml %{name}.xml


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


%check
cd %{pear_name}-%{version}/test/$(echo %{pear_name} | sed -e s:_:/:g)
%{_bindir}/phpunit .

if which php70; then
   php70 %{_bindir}/phpunit .
fi


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
%{pear_phpdir}/Horde/Compress
%{pear_testdir}/%{pear_name}


%changelog
* Mon Feb 01 2016 Remi Collet <remi@fedoraproject.org> - 1.1.1-1
- Update to 1.1.1
- PHP 7 compatible version
- run test suite with both PHP 5 and 7 when available

* Thu Jan 08 2015 Remi Collet <remi@fedoraproject.org> - 1.1.0-1
- Update to 1.1.0
- add provides php-composer(horde/horde-compress-fast)

* Tue Sep 16 2014 Remi Collet <remi@fedoraproject.org> - 1.0.3-2
- add optional dependency on horde_lz4

* Wed Jul 09 2014 Remi Collet <remi@fedoraproject.org> - 1.0.3-1
- Update to 1.0.3

* Wed Jul 17 2013 Remi Collet <remi@fedoraproject.org> - 1.0.2-1
- Update to 1.0.2

* Wed Mar 06 2013 Remi Collet <remi@fedoraproject.org> - 1.0.1-1
- New Package
