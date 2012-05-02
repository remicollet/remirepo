# Fedora 5, 6, and 7 versions includes SELinux policy module package
# Fedora 8 and 9 versions include policy in errata selinux-policy releases
# Fedora 10 onwards include policy in standard selinux-policy releases
# RHEL 5.5 onwards include policy in standard selinux-policy releases
%if 0%{?fedora} < 5 || 0%{?fedora} > 7 || 0%{?rhel}
%global selinux_module 0
%global selinux_types %{nil}
%global selinux_variants %{nil}
%global selinux_buildreqs %{nil}
%else
%global selinux_module 1
%global selinux_types %(awk '/^#[[:space:]]*SELINUXTYPE=/,/^[^#]/ { if ($3 == "-") printf "%s ", $2 }' /etc/selinux/config 2>/dev/null)
%global selinux_variants %([ -z "%{selinux_types}" ] && echo mls strict targeted || echo %{selinux_types})
%global selinux_buildreqs checkpolicy, selinux-policy-devel, hardlink
%endif

# apxs script location
%{!?_httpd_apxs: %global _httpd_apxs %{_sbindir}/apxs}

# Module Magic Number
%{!?_httpd_mmn: %global _httpd_mmn %(cat %{_includedir}/httpd/.mmn 2>/dev/null || echo missing-httpd-devel)}

# Configuration directory
%{!?_httpd_confdir: %global _httpd_confdir %{_sysconfdir}/httpd/conf.d}

# For httpd ≥ 2.4 we have a different filesystem layout
%if 0%{?fedora} > 17 || 0%{?rhel} > 6
%global httpd24 1
%global rundir /run
%else
%global httpd24 1
%global rundir %{_localstatedir}/run
%endif

Name:		mod_fcgid
Version:	2.3.7
Release:	3%{?dist}
Summary:	FastCGI interface module for Apache 2
Group:		System Environment/Daemons
License:	ASL 2.0
URL:		http://httpd.apache.org/mod_fcgid/
Source0:	http://www.apache.org/dist/httpd/mod_fcgid/mod_fcgid-%{version}.tar.bz2
Source1:	fcgid.conf
Source2:	mod_fcgid-2.1-README.RPM
Source3:	mod_fcgid-2.1-README.SELinux
Source4:	mod_fcgid-tmpfs.conf
Source5:	fcgid24.conf
Source10:	fastcgi.te
Source11:	fastcgi-2.5.te
Source12:	fastcgi.fc
Patch0:		mod_fcgid-2.3.4-fixconf-shellbang.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(id -nu)
BuildRequires:	httpd-devel >= 2.0, pkgconfig
Requires:	httpd-mmn = %{_httpd_mmn}
# sed required for fixconf script
Requires:	/bin/sed
# systemd-units needed for ownership of /etc/tmpfiles.d directory
%if 0%{?fedora} > 14 || 0%{?rhel} > 6
Requires:	systemd-units
%endif
# Make sure that selinux-policy is sufficiently up-to-date if it's installed
# FastCGI policy properly incorporated into EL 5.5
%if "%{?rhel}" == "5"
Conflicts:	selinux-policy < 2.4.6-279.el5
# No provide here because selinux-policy >= 2.4.6-279.el5 does the providing
Obsoletes:	mod_fcgid-selinux <= %{version}-%{release}
%endif
%if "%{?fedora}" == "8"
Conflicts:	selinux-policy < 3.0.8-123.fc8
%endif
%if "%{?fedora}" == "9"
Conflicts:	selinux-policy < 3.3.1-107.fc9
%endif
%if "%{?fedora}" == "10"
Conflicts:	selinux-policy < 3.5.13-8.fc10
%endif

%description
mod_fcgid is a binary-compatible alternative to the Apache module mod_fastcgi.
mod_fcgid has a new process management strategy, which concentrates on reducing
the number of fastcgi servers, and kicking out corrupt fastcgi servers as soon
as possible.

