# SPEC file for
# oracle-instantclient-basic
# oracle-instantclient-devel
# oracle-instantclient-sqlplus
# oracle-instantclient-jdbc

%define __arch_install_post /bin/true

Summary: 	Instant Client for Oracle Database 10g
Name: 		oracle-instantclient
Version: 	10.2.0.3
Release:	3%{?dist}
License:	Oracle
Group:		Applications/File
Url:		http://www.oracle.com/technology/software/tech/oci/instantclient/index.html

Source0:	instantclient-basic-linux32-%{version}-20061115.zip
Source1:	instantclient-jdbc-linux32-%{version}-20061115.zip
Source2:	instantclient-odbc-linux32-%{version}-20061115.zip
Source3:	instantclient-sdk-linux32-%{version}-20061115.zip
Source4:	instantclient-sqlplus-linux32-%{version}-20061115.zip

Source10:	instantclient-basic-linux-x86-64-%{version}-20070103.zip
Source11:	instantclient-jdbc-linux-x86-64-%{version}-20070103.zip
Source12:	instantclient-odbc-linux-x86-64-%{version}-20070103.zip
Source13:	instantclient-sdk-linux-x86-64-%{version}-20070103.zip
Source14:	instantclient-sqlplus-linux-x86-64-%{version}-20070103.zip
NoSource:       0
NoSource:       1
NoSource:       2
NoSource:       3
NoSource:       4
NoSource:       10
NoSource:       11
NoSource:       12
NoSource:       13
NoSource:       14

Buildroot: 	%{_tmppath}/%{name}-root
BuildArch:      i386 x86_64

%define topdir	instantclient_10_2
%define oradir	%{_libdir}/oracle/%{version}/client
%define incdir	%{_includedir}/oracle/%{version}/client

%description
Base files for Instant Client.  Support for OCI, OCCI, 
and JDBC-OCI applications.

%package basic
Summary:	Instant Client for Oracle Database 10g
Group:		Applications/File

%description basic
Base files for Instant Client.  Support for OCI, OCCI,
and JDBC-OCI applications.

%package devel
Summary:	Development headers for Instant Client
Group:		Applications/File
Requires: 	%{name}-basic = %version

%description devel
Additional header files and an example Makefile for developing Oracle
applications with Instant Client.

%package jdbc
Summary: 	Supplemental JDBC features under Instant Client
Group:		Applications/File
Requires: 	%{name}-basic = %version

%description jdbc
Additional support for XA, Internationalization,
and RowSet operations under JDBC.

%package odbc
Summary: 	Oracle  ODBC Instant Client for Linux
Group:		Applications/File
Requires: 	%{name}-basic = %version

%description odbc
Oracle  ODBC Instant Client for Linux complies with 
ODBC 3.52 specifications. It is based on features of 
Oracle 10.2.0.1.0  ODBC driver for Windows, without 
the need for a traditional ORACLE_HOME installation.

%package sqlplus
Summary:	SQL*Plus for Instant Client
Group:		Applications/File
Requires: 	%{name}-basic = %version

%description sqlplus
Additional libraries and executable for running 
SQL*Plus with Instant Client.

%prep
rm -rf %{topdir}

%ifarch i386
unzip %{SOURCE0}
unzip %{SOURCE1}
unzip %{SOURCE2}
unzip %{SOURCE3}
unzip %{SOURCE4}
%else
unzip %{SOURCE10}
unzip %{SOURCE11}
unzip %{SOURCE12}
unzip %{SOURCE13}
unzip %{SOURCE14}
%endif

%install
rm -rf %{buildroot}
cd %{topdir}

%{__mkdir_p} %{buildroot}%{_bindir} 
%{__mkdir_p} %{buildroot}%{oradir}/bin 
%{__mkdir_p} %{buildroot}%{oradir}/lib 
%{__mkdir_p} %{buildroot}%{incdir}
%{__mkdir_p} %{buildroot}%{_sysconfdir}/ld.so.conf.d

