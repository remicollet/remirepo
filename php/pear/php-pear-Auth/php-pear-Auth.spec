%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%define pear_name Auth

Name:           php-pear-Auth
Version:        1.6.2
Release:        1%{?dist}
Summary:        Authentication provider for PHP
Group:          Development/Libraries
License:        PHP
URL:            http://pear.php.net/package/Auth
Source0:        http://pear.php.net/get/%{pear_name}-%{version}.tgz
Source1:        PHP-LICENSE-3.01
#Patch0:         %{name}-1.6.1-md5sum.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php-pear >= 1:1.4.9-1.2

Provides:        php-pear(%{pear_name}) = %{version}
Requires:        php-pear(Net_POP3) >= 1.3.0
Requires:        php-imap
Requires:        php-ldap
Requires:        php-soap
Requires:        php-pear(DB) >= 1.6.0
Requires:        php-pear(File_Passwd) >= 1.1.0
Requires:        php-pear(HTTP_Client) >= 1.1.0
Requires:        php-pear(Log) >= 1.9.10
Requires:        php-pear(Net_POP3) >= 1.3.0
Requires:        php-pear(MDB2) >= 2.0
Requires:        php-pear(SOAP) >= 0.9.0

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
[ -f package2.xml ] || mv package.xml package2.xml
mv package2.xml %{pear_name}-%{version}/%{pear_name}.xml
cd %{pear_name}-%{version}

# Fix end of line encodings
# %patch0 -p0 -b .md5sum
%{__sed} -i 's/\r//' README.Auth

%build
cd %{pear_name}-%{version}
# Empty build section, most likely nothing required.

%install
cd %{pear_name}-%{version}
rm -rf $RPM_BUILD_ROOT docdir
%{__pear} install --offline --nodeps --installroot $RPM_BUILD_ROOT %{pear_name}.xml

# Move documentation
mkdir -p docdir
mv $RPM_BUILD_ROOT%{pear_docdir}/* docdir
# License file added
install -pm 644 -c  %{SOURCE1} docdir/LICENSE

# Clean up unnecessary files
rm -rf $RPM_BUILD_ROOT%{pear_phpdir}/.??*

# Install XML package description
mkdir -p $RPM_BUILD_ROOT%{pear_xmldir}
install -pm 644 %{pear_name}.xml $RPM_BUILD_ROOT%{pear_xmldir}

%clean
rm -rf $RPM_BUILD_ROOT


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
%doc %{pear_name}-%{version}/docdir/%{pear_name}/*
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
