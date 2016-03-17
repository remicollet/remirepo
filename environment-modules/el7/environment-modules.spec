Name:           environment-modules
Version:        3.2.10
Release:        10%{?dist}
Summary:        Provides dynamic modification of a user's environment

Group:          System Environment/Base
License:        GPLv2+
URL:            http://modules.sourceforge.net/
Source0:        http://downloads.sourceforge.net/modules/modules-%{version}.tar.bz2
Source1:        modules.sh
Source2:        createmodule.sh
Source3:        createmodule.py
Patch0:         environment-modules-3.2.7-bindir.patch
# Comment out stray module use in modules file when not using versioning
# https://bugzilla.redhat.com/show_bug.cgi?id=895555
Patch1:         environment-modules-versioning.patch
# Fix module clear command
# https://bugzilla.redhat.com/show_bug.cgi?id=895551
Patch2:         environment-modules-clear.patch
# Patch from modules list to add completion to avail command
Patch3:         environment-modules-avail.patch
Patch4:         environment-modules-3.2.9-call-test-by-full-path-in-csh.patch
Patch5:         environment-modules-3.2.10-ignore-nested-dirs.patch
Patch6:         environment-modules-3.2.10-unload-from-module.patch

BuildRequires:  tcl-devel, tclx-devel, libX11-devel
BuildRequires:  dejagnu
BuildRequires:  man
#For ps in startup script
Requires:       procps

%description
The Environment Modules package provides for the dynamic modification of
a user's environment via modulefiles.

Each modulefile contains the information needed to configure the shell
for an application. Once the Modules package is initialized, the
environment can be modified on a per-module basis using the module
command which interprets modulefiles. Typically modulefiles instruct
the module command to alter or set shell environment variables such as
PATH, MANPATH, etc. modulefiles may be shared by many users on a system
and users may have their own collection to supplement or replace the
shared modulefiles.

Modules can be loaded and unloaded dynamically and atomically, in an
clean fashion. All popular shells are supported, including bash, ksh,
zsh, sh, csh, tcsh, as well as some scripting languages such as perl.

Modules are useful in managing different versions of applications.
Modules can also be bundled into metamodules that will load an entire
suite of different applications.

NOTE: You will need to get a new shell after installing this package to
have access to the module alias.


%prep
%setup -q -n modules-%{version}
%patch0 -p1 -b .bindir
%patch1 -p1 -b .versioning
%patch2 -p1 -b .clear
%patch3 -p1 -b .avail
%patch4 -p1 -b .call-test-by-full-path-in-csh
%patch5 -p1 -b .ignore-nested-dirs
%patch6 -p1 -b .unload-from-module


%build
%configure --disable-versioning \
           --prefix=%{_datadir} \
           --exec-prefix=%{_datadir}/Modules \
           --with-man-path=$(manpath) \
           --with-module-path=%{_sysconfdir}/modulefiles
#           --with-debug=42 --with-log-facility-debug=stderr
make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/profile.d
cp -p %SOURCE1 $RPM_BUILD_ROOT%{_sysconfdir}/profile.d/modules.sh
cp -p %SOURCE2 %SOURCE3 $RPM_BUILD_ROOT%{_datadir}/Modules/bin
ln -s %{_datadir}/Modules/init/csh $RPM_BUILD_ROOT%{_sysconfdir}/profile.d/modules.csh
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/modulefiles


%check
make test


