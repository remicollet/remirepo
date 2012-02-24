%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

%global mw_version 5.2.38
%global mw_release 1
%global tarversion gpl-%{mw_version}-src
%global srcversion gpl-%{mw_version}-src

# Use system cppconn if a compatible upstream version exists
#global cppconnver 1.1.0-0.3.bzr895

# "script_templates" (and some others) shouldn't be compiled
%global _python_bytecompile_errors_terminate_build 0

Summary:   A MySQL visual database modeling, administration and querying tool
Name:      mysql-workbench
Version:   %{mw_version}
Release:   %{mw_release}%{?dist}
Group:     Applications/Databases
License:   GPLv2 with exceptions

URL:       http://wb.mysql.com
# Upstream has a mirror redirector for downloads, so the URL is hard to
# represent statically.  You can get the tarball by following a link from
# http://dev.mysql.com/downloads/workbench/
Source:    http://gd.tuwien.ac.at/db/mysql/Downloads/MySQLGUITools/%{name}-%{tarversion}.tar.gz

# don't build extension, use system one
# !!! This patch use versioned soname (libmysqlcppconn.so.5) !!!
Patch1:    %{name}-5.2.28-cppconn.patch
Patch2:    %{name}-5.2.32-ctemplate.patch
Patch3:    %{name}-5.2.36-tinyxml.patch
# redirect man page to /usr/share
Patch5:    %{name}-5.2.34-man.patch
# http://bugs.mysql.com/63705 - Only <glib.h> can be included directly
Patch6:    %{name}-5.2.36-glib.patch
# http://bugs.mysql.com/63777 - service startup/shutdown command
Patch7:    %{name}-5.2.36-profiles.patch
# http://bugs.mysql.com/63898 - fix for automake >= 1.11.2
Patch8:    %{name}-5.2.37-automake.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: pcre-devel >= 3.9
BuildRequires: libglade2-devel >= 2.0.0
BuildRequires: lua-devel >= 5.1
%if 0%{?fedora} >= 12
BuildRequires: ctemplate-devel
%endif
BuildRequires: libgnome-devel >= 2
BuildRequires: automake autoconf libtool
BuildRequires: libzip-devel libxml2-devel
BuildRequires: readline-devel
BuildRequires: python-devel >= 2.4
%if 0%{?fedora} > 15
BuildRequires: libgnome-keyring-devel
%else
BuildRequires: gnome-keyring-devel
%endif
BuildRequires: boost-devel >= 1.37
BuildRequires: libsigc++20-devel
BuildRequires: curl-devel
BuildRequires: openssl-devel
BuildRequires: mysql-devel >= 5.1
%if 0%{?fedora} >= 12 || 0%{?rhel} >= 6
BuildRequires: libuuid-devel
%else
BuildRequires: uuid-devel
%endif
BuildRequires: gtkmm24-devel >= 2.18
BuildRequires: libGL-devel
BuildRequires: sqlite-devel
%if 0%{?cppconnver:1}
BuildRequires: mysql-connector-c++-devel >= %{cppconnver}
%endif
BuildRequires: desktop-file-utils
%if 0%{?fedora} >= 14 || 0%{?rhel} >= 6
BuildRequires: tinyxml-devel >= 2.6.0
%endif

Requires: python-paramiko pexpect
%if 0%{?fedora} < 17
Requires: python-sqlite2
%endif
Requires: mysql-utilities
# requires mysql client pkg (for mysqldump and mysql cmdline client)
Requires: mysql gnome-keyring
%if 0%{?cppconnver:1}
Requires: mysql-connector-c++ >= %{cppconnver}
%endif
# Official upstream builds (name changes quite often)
Conflicts: mysql-workbench-oss
Conflicts: mysql-workbench-ce
Conflicts: mysql-workbench-gpl
Conflicts: mysql-workbench-com-se
# Old GUI Tools no more maintained
Obsoletes: mysql-gui-tools < 5.1
Obsoletes: mysql-administrator < 5.1
Obsoletes: mysql-query-browser < 5.1
Provides:  mysql-gui-tools = %{version}
Provides:  mysql-administrator = %{version}
Provides:  mysql-query-browser = %{version}


