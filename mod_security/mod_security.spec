%{!?_httpd_apxs: %{expand: %%global _httpd_apxs %%{_sbindir}/apxs}}
%{!?_httpd_mmn: %{expand: %%global _httpd_mmn %%(cat %{_includedir}/httpd/.mmn || echo missing-httpd-devel)}}
# /etc/httpd/conf.d with httpd < 2.4 and defined as /etc/httpd/conf.modules.d with httpd >= 2.4
%{!?_httpd_modconfdir: %{expand: %%global _httpd_modconfdir %%{_sysconfdir}/httpd/conf.d}}
%{!?_httpd_confdir:    %{expand: %%global _httpd_confdir    %%{_sysconfdir}/httpd/conf.d}}
%{!?_httpd_moddir:    %{expand: %%global _httpd_moddir    %%{_libdir}/httpd/modules}}

Summary: Security module for the Apache HTTP Server
Name: mod_security 
Version: 2.6.5
Release: 3%{?dist}
License: ASL 2.0
URL: http://www.modsecurity.org/
Group: System Environment/Daemons
Source: http://www.modsecurity.org/download/modsecurity-apache_%{version}.tar.gz
Source1: mod_security.conf
Requires: httpd httpd-mmn = %{_httpd_mmn}
BuildRequires: httpd-devel libxml2-devel pcre-devel curl-devel lua-devel

%description
ModSecurity is an open source intrusion detection and prevention engine
for web applications. It operates embedded into the web server, acting
as a powerful umbrella - shielding web applications from attacks.

%package -n     mlogc
Summary:        ModSecurity Audit Log Collector
Group:          System Environment/Daemons
Requires:       mod_security

%description -n mlogc
This package contains the ModSecurity Audit Log Collector.

%prep
%setup -q -n modsecurity-apache_%{version}

%build
%configure --enable-pcre-match-limit=1000000 \
           --enable-pcre-match-limit-recursion=1000000 \
           --with-apxs=%{_httpd_apxs}
# remove rpath
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make %{_smp_mflags}

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_sbindir}
install -d %{buildroot}%{_bindir}
install -d %{buildroot}%{_httpd_moddir}
install -d %{buildroot}%{_sysconfdir}/httpd/modsecurity.d/
install -d %{buildroot}%{_sysconfdir}/httpd/modsecurity.d/activated_rules

install -m0755 apache2/.libs/mod_security2.so %{buildroot}%{_httpd_moddir}/mod_security2.so

%if "%{_httpd_modconfdir}" != "%{_httpd_confdir}"
# 2.4-style
sed -n /^LoadModule/p %{SOURCE1} > 10-mod_security.conf
sed    /LoadModule/d  %{SOURCE1} > mod_security.conf
touch -r %{SOURCE1} *.conf
install -Dp -m0644 mod_security.conf %{buildroot}%{_httpd_confdir}/mod_security.conf
install -Dp -m0644 10-mod_security.conf %{buildroot}%{_httpd_modconfdir}/10-mod_security.conf
%else
# 2.2-style
install -Dp -m0644 %{SOURCE1} %{buildroot}%{_httpd_confdir}/mod_security.conf
%endif

# mlogc
install -d %{buildroot}%{_localstatedir}/log/mlogc
install -d %{buildroot}%{_localstatedir}/log/mlogc/data
install -m0755 mlogc/mlogc %{buildroot}%{_bindir}/mlogc
install -m0755 mlogc/mlogc-batch-load.pl %{buildroot}%{_bindir}/mlogc-batch-load
install -m0644 mlogc/mlogc-default.conf %{buildroot}%{_sysconfdir}/mlogc.conf

%clean
rm -rf %{buildroot}

