# remirepo spec file for redis, from:
#
# Fedora spec file for redis
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#
%global _hardened_build 1

# systemd >= 204 with additional service config
%if 0%{?fedora} >= 19 || 0%{?rhel} >= 7
%global with_systemd 1
%else
%global with_systemd 0
%endif

# Tests fail in mock, not in local build.
%global with_tests   %{?_with_tests:1}%{!?_with_tests:0}

# Pre-version are only available in github
#global prever       rc3
%global gh_commit    d5dab73127a3f02cf5c4964c66a6c7c7147b9dc0
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     antirez
%global gh_project   redis

Name:             redis
Version:          3.2.0
Release:          1%{?dist}
Summary:          A persistent key-value database

Group:            Applications/Databases
License:          BSD
URL:              http://redis.io
%if 0%{?prever:1}
Source0:          https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{name}-%{version}-%{gh_short}.tar.gz
%else
Source0:          http://download.redis.io/releases/%{name}-%{version}.tar.gz
%endif
Source1:          %{name}.logrotate
Source2:          %{name}.init
Source3:          %{name}.service
Source4:          %{name}.tmpfiles
Source5:          %{name}-sentinel.init
Source6:          %{name}-sentinel.service
Source7:          %{name}-shutdown
Source8:          %{name}-limit-systemd
Source9:          %{name}-limit-init

# Update configuration for Fedora
Patch0:           0001-redis-3.2-redis-conf.patch
Patch1:           0002-redis-3.2-deps-library-fPIC-performance-tuning.patch
Patch2:           0003-redis-2.8.11-use-system-jemalloc.patch

BuildRoot:        %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
%if !0%{?el5}
BuildRequires:    tcl >= 8.5
%endif
BuildRequires:    jemalloc-devel

# Required for redis-shutdown
Requires:         /bin/awk
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
Redis is an advanced key-value store. It is often referred to as a data
structure server since keys can contain strings, hashes, lists, sets and
sorted sets.

You can run atomic operations on these types, like appending to a string;
incrementing the value in a hash; pushing to a list; computing set
intersection, union and difference; or getting the member with highest
ranking in a sorted set.

In order to achieve its outstanding performance, Redis works with an
in-memory dataset. Depending on your use case, you can persist it either
by dumping the dataset to disk every once in a while, or by appending
each command to a log.

Redis also supports trivial-to-setup master-slave replication, with very
fast non-blocking first synchronization, auto-reconnection on net split
and so forth.

Other features include Transactions, Pub/Sub, Lua scripting, Keys with a
limited time-to-live, and configuration settings to make Redis behave like
a cache.

You can use Redis from most programming languages also.

Documentation: http://redis.io/documentation


%prep
%if 0%{?prever:1}
%setup -q -n %{gh_project}-%{gh_commit}
%else
%setup -q -n %{name}-%{version}
%endif

%patch0 -p1 -b .rpmconf
%patch1 -p1 -b .pic
%patch2 -p1 -b .jem


%build
rm -rvf deps/jemalloc

export CFLAGS="$RPM_OPT_FLAGS"
make %{?_smp_mflags} V=1 \
  DEBUG="" \
  LDFLAGS="%{?__global_ldflags}" \
  CFLAGS="$RPM_OPT_FLAGS -fPIC" \
  LUA_CFLAGS="-fPIC" \
  MALLOC=jemalloc \
  all

%check
%if %{with_tests}
make test
make test-sentinel
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
# this folder requires systemd >= 204
install -p -D -m 644 %{SOURCE8} %{buildroot}%{_sysconfdir}/systemd/system/%{name}.service.d/limit.conf
install -p -D -m 644 %{SOURCE8} %{buildroot}%{_sysconfdir}/systemd/system/%{name}-sentinel.service.d/limit.conf
%else
install -p -D -m 755 %{SOURCE2} %{buildroot}%{_initrddir}/%{name}
install -p -D -m 755 %{SOURCE5} %{buildroot}%{_initrddir}/%{name}-sentinel
install -p -D -m 644 %{SOURCE9} %{buildroot}%{_sysconfdir}/security/limits.d/95-%{name}.conf
%endif

# Fix non-standard-executable-perm error
chmod 755 %{buildroot}%{_bindir}/%{name}-*

# create redis-sentinel command as described on
# http://redis.io/topics/sentinel
ln -sf %{name}-server %{buildroot}%{_bindir}/%{name}-sentinel

# Install redis-shutdown
install -pDm755 %{SOURCE7} %{buildroot}%{_bindir}/%{name}-shutdown


