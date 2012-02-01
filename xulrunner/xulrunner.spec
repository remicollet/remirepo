# Use system libvpx
%if 0%{?fedora} < 17
%define system_vpx        0
%else
%define system_vpx        1
%endif
# Use system sqlite?
%if 0%{?fedora} < 16
%define system_sqlite     0
%else
%define system_sqlite     1
%endif
# Use system nspr/nss/cairo
%if 0%{?fedora} < 15
%define system_nspr       0
%define system_nss        0
%define system_cairo      0
%else
%define system_nspr       1
%define system_nss        1
%define system_cairo      1
%endif

# TODO low requirement for libvpx when 1.0.0 available in stable

%global shortname         xulrunner

# Minimal required versions
%global nspr_version 4.8.9
%global nss_version 3.13.1
%global cairo_version 1.10.2
%global freetype_version 2.1.9
%global libnotify_version 0.7.0
%global libvpx_version 1.0.0
%global lcms_version 1.18

%if %{?system_sqlite}
%global sqlite_version 3.7.7.1
# The actual sqlite version (see #480989):
%global sqlite_build_version %(pkg-config --silence-errors --modversion sqlite3 2>/dev/null || echo 65536)
%endif

# gecko_dir_ver should be set to the version in our directory names
# alpha_version should be set to the alpha number if using an alpha, 0 otherwise
# beta_version  should be set to the beta number if using a beta, 0 otherwise
# rc_version    should be set to the RC number if using an RC, 0 otherwise
%global gecko_dir_ver 10
%global alpha_version 0
%global beta_version  0
%global rc_version    0

%global mozappdir         %{_libdir}/%{shortname}-%{gecko_dir_ver}
%global tarballdir  mozilla-release

# crash reporter work only on x86/x86_64
#%ifarch %{ix86} x86_64
#%global enable_mozilla_crashreporter 1
#%else
%global enable_mozilla_crashreporter 0
#%endif

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
Name:           %{shortname}%{gecko_dir_ver}
Version:        10.0
Release:        1%{?dist}
URL:            http://developer.mozilla.org/En/XULRunner
License:        MPLv1.1 or GPLv2+ or LGPLv2+
Group:          Applications/Internet
# You can get sources at ftp://ftp.mozilla.org/pub/firefox/releases/%{version}%{?pre_ver}/source
#Source0:        %{name}-%{version}%{?pre_version}.source.tar.bz2
Source0:        firefox-%{version}%{?pre_version}.source.tar.bz2
Source10:       %{shortname}-mozconfig
Source11:       %{shortname}-mozconfig-debuginfo
Source12:       %{shortname}-redhat-default-prefs.js
Source21:       %{shortname}.sh.in

# build patches
Patch0:         xulrunner-version.patch
Patch1:         mozilla-build.patch
Patch14:        xulrunner-2.0-chromium-types.patch
Patch17:	xulrunner-10.0-gcc47.patch


# Fedora specific patches
Patch20:        mozilla-193-pkgconfig.patch
Patch23:        wmclass.patch
Patch24:        crashreporter-remove-static.patch

# Upstream patches
Patch38:        mozilla-696393.patch
# https://bugzilla.mozilla.org/show_bug.cgi?id=707993
Patch39:        xulrunner-8.0-fix-maemo-checks-in-npapi.patch
Patch40:        mozilla-682832-proxy.patch
# cherry-picked from 13afcd4c097c
Patch41:        xulrunner-9.0-secondary-build-fix.patch
Patch42:        mozilla-706724.patch
Patch43:        mozilla-file.patch
# Needed to detect/use libvpx-1.0.0
# https://bugzilla.mozilla.org/show_bug.cgi?id=722127
Patch44:	mozilla-722127.patch

# ---------------------------------------------------

BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
%if %{system_nspr}
BuildRequires:  nspr-devel >= %{nspr_version}
%endif
%if %{system_nss}
BuildRequires:  nss-devel >= %{nss_version}
%endif
%if %{system_cairo}
BuildRequires:  cairo-devel >= %{cairo_version}
%endif
BuildRequires:  libpng-devel
BuildRequires:  libjpeg-devel
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
BuildRequires:  lcms-devel >= %{lcms_version}
BuildRequires:  yasm
BuildRequires:  curl-devel
%ifarch %{ix86} x86_64
BuildRequires:  wireless-tools-devel
%endif
%if %{system_vpx}
BuildRequires:  libvpx-devel >= %{libvpx_version}
%endif

