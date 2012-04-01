%{!?_httpd_apxs: %{expand: %%global _httpd_apxs %%{_sbindir}/apxs}}
%{!?_httpd_mmn: %{expand: %%global _httpd_mmn %%(cat %{_includedir}/httpd/.mmn || echo missing-httpd-devel)}}

Name:           mod_bw
Version:        0.92
Release:        1%{?dist}
Summary:        Bandwidth Limiter For Apache

Group:          System Environment/Daemons
License:        ASL 2.0
URL:            http://www.ivn.cl/apache
Source0:        http://www.ivn.cl/apache/files/source/mod_bw-%{version}.tgz
Source1:        mod_bw.conf

Patch0:         mod_bw-httpd24.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  httpd-devel
Requires:       httpd-mmn = %{_httpd_mmn}

%description
mod_bw is a bandwidth administration module for Apache httpd 2.x

* Restricts the number of simultaneous connections per vhost/dir
* Limits the bandwidth for files on vhost/dir

%prep
%setup -q -c

%patch0 -p1 -b .httpd24

mv mod_bw.txt mod_bw.txt.iso8859
iconv -f ISO-8859-1 -t UTF-8 mod_bw.txt.iso8859 > mod_bw.txt 


%build
%{_httpd_apxs} -Wc,"%{optflags}" -c mod_bw.c


%install
rm -rf $RPM_BUILD_ROOT
install -Dpm 755 .libs/mod_bw.so \
                 $RPM_BUILD_ROOT%{_libdir}/httpd/modules/mod_bw.so
install -Dpm 644 %{SOURCE1} \
                 $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d/mod_bw.conf


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc ChangeLog LICENSE TODO mod_bw.txt
%config(noreplace) %{_sysconfdir}/httpd/conf.d/mod_bw.conf
%{_libdir}/httpd/modules/mod_bw.so


%changelog
* Sun Apr 01 2012 Remi Collet <RPMS@FamilleCollet.com> - 0.92-1
- update to 0.92 for remi repo and httpd 2.4

* Wed Mar 14 2012 Jakub Hrozek <jhrozek@redhat.com> - 0.8-7
- Do not require httpd itself

* Wed Mar 14 2012 Jakub Hrozek <jhrozek@redhat.com> - 0.8-6
- Require httpd-mmn (#803067)

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 18 2008 Jakub Hrozek <jhrozek@redhat.com> - 0.8-1
- initial packaging
