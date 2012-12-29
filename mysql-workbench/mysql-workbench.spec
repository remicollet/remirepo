%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

%global tarversion gpl-%{version}-src

# Use system cppconn if a compatible upstream version exists
%global cppconnver 1.1.1

# "script_templates" (and some others) shouldn't be compiled
%global _python_bytecompile_errors_terminate_build 0

Summary:   A MySQL visual database modeling, administration and querying tool
Name:      mysql-workbench
Version:   5.2.45
Release:   1%{?dist}
Group:     Applications/Databases
License:   GPLv2 with exceptions

URL:       http://wb.mysql.com

# The upstream tarball includes non-free documentation that we cannot ship.
# To remove the non-free documentation, run this script after downloading
# the tarball into the current directory:
# ./stripdocs.sh $VERSION
Source0:   %{name}-nodocs-%{version}.tar.xz
Source1:   stripdocs.sh

# don't build extension, use system one
# !!! This patch use versioned soname (libmysqlcppconn.so.6) !!!
Patch1:    %{name}-5.2.45-cppconn.patch
# Use system ctemplate
Patch2:    %{name}-5.2.43-ctemplate.patch
# Use system tinyxml
Patch3:    %{name}-5.2.41-tinyxml.patch
# Use system antlr (keep bundled vsqlite)
Patch4:    %{name}-5.2.43-antlr.patch
# Use system antlr (and vsqlite) - NOT applied
Patch5:    %{name}-5.2.44-antlr.patch
# Disable broken AutoCompletion feature
Patch6:    %{name}-5.2.45-noautocc.patch
# Use system vsqlite++ (not ready) - NOT applied
Patch7:    %{name}-5.2.44-vsqlite.patch

# don't use bundled documentation, redirect to online doc
Patch9:    %{name}-5.2.45-nodocs.patch

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
BuildRequires: libiodbc-devel
%if 0
BuildRequires: vsqlite++-devel
%endif
%if 0%{?fedora} >= 17
BuildRequires: antlr3-C-devel >= 3.4
%endif

Requires: python-paramiko pexpect
%if 0%{?fedora} < 17
Requires: python-sqlite2
%endif
Requires: mysql-utilities
# requires mysql client pkg (for mysqldump and mysql cmdline client)
Requires: mysql%{?_isa}
Requires: gnome-keyring%{?_isa}
# For migration wizard (2.1.18 prefered, but not yet available)
# see https://bugzilla.redhat.com/847440
Requires: pyodbc%{?_isa}
%if 0%{?cppconnver:1}
Requires: mysql-connector-c++%{?_isa} >= %{cppconnver}
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


%prep
%setup -q -n %{name}-%{tarversion}

%if 0%{?cppconnver:1}
%patch1 -p1 -b .cppconn
rm -rf ext/cppconn
%endif

%if 0%{?fedora} >= 12
%patch2 -p1 -b .ctemplate
rm -rf ext/ctemplate
%endif

%if 0
%patch7 -p1 -b .vsqlite
rm -rf ext/vsqlite++
%endif

%if 0%{?fedora} >= 14 || 0%{?rhel} >= 6
%patch3 -p1 -b .tinyxml
rm -rf library/tinyxml
%endif

%if 0%{?fedora} >= 17
%patch4 -p1 -b .antlr
rm -rf ext/antlr-runtime
%endif

%patch6 -p1 -b .noautocc
%patch9 -p1 -b .nodocs

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
NOCONFIGURE=yes ./autogen.sh
export CXXFLAGS="$RPM_OPT_FLAGS -fpermissive"
%configure \
    --disable-debug \
%if 0%{?fedora} < 12 && 0%{?rhel} < 7
    --with-bundled-ctemplate \
%endif
    --with-odbc-cflags="$(pkg-config --cflags libiodbc)" \
    --with-odbc-libs="$(pkg-config --libs libiodbc)" \
    --enable-mysql-utilities

make %{?_smp_mflags}


%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

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
%{_bindir}/wbcopytables
%{_datadir}/applications/MySQLWorkbench.desktop
%{_datadir}/icons/hicolor/*/mimetypes/*%{name}*.png
%{_datadir}/icons/hicolor/*/apps/%{name}.png
%{_datadir}/mime-info/%{name}.mime
%{_datadir}/mime/packages/%{name}.xml
%{_libexecdir}/mysql-workbench-bin
%{_libdir}/%{name}
%{_datadir}/%{name}
%exclude %{_datadir}/doc/%{name}


%changelog
* Sat Dec 29 2012 Remi Collet <remi@fedoraproject.org> 5.2.45-1
- update to 5.2.45 Community (OSS) Edition (GPL)
  http://dev.mysql.com/doc/relnotes/workbench/en/wb-news-5-2-45.html

* Sat Oct 20 2012 Remi Collet <remi@fedoraproject.org> 5.2.44-1
- update to 5.2.44 Community (OSS) Edition (GPL)
  http://dev.mysql.com/doc/workbench/en/wb-news-5-2-44.html
- keep bundled vsqlite++ for now

* Thu Sep 13 2012 Remi Collet <remi@fedoraproject.org> 5.2.43-1
- update to 5.2.43 Community (OSS) Edition (GPL)
  http://dev.mysql.com/doc/workbench/en/wb-news-5-2-43.html

* Tue Aug 28 2012 Remi Collet <remi@fedoraproject.org> 5.2.42-2
- disable broken auto completion (#851283)

* Tue Aug 14 2012 Remi Collet <remi@fedoraproject.org> 5.2.42-1
- update to 5.2.42 Community (OSS) Edition (GPL)
  http://dev.mysql.com/doc/workbench/en/wb-news-5-2-42.html

* Sat Aug 11 2012 Remi Collet <remi@fedoraproject.org> 5.2.41-2
- remove bundled documentation, redirect to online
  This documentation is NOT distributed under a GPL license

* Sun Aug 05 2012 Remi Collet <remi@fedoraproject.org> 5.2.41-1
- update to 5.2.41 Community (OSS) Edition (GPL)
  http://dev.mysql.com/doc/workbench/en/wb-news-5-2-41.html
- use system cppconn and antlr
- move binary to libdir (only launcher in bindir)

* Tue May 15 2012 Remi Collet <remi@fedoraproject.org> 5.2.40-1
- update to 5.2.40 Community (OSS) Edition (GPL)
  http://dev.mysql.com/doc/workbench/en/wb-news-5-2-40.html

* Sun Apr 15 2012 Remi Collet <remi@fedoraproject.org> 5.2.39-1
- update to 5.2.39 Community (OSS) Edition (GPL)
  http://dev.mysql.com/doc/workbench/en/wb-news-5-2-39.html
- remove mysql-utilities sub-package (available separately)

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

