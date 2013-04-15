# Use system nspr/nss?
%if 0%{?fedora} < 17
%define system_nss        0
%else
%define system_nss        1
%endif

%if 0%{?fedora} < 15
%define system_vpx        0
%else
%define system_vpx        1
%endif

# Use system sqlite?
%if 0%{?fedora} < 19
%define system_sqlite     0
%else
%define system_sqlite     1
%endif

# Use system libpeg (and libjpeg-turbo) ?
%if 0%{?fedora} < 14 && 0%{?rhel} < 6
%define system_jpeg       0
%else
%define system_jpeg       1
%endif

# Use system cairo?
%define system_cairo      0

%global shortname         xulrunner

# Build as a debug package?
%define debug_build       0

# Minimal required versions
%global cairo_version 1.10.2
%global freetype_version 2.1.9
%global libnotify_version 0.7.0
%global libvpx_version 1.0.0

%if %{?system_nss}
# grep 'min_ns.*=[0-9]' configure
%global nspr_version 4.9.4
%global nspr_build_version %(pkg-config --silence-errors --modversion nspr 2>/dev/null || echo 65536)
%global nss_version 3.14.3
%global nss_build_version %(pkg-config --silence-errors --modversion nss 2>/dev/null || echo 65536)
%endif

%if %{?system_sqlite}
# grep '^SQLITE_VERSION' configure
%global sqlite_version 3.7.15.2
# The actual sqlite version (see #480989):
%global sqlite_build_version %(pkg-config --silence-errors --modversion sqlite3 2>/dev/null || echo 65536)
%endif

# gecko_dir_ver should be set to the version in our directory names
# alpha_version should be set to the alpha number if using an alpha, 0 otherwise
# beta_version  should be set to the beta number if using a beta, 0 otherwise
# rc_version    should be set to the RC number if using an RC, 0 otherwise
%global gecko_dir_ver %{version}
%global alpha_version 0
%global beta_version  0
%global rc_version    0

%global tarballname   firefox
%global mozappdir     %{_libdir}/%{name}
%global tarballdir    mozilla-release

# no crash reporter for remi repo
%global enable_mozilla_crashreporter 0

%if %{alpha_version} > 0
%global pre_version a%{alpha_version}
%global tarballdir  mozilla-beta
%endif
%if %{beta_version} > 0
%global pre_version b%{beta_version}
%global tarballdir  mozilla-beta
%endif
%if %{rc_version} > 0
%global pre_version rc%{rc_version}
%global tarballdir  mozilla-release
%endif

%if %{defined pre_version}
%global gecko_verrel %{expand:%%{version}}-%{pre_version}
%global pre_tag .%{pre_version}
%else
%global gecko_verrel %{expand:%%{version}}
%endif

Summary:        XUL Runtime for Gecko Applications
Name:           %{shortname}-last
Version:        20.0.1
Release:        1%{?pre_tag}%{?dist}
URL:            http://developer.mozilla.org/En/XULRunner
License:        MPLv1.1 or GPLv2+ or LGPLv2+
Group:          Applications/Internet
Source0:        ftp://ftp.mozilla.org/pub/%{tarballname}/releases/%{version}%{?pre_version}/source/%{tarballname}-%{version}%{?pre_version}.source.tar.bz2
Source10:       %{shortname}-mozconfig
Source11:       %{shortname}-mozconfig-debuginfo
Source12:       %{shortname}-redhat-default-prefs.js
Source21:       %{shortname}.sh.in

# build patches
Patch1:         xulrunner-install-dir.patch
Patch2:         mozilla-build.patch
Patch14:        xulrunner-2.0-chromium-types.patch
Patch17:        xulrunner-15.0-gcc47.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=814879#c3
Patch18:        xulrunner-16.0-jemalloc-ppc.patch
Patch19:        rhbz-304121.patch

# Fedora specific patches
Patch20:        mozilla-193-pkgconfig.patch
Patch21:        rhbz-911314.patch
Patch22:        rhbz-928353.patch

# Upstream patches
Patch101:       mozilla-791626.patch
Patch102:       mozilla-239254.patch
Patch104:       mozilla-844883.patch

# ---------------------------------------------------

%if %{?system_nss}
BuildRequires:  nspr-devel >= %{nspr_version}
BuildRequires:  nss-devel >= %{nss_version}
BuildRequires:  nss-static >= %{nss_version}
%endif
%if %{?system_cairo}
BuildRequires:  cairo-devel >= %{cairo_version}
%endif
BuildRequires:  libpng-devel
%if %{system_jpeg}
BuildRequires:  libjpeg-turbo-devel
%endif
BuildRequires:  zip
BuildRequires:  bzip2-devel
BuildRequires:  zlib-devel
BuildRequires:  libIDL-devel
BuildRequires:  gtk2-devel
BuildRequires:  krb5-devel
BuildRequires:  pango-devel
BuildRequires:  freetype-devel >= %{freetype_version}
BuildRequires:  libXt-devel
BuildRequires:  libXrender-devel
BuildRequires:  hunspell-devel
BuildRequires:  startup-notification-devel
BuildRequires:  alsa-lib-devel
BuildRequires:  libnotify-devel
BuildRequires:  mesa-libGL-devel
BuildRequires:  curl-devel
%if %{system_vpx}
BuildRequires:  libvpx-devel >= %{libvpx_version}
%endif
#BuildRequires:  autoconf213
BuildRequires:  yasm