%post
%if 0%{?systemd_post:1}
%systemd_post redis.service
%systemd_post redis-sentinel.service
%else
# Initial installation (always, for new service)
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
  /sbin/service redis-sentinel stop &> /dev/null
  /sbin/chkconfig --del redis-sentinel &> /dev/null

  /sbin/service redis stop &> /dev/null
  /sbin/chkconfig --del redis &> /dev/null
fi
%endif

%if 0%{?systemd_postun_with_restart:1}
%systemd_postun_with_restart redis.service
%systemd_postun_with_restart redis-sentinel.service
%else
if [ $1 -ge 1 ]; then
  /sbin/service redis          condrestart >/dev/null 2>&1 || :
  /sbin/service redis-sentinel condrestart >/dev/null 2>&1 || :
fi
%endif


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc 00-RELEASENOTES BUGS CONTRIBUTING MANIFESTO README.md
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%attr(0644, redis, root) %config(noreplace) %{_sysconfdir}/%{name}.conf
%attr(0644, redis, root) %config(noreplace) %{_sysconfdir}/%{name}-sentinel.conf
%dir %attr(0755, redis, redis) %{_localstatedir}/lib/%{name}
%dir %attr(0755, redis, redis) %{_localstatedir}/log/%{name}
%dir %attr(0755, redis, redis) %{_localstatedir}/run/%{name}
%{_bindir}/%{name}-*
%if %{with_systemd}
%{_prefix}/lib/tmpfiles.d/%{name}.conf
%{_unitdir}/%{name}.service
%{_unitdir}/%{name}-sentinel.service
%dir %{_sysconfdir}/systemd/system/%{name}.service.d
%config(noreplace) %{_sysconfdir}/systemd/system/%{name}.service.d/limit.conf
%dir %{_sysconfdir}/systemd/system/%{name}-sentinel.service.d
%config(noreplace) %{_sysconfdir}/systemd/system/%{name}-sentinel.service.d/limit.conf
%else
%{_initrddir}/%{name}
%{_initrddir}/%{name}-sentinel
%config(noreplace) %{_sysconfdir}/security/limits.d/95-%{name}.conf
%endif


%changelog
* Tue May 10 2016 Remi Collet <remi@fedoraproject.org> - 3.2.0-1
- update to 3.2.0

* Mon Feb  8 2016 Haïkel Guémar <hguemar@fedoraproject.org> - 3.2-0.4.rc3
- Fix redis-shutdown to handle password-protected instances shutdown

* Thu Jan 28 2016 Remi Collet <remi@fedoraproject.org> - 3.2-0.3.rc3
- update to 3.2-rc3 (version 3.1.103)

* Tue Jan 26 2016 Remi Collet <remi@fedoraproject.org> - 3.2-0.2.rc2
- update to 3.2-rc2 (version 3.1.102)

* Fri Jan 15 2016 Remi Collet <remi@fedoraproject.org> - 3.2-0.1.rc1
- update to 3.2-rc1 (version 3.1.101)
  This is the first release candidate of Redis 3.2

* Sat Dec 26 2015 Remi Collet <remi@fedoraproject.org> - 3.0.6-1
- Redis 3.0.6 - Release date: 18 Dec 2015
- Upgrade urgency: MODERATE

* Fri Oct 16 2015 Remi Collet <remi@fedoraproject.org> - 3.0.5-1
- Redis 3.0.5 - Release date: 15 Oct 2015
- Upgrade urgency: MODERATE

* Thu Sep 10 2015 Remi Collet <remi@fedoraproject.org> - 3.0.4-1
- Redis 3.0.4 - Release date: 8 Sep 2015
- Upgrade urgency: HIGH for Redis and Sentinel.

* Wed Aug  5 2015 Remi Collet <remi@fedoraproject.org> - 3.0.3-1.1
- make redis-shutdown more robust, see #22

* Fri Jul 17 2015 Remi Collet <remi@fedoraproject.org> - 3.0.3-1
- Redis 3.0.3 - Release date: 17 Jul 2015
- Upgrade urgency: LOW for Redis and Sentinel.

* Tue Jun  9 2015 Remi Collet <remi@fedoraproject.org> - 3.0.2-1
- Redis 3.0.2 - Release date: 4 Jun 2015
- Upgrade urgency: HIGH for Redis because of a security issue.
                   LOW for Sentinel.

