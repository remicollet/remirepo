# spec file for php-phpseclib-file-asn1
#
# Copyright (c) 2014-2016 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%{!?pear_metadir: %global pear_metadir %{pear_phpdir}}
%{!?__pear:       %global __pear       %{_bindir}/pear}
%global pear_name    File_ASN1
%global pear_channel phpseclib.sourceforge.net

Name:           php-phpseclib-file-asn1
Version:        1.0.2
Release:        1%{?dist}
Summary:        Pure-PHP ASN1 parser

Group:          Development/Libraries
# License text included in the header
License:        MIT
URL:            http://%{pear_channel}
Source0:        http://%{pear_channel}/get/%{pear_name}-%{version}.tgz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php-pear(PEAR)
BuildRequires:  php-channel(%{pear_channel})

Requires(post): %{__pear}
Requires(postun): %{__pear}
Requires:       php-date
Requires:       php-pcre
Requires:       php-pear(PEAR)
Requires:       php-channel(%{pear_channel})

Provides:       php-pear(%{pear_channel}/%{pear_name}) = %{version}


%description
Pure-PHP ASN1 parser.


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
%{pear_xmldir}/%{name}.xml
%{pear_phpdir}/File/


%changelog
* Wed May 11 2016 Remi Collet <remi@fedoraproject.org> - 1.0.2-1
- Update to 1.0.2 (no change)

* Tue Jan 19 2016 Remi Collet <remi@fedoraproject.org> - 1.0.1-1
- Update to 1.0.1

* Mon Aug 03 2015 Remi Collet <remi@fedoraproject.org> - 1.0.0-1
- Update to 1.0.0

* Tue Feb 10 2015 Remi Collet <remi@fedoraproject.org> - 0.3.10-1
- Update to 0.3.10

* Thu Jan 15 2015 Remi Collet <remi@fedoraproject.org> - 0.3.9-1
- Initial packaging, version 0.3.9
