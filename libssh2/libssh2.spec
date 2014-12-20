# Fedora 10 onwards support noarch subpackages; by using one, we can
# put the arch-independent docs in a common subpackage and save lots
# of space on the mirrors
%if 0%{?fedora} > 9 || 0%{?rhel} > 5
%global noarch_docs_package 1
%else
%global noarch_docs_package 0
%endif

# Define %%{__isa_bits} for old releases
%{!?__isa_bits: %global __isa_bits %((echo '#include <bits/wordsize.h>'; echo __WORDSIZE) | cpp - | grep -Ex '32|64')}

Name:           libssh2
Version:        1.4.3
Release:        8%{?dist}
Summary:        A library implementing the SSH2 protocol
Group:          System Environment/Libraries
License:        BSD
URL:            http://www.libssh2.org/
Source0:        http://libssh2.org/download/libssh2-%{version}.tar.gz
Patch0:         libssh2-1.4.2-utf8.patch
Patch1:         0001-sftp-seek-Don-t-flush-buffers-on-same-offset.patch
Patch2:         0002-sftp-statvfs-Along-error-path-reset-the-correct-stat.patch
Patch3:         0003-sftp-Add-support-for-fsync-OpenSSH-extension.patch
Patch4:         0004-partially-revert-window_size-explicit-adjustments-on.patch
Patch5:         0005-channel.c-fix-a-use-after-free.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(id -nu)
BuildRequires:  openssl-devel
BuildRequires:  zlib-devel
BuildRequires:  /usr/bin/man

# Test suite requirements - we run the OpenSSH server and try to connect to it
BuildRequires:  openssh-server
# We use matchpathcon to get the correct SELinux context for the ssh server
# initialization script so that it can transition correctly in an SELinux
# environment; matchpathcon is only available from FC-4 and moved from the
# libselinux to libselinux-utils package in F-10
%if (0%{?fedora} >= 4 || 0%{?rhel} >= 5) && !(0%{?fedora} >=17 || 0%{?rhel} >=7)
BuildRequires:  /usr/sbin/matchpathcon selinux-policy-targeted
%endif

%description
libssh2 is a library implementing the SSH2 protocol as defined by
Internet Drafts: SECSH-TRANS(22), SECSH-USERAUTH(25),
SECSH-CONNECTION(23), SECSH-ARCH(20), SECSH-FILEXFER(06)*,
SECSH-DHGEX(04), and SECSH-NUMBERS(10).

%package        devel
Summary:        Development files for libssh2
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       pkgconfig

%description    devel
The libssh2-devel package contains libraries and header files for
developing applications that use libssh2.

%package        docs
Summary:        Documentation for libssh2
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
%if %{noarch_docs_package}
BuildArch:      noarch
%endif

%description    docs
The libssh2-docs package contains man pages and examples for
developing applications that use libssh2.

%prep
%setup -q

# Replace hard wired port number in the test suite to avoid collisions
# between 32-bit and 64-bit builds running on a single build-host
sed -i s/4711/47%{?__isa_bits}/ tests/ssh2.{c,sh}

# Make sure things are UTF-8...
%patch0 -p1

# Three upstream patches required for qemu ssh block driver.
%patch1 -p1
%patch2 -p1
%patch3 -p1

# http://thread.gmane.org/gmane.network.ssh.libssh2.devel/6428
%patch4 -p1

# https://trac.libssh2.org/ticket/268
%patch5 -p1

# Make sshd transition appropriately if building in an SELinux environment
%if !(0%{?fedora} >= 17 || 0%{?rhel} >= 7)
chcon $(/usr/sbin/matchpathcon -n /etc/rc.d/init.d/sshd) tests/ssh2.sh || :
chcon -R $(/usr/sbin/matchpathcon -n /etc) tests/etc || :
chcon $(/usr/sbin/matchpathcon -n /etc/ssh/ssh_host_key) tests/etc/{host,user} || :
%endif

%build
%configure --disable-static --enable-shared
make %{?_smp_mflags}

# Avoid polluting libssh2.pc with linker options (#947813)
sed -i -e 's|[[:space:]]-Wl,[^[:space:]]*||' libssh2.pc

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot} INSTALL="install -p"
find %{buildroot} -name '*.la' -exec rm -f {} \;

# clean things up a bit for packaging
make -C example clean
rm -rf example/.deps
find example/ -type f '(' -name '*.am' -o -name '*.in' ')' -exec rm -v {} \;

# avoid multilib conflict on libssh2-devel
mv -v example example.%{_arch}

%check
# The SSH test will fail if we don't have /dev/tty, as is the case in some
# versions of mock (#672713)
if [ ! -c /dev/tty ]; then
	echo Skipping SSH test due to missing /dev/tty
	echo "exit 0" > tests/ssh2.sh
