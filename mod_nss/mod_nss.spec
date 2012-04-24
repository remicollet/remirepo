%{!?_httpd_apxs:       %{expand: %%global _httpd_apxs       %%{_sbindir}/apxs}}
%{!?_httpd_mmn:        %{expand: %%global _httpd_mmn        %%(cat %{_includedir}/httpd/.mmn || echo missing-httpd-devel)}}
%{!?_httpd_confdir:    %{expand: %%global _httpd_confdir    %%{_sysconfdir}/httpd/conf.d}}
# /etc/httpd/conf.d with httpd < 2.4 and defined as /etc/httpd/conf.modules.d with httpd >= 2.4
%{!?_httpd_modconfdir: %{expand: %%global _httpd_modconfdir %%{_sysconfdir}/httpd/conf.d}}
%{!?_httpd_moddir:    %{expand: %%global _httpd_moddir    %%{_libdir}/httpd/modules}}

Name: mod_nss
Version: 1.0.8
Release: 16%{?dist}
Summary: SSL/TLS module for the Apache HTTP server
Group: System Environment/Daemons
License: ASL 2.0
URL: http://directory.fedoraproject.org/wiki/Mod_nss
Source: http://directory.fedoraproject.org/sources/%{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: nspr-devel >= 4.6.3, nss-devel >= 3.12.6
BuildRequires: httpd-devel, apr-devel, apr-util-devel
BuildRequires: pkgconfig
Requires: httpd-mmn = %{_httpd_mmn}
Requires(post): httpd, nss-tools
Requires: nss >= 3.12.6
Patch1: mod_nss-conf.patch
Patch2: mod_nss-gencert.patch
Patch3: mod_nss-wouldblock.patch
# Add options for tuning client negotiate in NSS
Patch4: mod_nss-negotiate.patch
Patch5: mod_nss-reverseproxy.patch
Patch6: mod_nss-pcachesignal.h
Patch7: mod_nss-reseterror.patch
Patch8: mod_nss-lockpcache.patch

%description
The mod_nss module provides strong cryptography for the Apache Web
server via the Secure Sockets Layer (SSL) and Transport Layer
Security (TLS) protocols using the Network Security Services (NSS)
security library.

%prep
%setup -q
%patch1 -p1 -b .conf
%patch2 -p1 -b .gencert
%patch3 -p1 -b .wouldblock
%patch4 -p1 -b .negotiate
%patch5 -p1 -b .reverseproxy
%patch6 -p1 -b .pcachesignal.h
%patch7 -p1 -b .reseterror
%patch8 -p1 -b .lockpcache

# Touch expression parser sources to prevent regenerating it
touch nss_expr_*.[chyl]

%build

CFLAGS="$RPM_OPT_FLAGS"
APXS=%{_httpd_apxs}

export CFLAGS APXS

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
    --with-apr-config

make %{?_smp_mflags} all

%install
# The install target of the Makefile isn't used because that uses apxs
# which tries to enable the module in the build host httpd instead of in
# the build root.
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf
mkdir -p $RPM_BUILD_ROOT%{_httpd_confdir}
mkdir -p $RPM_BUILD_ROOT%{_libdir}/httpd/modules
mkdir -p $RPM_BUILD_ROOT%{_sbindir}
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/httpd/alias

%if "%{_httpd_modconfdir}" != "%{_httpd_confdir}"
# httpd >= 2.4.x
mkdir -p $RPM_BUILD_ROOT%{_httpd_modconfdir}
sed -n /^LoadModule/p nss.conf > 10-nss.conf
sed -i /^LoadModule/d nss.conf
install -m 644 10-nss.conf $RPM_BUILD_ROOT%{_httpd_modconfdir}
%endif

install -m 644 nss.conf $RPM_BUILD_ROOT%{_httpd_confdir}

