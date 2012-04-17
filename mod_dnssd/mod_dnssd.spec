%{!?_httpd_apxs:       %{expand: %%global _httpd_apxs       %%{_sbindir}/apxs}}
%{!?_httpd_mmn:        %{expand: %%global _httpd_mmn        %%(cat %{_includedir}/httpd/.mmn || echo missing-httpd-devel)}}
%{!?_httpd_confdir:    %{expand: %%global _httpd_confdir    %%{_sysconfdir}/httpd/conf.d}}
# /etc/httpd/conf.d with httpd < 2.4 and defined as /etc/httpd/conf.modules.d with httpd >= 2.4
%{!?_httpd_modconfdir: %{expand: %%global _httpd_modconfdir %%{_sysconfdir}/httpd/conf.d}}

Name:           mod_dnssd
Version:        0.6
Release:        6%{?dist}
Summary:        An Apache HTTPD module which adds Zeroconf support

Group:          System Environment/Daemons
License:        ASL 2.0
URL:            http://0pointer.de/lennart/projects/mod_dnssd/
Source0:        http://0pointer.de/lennart/projects/mod_dnssd/%{name}-%{version}.tar.gz
Source1:        mod_dnssd.conf-httpd
Patch0:         mod_dnssd-0.6-httpd24.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:       httpd-mmn = %{_httpd_mmn}
BuildRequires:  httpd-devel avahi-devel e2fsprogs-devel

%description
mod_dnssd is an Apache HTTPD module which adds Zeroconf support via DNS-SD
using Avahi.

%prep
%setup -q
%patch0 -p1 -b .httpd24

%build
export APXS=%{_httpd_apxs}
%configure --disable-lynx
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
install -Dp src/.libs/mod_dnssd.so $RPM_BUILD_ROOT%{_libdir}/httpd/modules/mod_dnssd.so
%if "%{_httpd_confdir}" == "%{_httpd_modconfdir}"
install -Dp -m 0644 %{SOURCE1} $RPM_BUILD_ROOT%{_httpd_confdir}/mod_dnssd.conf
%else
sed -n /^LoadModule/p %{SOURCE1} > 10-mod_dnssd.conf
sed /^LoadModule/d %{SOURCE1} > mod_dnssd.conf
touch -r %{SOURCE1} 10-mod_dnssd.conf mod_dnssd.conf
install -Dp -m 0644 mod_dnssd.conf $RPM_BUILD_ROOT%{_httpd_confdir}/mod_dnssd.conf
install -Dp -m 0644 10-mod_dnssd.conf $RPM_BUILD_ROOT%{_httpd_modconfdir}/10-mod_dnssd.conf
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc LICENSE doc/README doc/README.html
%config(noreplace) %{_sysconfdir}/httpd/conf.*/*.conf
%{_libdir}/httpd/modules/mod_dnssd.so

%changelog
* Tue Apr 17 2012 Joe Orton <jorton@redhat.com> - 0.6-6
- update for httpd 2.4, fix deps etc (#803069)

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jan 28 2009 Lennart Poettering <lpoetter@redhat.com> - 0.6-1
- New upstream

* Mon Aug 11 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.5-7
- fix license tag

* Sun Feb 10 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> 0.5-6
- Rebuild for GCC 4.3

* Mon Sep  3 2007 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> 0.5-5
- Rebuild for new 32-bit APR ABI

* Tue Aug 21 2007 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> 0.5-4
- Fix License tag
- Rebuild for F8t2

* Tue Jul 24 2007 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> 0.5-3
- Add upstream patch to fix UID issue

* Mon Jun 25 2007 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> 0.5-2
- Add LoadModule to the config file

* Mon Jun 18 2007 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> 0.5-1
- Initial RPM release