Requires:       mozilla-filesystem
Requires:       liberation-sans-fonts
%if %{?system_nss}
Requires:       nspr >= %{nspr_build_version}
Requires:       nss >= %{nss_build_version}
%endif
Provides:       gecko-libs = %{gecko_verrel}
Provides:       gecko-libs%{?_isa} = %{gecko_verrel}
Obsoletes:      xulrunner13
Obsoletes:      xulrunner14
Obsoletes:      xulrunner15
Obsoletes:      xulrunner16

%if %{?system_sqlite}
BuildRequires:  sqlite-devel >= %{sqlite_version}
Requires:       sqlite >= %{sqlite_build_version}
%endif

%description
XULRunner is a Mozilla runtime package that can be used to bootstrap XUL+XPCOM
applications that are as rich as Firefox and Thunderbird. It provides mechanisms
for installing, upgrading, and uninstalling these applications. XULRunner also
provides libxul, a solution which allows the embedding of Mozilla technologies
in other projects and products.

%package devel
Summary: Development files for Gecko
Group: Development/Libraries
Obsoletes: mozilla-devel < 1.9
Obsoletes: firefox-devel < 2.1
Obsoletes: xulrunner-devel-unstable
Obsoletes: xulrunner13-devel
Obsoletes: xulrunner14-devel
Obsoletes: xulrunner15-devel
Obsoletes: xulrunner16-devel
Provides: gecko-devel = %{gecko_verrel}
Provides: gecko-devel%{?_isa} = %{gecko_verrel}
Provides: gecko-devel-unstable = %{gecko_verrel}
Provides: gecko-devel-unstable%{?_isa} = %{gecko_verrel}

Requires: %{name}%{?_isa} = %{version}-%{release}
%if %{?system_nss}
Requires: nspr-devel >= %{nspr_build_version}
Requires: nss-devel >= %{nss_build_version}
%endif
%if %{?system_cairo}
# Library requirements (cairo-tee >= 1.10)
Requires: cairo-devel >= %{cairo_version}
%endif
%if %{system_jpeg}
Requires: libjpeg-turbo-devel
%endif
Requires: zip
Requires: bzip2-devel
Requires: zlib-devel
Requires: libIDL-devel
Requires: gtk2-devel
Requires: krb5-devel
Requires: pango-devel
Requires: freetype-devel >= %{freetype_version}
Requires: libXt-devel
Requires: libXrender-devel
Requires: hunspell-devel
%if %{?system_sqlite}
Requires: sqlite-devel >= %{sqlite_build_version}
%endif
Requires: startup-notification-devel
Requires: alsa-lib-devel
Requires: libnotify-devel
Requires: mesa-libGL-devel
%if %{system_vpx}
Requires: libvpx-devel >= %{libvpx_version}
%endif
Requires: yasm

%description devel
This package contains the libraries amd header files that are needed
for writing XUL+XPCOM applications with Mozilla XULRunner and Gecko.

%if %{enable_mozilla_crashreporter}
%global moz_debug_prefix %{_prefix}/lib/debug
%global moz_debug_dir %{moz_debug_prefix}%{mozappdir}
%global uname_m %(uname -m)
%global symbols_file_name %{shortname}-%{version}.en-US.%{_os}-%{uname_m}.crashreporter-symbols.zip
%global symbols_file_path %{moz_debug_dir}/%{symbols_file_name}
%global _find_debuginfo_opts -p %{symbols_file_path} -o debugcrashreporter.list
%global crashreporter_pkg_name mozilla-crashreporter-%{name}-debuginfo
%package -n %{crashreporter_pkg_name}
Summary: Debugging symbols used by Mozilla's crash reporter servers
Group: Development/Debug
%description -n %{crashreporter_pkg_name}
This package provides debug information for XULRunner, for use by
Mozilla's crash reporter servers.  If you are trying to locally
debug %{name}, you want to install %{name}-debuginfo instead.
%files -n %{crashreporter_pkg_name} -f debugcrashreporter.list
%defattr(-,root,root)
%endif

#---------------------------------------------------------------------

%prep
echo TARGET = %{name}-%{version}-%{release}  GECKO = %{gecko_verrel}
%setup -q -c
cd %{tarballdir}

%patch1  -p1
%patch2  -p1 -b .build
%patch14 -p2 -b .chromium-types
%patch17 -p2 -b .gcc47
%patch18 -p2 -b .jemalloc-ppc
%patch19 -p2 -b .rhbz-304121

%patch20  -p2 -b .pk
%ifarch ppc ppc64
%patch21  -p1 -b .ppc
%patch104 -p1 -b .844883
%endif

%if 0%{?fedora} >= 19
%ifarch %{ix86}
%patch22  -p2
%endif
%endif

%patch101 -p1 -b .791626
%patch102 -p1 -b .239254

%{__rm} -f .mozconfig
%{__cat} %{SOURCE10} \
%if ! %{system_vpx}
  | grep -v with-system-libvpx     \
%endif
%if ! %{system_jpeg}
  | grep -v with-system-jpeg     \
%endif
  | tee .mozconfig

%if %{enable_mozilla_crashreporter}
%{__cat} %{SOURCE11} >> .mozconfig
%endif

%if %{?system_nss}
echo "ac_add_options --with-system-nspr" >> .mozconfig
echo "ac_add_options --with-system-nss" >> .mozconfig
%else
echo "ac_add_options --without-system-nspr" >> .mozconfig
echo "ac_add_options --without-system-nss" >> .mozconfig
%endif

%if %{?system_sqlite}
echo "ac_add_options --enable-system-sqlite" >> .mozconfig
%else
echo "ac_add_options --disable-system-sqlite" >> .mozconfig
%endif

