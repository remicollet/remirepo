%{!?_httpd_contentdir: %{expand: %%global _httpd_contentdir /var/www}}

Name:           php-adodb
Summary:        Database abstraction layer for PHP
Version:        5.20.6
Release:        2%{?dist}

License:        BSD or LGPLv2+
URL:            http://adodb.org
Group:          Development/Libraries
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
# for macros
BuildRequires:  httpd-devel

Source0:        http://downloads.sourceforge.net/adodb/adodb-%{version}.tar.gz

Requires:       php-common

%description
ADOdb is an object oriented library written in PHP that abstracts database 
operations for portability. It is modelled on Microsoft's ADO, but has many
improvements that make it unique (eg. pivot tables, Active Record support, 
generating HTML for paging recordsets with next and previous links, cached 
recordsets, HTML menu generation, etc).
ADOdb hides the differences between the different databases so you can easily
switch DBs without changing code.

# !! TODO !! MAKE A SUBPACKAGE FOR THE PEAR::AUTH DRIVER

%prep
%setup -q -n adodb5


%build
# fix dir perms
find . -type d | xargs chmod 755
# fix file perms
find . -type f | xargs chmod 644


%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_httpd_contentdir}/icons
install -d $RPM_BUILD_ROOT%{_datadir}/php/adodb
cp -pr * $RPM_BUILD_ROOT%{_datadir}/php/adodb/

install -m644 cute_icons_for_site/* $RPM_BUILD_ROOT%{_httpd_contentdir}/icons

# cleanup
rm -rf $RPM_BUILD_ROOT%{_datadir}/php/adodb/cute_icons_for_site
rm -rf $RPM_BUILD_ROOT%{_datadir}/php/adodb/docs
rm -rf $RPM_BUILD_ROOT%{_datadir}/php/adodb/tests
rm -f $RPM_BUILD_ROOT%{_datadir}/adodb/*.txt

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{!?_licensedir:%global license %%doc}
%license LICENSE.md
%doc README.md docs
%{_datadir}/php/adodb
%{_httpd_contentdir}/icons/*


%changelog
* Tue Sep 20 2016 Gianluca Sforna <giallu@gmail.com> - 5.20.6-2
- update to latest release
- fix for CVE-2016-7405 (#1376365)
- spec file clean up

* Tue Sep  6 2016 Gianluca Sforna <giallu@gmail.com> - 5.15-10
- fix for CVE-2016-4855 (#1373374)

* Sat Feb 11 2012 Remi Collet <RPMS@FamilleCollet.com> - 5.15-1
- upstream 5.15, rebuild for remi repository

* Wed Feb  8 2012 Gianluca Sforna <giallu@gmail.com> - 5.15-1
- New upstream release

* Sat Aug 06 2011 Remi Collet <RPMS@FamilleCollet.com> - 5.12-1
- rebuild for remi repository

* Fri Aug 05 2011 Gianluca Sforna <giallu@gmail.com> - 5.12-1
- New upstream release

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu May 27 2010 Remi Collet <RPMS@FamilleCollet.com> - 5.11-1
- rebuild for remi repository

* Sun May 23 2010 Gianluca Sforna <giallu gmail com> - 5.11-1
- New upstream release

* Thu Nov 18 2009 Remi Collet <RPMS@FamilleCollet.com> - 5.10-1
- rebuild for remi repository

* Thu Nov 12 2009 Gianluca Sforna <giallu gmail com> - 5.10-1
- New upstream release

* Tue Aug 25 2009 Gianluca Sforna <giallu gmail com> - 5.09a-1
- Update to latest release
- Fix download URL
- Update summary and description
- Requires php-common

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.95-3.a
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.95-2.a
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Aug 26 2007 Aurelien Bompard <abompard@fedoraproject.org> 4.95-1.a
- version 4.95a
- fix license tag

* Fri Apr 06 2007 Aurelien Bompard <abompard@fedoraproject.org> 4.94-1
- version 4.94
- move install path to %%_datadir/php/adodb (#235461)

* Wed Aug 30 2006 Aurelien Bompard <abompard@fedoraproject.org> 4.92-1
- version 4.92

* Fri Apr 14 2006 Aurelien Bompard <gauret[AT]free.fr> 4.80-1
- version 4.80

* Wed Feb 22 2006 Aurelien Bompard <gauret[AT]free.fr> 4.72-1
- version 4.72

* Fri Dec 23 2005 Aurelien Bompard <gauret[AT]free.fr> 4.68-1
- version 4.68

* Fri Nov 18 2005 Aurelien Bompard <gauret[AT]free.fr> 4.67-1
- version 4.67

* Sun May 08 2005 Aurelien Bompard <gauret[AT]free.fr> 4.62-1%{?dist}
- version 4.62
- use disttag

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Wed Aug 11 2004 Aurelien Bompard <gauret[AT]free.fr> 0:4.52-0.fdr.1
- update to 4.52

* Sat Jul 31 2004 Aurelien Bompard <gauret[AT]free.fr> 0:4.51-0.fdr.1
- update to 4.51

* Sat Jul 03 2004 Aurelien Bompard <gauret[AT]free.fr> 0:4.23-0.fdr.2
- move to _datadir instead of _libdir
- use the _var macro

* Wed Jun 30 2004 Aurelien Bompard <gauret[AT]free.fr> 0:4.23-0.fdr.1
- Initial Fedora package (from Mandrake)

