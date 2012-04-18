%{!?_httpd_apxs:       %{expand: %%global _httpd_apxs       %%{_sbindir}/apxs}}
%{!?_httpd_mmn:        %{expand: %%global _httpd_mmn        %%(cat %{_includedir}/httpd/.mmn || echo missing-httpd-devel)}}
%{!?_httpd_confdir:    %{expand: %%global _httpd_confdir    %%{_sysconfdir}/httpd/conf.d}}
# /etc/httpd/conf.d with httpd < 2.4 and defined as /etc/httpd/conf.modules.d with httpd >= 2.4
%{!?_httpd_modconfdir: %{expand: %%global _httpd_modconfdir %%{_sysconfdir}/httpd/conf.d}}

Name: mod_revocator
Version: 1.0.3
Release: 11%{?dist}
Summary: CRL retrieval module for the Apache HTTP server
Group: System Environment/Daemons
License: ASL 2.0
URL: http://directory.fedora.redhat.com/wiki/Mod_revocator
Source: http://directory.fedora.redhat.com/sources/%{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: nspr-devel >= 4.6, nss-devel >= 3.11.9
BuildRequires: nss-pkcs11-devel >= 3.11
BuildRequires: nss-pkcs11-devel-static
BuildRequires: httpd-devel >= 0:2.0.52, apr-devel, apr-util-devel
BuildRequires: pkgconfig, autoconf, automake, libtool
BuildRequires: openldap-devel >= 2.2.29
Requires: mod_nss >= 1.0.8
Requires: httpd-mmn = %{_httpd_mmn}
Patch1: mod_revocator-libpath.patch
Patch2: mod_revocator-kill.patch
Patch3: mod_revocator-segfault-fix.patch
Patch4: mod_revocator-32-bit-semaphore-fix.patch
Patch5: mod_revocator-array-size.patch

%description
The mod_revocator module retrieves and installs remote
Certificate Revocate Lists (CRLs) into an Apache web server. 

%prep
%setup -q
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

%build
autoreconf -fvi

# Needed for ppc64, automake can't be run here
for file in %{_datadir}/automake-*/config.{guess,sub}
do
    cp -f $file .
done

CFLAGS="$RPM_OPT_FLAGS"
export CFLAGS

NSPR_INCLUDE_DIR=`/usr/bin/pkg-config --variable=includedir nspr`
NSPR_LIB_DIR=`/usr/bin/pkg-config --variable=libdir nspr`

NSS_INCLUDE_DIR=`/usr/bin/pkg-config --variable=includedir nss`
NSS_LIB_DIR=`/usr/bin/pkg-config --variable=libdir nss`

NSS_BIN=`/usr/bin/pkg-config --variable=exec_prefix nss`

%configure \
    --with-nss-lib=$NSS_LIB_DIR \
    --with-nss-inc=$NSS_INCLUDE_DIR \
    --with-nspr-lib=$NSPR_LIB_DIR \
    --with-nspr-inc=$NSPR_INCLUDE_DIR \
    --with-apr-config --enable-openldap \
    --with-apxs=%{_httpd_apxs}

make %{?_smp_flags} all

%install
# The install target of the Makefile isn't used because that uses apxs
# which tries to enable the module in the build host httpd instead of in
# the build root.
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_httpd_confdir} $RPM_BUILD_ROOT%{_httpd_modconfdir} \
       $RPM_BUILD_ROOT%{_libdir}/httpd/modules $RPM_BUILD_ROOT%{_bindir}


