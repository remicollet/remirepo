# SPEC file for i386 version of
# oracle-instantclient-basic
# oracle-instantclient-devel
# oracle-instantclient-sqlplus
# oracle-instantclient-jdbc
# oracle-instantclient-odbc
# oracle-instantclient-tools

%define __arch_install_post /bin/true

%global major   12
%global mainver 12.1

Summary: 	Instant Client for Oracle Database 11g
Name: 		oracle-instantclient-i386
Version: 	12.1.0.1.0
Release:	1%{?dist}
License:	Oracle
Group:		Applications/File
Url:		http://www.oracle.com/technology/software/tech/oci/instantclient/index.html

Source0:	instantclient-basic-linux-%{version}.zip
Source1:	instantclient-jdbc-linux-%{version}.zip
Source2:	instantclient-odbc-linux-%{version}.zip
Source3:	instantclient-sdk-linux-%{version}.zip
Source4:	instantclient-sqlplus-linux-%{version}.zip
Source5:	instantclient-tools-linux-%{version}.zip
Source6:	instantclient-precomp-linux-%{version}.zip
NoSource:       0
NoSource:       1
NoSource:       2
NoSource:       3
NoSource:       4
NoSource:       5
NoSource:       6

Buildroot: 	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
#BuildArch:      i386

%global topdir	instantclient_12_1
%global oradir	%{_libdir}/oracle/%{mainver}/client
%global incdir	%{_includedir}/oracle/%{mainver}/client

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
Requires: 	oracle-instantclient-basic%{?_isa} = %version

%description -n oracle-instantclient-devel
Additional header files and an example Makefile for developing Oracle
applications with Instant Client.

%package -n oracle-instantclient-jdbc
Summary: 	Supplemental JDBC features under Instant Client
Group:		Applications/File
Requires: 	oracle-instantclient-basic%{?_isa} = %version

%description -n oracle-instantclient-jdbc
Additional support for XA, Internationalization,
and RowSet operations under JDBC.

%package -n oracle-instantclient-odbc
Summary: 	Oracle  ODBC Instant Client for Linux
Group:		Applications/File
Requires: 	oracle-instantclient-basic%{?_isa} = %version

%description -n oracle-instantclient-odbc
Oracle  ODBC Instant Client for Linux complies with 
ODBC 3.52 specifications. It is based on features of 
Oracle %{version} ODBC driver for Windows, without 
the need for a traditional ORACLE_HOME installation.

%package -n oracle-instantclient-sqlplus
Summary:	SQL*Plus for Instant Client
Group:		Applications/File
Requires: 	oracle-instantclient-basic%{?_isa} = %version

%description -n oracle-instantclient-sqlplus
Additional libraries and executable for running 
SQL*Plus with Instant Client.

%package -n oracle-instantclient-tools
Summary:	Tools for Oracle Database 11g
Group:		Applications/File
Requires: 	oracle-instantclient-basic%{?_isa} = %version

%description -n oracle-instantclient-tools
This package provides tools to be used with the Oracle Database.
It currently includes
- wrc : a client to be used with the Database Replay feature

%package -n oracle-instantclient-precomp
Summary:	Oracle Precompilers for Pro*C and Pro*COBOL
Group:		Applications/File
Requires: 	oracle-instantclient-devel%{?_isa} = %version

%description -n oracle-instantclient-precomp
PRECOMP Instant Client (IC) Package contains following
components:
  i) "proc" binary to precompile a Pro*C application
 ii) "procob" binary to precompile a Pro*COBOL application
iii) sample configuration files, demo programs and demo
     make files for building proc and procob demos and
     in general any Pro*C/Pro*COBOL application.


%prep
rm -rf %{topdir}

unzip %{SOURCE0}
unzip %{SOURCE1}
unzip %{SOURCE2}
unzip %{SOURCE3}
unzip %{SOURCE4}
unzip %{SOURCE5}
unzip %{SOURCE6}

%install
rm -rf %{buildroot}
cd %{topdir}

mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{oradir}/{bin,lib,precomp/admin}
mkdir -p %{buildroot}%{oradir}/lib
mkdir -p %{buildroot}%{incdir}
mkdir -p %{buildroot}%{_sysconfdir}/ld.so.conf.d