%files
%defattr (-,root,root)
%doc CHANGES LICENSE README.TXT NOTICE
%{_httpd_moddir}/mod_security2.so
%config(noreplace) %{_httpd_confdir}/*.conf
%if "%{_httpd_modconfdir}" != "%{_httpd_confdir}"
%config(noreplace) %{_httpd_modconfdir}/*.conf
%endif
%dir %{_sysconfdir}/httpd/modsecurity.d
%dir %{_sysconfdir}/httpd/modsecurity.d/activated_rules

%files -n mlogc
%defattr (-,root,root)
%doc mlogc/INSTALL
%attr(0640,root,apache) %config(noreplace) %{_sysconfdir}/mlogc.conf
%attr(0755,root,root) %dir %{_localstatedir}/log/mlogc
%attr(0770,root,apache) %dir %{_localstatedir}/log/mlogc/data
%attr(0755,root,root) %{_bindir}/mlogc
%attr(0755,root,root) %{_bindir}/mlogc-batch-load


%changelog
* Mon May  7 2012 Joe Orton <jorton@redhat.com> - 2.6.5-3
- packaging fixes

* Fri Apr 27 2012 Peter Vrabec <pvrabec@redhat.com> 2.6.5-2
- fix license tag

* Thu Apr 05 2012 Peter Vrabec <pvrabec@redhat.com> 2.6.5-1
- upgrade & move rules into new package mod_security_crs

* Fri Feb 10 2012 Petr Pisar <ppisar@redhat.com> - 2.5.13-3
- Rebuild against PCRE 8.30
- Do not install non-existing files

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed May 3 2011 Michael Fleming <mfleming+rpm@thatfleminggent.com> - 2.5.13-1
- Newer upstream version

* Wed Jun 30 2010 Michael Fleming <mfleming+rpm@thatfleminggent.com> - 2.5.12-3
- Fix log dirs and files ordering per bz#569360

* Thu Apr 29 2010 Michael Fleming <mfleming+rpm@thatfleminggent.com> - 2.5.12-2
- Fix SecDatadir and minimal config per bz #569360

* Sat Feb 13 2010 Michael Fleming <mfleming+rpm@thatfleminggent.com> - 2.5.12-1
- Update to latest upstream release
- SECURITY: Fix potential rules bypass and denial of service (bz#563576)

* Fri Nov 6 2009 Michael Fleming <mfleming+rpm@thatfleminggent.com> - 2.5.10-2
- Fix rules and Apache configuration (bz#533124)

* Thu Oct 8 2009 Michael Fleming <mfleming+rpm@thatfleminggent.com> - 2.5.10-1
- Upgrade to 2.5.10 (with Core Rules v2)

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Mar 12 2009 Michael Fleming <mfleming+rpm@thatfleminggent.com> 2.5.9-1
- Update to upstream release 2.5.9
- Fixes potential DoS' in multipart request and PDF XSS handling

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Dec 29 2008 Michael Fleming <mfleming+rpm@enlartenment.com> 2.5.7-1
- Update to upstream 2.5.7
- Reinstate mlogc

* Sat Aug 2 2008 Michael Fleming <mfleming+rpm@enlartenment.com> 2.5.6-1
- Update to upstream 2.5.6
- Remove references to mlogc, it no longer ships in the main tarball.
- Link correctly vs. libxml2 and lua (bz# 445839)
- Remove bogus LoadFile directives as they're no longer needed.

* Sun Apr 13 2008 Michael Fleming <mfleming+rpm@enlartenment.com> 2.1.7-1
- Update to upstream 2.1.7

* Sat Feb 23 2008 Michael Fleming <mfleming+rpm@enlartenment.com> 2.1.6-1
- Update to upstream 2.1.6 (Extra features including SecUploadFileMode)

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.1.5-3
- Autorebuild for GCC 4.3

* Sat Jan 27 2008 Michael Fleming <mfleming+rpm@enlartenment.com> 2.1.5-2
- Update to 2.1.5 (bz#425986)
- "blocking" -> "optional_rules" per tarball ;-)


* Thu Sep  13 2007 Michael Fleming <mfleming+rpm@enlartenment.com> 2.1.3-1
- Update to 2.1.3
- Update License tag per guidelines.

* Mon Sep  3 2007 Joe Orton <jorton@redhat.com> 2.1.1-3
- rebuild for fixed 32-bit APR (#254241)

* Wed Aug 29 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 2.1.1-2
- Rebuild for selinux ppc32 issue.

* Tue Jun 19 2007 Michael Fleming <mfleming+rpm@enlartenment.com> 2.1.1-1
- New upstream release
- Drop ASCIIZ rule (fixed upstream)
- Re-enable protocol violation/anomalies rules now that REQUEST_FILENAME
  is fixed upstream.

* Sun Apr 1 2007 Michael Fleming <mfleming+rpm@enlartenment.com> 2.1.0-3
- Automagically configure correct library path for libxml2 library.
- Add LoadModule for mod_unique_id as the logging wants this at runtime

* Mon Mar 26 2007 Michael Fleming <mfleming+rpm@enlartenment.com> 2.1.0-2
- Fix DSO permissions (bz#233733)

* Tue Mar 13 2007 Michael Fleming <mfleming+rpm@enlartenment.com> 2.1.0-1
- New major release - 2.1.0
- Fix CVE-2007-1359 with a local rule courtesy of Ivan Ristic
- Addition of core ruleset
- (Build)Requires libxml2 and pcre added.

* Sun Sep 3 2006 Michael Fleming <mfleming+rpm@enlartenment.com> 1.9.4-2
- Rebuild
- Fix minor longstanding braino in included sample configuration (bz #203972)

* Mon May 15 2006 Michael Fleming <mfleming+rpm@enlartenment.com> 1.9.4-1
- New upstream release

* Tue Apr 11 2006 Michael Fleming <mfleming+rpm@enlartenment.com> 1.9.3-1
- New upstream release
- Trivial spec tweaks

* Wed Mar 1 2006 Michael Fleming <mfleming+rpm@enlartenment.com> 1.9.2-3
- Bump for FC5

* Fri Feb 10 2006 Michael Fleming <mfleming+rpm@enlartenment.com> 1.9.2-2
- Bump for newer gcc/glibc

* Wed Jan 18 2006 Michael Fleming <mfleming+rpm@enlartenment.com> 1.9.2-1
- New upstream release

* Fri Dec 16 2005 Michael Fleming <mfleming+rpm@enlartenment.com> 1.9.1-2
- Bump for new httpd

* Thu Dec 1 2005 Michael Fleming <mfleming+rpm@enlartenment.com> 1.9.1-1
- New release 1.9.1 

* Wed Nov 9 2005 Michael Fleming <mfleming+rpm@enlartenment.com> 1.9-1
- New stable upstream release 1.9

* Sat Jul 9 2005 Michael Fleming <mfleming+rpm@enlartenment.com> 1.8.7-4
- Add Requires: httpd-mmn to get the appropriate "module magic" version
  (thanks Ville Skytta)
- Disabled an overly-agressive rule or two..

* Sat Jul 9 2005 Michael Fleming <mfleming+rpm@enlartenment.com> 1.8.7-3
- Correct Buildroot
- Some sensible and safe rules for common apps in mod_security.conf

* Thu May 19 2005 Michael Fleming <mfleming+rpm@enlartenment.com> 1.8.7-2
- Don't strip the module (so we can get a useful debuginfo package)

* Thu May 19 2005 Michael Fleming <mfleming+rpm@enlartenment.com> 1.8.7-1
- Initial spin for Extras