Requires:       mozilla-filesystem
%if %{system_nspr}
Requires:       nspr >= %{nspr_version}
%endif
%if %{system_nspr}
Requires:       nss >= %{nss_version}
%endif
Provides:       gecko-libs = %{gecko_verrel}
Provides:       gecko-libs%{?_isa} = %{gecko_verrel}
Obsoletes:      xulrunner2
Obsoletes:      xulrunner5
Obsoletes:      xulrunner6
Obsoletes:      xulrunner7
Obsoletes:      xulrunner8
Obsoletes:      xulrunner9

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
Provides: gecko-devel = %{gecko_verrel}
Provides: gecko-devel%{?_isa} = %{gecko_verrel}
Provides: gecko-devel-unstable = %{gecko_verrel}
Provides: gecko-devel-unstable%{?_isa} = %{gecko_verrel}

Requires: %{name}%{?_isa} = %{version}-%{release}
%if %{system_nspr}
Requires: nspr-devel >= %{nspr_version}
%endif
%if %{system_nspr}
Requires: nss-devel >= %{nss_version}
%endif
%if %{system_cairo}
# Library requirements (cairo-tee >= 1.10)
Requires: cairo-devel >= %{cairo_version}
%endif
Requires: libjpeg-devel
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
Requires: sqlite-devel
%endif
Requires: startup-notification-devel
Requires: alsa-lib-devel
Requires: libnotify-devel
Requires: mesa-libGL-devel
Requires: lcms-devel
Requires: yasm
%ifarch %{ix86} x86_64
Requires: wireless-tools-devel
%endif
Obsoletes: xulrunner2-devel
Obsoletes: xulrunner5-devel
Obsoletes: xulrunner6-devel
Obsoletes: xulrunner7-devel
Obsoletes: xulrunner8-devel

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
echo TARGET = %{name}-%{version}-%{release}%{?dist}  GECKO = %{gecko_verrel}
%setup -q -c
cd %{tarballdir}

sed -e 's/__RPM_VERSION_INTERNAL__/%{gecko_dir_ver}/' %{P:%%PATCH0} \
    > version.patch
%{__patch} -p1 -b --suffix .version --fuzz=0 < version.patch

%patch1  -p2 -b .build
%patch14 -p1 -b .chromium-types
%patch17 -p1 -b .gcc47

%patch20 -p2 -b .pk
%patch23 -p1 -b .wmclass
%patch24 -p1 -b .static

%patch38 -p2 -b .696393
%patch39 -p1 -b .707993
%patch40 -p2 -b .682832
%patch41 -p2 -b .secondary-build
%patch42 -p1 -b .706724
%patch43 -p1 -b .file
%if %{system_vpx}
%patch44 -p2 -b .vpx1.0.0
%endif

%{__rm} -f .mozconfig
%{__cat} %{SOURCE10} \
%if ! %{system_sqlite}
  | grep -v enable-system-sqlite   \
%endif
%if ! %{system_nspr}
  | grep -v with-system-nspr       \
%endif
%if ! %{system_nspr}
  | grep -v with-system-nss        \
%endif
%if ! %{system_cairo}
  | grep -v enable-system-cairo    \
%endif
%ifarch %{ix86} x86_64
  | grep -v disable-necko-wifi     \
%endif
%if ! %{system_vpx}
  | grep -v with-system-libvpx     \
%endif
  | tee .mozconfig

%if %{enable_mozilla_crashreporter}
%{__cat} %{SOURCE11} >> .mozconfig
%endif

echo "ac_add_options --enable-system-lcms" >> .mozconfig

%if %{?system_sqlite}
echo "ac_add_options --enable-system-sqlite" >> .mozconfig
%else
echo "ac_add_options --disable-system-sqlite" >> .mozconfig
%endif

# s390(x) fails to start with jemalloc enabled
%ifarch s390 s390x
echo "ac_add_options --disable-jemalloc" >> .mozconfig
%endif

