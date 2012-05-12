# set to zero to avoid running test suite
%define make_check 1

%define with_java 1
%define with_kwallet 1

# set JDK path to build javahl; default for JPackage
%define jdk_path /usr/lib/jvm/java

%define perl_vendorarch %(eval "`%{__perl} -V:installvendorarch`"; echo $installvendorarch)

%if 0%{?fedora} < 18
%define dbdevel db4-devel
%else
%define dbdevel libdb-devel
%endif

%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

%{!?_httpd_apxs: %{expand: %%global _httpd_apxs %%{_sbindir}/apxs}}
%{!?_httpd_mmn: %{expand: %%global _httpd_mmn %%(cat %{_includedir}/httpd/.mmn || echo missing-httpd-devel)}}
%{!?_httpd_confdir:    %{expand: %%global _httpd_confdir    %%{_sysconfdir}/httpd/conf.d}}
# /etc/httpd/conf.d with httpd < 2.4 and defined as /etc/httpd/conf.modules.d with httpd >= 2.4
%{!?_httpd_modconfdir: %{expand: %%global _httpd_modconfdir %%{_sysconfdir}/httpd/conf.d}}

Summary: A Modern Concurrent Version Control System
Name: subversion
Version: 1.7.4
Release: 6%{?dist}
License: ASL 2.0
Group: Development/Tools
URL: http://subversion.apache.org/
Source0: http://subversion.tigris.org/downloads/subversion-%{version}.tar.bz2
Source1: subversion.conf
Source3: filter-requires.sh
Source4: http://www.xsteve.at/prg/emacs/psvn.el
Source5: psvn-init.el
Source6: svnserve.service
Source7: svnserve.tmpfiles
Source8: svnserve.sysconf
Patch1: subversion-1.7.0-rpath.patch
Patch2: subversion-1.7.0-pie.patch
Patch3: subversion-1.7.0-kwallet.patch
Patch4: subversion-1.7.2-ruby19.patch
Patch5: subversion-1.7.4-hashorder.patch
Patch6: subversion-1.7.4-httpd24.patch
Patch7: subversion-1.7.4-kwallet2.patch
Patch8: subversion-1.7.4-sqlitever.patch
BuildRequires: autoconf, libtool, python, python-devel, texinfo, which
BuildRequires: %{dbdevel} >= 4.1.25, swig >= 1.3.24, gettext
BuildRequires: apr-devel >= 1.3.0, apr-util-devel >= 1.3.0
BuildRequires: neon-devel >= 0:0.24.7-1, cyrus-sasl-devel
BuildRequires: sqlite-devel >= 3.4.0, file-devel, systemd-units
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Provides: svn = %{version}-%{release}
Requires: subversion-libs%{?_isa} = %{version}-%{release}
Requires(post): systemd-sysv, /sbin/chkconfig

%define __perl_requires %{SOURCE3}

# Put Python bindings in site-packages
%define swigdirs swig_pydir=%{python_sitearch}/libsvn swig_pydir_extra=%{python_sitearch}/svn

%description
Subversion is a concurrent version control system which enables one
or more users to collaborate in developing and maintaining a
hierarchy of files and directories while keeping a history of all
changes.  Subversion only stores the differences between versions,
instead of every complete file.  Subversion is intended to be a
compelling replacement for CVS.

%package libs
Group: Development/Tools
Summary: Libraries for Subversion Version Control system
# APR 1.3.x interfaces are required
Conflicts: apr%{?_isa} < 1.3.0

%description libs
The subversion-libs package includes the essential shared libraries
used by the Subversion version control tools.

%package python
Group: Development/Libraries
Summary: Python bindings for Subversion Version Control system

%description python
The subversion-python package includes the Python bindings to the
Subversion libraries.

%package devel
Group: Development/Tools
Summary: Development package for the Subversion libraries
Requires: subversion%{?_isa} = %{version}-%{release}
Requires: apr-devel%{?_isa}, apr-util-devel%{?_isa}

%description devel
The subversion-devel package includes the libraries and include files
for developers interacting with the subversion package.

%package gnome
Group: Development/Tools
Summary: GNOME Keyring support for Subversion
Requires: subversion%{?_isa} = %{version}-%{release}
BuildRequires: libgnome-keyring-devel, dbus-devel

%description gnome
The subversion-gnome package adds support for storing Subversion
passwords in the GNOME Keyring.

%if %{with_kwallet}
%package kde
Group: Development/Tools
Summary: KDE Wallet support for Subversion
Requires: subversion%{?_isa} = %{version}-%{release}
BuildRequires: kdelibs-devel >= 4.0.0

%description kde
The subversion-kde package adds support for storing Subversion
passwords in the KDE Wallet.
%endif

%package -n mod_dav_svn
Group: System Environment/Daemons
Summary: Apache httpd module for Subversion server
Requires: httpd-mmn = %{_httpd_mmn}
Requires: subversion-libs%{?_isa} = %{version}-%{release}
BuildRequires: httpd-devel >= 2.0.45

%description -n mod_dav_svn
The mod_dav_svn package allows access to a Subversion repository
using HTTP, via the Apache httpd server.

%package perl
Group: Development/Libraries
Summary: Perl bindings to the Subversion libraries
BuildRequires: perl-devel >= 2:5.8.0, perl(ExtUtils::MakeMaker)
BuildRequires: perl(Test::More), perl(ExtUtils::Embed)
Requires: %(eval `perl -V:version`; echo "perl(:MODULE_COMPAT_$version)")
Requires: subversion%{?_isa} = %{version}-%{release}

%description perl
This package includes the Perl bindings to the Subversion libraries.

%if %{with_java}
%package javahl
Group: Development/Libraries
Summary: JNI bindings to the Subversion libraries
Requires: subversion%{?_isa} = %{version}-%{release}
BuildRequires: java-devel-openjdk
# JAR repacking requires both zip and unzip in the buildroot
BuildRequires: zip, unzip
# For the tests
BuildRequires: junit

%description javahl
This package includes the JNI bindings to the Subversion libraries.
%endif