%files
%doc LICENSE.GPL README TODO
%{_sysconfdir}/modulefiles
%config(noreplace) %{_sysconfdir}/profile.d/*
%{_bindir}/modulecmd
%dir %{_datadir}/Modules
%{_datadir}/Modules/bin/
%dir %{_datadir}/Modules/init
%config(noreplace) %{_datadir}/Modules/init/*
%config(noreplace) %{_datadir}/Modules/init/.modulespath
%{_datadir}/Modules/modulefiles
%{_mandir}/man1/module.1.gz
%{_mandir}/man4/modulefile.4.gz


%changelog
* Mon Jun 22 2015 Jan Synáček <jsynacek@redhat.com> - 3.2.10-10
- fix: createmodule scripts incorrectly handles env vars prefixed/suffixed without colon (#1233223)

* Wed Apr 29 2015 Jan Synáček <jsynacek@redhat.com> - 3.2.10-9
- fix: SourceVers wrongly sets version in nested directory (#1180652)
- fix: unload from loaded modulefile broken (#1117327)

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 3.2.10-8
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 3.2.10-7
- Mass rebuild 2013-12-27

* Thu Aug  8 2013 Jan Synáček <jsynacek@redhat.com> - 3.2.10-6
- Call test command in csh alias by its full path (bug #977331)

* Tue May 14 2013 Orion Poplawski <orion@cora.nwra.com> - 3.2.10-5
- Really do not replace modified profile.d scripts (bug #962762)
- Specfile cleanup

* Wed Apr 17 2013 Orion Poplawski <orion@cora.nwra.com> - 3.2.10-4
- Do not replace modified profile.d scripts (bug #953199)

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Jan 15 2013 Orion Poplawski <orion@cora.nwra.com> - 3.2.10-2
- Add patch to comment out stray module use in modules file when not using
  versioning (bug #895555)
- Add patch to fix module clear command (bug #895551)
- Add patch from modules list to add completion to avail command

* Fri Dec 21 2012 Orion Poplawski <orion@cora.nwra.com> - 3.2.10-1
- Update to 3.2.10
- Drop regex patch

* Wed Oct 31 2012 Orion Poplawski <orion@cora.nwra.com> - 3.2.9c-5
- Updated createmodule.sh, added createmodule.py, can handle path prefixes

* Fri Aug 24 2012 Orion Poplawski <orion@cora.nwra.com> - 3.2.9c-4
- Add patch to fix segfault from Tcl RexExp handling (bug 834580)

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.9c-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.9c-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Nov 29 2011 Orion Poplawski <orion@cora.nwra.com> - 3.2.9c-1
- Update to 3.2.9c (fixes bug 753760)

* Tue Nov 22 2011 Orion Poplawski <orion@cora.nwra.com> - 3.2.9b-2
- Make .modulespath a config file

* Tue Nov 15 2011 Orion Poplawski <orion@cora.nwra.com> - 3.2.9b-1
- Update to 3.2.9b

* Fri Nov 11 2011 Orion Poplawski <orion@cora.nwra.com> - 3.2.9a-2
- Add %%check section

* Fri Nov 11 2011 Orion Poplawski <orion@cora.nwra.com> - 3.2.9a-1
- Update to 3.2.9a
- Drop strcpy patch

* Thu Sep 22 2011 Orion Poplawski <orion@cora.nwra.com> - 3.2.8a-3
- Add patch to fix overlapping strcpy() in Remove_Path, hopefully fixes
  bug 737043

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.8a-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Oct 4 2010 Orion Poplawski <orion@cora.nwra.com> - 3.2.8a-1
- Update to 3.2.8a, changes --with-def-man-path to --with-man-path

* Mon Oct 4 2010 Orion Poplawski <orion@cora.nwra.com> - 3.2.8-1
- Update to 3.2.8
- Drop mandir patch, use --with-def-man-path

* Thu Jan 7 2010 Orion Poplawski <orion@cora.nwra.com> - 3.2.7b-7
- Add patch to set a sane default MANPATH
- Add createmodule.sh utility script for creating modulefiles
 
* Mon Nov 30 2009 Orion Poplawski <orion@cora.nwra.com> - 3.2.7b-6
- Add Requires: propcs (bug #54272)

* Mon Oct 26 2009 Orion Poplawski <orion@cora.nwra.com> - 3.2.7b-5
- Don't assume different shell init scripts exist (bug #530770)

* Fri Oct 23 2009 Orion Poplawski <orion@cora.nwra.com> - 3.2.7b-4
- Don't load bash init script when bash is running as "sh" (bug #529745)

* Mon Oct 19 2009 Orion Poplawski <orion@cora.nwra.com> - 3.2.7b-3
- Support different flavors of "sh" (bug #529493)

* Wed Sep 23 2009 Orion Poplawski <orion@cora.nwra.com> - 3.2.7b-2
- Add patch to fix modulecmd path in init files

* Wed Sep 23 2009 Orion Poplawski <orion@cora.nwra.com> - 3.2.7b-1
- Update to 3.2.7b

* Mon Sep 21 2009 Orion Poplawski <orion@cora.nwra.com> - 3.2.7-1
- Update to 3.2.7, fixes bug #524475
- Drop versioning patch fixed upstream

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.6-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.6-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Sep 3 2008 - Orion Poplawski <orion@cora.nwra.com> - 3.2.6-6
- Change %%patch -> %%patch0

* Fri Mar 14 2008 - Orion Poplawski <orion@cora.nwra.com> - 3.2.6-5
- Add BR libX11-devel so modulecmd can handle X resources

* Wed Mar  5 2008 - Orion Poplawski <orion@cora.nwra.com> - 3.2.6-4
- Add patch to fix extraneous version path entry properly
- Use --with-module-path to point to /etc/modulefiles for local modules,
  this also fixes bug #436041

* Sat Feb  9 2008 - Orion Poplawski <orion@cora.nwra.com> - 3.2.6-3
- Rebuild for gcc 3.4

* Thu Jan 03 2008 - Alex Lancaster <alexlan at fedoraproject.org> - 3.2.6-2
- Rebuild for new Tcl (8.5).

* Fri Nov  2 2007 - Orion Poplawski <orion@cora.nwra.com> - 3.2.6-1
- Update to 3.2.6

* Tue Aug 21 2007 - Orion Poplawski <orion@cora.nwra.com> - 3.2.5-2
- Update license tag to GPLv2

* Fri Feb 16 2007 - Orion Poplawski <orion@cora.nwra.com> - 3.2.5-1
- Update to 3.2.5

* Wed Feb 14 2007 - Orion Poplawski <orion@cora.nwra.com> - 3.2.4-2
- Rebuild for Tcl downgrade

* Fri Feb 09 2007 - Orion Poplawski <orion@cora.nwra.com> - 3.2.4-1
- Update to 3.2.4

* Wed Dec 20 2006 - Orion Poplawski <orion@cora.nwra.com> - 3.2.3-3
- Add --with-version-path to set VERSIONPATH (bug 220260)

* Tue Aug 29 2006 - Orion Poplawski <orion@cora.nwra.com> - 3.2.3-2
- Rebuild for FC6

* Fri Jun  2 2006 - Orion Poplawski <orion@cora.nwra.com> - 3.2.3-1
- Update to 3.2.3

* Fri May  5 2006 - Orion Poplawski <orion@cora.nwra.com> - 3.2.2-1
- Update to 3.2.2

* Fri Mar 24 2006 - Orion Poplawski <orion@cora.nwra.com> - 3.2.1-1
- Update to 3.2.1

* Thu Feb  9 2006 - Orion Poplawski <orion@cora.nwra.com> - 3.2.0p1-1
- Update to 3.2.0p1

* Fri Jan 27 2006 - Orion Poplawski <orion@cora.nwra.com> - 3.2.0-2
- Add profile.d links

* Tue Jan 24 2006 - Orion Poplawski <orion@cora.nwra.com> - 3.2.0-1
- Fedora Extras packaging
