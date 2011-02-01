# Minimal required versions
%global nspr_version 4.8.7
%global nss_version 3.12.9
%global cairo_version 1.10.0
%global freetype_version 2.1.9
%global sqlite_version 3.7.4
#global libnotify_version 0.7
%global lcms_version 1.18

%global shortname         xulrunner

%global version_internal  2
%global pretag            b10
%global mozappdir         %{_libdir}/%{shortname}-%{version_internal}
%global tarballdir        mozilla-central

# build crash reporter only on x86/x86_64 for now
%ifarch %{ix86} x86_64
%global enable_mozilla_crashreporter 1
%global moz_out_of_process_plugins   1
%else
%global enable_mozilla_crashreporter 0
%global moz_out_of_process_plugins   0
%endif

# The actual sqlite version (see #480989):
%global sqlite_build_version %(pkg-config --silence-errors --modversion sqlite3 2>/dev/null || echo 65536)


Summary:        XUL Runtime for Gecko Applications
%if %{fedora} >= 15
Name:           %{shortname}
%else
Name:           %{shortname}2
%endif
Version:        2.0
Release:        0.18.beta10%{?dist}
URL:            http://developer.mozilla.org/En/XULRunner
License:        MPLv1.1 or GPLv2+ or LGPLv2+
Group:          Applications/Internet
# You can get sources at ftp://ftp.mozilla.org/pub/firefox/releases/%{version}%{?pretag}/source
Source0:        %{shortname}-%{version}%{?pretag}.source.tar.bz2
Source10:       %{shortname}-mozconfig
Source11:       %{shortname}-mozconfig-debuginfo
Source12:       %{shortname}-redhat-default-prefs.js
Source21:       %{shortname}.sh.in

# build patches
Patch0:         xulrunner-version.patch
Patch1:         mozilla-build.patch
Patch9:         mozilla-build-sbrk.patch
Patch12:        xulrunner-2.0-64bit-big-endian.patch
Patch13:        xulrunner-2.0-secondary-jit.patch
Patch14:        xulrunner-2.0-chromium-types.patch
Patch15:        xulrunner-2.0-system-cairo.patch
Patch16:        xulrunner-2.0-system-cairo-tee.patch
Patch17:        xulrunner-2.0-os2cc.patch

# Fedora specific patches
Patch20:        mozilla-193-pkgconfig.patch
Patch21:        mozilla-libjpeg-turbo.patch
Patch22:        mozilla-notify.patch
Patch23:        wmclass.patch
Patch24:        crashreporter-remove-static.patch

# Upstream patches
Patch30:        revert-562138.patch

# ---------------------------------------------------

BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
%if %{fedora} >= 14
BuildRequires:  nspr-devel >= %{nspr_version}
BuildRequires:  nss-devel >= %{nss_version}
%endif
%if %{fedora} >= 15
BuildRequires:  cairo-devel >= %{cairo_version}
%endif
BuildRequires:  libpng-devel
BuildRequires:  libjpeg-devel
BuildRequires:  zip
BuildRequires:  bzip2-devel
BuildRequires:  zlib-devel
BuildRequires:  libIDL-devel
BuildRequires:  gtk2-devel
BuildRequires:  gnome-vfs2-devel
BuildRequires:  libgnome-devel
BuildRequires:  libgnomeui-devel
BuildRequires:  krb5-devel
BuildRequires:  pango-devel
BuildRequires:  freetype-devel >= %{freetype_version}
BuildRequires:  libXt-devel
BuildRequires:  libXrender-devel
%if %{fedora} >= 11
BuildRequires:  hunspell-devel
%endif
%if %{fedora} >= 15
BuildRequires:  sqlite-devel >= %{sqlite_version}
%endif
BuildRequires:  startup-notification-devel
BuildRequires:  alsa-lib-devel
BuildRequires:  libnotify-devel
BuildRequires:  autoconf213
BuildRequires:  mesa-libGL-devel
BuildRequires:  yasm
BuildRequires:  libcurl-devel
BuildRequires:  lcms-devel >= %{lcms_version}
%ifarch %{ix86} x86_64
BuildRequires:  wireless-tools-devel
%endif

Requires:       mozilla-filesystem
%if %{fedora} >= 14
Requires:       nspr >= %{nspr_version}
Requires:       nss >= %{nss_version}
%endif
%if %{fedora} >= 15
Requires:       sqlite >= %{sqlite_build_version}
%endif
Provides:       gecko-libs = %{version}

%description
XULRunner provides the XUL Runtime environment for Gecko applications.

%package devel
Summary: Development files for Gecko
Group: Development/Libraries
Obsoletes: mozilla-devel < 1.9
Obsoletes: firefox-devel < 2.1
Obsoletes: xulrunner-devel-unstable
Provides: gecko-devel = %{version}
Provides: gecko-devel-unstable = %{version}

Requires: %{name} = %{version}-%{release}
%if %{fedora} >= 14
Requires: nspr-devel >= %{nspr_version}
Requires: nss-devel >= %{nss_version}
%endif
%if %{fedora} >= 15
Requires: cairo-devel >= %{cairo_version}
%endif
Requires: libjpeg-devel
Requires: zip
Requires: bzip2-devel
Requires: zlib-devel
Requires: libIDL-devel
Requires: gtk2-devel
Requires: gnome-vfs2-devel
Requires: libgnome-devel
Requires: libgnomeui-devel
Requires: krb5-devel
Requires: pango-devel
Requires: freetype-devel >= %{freetype_version}
Requires: libXt-devel
Requires: libXrender-devel
%if %{fedora} >= 11
Requires: hunspell-devel
%endif
Requires: sqlite-devel
Requires: startup-notification-devel
Requires: alsa-lib-devel
Requires: libnotify-devel
Requires: mesa-libGL-devel
Requires: lcms-devel
Requires: yasm
%ifarch %{ix86} x86_64
Requires: wireless-tools-devel
%endif