%if %{selinux_module}
%global selinux_policyver %(sed -e 's,.*selinux-policy-\\([^/]*\\)/.*,\\1,' /usr/share/selinux/devel/policyhelp || echo 0.0.0)
%global selinux_policynum %(echo %{selinux_policyver} | awk -F. '{ printf "%d%02d%02d", $1, $2, $3 }')
%package selinux
Summary:	  SELinux policy module supporting FastCGI applications with mod_fcgid
Group:		  System Environment/Base
BuildRequires:	  %{selinux_buildreqs}
# selinux-policy is required for directory ownership of %%{_datadir}/selinux/*
# Modules built against one version of a policy may not work with older policy
# versions, as noted on fedora-selinux-list:
# http://www.redhat.com/archives/fedora-selinux-list/2006-May/msg00102.html
# Hence the versioned dependency. The versioning will hopefully be replaced by
# an ABI version requirement or something similar in the future
Requires:	  selinux-policy >= %{selinux_policyver}
Requires:	  %{name} = %{version}-%{release}
Requires(post):	  /usr/sbin/semodule, /sbin/restorecon
Requires(postun): /usr/sbin/semodule, /sbin/restorecon

%description selinux
SELinux policy module supporting FastCGI applications with mod_fcgid.
%endif

%prep
%setup -q
cp -p %{SOURCE1} fcgid.conf
cp -p %{SOURCE2} README.RPM
cp -p %{SOURCE3} README.SELinux
cp -p %{SOURCE5} fcgid24.conf
%if 0%{?selinux_policynum} < 20501
cp -p %{SOURCE10} fastcgi.te
%else
cp -p %{SOURCE11} fastcgi.te
%endif
cp -p %{SOURCE12} fastcgi.fc

# Fix shellbang in fixconf script for our location of sed
%patch0 -p1

%build
APXS=%{_httpd_apxs} ./configure.apxs
make
%if %{selinux_module}
for selinuxvariant in %{selinux_variants}
do
	make NAME=${selinuxvariant} -f /usr/share/selinux/devel/Makefile
	mv fastcgi.pp fastcgi.pp.${selinuxvariant}
	make NAME=${selinuxvariant} -f /usr/share/selinux/devel/Makefile clean
done
%endif

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} MKINSTALLDIRS="mkdir -p" install
%if %{httpd24}
mkdir -p %{buildroot}{%{_httpd_confdir},%{_httpd_modconfdir}}
echo "LoadModule fcgid_module modules/mod_fcgid.so" > %{buildroot}%{_httpd_modconfdir}/10-fcgid.conf
install -D -m 644 fcgid24.conf %{buildroot}%{_httpd_confdir}/fcgid.conf
%else
install -D -m 644 fcgid.conf %{buildroot}%{_httpd_confdir}/fcgid.conf
%endif
install -d -m 755 %{buildroot}%{rundir}/mod_fcgid

# Include the manual as %%doc, don't need it elsewhere
%if %{httpd24}
rm -rf %{buildroot}%{_httpd_contentdir}/manual
%else
rm -rf %{buildroot}%{_var}/www/manual
%endif

# Make sure %%{rundir}/mod_fcgid exists at boot time for systems
# with %%{rundir} on tmpfs (#656625)
%if 0%{?fedora} > 14 || 0%{?rhel} > 6
install -d -m 755 %{buildroot}%{_sysconfdir}/tmpfiles.d
install -p -m 644 %{SOURCE4} %{buildroot}%{_sysconfdir}/tmpfiles.d/mod_fcgid.conf
%endif

# Install SELinux policy modules
%if %{selinux_module}
for selinuxvariant in %{selinux_variants}
do
	install -d %{buildroot}%{_datadir}/selinux/${selinuxvariant}
	install -p -m 644 fastcgi.pp.${selinuxvariant} \
		%{buildroot}%{_datadir}/selinux/${selinuxvariant}/fastcgi.pp
done
# Hardlink identical policy module packages together
hardlink -cv %{buildroot}%{_datadir}/selinux
%endif

%clean
rm -rf %{buildroot}

%if %{selinux_module}
%post selinux
# Install SELinux policy modules
for selinuxvariant in %{selinux_variants}
do
	/usr/sbin/semodule -s ${selinuxvariant} -i \
		%{_datadir}/selinux/${selinuxvariant}/fastcgi.pp &> /dev/null || :
done
# Fix up non-standard directory context from earlier packages
/sbin/restorecon -R %{rundir}/mod_fcgid || :

%postun selinux
# Clean up after package removal
if [ $1 -eq 0 ]; then
	# Remove SELinux policy modules
	for selinuxvariant in %{selinux_variants}; do
		/usr/sbin/semodule -s ${selinuxvariant} -r fastcgi &> /dev/null || :
	done
	# Clean up any remaining file contexts (shouldn't be any really)
	[ -d %{rundir}/mod_fcgid ] && \
		/sbin/restorecon -R %{rundir}/mod_fcgid &> /dev/null || :
fi
exit 0
%endif

