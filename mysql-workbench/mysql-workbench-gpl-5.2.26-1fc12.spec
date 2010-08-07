%if !%{defined version}
%define version		5.2.26
%endif
%define release		1
%define edition   gpl

Summary: A MySQL visual database modeling, administration and querying tool.
Name: mysql-workbench-%{edition}
Version: %{version}
Release: %{release}%{targos}
Group: Applications/Databases
Vendor: Oracle Corporation
License: GPL
URL: http://wb.mysql.com
Source: %{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildRequires: pcre-devel >= 3.9
BuildRequires: libglade2-devel >= 2.0.0
BuildRequires: lua-devel >= 5.1
BuildRequires: libgnome-devel >= 2
BuildRequires: automake autoconf libtool
BuildRequires: lua-devel
BuildRequires: libzip-devel libxml2-devel
BuildRequires: libglade2-devel 
BuildRequires: readline-devel
BuildRequires: python-devel >= 2.4
BuildRequires: gnome-keyring-devel
BuildRequires: boost-devel

%if %{defined suse}
BuildRequires: libmysqlclient-devel
BuildRequires: Mesa
%else
BuildRequires: mysql-devel >= 5.1
%if !%{defined centos}
BuildRequires: uuid-devel
%endif
BuildRequires: gtkmm24-devel
BuildRequires: mesa-libGL-devel
%endif

%if %{defined suse}
Requires: python-paramiko python-pexpect 
%else
Requires: python-paramiko pexpect 
%endif
%if %{defined fc12}
Requires: python-sqlite2
%endif
# requires mysql client pkg (for mysqldump and mysql cmdline client)
Requires: mysql gnome-keyring

# our old package name
Obsoletes: mysql-workbench-oss
Conflicts: mysql-workbench-oss

%description
MySQL Workbench is a modeling tool that allows you to design
and generate MySQL databases graphically. It also has administration
and query development modules where you can manage MySQL server instances
and execute SQL queries.

%prep
%setup -q -n %{name}-%{version}

%build

NOCONFIGURE=yes ./autogen.sh
%configure --disable-debug --enable-python-modules
make

%install
make install DESTDIR=%{buildroot}
%if %{defined centos}
for l in libpixman-1.so.0 libcairo.so.2 libatkmm-1.6.so.1 libcairomm-1.0.so.1 libgdkmm-2.4.so.1 libglibmm-2.4.so.1 libgtkmm-2.4.so.1 libpangomm-1.4.so.1 libzip.so.1 libsigc-2.0.so.0; do
cp %{_libdir}/$l %{buildroot}/%{_libdir}/mysql-workbench
/usr/sbin/prelink -u %{buildroot}/%{_libdir}/mysql-workbench/$l || true
done
%endif

%clean
rm -rf %{buildroot}
rm -rf %{_builddir}/%{name}-%{version}

%files
%defattr(0644, root, root, 0755)
%doc COPYING
%attr(0755,root,root) %{_bindir}/mysql-workbench
%attr(0755,root,root) %{_bindir}/mysql-workbench-bin
%dir %{_libdir}/mysql-workbench
%{_libdir}/mysql-workbench/*
%{_datadir}/applications/*.desktop
%dir %{_datadir}/mysql-workbench
%{_datadir}/mysql-workbench/*

%changelog