%description devel
Gecko development files.

#---------------------------------------------------------------------

%prep
%setup -q -c
cd %{tarballdir}

sed -e 's/__RPM_VERSION_INTERNAL__/%{version_internal}/' %{P:%%PATCH0} \
    > version.patch
%{__patch} -p1 -b --suffix .version --fuzz=0 < version.patch

%patch1  -p2 -b .build
%patch9  -p2 -b .sbrk
%patch12 -p2 -b .64bit-big-endian
%patch13 -p2 -b .secondary-jit
%patch14 -p2 -b .chromium-types
%if %{fedora} >= 15
%patch15 -p1 -b .system-cairo
%patch16 -p1 -b .system-cairo-tee
%endif
%patch17 -p1 -b .os2cc

%patch20 -p2 -b .pk
%patch21 -p2 -b .jpeg-turbo
%patch22 -p1 -b .notify
%patch23 -p1 -b .wmclass
%patch24 -p1 -b .static

%patch30 -p1 -b .revert-562138

%if %{fedora} >= 15
# For xulrunner-2.0-system-cairo-tee.patch
autoconf-2.13
%endif

%{__rm} -f .mozconfig
%{__cat} %{SOURCE10} \
%if %{fedora} < 15
   | grep -v enable-system-sqlite  \
%endif
%if %{fedora} < 14
  | grep -v with-system-nspr       \
  | grep -v with-system-nss        \
%endif
%if %{fedora} < 11
  | grep -v enable-system-hunspell \
%endif
%if %{fedora} < 15
  | grep -v enable-system-cairo    \
%endif
%ifarch %{ix86} x86_64
  | grep -v disable-necko-wifi     \
%endif
  | tee .mozconfig

%if %{enable_mozilla_crashreporter}
%{__cat} %{SOURCE11} >> .mozconfig
%endif

echo "ac_add_options --enable-system-lcms" >> .mozconfig

%if !%{?moz_out_of_process_plugins}
echo "ac_add_options --disable-ipc" >> .mozconfig
%endif

#---------------------------------------------------------------------

%build
%if %{fedora} >= 15
# Do not proceed with build if the sqlite require would be broken:
# make sure the minimum requirement is non-empty, ...
sqlite_version=$(expr "%{sqlite_version}" : '\([0-9]*\.\)[0-9]*\.') || exit 1
# ... and that major number of the computed build-time version matches:
case "%{sqlite_build_version}" in
  "$sqlite_version"*) ;;
  *) exit 1 ;;
esac
%endif

cd %{tarballdir}

INTERNAL_GECKO=%{version_internal}
MOZ_APP_DIR=%{_libdir}/%{shortname}-${INTERNAL_GECKO}


# -fpermissive is needed to build with gcc 4.6+ which has become stricter
# 
# Mozilla builds with -Wall with exception of a few warnings which show up
# everywhere in the code; so, don't override that.
#
# Disable C++ exceptions since Mozilla code is not exception-safe
#
MOZ_OPT_FLAGS=$(echo "$RPM_OPT_FLAGS -fpermissive" | \
                             %{__sed} -e 's/-Wall//' -e 's/-fexceptions//g')
export CFLAGS=$MOZ_OPT_FLAGS
export CXXFLAGS=$MOZ_OPT_FLAGS

export PREFIX='%{_prefix}'
export LIBDIR='%{_libdir}'

MOZ_SMP_FLAGS=-j1
# On x86 architectures, Mozilla can build up to 4 jobs at once in parallel,
# however builds tend to fail on other arches when building in parallel.
%ifarch %{ix86} x86_64
[ -z "$RPM_BUILD_NCPUS" ] && \
     RPM_BUILD_NCPUS="`/usr/bin/getconf _NPROCESSORS_ONLN`"
[ "$RPM_BUILD_NCPUS" -ge 2 ] && MOZ_SMP_FLAGS=-j2
[ "$RPM_BUILD_NCPUS" -ge 4 ] && MOZ_SMP_FLAGS=-j4
%endif

export LDFLAGS="-Wl,-rpath,${MOZ_APP_DIR}"
make -f client.mk build STRIP="/bin/true" MOZ_MAKE_FLAGS="$MOZ_SMP_FLAGS" MOZ_SERVICES_SYNC="1"

# create debuginfo for crash-stats.mozilla.com
%if %{enable_mozilla_crashreporter}
#cd %{moz_objdir}
make buildsymbols
%endif

#---------------------------------------------------------------------

%install
cd %{tarballdir}
%{__rm} -rf $RPM_BUILD_ROOT

INTERNAL_GECKO=%{version_internal}

INTERNAL_APP_NAME=%{shortname}-${INTERNAL_GECKO}
MOZ_APP_DIR=%{_libdir}/${INTERNAL_APP_NAME}

INTERNAL_APP_SDK_NAME=%{shortname}-sdk-${INTERNAL_GECKO}
MOZ_APP_SDK_DIR=%{_libdir}/${INTERNAL_APP_SDK_NAME}

DESTDIR=$RPM_BUILD_ROOT make install

%{__mkdir_p} $RPM_BUILD_ROOT/${MOZ_APP_DIR} \
             $RPM_BUILD_ROOT%{_datadir}/idl/${INTERNAL_APP_SDK_NAME} \
             $RPM_BUILD_ROOT%{_includedir}/${INTERNAL_APP_SDK_NAME}
%{__mkdir_p} $RPM_BUILD_ROOT{%{_libdir},%{_bindir},%{_datadir}/applications}

# set up our default preferences
%{__cat} %{SOURCE12} | %{__sed} -e 's,RPM_VERREL,%{version}-%{release},g' > rh-default-prefs
%{__install} -p -D -m 644 rh-default-prefs $RPM_BUILD_ROOT/${MOZ_APP_DIR}/defaults/pref/all-redhat.js
%{__rm} rh-default-prefs