%package ruby
Group: Development/Libraries
Summary: Ruby bindings to the Subversion libraries
BuildRequires: ruby-devel >= 1.9.1, ruby >= 1.9.1
Requires: subversion%{?_isa} = %{version}-%{release}
Conflicts: ruby-libs%{?_isa} < 1.8.2
### this should not be hard-coded!
Requires: ruby(abi) = 1.9.1

%description ruby
This package includes the Ruby bindings to the Subversion libraries.

%package tools
Group: Development/Tools
Summary: Supplementary tools for Subversion
Requires: subversion%{?_isa} = %{version}-%{release}

%description tools
This package includes supplementary tools for use with Subversion.

%prep
%setup -q
%patch1 -p1 -b .rpath
%patch2 -p1 -b .pie
%patch3 -p1 -b .kwallet
%patch4 -p1 -b .ruby
%patch5 -p1 -b .hashorder
%patch6 -p1 -b .httpd24
%patch7 -p1 -b .kwallet2
%patch8 -p1 -b .sqlitever

%build
# Regenerate the buildsystem, so that:
#  1) patches applied to configure.in take effect
#  2) the swig bindings are regenerated using the system swig
# (2) is not ideal since typically upstream test with a different
# swig version
# This PATH order makes the fugly test for libtoolize work...
PATH=/usr/bin:$PATH ./autogen.sh --release

# fix shebang lines, #111498
perl -pi -e 's|/usr/bin/env perl -w|/usr/bin/perl -w|' tools/hook-scripts/*.pl.in

# override weird -shrext from ruby
export svn_cv_ruby_link="%{__cc} -shared"
export svn_cv_ruby_sitedir_libsuffix=""
export svn_cv_ruby_sitedir_archsuffix=""

%ifarch sparc64
sed -i 's/-fpie/-fPIE/' Makefile.in
%endif

export CC=gcc CXX=g++ JAVA_HOME=%{jdk_path} CFLAGS="$RPM_OPT_FLAGS"
%configure --with-apr=%{_prefix} --with-apr-util=%{_prefix} \
        --with-swig --with-neon=%{_prefix} \
        --with-ruby-sitedir=%{ruby_vendorarchdir} \
        --with-apxs=%{_httpd_apxs} --disable-mod-activation \
        --disable-static --with-sasl=%{_prefix} \
        --disable-neon-version-check \
        --with-gnome-keyring \
%if %{with_java}
        --enable-javahl \
        --with-junit=%{_prefix}/share/java/junit.jar \
%endif
%if %{with_kwallet}
        --with-kwallet \
%endif
        --with-berkeley-db || (cat config.log; exit 1)
make %{?_smp_mflags} all tools
make swig-py swig-py-lib %{swigdirs}
make swig-pl swig-pl-lib swig-rb swig-rb-lib
%if %{with_java}
# javahl-javah does not parallel-make with javahl
#make javahl-java javahl-javah
make javahl
%endif

%install
rm -rf ${RPM_BUILD_ROOT}
make install install-swig-py install-swig-pl-lib install-swig-rb \
        DESTDIR=$RPM_BUILD_ROOT %{swigdirs}
%if %{with_java}
make install-javahl-java install-javahl-lib javahl_javadir=%{_javadir} DESTDIR=$RPM_BUILD_ROOT
%endif

make pure_vendor_install -C subversion/bindings/swig/perl/native \
        PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
install -m 755 -d ${RPM_BUILD_ROOT}%{_sysconfdir}/subversion

mkdir -p ${RPM_BUILD_ROOT}{%{_httpd_modconfdir},%{_httpd_confdir}}

%if "%{_httpd_modconfdir}" == "%{_httpd_confdir}"
# httpd <= 2.2.x
install -p -m 644 %{SOURCE1} ${RPM_BUILD_ROOT}%{_httpd_confdir}
%else
sed -n /^LoadModule/p %{SOURCE1} > 10-subversion.conf
sed    /^LoadModule/d %{SOURCE1} > example.conf
touch -r %{SOURCE1} 10-subversion.conf example.conf
install -p -m 644 10-subversion.conf ${RPM_BUILD_ROOT}%{_httpd_modconfdir}
%endif

# Remove unpackaged files
rm -rf ${RPM_BUILD_ROOT}%{_includedir}/subversion-*/*.txt \
       ${RPM_BUILD_ROOT}%{python_sitearch}/*/*.{a,la}

# The SVN build system is broken w.r.t. DSO support; it treats
# normal libraries as DSOs and puts them in $libdir, whereas they
# should go in some subdir somewhere, and be linked using -module,
# etc.  So, forcibly nuke the .so's for libsvn_auth_{gnome,kde},
# since nothing should ever link against them directly.
rm -f ${RPM_BUILD_ROOT}%{_libdir}/libsvn_auth_*.so

# remove stuff produced with Perl modules
find $RPM_BUILD_ROOT -type f \
    -a \( -name .packlist -o \( -name '*.bs' -a -empty \) \) \
    -print0 | xargs -0 rm -f

# make Perl modules writable so they get stripped
find $RPM_BUILD_ROOT%{_libdir}/perl5 -type f -perm 555 -print0 |
        xargs -0 chmod 755

# unnecessary libraries for swig bindings
rm -f ${RPM_BUILD_ROOT}%{_libdir}/libsvn_swig_*.{so,la,a}

# Remove unnecessary ruby libraries
rm -f ${RPM_BUILD_ROOT}%{ruby_sitearch}/svn/ext/*.*a

# Trim what goes in docdir
rm -rf tools/*/*.in

# Install psvn for emacs and xemacs
for f in emacs/site-lisp xemacs/site-packages/lisp; do
  install -m 755 -d ${RPM_BUILD_ROOT}%{_datadir}/$f
  install -m 644 $RPM_SOURCE_DIR/psvn.el ${RPM_BUILD_ROOT}%{_datadir}/$f
done

install -m 644 $RPM_SOURCE_DIR/psvn-init.el \
        ${RPM_BUILD_ROOT}%{_datadir}/emacs/site-lisp

# Rename authz_svn INSTALL doc for docdir
ln -f subversion/mod_authz_svn/INSTALL mod_authz_svn-INSTALL

