# remirepo spec file for memcached
# lastest version with SASL support enabled, from:
#
# Fedora spec file for memcached
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#
%global username   memcached
%global groupname  memcached

%if 0%{?fedora} >= 17 || 0%{?rhel} >= 7
%global with_systemd 1
%else
%global with_systemd 0
%endif

%global with_sasl    1

# Regression tests take a long time, you can skip 'em with this
%{!?runselftest: %global runselftest 1}

Name:           memcached
Version:        1.4.36
Release:        1%{?dist}
Epoch:          0
Summary:        High Performance, Distributed Memory Object Cache

Group:          System Environment/Daemons
License:        BSD
URL:            http://www.memcached.org/
Source0:        http://www.memcached.org/files/%{name}-%{version}.tar.gz
Source1:        memcached.sysconfig

# custom init script
Source2:        memcached.sysv
# custom unit file
Source3:        memcached.service

Patch1:         memcached-unit.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
%if "%{?vendor}" == "Remi Collet"
BuildRequires:  libevent-devel > 2
%else
BuildRequires:  libevent-devel
%endif
%if 0%{?fedora} > 22
BuildRequires:  perl-generators
%endif
BuildRequires:  perl(Test::More), perl(Test::Harness)
%if %{with_sasl}
BuildRequires:  cyrus-sasl-devel
%endif

%if %{with_systemd}
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
# For triggerun
Requires(post): systemd-sysv
%else
Requires: initscripts
Requires(post): /sbin/chkconfig
Requires(preun): /sbin/chkconfig, /sbin/service
Requires(postun): /sbin/service
%endif
Requires(pre):  shadow-utils

# as of 3.5.5-4 selinux has memcache included
Obsoletes: memcached-selinux


%description
memcached is a high-performance, distributed memory object caching
system, generic in nature, but intended for use in speeding up dynamic
web applications by alleviating database load.


%package devel
Summary:	Files needed for development using memcached protocol
Group:		Development/Libraries 
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description devel
Install memcached-devel if you are developing C/C++ applications that require
access to the memcached binary include files.


%prep
%setup -q
%patch1 -p1 -b .unit


%build
# compile with full RELRO
export CFLAGS="%{optflags} -pie -fpie"
export LDFLAGS="-Wl,-z,relro,-z,now"

%configure \
%if %{with_sasl}
   --enable-sasl
%endif

sed -i 's/-Werror / /' Makefile
make %{?_smp_mflags}


%check
%if %runselftest
%if 0%{?rhel} == 5
rm t/chunked-items.t
%endif

make test
%endif


%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot} INSTALL="%{__install} -p"
# remove memcached-debug
rm -f %{buildroot}/%{_bindir}/memcached-debug

# Perl script for monitoring memcached
install -Dp -m0755 scripts/memcached-tool %{buildroot}%{_bindir}/memcached-tool
install -Dp -m0644 scripts/memcached-tool.1 \
        %{buildroot}%{_mandir}/man1/memcached-tool.1

%if %{with_systemd}
# Unit file
%if 0%{?fedora} < 25
install -Dp -m0644 %{SOURCE3} %{buildroot}%{_unitdir}/memcached.service
%else
install -Dp -m0644 scripts/memcached.service \
        %{buildroot}%{_unitdir}/memcached.service
%endif
%else
# Init script
install -Dp -m0755 %{SOURCE2} %{buildroot}%{_initrddir}/memcached

# pid directory
mkdir -p %{buildroot}/%{_localstatedir}/run/memcached
%endif


# Default configs
%if 0%{?fedora} < 25
mkdir -p %{buildroot}/%{_sysconfdir}/sysconfig
cat <<EOF >%{buildroot}/%{_sysconfdir}/sysconfig/%{name}
PORT="11211"
USER="%{username}"
MAXCONN="1024"
CACHESIZE="64"
OPTIONS=""
EOF

# Constant timestamp on the config file.
touch -r %{SOURCE1} %{buildroot}/%{_sysconfdir}/sysconfig/%{name}
%else
install -Dp -m0644 %{SOURCE1} %{buildroot}/%{_sysconfdir}/sysconfig/%{name}
%endif


%clean
rm -rf %{buildroot}


