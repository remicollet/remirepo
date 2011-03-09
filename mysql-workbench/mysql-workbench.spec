%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

%global postver -src
%global mw_version 5.2.32
%global tartype gpl
#global cppconnver 1.1.0-0.3.bzr895

# "script_templates" (and some others) shouldn't be compiled
%global _python_bytecompile_errors_terminate_build 0

Summary:   A MySQL visual database modeling, administration and querying tool
Name:      mysql-workbench
Version:   %{mw_version}
Release:   1%{?dist}
Group:     Applications/Databases
License:   GPLv2 with exceptions

URL:       http://wb.mysql.com
# Upstream has a mirror redirector for downloads, so the URL is hard to
# represent statically.  You can get the tarball by following a link from
# http://dev.mysql.com/downloads/workbench/
Source:    http://gd.tuwien.ac.at/db/mysql/Downloads/MySQLGUITools/%{name}-%{tartype}-%{version}%{?postver}.tar.gz

# don't build extension, use system one
# !!! This patch use versioned soname (libmysqlcppconn.so.5) !!!
Patch1:    %{name}-5.2.28-cppconn.patch
Patch2:    %{name}-5.2.32-ctemplate.patch
Patch3:    %{name}-5.2.32-tinyxml.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: pcre-devel >= 3.9
BuildRequires: libglade2-devel >= 2.0.0
BuildRequires: lua-devel >= 5.1
%if 0%{?fedora} >= 12 || 0%{?rhel} >= 6
BuildRequires: ctemplate-devel
%endif
BuildRequires: libgnome-devel >= 2
BuildRequires: automake autoconf libtool
BuildRequires: libzip-devel libxml2-devel
BuildRequires: readline-devel
BuildRequires: python-devel >= 2.4
BuildRequires: gnome-keyring-devel
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
BuildRequires: gtkmm24-devel
BuildRequires: libGL-devel
BuildRequires: sqlite-devel
%if 0%{?cppconnver:1}
BuildRequires: mysql-connector-c++-devel >= %{cppconnver}
%endif
BuildRequires: desktop-file-utils
BuildRequires: tinyxml-devel

Requires: python-paramiko pexpect python-sqlite2
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
Version:        1.0.0
Release:        0%{?dist}

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
%setup -q -n %{name}-%{tartype}-%{mw_version}%{?postver}

%if 0%{?cppconnver:1}
# Use system cppconn if an upstream version
%patch1 -p1 -b .cppconn
rm -rf ext/cppconn
%endif

%if 0%{?fedora} >= 12 || 0%{?rhel} >= 6
%patch2 -p1 -b .ctemplate
%endif

%patch3 -p1 -b .tinyxml

touch -r COPYING .timestamp4rpm
%{__sed} -i -e 's/\r//g' COPYING
touch -r .timestamp4rpm COPYING

# we use System provided libraries
rm -rf ext/boost
rm -rf ext/curl
rm -rf ext/libsigc++
rm -rf ext/yassl
%if 0%{?fedora} >= 12 || 0%{?rhel} >= 6
rm -rf ext/ctemplate
%endif
rm -rf library/tinyxml

# avoid "No such file" during configure
touch po/POTFILES.in


%build
NOCONFIGURE=yes ./autogen.sh
%configure --disable-debug --enable-mysql-utilities

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
%{__install} --directory %{buildroot}%{_prefix}/man/man1
%{__python} setup.py install --skip-profile --root %{buildroot}

%if 0%{?fedora} >= 14
%{__install} --directory %{buildroot}%{_mandir}
%{__mv} %{buildroot}%{_prefix}/man/man1 %{buildroot}%{_mandir}/man1
%endif
popd


# clean dev files
echo Cleanup dev file
find %{buildroot}%{_libdir}/%{name} -name \*.a  -exec rm {} \; -print
find %{buildroot}%{_libdir}/%{name} -name \*.la -exec rm {} \; -print

# fix perms
%{__chmod} +x %{buildroot}%{_datadir}/%{name}/sshtunnel.py

#desktop file
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
# NEWS and ChangeLog are empty or outdated
%doc AUTHORS COPYING COPYING.LGPL README samples
%{_bindir}/%{name}
%{_bindir}/%{name}-bin
%{_datadir}/applications/MySQLWorkbench.desktop
%{_libdir}/%{name}
%{_datadir}/%{name}
%exclude %{_datadir}/doc/%{name}


%files -n mysql-utilities
%defattr(-, root, root, -)
%doc ext/mysql-utilities/*.txt
%{_bindir}/mysqldbcopy
%{_bindir}/mysqldbexport
%{_bindir}/mysqldbimport
%{_bindir}/mysqldiff
%{_bindir}/mysqldiskusage
%{_bindir}/mysqlindexcheck
%{_bindir}/mysqlmetagrep
%{_bindir}/mysqlprocgrep
%{_bindir}/mysqlreplicate
%{_bindir}/mysqlserverclone
%{_bindir}/mysqluserclone
%{python_sitelib}/mysql/utilities
%{python_sitelib}/mysql_utilities*
%if 0%{?fedora} >= 14
%{_mandir}/man1/*
%endif
# empty file already provided by mysql-connector-python
%exclude %{python_sitelib}/mysql/__init*


%changelog
* Wed Mar 09 2011 Remi Collet <Fedora@famillecollet.com> 5.2.32-1
- update to 5.2.32 Community (OSS) Edition (GPL)
  http://dev.mysql.com/doc/workbench/en/wb-news-5-2-32.html
- use bundled cppconn (which is a fork of svn version...)
- add mysql-utilities sub-package
- requires mysql-connector-python

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