%description
MySQL Workbench provides Database administrators and developers 
an integrated tools environment for:
* Database Design and Modeling
* SQL Development (replacing MySQL Query Browser)
* Database Administration (replacing MySQL Administrator)


%package -n mysql-utilities

Summary:        Scripts for managing and administering MySQL servers
# Not yet published (else will be package separatly)
# see ext/mysql-utilities/CHANGES.txt
Version:        1.0.3
Release:        0.%{mw_version}%{?dist}.%{mw_release}

BuildArch:      noarch
BuildRequires:  python-devel >= 2.4
%if 0%{?fedora} >= 14
BuildRequires:  python-sphinx >= 1.0
%endif

Requires:       mysql-connector-python

%description -n mysql-utilities
MySQL Utilities contain a collection of scripts useful for managing
and administering MySQL servers.


%prep
%setup -q -n %{name}-%{srcversion}

%if 0%{?cppconnver:1}
%patch1 -p1 -b .cppconn
rm -rf ext/cppconn
%endif

%if 0%{?fedora} >= 12
%patch2 -p1 -b .ctemplate
rm -rf ext/ctemplate
%endif

%if 0%{?fedora} >= 14 || 0%{?rhel} >= 6
%patch3 -p1 -b .tinyxml
rm -rf library/tinyxml
%endif

%patch5 -p1 -b .man
%patch6 -p1 -b .glib
%patch7 -p1 -b .profiles
%patch8 -p1 -b .automake


touch -r COPYING .timestamp4rpm
sed -i -e 's/\r//g' COPYING
touch -r .timestamp4rpm COPYING

# we use System provided libraries
rm -rf ext/boost
rm -rf ext/curl
rm -rf ext/libsigc++
rm -rf ext/yassl

# avoid "No such file" during configure
touch po/POTFILES.in


%build
#NOCONFIGURE=yes ./autogen.sh
export CXXFLAGS="$RPM_OPT_FLAGS -fpermissive"
%configure \
    --disable-debug \
%if 0%{?fedora} < 12 && 0%{?rhel} < 7
    --with-bundled-ctemplate \
%endif
    --enable-mysql-utilities

make %{?_smp_mflags}

%if 0%{?fedora} >= 14
pushd ext/mysql-utilities
%{__python} setup.py build_man
popd
%endif


%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

pushd ext/mysql-utilities
install --directory %{buildroot}%{_mandir}/man1
%{__python} setup.py install --skip-profile --root %{buildroot}
popd

# clean dev files
echo Cleanup dev file
find %{buildroot}%{_libdir}/%{name} -name \*.a  -exec rm {} \; -print
find %{buildroot}%{_libdir}/%{name} -name \*.la -exec rm {} \; -print

# fix perms
chmod +x %{buildroot}%{_datadir}/%{name}/sshtunnel.py

#desktop file
desktop-file-install --vendor="" \
   --dir=%{buildroot}%{_datadir}/applications/ \
         MySQLWorkbench.desktop


%clean
rm -rf %{buildroot}


%post
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
/usr/bin/update-desktop-database &> /dev/null || :
/usr/bin/update-mime-database %{_datadir}/mime &> /dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
    /usr/bin/update-desktop-database &> /dev/null || :
    /usr/bin/update-mime-database %{_datadir}/mime &> /dev/null || :
fi


%files
%defattr(-, root, root, -)
# NEWS and ChangeLog are empty or outdated
%doc AUTHORS COPYING COPYING.LGPL README samples
%{_bindir}/%{name}
%{_bindir}/%{name}-bin
%{_datadir}/applications/MySQLWorkbench.desktop
%{_datadir}/icons/hicolor/*/mimetypes/*%{name}*.png
%{_datadir}/icons/hicolor/*/apps/%{name}.png
%{_datadir}/mime-info/%{name}.mime
%{_datadir}/mime/packages/%{name}.xml
%{_libdir}/%{name}
%{_datadir}/%{name}
%exclude %{_datadir}/doc/%{name}


