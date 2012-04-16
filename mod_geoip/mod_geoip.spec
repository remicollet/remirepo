%{!?_httpd_apxs: %{expand: %%global _httpd_apxs %%{_sbindir}/apxs}}
%{!?_httpd_mmn: %{expand: %%global _httpd_mmn %%(cat %{_includedir}/httpd/.mmn || echo missing-httpd-devel)}}
# /etc/httpd/conf.d with httpd < 2.4 and defined as /etc/httpd/conf.modules.d with httpd >= 2.4
%{!?_httpd_modconfdir: %{expand: %%global _httpd_modconfdir %%{_sysconfdir}/httpd/conf.d}}
%{!?_httpd_confdir:    %{expand: %%global _httpd_confdir    %%{_sysconfdir}/httpd/conf.d}}
%{!?_httpd_moddir:    %{expand: %%global _httpd_moddir    %%{_libdir}/httpd/modules}}

Summary: GeoIP module for the Apache HTTP Server
Name: mod_geoip
Version: 1.2.5
Release: 8%{?dist}
License: ASL 1.1
Group: System Environment/Daemons
URL: http://www.maxmind.com/app/mod_geoip
Source: http://www.maxmind.com/download/geoip/api/mod_geoip2/mod_geoip2_%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: GeoIP httpd httpd-mmn = %([ -a %{_includedir}/httpd/.mmn ] && cat %{_includedir}/httpd/.mmn || echo missing)
BuildRequires: httpd-devel GeoIP-devel
# Not upstream
Patch0: mod_geoip-httpd24.patch

%description
mod_geoip is an Apache module for finding the country that a web request
originated from.  It uses the GeoIP library and database to perform
the lookup.  It is free software, licensed under the Apache license.

%prep

%setup -q -n mod_geoip2_%{version}
%patch0 -p0 -b .geoip

%build
%{_httpd_apxs} -Wc,"%{optflags}" -Wl,"-lGeoIP" -c mod_geoip.c

%install
mkdir -p %{buildroot}%{_httpd_confdir} %{buildroot}%{_httpd_modconfdir} \
      %{buildroot}%{_httpd_moddir}
install -Dp .libs/mod_geoip.so %{buildroot}%{_httpd_moddir}

cat << EOF > 10-mod_geoip.conf
LoadModule geoip_module modules/mod_geoip.so

EOF
cat << EOF > mod_geoip.conf
<IfModule mod_geoip.c>
  GeoIPEnable On
  GeoIPDBFile /usr/share/GeoIP/GeoIP.dat
</IfModule>

EOF

%if "%{_httpd_modconfdir}" != "%{_httpd_confdir}"
# 2.4-style
install -m 0644 10-mod_geoip.conf %{buildroot}%{_httpd_modconfdir}
install -m 0644 mod_geoip.conf %{buildroot}%{_httpd_confdir}
%else
# old-style
cat 10-mod_geoip.conf mod_geoip.conf > unified.conf
install -m 0644 unified.conf %{buildroot}%{_httpd_confdir}/mod_geoip.conf
%endif

%clean
rm -rf %{buildroot}

%files
%defattr (-,root,root)
%doc INSTALL README* Changes
%{_libdir}/httpd/modules/mod_geoip.so
%config(noreplace) %{_sysconfdir}/httpd/conf.d/mod_geoip.conf
%if "%{_httpd_modconfdir}" != "%{_httpd_confdir}"
%config(noreplace) %{_sysconfdir}/httpd/conf.modules.d/10-mod_geoip.conf
%endif

%changelog
* Mon Apr 16 2012 Remi Collet <RPMS@FamilleCollet.com> - 1.2.5-8
- rebuild for remi repo and httpd 2.4

* Mon Apr 16 2012 Joe Orton <jorton@redhat.com> - 1.2.5-8
- fix config perms

* Wed Apr 04 2012 Jan Kaluza <jkaluza@redhat.com> - 1.2.5-7
- Fix compilation error with httpd-2.4 (#809698)

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Aug 29 2008 Michael Fleming <mfleming+rpm@enlartenment.com> - 1.2.5-2
- Update setup macro

* Fri Aug 29 2008 Michael Fleming <mfleming+rpm@enlartenment.com> - 1.2.5-1
- Update to 1.2.5

* Mon Aug 11 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.2.4-3
- fix license tag

* Fri Jun 20 2008 Michael Fleming <mfleming+rpm@enlartenment.com> 1.2.4-2
- New upstream update
- Minor spec tweaks

* Sun Apr 13 2008 Michael Fleming <mfleming+rpm@enlartenment.com> 1.2.2-1
- New upstream update

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.2.0-2
- Autorebuild for GCC 4.3

* Wed Sep 5 2007 Michael Fleming <mfleming+rpm@enlartenment.com> 1.2.0-1
- New upstream release
- Employ some macro sanity..

* Sun Sep 3 2006 Michael Fleming <mfleming+rpm@enlartenment.com> 1.1.8-2
- Bump and rebuild

* Mon May 1 2006 Michael Fleming <mfleming+rpm@enlartenment.com> 1.1.8-1
- New upstream release

* Sat Feb 18 2006 Michael Fleming <mfleming+rpm@enlartenment.com> 1.1.7-2
- Small cleanups, including a saner Requires: for httpd
- Don't strip the binary

* Sun Feb 5 2006 Michael Fleming <mfleming+rpm@enlartenment.com> 1.1.7-1
- Initial review package for Extras