# Trim exported dependencies to APR libraries only:
sed -i "/^dependency_libs/{
     s, -l[^ ']*, ,g;
     s, -L[^ ']*, ,g;
     s,%{_libdir}/lib[^a][^p][^r][^ ']*.la, ,g;
     }"  $RPM_BUILD_ROOT%{_libdir}/*.la

# Install bash completion
install -Dpm 644 tools/client-side/bash_completion \
        $RPM_BUILD_ROOT%{_sysconfdir}/bash_completion.d/%{name}

# Install svnserve bits
mkdir -p %{buildroot}%{_unitdir} \
      %{buildroot}%{_localstatedir}/run/svnserve \
      %{buildroot}%{_sysconfdir}/tmpfiles.d \
      %{buildroot}%{_sysconfdir}/sysconfig

install -p -m 644 $RPM_SOURCE_DIR/svnserve.service \
        %{buildroot}%{_unitdir}/svnserve.service
install -p -m 644 $RPM_SOURCE_DIR/svnserve.tmpfiles \
        %{buildroot}%{_sysconfdir}/tmpfiles.d/svnserve.conf
install -p -m 644 $RPM_SOURCE_DIR/svnserve.sysconf \
        %{buildroot}%{_sysconfdir}/sysconfig/svnserve

# Install tools ex diff*
make install-tools DESTDIR=$RPM_BUILD_ROOT toolsdir=%{_bindir}
rm -f $RPM_BUILD_ROOT%{_bindir}/diff*

for f in svn-populate-node-origins-index svn-rep-sharing-stats svnauthz-validate svnmucc svnraisetreeconflict; do
    echo %{_bindir}/$f
done | tee tools.files | sed 's/^/%%exclude /' > exclude.tools.files

%find_lang %{name}

cat %{name}.lang exclude.tools.files >> %{name}.files

%if %{make_check}
%check
export LANG=C LC_ALL=C
export LD_LIBRARY_PATH=$RPM_BUILD_ROOT%{_libdir}
#export MALLOC_PERTURB_=171 MALLOC_CHECK_=3
#export LIBC_FATAL_STDERR_=1
if ! make check check-swig-pl check-swig-py CLEANUP=yes; then
   : Test suite failure.
   cat fails.log
   exit 1
fi
# check-swig-rb omitted: it runs svnserve
%if %{with_java}
make check-javahl
%endif
%endif

%clean
rm -rf ${RPM_BUILD_ROOT}

%post
if [ $1 -eq 1 ] ; then 
    # Initial installation 
    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
fi

%preun
if [ $1 = 0 ]; then
    # Package removal, not upgrade
    /bin/systemctl --no-reload disable svnserve.service > /dev/null 2>&1 || :
    /bin/systemctl stop svnserve.service > /dev/null 2>&1 || :
fi

%postun
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
if [ $1 -ge 1 ] ; then
    # Package upgrade, not uninstall
    /bin/systemctl try-restart svnserve.service >/dev/null 2>&1 || :
fi

%triggerun -- subversion < 1.7.3-2
/usr/bin/systemd-sysv-convert --save svnserve >/dev/null 2>&1 ||:
/sbin/chkconfig --del svnserve >/dev/null 2>&1 || :
/bin/systemctl try-restart svnserve.service >/dev/null 2>&1 || :

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%post perl -p /sbin/ldconfig

%postun perl -p /sbin/ldconfig

%post ruby -p /sbin/ldconfig

%postun ruby -p /sbin/ldconfig

%if %{with_java}
%post javahl -p /sbin/ldconfig

%postun javahl -p /sbin/ldconfig
%endif

%files -f %{name}.files
%defattr(-,root,root)
%doc BUGS COMMITTERS LICENSE NOTICE INSTALL README CHANGES
%doc tools/hook-scripts tools/backup tools/bdb tools/examples tools/xslt
%doc mod_authz_svn-INSTALL
%{_bindir}/*
%{_mandir}/man*/*
%{_datadir}/emacs/site-lisp/*.el
%{_datadir}/xemacs/site-packages/lisp/*.el
%{_sysconfdir}/bash_completion.d
%config(noreplace) %{_sysconfdir}/sysconfig/svnserve
%dir %{_sysconfdir}/subversion
%exclude %{_mandir}/man*/*::*
%{_unitdir}/*.service
%{_localstatedir}/run/svnserve
%{_sysconfdir}/tmpfiles.d/svnserve.conf

%files tools -f tools.files
%defattr(-,root,root)

%files libs
%defattr(-,root,root)
%doc LICENSE NOTICE
%{_libdir}/libsvn_*.so.*
%exclude %{_libdir}/libsvn_swig_perl*
%exclude %{_libdir}/libsvn_swig_ruby*
%if %{with_kwallet}
%exclude %{_libdir}/libsvn_auth_kwallet*
%endif
%exclude %{_libdir}/libsvn_auth_gnome*

%files python
%defattr(-,root,root)
%{python_sitearch}/svn
%{python_sitearch}/libsvn

%files gnome
%defattr(-,root,root)
%{_libdir}/libsvn_auth_gnome_keyring-*.so.*

%if %{with_kwallet}
%files kde
%defattr(-,root,root)
%{_libdir}/libsvn_auth_kwallet-*.so.*
%endif

%files devel
%defattr(-,root,root)
%{_includedir}/subversion-1
%{_libdir}/libsvn*.*a
%{_libdir}/libsvn*.so
%exclude %{_libdir}/libsvn_swig_perl*
%if %{with_java}
%exclude %{_libdir}/libsvnjavahl-1.*
%endif

%files -n mod_dav_svn
%defattr(-,root,root)
%config(noreplace) %{_httpd_modconfdir}/*.conf
%{_libdir}/httpd/modules/mod_*.so
%if "%{_httpd_modconfdir}" != "%{_httpd_confdir}"
%doc example.conf
%endif

%files perl
%defattr(-,root,root,-)
%{perl_vendorarch}/auto/SVN
%{perl_vendorarch}/SVN
%{_libdir}/libsvn_swig_perl*
%{_mandir}/man*/*::*

%files ruby
%defattr(-,root,root,-)
%{_libdir}/libsvn_swig_ruby*
%{ruby_vendorarchdir}/svn

%if %{with_java}
%files javahl
%defattr(-,root,root,-)
%{_libdir}/libsvnjavahl-1.*
%{_javadir}/svn-javahl.jar
%endif

%changelog
* Sat May 12 2012 Remi Collet <RPMS@FamilleCollet.com> - 1.7.4-6
- rebuild for remi repo and httpd 2.4

* Tue Apr 24 2012 Joe Orton <jorton@redhat.com> - 1.7.4-6
- drop strict sqlite version requirement (#815396)

* Mon Apr 23 2012 Joe Orton <jorton@redhat.com> - 1.7.4-5
- switch to libdb-devel (#814090)

* Thu Apr 19 2012 Joe Orton <jorton@redhat.com> - 1.7.4-4
- adapt for conf.modules.d with httpd 2.4
- add possible workaround for kwallet crasher (#810861)

* Fri Mar 30 2012 Joe Orton <jorton@redhat.com> - 1.7.4-3
- re-enable test suite

* Fri Mar 30 2012 Joe Orton <jorton@redhat.com> - 1.7.4-2
- fix build with httpd 2.4

* Mon Mar 12 2012 Joe Orton <jorton@redhat.com> - 1.7.4-1
- update to 1.7.4
- fix build with httpd 2.4

* Thu Mar  1 2012 Joe Orton <jorton@redhat.com> - 1.7.3-7
- re-enable kwallet (#791031)

* Wed Feb 29 2012 Joe Orton <jorton@redhat.com> - 1.7.3-6
- update psvn

* Wed Feb 29 2012 Joe Orton <jorton@redhat.com> - 1.7.3-5
- add tools subpackage (#648015)

* Tue Feb 28 2012 Joe Orton <jorton@redhat.com> - 1.7.3-4
- trim contents of doc dic (#746433)

* Tue Feb 28 2012 Joe Orton <jorton@redhat.com> - 1.7.3-3
- re-enable test suite

* Tue Feb 28 2012 Joe Orton <jorton@redhat.com> - 1.7.3-2
- add upstream test suite fixes for APR hash change (r1293602, r1293811)
- use ruby vendorlib directory (#798203)
- convert svnserve to systemd (#754074)

* Mon Feb 13 2012 Joe Orton <jorton@redhat.com> - 1.7.3-1
- update to 1.7.3
- ship, enable mod_dontdothat

* Mon Feb 13 2012 Joe Orton <jorton@redhat.com> - 1.7.2-2
- require ruby 1.9.1 abi

* Thu Feb  9 2012 Joe Orton <jorton@redhat.com> - 1.7.2-1
- update to 1.7.2
- add Vincent Batts' Ruby 1.9 fixes from dev@

* Sun Feb  5 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 1.7.1-3
- fix gnome-keyring build deps 

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Nov 28 2011 Joe Orton <jorton@redhat.com> - 1.7.1-1
- update to 1.7.1
- (temporarily) disable failing kwallet support

* Sun Nov 27 2011 Ville Skyttä <ville.skytta@iki.fi> - 1.7.0-3
- Build with libmagic support.

* Sat Oct 15 2011 Ville Skyttä <ville.skytta@iki.fi> - 1.7.0-2
- Fix apr Conflicts syntax in -libs.
- Fix obsolete chown syntax in subversion.conf.
- Fix use of spaces vs tabs in specfile.

* Wed Oct 12 2011 Joe Orton <jorton@redhat.com> - 1.7.0-1
- update to 1.7.0
- drop svn2cl (no longer shipped in upstream tarball)

* Thu Jul 21 2011 Petr Sabata <contyk@redhat.com> - 1.6.17-5
- Perl mass rebuild

* Wed Jul 20 2011 Joe Orton <jorton@redhat.com> - 1.6.17-4
- run javahl tests (Blair Zajac, #723338)

* Wed Jul 20 2011 Joe Orton <jorton@redhat.com> - 1.6.17-3
- split out python subpackage

* Wed Jun 15 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.6.17-2
- Perl mass rebuild
- change cflags in Makefile.PL to work with Perl 5.14.1

* Thu Jun  2 2011 Joe Orton <jorton@redhat.com> - 1.6.17-1
- update to 1.6.17 (#709952)

* Fri Mar  4 2011 Joe Orton <jorton@redhat.com> - 1.6.16-1
- update to 1.6.16 (#682203)
- tweak arch-specific requires

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Nov 28 2010 Joe Orton <jorton@redhat.com> - 1.6.15-1
- update to 1.6.15

* Sun Oct 17 2010 Ville Skyttä <ville.skytta@iki.fi> - 1.6.13-3
- Make name based dependencies arch qualified where appropriate (#643714).

* Tue Oct 12 2010 Joe Orton <jorton@redhat.com> - 1.6.13-2
- trim tools/buildbot, tools/dist from docdir

* Tue Oct  5 2010 Joe Orton <jorton@redhat.com> - 1.6.13-1
- update to 1.6.13

* Tue Sep  7 2010 Joe Orton <jorton@redhat.com> - 1.6.12-5
- add svnserve init script
- split out -libs subpackage

* Fri Sep  3 2010 Joe Orton <jorton@redhat.com> - 1.6.12-4
- restore PIE support

* Sat Jul 24 2010 David Malcolm <dmalcolm@redhat.com> - 1.6.12-3
- for now, disable python cases that fail against python 2.7 (patch 9)

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 1.6.12-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Wed Jul  7 2010 Joe Orton <jorton@redhat.com> - 1.6.12-1
- update to 1.6.12 (#586629)
- fix comments in subversion.conf (#551484)

* Wed Jun 02 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.6.11-2
- Mass rebuild with perl-5.12.0

* Sat Apr 17 2010 Joe Orton <jorton@redhat.com> - 1.6.11-1
- update to 1.6.11

* Sat Feb 13 2010 Joe Orton <jorton@redhat.com> - 1.6.9-2
- fix detection of libkdecore

* Mon Feb  8 2010 Joe Orton <jorton@redhat.com> - 1.6.9-1
- update to 1.6.9 (#561810)
- fix comments in subversion.conf (#551484)
- update to psvn.el r40299

* Mon Jan 25 2010 Ville Skyttä <ville.skytta@iki.fi> - 1.6.6-5
- Include svn2cl and its man page only in the -svn2cl subpackage (#558598).
- Do not include bash completion in docs, it's installed.

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.6.6-4
- rebuild against perl 5.10.1

* Thu Nov 26 2009 Joe Orton <jorton@redhat.com> - 1.6.6-3
- rebuild for new db4
- trim libsvn_* from dependency_libs in *.la

* Wed Nov 25 2009 Kevin Kofler <Kevin@tigcc.ticalc.org> 1.6.6-2
- rebuild for Qt 4.6.0 RC1 in F13 (was built against Beta 1 with unstable ABI)

* Sun Nov  8 2009 Joe Orton <jorton@redhat.com> - 1.6.6-1
- update to 1.6.6

* Mon Nov  2 2009 Ville Skyttä <ville.skytta@iki.fi> - 1.6.5-3
- Apply svn2cl upstream patch to fix newline issues with libxml2 2.7.4+,
  see http://bugs.debian.org/546990 for details.

* Sat Sep 19 2009 Ville Skyttä <ville.skytta@iki.fi> - 1.6.5-2
- Ship svn2cl and bash completion (#496456).
- Add %%defattr to -gnome and -kde.

* Sun Aug 23 2009 Joe Orton <jorton@redhat.com> 1.6.5-1
- update to 1.6.5

* Tue Aug 18 2009 Joe Orton <jorton@redhat.com> 1.6.4-4
- rebuild

* Tue Aug 11 2009 Ville Skyttä <ville.skytta@iki.fi> - 1.6.4-3
- Use bzipped upstream tarball.

* Fri Aug  7 2009 Joe Orton <jorton@redhat.com> 1.6.4-2
- update to 1.6.4

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul 23 2009 Joe Orton <jorton@redhat.com> 1.6.3-2
- remove -devel dependency on -gnome, -kde (#513313)

* Tue Jun 23 2009 Joe Orton <jorton@redhat.com> 1.6.3-1
- update to 1.6.3

* Sun Jun 14 2009 Joe Orton <jorton@redhat.com> 1.6.2-3
- add -gnome, -kde subpackages

* Mon Jun  1 2009 Joe Orton <jorton@redhat.com> 1.6.2-2
- enable KWallet, gnome-keyring support

* Fri May 15 2009 Joe Orton <jorton@redhat.com> 1.6.2-1
- update to 1.6.2

* Wed Apr 15 2009 Joe Orton <jorton@redhat.com> 1.6.1-4
- really disable PIE

* Tue Apr 14 2009 Joe Orton <jorton@redhat.com> 1.6.1-3
- update to 1.6.1; disable PIE patch for the time being

* Tue Mar 31 2009 Joe Orton <jorton@redhat.com> 1.6.0-3
- BR sqlite-devel

* Tue Mar 31 2009 Joe Orton <jorton@redhat.com> 1.6.0-1
- update to 1.6.0

* Thu Mar 12 2009 Dennis Gilmore <dennis@ausil.us> - 1.5.6-4
- use -fPIE on sparc64

* Mon Mar  9 2009 Joe Orton <jorton@redhat.com> 1.5.6-3
- update to 1.5.6
- autoload psvn (#238491, Tom Tromey)
- regenerate swig bindings (#480503)
- fix build with libtool 2.2 (#469524)

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Jan 30 2009 Joe Orton <jorton@redhat.com> 1.5.5-5
- update to 1.5.5

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 1.5.4-4
- Rebuild for Python 2.6

* Mon Oct 27 2008 Joe Orton <jorton@redhat.com> 1.5.4-3
- update to 1.5.4

* Mon Oct 13 2008 Joe Orton <jorton@redhat.com> 1.5.3-3
- fix build

* Mon Oct 13 2008 Joe Orton <jorton@redhat.com> 1.5.3-2
- update to 1.5.3 (#466674)
- update psvn.el to r33557

* Tue Sep 30 2008 Joe Orton <jorton@redhat.com> 1.5.2-3
- enable SASL support (#464267)

* Fri Sep 12 2008 Joe Orton <jorton@redhat.com> 1.5.2-2
- update to 1.5.2

* Mon Jul 28 2008 Joe Orton <jorton@redhat.com> 1.5.1-2
- update to 1.5.1
- require suitable APR

* Thu Jul 10 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.5.0-8
- rebuild against new db4-4.7

* Thu Jul  3 2008 Joe Orton <jorton@redhat.com> 1.5.0-7
- add svnmerge and wcgrep to docdir (Edward Rudd, #451932)
- drop neon version overrides

* Wed Jul  2 2008 Joe Orton <jorton@redhat.com> 1.5.0-6
- build with OpenJDK

* Wed Jul  2 2008 Joe Orton <jorton@redhat.com> 1.5.0-5
- fix files list

* Wed Jul  2 2008 Joe Orton <jorton@redhat.com> 1.5.0-4
- swig-perl test suite fix for Perl 5.10 (upstream r31546)

* Tue Jul  1 2008 Joe Orton <jorton@redhat.com> 1.5.0-3
- attempt build without java bits

* Thu Jun 26 2008 Joe Orton <jorton@redhat.com> 1.5.0-2
- update to 1.5.0

* Mon Mar  3 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.4.6-7
- tests are randomly failing, unrelated to new perl, disabled tests

* Mon Mar  3 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.4.6-6
- rebuild for new perl (again)

* Thu Feb 21 2008 Lubomir Kundrak <lkundrak@redhat.com> 1.4.6-5
- Correct install location of java stuff (#433295)

* Wed Feb  6 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.4.6-4
- BR perl(ExtUtils::Embed)

* Tue Feb  5 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.4.6-3
- rebuild for new perl

* Fri Dec 21 2007 Joe Orton <jorton@redhat.com> 1.4.6-2
- update to 1.4.6

* Mon Dec 10 2007 Warren Togami <wtogami@redhat.com> 1.4.4-11
- temporarily disable test suite

* Thu Dec  6 2007 Joe Orton <jorton@redhat.com> 1.4.4-10
- fix build with swig 1.3.33 (patch by Torsten Landschoff)

* Wed Dec  5 2007 Joe Orton <jorton@redhat.com> 1.4.4-9
- rebuild for OpenLDAP soname bump

* Tue Sep  4 2007 Joe Orton <jorton@redhat.com> 1.4.4-8
- update to psvn.el r26383 from upstream

* Sun Sep  2 2007 Joe Orton <jorton@redhat.com> 1.4.4-7
- rebuild for fixed 32-bit APR 

* Thu Aug 30 2007 Joe Orton <jorton@redhat.com> 1.4.4-6
- clarify License tag; re-enable test suite

* Thu Aug 23 2007 Joe Orton <jorton@redhat.com> 1.4.4-5
- rebuild for neon 0.27

* Wed Aug 22 2007 Joe Orton <jorton@redhat.com> 1.4.4-4
- trim dependencies from .la files
- detabify spec file
- test suite disabled to ease stress on builders

* Wed Aug  8 2007 Joe Orton <jorton@redhat.com> 1.4.4-3
- fix build with new glibc open()-as-macro
- build all swig code in %%build, not %%install
- BuildRequire perl(Test::More), perl(ExtUtils::MakeMaker)

* Tue Jul  3 2007 Joe Orton <jorton@redhat.com> 1.4.4-2
- update to 1.4.4
- add Provides: svn (#245087)
- fix without-java build (Lennert Buytenhek, #245467)

* Wed Apr 11 2007 Joe Orton <jorton@redhat.com> 1.4.3-5
- fix version of apr/apr-util in BR (#216181)

* Thu Mar 29 2007 Joe Orton <jorton@redhat.com> 1.4.3-4
- fix javahl compile failure

* Mon Jan 29 2007 Joe Orton <jorton@redhat.com> 1.4.3-3
- update to 1.4.3 (#228691)
- remove trailing dot from Summary
- use current preferred standard BuildRoot
- add post/postun ldconfig scriptlets for -ruby and -javahl

* Fri Dec  8 2006 Joe Orton <jorton@redhat.com> 1.4.2-5
- fix use of python_sitearch

* Thu Dec  7 2006 Jeremy Katz <katzj@redhat.com> - 1.4.2-4
- rebuild against python 2.5
- follow python packaging guidelines

* Wed Nov  8 2006 Joe Orton <jorton@redhat.com> 1.4.2-3
- update to 1.4.2

* Mon Sep 11 2006 Joe Orton <jorton@redhat.com> 1.4.0-2
- update to 1.4.0

* Thu Jul 13 2006 Joe Orton <jorton@redhat.com> 1.3.2-6
- fix ruby packaging (#191611)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> 1.3.2-5.1
- rebuild

* Wed Jun  7 2006 Joe Orton <jorton@redhat.com> 1.3.2-5
- disable test suite

* Wed Jun  7 2006 Joe Orton <jorton@redhat.com> 1.3.2-4
- BR gettext

* Fri Jun  2 2006 Joe Orton <jorton@redhat.com> 1.3.2-3
- re-enable test suite

* Fri Jun  2 2006 Joe Orton <jorton@redhat.com> 1.3.2-2
- update to 1.3.2
- fix Ruby sitelibdir (Garrick Staples, #191611)
- own /etc/subversion (#189071)
- update to psvn.el r19857

* Thu Apr  6 2006 Joe Orton <jorton@redhat.com> 1.3.1-4
- move libsvn_swig_ruby* back to subversion-ruby

* Tue Apr  4 2006 Joe Orton <jorton@redhat.com> 1.3.1-3
- update to 1.3.1
- update to psvn.el r19138 (Stefan Reichoer)
- build -java on s390 again

* Thu Feb 16 2006 Florian La Roche <laroche@redhat.com> - 1.3.0-5
- do not package libs within subversion-ruby, these are already
  available via the main package

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.3.0-4.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.3.0-4.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Tue Jan 31 2006 Joe Orton <jorton@redhat.com> 1.3.0-4
- run check-swig-py in %%check (#178448)
- relax JDK requirement (Kenneth Porter, #177367)

* Tue Jan 31 2006 Joe Orton <jorton@redhat.com> 1.3.0-3
- rebuild for neon 0.25

* Wed Jan  4 2006 Joe Orton <jorton@redhat.com> 1.3.0-2
- update to 1.3.0 (#176833)
- update to psvn.el r17921 Stefan Reichoer

* Mon Dec 12 2005 Joe Orton <jorton@redhat.com> 1.2.3-6
- fix ownership of libsvnjavahl.* (#175289)
- try building javahl on ia64/ppc64 again

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Fri Dec  2 2005 Joe Orton <jorton@redhat.com> 1.2.3-5
- rebuild for httpd-2.2/apr-1.2/apr-util-1.2

* Thu Nov 10 2005 Tomas Mraz <tmraz@redhat.com> 1.2.3-4
- rebuilt against new openssl

* Thu Sep  8 2005 Joe Orton <jorton@redhat.com> 1.2.3-3
- update to 1.2.3
- update to psvn.el r16070 from Stefan Reichoer
- merge subversion.conf changes from RHEL4
- merge filter-requires.sh changes from FC4 updates

* Mon Aug  8 2005 Joe Orton <jorton@redhat.com> 1.2.1-4
- add BR for which (#161015)

* Fri Jul 22 2005 Joe Orton <jorton@redhat.com> 1.2.0-3
- update to 1.2.1
- fix BuildRequires for ruby and apr-util (#163126)
- drop static library archives

* Wed May 25 2005 Joe Orton <jorton@redhat.com> 1.2.0-2
- disable java on all but x86, x86_64, ppc (#158719)

* Tue May 24 2005 Joe Orton <jorton@redhat.com> 1.2.0-1
- update to 1.2.0; add ruby subpackage

* Wed Apr 13 2005 Joe Orton <jorton@redhat.com> 1.1.4-3
- enable java subpackage again
- tweak subversion.conf comments

* Sun Apr  3 2005 Joe Orton <jorton@redhat.com> 1.1.4-2
- update to 1.1.4

* Tue Mar 22 2005 Joe Orton <jorton@redhat.com> 1.1.3-8
- further swig bindings fix (upstream via Max Bowsher, #151798)
- fix perl File::Path dependency in filter-requires.sh

* Tue Mar 22 2005 Joe Orton <jorton@redhat.com> 1.1.3-7
- restore swig bindings support (from upstream via Max Bowsher, #141343)
- tweak SELinux commentary in default subversion.conf

* Wed Mar  9 2005 Joe Orton <jorton@redhat.com> 1.1.3-6
- fix svn_load_dirs File::Path version requirement

* Tue Mar  8 2005 Joe Orton <jorton@redhat.com> 1.1.3-5
- add -java subpackage for javahl libraries (Anthony Green, #116202)

* Fri Mar  4 2005 Joe Orton <jorton@redhat.com> 1.1.3-4
- rebuild

* Tue Feb 15 2005 Joe Orton <jorton@redhat.com> 1.1.3-3
- run test suite in C locale (#146125)
- adjust -pie patch for build.conf naming upstream

* Wed Jan 19 2005 Joe Orton <jorton@redhat.com> 1.1.3-2
- rebuild to pick up db-4.3 properly; don't ignore test failures

* Sun Jan 16 2005 Joe Orton <jorton@redhat.com> 1.1.3-1
- update to 1.1.3 (#145236)
- fix python bindings location on x86_64 (#143522)

* Mon Jan 10 2005 Joe Orton <jorton@redhat.com> 1.1.2-3
- update to 1.1.2
- disable swig bindings due to incompatible swig version

* Wed Nov 24 2004 Joe Orton <jorton@redhat.com> 1.1.1-5
- update subversion.conf examples to be SELinux-friendly

* Thu Nov 11 2004 Jeff Johnson <jbj@jbj.org> 1.1.1-4
- rebuild against db-4.3.21.
- x86_64: don't fail "make check" while diagnosing db-4.3.21 upgrade.

* Mon Nov  8 2004 Jeremy Katz <katzj@redhat.com> - 1.1.1-3
- rebuild against python 2.4

* Mon Oct 25 2004 Joe Orton <jorton@redhat.com> 1.1.1-2
- update to 1.1.1
- update -pie patch to address #134786

* Mon Oct  4 2004 Joe Orton <jorton@redhat.com> 1.1.0-5
- use pure_vendor_install to fix Perl modules
- use %%find_lang to package translations (Axel Thimm)

* Thu Sep 30 2004 Joe Orton <jorton@redhat.com> 1.1.0-4
- don't use parallel make for swig-py

* Thu Sep 30 2004 Joe Orton <jorton@redhat.com> 1.1.0-3
- BuildRequire newest swig for "swig -ldflags" fix

* Thu Sep 30 2004 Joe Orton <jorton@redhat.com> 1.1.0-2
- fix swig bindings build on x86_64

* Thu Sep 30 2004 Joe Orton <jorton@redhat.com> 1.1.0-1
- update to 1.1.0

* Thu Sep 23 2004 Joe Orton <jorton@redhat.com> 1.0.8-2
- update to 1.0.8
- remove -neonver patch
- update psvn.el to 11062

* Mon Aug 23 2004 Joe Orton <jorton@redhat.com> 1.0.6-3
- add svn_load_dirs.pl to docdir (#128338)
- add psvn.el (#128356)

* Thu Jul 22 2004 Joe Orton <jorton@redhat.com> 1.0.6-2
- rebuild

* Tue Jul 20 2004 Joe Orton <jorton@redhat.com> 1.0.6-1
- update to 1.0.6
- allow build against neon 0.24.*

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Jun 10 2004 Joe Orton <jorton@redhat.com> 1.0.5-1
- update to 1.0.5

* Mon Jun  7 2004 Joe Orton <jorton@redhat.com> 1.0.4-2
- add ra_svn security fix for CVE CAN-2004-0413 (Ben Reser)

* Fri May 28 2004 Joe Orton <jorton@redhat.com> 1.0.4-1.1
- rebuild for new swig

* Sat May 22 2004 Joe Orton <jorton@redhat.com> 1.0.4-1
- update to 1.0.4

* Fri May 21 2004 Joe Orton <jorton@redhat.com> 1.0.3-2
- build /usr/bin/* as PIEs
- add fix for libsvn_client symbol namespace violation (r9608)

* Wed May 19 2004 Joe Orton <jorton@redhat.com> 1.0.3-1
- update to 1.0.3

* Sun May 16 2004 Joe Orton <jorton@redhat.com> 1.0.2-3
- add ldconfig invocations for -perl post/postun (Ville Skyttä)

* Tue May  4 2004 Joe Orton <jorton@redhat.com> 1.0.2-2
- add perl MODULE_COMPAT requirement for -perl subpackage
- move perl man pages into -perl subpackage
- clean up -perl installation and dependencies (Ville Skyttä, #123045)

* Mon Apr 19 2004 Joe Orton <jorton@redhat.com> 1.0.2-1
- update to 1.0.2

* Fri Mar 12 2004 Joe Orton <jorton@redhat.com> 1.0.1-1
- update to 1.0.1; cvs2svn no longer included

* Fri Mar 12 2004 Joe Orton <jorton@redhat.com> 1.0.0-3
- add -perl subpackage for Perl bindings (steve@silug.org)
- include mod_authz_svn INSTALL file

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com> 1.0.0-2.1
- rebuilt

* Wed Feb 25 2004 Joe Orton <jorton@redhat.com> 1.0.0-2
- add fix for lack of apr_dir_read ordering guarantee (Philip Martin)
- enable compression in ra_dav by default (Tobias Ringström)

* Mon Feb 23 2004 Joe Orton <jorton@redhat.com> 1.0.0-1
- update to one-dot-oh

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com> 0.37.0-2
- rebuilt

* Sat Jan 24 2004 Joe Orton <jorton@redhat.com> 0.37.0-1
- update to 0.37.0

* Tue Jan 13 2004 Joe Orton <jorton@redhat.com> 0.36.0-1
- update to 0.36.0

* Thu Jan  8 2004 Joe Orton <jorton@redhat.com> 0.35.1-1
- update to 0.35.1
- fix shebang lines in hook scripts (#111498)

* Sat Dec 13 2003 Jeff Johnson <jbj@jbj.org> 0.34.0-3
- rebuild against db-4.2.52.

* Thu Dec  4 2003 Joe Orton <jorton@redhat.com> 0.34.0-2
- package all man pages

* Thu Dec 04 2003 Joe Orton <jorton@redhat.com> 0.34.0-1
- update to 0.34.0

* Thu Nov 13 2003 Joe Orton <jorton@redhat.com> 0.32.1-3
- remove workarounds for #109268 and #109267

* Thu Nov  6 2003 Joe Orton <jorton@redhat.com> 0.32.1-2
- rebuild for Python 2.3.2
- remove libtool workaround
- add workarounds for #109268 and #109267

* Fri Oct 24 2003 Joe Orton <jorton@redhat.com> 0.32.1-1
- update to 0.31.2
- work around libtool/ppc64/db4 confusion

* Mon Oct 13 2003 Jeff Johnson <jbj@jbj.org> 0.31.0-2.1
- rebuild against db-4.2.42.

* Fri Oct 10 2003 Joe Orton <jorton@redhat.com> 0.31.0-2
- include The Book
- don't add an RPATH for libdir to executables

* Thu Oct  9 2003 Joe Orton <jorton@redhat.com> 0.31.0-1
- update to 0.31.0

* Wed Sep 24 2003 Joe Orton <jorton@redhat.com> 0.30.0-1
- update to 0.30.0

* Sun Sep  7 2003 Joe Orton <jorton@redhat.com> 0.29.0-1
- update to 0.29.0

* Tue Jul 22 2003 Nalin Dahyabhai <nalin@redhat.com> 0.25-2
- rebuild

* Tue Jul 15 2003 Joe Orton <jorton@redhat.com> 0.25-1
- update to 0.25

* Mon Jul 14 2003 Joe Orton <jorton@redhat.com> 0.24.2-4
- rebuild

* Tue Jun 24 2003 Joe Orton <jorton@redhat.com> 0.24.2-3
- rebuild

* Tue Jun 24 2003 Joe Orton <jorton@redhat.com> 0.24.2-2
- don't use any LDFLAGS when building swig, fix for libdir=lib64

* Tue Jun 24 2003 Joe Orton <jorton@redhat.com> 0.24.2-1
- update to 0.24.2; fix Python bindings

* Tue Jun 17 2003 Joe Orton <jorton@redhat.com> 0.24.1-1
- update to 0.24.1; include mod_authz_svn
- force use of CC=gcc CXX=g++

* Mon Jun  9 2003 Joe Orton <jorton@redhat.com> 0.23.0-2
- add cvs2svn man page

* Mon Jun  9 2003 Joe Orton <jorton@redhat.com> 0.23.0-1
- update to 0.23.0

* Sun Jun  8 2003 Joe Orton <jorton@redhat.com> 0.22.2-7
- package cvs2svn to be usable outside docdir
- remove unnecessary files

* Thu Jun  5 2003 Joe Orton <jorton@redhat.com> 0.22.2-6
- add fix for unhandled deadlock errors in libsvn_fs
- don't package the out-of-date info pages

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com> 0.22.2-5
- rebuilt

* Tue Jun  3 2003 Joe Orton <jorton@redhat.com> 0.22.2-4
- cleanups

* Mon Jun  2 2003 Elliot Lee <sopwith@redhat.com> 0.22.2-3
- Add back in s390x, excludearch bad.

* Tue May 20 2003 Jeff Johnson <jbj@redhat.com> 0.22.2-2
- use external neon-0.23.9-2 (i.e. with neon-config), drop internal neon.
- use db-4.1.25, not db-4.0.14.
- do "make check" (but ignore failure for now).
- s390x knows not of httpd >= 2.0.45.

* Thu May  8 2003 Joe Orton <jorton@redhat.com> 0.22.2-1
- update to 0.22.2; add mod_dav_svn subpackage
- include Python bindings
- neon: force use of expat, enable SSL
- drop check for specific apr version added in -3

* Thu May  1 2003 Joe Orton <jorton@redhat.com> 0.20.1-6
- filter out perl(Config::IniFiles) requirement

* Thu May  1 2003 Joe Orton <jorton@redhat.com> 0.20.1-5
- fail early if apr-config is not 0.9.3

* Wed Apr 30 2003 Joe Orton <jorton@redhat.com> 0.20.1-4
- fix workaround for non-lib64 platforms

* Wed Apr 30 2003 Joe Orton <jorton@redhat.com> 0.20.1-3
- add workaround for libtool problem

* Tue Apr 29 2003 Joe Orton <jorton@redhat.com> 0.20.1-2
- require and use system apr, apr-util libraries
- use License not Copyright

* Fri Apr 04 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 0.20.1

* Wed Jan 22 2003 Jeff Johnson <jbj@redhat.com> 0.17.1-4503.0
- upgrade to 0.17.1.

* Wed Dec 11 2002 Jeff Johnson <jbj@redhat.com> 0.16-3987.1
- upgrade to 0.16.

* Wed Nov 13 2002 Jeff Johnson <jbj@redhat.com> 0.15-3687.2
- don't mess with the info handbook install yet.

* Sun Nov 10 2002 Jeff Johnson <jbj@redhat.com> 0.15-3687.1
- use libdir, build on x86_64 too.
- avoid "perl(Config::IniFiles) >= 2.27" dependency.

* Sat Nov  9 2002 Jeff Johnson <jbj@redhat.com> 0.15-3687.0
- first build from adapted spec file, only client and libraries for now.
- internal apr/apr-utils/neon until incompatibilities sort themselves out.
- avoid libdir issues on x86_64 for the moment.
