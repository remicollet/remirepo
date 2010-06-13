%global selinux 0
%if 0%{?rhel} == 5
%global selinux 1
%endif
%if %{?fedora}%{!?fedora:99} < 13
%global selinux 1
%endif

%if %{selinux}
%define selinux_variants mls strict targeted 
%endif
%global modulename memcached

%global username   memcached
%global groupname  memcached

Name:           memcached
Version:        1.4.5
Release:        1%{?dist}
Epoch:		0
Summary:        High Performance, Distributed Memory Object Cache

Group:          System Environment/Daemons
License:        BSD
URL:            http://www.memcached.org/
Source0:        http://memcached.googlecode.com/files/%{name}-%{version}.tar.gz

# custom init script
Source1:        memcached.sysv
Source2:        memcached.sysvel4

# SELinux files
Source10:       %{modulename}.te
Source11:       %{modulename}.fc
Source12:       %{modulename}.if

# Fixes

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  libevent-devel
BuildRequires:  perl(Test::More)

Requires: initscripts
Requires: libevent
Requires(pre):  shadow-utils
Requires(post): /sbin/chkconfig
Requires(preun): /sbin/chkconfig, /sbin/service
Requires(postun): /sbin/service

%if %{selinux} == 0
# as of 3.5.5-4 selinux has memcache included
Obsoletes: memcached-selinux
%endif

%description
memcached is a high-performance, distributed memory object caching
system, generic in nature, but intended for use in speeding up dynamic
web applications by alleviating database load.


%if %{selinux}
%package selinux
Summary:        SELinux policy module supporting memcached
Group:          System Environment/Base
BuildRequires:  checkpolicy, selinux-policy-devel, hardlink
Requires:       %{name} = %{epoch}:%{version}-%{release}
Requires(post):  policycoreutils
Requires(postun): policycoreutils


%description selinux
SELinux policy module supporting memcached.
%endif

%package devel
Summary:	Files needed for development using memcached protocol
Group:		Development/Libraries 
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description devel
Install memcached-devel if you are developing C/C++ applications that require access to the
memcached binary include files.

%prep
%setup -q

%if %{selinux}
mkdir SELinux
cp -p %{SOURCE10} %{SOURCE11} %{SOURCE12} SELinux/
%endif

%build
%configure

make %{?_smp_mflags}

%if %{selinux}
pushd SELinux
for selinuxvariant in %{selinux_variants}; do
    make NAME=${selinuxvariant} -f /usr/share/selinux/devel/Makefile
    mv %{modulename}.pp %{modulename}.pp.${selinuxvariant}
    make NAME=${selinuxvariant} -f /usr/share/selinux/devel/Makefile clean
done
popd
%endif

%check
# remove failing test that doesn't work in
# build systems
rm -f t/daemonize.t 
make test

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot} INSTALL="%{__install} -p"                                         
# remove memcached-debug
rm -f %{buildroot}/%{_bindir}/memcached-debug

# Perl script for monitoring memcached
install -Dp -m0755 scripts/memcached-tool %{buildroot}%{_bindir}/memcached-tool

# Init script
%if 0%{?rhel} == 4
install -Dp -m0755 %{SOURCE2} %{buildroot}%{_initrddir}/memcached
%else
install -Dp -m0755 %{SOURCE1} %{buildroot}%{_initrddir}/memcached

# pid directory
mkdir -p %{buildroot}/%{_localstatedir}/run/memcached
%endif

# Default configs
mkdir -p %{buildroot}/%{_sysconfdir}/sysconfig
cat <<EOF >%{buildroot}/%{_sysconfdir}/sysconfig/%{name}
PORT="11211"
USER="%{username}"
MAXCONN="1024"
CACHESIZE="64"
OPTIONS=""
EOF

%if %{selinux}
# Install SELinux policy modules
pushd SELinux
for selinuxvariant in %{selinux_variants}; do
    install -d %{buildroot}%{_datadir}/selinux/${selinuxvariant}
    install -p -m 644 %{modulename}.pp.${selinuxvariant} \
        %{buildroot}%{_datadir}/selinux/${selinuxvariant}/%{modulename}.pp
done
popd

# Hardlink identical policy module packages together
/usr/sbin/hardlink -cv %{buildroot}%{_datadir}/selinux
%endif

%clean
rm -rf %{buildroot}


%pre
getent group %{groupname} >/dev/null || groupadd -r %{groupname}
getent passwd %{username} >/dev/null || \
useradd -r -g %{groupname} -d %{_localstatedir}/run/memcached \
    -s /sbin/nologin -c "Memcached daemon" %{username}
exit 0


%post
/sbin/chkconfig --add %{name}


%preun
if [ "$1" = 0 ] ; then
    /sbin/service %{name} stop > /dev/null 2>&1
    /sbin/chkconfig --del %{name}
fi
exit 0


%postun
if [ "$1" -ge 1 ]; then
    /sbin/service %{name} condrestart > /dev/null 2>&1
fi
exit 0


%if %{selinux}
%post selinux
# Install SELinux policy modules
for selinuxvariant in %{selinux_variants}
do
  /usr/sbin/semodule -s ${selinuxvariant} -i \
    %{_datadir}/selinux/${selinuxvariant}/%{modulename}.pp &> /dev/null || :
done
/usr/sbin/semanage port -a -t memcached_port_t -p tcp 11211 &> /dev/null || :
/sbin/fixfiles -R %{name} restore || :


%postun selinux
# Clean up after package removal
if [ $1 -eq 0 ]; then
  /usr/sbin/semanage port -d -t memcached_port_t -p tcp 11211 &> /dev/null || :
  # Remove SELinux policy modules
  for selinuxvariant in %{selinux_variants}
  do
    /usr/sbin/semodule -s ${selinuxvariant} -r %{modulename} &> /dev/null || :
  done
  /sbin/fixfiles -R %{name} restore || :
fi
%endif

%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING NEWS README doc/CONTRIBUTORS doc/*.txt
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}

%if %{?rhel}%{?fedora} > 4
%dir %attr(755,%{username},%{groupname}) %{_localstatedir}/run/memcached
%endif
%{_bindir}/memcached-tool
%{_bindir}/memcached
%{_mandir}/man1/memcached.1*
%{_initrddir}/memcached

%if %{selinux}
%files selinux
%defattr(-,root,root,0755)
%doc SELinux/*.te SELinux/*.fc SELinux/*.if
%{_datadir}/selinux/*/%{modulename}.pp
%endif

%files devel
%defattr(-,root,root,0755)
%{_includedir}/memcached/*

%changelog
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