# Basic
%__install libclntsh.so.10.1	%{buildroot}%{oradir}/lib
%__install libnnz10.so		%{buildroot}%{oradir}/lib
%__install libocci.so.10.1	%{buildroot}%{oradir}/lib
%__install libociei.so		%{buildroot}%{oradir}/lib
%__install libocijdbc10.so	%{buildroot}%{oradir}/lib
%__install classes12.jar	%{buildroot}%{oradir}/lib
%__install ojdbc14.jar		%{buildroot}%{oradir}/lib
%__install genezi		%{buildroot}%{oradir}/bin

echo %{oradir}/lib >%{buildroot}%{_sysconfdir}/ld.so.conf.d/%{name}.conf

# Devel
%__install -m 644 sdk/include/*.h 	%{buildroot}%{incdir}

ln -s libocci.so.10.1   %{buildroot}%{oradir}/lib/libocci.so
ln -s libclntsh.so.10.1 %{buildroot}%{oradir}/lib/libclntsh.so

# SQL*Plus
%__install sqlplus 		%{buildroot}%{oradir}/bin
%__install glogin.sql 		%{buildroot}%{oradir}/lib
%__install libsqlplus.so 	%{buildroot}%{oradir}/lib
%__install libsqlplusic.so 	%{buildroot}%{oradir}/lib

ln -sf %{oradir}/bin/sqlplus %{buildroot}%{_bindir}/sqlplus

# JDBC
%__install libheteroxa10.so	%{buildroot}%{oradir}/lib
%__install orai18n.jar		%{buildroot}%{oradir}/lib

# ODBC
%__install libsqora.so.10.1	%{buildroot}%{oradir}/lib

%clean
rm -rf %{buildroot}

%post basic
/sbin/ldconfig 

%postun basic
/sbin/ldconfig

%files basic
%defattr(-,root,root)
%{oradir}/lib/libclntsh.so.10.1
%{oradir}/lib/libnnz10.so
%{oradir}/lib/libocci.so.10.1
%{oradir}/lib/libociei.so
%{oradir}/lib/libocijdbc10.so
%{oradir}/lib/classes12.jar
%{oradir}/lib/ojdbc14.jar
%{_sysconfdir}/ld.so.conf.d/%{name}.conf
%{oradir}/bin/genezi

%files devel
%defattr(-,root,root)
%doc %{topdir}/sdk/demo
%{oradir}/lib/libclntsh.so
%{oradir}/lib/libocci.so
%{incdir}/*

%post sqlplus
/sbin/ldconfig 

%postun sqlplus
/sbin/ldconfig

%files sqlplus
%defattr(-,root,root)
%{_bindir}/sqlplus
%{oradir}/bin/sqlplus
%{oradir}/lib/glogin.sql
%{oradir}/lib/libsqlplus.so
%{oradir}/lib/libsqlplusic.so

%files jdbc
%defattr(-,root,root)
%{oradir}/lib/libheteroxa10.so
%{oradir}/lib/orai18n.jar

%files odbc
%defattr(-,root,root)
%doc %{topdir}/ODBC_IC_Readme_Linux.html %{topdir}/ODBCRelnotesJA.htm %{topdir}/ODBCRelnotesUS.htm
%doc %{topdir}/odbc_update_ini.sh
%{oradir}/lib/libsqora.so.10.1

%changelog
* Sun Aug 19 2007 Ciro Iriarte <ciriarte@personal.net.py> 10.2.0.3-3.###.remi
- added genezi to basic package

* Tue May 22 2007 Remi Collet <RPMS@famillecollet.com> 10.2.0.3-3.fc6.remi
- merge 32/64 spec file for mock

* Tue Nov 14 2006 Remi Collet <RPMS@famillecollet.com> 10.2.0.3-1.fc6.remi
- update to 10.2.0.3

* Tue Nov 14 2006 Remi Collet <RPMS@famillecollet.com> 10.2.0.2-3.fc6.remi
- FC6.x86_64 build (conditional targetname & datever)

* Thu Oct 26 2006 Remi Collet <RPMS@famillecollet.com> 10.2.0.2-2.fc6.remi
- FC6.i386 build 

* Fri Jun 23 2006 Remi Collet <RPMS@famillecollet.com> 10.2.0.2-2.fc5.remi
- Switch back to defaut oracle strategie.
- add /etc/ld.so.conf.d/oracle-instantclient.conf

* Fri Jun 23 2006 Remi Collet <RPMS@famillecollet.com> 10.2.0.2-1.fc5.remi
- initial RPM