%ifarch armv7hl
echo "ac_add_options --with-arch=armv7-a" >> .mozconfig
echo "ac_add_options --with-float-abi=hard" >> .mozconfig
echo "ac_add_options --with-fpu=vfpv3-d16" >> .mozconfig
%endif
%ifarch armv7hnl
echo "ac_add_options --with-arch=armv7-a" >> .mozconfig
echo "ac_add_options --with-float-abi=hard" >> .mozconfig
echo "ac_add_options --with-fpu=neon" >> .mozconfig
%endif
%ifarch armv5tel
echo "ac_add_options --with-arch=armv5te" >> .mozconfig
echo "ac_add_options --with-float-abi=soft" >> .mozconfig
%endif

%ifnarch %{ix86} x86_64
echo "ac_add_options --disable-methodjit" >> .mozconfig
echo "ac_add_options --disable-monoic" >> .mozconfig
echo "ac_add_options --disable-polyic" >> .mozconfig
echo "ac_add_options --disable-tracejit" >> .mozconfig
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
MOZ_OPT_FLAGS=$(echo "$RPM_OPT_FLAGS -fpermissive" | \
                      %{__sed} -e 's/-Wall//' -e 's/-fexceptions/-fno-exceptions/g')
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

# set up our prefs before install, so it gets pulled in to omni.jar
%{__cp} -p %{SOURCE12} dist/bin/defaults/pref/all-redhat.js

DESTDIR=$RPM_BUILD_ROOT make install

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

%if ! %{system_nspr}
%{__install} -D -p -m 755 \
   dist/sdk/bin/nspr-config \
   $RPM_BUILD_ROOT%{_libdir}/%{shortname}-devel-%{gecko_dir_ver}/sdk/bin/nspr-config
%endif

# Library path
LD_SO_CONF_D=%{_sysconfdir}/ld.so.conf.d
LD_CONF_FILE=xulrunner-%{__isa_bits}.conf

%if %{name} == %{shortname}
%{__mkdir_p} ${RPM_BUILD_ROOT}${LD_SO_CONF_D}
%{__cat} > ${RPM_BUILD_ROOT}${LD_SO_CONF_D}/${LD_CONF_FILE} << EOF
%{mozappdir}
EOF
%endif

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
%{__mkdir_p} $RPM_BUILD_ROOT/%{moz_debug_dir}
%{__cp} dist/%{symbols_file_name} $RPM_BUILD_ROOT/%{moz_debug_dir}
%endif

# Remi : this appears on Fedora <= 13
%{__rm} -f $RPM_BUILD_ROOT/%{mozappdir}/*.chk


#---------------------------------------------------------------------

%clean
%{__rm} -rf $RPM_BUILD_ROOT

#---------------------------------------------------------------------

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

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
%{mozappdir}/components/*.manifest
%{mozappdir}/omni.ja
%{mozappdir}/plugins
%{mozappdir}/*.so
%{mozappdir}/mozilla-xremote-client
%{mozappdir}/run-mozilla.sh
%{mozappdir}/xulrunner
%{mozappdir}/xulrunner-bin
%{mozappdir}/xulrunner-stub
%{mozappdir}/platform.ini
%{mozappdir}/dependentlibs.list
%if %{name} == %{shortname}
%{_sysconfdir}/ld.so.conf.d/xulrunner*.conf
%endif
%{mozappdir}/plugin-container

%if %{enable_mozilla_crashreporter}
%{mozappdir}/crashreporter
%{mozappdir}/crashreporter.ini
%{mozappdir}/Throbber-small.gif
%endif

%files devel
%defattr(-,root,root,-)
#%dir %{_libdir}/%{shortname}-devel-*
%{_datadir}/idl/%{shortname}*%{gecko_dir_ver}
%{_includedir}/%{shortname}*%{gecko_dir_ver}
%{_libdir}/%{shortname}-devel-*
%{_libdir}/pkgconfig/*.pc
%{mozappdir}/xpcshell

#---------------------------------------------------------------------

%changelog
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

* Tue Oct 18 2011 Ville SkyttÃ¤ <ville.skytta@iki.fi> - 7.0.1-5
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