install -m 755 .libs/libmodnss.so $RPM_BUILD_ROOT%{_libdir}/httpd/modules/
install -m 755 nss_pcache $RPM_BUILD_ROOT%{_sbindir}/
install -m 755 gencert $RPM_BUILD_ROOT%{_sbindir}/
ln -s ../../../%{_libdir}/libnssckbi.so $RPM_BUILD_ROOT%{_sysconfdir}/httpd/alias/
touch $RPM_BUILD_ROOT%{_sysconfdir}/httpd/alias/secmod.db
touch $RPM_BUILD_ROOT%{_sysconfdir}/httpd/alias/cert8.db
touch $RPM_BUILD_ROOT%{_sysconfdir}/httpd/alias/key3.db
touch $RPM_BUILD_ROOT%{_sysconfdir}/httpd/alias/install.log

perl -pi -e "s:$NSS_LIB_DIR:$NSS_BIN:" $RPM_BUILD_ROOT%{_sbindir}/gencert

%clean
rm -rf $RPM_BUILD_ROOT

%post
umask 077

if [ "$1" -eq 1 ] ; then
    if [ ! -e %{_sysconfdir}/httpd/alias/key3.db ]; then
        %{_sbindir}/gencert %{_sysconfdir}/httpd/alias > %{_sysconfdir}/httpd/alias/install.log 2>&1
        echo ""
        echo "%{name} certificate database generated."
        echo ""
    fi

    # Make sure that the database ownership is setup properly.
    /bin/find %{_sysconfdir}/httpd/alias -user root -name "*.db" -exec /bin/chgrp apache {} \;
    /bin/find %{_sysconfdir}/httpd/alias -user root -name "*.db" -exec /bin/chmod g+r {} \;
fi

%files
%defattr(-,root,root,-)
%doc README LICENSE docs/mod_nss.html
%config(noreplace) %{_httpd_confdir}/nss.conf
%if "%{_httpd_modconfdir}" != "%{_httpd_confdir}"
%config(noreplace) %{_httpd_modconfdir}/10-nss.conf
%endif
%{_libdir}/httpd/modules/libmodnss.so
%dir %{_sysconfdir}/httpd/alias/
%ghost %attr(0640,root,apache) %config(noreplace) %{_sysconfdir}/httpd/alias/secmod.db
%ghost %attr(0640,root,apache) %config(noreplace) %{_sysconfdir}/httpd/alias/cert8.db
%ghost %attr(0640,root,apache) %config(noreplace) %{_sysconfdir}/httpd/alias/key3.db
%ghost %config(noreplace) %{_sysconfdir}/httpd/alias/install.log
%{_sysconfdir}/httpd/alias/libnssckbi.so
%{_sbindir}/nss_pcache
%{_sbindir}/gencert

