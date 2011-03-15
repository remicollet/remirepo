Summary:    C++ wrapper for the MySQL C API
Name:       mysql++
Version:    3.1.0
Release:    6%{?dist}
License:    LGPLv2
Group:      Development/Libraries
URL:        http://tangentsoft.net/mysql++/

Source0:    http://tangentsoft.net/mysql++/releases/mysql++-%{version}.tar.gz
Source1:    mysql++.devhelp

Patch0:     mysql++-gcc.patch

BuildRoot:  %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildRequires: mysql-devel


%description
MySQL++ is a C++ wrapper for MySQL’s C API. 

It is built around STL principles, to make dealing with the database as easy
as dealing with an STL container. MySQL++ relieves the programmer of dealing
with cumbersome C data structures, generation of repetitive SQL statements,
and manual creation of C++ data structures to mirror the database schema.

If you are building your own MySQL++-based programs, you also need 
to install the -devel package.


%package devel
Summary:   MySQL++ developer files (headers, examples, etc.)
Group:     Development/Libraries
Requires:  mysql++%{?_isa} = %{version}-%{release}
Requires:  mysql-devel%{?_isa}

%description devel
These are the files needed to compile MySQL++ based programs, 
plus some sample code to get you started.You probably need to
install the -manuals package.  

If you aren't building your own programs, you probably don't need 
to install this package.


%package manuals
Summary:   MySQL++ user and reference manuals
Group:     Development/Libraries
Requires:  devhelp

%description manuals
This is the MySQL++ documentation.  It's a separate RPM just because
it's so large, and it doesn't change with every release.

User Manual and Reference Manual are provided both in PDF and in
HTML format. You can use devhelp to browse it.


%prep
%setup -q

%patch0 -p1 -b gcc44

for file in CREDITS COPYING LICENSE; do
  touch -r $file.txt timestamp
  %{__sed} -i -e 's/\r//' $file.txt
  touch -r timestamp $file.txt 
done


%build
%configure --with-mysql-lib=%{_libdir}/mysql \
           --enable-thread-check \
           --disable-dependency-tracking \
           PTHREAD_CFLAGS=-pthread PTHREAD_LIBS=-lpthread

%{__make} %{?_smp_mflags}


%install
rm -rf %{buildroot} doc/examples

%{__mkdir_p} %{buildroot}{%{_libdir},%{_includedir}}

%{__make} DESTDIR=%{buildroot} install