%pre
getent group %{groupname} >/dev/null || groupadd -r %{groupname}
getent passwd %{username} >/dev/null || \
%if %{with_systemd}
useradd -r -g %{groupname} -d /run/memcached \
%else
useradd -r -g %{groupname} -d %{_localstatedir}/run/memcached \
%endif
    -s /sbin/nologin -c "Memcached daemon" %{username}
exit 0


%post
%if 0%{?systemd_post:1}
%systemd_post %{name}.service
%else
if [ $1 = 1 ]; then
    # Initial installation
    /sbin/chkconfig --add %{name}
fi
%endif


%preun
%if 0%{?systemd_preun:1}
%systemd_preun %{name}.service
%else
if [ "$1" = 0 ] ; then
    # Package removal, not upgrade
    /sbin/service %{name} stop > /dev/null 2>&1
    /sbin/chkconfig --del %{name}
fi
exit 0
%endif


%postun
%if 0%{?systemd_postun_with_restart:1}
%systemd_postun_with_restart %{name}.service
%else
if [ "$1" -ge 1 ]; then
    /sbin/service %{name} condrestart > /dev/null 2>&1
fi
exit 0
%endif

%triggerun -- memcached
%if %{with_systemd}
if [ -f /etc/rc.d/init.d/memcached ]; then
# Save the current service runlevel info
# User must manually run systemd-sysv-convert --apply memcached
# to migrate them to systemd targets
/usr/bin/systemd-sysv-convert --save memcached >/dev/null 2>&1 ||:

