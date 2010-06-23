#global postver b

%global tartype ce
%global cppconnver 1.1.0-0.1.bzr819

Summary: A MySQL visual database modeling tool
Name: mysql-workbench
Version: 5.2.24
Release: 1%{?dist}
Group: Applications/Databases
License: GPLv2

URL: http://wb.mysql.com
Source: %{name}-%{tartype}-%{version}%{?postver}.tar.gz

# don't build extension, use system one
# !!! This patch use versioned soname !!!
Patch1: %{name}-5.2.24-cppconn.patch
Patch2: %{name}-5.2.16-scintilla.patch
Patch3: %{name}-5.2.22-python.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: pcre-devel >= 3.9
BuildRequires: libglade2-devel >= 2.0.0
BuildRequires: lua-devel >= 5.1
%if %{fedora} >= 12
BuildRequires: ctemplate-devel
%endif
BuildRequires: libgnome-devel >= 2
BuildRequires: automake autoconf libtool
BuildRequires: lua-devel
BuildRequires: libzip-devel libxml2-devel
BuildRequires: libglade2-devel
BuildRequires: readline-devel
BuildRequires: python-devel >= 2.4
BuildRequires: gnome-keyring-devel
BuildRequires: boost-devel
BuildRequires: libsigc++20-devel
BuildRequires: curl-devel
BuildRequires: openssl-devel
BuildRequires: mysql-devel >= 5.1
%if %{fedora} >= 12
BuildRequires: libuuid-devel
%endif
BuildRequires: uuid-devel
BuildRequires: gtkmm24-devel
BuildRequires: mesa-libGL-devel
BuildRequires: sqlite-devel


BuildRequires: mysql-connector-c++-devel >= %{cppconnver}
BuildRequires:    desktop-file-utils
Requires(post):   desktop-file-utils
Requires(postun): desktop-file-utils

Requires: python-paramiko pexpect python-sqlite2
# requires mysql client pkg (for mysqldump and mysql cmdline client)
Requires: mysql gnome-keyring
Requires: mysql-connector-c++ >= %{cppconnver}
# Official upstream build
Conflicts: mysql-workbench-oss
Conflicts: mysql-workbench-ce


%description
MySQL Workbench provides DBAs and developers an integrated 
tools environment for:
* Database Design & Modeling
* SQL Development (replacing MySQL Query Browser)
* Database Administration (replacing MySQL Administrator)


%prep
%setup -q -n %{name}-%{tartype}-%{version}%{?postver}

%patch1 -p1 -b .cppconn
#patch2 -p1 -b .scintilla
%patch3 -p1 -b .fixindent

# we use System provided libraries
rm -rf ext/boost
rm -rf ext/curl
rm -rf ext/libsigc++
rm -rf ext/yassl
rm -rf ext/cppconn
#rm -rf ext/scintilla



%build
NOCONFIGURE=yes ./autogen.sh
%configure \
%if %{fedora} >= 12
    --with-system-ctemplate \
%endif
    --disable-debug

make %{?_smp_mflags}


%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

# clean dev files
echo Cleanup dev file
find %{buildroot}%{_libdir}/mysql-workbench -name \*.a  -exec rm {} \; -print
find %{buildroot}%{_libdir}/mysql-workbench -name \*.la -exec rm {} \; -print
#find %{buildroot}%{_libdir}/mysql-workbench -type f -name \*.so.\* -exec chmod +x {} \;

desktop-file-install --vendor="" \
   --dir=%{buildroot}%{_datadir}/applications/ \
         MySQLWorkbench.desktop


%clean
rm -rf %{buildroot}


%post
update-desktop-database &> /dev/null || :


%postun
update-desktop-database &> /dev/null || :