# Start script install
%{__rm} -rf $RPM_BUILD_ROOT%{_bindir}/%{shortname}
%{__cat} %{SOURCE21} | %{__sed} -e 's,XULRUNNER_VERSION,%{version_internal},g' > \
  $RPM_BUILD_ROOT%{_bindir}/%{name}
%{__chmod} 755 $RPM_BUILD_ROOT%{_bindir}/%{name}

%{__rm} -f $RPM_BUILD_ROOT${MOZ_APP_DIR}/%{shortname}-config

cd $RPM_BUILD_ROOT${MOZ_APP_DIR}/chrome
find . -name "*" -type d -maxdepth 1 -exec %{__rm} -rf {} \;
cd -

# Prepare our devel package
%{__mkdir_p} $RPM_BUILD_ROOT/%{_includedir}/${INTERNAL_APP_SDK_NAME}
%{__mkdir_p} $RPM_BUILD_ROOT/%{_datadir}/idl/${INTERNAL_APP_SDK_NAME}
%{__mkdir_p} $RPM_BUILD_ROOT/%{_libdir}/pkgconfig

%{__cp} -rL dist/include/* \
  $RPM_BUILD_ROOT/%{_includedir}/${INTERNAL_APP_SDK_NAME}

# Copy pc files (for compatibility with 1.9.1)
%{__cp} $RPM_BUILD_ROOT/%{_libdir}/pkgconfig/libxul.pc \
        $RPM_BUILD_ROOT/%{_libdir}/pkgconfig/libxul-unstable.pc
%{__cp} $RPM_BUILD_ROOT/%{_libdir}/pkgconfig/libxul-embedding.pc \
        $RPM_BUILD_ROOT/%{_libdir}/pkgconfig/libxul-embedding-unstable.pc


# Fix multilib devel conflicts...
%ifarch x86_64 ia64 s390x ppc64 sparc64
%define mozbits 64
%else
%define mozbits 32
%endif

function install_file() {
genheader=$*
mv ${genheader}.h ${genheader}%{mozbits}.h
cat > ${genheader}.h << EOF
/* This file exists to fix multilib conflicts */
#if defined(__x86_64__) || defined(__ia64__) || defined(__s390x__) || defined(__powerpc64__) || (defined(__sparc__) && defined(__arch64__))
#include "${genheader}64.h"
#else
#include "${genheader}32.h"
#endif
EOF
}

pushd $RPM_BUILD_ROOT/%{_includedir}/${INTERNAL_APP_SDK_NAME}
install_file "mozilla-config"
popd

pushd $RPM_BUILD_ROOT/%{_includedir}/${INTERNAL_APP_SDK_NAME}
install_file "jsautocfg"
popd

pushd $RPM_BUILD_ROOT/%{_includedir}/${INTERNAL_APP_SDK_NAME}
install_file "js-config"
popd

%{__install} -p -c -m 755 dist/bin/xpcshell \
  dist/bin/xpidl \
  dist/bin/xpt_dump \
  dist/bin/xpt_link \
  $RPM_BUILD_ROOT/${MOZ_APP_DIR}

%{__rm} -rf $RPM_BUILD_ROOT/%{_includedir}/${INTERNAL_APP_NAME}
%{__rm} -rf $RPM_BUILD_ROOT/%{_datadir}/idl/${INTERNAL_APP_NAME}

%{__rm} -rf $RPM_BUILD_ROOT${MOZ_APP_SDK_DIR}/include
ln -s  %{_includedir}/${INTERNAL_APP_SDK_NAME} \
       $RPM_BUILD_ROOT${MOZ_APP_SDK_DIR}/include

%{__rm} -rf $RPM_BUILD_ROOT${MOZ_APP_SDK_DIR}/idl
ln -s  %{_datadir}/idl/${INTERNAL_APP_SDK_NAME} \
       $RPM_BUILD_ROOT${MOZ_APP_SDK_DIR}/idl

%{__rm} -rf $RPM_BUILD_ROOT${MOZ_APP_SDK_DIR}/sdk/include
ln -s  %{_includedir}/${INTERNAL_APP_SDK_NAME} \
       $RPM_BUILD_ROOT${MOZ_APP_SDK_DIR}/sdk/include

%{__rm} -rf $RPM_BUILD_ROOT${MOZ_APP_SDK_DIR}/sdk/idl
ln -s  %{_datadir}/idl/${INTERNAL_APP_SDK_NAME} \
       $RPM_BUILD_ROOT${MOZ_APP_SDK_DIR}/sdk/idl

find $RPM_BUILD_ROOT/%{_includedir} -type f -name "*.h" | xargs chmod 644
find $RPM_BUILD_ROOT/%{_datadir}/idl -type f -name "*.idl" | xargs chmod 644

