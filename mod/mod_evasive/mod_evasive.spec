Name:           mod_evasive
Version:        1.10.1
Release:        15%{?dist}
Summary:        Denial of Service evasion module for Apache

Group:          System Environment/Daemons
License:        GPLv2+
URL:            http://www.zdziarski.com/projects/mod_evasive/
Source0:        http://www.zdziarski.com/projects/mod_evasive/mod_evasive_%{version}.tar.gz
Source1:        mod_evasive.conf
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  httpd-devel
Requires:       httpd
Requires:       httpd-mmn = %([ -a %{_includedir}/httpd/.mmn ] && cat %{_includedir}/httpd/.mmn || echo missing)

%description
mod_evasive is an evasive maneuvers module for Apache to provide evasive 
action in the event of an HTTP DoS or DDoS attack or brute force attack. It 
is also designed to be a detection and network management tool, and can be 
easily configured to talk to firewalls, routers, etc. mod_evasive presently 
reports abuses via email and syslog facilities. 


%prep
%setup -q -n %{name}


%build
# create apache httpd-2.4 version and compile it
sed 's/connection->remote_ip/connection->client_ip/' \
  < mod_evasive20.c > mod_evasive24.c
apxs -Wc,"%{optflags}" -c mod_evasive24.c


%install
rm -rf $RPM_BUILD_ROOT
mkdir -pm 755 \
    $RPM_BUILD_ROOT%{_libdir}/httpd/modules \
    $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d
install -pm 755 .libs/mod_evasive24.so $RPM_BUILD_ROOT%{_libdir}/httpd/modules/
install -pm 644 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d/


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc README LICENSE CHANGELOG test.pl
%config(noreplace) %{_sysconfdir}/httpd/conf.d/*
%{_libdir}/httpd/modules/*


%changelog
* Wed Feb 13 2013 Remi Collet <RPMS@FamilleCollet.com> - 1.10.1-15
- rebuild for remi repo and httpd 2.4

* Mon Nov 26 2012 Ján ONDREJ (SAL) <ondrejj(at)salstar.sk> - 1.10.1-15
- fix configuration file for new version (#879269)

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10.1-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Mar 31 2012 Remi Collet <RPMS@FamilleCollet.com> - 1.1.1-4
- rebuild for remi repo and httpd 2.4

* Sat Mar 31 2012 Ján ONDREJ (SAL) <ondrejj(at)salstar.sk> - 1.10.1-13
- adapt to httpd-2.4: changed remote_ip to client_ip

* Thu Mar 29 2012 Ján ONDREJ (SAL) <ondrejj(at)salstar.sk> - 1.10.1-12
- apxs moved to bindir, do not use sbindir macro

* Tue Mar 27 2012 Ján ONDREJ (SAL) <ondrejj(at)salstar.sk> - 1.10.1-11
- Rebuild for new httpd-mmn

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Aug 11 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.10.1-6
- fix license tag

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.10.1-5.1
- Autorebuild for GCC 4.3

* Wed Sep 05 2007 Konstantin Ryabitsev <icon@fedoraproject.org> - 1.10.1-4.1
- Rebuild for APR changes

* Wed Aug 29 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 1.10.1-4
- Rebuild for selinux ppc32 issue.

* Tue Apr 10 2007 Konstantin Ryabitsev <icon@fedoraproject.org> - 1.10.1-3
- Modify the URL and finally import into extras.

* Mon Jan 29 2007 Konstantin Ryabitsev <icon@fedoraproject.org> - 1.10.1-2
- The source moved to another domain since last year.
- use _sbindir macro for apxs.

* Tue Dec 06 2005 Konstantin Ryabitsev <icon@fedoraproject.org> - 1.10.1-1
- Cleaning up description
- Cleaning up install
- Slight modification to default config (add DOSWhitelist entries)
- Disttagging
- Adding test.pl to docs

* Wed Nov 16 2005 Kosntantin Ryabitsev <icon@fedoraproject.org> - 1.10.1-0.1
- Initial packaging.