* Wed May  6 2015 Remi Collet <remi@fedoraproject.org> - 3.0.1-1
- Redis 3.0.1 - Release date: 5 May 2015
- Upgrade urgency: LOW for Redis and Cluster, MODERATE for Sentinel.

* Tue Apr 14 2015 Remi Collet <remi@fedoraproject.org> - 3.0.0-2
- rebuild with new redis-shutdown from rawhide
- improved description from rawhide
- use redis/redis owner for directories under /var

* Mon Apr  6 2015 Remi Collet <remi@fedoraproject.org> - 3.0.0-1
- Redis 3.0.0 - Release date: 1 Apr 2015

* Thu Mar 26 2015 Haïkel Guémar <hguemar@fedoraproject.org> - 2.8.19-2
- Fix redis-shutdown on multiple NIC setup (RHBZ #1201237)

* Wed Dec 17 2014 Remi Collet <remi@fedoraproject.org> - 2.8.19-1
- Redis 2.8.19 - Release date: 16 Dec 2014
  upgrade urgency: LOW for both Redis and Sentinel.

* Sat Dec 13 2014 Remi Collet <remi@fedoraproject.org> - 2.8.18-2
- provides /etc/systemd/system/redis.service.d/limit.conf
  and /etc/systemd/system/redis-sentinel.service.d/limit.conf
  or /etc/security/limits.d/95-redis.conf

* Thu Dec  4 2014 Remi Collet <remi@fedoraproject.org> - 2.8.18-1.1
- EL-5 rebuild with upstream patch

* Thu Dec  4 2014 Remi Collet <remi@fedoraproject.org> - 2.8.18-1
- Redis 2.8.18 - Release date: 4 Dec 2014
  upgrade urgency: LOW for both Redis and Sentinel.
- fix isfinite missing on EL-5

* Sun Sep 21 2014 Remi Collet <remi@fedoraproject.org> - 2.8.17-2
- fix sentinel service unit file for systemd
- also use redis-shutdown in init scripts

* Sat Sep 20 2014 Remi Collet <remi@fedoraproject.org> - 2.8.17-1
- Redis 2.8.17 - Release date: 19 Sep 2014
  upgrade urgency: HIGH for Redis Sentinel, LOW for Redis Server.

* Wed Sep 17 2014 Remi Collet <remi@fedoraproject.org> - 2.8.16-1
- Redis 2.8.16 - Release date: 16 Sep 2014
  upgrade urgency: HIGH for Redis, LOW for Sentinel.

* Fri Sep 12 2014 Remi Collet <remi@fedoraproject.org> - 2.8.15-1
- Redis 2.8.15 - Release date: 12 Sep 2014
  upgrade urgency: LOW for Redis, HIGH for Sentinel.
- move commands from /usr/sbin to /usr/bin
- add redis-shutdown command (systemd)

* Thu Sep  4 2014 Remi Collet <remi@fedoraproject.org> - 2.8.14-1
- Redis 2.8.14 - Release date:  1 Sep 2014
  upgrade urgency: HIGH for Lua scripting users, otherwise LOW.

* Tue Jul 15 2014 Remi Collet <remi@fedoraproject.org> - 2.8.13-1
- Redis 2.8.13 - Release date: 14 Jul 2014
  upgrade urgency: LOW for Redis and Sentinel

* Tue Jun 24 2014 Remi Collet <remi@fedoraproject.org> - 2.8.12-1
- Redis 2.8.12 - Release date: 23 Jun 2014
  upgrade urgency: HIGH for Redis, CRITICAL for Sentinel.
- always use jemalloc (instead of tcmalloc)

* Mon Jun 16 2014 Remi Collet <remi@fedoraproject.org> - 2.8.11-1
- Redis 2.8.11 - Release date: 11 Jun 2014
  upgrade urgency: HIGH if you use Lua scripting, LOW otherwise.

* Fri Jun  6 2014 Remi Collet <remi@fedoraproject.org> - 2.8.10-1
- Redis 2.8.10 - Release date: 5 Jun 2014
  upgrade urgency: HIGH if you use min-slaves-to-write option.

* Tue Apr 22 2014 Remi Collet <remi@fedoraproject.org> - 2.8.9-1
- Redis 2.8.9 - Release date: 22 Apr 2014
  upgrade urgency: LOW, only new features introduced, no bugs fixed.

* Thu Mar 27 2014 Remi Collet <remi@fedoraproject.org> - 2.8.8-1
- Redis 2.8.8 - Release date: 25 Mar 2014
  upgrade urgency: HIGH for Redis, LOW for Sentinel.

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