# Copy example programs to doc directory
%{__mkdir_p} doc/examples/{ssx,test}
%{__install} -m644 examples/*.{cpp,h} doc/examples/
%{__install} -m644 config.h doc/examples/
%{__install} -m644 ssx/{parsev2,genv2,main}.cpp doc/examples/ssx
%{__install} -m644 ssx/{parsev2,genv2}.h doc/examples/ssx
%{__install} -m644 test/ssqls2.cpp doc/examples/test
sed -i -e s@../config.h@config.h@ doc/examples/threads.h


# Fix up simple example Makefile to allow it to build on the install
# system, as opposed to the system where the Makefile was created.
# Only build examples, not test_
%{__sed} -e 's@./examples/@@' \
  -e 's@^CPPFLAGS ?=.*$@CPPFLAGS ?= $(shell mysql_config --cflags)@' \
  -e 's@^LDFLAGS ?=.*$@LDFLAGS ?= $(shell mysql_config --libs_r)@' \
  -e '/^all:/s/test_[a-z,_]* //g' \
  Makefile.simple > doc/examples/Makefile

# DevHelp stuff
%{__mkdir_p} %{buildroot}%{_datadir}/devhelp/books/%{name}
%{__install} -m644 %{SOURCE1} %{buildroot}%{_datadir}/devhelp/books/%{name}/%{name}.devhelp
%{__cp} -r doc/html/userman %{buildroot}%{_datadir}/devhelp/books/%{name}/userman
%{__cp} -r doc/html/refman %{buildroot}%{_datadir}/devhelp/books/%{name}/refman


%clean
rm -rf %{buildroot} doc/examples

%post -p /sbin/ldconfig 

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc ChangeLog COPYING.txt CREDITS.txt LICENSE.txt README.txt
%{_libdir}/libmysqlpp.so.*


%files devel
%defattr(-,root,root,-)
%doc doc/examples doc/README-devel-RPM.txt README-examples.txt Wishlist
%{_includedir}/mysql++
%{_libdir}/libmysqlpp.so


%files manuals
%defattr(-,root,root,-)
%doc doc/pdf/* doc/README-manuals-RPM.txt doc/userman/LICENSE.txt
%{_datadir}/devhelp/books/%{name}


%changelog
* Sat Feb 12 2011 Remi Collet <Fedora@FamilleCollet.com> 3.1.0-6
- arch specific requires

* Fri Feb 11 2011 Remi Collet <Fedora@FamilleCollet.com> 3.1.0-5
- update patch for gcc 4.6

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 28 2010 Remi Collet <Fedora@FamilleCollet.com> 3.1.0-3
- rebuild against MySQL 5.5.8
- add missing files in the "examples" provided

* Thu Jul 08 2010 Remi Collet <Fedora@FamilleCollet.com> 3.1.0-2
- add LICENSE to manuals subpackage

* Sun Jun 20 2010 Remi Collet <Fedora@FamilleCollet.com> 3.1.0-1
- update to 3.1.0

* Sat Feb 13 2010 Remi Collet <Fedora@FamilleCollet.com> 3.0.9-4
- add explicit -lpthread linker flag (fix DSO bug)

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 05 2009 Remi Collet <Fedora@FamilleCollet.com> 3.0.9-1
- update to 3.0.9

* Fri Jan 23 2009 Remi Collet <Fedora@FamilleCollet.com> 3.0.8-2
- rebuild against MySQL Client 5.1 (libmysqlclient.so.16)

* Sun Nov 30 2008 Remi Collet <Fedora@FamilleCollet.com> 3.0.8-1
- update to 3.0.8

* Sun Nov 23 2008 Remi Collet <Fedora@FamilleCollet.com> 3.0.7-1
- update to 3.0.7

* Sun Aug 17 2008 Remi Collet <Fedora@FamilleCollet.com> 3.0.6-1
- update to 3.0.6
- thread aware examples.

* Sat Aug 09 2008 Remi Collet <Fedora@FamilleCollet.com> 3.0.5-1
- update to 3.0.5

* Sat Jul 05 2008 Remi Collet <Fedora@FamilleCollet.com> 3.0.4-1
- update to 3.0.4

* Tue May 13 2008 Remi Collet <Fedora@FamilleCollet.com> 3.0.3-1
- update to 3.0.3
- add mysql++-3.0.3-mystring.patch for x86_64 build

* Tue Apr 15 2008 Remi Collet <Fedora@FamilleCollet.com> 3.0.2-1
- update to 3.0.2

* Sat Mar 29 2008 Remi Collet <Fedora@FamilleCollet.com> 3.0.1-1
- update to 3.0.1

* Sat Mar  1 2008 Remi Collet <Fedora@FamilleCollet.com> 3.0.0-1
- update to 3.0.0 Finale
- use devhelp to browse manuals

* Wed Feb 20 2008 Remi Collet <rpms@FamilleCollet.com> 3.0.0-0.1.rc5
- update to 3.0.0 rc5

* Tue Feb 12 2008 Remi Collet <rpms@FamilleCollet.com> 3.0.0-0.1.rc4
- update to 3.0.0 rc4 (not published)

* Sat Feb  9 2008 Remi Collet <rpms@FamilleCollet.com> 3.0.0-0.1.rc3
- update to 3.0.0 rc3 (not published)

* Sat Feb  9 2008 Remi Collet <rpms@FamilleCollet.com> 2.3.2-3
- rebuild for gcc 4.3

* Thu Aug 23 2007 Remi Collet <rpms@FamilleCollet.com> 2.3.2-2
- Fix License
- F-8 rebuild (BuildID)

* Sat Jul 14 2007 Remi Collet <rpms@FamilleCollet.com> 2.3.2-1
- update to 2.3.2

* Wed Jul 11 2007 Remi Collet <rpms@FamilleCollet.com> 2.3.1-1
- update to 2.3.1

* Tue Jul 03 2007 Remi Collet <rpms@FamilleCollet.com> 2.3.0-1
- update to 2.3.0 

* Tue Apr 17 2007 Remi Collet <rpms@FamilleCollet.com> 2.2.3-1
- update to 2.2.3, 
- del doc patch
- change BuildRoot
- add Requires mysql-devel for mysql++-devel

* Mon Apr 16 2007 Remi Collet <rpms@FamilleCollet.com> 2.2.2-1
- update to 2.2.2, with soname support :)

* Mon Mar 19 2007 Remi Collet <rpms@FamilleCollet.com> 2.2.1-3
- Warren Young comments : http://lists.mysql.com/plusplus/6444

* Sun Mar 18 2007 Remi Collet <rpms@FamilleCollet.com> 2.2.1-2
- find perm on common.h
- soname mysql++-2.2.1-bkl.patch

* Wed Feb 28 2007 Remi Collet <rpms@FamilleCollet.com> 2.2.1-1
- Initial spec for Extras

* Wed Feb 28 2007 Remi Collet <rpms@FamilleCollet.com> 2.2.1-1.fc{3-6}.remi
- update to version 2.2.1

* Thu Jan 25 2007 Remi Collet <rpms@FamilleCollet.com> 2.2.0-1.fc{3-6}.remi
- update to version 2.2.0

* Mon Nov 13 2006 Remi Collet <rpms@FamilleCollet.com> 2.1.1.fc6.remi
- FC6.x86_64 build
- dynamic (sed) patch for Makefile (use mysql_config)

* Thu Nov 02 2006 Remi Collet <rpms@FamilleCollet.com> 2.1.1.fc6.remi
- FC6 build

* Sat Apr  8 2006 Remi Collet <rpms@FamilleCollet.com> 2.1.1.fc{3,4,5}.remi
- update to version 2.1.1

* Sat Nov 26 2005 Remi Collet <remi.collet@univ-reims.fr> 2.0.7-1.fc3.remi - 2.0.7-1.fc4.remi
- update to version 2.0.4
- build with mysql-5.0.15 (requires libmysqlclient.so.15)

* Sun Sep  4 2005 Remi Collet <remi.collet@univ-reims.fr> 2.0.4-1.FC4.remi
- version 2.0.4

* Sat Aug 20 2005 Remi Collet <remi.collet@univ-reims.fr> 2.0.2-1.FC4.remi
- built for FC4
- spec cleanning...

* Thu Jun 16 2005 Remi Collet <Remi.Collet@univ-reims.fr> 1.7.40-1.FC3.remi
- built for FC3 and MySQL 4.1.11
- examples in /usr/share/doc/mysql++-%%{version}/examples

* Sat Apr 30 2005 Warren Young <mysqlpp@etr-usa.com> 1.7.34-1
- Split manuals out into their own sub-package.

* Thu Mar 10 2005 Warren Young <mysqlpp@etr-usa.com> 1.7.32-1
- Disabled building of examples, to speed RPM build.

* Fri Nov 05 2004 Warren Young <mysqlpp@etr-usa.com> 1.7.21-1
- Split out -devel subpackage, which now includes the examples

* Wed Aug 18 2004 Warren Young <mysqlpp@etr-usa.com> 1.7.11-1
- Removed examples from documentation.
- Limited documentation to just the generated files, not the sources.

* Wed Apr 16 2003 Tuan Hoang <tqhoang@bigfoot.com> 1.7.9-4
- Added gcc 3.2.2 patch.
- Packaged using Red Hat Linux 8.0 and 9.

* Thu Nov 14 2002 Tuan Hoang <tqhoang@bigfoot.com> 1.7.9-3
- Changed the version passed to libtool.

* Mon Oct 28 2002 Tuan Hoang <tqhoang@bigfoot.com> 1.7.9-2
- Updated the version numbering of the library to be 1.7.9.
- Packaged using Red Hat Linux 8.0.

* Thu Oct 17 2002 Philipp Berndt <philipp.berndt@gmx.net>
- packaged
