%if !%{defined version}
%define version		5.2.45
%endif
%define release 1
%define edition   gpl
# whether at least Python 2.6 is available
%define have_python26 1
%include %{_rpmconfigdir}/macros.python

# Directory where iodbc and pyodbc binaries are located. Build both using the build_iodbc.sh script
# If using distribution provided ODBC manager lib and pyodbc, then comment out this
%define odbc_home	%{_builddir}/../odbc/usr

Summary: A MySQL visual database modeling, administration and querying tool.
Name: mysql-workbench-%{edition}
Version: %{version}
Release: %{release}%{targos}
Group: Applications/Databases
Vendor: Oracle Corporation
License: GPL
URL: http://wb.mysql.com
Source: %{name}-%{version}-src.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildRequires: pcre-devel >= 3.9
BuildRequires: lua-devel >= 5.1
BuildRequires: automake autoconf libtool
BuildRequires: libzip-devel libxml2-devel
BuildRequires: python-devel >= 2.5
BuildRequires: gnome-keyring-devel
BuildRequires: boost-devel

%if %_vendor == suse
BuildRequires: libmysqlclient-devel, libctemplate-devel
BuildRequires: Mesa
%else
%if %targos == fc17
BuildRequires: ctemplate-devel
%endif
BuildRequires: mysql-devel >= 5.1
BuildRequires: gtkmm24-devel
BuildRequires: mesa-libGL-devel
BuildRequires: sqlite-devel
# In Oracle packages, iodbc is bundled, so we don't need it
#BuildRequires: libiodbc-devel
BuildRequires: make
BuildRequires: tar
BuildRequires: gcc-c++
%endif

%if %_vendor == suse
Requires: python-paramiko python-pexpect
%else
Requires: python-paramiko pexpect
%endif
%if %{defined fc13}
Requires: python-sqlite2
%endif
# requires mysql client pkg (for mysqldump and mysql cmdline client)
Requires: mysql gnome-keyring

# our old package name
Obsoletes: mysql-workbench-oss
Conflicts: mysql-workbench-oss
Conflicts: mysql-workbench-com-se

%description
MySQL Workbench is a modeling tool that allows you to design
and generate MySQL databases graphically. It also has administration
and query development modules where you can manage MySQL server instances
and execute SQL queries.

%prep
%setup -q -n %{name}-%{version}-src

%build

%if %{defined have_python26}
mysql_utilities_flags=--enable-mysql-utilities
%endif

%if %targos == el6
ctemplate_flags=--with-bundled-ctemplate
%endif

NOCONFIGURE=yes ./autogen.sh
%if %{defined odbc_home}
%configure --disable-debug  --disable-dependency-tracking $mysql_utilities_flags $ctemplate_flags --with-odbc-cflags=-I%{odbc_home}/include --with-odbc-libs="-L%{odbc_home}/lib -liodbc"
%else
%configure --disable-debug  --disable-dependency-tracking $mysql_utilities_flags $ctemplate_flags
%endif
make

%install
make install DESTDIR=%{buildroot}
rm -fr %{buildroot}/usr/share/doc/mysql-workbench
%if %{have_python26}
make -C ext install-utils DESTDIR=%{buildroot} 
make -C ext install-connector DESTDIR=%{buildroot} 
%endif

find %{buildroot}%{_libdir}/mysql-workbench -name \*.a  -exec rm {} \; -print
find %{buildroot}%{_libdir}/mysql-workbench -name \*.la -exec rm {} \; -print

%if %{defined odbc_home}
for l in %{odbc_home}/lib/libiodbc.so.* %{odbc_home}/lib/libiodbcinst.so.* %{odbc_home}/lib/libiodbcadm.so.*; do
cp -a $l %{buildroot}%{_libdir}/mysql-workbench
/usr/sbin/prelink -u %{buildroot}%{_libdir}/mysql-workbench/`basename $l` || true
done

if [ %{odbc_home}/../pyodbc.so ]; then
cp -a %{odbc_home}/../pyodbc.so %{buildroot}%{_libdir}/mysql-workbench/modules
fi
cp -a %{odbc_home}/bin/iodbcadm-gtk %{buildroot}%{_libdir}/mysql-workbench/
%endif

%post
touch --no-create %{_datadir}/icons/hicolor || :
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
   %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi

if [ -x %{_bindir}/update-desktop-database ]; then
    %{_bindir}/update-desktop-database
fi

if [ -x %{_bindir}/update-mime-database ]; then
    %{_bindir}/update-mime-database %{_datadir}/mime
fi

%postun
touch --no-create %{_datadir}/icons/hicolor || :
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
   %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi

if [ -x %{_bindir}/update-desktop-database ]; then
    %{_bindir}/update-desktop-database 
fi

if [ -x %{_bindir}/update-mime-database ]; then
    %{_bindir}/update-mime-database %{_datadir}/mime
fi


%clean
rm -rf %{buildroot}
rm -rf %{_builddir}/%{name}-%{version}-src

%files 
%defattr(0644, root, root, 0755)
%doc COPYING README
%attr(0755,root,root) %{_bindir}/mysql*
%attr(0755,root,root) %{_bindir}/wbcopytables
%attr(0755,root,root) %{_datadir}/mysql-workbench/python/mysql*
%attr(0755,root,root) %{_datadir}/mysql-workbench/extras/*.sh
%attr(0755,root,root) %{_libexecdir}/mysql-workbench-bin
%dir %{_libdir}/mysql-workbench
%{_libdir}/mysql-workbench/*
%{_datadir}/icons/hicolor/*/mimetypes/*
%{_datadir}/icons/hicolor/*/apps/*
%{_datadir}/mime-info/*
%{_datadir}/mime/packages/*
%{_datadir}/applications/*.desktop
%dir %{_datadir}/mysql-workbench
%{_datadir}/mysql-workbench/*

%attr(0755,root,root) %{_libdir}/mysql-workbench/iodbcadm-gtk

%changelog

