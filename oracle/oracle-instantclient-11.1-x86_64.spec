# SPEC file for
# oracle-instantclient-basic
# oracle-instantclient-devel
# oracle-instantclient-sqlplus
# oracle-instantclient-jdbc
# oracle-instantclient-tools

%define __arch_install_post /bin/true

Summary: 	Instant Client for Oracle Database 11g
Name: 		oracle-instantclient-x86_64
Version: 	11.1.0.7
Release:	1%{?dist}
License:	Oracle
Group:		Applications/File
Url:		http://www.oracle.com/technology/software/tech/oci/instantclient/index.html

Source0:	basic-%{version}0-linux-x86_64.zip
Source1:	jdbc-%{version}.0-linux-x86_64.zip
#Source2:	odbc-%{version}.0-linux-x86_64.zip
Source3:	sdk-%{version}.0-linux-x86_64.zip
Source4:	sqlplus-%{version}.0-linux-x86_64.zip
Source5:	tools-%{version}.0-linux-x86_64.zip
NoSource:       0
NoSource:       1
#NoSource:       2
NoSource:       3
NoSource:       4
NoSource:       5

Buildroot: 	%{_tmppath}/%{name}-root
BuildArch:      x86_64

%define topdir	instantclient_11_1
%define oradir	%{_libdir}/oracle/%{version}/client64
%define incdir	%{_includedir}/oracle/%{version}/client64

%description
Base files for Instant Client.  Support for OCI, OCCI, 
and JDBC-OCI applications.

%package -n oracle-instantclient-basic
Summary:	Instant Client for Oracle Database 11g
Group:		Applications/File

%description -n oracle-instantclient-basic
Base files for Instant Client.  Support for OCI, OCCI,
and JDBC-OCI applications.

%package -n oracle-instantclient-devel
Summary:	Development headers for Instant Client
Group:		Applications/File
Requires: 	oracle-instantclient-basic = %version

%description -n oracle-instantclient-devel
Additional header files and an example Makefile for developing Oracle
applications with Instant Client.

%package -n oracle-instantclient-jdbc
Summary: 	Supplemental JDBC features under Instant Client
Group:		Applications/File
Requires: 	oracle-instantclient-basic = %version

%description -n oracle-instantclient-jdbc
Additional support for XA, Internationalization,
and RowSet operations under JDBC.

#%package -n oracle-instantclient-odbc
#Summary: 	Oracle  ODBC Instant Client for Linux
#Group:		Applications/File
#Requires: 	oracle-instantclient-basic = %version

#%description -n oracle-instantclient-odbc
#Oracle  ODBC Instant Client for Linux complies with 
#ODBC 3.52 specifications. It is based on features of 
#Oracle %{version} ODBC driver for Windows, without 
#the need for a traditional ORACLE_HOME installation.

%package -n oracle-instantclient-sqlplus
Summary:	SQL*Plus for Instant Client
Group:		Applications/File
Requires: 	oracle-instantclient-basic = %version

%description -n oracle-instantclient-sqlplus
Additional libraries and executable for running 
SQL*Plus with Instant Client.

%package -n oracle-instantclient-tools
Summary:	Tools for Oracle Database 11g
Group:		Applications/File
Requires: 	oracle-instantclient-basic = %version

%description -n oracle-instantclient-tools
This package provides tools to be used with the Oracle Database.
It currently includes
- wrc : a client to be used with the Database Replay feature

%prep
rm -rf %{topdir}

unzip %{SOURCE0}
unzip %{SOURCE1}
#unzip %{SOURCE2}
unzip %{SOURCE3}
unzip %{SOURCE4}
unzip %{SOURCE5}

%install
rm -rf %{buildroot}
cd %{topdir}

%{__mkdir_p} %{buildroot}%{_bindir} 
%{__mkdir_p} %{buildroot}%{oradir}/bin 
%{__mkdir_p} %{buildroot}%{oradir}/lib 
%{__mkdir_p} %{buildroot}%{incdir}
%{__mkdir_p} %{buildroot}%{_sysconfdir}/ld.so.conf.d

# Basic
%__install libclntsh.so.11.1	%{buildroot}%{oradir}/lib
%__install libnnz11.so		%{buildroot}%{oradir}/lib
%__install libocci.so.11.1	%{buildroot}%{oradir}/lib
%__install libociei.so		%{buildroot}%{oradir}/lib
%__install libocijdbc11.so	%{buildroot}%{oradir}/lib
%__install ojdbc5.jar		%{buildroot}%{oradir}/lib
%__install ojdbc6.jar		%{buildroot}%{oradir}/lib
%__install adrci		%{buildroot}%{oradir}/bin
%__install genezi		%{buildroot}%{oradir}/bin