%if %{?system_cairo}
echo "ac_add_options --enable-system-cairo" >> .mozconfig
%else
echo "ac_add_options --disable-system-cairo" >> .mozconfig
%endif

%if %{?debug_build}
echo "ac_add_options --enable-debug" >> .mozconfig
echo "ac_add_options --disable-optimize" >> .mozconfig
%else
echo "ac_add_options --disable-debug" >> .mozconfig
echo "ac_add_options --enable-optimize" >> .mozconfig
%endif

# s390(x) fails to start with jemalloc enabled
%ifarch s390 s390x
echo "ac_add_options --disable-jemalloc" >> .mozconfig
%endif

%ifarch armv7hl
echo "ac_add_options --with-arch=armv7-a" >> .mozconfig
echo "ac_add_options --with-float-abi=hard" >> .mozconfig
echo "ac_add_options --with-fpu=vfpv3-d16" >> .mozconfig
echo "ac_add_options --disable-elf-hack" >> .mozconfig
%endif
%ifarch armv7hnl
echo "ac_add_options --with-arch=armv7-a" >> .mozconfig
echo "ac_add_options --with-float-abi=hard" >> .mozconfig
echo "ac_add_options --with-fpu=neon" >> .mozconfig
echo "ac_add_options --disable-elf-hack" >> .mozconfig
%endif
%ifarch armv5tel
echo "ac_add_options --with-arch=armv5te" >> .mozconfig
echo "ac_add_options --with-float-abi=soft" >> .mozconfig
echo "ac_add_options --disable-elf-hack" >> .mozconfig
%endif

%ifnarch %{ix86} x86_64 armv7hl armv7hnl
echo "ac_add_options --disable-methodjit" >> .mozconfig
echo "ac_add_options --disable-monoic" >> .mozconfig
echo "ac_add_options --disable-polyic" >> .mozconfig
echo "ac_add_options --disable-tracejit" >> .mozconfig
%endif

%ifnarch %{ix86} x86_64
echo "ac_add_options --disable-webrtc" >> .mozconfig
%endif

#---------------------------------------------------------------------

%build
%if %{?system_sqlite}
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
MOZ_OPT_FLAGS=$(echo "$RPM_OPT_FLAGS" | %{__sed} -e 's/-Wall//')
%if %{?debug_build}
MOZ_OPT_FLAGS=$(echo "$MOZ_OPT_FLAGS" | %{__sed} -e 's/-O2//')
%endif
%ifarch s390
MOZ_OPT_FLAGS=$(echo "$MOZ_OPT_FLAGS" | %{__sed} -e 's/-g/-g1/')
%endif
%ifarch s390 %{arm} ppc
MOZ_LINK_FLAGS="-Wl,--no-keep-memory -Wl,--reduce-memory-overheads"
%endif

export CFLAGS=$MOZ_OPT_FLAGS
export CXXFLAGS="$MOZ_OPT_FLAGS -fpermissive"
export LDFLAGS=$MOZ_LINK_FLAGS

export PREFIX='%{_prefix}'
export LIBDIR='%{_libdir}'

MOZ_SMP_FLAGS=-j1
# On x86 architectures, Mozilla can build up to 4 jobs at once in parallel,
# however builds tend to fail on other arches when building in parallel.
%ifarch %{ix86} x86_64 ppc ppc64
[ -z "$RPM_BUILD_NCPUS" ] && \
     RPM_BUILD_NCPUS="`/usr/bin/getconf _NPROCESSORS_ONLN`"
[ "$RPM_BUILD_NCPUS" -ge 2 ] && MOZ_SMP_FLAGS=-j2
[ "$RPM_BUILD_NCPUS" -ge 4 ] && MOZ_SMP_FLAGS=-j4
[ "$RPM_BUILD_NCPUS" -ge 8 ] && MOZ_SMP_FLAGS=-j8
%endif

export LDFLAGS="-Wl,-rpath,%{mozappdir}"
make -f client.mk build STRIP="/bin/true" MOZ_MAKE_FLAGS="$MOZ_SMP_FLAGS" MOZ_SERVICES_SYNC="1"

# create debuginfo for crash-stats.mozilla.com
%if %{enable_mozilla_crashreporter}
#cd %{moz_objdir}
make -C objdir buildsymbols
%endif

#---------------------------------------------------------------------

%install
cd %{tarballdir}

# set up our prefs before install, so it gets pulled in to omni.jar
%{__cp} -p %{SOURCE12} objdir/dist/bin/defaults/pref/all-redhat.js

DESTDIR=$RPM_BUILD_ROOT make -C objdir install

# Start script install
%{__rm} -rf $RPM_BUILD_ROOT%{_bindir}/%{shortname}
%{__cat} %{SOURCE21} | %{__sed} -e 's,XULRUNNER_VERSION,%{gecko_dir_ver},g' > \
  $RPM_BUILD_ROOT%{_bindir}/%{name}
%{__chmod} 755 $RPM_BUILD_ROOT%{_bindir}/%{name}

%{__rm} -f $RPM_BUILD_ROOT%{mozappdir}/%{shortname}-config

# Copy pc files (for compatibility with 1.9.1)
%{__cp} $RPM_BUILD_ROOT/%{_libdir}/pkgconfig/libxul.pc \
        $RPM_BUILD_ROOT/%{_libdir}/pkgconfig/libxul-unstable.pc
%{__cp} $RPM_BUILD_ROOT/%{_libdir}/pkgconfig/libxul-embedding.pc \
        $RPM_BUILD_ROOT/%{_libdir}/pkgconfig/libxul-embedding-unstable.pc

