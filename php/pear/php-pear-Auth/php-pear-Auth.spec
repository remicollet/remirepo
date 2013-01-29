%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%define pear_name Auth

Name:           php-pear-Auth
Version:        1.6.4
Release:        2%{?dist}
Summary:        Authentication provider for PHP
Group:          Development/Libraries
License:        PHP
URL:            http://pear.php.net/package/Auth
Source0:        http://pear.php.net/get/%{pear_name}-%{version}.tgz
# https://pear.php.net/bugs/19805
Source1:        PHP-LICENSE-3.01

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php-pear

Requires:        php-pear(Net_POP3) >= 1.3.0
Requires:        php-imap
Requires:        php-ldap
Requires:        php-pcre
Requires:        php-session
Requires:        php-soap
Requires:        php-xml
Requires:        php-pear(DB) >= 1.6.0
Requires:        php-pear(File_Passwd) >= 1.1.0
Requires:        php-pear(HTTP_Client) >= 1.1.0
Requires:        php-pear(Log) >= 1.9.10
Requires:        php-pear(Net_POP3) >= 1.3.0
Requires:        php-pear(MDB2) >= 2.0
Requires:        php-pear(SOAP) >= 0.9.0

Provides:        php-pear(%{pear_name}) = %{version}

Requires(post): %{__pear}
Requires(postun): %{__pear}

%description
The PEAR::Auth package provides methods for creating an authentication
system using PHP.

%package        samba
Summary:        Samba support for php-pear-Auth
Group:          Development/Libraries
Requires:       php-pear(File_SMBPasswd) >= 1.0.0
Requires:       %{name} = %{version}-%{release}

%description samba
This package adds a SMBPasswd container for the PHP Auth system.

%package        radius
Summary:        RADIUS support for php-pear-Auth
Group:          Development/Libraries
Requires:       php-pear(Auth_RADIUS)
Requires:       %{name} = %{version}-%{release}

%description radius
This package adds a RADIUS container for the PHP Auth system.


%prep
%setup -q -c

cp %{SOURCE1} LICENSE

cd %{pear_name}-%{version}

# https://pear.php.net/bugs/19806
sed -e '/md5.js/s/role="data"/role="php"/' \
    ../package.xml >%{pear_name}.xml


%build
cd %{pear_name}-%{version}
# Empty build section, most likely nothing required.


%install
rm -rf %{buildroot}
cd %{pear_name}-%{version}
%{__pear} install --force --nodeps --installroot %{buildroot} %{pear_name}.xml

# Clean up unnecessary files
rm -rf %{buildroot}%{pear_metadir}/.??*

# Install XML package description
mkdir -p %{buildroot}%{pear_xmldir}
install -pm 644 %{pear_name}.xml %{buildroot}%{pear_xmldir}


%clean
rm -rf %{buildroot}


%post
%{__pear} install --nodeps --soft --force --register-only \
    %{pear_xmldir}/%{pear_name}.xml >/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    %{__pear} uninstall --nodeps --ignore-errors --register-only \
        %{pear_name} >/dev/null || :
fi


%files
%defattr(-,root,root,-)
%doc LICENSE
%doc %{pear_docdir}/%{pear_name}
%{pear_xmldir}/%{pear_name}.xml
%{pear_phpdir}/%{pear_name}*
%{pear_testdir}/%{pear_name}
%exclude %{pear_phpdir}/%{pear_name}/Container/SMBPasswd.php
%exclude %{pear_phpdir}/%{pear_name}/Container/RADIUS.php

%files samba
%defattr(-,root,root,-)
%{pear_phpdir}/%{pear_name}/Container/SMBPasswd.php

%files radius
%defattr(-,root,root,-)
%{pear_phpdir}/%{pear_name}/Container/RADIUS.php


%changelog
* Tue Jan 29 2013 Remi Collet <rpms@fedoraproject.org> - 1.6.4-2
- rebuild

* Tue Jan 29 2013 Remi Collet <remi@fedoraproject.org> - 1.6.4-1
- Updated to 1.6.4 (stable), API 1.5.0 (stable)
- add link to upstream bugs
  https://pear.php.net/bugs/19805 : missing LICENSE
  https://pear.php.net/bugs/19806 : md5.js
- doc in /usr/share/doc/pear

* Tue Aug 21 2012 Remi Collet <remi@fedoraproject.org> - 1.6.4-1
- update to 1.6.4 for remi repo
- move doc to /usr/share/doc/pear

* Tue Aug 14 2012 Remi Collet <remi@fedoraproject.org> - 1.6.2-5
- rebuilt for new pear_testdir

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri May 07 2010 Remi Collet <RPMS@FamilleCollet.com> - 1.6.2-1
- rebuild for remi repository

* Mon May 03 2010 Rakesh Pandit <rakesh@fedoraproject.org> 1.6.2-1
- Updated to 1.6.2

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Jul 18 2009 Remi Collet <RPMS@FamilleCollet.com> - 1.6.1-9
- rebuild for remi repository

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Oct 24 2008 Rakesh Pandit <rakesh@fedoraproject.org> 1.6.1-8
- added license file

* Fri Aug 29 2008 Rakesh Pandit <rakesh@fedoraproject.org> 1.6.1-7
- fixed %%doc (Christopher Stone)

* Fri Aug 29 2008 Rakesh Pandit <rakesh@fedoraproject.org> 1.6.1-6
- fixed some consmetic stuff - space, spelling
- used --installroot in place of --packagingroot - fix build WARNING

* Sat Jun 28 2008 David Hollis <dhollis@davehollis.com> 1.6.1-5
- -radius requires php-pear(Auth_RADIUS)
- -samba requires php-pear(File_SMBPasswd)

* Sat Jun 28 2008 David Hollis <dhollis@davehollis.com> 1.6.1-4
- Fix subpackage requires
- Add defattr for subpackages

* Wed Jun 18 2008 David Hollis <dhollis@davehollis.com> 1.6.1-3
- Nuke addons package, make a -radius subpackage

* Tue Jun 17 2008 David Hollis <dhollis@davehollis.com> 1.6.1-2
- Separate out -samba and -addons packages

* Sat May 31 2008 David Hollis <dhollis@davehollis.com> 1.6.1-1
- Update to 1.6.1
- Add Requires: for packages that Auth can make use of that already
  exist within Fedora

* Mon Mar 24 2008 David Hollis <dhollis@davehollis.com> 1.5.4-1
- RPM Created