%changelog
* Mon Apr 23 2012 Joe Orton <jorton@redhat.com> - 1.0.8-16
- packaging fixes/updates (#803072)

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.8-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Mar  7 2011 Rob Crittenden <rcritten@redhat.com> - 1.0.8-14
- Add Requires(post) for nss-tools, gencert needs it (#652007)

* Wed Mar  2 2011 Rob Crittenden <rcritten@redhat.com> - 1.0.8-13
- Lock around the pipe to nss_pcache for retrieving the token PIN
  (#677701)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.8-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan 12 2011 Rob Crittenden <rcritten@redhat.com> - 1.0.8-11
- Use memmove in place of memcpy since the buffers can overlap (#669118)

* Wed Sep 29 2010 jkeating - 1.0.8-10
- Rebuilt for gcc bug 634757

* Thu Sep 23 2010 Rob Crittenden <rcritten@redhat.com> - 1.0.8-9
- Revert mod_nss-wouldblock patch
- Reset NSPR error before calling PR_Read(). This should fix looping
  in #620856

* Fri Sep 17 2010 Rob Crittenden <rcritten@redhat.com> - 1.0.8-8
- Fix hang when handling large POST under some conditions (#620856)

* Tue Jun 22 2010 Rob Crittenden <rcritten@redhat.com> - 1.0.8-7
- Remove file Requires on libnssckbi.so (#601939)

* Fri May 14 2010 Rob Crittenden <rcritten@redhat.com> - 1.0.8-6
- Ignore SIGHUP in nss_pcache (#591889).

* Thu May 13 2010 Rob Crittenden <rcritten@redhat.com> - 1.0.8-5
- Use remote hostname set by mod_proxy to compare to CN in peer cert (#591224)

* Thu Mar 18 2010 Rob Crittenden <rcritten@redhat.com> - 1.0.8-4
- Patch to add configuration options for new NSS negotiation API (#574187)
- Add (pre) for Requires on httpd so we can be sure the user and group are
  already available
- Add file Requires on libnssckbi.so so symlink can't fail
- Use _sysconfdir macro instead of /etc
- Set minimum level of NSS to 3.12.6

* Mon Jan 25 2010 Rob Crittenden <rcritten@redhat.com> - 1.0.8-3
- The location of libnssckbi moved from /lib[64] to /usr/lib[64] (556744)

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Mar  2 2009 Rob Crittenden <rcritten@redhat.com> - 1.0.8-1
- Update to 1.0.8
- Add patch that fixes NSPR layer bug

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.7-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Aug 11 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.0.7-10
- fix license tag

* Mon Jul 28 2008 Rob Crittenden <rcritten@redhat.com> - 1.0.7-9
- rebuild to bump NVR

* Mon Jul 14 2008 Rob Crittenden <rcritten@redhat.com> - 1.0.7-8
- Don't force module de-init during the configuration stage (453508)

* Thu Jul 10 2008 Rob Crittenden <rcritten@redhat.com> - 1.0.7-7
- Don't inherit the MP cache in multi-threaded mode (454701)
- Don't initialize NSS in each child if SSL isn't configured

* Wed Jul  2 2008 Rob Crittenden <rcritten@redhat.com> - 1.0.7-6
- Update the patch for FIPS to include fixes for nss_pcache, enforce
  the security policy and properly initialize the FIPS token.

* Mon Jun 30 2008 Rob Crittenden <rcritten@redhat.com> - 1.0.7-5
- Include patch to fix NSSFIPS (446851)

* Mon Apr 28 2008 Rob Crittenden <rcritten@redhat.com> - 1.0.7-4
- Apply patch so that mod_nss calls NSS_Init() after Apache forks a child
  and not before. This is in response to a change in the NSS softtokn code
  and should have always been done this way. (444348)
- The location of libnssckbi moved from /usr/lib[64] to /lib[64]
- The NSS database needs to be readable by apache since we need to use it
  after the root priviledges are dropped.

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.0.7-3
- Autorebuild for GCC 4.3

* Thu Oct 18 2007 Rob Crittenden <rcritten@redhat.com> 1.0.7-2
- Register functions needed by mod_proxy if mod_ssl is not loaded.

* Fri Jun  1 2007 Rob Crittenden <rcritten@redhat.com> 1.0.7-1
- Update to 1.0.7
- Remove Requires for nss and nspr since those are handled automatically
  by versioned libraries
- Updated URL and Source to reference directory.fedoraproject.org

* Mon Apr  9 2007 Rob Crittenden <rcritten@redhat.com> 1.0.6-2
- Patch to properly detect the Apache model and set up NSS appropriately
- Patch to punt if a bad password is encountered
- Patch to fix crash when password.conf is malformatted
- Don't enable ECC support as NSS doesn't have it enabled (3.11.4-0.7)

* Mon Oct 23 2006 Rob Crittenden <rcritten@redhat.com> 1.0.6-1
- Update to 1.0.6

* Fri Aug 04 2006 Rob Crittenden <rcritten@redhat.com> 1.0.3-4
- Include LogLevel warn in nss.conf and use separate log files

* Fri Aug 04 2006 Rob Crittenden <rcritten@redhat.com> 1.0.3-3
- Need to initialize ECC certificate and key variables

* Fri Aug 04 2006 Jarod Wilson <jwilson@redhat.com> 1.0.3-2
- Use %%ghost for db files and install.log

* Tue Jun 20 2006 Rob Crittenden <rcritten@redhat.com> 1.0.3-1
- Initial build
