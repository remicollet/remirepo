%ifarch ppc ppc64
%define oraclever 10.2.0.2
%else
%define oraclever 11.1.0.7
%endif

%ifarch x86_64
# "client64" is only on 11.1 and x86_64, (10.2 use client)
%define oraclelib %{_libdir}/oracle/%{oraclever}/client64/lib
%define oracleinc %{_includedir}/oracle/%{oraclever}/client64
%else
%define oraclelib %{_libdir}/oracle/%{oraclever}/client/lib
%define oracleinc %{_includedir}/oracle/%{oraclever}/client
%endif


Summary:                Toolkit for Oracle
Name:                   tora
Version:                2.1.0
Release:                1%{?dist}
URL:                    http://tora.sourceforge.net
Group:                  Development/Databases
License:                GPLv2

Source:                 %{name}-%{version}.tar.gz

Patch0:         %{name}-2.1.0.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: desktop-file-utils
BuildRequires: postgresql-devel
BuildRequires: oracle-instantclient-devel = %{oraclever}
BuildRequires: oracle-instantclient-sqlplus = %{oraclever}
BuildRequires: qt-devel >= 4.3.0 qscintilla-devel
BuildRequires: perl cmake openssl-devel glib2-devel

Requires:  qt-mysql qt-postgresql


%description
TOra - Toolkit for Oracle

TOra is supported for running with an Oracle 8.1.7 or newer
client installation. It has been verified to work with Oracle 10g and 11g.

This RPM is build to work with Oracle client %{oraclever}.

TOra also supports PostgreSQL and MySQL.

TOra is developed by a community of Open Source developers. The original 
(pre 1.3.15) development was done by Henrik Johnson of Quest Software, Inc.

The homepage for the TOra project is http://tora.sourceforge.net. If you 
encounter problems you can find both mailinglists and bugtracking tools 
from this page.

See the README file

%prep
%setup -q

%patch0 -p0 -b .orig

cat >%{name}.desktop <<EOF
[Desktop Entry]
Encoding=UTF-8
Name=Toolkit for Oracle
Comment=TOra - Toolkit for Oracle - version %{version}
Exec=tora
Icon=tora
Terminal=false
Type=Application
Categories=Development;
EOF


%{__rm} -rf CMakeFiles CMakeCache.txt

%cmake \
        -DCMAKE_INSTALL_PREFIX:PATH=%{_prefix} \
        -DORACLE_PATH_INCLUDES=%{oracleinc} \
        -DORACLE_PATH_LIB=%{oraclelib} \
        -DPOSTGRESQL_PATH_INCLUDES=%{_includedir} \
        .


%build
%{__make}


%install
%{__rm} -rf "${RPM_BUILD_ROOT}" 

%{__mkdir_p} "${RPM_BUILD_ROOT}%{_prefix}/bin"
%{__mkdir_p} "${RPM_BUILD_ROOT}%{_libdir}/tora/help"
%{__mkdir_p} "${RPM_BUILD_ROOT}%{_libdir}/tora/help/images"
%{__mkdir_p} "${RPM_BUILD_ROOT}%{_libdir}/tora/help/api"
%{__mkdir_p} "${RPM_BUILD_ROOT}%{_datadir}/icons/hicolor/16x16/apps"
%{__mkdir_p} "${RPM_BUILD_ROOT}%{_datadir}/icons/hicolor/32x32/apps"
%{__make} DESTDIR="${RPM_BUILD_ROOT}" install

%{__install} --mode=644 doc/help/*.html "${RPM_BUILD_ROOT}%{_libdir}/tora/help/"
%{__install} --mode=644 doc/help/images/*.png "${RPM_BUILD_ROOT}%{_libdir}/tora/help/images/"
#%{__install} --mode=644 doc/help/api/*.html "${RPM_BUILD_ROOT}%{_libdir}/tora/help/api/"

%{__install} --mode=644 src/icons/tora.xpm     "${RPM_BUILD_ROOT}%{_datadir}/icons/hicolor/32x32/apps/tora.xpm"
%{__install} --mode=644 src/icons/toramini.xpm "${RPM_BUILD_ROOT}%{_datadir}/icons/hicolor/16x16/apps/tora.xpm"

%{__rm} -rf ${RPM_BUILD_ROOT}/%{_datadir}/doc/%{name}

desktop-file-install \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications		\
  %{name}.desktop


%files 
%defattr(-,root,root)
%doc AUTHORS BUGS COPYING ChangeLog NEWS README* TODO
%{_prefix}/bin/%{name}
%{_libdir}/%{name}
%{_datadir}/icons/hicolor/*/apps/%{name}.xpm
%{_datadir}/applications/%{name}.desktop


%post
update-desktop-database &> /dev/null || :
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
  %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi

%postun
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi
update-desktop-database &> /dev/null || :


%clean
%{__rm} -rf "${RPM_BUILD_ROOT}"


%changelog
* Fri Sep 25 2009 Remi Collet <RPMS@famillecollet.com> 2.1.0-1
- Update

* Sun May 10 2009 Remi Collet <RPMS@famillecollet.com> 2.0.0-3.fc11.remi
- F11 build with gcc44 patch

* Wed Jan 07 2009 Remi Collet <RPMS@famillecollet.com> 2.0.0-2.fc10.remi
- PowerPC build againt Oracle 10.2

* Tue Jan 06 2009 Remi Collet <RPMS@famillecollet.com> 2.0.0-1.fc10.remi
- Fedora 10 build

* Tue Oct  7 2008 Michael Mraka <michael.mraka@redhat.com> 2.0.0-0.3041svn
- changed to cmake driven build for 2.0.0 version
- built against oracle-instantclient 

* Mon Jun 29 2005 Nathan Neulinger <nneul@neulinger.org>
- standardize on a single tora spec file


