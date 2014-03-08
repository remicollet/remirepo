# Check for status of man pages
# http://code.google.com/p/redis/issues/detail?id=202

%global _hardened_build 1

%if 0%{?rhel} == 5
%ifarch i386
%global with_perftools 1
%endif
%else
%ifarch %{ix86} x86_64 ppc %{arm}
# available only on selected architectures
%global with_perftools 1
%endif
%endif

%if 0%{?fedora} >= 15 || 0%{?rhel} >= 7
%global with_systemd 1
%else
%global with_systemd 0
%endif

# Tests fail in mock, not in local build.
%global with_tests   %{?_with_tests:1}%{!?_with_tests:0}

Name:             redis
Version:          2.8.7
Release:          1%{?dist}
Summary:          A persistent key-value database

Group:            Applications/Databases
License:          BSD
URL:              http://redis.io
Source0:          http://download.redis.io/releases/%{name}-%{version}%{?prever:-%{prever}}.tar.gz
Source1:          %{name}.logrotate
Source2:          %{name}.init
Source3:          %{name}.service
Source4:          %{name}.tmpfiles
Source5:          sentinel.init
Source6:          sentinel.service
# Update configuration for Fedora
Patch0:           %{name}-2.8.4-conf.patch
Patch1:           %{name}-deps-PIC.patch
Patch2:           %{name}-deps-unbundle-jemalloc.patch

BuildRoot:        %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
%if !0%{?el5}
BuildRequires:    tcl >= 8.5
%endif
%if 0%{?with_perftools}
%if 0%{?fedora} >= 15 || 0%{?rhel} >=6
BuildRequires:    gperftools-devel
%else
BuildRequires:    google-perftools-devel
%endif
%endif
BuildRequires:    jemalloc-devel

Requires:         logrotate
Requires(pre):    shadow-utils
%if %{with_systemd}
BuildRequires:    systemd-units
Requires(post):   systemd-units
Requires(preun):  systemd-units
Requires(postun): systemd-units
%else
Requires(post):   chkconfig
Requires(preun):  chkconfig
Requires(preun):  initscripts
Requires(postun): initscripts
%endif


%description
Redis is an advanced key-value store. It is similar to memcached but the data
set is not volatile, and values can be strings, exactly like in memcached, but
also lists, sets, and ordered sets. All this data types can be manipulated with
atomic operations to push/pop elements, add/remove elements, perform server side
union, intersection, difference between sets, and so forth. Redis supports
different kind of sorting abilities.

%prep
%setup -q -n %{name}-%{version}%{?prever:-%{prever}}
%patch0 -p1 -b .rpmconf
%patch1 -p1 -b .pic
%patch2 -p1 -b .jem

%if 0%{?rhel} == 5
%ifarch i386
# Fix undefined reference to __sync_add_and_fetch_4
sed -e '/HAVE_ATOMIC/d' -i ./src/config.h
%endif
%endif

%build
rm -rvf deps/jemalloc

export CFLAGS="$RPM_OPT_FLAGS"
make %{?_smp_mflags} V=1 \
  DEBUG="" \
  LDFLAGS="%{?__global_ldflags}" \
  CFLAGS="$RPM_OPT_FLAGS -fPIC" \
  LUA_CFLAGS="-fPIC" \
%if 0%{?with_perftools}
  MALLOC=tcmalloc \
%else
  MALLOC=jemalloc \
%endif
  all

%check
%if %{with_tests}
make test
%else
: Test disabled, missing '--with tests' option.
%endif

%install
make install PREFIX=%{buildroot}%{_prefix}
# Install misc other
install -p -D -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}
install -p -D -m 644 %{name}.conf  %{buildroot}%{_sysconfdir}/%{name}.conf
install -p -D -m 644 sentinel.conf %{buildroot}%{_sysconfdir}/%{name}-sentinel.conf
install -d -m 755 %{buildroot}%{_localstatedir}/lib/%{name}
install -d -m 755 %{buildroot}%{_localstatedir}/log/%{name}
install -d -m 755 %{buildroot}%{_localstatedir}/run/%{name}

%if %{with_systemd}
# Install systemd unit
install -p -D -m 644 %{SOURCE3} %{buildroot}%{_unitdir}/%{name}.service
install -p -D -m 644 %{SOURCE6} %{buildroot}%{_unitdir}/%{name}-sentinel.service
# Install systemd tmpfiles config, _tmpfilesdir only defined in fedora >= 18
install -p -D -m 644 %{SOURCE4} %{buildroot}%{_prefix}/lib/tmpfiles.d/%{name}.conf
%else
sed -e '/^daemonize/s/no/yes/' \
    -i %{buildroot}%{_sysconfdir}/%{name}.conf