# Fix multilib devel conflicts...
function install_file() {
genheader=$*
mv ${genheader}.h ${genheader}%{__isa_bits}.h
cat > ${genheader}.h << EOF
/* This file exists to fix multilib conflicts */
#if defined(__x86_64__) || defined(__ia64__) || defined(__s390x__) || defined(__powerpc64__) || (defined(__sparc__) && defined(__arch64__))
#include "${genheader}64.h"
#else
#include "${genheader}32.h"
#endif
EOF
}

INTERNAL_APP_NAME=%{shortname}-%{gecko_dir_ver}

pushd $RPM_BUILD_ROOT/%{_includedir}/${INTERNAL_APP_NAME}
install_file "mozilla-config"
install_file "js-config"
popd

# Link libraries in sdk directory instead of copying them:
pushd $RPM_BUILD_ROOT%{_libdir}/%{shortname}-devel-%{gecko_dir_ver}/sdk/lib
for i in *.so; do
     rm $i
     ln -s %{mozappdir}/$i $i
done
popd

%if ! %{system_nss}
%{__install} -D -p -m 755 \
   objdir/dist/sdk/bin/nspr-config \
   $RPM_BUILD_ROOT%{_libdir}/%{shortname}-devel-%{gecko_dir_ver}/sdk/bin/nspr-config
%endif

# Library path
LD_SO_CONF_D=%{_sysconfdir}/ld.so.conf.d
LD_CONF_FILE=xulrunner-%{__isa_bits}.conf

%if "%{name}" == "%{shortname}"
%{__mkdir_p} ${RPM_BUILD_ROOT}${LD_SO_CONF_D}
%{__cat} > ${RPM_BUILD_ROOT}${LD_SO_CONF_D}/${LD_CONF_FILE} << EOF
%{mozappdir}
EOF
%endif

# Copy over the LICENSE
%{__install} -p -c -m 644 LICENSE $RPM_BUILD_ROOT%{mozappdir}

# Install xpcshell
%{__cp} objdir/dist/bin/xpcshell $RPM_BUILD_ROOT/%{mozappdir}

# Fix libxpcom.so rights
chmod 755 $RPM_BUILD_ROOT/%{mozappdir}/libxpcom.so

# Install run-mozilla.sh
%{__cp} objdir/dist/bin/run-mozilla.sh $RPM_BUILD_ROOT/%{mozappdir}

# Use the system hunspell dictionaries
%{__rm} -rf ${RPM_BUILD_ROOT}%{mozappdir}/dictionaries
ln -s %{_datadir}/myspell ${RPM_BUILD_ROOT}%{mozappdir}/dictionaries

# Remove tmp files
find $RPM_BUILD_ROOT/%{mozappdir} -name '.mkdir.done' -exec rm -rf {} \;

# ghost files
%{__mkdir_p} $RPM_BUILD_ROOT%{mozappdir}/components
touch $RPM_BUILD_ROOT%{mozappdir}/components/compreg.dat
touch $RPM_BUILD_ROOT%{mozappdir}/components/xpti.dat

# Add debuginfo for crash-stats.mozilla.com 
%if %{enable_mozilla_crashreporter}
%{__mkdir_p} $RPM_BUILD_ROOT/%{moz_debug_dir}
%{__cp} objdir/dist/%{symbols_file_name} $RPM_BUILD_ROOT/%{moz_debug_dir}
%endif

#---------------------------------------------------------------------

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%if "%{name}" == "%{shortname}"
%preun
# is it a final removal?
if [ $1 -eq 0 ]; then
  %{__rm} -rf %{mozappdir}/components
fi
%endif

