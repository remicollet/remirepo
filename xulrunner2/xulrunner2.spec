# Minimal required versions
%global nspr_version 4.8.7
%global nss_version 3.12.9
%global cairo_version 1.10.0
%global freetype_version 2.1.9
%global sqlite_version 3.7.4
%global libnotify_version 0.7.0
%global lcms_version 1.18

%global shortname         xulrunner

%global version_internal  2
%global pretag            b10
%global mozappdir         %{_libdir}/%{shortname}-%{version_internal}
%global tarballdir        mozilla-central

# crash reporter and out-of-process-plugins work only on x86/x86_64
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

export LDFLAGS="-Wl,-rpath,%{mozappdir}"
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

INTERNAL_APP_SDK_NAME=%{shortname}-sdk-%{version_internal}
MOZ_APP_SDK_DIR=%{_libdir}/${INTERNAL_APP_SDK_NAME}

DESTDIR=$RPM_BUILD_ROOT make install

%{__mkdir_p} $RPM_BUILD_ROOT/%{mozappdir} \
             $RPM_BUILD_ROOT%{_datadir}/idl/${INTERNAL_APP_SDK_NAME} \
             $RPM_BUILD_ROOT%{_includedir}/${INTERNAL_APP_SDK_NAME}
%{__mkdir_p} $RPM_BUILD_ROOT{%{_libdir},%{_bindir},%{_datadir}/applications}

# set up our default preferences - (change Vendor to Remi, requested by upstream)
%{__cat} %{SOURCE12} | %{__sed} -e 's,RPM_VERREL,%{version}-%{release},g' -e 's,Fedora,Remi,g' | tee rh-default-prefs
%{__install} -p -D -m 644 rh-default-prefs $RPM_BUILD_ROOT/%{mozappdir}/defaults/pref/all-remi.js
%{__rm} rh-default-prefs

# Start script install
%{__rm} -rf $RPM_BUILD_ROOT%{_bindir}/%{shortname}
%{__cat} %{SOURCE21} | %{__sed} -e 's,XULRUNNER_VERSION,%{version_internal},g' > \
  $RPM_BUILD_ROOT%{_bindir}/%{name}
%{__chmod} 755 $RPM_BUILD_ROOT%{_bindir}/%{name}

%{__rm} -f $RPM_BUILD_ROOT%{mozappdir}/%{shortname}-config

cd $RPM_BUILD_ROOT%{mozappdir}/chrome
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
  $RPM_BUILD_ROOT/%{mozappdir}

%{__rm} -rf $RPM_BUILD_ROOT/%{_includedir}/%{shortname}-%{version_internal}
%{__rm} -rf $RPM_BUILD_ROOT/%{_datadir}/idl/%{shortname}-%{version_internal}

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
pushd $RPM_BUILD_ROOT%{mozappdir}
for i in *.so; do
    ln -s %{mozappdir}/$i $RPM_BUILD_ROOT${MOZ_APP_SDK_DIR}/sdk/lib/$i
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

#%{__mkdir_p} $RPM_BUILD_ROOT/etc/ld.so.conf.d
#%{__cat} > $RPM_BUILD_ROOT/etc/ld.so.conf.d/%{ld_conf_file} << EOF
#%{mozappdir}
#EOF
                        
# Copy over the LICENSE
%{__install} -p -c -m 644 LICENSE $RPM_BUILD_ROOT%{mozappdir}

# Use the system hunspell dictionaries
%{__rm} -rf ${RPM_BUILD_ROOT}%{mozappdir}/dictionaries
ln -s %{_datadir}/myspell ${RPM_BUILD_ROOT}%{mozappdir}/dictionaries

# ghost files
%{__mkdir_p} $RPM_BUILD_ROOT%{mozappdir}/components
touch $RPM_BUILD_ROOT%{mozappdir}/components/compreg.dat
touch $RPM_BUILD_ROOT%{mozappdir}/components/xpti.dat

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

%if %{name} == %{shortname}
%preun
# is it a final removal?
if [ $1 -eq 0 ]; then
  %{__rm} -rf %{mozappdir}/components
fi
%endif

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
#%{_sysconfdir}/ld.so.conf.d/xulrunner*.conf
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