install -p -D -m 755 %{SOURCE2} %{buildroot}%{_initrddir}/%{name}
install -p -D -m 755 %{SOURCE5} %{buildroot}%{_initrddir}/%{name}-sentinel
%endif

# Fix non-standard-executable-perm error
chmod 755 %{buildroot}%{_bindir}/%{name}-*

# Ensure redis-server location doesn't change
mkdir -p %{buildroot}%{_sbindir}
mv %{buildroot}%{_bindir}/%{name}-server %{buildroot}%{_sbindir}/%{name}-server

# create redis-sentinel command as described on
# http://redis.io/topics/sentinel
ln -s %{name}-server %{buildroot}%{_sbindir}/%{name}-sentinel


%post
%if 0%{?systemd_post:1}
%systemd_post redis.service
%systemd_post redis-sentinel.service
%endif
# Initial installation (always, for new service)
%if %{with_systemd}
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
%else
/sbin/chkconfig --add redis
/sbin/chkconfig --add redis-sentinel
%endif

%pre
getent group  redis &> /dev/null || \
groupadd -r redis &> /dev/null
getent passwd redis &> /dev/null || \
useradd -r -g redis -d %{_sharedstatedir}/redis -s /sbin/nologin \
        -c 'Redis Server' redis &> /dev/null
exit 0

%preun
%if 0%{?systemd_preun:1}
%systemd_preun redis.service
%systemd_preun redis-sentinel.service
%else
if [ $1 = 0 ]; then
  # Package removal, not upgrade
%if %{with_systemd}
  /bin/systemctl --no-reload disable redis-sentinel.service >/dev/null 2>&1 || :
  /bin/systemctl stop redis-sentinel.service >/dev/null 2>&1 || :

  /bin/systemctl --no-reload disable redis.service          >/dev/null 2>&1 || :
  /bin/systemctl stop redis.service          >/dev/null 2>&1 || :
%else
  /sbin/service redis-sentinel stop &> /dev/null
  /sbin/chkconfig --del redis-sentinel &> /dev/null

  /sbin/service redis stop &> /dev/null
  /sbin/chkconfig --del redis &> /dev/null
%endif
fi
%endif

%if 0%{?systemd_postun_with_restart:1}
%systemd_postun_with_restart redis.service
%systemd_postun_with_restart redis-sentinel.service
%else
%if %{with_systemd}
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
if [ $1 -ge 1 ]; then
  # Package upgrade, not uninstall
  /bin/systemctl try-restart redis.service          >/dev/null 2>&1 || :
  /bin/systemctl try-restart redis-sentinel.service >/dev/null 2>&1 || :
fi
%else
if [ $1 -ge 1 ]; then
  /sbin/service redis          condrestart >/dev/null 2>&1 || :
  /sbin/service redis-sentinel condrestart >/dev/null 2>&1 || :
fi
%endif
%endif


%files
%defattr(-,root,root,-)
%doc 00-RELEASENOTES BUGS CONTRIBUTING COPYING README
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%attr(0644, redis, root) %config(noreplace) %{_sysconfdir}/%{name}.conf
%attr(0644, redis, root) %config(noreplace) %{_sysconfdir}/%{name}-sentinel.conf
%dir %attr(0755, redis, root) %{_localstatedir}/lib/%{name}
%dir %attr(0755, redis, root) %{_localstatedir}/log/%{name}
%dir %attr(0755, redis, root) %{_localstatedir}/run/%{name}
%{_bindir}/%{name}-*
%{_sbindir}/%{name}-*
%if %{with_systemd}
%{_prefix}/lib/tmpfiles.d/%{name}.conf
%{_unitdir}/%{name}.service
%{_unitdir}/%{name}-sentinel.service
%else
%{_initrddir}/%{name}
%{_initrddir}/%{name}-sentinel
%endif


%changelog
* Sat Mar  8 2014 Remi Collet <remi@fedoraproject.org> - 2.8.7-1
- Redis 2.8.7 - Release date: 5 Mar 2014
  upgrade urgency: LOW for Redis, LOW for Sentinel.

* Fri Feb 14 2014 Remi Collet <remi@fedoraproject.org> - 2.8.6-1
- Redis 2.8.6 - Release date: 13 Feb 2014
  upgrade urgency: HIGH for Redis, LOW for Sentinel.

