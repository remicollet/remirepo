%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%define pear_name Net_DNS

Name:           php-pear-Net-DNS
Version:        1.0.7
Release:        1%{?dist}
Summary:        Resolver library used to communicate with a DNS server

Group:          Development/Libraries
License:        PHP
URL:            http://pear.php.net/package/Net_DNS
Source:         http://download.pear.php.net/package/%{pear_name}-%{version}.tgz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  php-pear >= 1:1.4.9-1.2
BuildArch:      noarch
Requires:       php-pear(PEAR)
Requires(post): %{__pear}
Requires(postun): %{__pear}
Provides:       php-pear(%{pear_name}) = %{version}

%description
A resolver library used to communicate with a name server to perform DNS 
queries, zone transfers, dynamic DNS updates, etc. Creates an object 
hierarchy from a DNS server response, which allows you to view all of 
the information given by the DNS server. It bypasses the system 
resolver library and communicates directly with the server.


%prep
%setup -qc
# Package.xml is V2
mv package.xml %{pear_name}-%{version}/%{name}.xml
cd %{pear_name}-%{version}


%build
cd %{pear_name}-%{version}
# Empty build section, most likely nothing required.


%install
cd %{pear_name}-%{version}
rm -rf $RPM_BUILD_ROOT docdir
%{__pear} install --nodeps --packagingroot $RPM_BUILD_ROOT %{name}.xml

# Clean up unnecessary files
rm -rf $RPM_BUILD_ROOT%{pear_phpdir}/.??*

# Install XML package description
install -d $RPM_BUILD_ROOT%{pear_xmldir}
install -pm 644 %{name}.xml $RPM_BUILD_ROOT%{pear_xmldir}


%clean
rm -rf $RPM_BUILD_ROOT


%post
%{__pear} install --nodeps --soft --force --register-only \
    %{pear_xmldir}/%{name}.xml >/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    %{__pear} uninstall --nodeps --ignore-errors --register-only \
        %{pear_name} >/dev/null || :
fi


%files
%defattr(-,root,root,-)
%{pear_xmldir}/%{name}.xml
%dir %{pear_phpdir}/Net
%{pear_phpdir}/Net/DNS
%{pear_phpdir}/Net/DNS.php
%{pear_testdir}/%{pear_name}

%changelog
* Sun Aug 21 2011 Remi Collet <RPMS@FamilleCollet.com> - 1.0.7-1
- update to 1.0.7 for remi repo

* Sun Aug 15 2010 Remi Collet <RPMS@FamilleCollet.com> - 1.0.5-1
- rebuild for remi repository

* Thu Aug 14 2010 Steven Moix <steven.moix@axianet.ch> 1.0.5-1
- New upstream release
- Corrects https://bugzilla.redhat.com/show_bug.cgi?id=595462

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Jul 18 2009 Remi Collet <RPMS@FamilleCollet.com> - 1.0.1-1
- rebuild for remi repository

* Mon Jul 13 2009 Remi Collet <Fedora@FamilleCollet.com> - 1.0.1-1
- update to 1.0.1
- remove mhash dependency (now optional, and not provided by php 5.3.0)
- rename Net_DNS.xml to php-pear-Net-DNS.xml

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Jul 3 2008 Steven Moix <steven.moix@axianet.ch> 1.0.0-2
- Corrected the spec file thanks to Remi Collet

* Sat May 24 2008 Steven Moix <steven.moix@axianet.ch> 1.0.0-1
- Initial Release