fi
# Apparently it fails in the sparc and arm buildsystems too
%ifarch %{sparc} %{arm}
echo Skipping SSH test on sparc/arm
echo "exit 0" > tests/ssh2.sh
%endif
make -C tests check

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING README NEWS
%{_libdir}/libssh2.so.1
%{_libdir}/libssh2.so.1.*

%files docs
%defattr(-,root,root,-)
%doc HACKING
%{_mandir}/man3/libssh2_*.3*

%files devel
%defattr(-,root,root,-)
%doc example.%{_arch}/
%{_includedir}/libssh2.h
%{_includedir}/libssh2_publickey.h
%{_includedir}/libssh2_sftp.h
%{_libdir}/libssh2.so
%{_libdir}/pkgconfig/libssh2.pc

%changelog
* Sat Dec 20 2014 Remi Collet <RPMS@FamilleCollet.com> 1.4.3-8
- sync with 1.4.3-8 from RHEL-7
- ABI is compatible according to ABI compliance checker
  http://upstream.rosalinux.ru/versions/libssh2.html

* Sun Jul 24 2011 Remi Collet <RPMS@FamilleCollet.com> 1.2.7-1
- rebuild for remi repo (EL-5)

* Tue Oct 12 2010 Kamil Dudka <kdudka@redhat.com> 1.2.7-1
- update to 1.2.7 (#632916)
- avoid multilib conflict on libssh2-docs
- avoid build failure in mock with SELinux in the enforcing mode (#558964)

* Fri Mar 12 2010 Chris Weyl <cweyl@alumni.drew.edu> 1.2.4-1
- update to 1.2.4
- drop old patch0
- be more aggressive about keeping .deps from intruding into -docs

* Wed Jan 20 2010 Chris Weyl <cweyl@alumni.drew.edu> 1.2.2-5
- pkgconfig dep should be with -devel, not -docs

* Mon Jan 18 2010 Chris Weyl <cweyl@alumni.drew.edu> 1.2.2-4
- enable tests; conditionalize sshd test, which fails with a funky SElinux
  error when run locally

* Mon Jan 18 2010 Chris Weyl <cweyl@alumni.drew.edu> 1.2.2-3
- patch w/1aba38cd7d2658146675ce1737e5090f879f306; not yet in a GA release

* Thu Jan 14 2010 Chris Weyl <cweyl@alumni.drew.edu> 1.2.2-2
- correct bad file entry under -devel

* Thu Jan 14 2010 Chris Weyl <cweyl@alumni.drew.edu> 1.2.2-1
- update to 1.2.2
- drop old patch now in upstream
- add new pkgconfig file to -devel

* Mon Sep 21 2009 Chris Weyl <cweyl@alumni.drew.edu> 1.2-2
- patch based on 683aa0f6b52fb1014873c961709102b5006372fc
- disable tests (*sigh*)

* Tue Aug 25 2009 Chris Weyl <cweyl@alumni.drew.edu> 1.2-1
- update to 1.2

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 1.0-4
- rebuilt with new openssl

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 16 2009 Chris Weyl <cweyl@alumni.drew.edu> 1.0-1
- update to 1.0

* Sat Jan 17 2009 Tomas Mraz <tmraz@redhat.com> - 0.18-8
- rebuild with new openssl

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.18-7
- Autorebuild for GCC 4.3

* Wed Dec 05 2007 Chris Weyl <cweyl@alumni.drew.edu> 0.18-6
- rebuild for new openssl...

* Tue Nov 27 2007 Chris Weyl <cweyl@alumni.drew.edu> 0.18-5
- bump

* Tue Nov 27 2007 Chris Weyl <cweyl@alumni.drew.edu> 0.18-4
- add INSTALL arg to make install vs env. var

* Mon Nov 26 2007 Chris Weyl <cweyl@alumni.drew.edu> 0.18-3
- run tests; don't package test

* Sun Nov 18 2007 Chris Weyl <cweyl@alumni.drew.edu> 0.18-2
- split docs into -docs (they seemed... large.)

* Tue Nov 13 2007 Chris Weyl <cweyl@alumni.drew.edu> 0.18-1
- update to 0.18

* Sun Oct 14 2007 Chris Weyl <cweyl@alumni.drew.edu> 0.17-1
- update to 0.17
- many spec file changes

* Wed May 23 2007 Sindre Pedersen Bjørdal <foolish[AT]guezz.net> - 0.15-0.2.20070506
- Fix release tag
- Move manpages to -devel package
- Add Examples dir to -devel package

* Sun May 06 2007 Sindre Pedersen Bjørdal <foolish[AT]guezz.net> - 0.15-0.20070506.1
- Initial build