%files
%defattr(-,root,root,-)
%{_bindir}/%{name}
%dir %{mozappdir}
%doc %attr(644, root, root) %{mozappdir}/LICENSE
%doc %attr(644, root, root) %{mozappdir}/README.xulrunner
%{mozappdir}/chrome
%{mozappdir}/chrome.manifest
%{mozappdir}/dictionaries
%dir %{mozappdir}/components
%ghost %{mozappdir}/components/compreg.dat
%ghost %{mozappdir}/components/xpti.dat
%{mozappdir}/components/*.so
%{mozappdir}/components/*.manifest
%{mozappdir}/omni.ja
%{mozappdir}/*.so
%{mozappdir}/mozilla-xremote-client
%{mozappdir}/run-mozilla.sh
%{mozappdir}/xulrunner
%{mozappdir}/xulrunner-stub
%{mozappdir}/platform.ini
%{mozappdir}/dependentlibs.list
%if "%{name}" == "%{shortname}"
%{_sysconfdir}/ld.so.conf.d/xulrunner*.conf
%endif
%{mozappdir}/plugin-container
%if !%{?system_nss}
%{mozappdir}/*.chk
%endif
%if %{enable_mozilla_crashreporter}
%{mozappdir}/crashreporter
%{mozappdir}/crashreporter.ini
%{mozappdir}/Throbber-small.gif
%endif

%files devel
%defattr(-,root,root,-)
%dir %{_libdir}/%{shortname}-devel-*
%{_datadir}/idl/%{shortname}*%{gecko_dir_ver}
%{_includedir}/%{shortname}*%{gecko_dir_ver}
%{_libdir}/%{shortname}-devel-*/*
%{_libdir}/pkgconfig/*.pc
%{mozappdir}/xpcshell
%{mozappdir}/js-gdb.py
%ghost %{mozappdir}/js-gdb.pyc
%ghost %{mozappdir}/js-gdb.pyo


#---------------------------------------------------------------------

%changelog
* Mon Apr 15 2013 Remi Collet <RPMS@FamilleCollet.com> - 20.0.1-1
- Update to 20.0.1, sync with rawhide

* Fri Apr 5 2013 Martin Stransky <stransky@redhat.com> - 20.0-4
- Updated rhbz-911314.patch for xulrunner 20

* Wed Apr  3 2013 Remi Collet <RPMS@FamilleCollet.com> - 20.0-1
- Update to 20.0, sync with rawhide

* Wed Apr 3 2013 Martin Stransky <stransky@redhat.com> - 20.0-3
- A workaround for Bug 928353 - firefox i686 crashes
  for a number of web pages

* Tue Mar 19 2013 Martin Stransky <stransky@redhat.com> - 20.0-1
- Update to latest upstream (20.0)

* Tue Mar 19 2013 Martin Stransky <stransky@redhat.com> - 19.0.2-4
- Added fix for rhbz#913284 - Firefox segfaults
  in mozilla::gfx::AlphaBoxBlur::BoxBlur_C() on PPC64

* Tue Mar 19 2013 Martin Stransky <stransky@redhat.com> - 19.0.2-3
- Added fix for mozbz#826171/rhbz#922904 - strndup implementation
  in memory/build/mozmemory_wrap.c is broken

* Fri Mar  8 2013 Remi Collet <RPMS@FamilleCollet.com> - 19.0.2-1
- Update to 19.0.2 (security)

* Sat Feb 23 2013 Remi Collet <RPMS@FamilleCollet.com> - 19.0-1
- Update to 19.0

* Wed Feb 20 2013 Martin Stransky <stransky@redhat.com> - 19.0-2
- Added fix for rhbz#911314 (ppc only)

* Mon Feb 18 2013 Martin Stransky <stransky@redhat.com> - 19.0-1
- Update to 19.0
- Added fix for mozbz#239254

* Wed Feb  6 2013 Remi Collet <RPMS@FamilleCollet.com> - 18.0.2-1
- Update to 18.0.2

* Mon Jan 21 2013 Remi Collet <RPMS@FamilleCollet.com> - 18.0.1-1
- Update to 18.0.1

* Tue Jan 15 2013 Martin Stransky <stransky@redhat.com> - 18.0-8
- Added fix for NM regression (mozbz#791626)

* Sun Jan 13 2013 Remi Collet <RPMS@FamilleCollet.com> - 18.0-2
- sync with rawhide, re-enable webrtc

* Thu Jan 10 2013 Martin Stransky <stransky@redhat.com> - 18.0-7
- Fixed Makefile generator (rhbz#304121)

* Wed Jan 9 2013 Remi Collet <RPMS@FamilleCollet.com> - 18.0-1
- Sync with rawhide, Update to 18.0
- use bunled libjpeg-turbo on EL-6

* Wed Jan 9 2013 Martin Stransky <stransky@redhat.com> - 18.0-6
- Fixed missing libxpcom.so provides

* Wed Jan 9 2013 Martin Stransky <stransky@redhat.com> - 18.0-5
- Added fix for langpacks

* Wed Jan 9 2013 Martin Stransky <stransky@redhat.com> - 18.0-4
- Fixed source files
- Disabled WebRTC due to rhbz#304121

* Wed Jan 9 2013 Martin Stransky <stransky@redhat.com> - 18.0-2
- Disabled system sqlite on Fedora 18

* Mon Jan 7 2013 Martin Stransky <stransky@redhat.com> - 18.0-1
- Update to 18.0

* Thu Dec 13 2012 Peter Robinson <pbrobinson@fedoraproject.org> 17.0.1-3
- Disable webrtc on ARM as it currently tries to build SSE on ARM (fix FTBFS)
- Enable methodjit/tracejit on ARMv7 for more speed :) Fixes RHBZ 870548

* Thu Nov 29 2012 Remi Collet <RPMS@FamilleCollet.com> - 17.0-1
- Sync with rawhide, Update to 17.0.1

* Thu Nov 29 2012 Jan Horak <jhorak@redhat.com> - 17.0.1-1
- Update to 17.0.1

* Tue Nov 27 2012 Jan Horak <jhorak@redhat.com> - 17.0-4
- Rebuild agains older NSS

* Mon Nov 19 2012 Martin Stransky <stransky@redhat.com> - 17.0-3
- Updated second arch patches

* Mon Nov 19 2012 Dan Horák <dan[at]danny.cz> - 17.0-2
- webrtc is available only on selected arches

* Mon Nov 19 2012 Remi Collet <RPMS@FamilleCollet.com> - 17.0-1
- Update to 17.0

* Mon Nov 19 2012 Martin Stransky <stransky@redhat.com> - 17.0-1
- Update to 17.0

* Sun Nov 18 2012 Remi Collet <RPMS@FamilleCollet.com> - 17.0-0.2.b6
- Update to 17.0 Beta 6, sync with rawhide

* Wed Nov 14 2012 Martin Stransky <stransky@redhat.com> - 17.0-0.2b6
- Update to 17.0 Beta 6

* Tue Nov 13 2012 Martin Stransky <stransky@redhat.com> - 17.0-0.1b5
- Update to 17.0 Beta 5

* Tue Nov 6 2012 Martin Stransky <stransky@redhat.com> - 16.0.2-2
- Added fix for rhbz#872752

* Thu Nov  1 2012 Remi Collet <RPMS@FamilleCollet.com> - 16.0.2-1
- sync patch with rawhide
- rename to xulrunner-last

* Wed Oct 31 2012 Martin Stransky <stransky@redhat.com> - 16.0.2-1
- Updated mozilla-746112.patch for second arches
- Removed unused one (rhbz#855919)

* Fri Oct 26 2012 Remi Collet <RPMS@FamilleCollet.com> - 16.0.2-1
- Sync with rawhide, update to 16.0.2

* Fri Oct 26 2012 Jan Horak <jhorak@redhat.com> - 16.0.2-1
- Update to 16.0.2

* Tue Oct 16 2012 Jan Horak <jhorak@redhat.com> - 16.0.1-2
- Fixed required nss and nspr version

* Thu Oct 11 2012 Remi Collet <RPMS@FamilleCollet.com> - 16.0.1-1
- Sync with rawhide, update to 16.0.1

* Thu Oct 11 2012 Martin Stransky <stransky@redhat.com> - 16.0.1-1
- Update to 16.0.1

* Mon Oct 8 2012 Remi Collet <RPMS@FamilleCollet.com> - 16.0-1
- Sync with rawhide, update to 16.0

* Mon Oct 8 2012 Martin Stransky <stransky@redhat.com> - 16.0-1
- Update to 16.0

* Thu Sep 27 2012 Jan Horak <jhorak@redhat.com> - 15.0.1-4
- Rebuild with latest gcc to fix rhbz#830017

* Mon Sep 17 2012 Martin Stransky <stransky@redhat.com> - 15.0.1-3
- Added fix for rhbz#855919 - Firefox freezes on Fedora 18 for PPC64

* Fri Sep 14 2012 Martin Stransky <stransky@redhat.com> - 15.0.1-2
- Added build flags for second arches

* Sun Sep  9 2012 Remi Collet <RPMS@FamilleCollet.com> - 15.0.1-1
- update to 15.0.1

* Tue Aug 28 2012 Remi Collet <RPMS@FamilleCollet.com> - 15.0-1
- Sync with rawhide, update to 15.0

* Wed Aug 22 2012 Martin Stransky <stransky@redhat.com> - 15.0-2
- Update to 15.0

* Thu Aug  9 2012 Jan Horak <jhorak@redhat.com> - 14.0.1-6
- Added fix for mozbz#709732

* Wed Jul 25 2012 Dan Horák <dan[at]danny.cz> - 14.0.1-5
- Added fix for secondary arches - mozbz#750620

* Tue Jul 24 2012 Remi Collet <RPMS@FamilleCollet.com> - 14.0.1-1
- Sync with rawhide, update to 14.0.1

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 14.0.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul 16 2012 Martin Stransky <stransky@redhat.com> - 14.0.1-3
- Update to 14.0.1

* Sun Jun 16 2012 Remi Collet <RPMS@FamilleCollet.com> - 13.0.1-1
- Sync with rawhide, update to 13.0.1

* Sat Jun 16 2012 Jan Horak <jhorak@redhat.com> - 13.0.1-1
- Update to 13.0.1

* Wed Jun 06 2012 Remi Collet <RPMS@FamilleCollet.com> - 13.0-1
- Sync with rawhide, update to 13.0

* Wed Jun 5 2012 Martin Stransky <stransky@redhat.com> - 13.0-2
- src.rpm should include all patches

* Mon Jun 4 2012 Martin Stransky <stransky@redhat.com> - 13.0-1
- Update to 13.0

* Mon May 28 2012 Martin Stransky <stransky@redhat.com> - 12.0-7
- More ppc(64) fixes - mozbz#746112

* Mon May 28 2012 Martin Stransky <stransky@redhat.com> - 12.0-6
- Added workaround for ppc(64) - mozbz#746112

* Mon May 7 2012 Dan Horák <dan[at]danny.cz> - 12.0-5
- Used backported upstream patch from mozb#734335 for fixing the sps profiler build
- Fixed build of jemalloc on ppc (patch by Gustavo Luiz Duarte/IBM)

* Fri May 4 2012 Dan Horák <dan[at]danny.cz> - 12.0-4
- Added new patch for 691898 - backport from trunk
- Added build fix for secondary arches

* Fri May 4 2012 Martin Stransky <stransky@redhat.com> - 12.0-3
- Added requires for nss-static (rhbz#717247)

* Mon Apr 30 2012 Martin Stransky <stransky@redhat.com> - 12.0-2
- Enable ppc(64) paralell builds (rhbz#816612)

* Sun Apr 29 2012 Remi Collet <RPMS@FamilleCollet.com> - 12.0-1
- Sync with rawhide, update to 12.0

* Tue Apr 24 2012 Martin Stransky <stransky@redhat.com> - 12.0-1
- Update to 12.0

* Sat Mar 17 2012 Remi Collet <RPMS@FamilleCollet.com> - 11.0-1
- update to 11.0, sync with rawhide

* Tue Mar 13 2012 Martin Stransky <stransky@redhat.com> - 11.0-3
- Update to 11.0
- Fixed libvpx-devel dependency

* Fri Mar 9 2012 Martin Stransky <stransky@redhat.com> - 11.0-1
- Update to 11.0 Beta 7

* Fri Mar 09 2012 Dan Horák <dan[at]danny.cz> - 10.0.1-5
- Add fix for secondary arches from mozb#691898

* Mon Feb 27 2012 Martin Stransky <stransky@redhat.com> - 10.0.1-4
- Added fix from rhbz#796929 - xulrunner doesn't compile on ARM

* Sat Feb 18 2012 Remi Collet <RPMS@FamilleCollet.com> - 10.0.2-1
- update to 10.0.2

* Tue Feb 16 2012 Martin Stransky <stransky@redhat.com> - 10.0.1-3
- Added fix for mozbz#727401

* Tue Feb 14 2012 Martin Stransky <stransky@redhat.com> - 10.0.1-2
- Allow network manager to handle the offline status

* Thu Feb 09 2012 Remi Collet <RPMS@FamilleCollet.com> - 10.0.1-1
- update to 10.0.1, sync with rawhide

* Thu Feb  9 2012 Jan Horak <jhorak@redhat.com> - 10.0.1-1
- Update to 10.0.1

* Wed Feb 01 2012 Remi Collet <RPMS@FamilleCollet.com> - 10.0-1
- update to 10.0, sync with rawhide

* Tue Jan 31 2012 Jan Horak <jhorak@redhat.com> - 10.0-1
- Update to 10.0

* Mon Jan 30 2012 Tom Callaway <spot@fedoraproject.org> 10.0-3
- fix issues causing ftbfs in rawhide

* Mon Jan 30 2012 Tom Callaway <spot@fedoraproject.org> 10.0-2
- rebuild against libvpx 1.0.0 (and BR 1.0.0 or greater)

* Mon Jan 23 2012 Martin Stransky <stransky@redhat.com> 10.0-1
- Update to 10.0 Beta 6

* Thu Jan 19 2012 Dennis Gilmore <dennis@ausil.us> - 9.0.1-4
- add missing v from armv7hl and armv7hnl config options

* Wed Jan 04 2012 Dan Horák <dan[at]danny.cz> - 9.0.1-3
- fix build on secondary arches (cherry-picked from 13afcd4c097c)

* Fri Dec 23 2011 Peter Robinson <pbrobinson@fedoraproject.org> - 9.0.1-2
- Add compile options for ARM hfp/sfp - RHBZ #738509

* Thu Dec 22 2011 Remi Collet <RPMS@FamilleCollet.com> - 9.0.1-1
- update to 9.0.1

* Tue Dec 20 2011 Remi Collet <RPMS@FamilleCollet.com> - 9.0-1
- update to 9.0, sync with rawhide

* Tue Dec 20 2011 Jan Horak <jhorak@redhat.com> - 9.0-2
- Update to 9.0

* Fri Dec 9 2011 Martin Stransky <stransky@redhat.com> 9.0-1.beta5
- Updated to 9.0 Beta 5

* Wed Dec  7 2011 Jan Horak <jhorak@redhat.com> - 8.0-5
- Gnome 3 proxy settings are now honoured (mozbz#682832)

* Tue Dec  6 2011 Tom Callaway <spot@fedoraproject.org> 8.0-4
- fix bug in npapi.h causing compile failures

* Fri Nov 25 2011 Martin Stransky <stransky@redhat.com> 8.0-3
- s390 build fixes

* Sat Nov 12 2011 Remi Collet <RPMS@FamilleCollet.com> - 8.0-1
- update to 8.0, sync with rawhide

* Mon Nov 7 2011 Martin Stransky <stransky@redhat.com> 8.0-1
- Updated to 8.0

* Tue Oct 18 2011 Ville Skyttä <ville.skytta@iki.fi> - 7.0.1-5
- Avoid %%post/un shell invocations 
  and dependencies (rhbz#736830).

* Tue Oct 18 2011 Martin Stransky <stransky@redhat.com> 7.0.1-4
- Updated cairo dependency (rhbz#742853)

* Wed Oct 12 2011 Georgi Georgiev <chutzimir@gmail.com> - 7.0.1-1
- Make it work on RHEL

* Tue Oct 11 2011 Dan Horák <dan[at]danny.cz> 7.0.1-3
- fix build on secondary arches

* Fri Sep 30 2011 Remi Collet <RPMS@FamilleCollet.com> - 7.0.1-1
- update to 7.0.1

* Tue Sep 27 2011 Remi Collet <RPMS@FamilleCollet.com> - 7.0-1
- update to 7.0

* Tue Sep 06 2011 Remi Collet <RPMS@FamilleCollet.com> - 6.0.2-1
- update to 6.0.2

* Thu Sep 01 2011 Remi Collet <RPMS@FamilleCollet.com> - 6.0.1-1
- update to 6.0.1

* Wed Aug 17 2011 Remi Collet <RPMS@FamilleCollet.com> - 6.0-1
- sync with rawhide, update to 6.0

* Tue Aug 16 2011 Martin Stransky <stransky@redhat.com> 6.0-2
- Updated gtkmozembed patch

* Tue Aug 16 2011 Martin Stransky <stransky@redhat.com> 6.0-1
- 6.0

* Tue Aug 02 2011 Remi Collet <RPMS@FamilleCollet.com> - 6.0-0.1.beta4
- update to 6.0 beta4

* Sun Jul 24 2011 Remi Collet <RPMS@FamilleCollet.com> - 6.0-0.1.beta3.build2
- update to 6.0 beta3 build2 candidate

* Sat Jul 16 2011 Remi Collet <RPMS@FamilleCollet.com> - 5.0.1-1
- Update to 5.0.1

* Thu Jun 30 2011 Martin Stransky <stransky@redhat.com> 5.0-5
- Fixed build on powerpc(64)

* Tue Jun 28 2011 Dan Horák <dan[at]danny.cz> - 5.0-4
- fix build on secondary arches with IPC enabled

* Fri Jun 24 2011 Remi Collet <RPMS@FamilleCollet.com> - 5.0-1
- sync with f15/rawhide
- update to 5.0 finale

* Tue Jun 24 2011 Martin Stransky <stransky@redhat.com> 5.0-3
- libCurl build fix

* Wed Jun 22 2011 Martin Stransky <stransky@redhat.com> 5.0-2
- Reverted mozbz#648156 - Remove gtkmozembed

* Tue Jun 21 2011 Martin Stransky <stransky@redhat.com> 5.0-1
- 5.0

* Thu Jun 16 2011 Remi Collet <RPMS@FamilleCollet.com> - 5.0-0.6.build1
- Update to 5.0 build 1 candidate

* Wed Jun 15 2011 Remi Collet <RPMS@FamilleCollet.com> - 5.0-0.4.beta7.build1
- Update to 5.0 Beta 7 build 1 candidate

* Tue Jun 14 2011 Remi Collet <RPMS@FamilleCollet.com> - 5.0-0.2.beta6.build1
- Update to 5.0 Beta 6 build 1 candidate

* Sun Jun 12 2011 Remi Collet <RPMS@FamilleCollet.com> - 5.0-0.1.b5.build1
- use patch from spot
- Update to 5.0b5 build1

* Wed Jun  1 2011 Tom Callaway <spot@fedoraproject.org> - 5.0-0.1.b3
- firefox5, xulrunner5

* Wed Jun  1 2011 Remi Collet <RPMS@FamilleCollet.com> - 5.0-0.1.b3.build1
- xulrunner5

* Sun Apr 17 2011 Remi Collet <RPMS@FamilleCollet.com> - 2.0.1-0.1.build1
- Update to 2.0.1 build1 candidate

* Sun Apr 10 2011 Christopher Aillon <caillon@redhat.com> - 2.0-3
- Fix offline status issue on version upgrades
- Fix a hang with 20+ extensions

* Mon Apr  4 2011 Christopher Aillon <caillon@redhat.com> - 2.0-2
- Fix SIGABRT in X_CloseDevice: XI_BadDevice
- Updates for NetworkManager 0.9
- Updates for GNOME 3

* Tue Mar 22 2011 Christopher Aillon <caillon@redhat.com> - 2.0-1
- 2.0

* Tue Mar 22 2011 Remi Collet <RPMS@FamilleCollet.com> - 2.0-1
- Update to 2.0

* Sat Mar 19 2011 Remi Collet <RPMS@FamilleCollet.com> - 2.0-0.26.rc2
- Update to 2.0 RC2

* Fri Mar 18 2011 Christopher Aillon <caillon@redhat.com> - 2.0-0.28
- Update to 2.0 RC2

* Thu Mar 17 2011 Jan Horak <jhorak@redhat.com> - 2.0-0.27
- Disabled gnomevfs
- Enabled gio
- Build with system libvpx

* Thu Mar 10 2011 Remi Collet <RPMS@FamilleCollet.com> - 2.0-0.25.rc1
- Update to 2.0 RC1

* Wed Mar  9 2011 Christopher Aillon <caillon@redhat.com> - 2.0-0.26
- Update to 2.0 RC 1

* Sat Mar 05 2011 Remi Collet <RPMS@FamilleCollet.com> - 2.0-0.24.rc1.build1
- Update to 2.0 RC1 build1 candidate

* Mon Feb 28 2011 Remi Collet <RPMS@FamilleCollet.com> - 2.0-0.23.beta12
- sync with rawhide
- update to 2.0 Beta12

* Sun Feb 27 2011 Christopher Aillon <caillon@redhat.com> - 2.0-0.25
- Make Firefox's User-Agent string match upstream's

* Sat Feb 26 2011 Christopher Aillon <caillon@redhat.com> - 2.0-0.24
- Switch to using the omni chrome file format

* Fri Feb 25 2011 Christopher Aillon <caillon@redhat.com> - 2.0-0.23
- Update to 2.0 Beta 12

* Wed Feb 23 2011 Remi Collet <RPMS@FamilleCollet.com> - 2.0-0.22.beta12.build1
- sync with rawhide
- update to 2.0 Beta12 build1 candidate

* Sun Feb 13 2011 Dennis Gilmore <dennis@ausil.us> 2.0-0.22
- disable nanojit on sparc64 its not supported and doesnt get automatically switched off

* Thu Feb 10 2011 Christopher Aillon <caillon@redhat.com> - 2.0-0.21
- Also provide arch-agnostic versions of gecko virtual provides

* Thu Feb 10 2011 Christopher Aillon <caillon@redhat.com> - 2.0-0.20
- Introduce better versioning for our gecko virtual provides
- Now, the gecko-libs and gecko-devel virtual provides will be pinned
  to an individual Gecko release, so packages can do things like
    Requires: gecko-libs = 2.0-beta11
    BuildRequires: gecko-libs = 2.0-beta11
- Final releases will be pinned to e.g. 2.0-1 regardless of %%{release}
- Also, make sure those virtual provides are arch-specific

* Wed Feb 09 2011 Remi Collet <RPMS@FamilleCollet.com> - 2.0-0.21.beta11
- Update to 2.0 Beta 11

* Tue Feb  8 2011 Christopher Aillon <caillon@redhat.com> - 2.0-0.19
- Update to 2.0 Beta 11

* Fri Feb 04 2011 Remi Collet <RPMS@FamilleCollet.com> - 2.0-0.20.beta11.build3
- 2.0b11 build3 candidate (using firefox sources)

* Thu Feb 03 2011 Remi Collet <RPMS@FamilleCollet.com> - 2.0-0.19.beta11.build2
- 2.0b11 build2 candidate (using firefox sources)

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