* Thu Jan 16 2014 Remi Collet <remi@fedoraproject.org> - 2.8.4-1
- Redis 2.8.4 - Release date: 13 Jan 2014
  upgrade urgency: MODERATE for Redis and Sentinel.

* Mon Jan  6 2014 Remi Collet <remi@fedoraproject.org> - 2.8.3-2
- add redis-sentinel command (link to redis-server)
- don't rely on config for daemonize and pidfile
- add redis-sentinel service

* Sat Dec 14 2013 Remi Collet <remi@fedoraproject.org> - 2.8.3-1
- Redis 2.8.3
  upgrade urgency: MODERATE for Redis, HIGH for Sentinel.
- redis own /etc/redis.conf (needed CONFIG WRITE)
- add sentinel.conf as documentation

* Mon Dec  2 2013 Remi Collet <remi@fedoraproject.org> - 2.8.2-1
- Redis 2.8.2, new major version
- pull rawhide changes (add tmpfiles)

* Sun Sep  8 2013 Remi Collet <remi@fedoraproject.org> - 2.6.16-1
- Redis 2.6.16
  upgrade urgency: MODERATE

* Fri Sep 06 2013 Fabian Deutsch <fabian.deutsch@gmx.de> - 2.6.16-1
- Update to 2.6.16
- Fix rhbz#973151
- Fix rhbz#656683
- Fix rhbz#977357 (Jan Vcelak <jvcelak@fedoraproject.org>)

* Sat Aug 24 2013 Remi Collet <remi@fedoraproject.org> - 2.6.15-1
- Redis 2.6.15
  upgrade urgency: MODERATE, upgrade ASAP only if you experience
  issues related to the expired keys collection algorithm,
  or if you use the ZUNIONSTORE command.

* Sun Jul 28 2013 Remi Collet <remi@fedoraproject.org> - 2.6.14-1
- Redis 2.6.14
  upgrade urgency: HIGH because of the following two issues:
    Lua scripting + Replication + AOF in slaves problem
    AOF + expires possible race condition
- add option to run tests during build (not in mock)

* Tue Jul 23 2013 Peter Robinson <pbrobinson@fedoraproject.org> 2.6.13-4
- ARM has gperftools

* Wed Jun 19 2013 Fabian Deutsch <fabiand@fedoraproject.org> - 2.6.13-3
- Modify jemalloc patch for s390 compatibility (Thanks sharkcz)

* Fri Jun 07 2013 Fabian Deutsch <fabiand@fedoraproject.org> - 2.6.13-2
- Unbundle jemalloc