%files
%defattr(-, root, root, -)
%doc COPYING samples ChangeLog
%attr(0755,root,root) %{_bindir}/mysql-workbench
%attr(0755,root,root) %{_bindir}/mysql-workbench-bin
##%attr(0755,root,root) %{_bindir}/grtshell
%dir %{_libdir}/mysql-workbench
%{_libdir}/mysql-workbench/*
%{_datadir}/applications/*.desktop
%dir %{_datadir}/mysql-workbench
%{_datadir}/mysql-workbench/*


%changelog
* Wed Jun 23 2010 Remi Collet <RPMS@famillecollet.com> 5.2.24-1
- update to 5.2.24 RC3 Community Edition (CE)

* Fri Jun 04 2010 Remi Collet <RPMS@famillecollet.com> 5.2.22-1
- update to 5.2.22 RC Community (OSS) Edition
- build against mysql-connector-c++ 1.1.0 (bzr819)

* Wed May 12 2010 Remi Collet <RPMS@famillecollet.com> 5.2.21-1
- update to 5.2.21 RC Community (OSS) Edition

* Wed Apr 28 2010 Remi Collet <RPMS@famillecollet.com> 5.2.20-1.###.remi
- update to 5.2.20 beta 10 Community (OSS) Edition

* Sat Apr 17 2010 Remi Collet <RPMS@famillecollet.com> 5.2.19-1.###.remi
- update to 5.2.19 beta 9 Community (OSS) Edition

* Thu Apr 15 2010 Remi Collet <RPMS@famillecollet.com> 5.2.18-1.###.remi
- update to 5.2.18 beta 8 Community (OSS) Edition

* Sat Apr 03 2010 Remi Collet <RPMS@famillecollet.com> 5.2.17-1.###.remi
- update to 5.2.17 beta Community (OSS) Edition
- build against mysql-connector-c++ 1.1.0 (bzr818)

* Wed Feb 17 2010 Remi Collet <RPMS@famillecollet.com> 5.2.16-1.###.remi
- update to 5.2.16 beta Community (OSS) Edition

* Thu Feb 04 2010 Remi Collet <RPMS@famillecollet.com> 5.2.15-2.###.remi
- update to 5.2.15b beta Community (OSS) Edition

* Sat Jan 30 2010 Remi Collet <RPMS@famillecollet.com> 5.2.15-1.###.remi
- update to 5.2.15 beta Community (OSS) Edition

* Fri Jan 22 2010 Remi Collet <RPMS@famillecollet.com> 5.2.14-1.###.remi
- update to 5.2.14 beta Community (OSS) Edition

* Sun Jan 10 2010 Remi Collet <RPMS@famillecollet.com> 5.2.11-1.###.remi
- update to 5.2.11 beta Community (OSS) Edition

* Sat Sep 05 2009 Remi Collet <RPMS@famillecollet.com> 5.1.18-1.###.remi
- update to 5.1.18 GA Community (OSS) Edition

* Sun Aug 16 2009 Remi Collet <RPMS@famillecollet.com> 5.1.17-1.###.remi
- update to 5.1.17 GA Community (OSS) Edition

* Wed Jul 01 2009 Remi Collet <RPMS@famillecollet.com> 5.1.16-1.###.remi
- update to 5.1.16 GA Community (OSS) Edition

* Sun Jun 28 2009 Remi Collet <RPMS@famillecollet.com> 5.1.15-3.###.remi
- switch to system mysql-connector-c++ librairy

* Sat Jun 27 2009 Remi Collet <RPMS@famillecollet.com> 5.1.15-2.###.remi
- switch to system librairies (boost, libsigc++, curl, openssl)

* Sat Jun 27 2009 Remi Collet <RPMS@famillecollet.com> 5.1.15-1.###.remi
- update to 5.1.15 RC3 Community (OSS) Edition

* Fri Jun 19 2009 Remi Collet <RPMS@famillecollet.com> 5.1.14-1.###.remi
- update to 5.1.14 RC2 Community (OSS) Edition

* Fri Jun 12 2009 Remi Collet <RPMS@famillecollet.com> 5.1.13-1.###.remi
- update to 5.1.13 RC1 Community (OSS) Edition

* Fri May 01 2009 Remi Collet <RPMS@famillecollet.com> 5.1.12-2.fc11.remi
- F11 build
- add BR mesa-libGL-devel
- add gcc44 patch

* Tue Apr 28 2009 Remi Collet <RPMS@famillecollet.com> 5.1.12-1.###.remi
- update to 5.1.12 Beta Community (OSS) Edition
- add a patch for ppc build

* Fri Apr 10 2009 Remi Collet <RPMS@famillecollet.com> 5.1.10-1.###.remi
- update to 5.1.10 beta

* Sat Mar 21 2009 Remi Collet <RPMS@famillecollet.com> 5.1.9-1.###.remi
- update to 5.1.9 beta

* Sun Jan 13 2009 Remi Collet <RPMS@famillecollet.com> 5.1.7-1.###.remi
- update to 5.1.7 alpha

* Sat Dec 13 2008 Remi Collet <RPMS@famillecollet.com> 5.1.5-1.###.remi
- update to 5.1.5 alpha

* Wed Dec 03 2008 Remi Collet <RPMS@famillecollet.com> 5.1.4-1.fc10.remi.1
- remove dev files

* Tue Dec 02 2008 Remi Collet <RPMS@famillecollet.com> 5.1.4-1.fc10.remi
- F10 build