echo %{oradir}/lib >%{buildroot}%{_sysconfdir}/ld.so.conf.d/%{name}.conf

# Devel
%__install -m 644 sdk/include/*.h 	%{buildroot}%{incdir}
%__install sdk/ottclasses.zip		%{buildroot}%{oradir}/lib

ln -s libocci.so.11.1   %{buildroot}%{oradir}/lib/libocci.so
ln -s libclntsh.so.11.1 %{buildroot}%{oradir}/lib/libclntsh.so

# SQL*Plus
%__install sqlplus 		%{buildroot}%{oradir}/bin
%__install glogin.sql 		%{buildroot}%{oradir}/lib
%__install libsqlplus.so 	%{buildroot}%{oradir}/lib
%__install libsqlplusic.so 	%{buildroot}%{oradir}/lib

ln -sf %{oradir}/bin/sqlplus %{buildroot}%{_bindir}/sqlplus64

# JDBC
%__install libheteroxa11.so	%{buildroot}%{oradir}/lib
%__install orai18n-mapping.jar	%{buildroot}%{oradir}/lib
%__install orai18n.jar		%{buildroot}%{oradir}/lib

# ODBC
#%__install libsqora.so.11.1	%{buildroot}%{oradir}/lib

# Tools
%__install wrc 		%{buildroot}%{oradir}/bin
ln -sf %{oradir}/bin/wrc %{buildroot}%{_bindir}/wrc

%clean
rm -rf %{buildroot}

%post -n oracle-instantclient-basic
/sbin/ldconfig 

%postun -n oracle-instantclient-basic
/sbin/ldconfig

%files -n oracle-instantclient-basic
%defattr(-,root,root)
%doc %{topdir}/BASIC_README
%{oradir}/lib/libclntsh.so.11.1
%{oradir}/lib/libnnz11.so
%{oradir}/lib/libocci.so.11.1
%{oradir}/lib/libociei.so
%{oradir}/lib/libocijdbc11.so
%{oradir}/lib/ojdbc5.jar
%{oradir}/lib/ojdbc6.jar
%{_sysconfdir}/ld.so.conf.d/%{name}.conf
%{oradir}/bin/genezi
%{oradir}/bin/adrci

%files -n oracle-instantclient-devel
%defattr(-,root,root)
%doc %{topdir}/sdk/demo %{topdir}/sdk/SDK_README %{topdir}/sdk/ott 
%{oradir}/lib/libclntsh.so
%{oradir}/lib/libocci.so
%{oradir}/lib/ottclasses.zip
%{incdir}/*

%post -n oracle-instantclient-sqlplus
/sbin/ldconfig 

%postun -n oracle-instantclient-sqlplus
/sbin/ldconfig

%files -n oracle-instantclient-sqlplus
%defattr(-,root,root)
%doc %{topdir}/SQLPLUS_README
%{_bindir}/sqlplus64
%{oradir}/bin/sqlplus
%{oradir}/lib/glogin.sql
%{oradir}/lib/libsqlplus.so
%{oradir}/lib/libsqlplusic.so

%files -n oracle-instantclient-jdbc
%defattr(-,root,root)
%doc %{topdir}/JDBC_README
%{oradir}/lib/libheteroxa11.so
%{oradir}/lib/orai18n-mapping.jar
%{oradir}/lib/orai18n.jar

#%files -n oracle-instantclient-odbc
#%defattr(-,root,root)
#%doc %{topdir}/ODBC_IC_Readme_Linux.html %{topdir}/ODBCRelnotesJA.htm %{topdir}/ODBCRelnotesUS.htm
#%doc %{topdir}/odbc_update_ini.sh
#%{oradir}/lib/libsqora.so.11.1

%files -n oracle-instantclient-tools
%defattr(-,root,root)
%doc %{topdir}/TOOLS_README
%{_bindir}/wrc
%{oradir}/bin/wrc

%changelog
* Thu Dec 04 2008 Remi Collet <RPMS@famillecollet.com> 11.1.0.7-1.###.remi
- update to 11.1.0.7
- add tools sub-package

* Sat Sep 13 2008 Remi Collet <RPMS@famillecollet.com> 11.1.0.6-1.###.remi
- improved split spec

* Tue Dec 11 2007 Remi Collet <RPMS@famillecollet.com> 11.1.0.6-1.###.remi
- version 11.1.0.6

* Fri Nov 09 2007 Remi Collet <RPMS@famillecollet.com> 10.2.0.3-3.fc8.remi
- split spec for i386, x86_64 and ppc
- F8 rebuid

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