# Basic
install -p adrci		%{buildroot}%{oradir}/bin
install -p genezi		%{buildroot}%{oradir}/bin
install -p uidrvci		%{buildroot}%{oradir}/bin
install -p libclntshcore.so.%{mainver}	%{buildroot}%{oradir}/lib
install -p libclntsh.so.%{mainver}	%{buildroot}%{oradir}/lib
install -p libnnz%{major}.so		%{buildroot}%{oradir}/lib
install -p libocci.so.%{mainver}	%{buildroot}%{oradir}/lib
install -p libociei.so				%{buildroot}%{oradir}/lib
install -p libocijdbc%{major}.so	%{buildroot}%{oradir}/lib
install -p libons.so				%{buildroot}%{oradir}/lib
install -p liboramysql%{major}.so	%{buildroot}%{oradir}/lib
install -p ojdbc6.jar		%{buildroot}%{oradir}/lib
install -p ojdbc7.jar		%{buildroot}%{oradir}/lib
install -p xstreams.jar		%{buildroot}%{oradir}/lib

echo %{oradir}/lib >%{buildroot}%{_sysconfdir}/ld.so.conf.d/%{name}.conf

# Devel
install -p -m 644 sdk/include/*.h 	%{buildroot}%{incdir}
install -p sdk/ottclasses.zip		%{buildroot}%{oradir}/lib
install -p -m 755 sdk/ott		%{buildroot}%{oradir}/bin

ln -s %{oradir}/bin/ott           %{buildroot}%{_bindir}/ott
ln -s libocci.so.%{mainver}       %{buildroot}%{oradir}/lib/libocci.so
ln -s libclntsh.so.%{mainver}     %{buildroot}%{oradir}/lib/libclntsh.so
ln -s libclntshcore.so.%{mainver} %{buildroot}%{oradir}/lib/libclntshcore.so

# sdk/admin/oraaccess.xsd not provided in upstream RPM.

# SQL*Plus
install -p sqlplus 		%{buildroot}%{oradir}/bin
install -p glogin.sql 		%{buildroot}%{oradir}/lib
install -p libsqlplus.so 	%{buildroot}%{oradir}/lib
install -p libsqlplusic.so 	%{buildroot}%{oradir}/lib

ln -sf %{oradir}/bin/sqlplus %{buildroot}%{_bindir}/sqlplus

# JDBC
install -p libheteroxa%{major}.so	%{buildroot}%{oradir}/lib
install -p orai18n-mapping.jar	%{buildroot}%{oradir}/lib
install -p orai18n.jar		%{buildroot}%{oradir}/lib

# ODBC
install -p libsqora.so.%{mainver}	%{buildroot}%{oradir}/lib

# Tools
install -p wrc 		%{buildroot}%{oradir}/bin
ln -sf %{oradir}/bin/wrc %{buildroot}%{_bindir}/wrc

# Precomp
install -p -m 755 sdk/{proc,procob,rtsora}	%{buildroot}%{oradir}/bin
install -p -m 755 cobsqlintf.o		%{buildroot}%{oradir}/lib
install -p -m 644 precomp/admin/*	%{buildroot}%{oradir}/precomp/admin

ln -s %{oradir}/bin/proc %{buildroot}%{_bindir}/proc
ln -s %{oradir}/bin/procob %{buildroot}%{_bindir}/procob
ln -s %{oradir}/bin/rtsora %{buildroot}%{_bindir}/rtsora

# Precomp-Devel
install -p -m 644 sdk/include/*.h     %{buildroot}%{incdir}


%clean
rm -rf %{buildroot}

%post -n oracle-instantclient-basic
/sbin/ldconfig 

%postun -n oracle-instantclient-basic
/sbin/ldconfig

%files -n oracle-instantclient-basic
%defattr(-,root,root)
%doc %{topdir}/BASIC_README
%dir %{oradir}
%dir %{oradir}/lib
%dir %{oradir}/bin
%{oradir}/lib/libclntshcore.so.%{mainver}
%{oradir}/lib/libclntsh.so.%{mainver}
%{oradir}/lib/libnnz%{major}.so
%{oradir}/lib/libocci.so.%{mainver}
%{oradir}/lib/libociei.so
%{oradir}/lib/libocijdbc%{major}.so
%{oradir}/lib/libons.so
%{oradir}/lib/liboramysql%{major}.so
%{oradir}/lib/ojdbc6.jar
%{oradir}/lib/ojdbc7.jar
%{oradir}/lib/xstreams.jar
%{_sysconfdir}/ld.so.conf.d/%{name}.conf
%{oradir}/bin/genezi
%{oradir}/bin/adrci
%{oradir}/bin/uidrvci

%files -n oracle-instantclient-devel
%defattr(-,root,root)
%doc %{topdir}/sdk/demo %{topdir}/sdk/SDK_README %{topdir}/sdk/ott 
%{oradir}/lib/libclntshcore.so
%{oradir}/lib/libclntsh.so
%{oradir}/lib/libocci.so
%{oradir}/lib/ottclasses.zip
%{incdir}
%{_bindir}/ott
%{oradir}/bin/ott

%post -n oracle-instantclient-sqlplus
/sbin/ldconfig 

%postun -n oracle-instantclient-sqlplus
/sbin/ldconfig

%files -n oracle-instantclient-sqlplus
%defattr(-,root,root)
%doc %{topdir}/SQLPLUS_README
%{_bindir}/sqlplus
%{oradir}/bin/sqlplus
%{oradir}/lib/glogin.sql
%{oradir}/lib/libsqlplus.so
%{oradir}/lib/libsqlplusic.so

%files -n oracle-instantclient-jdbc
%defattr(-,root,root)
%doc %{topdir}/JDBC_README
%{oradir}/lib/libheteroxa%{major}.so
%{oradir}/lib/orai18n-mapping.jar
%{oradir}/lib/orai18n.jar

%files -n oracle-instantclient-odbc
%defattr(-,root,root)
%doc %{topdir}/ODBC_IC_Readme_Unix.html %{topdir}/ODBCRelnotesJA.htm %{topdir}/ODBCRelnotesUS.htm
%doc %{topdir}/odbc_update_ini.sh
%doc %{topdir}/help
%{oradir}/lib/libsqora.so.%{mainver}

%files -n oracle-instantclient-tools
%defattr(-,root,root)
%doc %{topdir}/TOOLS_README
%{_bindir}/wrc
%{oradir}/bin/wrc

%files -n oracle-instantclient-precomp
%defattr(-,root,root)
%doc %{topdir}/sdk/demo %{topdir}/PRECOMP_README
%dir %{oradir}/precomp
%dir %{oradir}/precomp/admin
%config  %{oradir}/precomp/admin/pcbcfg.cfg
%config  %{oradir}/precomp/admin/pcscfg.cfg
%{oradir}/lib/cobsqlintf.o
%{oradir}/bin/proc
%{oradir}/bin/procob
%{oradir}/bin/rtsora
%{_bindir}/proc
%{_bindir}/procob
%{_bindir}/rtsora


%changelog
* Fri Jul 26 2013 Remi Collet <RPMS@famillecollet.com> 12.1.0.1.0-1
- update to 12.1.0.1.0

* Wed Feb 29 2012 Remi Collet <RPMS@famillecollet.com> 11.2.0.3.0-1
- update to 11.2.0.3.0
- add precomp subpackage
- merge some changes from  Ciro Iriarte <ciro.iriarte@gmail.com>
  http://track.itsolutions.com.py/pub/oracle/oracle-instantclient.spec

* Thu Nov 11 2010 Remi Collet <RPMS@famillecollet.com> 11.2.0.2.0-1
- update to 11.2.0.2.0

* Sat Dec 26 2009 Remi Collet <RPMS@famillecollet.com> 11.2.0.1-1.###.remi
- update to 11.2.0.1

* Sun Nov 30 2008 Remi Collet <RPMS@famillecollet.com> 11.1.0.7-1.###.remi
- update to 11.1.0.7
- add tools sub-package

* Sat Sep 13 2008 Remi Collet <RPMS@famillecollet.com> 11.1.0.6-1.###.remi
- improved split spec

* Tue Oct 30 2007 Remi Collet <RPMS@famillecollet.com> 11.1.0.6-1.###.remi
- split spec for i386, x86_64 and ppc
- update to 11.1.0.6.0

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