%files
%defattr(-,root,root,-)
# mod_fcgid.html.en is explicitly encoded as ISO-8859-1
%doc CHANGES-FCGID LICENSE-FCGID NOTICE-FCGID README-FCGID STATUS-FCGID
%doc docs/manual/mod/mod_fcgid.html.en modules/fcgid/ChangeLog
%doc build/fixconf.sed
%{_libdir}/httpd/modules/mod_fcgid.so
%if %{httpd24}
%config(noreplace) %{_httpd_modconfdir}/10-fcgid.conf
%endif
%config(noreplace) %{_httpd_confdir}/fcgid.conf
%if 0%{?fedora} > 14 || 0%{?rhel} > 6
%{_sysconfdir}/tmpfiles.d/mod_fcgid.conf
%endif
%dir %attr(0755,apache,apache) %{rundir}/mod_fcgid/

%if %{selinux_module}
%files selinux
%defattr(-,root,root,-)
%doc fastcgi.fc fastcgi.te README.SELinux
%{_datadir}/selinux/*/fastcgi.pp
%endif

%changelog
* Wed May  2 2012 Remi Collet <RPMS@FamilleCollet.com> 2.3.7-3
- sync with rawhide, rebuild for remi repo

* Wed May  2 2012 Paul Howarth <paul@city-fan.org> 2.3.7-3
- Make %%files list more explicit

* Wed May  2 2012 Joe Orton <jorton@redhat.com> 2.3.7-2
- Use 10- prefix for conf file in conf.modules.d with httpd ≥ 2.4
- Use _httpd_confdir throughout

* Tue Apr 24 2012 Remi Collet <RPMS@FamilleCollet.com> 2.3.7-1
- update to 2.3.7, rebuild for remi repo

* Mon Apr 23 2012 Paul Howarth <paul@city-fan.org> 2.3.7-1
- Update to 2.3.7
  - Introduce FcgidWin32PreventOrphans directive on Windows to use OS Job
    Control Objects to terminate all running fcgi's when the worker process
    has been abruptly terminated (PR: 51078)
  - Periodically clean out the brigades that are pulling in the request body
    for handoff to the fcgid child (PR: 51749)
  - Resolve crash during graceful restarts (PR: 50309)
  - Solve latency/congestion of resolving effective user file access rights
    when no such info is desired, for config-related filename stats (PR: 51020)
  - Fix regression in 2.3.6 that broke process controls when using
    vhost-specific configuration
  - Account for first process in class in the spawn score
- Drop patch for CVE-2012-1181, now included in upstream release

* Sat Mar 31 2012 Remi Collet <RPMS@FamilleCollet.com> 2.3.6-6
- rebuild httpd 2.4

* Tue Mar 27 2012 Paul Howarth <paul@city-fan.org> 2.3.6-6
- Fix compatibility with httpd 2.4 in F-18/RHEL-7 onwards
- Use /run rather than /var/run from F-15/RHEL-7 onwards

* Sun Jan 22 2012 Paul Howarth <paul@city-fan.org> 2.3.6-5
- Fix regression in 2.3.6 that broke process controls when using vhost-specific
  configuration (upstream issue 49902, #783742, CVE-2012-1181)

* Fri Jan  6 2012 Paul Howarth <paul@city-fan.org> 2.3.6-4
- Nobody else likes macros for commands

* Tue Feb  8 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> 2.3.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec  1 2010 Paul Howarth <paul@city-fan.org> 2.3.6-2
- Add /etc/tmpfiles.d/mod_fcgid.conf for builds on Fedora 15 onwards to
  support running with /var/run on tmpfs (#656625)

* Thu Nov  4 2010 Paul Howarth <paul@city-fan.org> 2.3.6-1
- Update to 2.3.6 (see CHANGES-FCGID for full details)
  - Fix possible stack buffer overwrite (CVE-2010-3872)
  - Change the default for FcgidMaxRequestLen from 1GB to 128K; administrators
    should change this to an appropriate value based on site requirements
  - Correct a problem that resulted in FcgidMaxProcesses being ignored in some
    situations
  - Return 500 instead of segfaulting when the application returns no output
- Don't include SELinux policy for RHEL-5 builds since RHEL >= 5.5 includes it
- Explicitly require /bin/sed for fixconf script

* Tue Jun  8 2010 Paul Howarth <paul@city-fan.org> 2.3.5-2
- SELinux policy module not needed for RHEL-6 onwards

* Wed Jan 27 2010 Paul Howarth <paul@city-fan.org> 2.3.5-1
- Update to 2.3.5 (see CHANGES-FCGID for details)
- Drop upstream svn patch

* Wed Oct 21 2009 Paul Howarth <paul@city-fan.org> 2.3.4-2
- Add fixes from upstream svn for a number of issues, most notably that the
  fixconf script had an error in the regexp, which resulted in a prefix of
  "FcgidFcgid" on the updated directives

* Mon Oct 12 2009 Paul Howarth <paul@city-fan.org> 2.3.4-1
- Update to 2.3.4 (configuration directives changed again)
- Add fixconf.sed script for config file directives update

* Fri Sep 25 2009 Paul Howarth <paul@city-fan.org> 2.3.1-2.20090925svn818270
- Update to svn revision 818270
- DESTDIR and header detection patches upstreamed
- Build SELinux policy module for EL-5; support in EL-5.3 is incomplete and
  will be fixed in EL-5.5 (#519369)
- Drop aliases httpd_sys_content_r{a,o,w}_t -> httpd_fastcgi_content_r{a,o,w}_t
  from pre-2.5 SElinux policy module as these types aren't defined there

* Wed Sep 23 2009 Paul Howarth <paul@city-fan.org> 2.3.1-1.20090923svn817978
- Update to post-2.3.1 svn snapshot
- Upstream moved to apache.org
- License changed to ASL 2.0
- Use FCGID-prefixed config file options (old ones deprecated)
- Lots of documentation changes
- Renumber sources
- Don't defer to mod_fastcgi if both are present
- Drop gawk buildreq
- Add patches fixing RPM build issues (DESTDIR support, header detection)

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue May 26 2009 Paul Howarth <paul@city-fan.org> 2.2-12
- Don't use /etc/httpd/run as basis of "run" directory as its DAC permissions
  are not permissive enough in F-11 onwards; instead, revert to
  /var/run/mod_fcgid and tweak default config accordingly (#502273)

* Sun May 17 2009 Paul Howarth <paul@city-fan.org> 2.2-11
- Follow link /etc/httpd/run and make our "run" directory a subdir of wherever
  that leads (#501123)

* Mon Apr  6 2009 Paul Howarth <paul@city-fan.org> 2.2-10
- EL 5.3 now has SELinux support in the main selinux-policy package so handle
  that release as per Fedora >= 8, except that the RHEL selinux-policy package
  doesn't Obsolete/Provide mod_fcgid-selinux like the Fedora version, so do
  the obsoletion here instead

* Thu Feb 26 2009 Paul Howarth <paul@city-fan.org> 2.2-9
- Update documentation for MoinMoin, Rails (#476658), and SELinux

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Nov 12 2008 Paul Howarth <paul@city-fan.org> 2.2-7
- SELinux policy module no longer built for Fedora 8 onwards as it is
  obsoleted by the main selinux-policy package
- Conflicts for selinux-policy packages older than the releases where mod_fcgid
  policy was incorporated have been added for Fedora 8, 9, and 10 versions, to
  ensure that SELinux support will work if installed

* Tue Oct 21 2008 Paul Howarth <paul@city-fan.org> 2.2-6
- SELinux policy module rewritten to merge fastcgi and system script domains
  in preparation for merge into main selinux-policy package (#462318)
- Try to determine supported SELinux policy types by reading /etc/selinux/config

* Thu Jul 24 2008 Paul Howarth <paul@city-fan.org> 2.2-5
- Tweak selinux-policy version detection macro to work with current Rawhide

* Thu Feb 14 2008 Paul Howarth <paul@city-fan.org> 2.2-4
- Rebuild with gcc 4.3.0 for Fedora 9

* Mon Jan 14 2008 Paul Howarth <paul@city-fan.org> 2.2-3
- Update SELinux policy to fix occasional failures on restarts
  (move shared memory file into /var/run/mod_fcgid directory)

* Thu Jan  3 2008 Paul Howarth <paul@city-fan.org> 2.2-2
- Update SELinux policy to support file transition to httpd_tmp_t for
  temporary files

* Fri Sep 14 2007 Paul Howarth <paul@city-fan.org> 2.2-1
- Update to version 2.2
- Make sure docs are encoded as UTF-8

* Mon Sep  3 2007 Joe Orton <jorton@redhat.com> 2.1-6
- rebuild for fixed 32-bit APR (#254241)

* Thu Aug 23 2007 Paul Howarth <paul@city-fan.org> 2.1-5
- Update source URL to point to downloads.sf.net rather than dl.sf.net
- Upstream released new tarball without changing version number, though the
  only change was in arch/win32/fcgid_pm_win.c, which is not used to build the
  RPM package
- Clarify license as GPL (unspecified/any version)
- Unexpand tabs in spec
- Add buildreq of gawk

* Fri Aug  3 2007 Paul Howarth <paul@city-fan.org> 2.1-4
- Add buildreq of pkgconfig, a missing dependency of both apr-devel and
  apr-util-devel on FC5

* Fri Jun 15 2007 Paul Howarth <paul@city-fan.org> 2.1-3
- Major update of SELinux policy, supporting accessing data on NFS/CIFS shares
  and a new boolean, httpd_fastcgi_can_sendmail, to allow connections to SMTP
  servers
- Fix for SELinux policy on Fedora 7, which didn't work due to changes in the
  permissions macros in the underlying selinux-policy package

* Wed Mar 21 2007 Paul Howarth <paul@city-fan.org> 2.1-2
- Add RHEL5 with SELinux support
- Rename README.Fedora to README.RPM

* Fri Feb 16 2007 Paul Howarth <paul@city-fan.org> 2.1-1
- Update to 2.1
- Update documentation and patches
- Rename some source files to reduce chances of conflicting names
- Include SharememPath directive in conf file to avoid unfortunate upstream
  default location

* Mon Oct 30 2006 Paul Howarth <paul@city-fan.org> 2.0-1
- Update to 2.0
- Source is now hosted at sourceforge.net
- Update docs

* Wed Sep  6 2006 Paul Howarth <paul@city-fan.org> 1.10-7
- Include the right README* files

* Tue Aug 29 2006 Paul Howarth <paul@city-fan.org> 1.10-6
- Buildreqs for FC5 now identical to buildreqs for FC6 onwards

* Fri Jul 28 2006 Paul Howarth <paul@city-fan.org> 1.10-5
- Split off SELinux module into separate subpackage to avoid dependency on
  the selinux-policy package for the main package

* Fri Jul 28 2006 Paul Howarth <paul@city-fan.org> 1.10-4
- SELinux policy packages moved from %%{_datadir}/selinux/packages/POLICYNAME
  to %%{_datadir}/selinux/POLICYNAME
- hardlink identical policy module packages together to avoid duplicate files

* Thu Jul 20 2006 Paul Howarth <paul@city-fan.org> 1.10-3
- Adjust buildreqs for FC6 onwards
- Figure out where top_dir is dynamically since the /etc/httpd/build
  symlink is gone in FC6

* Wed Jul  5 2006 Paul Howarth <paul@city-fan.org> 1.10-2
- SELinux policy update: allow FastCGI apps to do DNS lookups

* Tue Jul  4 2006 Paul Howarth <paul@city-fan.org> 1.10-1
- Update to 1.10
- Expand tabs to shut rpmlint up

* Tue Jul  4 2006 Paul Howarth <paul@city-fan.org> 1.09-10
- SELinux policy update:
  * allow httpd to read httpd_fastcgi_content_t without having the
  | httpd_builtin_scripting boolean set
  * allow httpd_fastcgi_script_t to read /etc/resolv.conf without
  | having the httpd_can_network_connect boolean set

* Sun Jun 18 2006 Paul Howarth <paul@city-fan.org> 1.09-9
- Discard output of semodule in %%postun
- Include some documentation from upstream

* Fri Jun  9 2006 Paul Howarth <paul@city-fan.org> 1.09-8
- Change default context type for socket directory from var_run_t to
  httpd_fastcgi_sock_t for better separation

* Thu Jun  8 2006 Paul Howarth <paul@city-fan.org> 1.09-7
- Add SELinux policy module and README.Fedora
- Conflict with selinux-policy versions older than what we're built on

* Mon May 15 2006 Paul Howarth <paul@city-fan.org> 1.09-6
- Instead of conflicting with mod_fastcgi, don't add the handler for .fcg etc.
  if mod_fastcgi is present

* Fri May 12 2006 Paul Howarth <paul@city-fan.org> 1.09-5
- Use correct handler name in fcgid.conf
- Conflict with mod_fastcgi
- Create directory %%{_localstatedir}/run/mod_fcgid for sockets

* Thu May 11 2006 Paul Howarth <paul@city-fan.org> 1.09-4
- Cosmetic tweaks (personal preferences)
- Don't include INSTALL.TXT, nothing of use to end users

* Wed May 10 2006 Thomas Antony <thomas@antony.eu> 1.09-3
- Initial release