%files -n mysql-utilities
%defattr(-, root, root, -)
%doc ext/mysql-utilities/*.txt
%{_bindir}/mysqldbcompare
%{_bindir}/mysqldbcopy
%{_bindir}/mysqldbexport
%{_bindir}/mysqldbimport
%{_bindir}/mysqldiff
%{_bindir}/mysqldiskusage
%{_bindir}/mysqlindexcheck
%{_bindir}/mysqlmetagrep
%{_bindir}/mysqlprocgrep
%{_bindir}/mysqlreplicate
%{_bindir}/mysqlrplcheck
%{_bindir}/mysqlserverclone
%{_bindir}/mysqlserverinfo
%{_bindir}/mysqluserclone
%{python_sitelib}/mysql/utilities
%{python_sitelib}/mysql_utilities*
%if 0%{?fedora} >= 14
%{_mandir}/man1/*
%endif
# empty file already provided by mysql-connector-python
%exclude %{python_sitelib}/mysql/__init*


%changelog
* Fri Feb 24 2012 Remi Collet <remi@fedoraproject.org> 5.2.38-1
- update to 5.2.38 Community (OSS) Edition (GPL)
  http://dev.mysql.com/doc/workbench/en/wb-news-5-2-38.html

* Wed Feb  8 2012 Toshio Kuratomi <toshio@fedoraproject.org> - 5.2.37-4
- Remove the python-sqlite2 dep as mysql-workbench will work with sqlite3 from
  the stdlib

* Sat Feb 04 2012 Remi Collet <remi@fedoraproject.org> 5.2.37-3
- rebuild for new libzip
- add patch for automake > 1.11.2

* Tue Dec 27 2011 Remi Collet <remi@fedoraproject.org> 5.2.37-1.1
- Fix BR (lib)gnome-keyring-devel

* Tue Dec 27 2011 Remi Collet <remi@fedoraproject.org> 5.2.37-1
- update to 5.2.37 Community (OSS) Edition (GPL)
  http://dev.mysql.com/doc/workbench/en/wb-news-5-2-37.html

* Fri Dec 16 2011 Remi Collet <remi@fedoraproject.org> 5.2.36-3
- patch for server startup/shutdown command
  fixes bug #767391, upstream http://bugs.mysql.com/63777

* Sat Dec 10 2011 Remi Collet <remi@fedoraproject.org> 5.2.36-2
- patch for http://bugs.mysql.com/63705 (only include glib.h)

* Sat Dec 10 2011 Remi Collet <remi@fedoraproject.org> 5.2.36-1
- update to 5.2.36 Community (OSS) Edition (GPL)
  http://dev.mysql.com/doc/workbench/en/wb-news-5-2-36.html
- mysql-utilities 1.0.3

* Fri Sep 23 2011 Remi Collet <remi@fedoraproject.org> 5.2.35-1
- update to 5.2.35 Community (OSS) Edition (GPL)
  http://dev.mysql.com/doc/workbench/en/wb-news-5-2-35.html

* Wed Mar 23 2011 Remi Collet <Fedora@famillecollet.com> 5.2.34-1
- update to 5.2.34 Community (OSS) Edition (GPL)
  http://dev.mysql.com/doc/workbench/en/wb-news-5-2-34.html
  http://wb.mysql.com/?page_id=49
- mysql-utilities 1.0.1rc1

* Wed Mar 23 2011 Remi Collet <Fedora@famillecollet.com> 5.2.33b-1
- update to 5.2.33b Community (OSS) Edition (GPL)
  http://dev.mysql.com/doc/workbench/en/wb-news-5-2-33b.html
  http://wb.mysql.com/?page_id=49
- use bundled cppconn (which is a fork of svn version...)
- add mysql-utilities sub-package
- requires mysql-connector-python
- use system tinyxml >= 2.6.0 when available
- update bug for gcc 4.6
  http://bugs.mysql.com/60603
- rebuild for new MySQL client library

* Tue Mar 15 2011 Remi Collet <Fedora@FamilleCollet.com> 5.2.33-1
- rebuild for new mysql client ABI (.18)

* Fri Mar 11 2011 Remi Collet <Fedora@famillecollet.com> 5.2.33-1
- update to 5.2.33 Community (OSS) Edition (GPL)

* Wed Mar 09 2011 Remi Collet <Fedora@famillecollet.com> 5.2.32-1
- update to 5.2.32 Community (OSS) Edition (GPL)
  http://dev.mysql.com/doc/workbench/en/wb-news-5-2-32.html
- use bundled cppconn (which is a fork of svn version...)
- add mysql-utilities sub-package
- requires mysql-connector-python
- use system tinyxml >= 2.6.0 when available

* Mon Nov 22 2010 Remi Collet <Fedora@famillecollet.com> 5.2.30-1
- update to 5.2.30 Community (OSS) Edition (GPL)
  http://dev.mysql.com/doc/workbench/en/wb-news-5-2-30.html

* Tue Oct 12 2010 Remi Collet <Fedora@famillecollet.com> 5.2.29-1
- update to 5.2.29 Community (OSS) Edition (GPL)
  http://dev.mysql.com/doc/workbench/en/wb-news-5-2-29.html

* Mon Sep 27 2010 Remi Collet <Fedora@famillecollet.com> 5.2.28-3
- changes from review  (Liang Suilong <liangsuilong@gmail.com>)
- Edit the Source URL
- Replace mesa-libGL-devel by libGL-devel
- Remove Requires for desktop-file-utils
- Remove duplicate BR: libglade2-devel and lua-devel

* Fri Sep 24 2010 Remi Collet <Fedora@famillecollet.com> 5.2.28-2
- use system tinyxml

* Mon Sep 20 2010 Remi Collet <Fedora@famillecollet.com> 5.2.28-1
- update to 5.2.28 Community (OSS) Edition (GPL)
  http://dev.mysql.com/doc/workbench/en/wb-news-5-2-28.html
- build against mysql-connector-c++ 1.1.0 (bzr895)
- improve cppconn patch
- disable  _python_bytecompile_errors_terminate_build

* Sat Sep 18 2010 Remi Collet <Fedora@famillecollet.com> 5.2.27-2
- remove obsoleted configure options
- add patch to completely remove ctemplate from build process
- add patch to fix F-14 build

* Sat Aug 07 2010 Remi Collet <Fedora@famillecollet.com> 5.2.27-1
- update to 5.2.27 Community (OSS) Edition (GPL)
  http://dev.mysql.com/doc/workbench/en/wb-news-5-2-27.html
- clean spec for fedora review

* Sat Aug 07 2010 Remi Collet <RPMS@famillecollet.com> 5.2.26-1
- update to 5.2.26 Community Edition (GPL)
- build against mysql-connector-c++ 1.1.0 (bzr888)

* Thu Jul 01 2010 Remi Collet <RPMS@famillecollet.com> 5.2.25-1
- update to 5.2.25 Community Edition (GPL)

* Wed Jun 23 2010 Remi Collet <RPMS@famillecollet.com> 5.2.24-1
- update to 5.2.24 RC3 Community Edition (CE)

* Fri Jun 04 2010 Remi Collet <RPMS@famillecollet.com> 5.2.22-1
- update to 5.2.22 RC Community (OSS) Edition
- build against mysql-connector-c++ 1.1.0 (bzr819)

* Wed May 12 2010 Remi Collet <RPMS@famillecollet.com> 5.2.21-1
- update to 5.2.21 RC Community (OSS) Edition

* Wed Apr 28 2010 Remi Collet <RPMS@famillecollet.com> 5.2.20-1
- update to 5.2.20 beta 10 Community (OSS) Edition

* Sat Apr 17 2010 Remi Collet <RPMS@famillecollet.com> 5.2.19-1
- update to 5.2.19 beta 9 Community (OSS) Edition

* Thu Apr 15 2010 Remi Collet <RPMS@famillecollet.com> 5.2.18-1
- update to 5.2.18 beta 8 Community (OSS) Edition

* Sat Apr 03 2010 Remi Collet <RPMS@famillecollet.com> 5.2.17-1
- update to 5.2.17 beta Community (OSS) Edition
- build against mysql-connector-c++ 1.1.0 (bzr818)

* Wed Feb 17 2010 Remi Collet <RPMS@famillecollet.com> 5.2.16-1
- update to 5.2.16 beta Community (OSS) Edition

* Thu Feb 04 2010 Remi Collet <RPMS@famillecollet.com> 5.2.15-2
- update to 5.2.15b beta Community (OSS) Edition

* Sat Jan 30 2010 Remi Collet <RPMS@famillecollet.com> 5.2.15-1
- update to 5.2.15 beta Community (OSS) Edition

* Fri Jan 22 2010 Remi Collet <RPMS@famillecollet.com> 5.2.14-1
- update to 5.2.14 beta Community (OSS) Edition

* Sun Jan 10 2010 Remi Collet <RPMS@famillecollet.com> 5.2.11-1
- update to 5.2.11 beta Community (OSS) Edition

* Sat Sep 05 2009 Remi Collet <RPMS@famillecollet.com> 5.1.18-1
- update to 5.1.18 GA Community (OSS) Edition

* Sun Aug 16 2009 Remi Collet <RPMS@famillecollet.com> 5.1.17-1
- update to 5.1.17 GA Community (OSS) Edition

* Wed Jul 01 2009 Remi Collet <RPMS@famillecollet.com> 5.1.16-1
- update to 5.1.16 GA Community (OSS) Edition

* Sun Jun 28 2009 Remi Collet <RPMS@famillecollet.com> 5.1.15-3
- switch to system mysql-connector-c++ librairy

* Sat Jun 27 2009 Remi Collet <RPMS@famillecollet.com> 5.1.15-2
- switch to system librairies (boost, libsigc++, curl, openssl)

* Sat Jun 27 2009 Remi Collet <RPMS@famillecollet.com> 5.1.15-1
- update to 5.1.15 RC3 Community (OSS) Edition

* Fri Jun 19 2009 Remi Collet <RPMS@famillecollet.com> 5.1.14-1
- update to 5.1.14 RC2 Community (OSS) Edition

* Fri Jun 12 2009 Remi Collet <RPMS@famillecollet.com> 5.1.13-1
- update to 5.1.13 RC1 Community (OSS) Edition

* Fri May 01 2009 Remi Collet <RPMS@famillecollet.com> 5.1.12-2
- F11 build
- add BR mesa-libGL-devel
- add gcc44 patch

* Tue Apr 28 2009 Remi Collet <RPMS@famillecollet.com> 5.1.12-1
- update to 5.1.12 Beta Community (OSS) Edition
- add a patch for ppc build

* Fri Apr 10 2009 Remi Collet <RPMS@famillecollet.com> 5.1.10-1
- update to 5.1.10 beta

* Sat Mar 21 2009 Remi Collet <RPMS@famillecollet.com> 5.1.9-1
- update to 5.1.9 beta

* Sun Jan 13 2009 Remi Collet <RPMS@famillecollet.com> 5.1.7-1
- update to 5.1.7 alpha

* Sat Dec 13 2008 Remi Collet <RPMS@famillecollet.com> 5.1.5-1
- update to 5.1.5 alpha

* Wed Dec 03 2008 Remi Collet <RPMS@famillecollet.com> 5.1.4-1.1
- remove dev files

* Tue Dec 02 2008 Remi Collet <RPMS@famillecollet.com> 5.1.4-1
- F10 build