%{__rm} -rf $RPM_BUILD_ROOT${MOZ_APP_SDK_DIR}/sdk/lib/*.so
pushd $RPM_BUILD_ROOT${MOZ_APP_DIR}
for i in *.so; do
    ln -s ${MOZ_APP_DIR}/$i $RPM_BUILD_ROOT${MOZ_APP_SDK_DIR}/sdk/lib/$i
done
popd

# GRE stuff
%ifarch x86_64 ia64 ppc64 s390x sparc64
%define gre_conf_file gre2-64.conf
%else
%define gre_conf_file gre2.conf
%endif

MOZILLA_GECKO_VERSION=`./config/milestone.pl --topsrcdir=.`
%{__mv} $RPM_BUILD_ROOT/etc/gre.d/$MOZILLA_GECKO_VERSION".system.conf" \
        $RPM_BUILD_ROOT/etc/gre.d/%{gre_conf_file}
chmod 644 $RPM_BUILD_ROOT/etc/gre.d/%{gre_conf_file}

# Library path
%ifarch x86_64 ia64 ppc64 s390x sparc64
%define ld_conf_file %{name}-64.conf
%else
%define ld_conf_file %{name}-32.conf
%endif

%{__mkdir_p} $RPM_BUILD_ROOT/etc/ld.so.conf.d
%{__cat} > $RPM_BUILD_ROOT/etc/ld.so.conf.d/%{ld_conf_file} << EOF
${MOZ_APP_DIR}
EOF
                        
# Copy over the LICENSE
%{__install} -p -c -m 644 LICENSE $RPM_BUILD_ROOT${MOZ_APP_DIR}

# Use the system hunspell dictionaries
%{__rm} -rf ${RPM_BUILD_ROOT}${MOZ_APP_DIR}/dictionaries
ln -s %{_datadir}/myspell ${RPM_BUILD_ROOT}${MOZ_APP_DIR}/dictionaries

# ghost files
%{__mkdir_p} $RPM_BUILD_ROOT${MOZ_APP_DIR}/components
touch $RPM_BUILD_ROOT${MOZ_APP_DIR}/components/compreg.dat
touch $RPM_BUILD_ROOT${MOZ_APP_DIR}/components/xpti.dat

# Add debuginfo for crash-stats.mozilla.com 
%if %{enable_mozilla_crashreporter}
# Debug symbols are stored in /usr/lib even in x86_64 arch
DEBUG_LIB_DIR=`echo %{_libdir}|sed -e "s/lib64/lib/"`
mkdir -p $RPM_BUILD_ROOT$DEBUG_LIB_DIR/debug%{mozappdir}
cp dist/%{shortname}-%{version}*.crashreporter-symbols.zip $RPM_BUILD_ROOT$DEBUG_LIB_DIR/debug%{mozappdir}
%endif

#---------------------------------------------------------------------

%clean
%{__rm} -rf $RPM_BUILD_ROOT

#---------------------------------------------------------------------

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%preun
# is it a final removal?
if [ $1 -eq 0 ]; then
  %{__rm} -rf ${MOZ_APP_DIR}/components
fi

%files
%defattr(-,root,root,-)
%{_bindir}/%{name}
%dir /etc/gre.d
/etc/gre.d/%{gre_conf_file}
%dir %{mozappdir}
%doc %attr(644, root, root) %{mozappdir}/LICENSE
%doc %attr(644, root, root) %{mozappdir}/README.txt
%{mozappdir}/chrome
%{mozappdir}/chrome.manifest
%{mozappdir}/dictionaries
%dir %{mozappdir}/components
%ghost %{mozappdir}/components/compreg.dat
%ghost %{mozappdir}/components/xpti.dat
%{mozappdir}/components/*.so
%{mozappdir}/components/*.xpt
%{mozappdir}/components/*.manifest
%attr(644, root, root) %{mozappdir}/components/*.js
%{mozappdir}/defaults
%dir %{mozappdir}/icons
%attr(644, root, root) %{mozappdir}/icons/*
%{mozappdir}/modules
%{mozappdir}/plugins
%{mozappdir}/res
%{mozappdir}/*.so
%{mozappdir}/mozilla-xremote-client
%{mozappdir}/run-mozilla.sh
%{mozappdir}/xulrunner
%{mozappdir}/xulrunner-bin
%{mozappdir}/xulrunner-stub
%{mozappdir}/platform.ini
%{mozappdir}/dependentlibs.list
%{mozappdir}/greprefs.js
%{_sysconfdir}/ld.so.conf.d/xulrunner*.conf
%if %{?moz_out_of_process_plugins}
%{mozappdir}/plugin-container
%endif

# XXX See if these are needed still
%{mozappdir}/updater*
%exclude %{mozappdir}/update.locale

%if %{enable_mozilla_crashreporter}
%{mozappdir}/crashreporter
%{mozappdir}/crashreporter.ini
%{mozappdir}/Throbber-small.gif
%endif

%files devel
%defattr(-,root,root,-)
%{_datadir}/idl/%{shortname}*%{version_internal}
%{_includedir}/%{shortname}*%{version_internal}
%{_libdir}/%{shortname}-sdk-*/
%{_libdir}/pkgconfig/*.pc
%{mozappdir}/xpcshell
%{mozappdir}/xpidl
%{mozappdir}/xpt_dump
%{mozappdir}/xpt_link

#---------------------------------------------------------------------

%changelog
* Tue Feb 01 2011 Remi Collet <RPMS@FamilleCollet.com> - 2.0-0.18.beta10
- rename to xulrunner2
- merge most changes from spot
- backport to remi repo

* Wed Jan 26 2011 Christopher Aillon <caillon@redhat.com> - 2.0-0.18
- Fix issue with popup windows showing in the wrong place

* Tue Jan 25 2011 Christopher Aillon <caillon@redhat.com> - 2.0-0.17
- Update to 2.0 Beta 10

* Fri Jan 21 2011 Dan Horák <dan[at]danny.cz> - 2.0-0.16.b9
- updated the 64bit-big-endian patch (bmo#627664)
- added fix for build with --disable-methodjit (bmo#623277)

* Fri Jan 14 2011 Christopher Aillon <caillon@redhat.com> 2.0-0.15.b9
- Update to 2.0 Beta 9

* Thu Jan 11 2011 Tom Callaway <spot@fedoraproject.org> 2.0-0.14.b8
- enable system sqlite (see https://fedorahosted.org/fpc/ticket/34)

* Thu Dec 23 2010 Martin Stransky <stransky@redhat.com> 2.0-0.13.b8
- reverted fix for rhbz#658471

* Wed Dec 22 2010 Dan Horák <dan[at]danny.cz> - 2.0-0.11.b8
- updated the 64bit-big-endian patch

* Tue Dec 21 2010 Martin Stransky <stransky@redhat.com> 2.0-0.11.b8
- enable url-classifier and jar format for chrome files

* Tue Dec 21 2010 Martin Stransky <stransky@redhat.com> 2.0-0.10.b8
- Update to 2.0b8

* Mon Dec 20 2010 Martin Stransky <stransky@redhat.com> 2.0-0.9.b8
- removed unused library path (rhbz#658471)

* Fri Dec 17 2010 Dan Horák <dan[at]danny.cz> - 2.0-0.8.b7
- disable the crash reporter on non-x86 arches
- add sparc64 as 64-bit arch

* Tue Dec 14 2010 Jan Horak <jhorak@redhat.com> - 2.0-0.7.b7
- Enable mozilla crash reporter

* Thu Nov 11 2010 Dan Horák <dan[at]danny.cz> - 2.0-0.6.b7
- The s390 patch is not needed anymore

* Thu Nov 11 2010 Jan Horak <jhorak@redhat.com> - 2.0-0.5.b7
- Update to 2.0b7

* Thu Nov 4 2010 Christopher Aillon <caillon@redhat.com> 2.0-0.4.b6
- Ensure that WM_CLASS matches the desktop file

* Wed Nov 3 2010 Martin Stransky <stransky@redhat.com> 2.0-0.3.b6
- Libnotify rebuild (rhbz#649071)

* Wed Sep 29 2010 jkeating - 2.0-0.2b6
- Rebuilt for gcc bug 634757

* Tue Sep 21 2010 Martin Stransky <stransky@redhat.com> 2.0-0.1.b6
- Update to 2.0b6

* Tue Sep  7 2010 Tom "spot" Callaway <tcallawa@redhat.com> 1.9.3.0-0.2.b4
- spec file cleanup

* Fri Aug 27 2010 Martin Stransky <stransky@redhat.com> 1.9.3.0-0.1.b4
- Update to 1.9.3.1 beta 4

* Mon Aug 16 2010 Martin Stransky <stransky@redhat.com> 1.9.3.0-0.b3
- Update to 1.9.3.1 beta 3

* Tue Jul 20 2010 Jan Horak <jhorak@redhat.com> - 1.9.2.7-1
- Update to 1.9.2.7

* Wed Jul 1 2010 Martin Stransky <stransky@redhat.com> 1.9.2.6-2
- Disabled oopp on unsupported arches (rhbz#614363)

* Wed Jun 30 2010 Jan Horak <jhorak@redhat.com> - 1.9.2.6-1
- Update to 1.9.2.6

* Tue Jun 22 2010 Jan Horak <jhorak@redhat.com> - 1.9.2.4-1
- Update to 1.9.2.4

* Tue Jun 15 2010 Dan Horák <dan@danny.cz> 1.9.2.3-2
- Fixed build on s390

* Fri Apr 2 2010 Martin Stransky <stransky@redhat.com> 1.9.2.3-1
- Update to 1.9.2.3

* Tue Mar 23 2010 Jan Horak <jhorak@redhat.com> - 1.9.2.2-1
- Update to 1.9.2.2

* Mon Mar 15 2010 Colin Walters <walters@verbum.org> - 1.9.2.1-4
- Enable startup notification, closes #445543

* Thu Feb 18 2010 Jan Horak <jhorak@redhat.com> - 1.9.2.1-3
- Added fix for mozbz#462919 - Override NSS database path 
  for xulrunner application
       
* Wed Feb 17 2010 Martin Stransky <stransky@redhat.com> 1.9.2.1-2
- Added fix for #564184 - xulrunner-devel multilib conflict

* Fri Jan 22 2010 Martin Stransky <stransky@redhat.com> 1.9.2.1-1
- Update to 1.9.2.1

* Wed Jan 18 2010 Martin Stransky <stransky@redhat.com> 1.9.2.1-0.10.rc1
- Update to 1.9.2.1 RC2

* Wed Jan 13 2010 Martin Stransky <stransky@redhat.com> 1.9.2.1-0.9.rc1
- Update to 1.9.2.1 RC1

* Mon Dec 21 2009 Martin Stransky <stransky@redhat.com> 1.9.2.1-0.8.b5
- Update to 1.9.2.1 Beta 5

* Thu Dec 17 2009 Martin Stransky <stransky@redhat.com> 1.9.2.1-0.7.b4
- Added fix for mozbz#543585 - jemalloc alignment assertion 
  and abort on Linux

* Thu Dec 3 2009 Martin Stransky <stransky@redhat.com> 1.9.2.1-0.6.b4
- Added fix for #543585 - mozilla-plugin.pc contains incorrect CFLAGS

* Fri Nov 27 2009 Martin Stransky <stransky@redhat.com> 1.9.2.1-0.5.b4
- Update to 1.9.2.1 Beta 4

* Mon Nov 23 2009 Martin Stransky <stransky@redhat.com> 1.9.2.1-0.4.b3
- added -unstable.pc files for compatibility with 1.9.1

* Fri Nov 20 2009 Martin Stransky <stransky@redhat.com> 1.9.2.1-0.3.b3
- Necko wifi monitor disabled
- fixed a dependency (#539261)
- added source URL (#521704)

* Wed Nov 18 2009 Martin Stransky <stransky@redhat.com> 1.9.2.1-0.2.b3
- Rebase to 1.9.2.1 Beta 3

* Fri Nov 13 2009 Martin Stransky <stransky@redhat.com> 1.9.2.1-0.1.beta2
- Rebase to 1.9.2.1 Beta 2
- fix the sqlite runtime requires again (#480989), add a check 
  that the sqlite requires is sane (by Stepan Kasal)

* Thu Nov  5 2009 Jan Horak <jhorak@redhat.com> - 1.9.1.5-1
- Update to 1.9.1.5

* Mon Oct 26 2009 Jan Horak <jhorak@redhat.com> - 1.9.1.4-1
- Update to 1.9.1.4

* Mon Sep  7 2009 Jan Horak <jhorak@redhat.com> - 1.9.1.3-1
- Update to 1.9.1.3

* Fri Aug 21 2009 Jan Horak <jhorak@redhat.com> - 1.9.1.2-4
- Added libnotify support

* Wed Aug 12 2009 Martin Stransky <stransky@redhat.com> 1.9.1.2-3
- Added fix from #516118 - Headers not C89

* Mon Aug 6 2009 Martin Stransky <stransky@redhat.com> 1.9.1.2-2
- Rebuilt

* Mon Aug 3 2009 Martin Stransky <stransky@redhat.com> 1.9.1.2-1
- Update to 1.9.1.2

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jul 17 2009 Christopher Aillon <caillon@redhat.com> - 1.9.1.1-1
- Update to 1.9.1.1

* Mon Jul 13 2009 Jan Horak <jhorak@redhat.com> - 1.9.1-3
- Fixed wrong version of Firefox when loading 'about:' as location
- Added patch to compile against latest GTK

* Tue Jun 30 2009 Yanko Kaneti <yaneti@declera.com> - 1.9.1-2
- Build using system hunspell

* Tue Jun 30 2009 Christopher Aillon <caillon@redhat.com> 1.9.1-1
- Update to 1.9.1 final release

* Wed Jun 24 2009 Martin Stransky <stransky@redhat.com> 1.9.1-0.23
- Rebuilt because of gcc update (#506952)

* Thu Jun 18 2009 Martin Stransky <stransky@redhat.com> 1.9.1-0.22
- Backed out last change, it does not work inside mock (koji)

* Tue Jun 16 2009 Stepan Kasal <skasal@redhat.com> 1.9.1-0.21
- require sqlite of version >= what was used at buildtime (#480989)
- in devel subpackage, drop version from sqlite-devel require; that's
  handled indirectly through the versioned require in main package

* Mon Apr 27 2009 Christopher Aillon <caillon@redhat.com> 1.9.1-0.20
- 1.9.1 beta 4

* Fri Mar 27 2009 Christopher Aillon <caillon@redhat.com> 1.9.1-0.11
- Add patches for MFSA-2009-12, MFSA-2009-13

* Fri Mar 13 2009 Christopher Aillon <caillon@redhat.com> 1.9.1-0.10
- 1.9.1 beta 3

* Fri Feb 27 2009 Martin Stransky <stransky@redhat.com> 1.9.1-0.9
- Build fix for pango 1.23
- Misc. build fixes

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.1-0.8.beta2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jan 28 2009 Christopher Aillon <caillon@redhat.com> 1.9.1-0.7
- Re-enable NM by default

* Wed Jan  7 2009 Martin Stransky <stransky@redhat.com> 1.9.1-0.6
- Copied mozilla-config.h to stable include dir (#478445)

* Mon Dec 22 2008 Christopher Aillon <caillon@redhat.com> 1.9.1-0.5
- Typo fix

* Sat Dec 20 2008 Christopher Aillon <caillon@redhat.com> 1.9.1-0.4
- 1.9.1 beta 2

* Tue Dec  9 2008 Christopher Aillon <caillon@redhat.com> 1.9.1-0.3
- Mark this as a pre-release

* Tue Dec  9 2008 Christopher Aillon <caillon@redhat.com> 1.9.1-0.2
- Add needed -devel requires to the -devel package

* Thu Dec  4 2008 Christopher Aillon <caillon@redhat.com> 1.9.1-0.1
- 1.9.1 beta 1

* Wed Nov 12 2008 Christopher Aillon <caillon@redhat.com> 1.9.0.4-1
- Update to 1.9.0.4

* Mon Oct 27 2008 Christopher Aillon <caillon@redhat.com> 1.9.0.2-5
- Password manager fixes from upstream

* Tue Oct  7 2008 Marco Pesenti Gritti <mpg@redhat.com> 1.9.0.2-4
- Add missing dependency on python-devel

* Sun Oct  5 2008 Christopher Aillon <caillon@redhat.com> 1.9.0.2-3
- Enable PyXPCOM

* Thu Sep 25 2008 Martin Stransky <stransky@redhat.com> 1.9.0.2-2 
- Build with system cairo (#463341)

* Tue Sep 23 2008 Christopher Aillon <caillon@redhat.com> 1.9.0.2-1
- Update to 1.9.0.2

* Wed Jul 23 2008 Christopher Aillon <caillon@redhat.com> 1.9.0.1-2
- Disable system hunspell for now as it's causing some crashes (447444)

* Wed Jul 16 2008 Christopher Aillon <caillon@redhat.com> 1.9.0.1-1
- Update to 1.9.0.1

* Tue Jun 17 2008 Christopher Aillon <caillon@redhat.com> 1.9-1
- Update to 1.9 final

* Thu May 29 2008 Christopher Aillon <caillon@redhat.com> 1.9-0.63
- Simplify PS/PDF operators

* Thu May 22 2008 Christopher Aillon <caillon@redhat.com> 1.9-0.62
- Upstream patch to fsync() less

* Thu May 08 2008 Colin Walters <walters@redhat.com> 1.9-0.61
- Ensure we enable startup notification; add BR and modify config
  (bug #445543)

* Wed Apr 30 2008 Christopher Aillon <caillon@redhat.com> 1.9-0.60
- Some files moved to mozilla-filesystem; kill them and add the Req

* Mon Apr 28 2008 Christopher Aillon <caillon@redhat.com> 1.9-0.59
- Clean up the %%files list and get rid of the executable bit on some files

* Sat Apr 26 2008 Christopher Aillon <caillon@redhat.com> 1.9-0.58
- Fix font scaling

* Fri Apr 25 2008 Martin Stransky <stransky@redhat.com> 1.9-0.57
- Enabled phishing protection (#443403)

* Wed Apr 23 2008 Martin Stransky <stransky@redhat.com> 1.9-0.56
- Changed "__ppc64__" to "__powerpc64__", 
  "__ppc64__" doesn't work anymore
- Added fix for #443725 - Critical hanging bug with fix 
  available upstream (mozbz#429903)

* Fri Apr 18 2008 Martin Stransky <stransky@redhat.com> 1.9-0.55
- Fixed multilib issues, added starting script instead of a symlink
  to binary (#436393)

* Sat Apr 12 2008 Christopher Aillon <caillon@redhat.com> 1.9-0.54
- Add upstream patches for dpi, toolbar buttons, and invalid keys
- Re-enable system cairo

* Mon Apr  7 2008 Christopher Aillon <caillon@redhat.com> 1.9-0.53
- Spec cleanups

* Wed Apr  2 2008 Christopher Aillon <caillon@redhat.com> 1.9-0.52
- Beta 5

* Mon Mar 31 2008 Christopher Aillon <caillon@redhat.com> 1.9-0.51
- Beta 5 RC2

* Thu Mar 27 2008 Christopher Aillon <caillon@redhat.com> 1.9-0.50
- Update to latest trunk (2008-03-27)

* Wed Mar 26 2008 Christopher Aillon <caillon@redhat.com> 1.9-0.49
- Update to latest trunk (2008-03-26)

* Tue Mar 25 2008 Christopher Aillon <caillon@redhat.com> 1.9-0.48
- Update to latest trunk (2008-03-25)

* Mon Mar 24 2008 Christopher Aillon <caillon@redhat.com> 1.9-0.47
- Update to latest trunk (2008-03-24)

* Thu Mar 20 2008 Christopher Aillon <caillon@redhat.com> 1.9-0.46
- Update to latest trunk (2008-03-20)

* Mon Mar 17 2008 Christopher Aillon <caillon@redhat.com> 1.9-0.45
- Update to latest trunk (2008-03-17)

* Mon Mar 17 2008 Christopher Aillon <caillon@redhat.com> 1.9-0.44
- Revert to trunk from the 15th to fix crashes on HTTPS sites

* Sun Mar 16 2008 Christopher Aillon <caillon@redhat.com> 1.9-0.43
- Update to latest trunk (2008-03-16)
- Add patch to negate a11y slowdown on some pages (#431162)

* Sat Mar 15 2008 Christopher Aillon <caillon@redhat.com> 1.9-0.42
- Update to latest trunk (2008-03-15)

* Sat Mar 15 2008 Christopher Aillon <caillon@redhat.com> 1.9-0.41
- Avoid conflicts between gecko debuginfo packages

* Wed Mar 12 2008 Christopher Aillon <caillon@redhat.com> 1.9-0.40
- Update to latest trunk (2008-03-12)

* Tue Mar 11 2008 Christopher Aillon <caillon@redhat.com> 1.9-0.39
- Update to latest trunk (2008-03-11)

* Mon Mar 10 2008 Christopher Aillon <caillon@redhat.com> 1.9-0.38
- Update to latest trunk (2008-03-10)

* Sun Mar  9 2008 Christopher Aillon <caillon@redhat.com> 1.9-0.37
- Update to latest trunk (2008-03-09)

* Fri Mar  7 2008 Christopher Aillon <caillon@redhat.com> 1.9-0.beta4.36
- Update to latest trunk (2008-03-07)

* Thu Mar  6 2008 Christopher Aillon <caillon@redhat.com> 1.9-0.beta4.35
- Update to latest trunk (2008-03-06)

* Tue Mar  4 2008 Christopher Aillon <caillon@redhat.com> 1.9-0.beta4.34
- Update to latest trunk (2008-03-04)

* Sun Mar  2 2008 Christopher Aillon <caillon@redhat.com> 1.9-0.beta3.33
- Update to latest trunk (2008-03-02)

* Sat Mar  1 2008 Christopher Aillon <caillon@redhat.com> 1.9-0.beta3.32
- Update to latest trunk (2008-03-01)

* Fri Feb 29 2008 Christopher Aillon <caillon@redhat.com> 1.9-0.beta3.31
- Update to latest trunk (2008-02-29)

* Thu Feb 28 2008 Christopher Aillon <caillon@redhat.com> 1.9-0.beta3.30
- Update to latest trunk (2008-02-28)

* Wed Feb 27 2008 Christopher Aillon <caillon@redhat.com> 1.9-0.beta3.29
- Update to latest trunk (2008-02-27)

* Tue Feb 26 2008 Christopher Aillon <caillon@redhat.com> 1.9-0.beta3.28
- Update to latest trunk (2008-02-26)

* Sat Feb 23 2008 Christopher Aillon <caillon@redhat.com> 1.9-0.beta3.27
- Update to latest trunk (2008-02-23)

* Fri Feb 22 2008 Christopher Aillon <caillon@redhat.com> 1.9-0.beta3.26
- Update to latest trunk (2008-02-22)

* Thu Feb 21 2008 Christopher Aillon <caillon@redhat.com> 1.9-0.beta3.25
- Update to latest trunk (2008-02-21)

* Wed Feb 20 2008 Christopher Aillon <caillon@redhat.com> 1.9-0.beta3.24
- Update to latest trunk (2008-02-20)

* Sun Feb 17 2008 Christopher Aillon <caillon@redhat.com> 1.9-0.beta3.23
- Update to latest trunk (2008-02-17)

* Fri Feb 15 2008 Christopher Aillon <caillon@redhat.com> 1.9-0.beta3.22
- Update to latest trunk (2008-02-15)

* Thu Feb 14 2008 Christopher Aillon <caillon@redhat.com> 1.9-0.beta3.21
- Update to latest trunk (2008-02-14)
- Use system hunspell

* Mon Feb 11 2008 Christopher Aillon <caillon@redhat.com> 1.9-0.beta2.19
- Update to latest trunk (2008-02-11)

* Mon Feb 11 2008 Adam Jackson <ajax@redhat.com> 1.9-0.beta2.19
- STRIP="/bin/true" on the %%make line so xulrunner-debuginfo contains,
  you know, debuginfo.

* Sun Feb 10 2008 Christopher Aillon <caillon@redhat.com> 1.9-0.beta2.18
- Update to latest trunk (2008-02-10)

* Sat Feb  9 2008 Christopher Aillon <caillon@redhat.com> 1.9-0.beta2.17
- Update to latest trunk (2008-02-09)

* Wed Feb  6 2008 Christopher Aillon <caillon@redhat.com> 1.9-0.beta2.16
- Update to latest trunk (2008-02-06)

* Tue Jan 29 2008 Christopher Aillon <caillon@redhat.com> 1.9-0.beta2.15
- Update to latest trunk (2008-01-30)

* Wed Jan 25 2008 Martin Stransky <stransky@redhat.com> 1.9-0.beta2.14
- rebuild agains new nss
- enabled gnome vfs

* Wed Jan 23 2008 Martin Stransky <stransky@redhat.com> 1.9-0.beta2.13
- fixed stable pkg-config files (#429654)
- removed sqlite patch

* Mon Jan 21 2008 Christopher Aillon <caillon@redhat.com> 1.9-0.beta2.12
- Update to latest trunk (2008-01-21)

* Tue Jan 15 2008 Christopher Aillon <caillon@redhat.com> 1.9-0.beta2.11
- Update to latest trunk (2008-01-15)
- Now with system extensions directory support

* Sat Jan 13 2008 Christopher Aillon <caillon@redhat.com> 1.9-0.beta2.10
- Update to latest trunk (2008-01-13)
- Use CFLAGS instead of configure arguments
- Random cleanups: BuildRequires, scriptlets, prefs, etc.

* Sat Jan 12 2008 Christopher Aillon <caillon@redhat.com> 1.9-0.beta2.9
- Provide gecko-devel-unstable as well

* Wed Jan 9 2008 Martin Stransky <stransky@redhat.com> 1.9-0.beta2.8
- divided devel package to devel and devel-unstable

* Mon Jan 7 2008 Martin Stransky <stransky@redhat.com> 1.9-0.beta2.7
- removed fedora specific pkg-config files
- updated to the latest trunk (2008-01-07)
- removed unnecessary patches
- fixed idl dir (#427965)

* Thu Jan 3 2008 Christopher Aillon <caillon@redhat.com> 1.9-0.beta2.6
- Re-enable camellia256 support now that NSS supports it

* Thu Jan 3 2008 Martin Stransky <stransky@redhat.com> 1.9-0.beta2.5
- updated to the latest trunk (2008-01-03)

* Mon Dec 24 2007 Christopher Aillon <caillon@redhat.com> 1.9-0.beta2.4
- Don't Provide webclient (xulrunner is not itself a webclient)
- Don't Obsolete old firefox, only firefox-devel
- Kill legacy obsoletes (phoenix, etc) that were never in rawhide

* Thu Dec 21 2007 Martin Stransky <stransky@redhat.com> 1.9-0.beta2.3
- added java and plugin subdirs to plugin includes

* Thu Dec 20 2007 Martin Stransky <stransky@redhat.com> 1.9-0.beta2.2
- dependency fixes, obsoletes firefox < 3 and firefox-devel now

* Wed Dec 12 2007 Martin Stransky <stransky@redhat.com> 1.9-0.beta2.1
- updated to Beta 2.
- moved SDK to xulrunner-sdk

* Thu Dec 06 2007 Martin Stransky <stransky@redhat.com> 1.9-0.beta1.4
- fixed mozilla-plugin.pc (#412971)

* Tue Nov 27 2007 Martin Stransky <stransky@redhat.com> 1.9-0.beta1.3
- export /etc/gre.d/gre.conf (it's used by python gecko applications)

* Mon Nov 26 2007 Martin Stransky <stransky@redhat.com> 1.9-0.beta1.2
- added xulrunner/js include dir to xulrunner-js

* Tue Nov 20 2007 Martin Stransky <stransky@redhat.com> 1.9-0.beta1.1
- update to beta 1

* Mon Nov 19 2007 Martin Stransky <stransky@redhat.com> 1.9-0.alpha9.6
- packed all gecko libraries (#389391)

* Thu Nov 15 2007 Martin Stransky <stransky@redhat.com> 1.9-0.alpha9.5
- registered xulrunner libs system-wide
- added xulrunner-gtkmozembed.pc

* Wed Nov 14 2007 Martin Stransky <stransky@redhat.com> 1.9-0.alpha9.4
- added proper nss/nspr dependencies

* Wed Nov 14 2007 Martin Stransky <stransky@redhat.com> 1.9-0.alpha9.3
- more build fixes, use system nss libraries

* Tue Nov 6 2007 Martin Stransky <stransky@redhat.com> 1.9-0.alpha9.2
- build fixes

* Tue Oct 30 2007 Martin Stransky <stransky@redhat.com> 1.9-0.alpha9.1
- updated to the latest trunk

* Thu Sep 20 2007 David Woodhouse <dwmw2@infradead.org> 1.9-0.alpha7.4
- build fixes for ppc/ppc64

* Tue Sep 20 2007 Martin Stransky <stransky@redhat.com> 1.9-0.alpha7.3
- removed conflicts with the current gecko-based apps
- added updated ppc64 patch

* Tue Sep 18 2007 Martin Stransky <stransky@redhat.com> 1.9-0.alpha7.2
- build fixes

* Wed Sep  5 2007 Christopher Aillon <caillon@redhat.com> 1.9-0.alpha7.1
- Initial cut at XULRunner 1.9 Alpha 7
- Temporarily revert camellia 256 support since our nss doesn't support it yet