# Run these because the SysV package being removed won't do them
/sbin/chkconfig --del memcached >/dev/null 2>&1 || :
/bin/systemctl try-restart memcached.service >/dev/null 2>&1 || :
fi
%endif


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc AUTHORS ChangeLog NEWS README.md doc/CONTRIBUTORS doc/*.txt
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%{_bindir}/memcached-tool
%{_bindir}/memcached
%{_mandir}/man1/memcached-tool.1*
%{_mandir}/man1/memcached.1*
%if %{with_systemd}
%{_unitdir}/memcached.service
%else
%{_initrddir}/memcached
%dir %attr(755,%{username},%{groupname}) %{_localstatedir}/run/memcached
%endif


%files devel
%defattr(-,root,root,-)
%{_includedir}/memcached/*


%changelog
* Wed Mar 22 2017 Remi Collet <remi@remirepo.net> - 0:1.4.36-1
- Update to 1.4.36

* Mon Feb 27 2017 Remi Collet <remi@remirepo.net> - 0:1.4.35-1
- Update to 1.4.35

* Tue Jan 17 2017 Remi Collet <remi@remirepo.net> - 0:1.4.34-1
- Update to 1.4.34

* Tue Nov  1 2016 Remi Collet <remi@remirepo.net> - 0:1.4.33-1
- Update to 1.4.33

* Thu Oct 13 2016 Remi Collet <remi@remirepo.net> - 0:1.4.32-1
- Update to 1.4.32

* Fri Sep  2 2016 Remi Collet <remi@remirepo.net> - 0:1.4.31-1
- Update to 1.4.31

* Sat Aug 13 2016 Remi Collet <remi@remirepo.net> - 0:1.4.30-1
- Update to 1.4.30

* Mon Jul 18 2016 Remi Collet <remi@remirepo.net> - 0:1.4.29-1
- Update to 1.4.29

* Thu Jul 14 2016 Miroslav Lichvar <mlichvar@redhat.com> - 0:1.4.29-1
- update to 1.4.29

* Tue Jul 12 2016 Miroslav Lichvar <mlichvar@redhat.com> - 0:1.4.28-1
- update to 1.4.28
- listen only on loopback interface by default (#1182542)
- use upstream unit file (#1350939)
- remove obsolete macros and scriptlet

* Sun Jul  3 2016 Remi Collet <rpms@famillecollet.com> - 0:1.4.28-1
- Update to 1.4.28

* Sat Jun 25 2016 Remi Collet <rpms@famillecollet.com> - 0:1.4.27-1
- Update to 1.4.27
- run all tests during the build

* Wed Jun 22 2016 Remi Collet <rpms@famillecollet.com> - 0:1.4.26-1
- Update to 1.4.26 (backported from Fedora)

* Sun Jan  3 2016 Remi Collet <rpms@famillecollet.com> - 0:1.4.25-1
- Update to 1.4.25

* Mon Jan  5 2015 Remi Collet <rpms@famillecollet.com> - 0:1.4.22-1
- Update to 1.4.22

* Sun Oct 26 2014 Remi Collet <rpms@famillecollet.com> - 0:1.4.21-1
- Update to 1.4.21
- fix license handling

* Mon May 12 2014 Remi Collet <rpms@famillecollet.com> - 0:1.4.20-1
- Update to 1.4.20

* Fri May  2 2014 Remi Collet <rpms@famillecollet.com> - 0:1.4.19-1
- Update to 1.4.19

* Mon Apr  7 2014 Remi Collet <rpms@famillecollet.com> - 0:1.4.17-1
- Update to 1.4.17
- Sync with rawhide
- Build against libevent 2

* Sun Dec  2 2012 Remi Collet <rpms@famillecollet.com> - 0:1.4.15-2.1
- build test without SASL

* Mon Nov 26 2012 Remi Collet <rpms@famillecollet.com> - 0:1.4.15-2
- enable SASL support

* Mon Nov 26 2012 Remi Collet <rpms@famillecollet.com> - 0:1.4.15-1
- sync with rawhide, backport for remi repo

* Tue Nov 20 2012 Joe Orton <jorton@redhat.com> - 0:1.4.15-2
- BR perl(Test::Harness)

* Tue Nov 20 2012 Joe Orton <jorton@redhat.com> - 0:1.4.15-1
- update to 1.4.15 (#782395)
- switch to simple systemd service (#878198)
- use systemd scriptlet macros (Václav Pavlín, #850204)

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.4.13-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri May 04 2012 Jon Ciesla <limburgher@gmail.com> - 0:1.4.13-2
- Migrate to systemd, 783112.

* Tue Feb  7 2012 Paul Lindner <lindner@mirth.inuus.com> - 0:1.4.13-1
- Upgrade to memcached 1.4.13
- http://code.google.com/p/memcached/wiki/ReleaseNotes1413
- http://code.google.com/p/memcached/wiki/ReleaseNotes1412
- http://code.google.com/p/memcached/wiki/ReleaseNotes1411

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.4.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Nov  9 2011 Paul Lindner <lindner@mirth.inuus.com> - 0:1.4.10-1
- Upgrade to memcached 1.4.10 (http://code.google.com/p/memcached/wiki/ReleaseNotes1410)

* Tue Aug 16 2011 Paul Lindner <lindner@inuus.com> - 0:1.4.7-1
- Upgrade to memcached 1.4.7 (http://code.google.com/p/memcached/wiki/ReleaseNotes147)
- Fix some rpmlint errors/warnings.

* Tue Aug  2 2011 Paul Lindner <lindner@inuus.com> - 0:1.4.6-1
- Upgrade to memcached-1.4.6

* Wed Feb 16 2011 Joe Orton <jorton@redhat.com> - 0:1.4.5-7
- fix build

* Mon Feb 14 2011 Paul Lindner <lindner@inuus.com> - 0:1.4.5-6
- Rebuild for updated libevent

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.4.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Nov 28 2010 Paul Lindner <lindner@inuus.com> - 0:1.4.5-4
- Add code to deal with /var/run/memcached on tmpfs

* Wed Sep  8 2010 Paul Lindner <lindner@inuus.com> - 0:1.4.5-3
- Apply patch from memcached issue #60, solves Bugzilla 631051

* Tue Jun 15 2010 Remi Collet <rpms@famillecollet.com> - 1.4.5-2.el4.1
- also use /var/run/memcached/memcached.pid on EL-4

* Sun Jun 13 2010 Remi Collet <rpms@famillecollet.com> - 1.4.5-2
- sync with rawhide rebuild for remi repository
  EL-5.5 : rebuild against latest libevent

* Wed May 26 2010 Joe Orton <jorton@redhat.com> - 0:1.4.5-2
- LSB compliance fixes for init script
- don't run the test suite as root
- ensure a constant timestamp on the sysconfig file

* Sun Apr  4 2010 Remi Collet <rpms@famillecollet.com> - 0:1.4.5-1
- rebuild for remi repository

* Sun Apr  4 2010 Paul Lindner <lindner@inuus.com> - 0:1.4.5-1
- Upgrade to upstream memcached-1.4.5 (http://code.google.com/p/memcached/wiki/ReleaseNotes145)

* Wed Jan 20 2010 Paul Lindner <lindner@inuus.com> - 0:1.4.4-2
- Remove SELinux policies fixes Bugzilla 557073

* Sat Nov 28 2009 Remi Collet <rpms@famillecollet.com> - 1.4.4-1
- rebuild for remi repository

* Sat Nov 28 2009 Paul Lindner <lindner@inuus.com> - 0:1.4.4-1
- Upgraded to upstream memcached-1.4.4 (http://code.google.com/p/memcached/wiki/ReleaseNotes144)
- Add explicit Epoch to fix issue with broken devel dependencies (resolves 542001)

* Sat Nov 28 2009 Remi Collet <rpms@famillecollet.com> - 1.4.3-1
- rebuild for remi repository

* Thu Nov 12 2009 Paul Lindner <lindner@mirth.inuus.com> - 1.4.3-1
- Add explicit require on memcached for memcached-devel (resolves 537046)
- enable-threads option no longer needed
- Update web site address

* Wed Nov 11 2009 Paul Lindner <lindner@inuus.com> - 1.4.3-1
- Upgrade to memcached-1.4.3

* Mon Oct 12 2009 Paul Lindner <lindner@inuus.com> - 1.4.2-1
- Upgrade to memcached-1.4.2
- Addresses CVE-2009-2415

* Sun Sep 06 2009 Remi Collet <rpms@famillecollet.com> - 1.4.1-1
- rebuild for remi repository

* Sat Aug 29 2009 Paul Lindner <lindner@inuus.com> - 1.4.1-1
- Upgrade to 1.4.1 
- http://code.google.com/p/memcached/wiki/ReleaseNotes141

* Thu Jul 16 2009 Remi Collet <rpms@famillecollet.com> - 1.2.8-1.el4.remi.1
- fix init script syntax for EL4

* Wed Apr 29 2009 Paul Lindner <lindner@inuus.com> - 1.2.8-1
- Upgrade to memcached-1.2.8
- Addresses CVE-2009-1255

* Sun Apr 26 2009 Remi Collet <rpms@famillecollet.com> - 1.2.8-1
- Upgrade to memcached-1.2.8
- add conditional Selinux build (for EL4)

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jul 29 2008 Paul Lindner <lindner@inuus.com> - 1.2.6-1
- Upgrade to memcached-1.2.6

* Tue Mar  4 2008 Paul Lindner <lindner@inuus.com> - 1.2.5-1
- Upgrade to memcached-1.2.5

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.2.4-4
- Autorebuild for GCC 4.3

* Sun Jan 27 2008 Paul Lindner <lindner@inuus.com> - 1.2.4-3
- Adjust libevent dependencies

* Sat Dec 22 2007 Paul Lindner <lindner@inuus.com> - 1.2.4-2
- Upgrade to memcached-1.2.4

* Fri Sep 07 2007 Konstantin Ryabitsev <icon@fedoraproject.org> - 1.2.3-8
- Add selinux policies
- Create our own system user

* Mon Aug  6 2007 Paul Lindner <lindner@inuus.com> - 1.2.3-7
- Fix problem with -P and -d flag combo on x86_64
- Fix init script for FC-6

* Fri Jul 13 2007 Paul Lindner <lindner@inuus.com> - 1.2.3-4
- Remove test that fails in fedora build system on ppc64

* Sat Jul  7 2007 root <lindner@inuus.com> - 1.2.3-2
- Upgrade to 1.2.3 upstream
- Adjust make install to preserve man page timestamp
- Conform with LSB init scripts standards, add force-reload

* Wed Jul  4 2007 Paul Lindner <lindner@inuus.com> - 1.2.2-5
- Use /var/run/memcached/ directory to hold PID file

* Sat May 12 2007 Paul Lindner <lindner@inuus.com> - 1.2.2-4
- Remove tabs from spec file, rpmlint reports no more errors

* Thu May 10 2007 Paul Lindner <lindner@inuus.com> - 1.2.2-3
- Enable build-time regression tests
- add dependency on initscripts
- remove memcached-debug (not needed in dist)
- above suggestions from Bernard Johnson

* Mon May  7 2007 Paul Lindner <lindner@inuus.com> - 1.2.2-2
- Tidyness improvements suggested by Ruben Kerkhof in bugzilla #238994

* Fri May  4 2007 Paul Lindner <lindner@inuus.com> - 1.2.2-1
- Initial spec file created via rpmdev-newspec
