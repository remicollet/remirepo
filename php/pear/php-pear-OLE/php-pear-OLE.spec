%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name OLE
%global prever    RC2

Name:           php-pear-OLE
Version:        1.0.0
Release:        %{?prever:0.}8%{?prever:.%{prever}}%{?dist}
Summary:        Package for reading and writing OLE containers

Group:          Development/Libraries
License:        PHP
URL:            http://pear.php.net/package/OLE
Source0:        http://pear.php.net/get/%{pear_name}-1.0.0%{?prever}.tgz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php-pear >= 1:1.4.9-1.2

Requires:       php-date
Requires:       php-pear(PEAR)
Requires(post): %{__pear}
Requires(postun): %{__pear}

Provides:       php-pear(%{pear_name}) = %{version}


%description
This package allows reading and writing of OLE (Object Linking and
Embedding) compound documents. This format is used as container for Excel
(.xls), Word (.doc) and other Microsoft file formats.

%prep
%setup -q -c
[ -f package2.xml ] || mv package.xml package2.xml
mv package2.xml %{pear_name}-%{version}%{?prever}/%{name}.xml
cd %{pear_name}-%{version}%{?prever}


%build
cd %{pear_name}-%{version}%{?prever}
# Empty build section, most likely nothing required.


%install
rm -rf $RPM_BUILD_ROOT
cd %{pear_name}-%{version}%{?prever}
%{__pear} install --nodeps --packagingroot $RPM_BUILD_ROOT %{name}.xml

# Clean up unnecessary files
rm -rf $RPM_BUILD_ROOT%{pear_metadir}/.??*

# Install XML package description
mkdir -p $RPM_BUILD_ROOT%{pear_xmldir}
install -pm 644 %{name}.xml $RPM_BUILD_ROOT%{pear_xmldir}


%clean
rm -rf $RPM_BUILD_ROOT


%post
%{__pear} install --nodeps --soft --force --register-only \
    %{pear_xmldir}/%{name}.xml >/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    %{__pear} uninstall --nodeps --ignore-errors --register-only \
        pear.php.net/%{pear_name} >/dev/null || :
fi


%files
%defattr(-,root,root,-)
%{pear_xmldir}/%{name}.xml
%{pear_phpdir}/OLE
%{pear_phpdir}/OLE.php


%changelog
* Mon Aug 06 2012 Remi Collet <RPMS@FamilleCollet.com> - 1.0.0-0.8.RC2
- update to 1.0.0RC2 for remi repo

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-0.7.rc1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-0.6.rc1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-0.5.rc1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 08 2009 David Nalley <david@gnsa.us> 1.0.0-0.4.rc1
- really fixed php-pear require
* Sun Dec 06 2009 David Nalley <david@gnsa.us> 1.0.0-0.3.rc1
- added require for php(pear)
* Wed Dec 02 2009 David Nalley <david@gnsa.us> 1.0.0-0.2.rc1
- removed require for php
* Sat Nov 28 2009 David Nalley <david@gnsa.us> 1.0.0-0.1.rc1
- Initial packaging efforts