* Fri Jun 07 2013 Fabian Deutsch <fabiand@fedoraproject.org> - 2.6.13-1
- Add compile PIE flag (rhbz#955459)
- Update to redis 2.6.13 (rhbz#820919)

* Tue Apr 30 2013 Remi Collet <remi@fedoraproject.org> - 2.6.13-1
- Redis 2.6.13
  upgrade urgency: MODERATE, nothing very critical

* Sat Mar 30 2013 Remi Collet <remi@fedoraproject.org> - 2.6.12-1
- Redis 2.6.12
  upgrade urgency: MODERATE, nothing very critical
  but a few non trivial bugs

* Tue Mar 12 2013 Remi Collet <remi@fedoraproject.org> - 2.6.11-1
- Redis 2.6.11
  upgrade urgency: LOW, however updating is encouraged
  if you have many instances per server and you want
  to lower the CPU / energy usage.

* Mon Feb 11 2013 Remi Collet <remi@fedoraproject.org> - 2.6.10-1
- Redis 2.6.10
  upgrade urgency: MODERATE, this release contains many non
  critical fixes and many small improvements.

* Thu Jan 17 2013 Remi Collet <remi@fedoraproject.org> - 2.6.9-1
- Redis 2.6.9
  upgrade urgency: MODERATE if you use replication.

* Fri Jan 11 2013 Remi Collet <remi@fedoraproject.org> - 2.6.8-1
- Redis 2.6.8
  upgrade urgency: MODERATE if you use Lua scripting. Otherwise LOW.

* Tue Dec  4 2012 Remi Collet <remi@fedoraproject.org> - 2.6.7-1
- Redis 2.6.7
  upgrade urgency: MODERATE (unless you BLPOP using the same
  key multiple times).

* Fri Nov 23 2012 Remi Collet <remi@fedoraproject.org> - 2.6.5-1
- Redis 2.6.5 (upgrade urgency: moderate)

* Fri Nov 16 2012 Remi Collet <remi@fedoraproject.org> - 2.6.4-1
- Redis 2.6.4 (upgrade urgency: low)

* Sun Oct 28 2012 Remi Collet <remi@fedoraproject.org> - 2.6.2-1
- Redis 2.6.2 (upgrade urgency: low)
- fix typo in systemd macro

* Wed Oct 24 2012 Remi Collet <remi@fedoraproject.org> - 2.6.0-1
- Redis 2.6.0 is the latest stable version
- add patch for old glibc on RHEL-5

* Sat Oct 20 2012 Remi Collet <remi@fedoraproject.org> - 2.6.0-0.2.rc8
- Update to redis 2.6.0-rc8
- improve systemd integration

* Thu Aug 30 2012 Remi Collet <remi@fedoraproject.org> - 2.6.0-0.1.rc6
- Update to redis 2.6.0-rc6

* Thu Aug 30 2012 Remi Collet <remi@fedoraproject.org> - 2.4.16-1
- Update to redis 2.4.16

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.15-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Jul 08 2012 Silas Sewell <silas@sewell.org> - 2.4.15-2
- Remove TODO from docs

* Sun Jul 08 2012 Silas Sewell <silas@sewell.org> - 2.4.15-1
- Update to redis 2.4.15

* Sat May 19 2012 Silas Sewell <silas@sewell.org> - 2.4.13-1
- Update to redis 2.4.13

* Sat Mar 31 2012 Silas Sewell <silas@sewell.org> - 2.4.10-1
- Update to redis 2.4.10

* Fri Feb 24 2012 Silas Sewell <silas@sewell.org> - 2.4.8-1
- Update to redis 2.4.8

* Sat Feb 04 2012 Silas Sewell <silas@sewell.org> - 2.4.7-1
- Update to redis 2.4.7

* Wed Feb 01 2012 Fabian Deutsch <fabiand@fedoraproject.org> - 2.4.6-4
- Fixed a typo in the spec

* Tue Jan 31 2012 Fabian Deutsch <fabiand@fedoraproject.org> - 2.4.6-3
- Fix .service file, to match config (Type=simple).

* Tue Jan 31 2012 Fabian Deutsch <fabiand@fedoraproject.org> - 2.4.6-2
- Fix .service file, credits go to Timon.

* Thu Jan 12 2012 Fabian Deutsch <fabiand@fedoraproject.org> - 2.4.6-1
- Update to 2.4.6
- systemd unit file added
- Compiler flags changed to compile 2.4.6
- Remove doc/ and Changelog

* Sun Jul 24 2011 Silas Sewell <silas@sewell.org> - 2.2.12-1
- Update to redis 2.2.12

* Fri May 06 2011 Dan Horák <dan[at]danny.cz> - 2.2.5-2
- google-perftools exists only on selected architectures

* Sat Apr 23 2011 Silas Sewell <silas@sewell.ch> - 2.2.5-1
- Update to redis 2.2.5

* Sat Mar 26 2011 Silas Sewell <silas@sewell.ch> - 2.2.2-1
- Update to redis 2.2.2

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Dec 19 2010 Silas Sewell <silas@sewell.ch> - 2.0.4-1
- Update to redis 2.0.4

* Tue Oct 19 2010 Silas Sewell <silas@sewell.ch> - 2.0.3-1
- Update to redis 2.0.3

* Fri Oct 08 2010 Silas Sewell <silas@sewell.ch> - 2.0.2-1
- Update to redis 2.0.2
- Disable checks section for el5

* Sat Sep 11 2010 Silas Sewell <silas@sewell.ch> - 2.0.1-1
- Update to redis 2.0.1

* Sat Sep 04 2010 Silas Sewell <silas@sewell.ch> - 2.0.0-1
- Update to redis 2.0.0

* Thu Sep 02 2010 Silas Sewell <silas@sewell.ch> - 1.2.6-3
- Add Fedora build flags
- Send all scriplet output to /dev/null
- Remove debugging flags
- Add redis.conf check to init script

* Mon Aug 16 2010 Silas Sewell <silas@sewell.ch> - 1.2.6-2
- Don't compress man pages
- Use patch to fix redis.conf

* Tue Jul 06 2010 Silas Sewell <silas@sewell.ch> - 1.2.6-1
- Initial package