%if "%{_httpd_modconfdir}" != "%{_httpd_confdir}"
# httpd >= 2.4.x
sed -n /^LoadModule/p revocator.conf > 10-revocator.conf
sed -i /^LoadModule/d revocator.conf
install -m 644 10-revocator.conf $RPM_BUILD_ROOT%{_httpd_modconfdir}/10-revocator.conf
%endif
install -m 644 revocator.conf $RPM_BUILD_ROOT%{_httpd_confdir}/revocator.conf
install -m 755 .libs/libmodrev.so $RPM_BUILD_ROOT%{_libdir}/httpd/modules/mod_rev.so
# Ugh, manually create the ldconfig symbolic links
version=`grep -v '^\#' ./libtool-version`
current=`echo $version | cut -d: -f1`
revision=`echo $version | cut -d: -f2`
age=`echo $version | cut -d: -f3`
install -m  755 .libs/librevocation.so.$current.$revision.$age $RPM_BUILD_ROOT%{_libdir}/
(cd $RPM_BUILD_ROOT%{_libdir} && ln -s librevocation.so.$current.$revision.$age librevocation.so.0)
(cd $RPM_BUILD_ROOT%{_libdir} && ln -s librevocation.so.$current.$revision.$age  librevocation.so)
install -m 755 ldapget $RPM_BUILD_ROOT%{_bindir}/
install -m 755 crlhelper $RPM_BUILD_ROOT%{_bindir}/

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc README LICENSE docs/mod_revocator.html
%config(noreplace) %{_sysconfdir}/httpd/conf.*/*.conf
%{_libdir}/httpd/modules/mod_rev.so
# rpmlint will complain that librevocation.so is a shared library but this
# must be ignored because this file is loaded directly by name by the Apache
# module.
%{_libdir}/librevocation.*so*
%{_bindir}/ldapget
%{_bindir}/crlhelper

%changelog
* Wed Apr 18 2012 Joe Orton <jorton@redhat.com> - 1.0.3-11
- fix deps, packaging for 2.4 (#803074)

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Oct 27 2011 Matthew Harmsen <mharmsen@redhat.com> - 1.0.3-9
- Bugzilla Bug #716874 - httpd (32 bit) failed to start if mod_revocator
  (32 bit) is installed on ppc64

* Fri Oct 21 2011 Matthew Harmsen <mharmsen@redhat.com> - 1.0.3-7
- Bugzilla Bug #716355 - mod_revocator does not shut down httpd server if
  expired CRL is fetched
- Bugzilla Bug #716361 - mod_revocator does not bring down httpd server if
  CRLUpdate fails

* Tue Oct 11 2011 Matthew Harmsen <mharmsen@redhat.com> - 1.0.3-6
- Bugzilla Bug #737556 - CRLS are not downloaded when mod_revocator module
  is loaded successfully. And no error was thrown in httpd error_log -
  mharmsen
- Add 'autoreconf -fvi' to build section - mharmsen
- Fix shutting down Apache if CRLUpdateCritical is on and a CRL
  is not available at startup (#654378) - rcritten@redhat.com
- Updated mod_revocator-kill patch. The ownership of the semaphore used to
  control access to crlhelper was not always changed to the Apache user
  (#648546) - rcritten@redhat.com
- Actually apply the patch (#648546) - rcritten@redhat.com
- Fix killing the web server if updatecritical is set (#648546) -
  rcritten@redhat.com

* Mon Mar  7 2011 Rob Crittenden <rcritten@redhat.com> - 1.0.3-4
- Use correct package name, nss-pkcs11-devel-static (#640293)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Oct  4 2010 Rob Crittenden <rcritten@redhat.com> - 1.0.3-2
- Add BuildRequires: nss-pkcs11-static (#640293)

* Tue Apr 14 2010 Rob Crittenden <rcritten@redhat.com> - 1.0.3-1
- Update to upstream 1.0.3

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Mar 04 2009 Robert Scheck <robert@fedoraproject.org> - 1.0.2-7
- Solve the ppc64-redhat-linux-gnu configure target error

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Aug 11 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.0.2-5
- fix license tag

* Mon Feb 25 2008 Rob Crittenden <rcritten@redhat.com> 1.0.2-4
- The nss package changed the location of the NSS shared libraries to /lib from
  /usr/lib. Static libraries remained in /usr/lib. They then updated their
  devel package to put symlinks back from /lib to /usr. Respin to pick that up.
  BZ 434395.

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.0.2-3
- Autorebuild for GCC 4.3

* Wed Dec  5 2007 Rob Crittenden <rcritten@redhat.com> 1.0.2-2
- Respin to pick up new openldap

* Mon Oct 16 2006 Rob Crittenden <rcritten@redhat.com> 1.0.2-1
- Initial build
