%global nspr_version 4.8.7
%global nss_version 3.12.9
%global cairo_version 1.10
%global freetype_version 2.1.9
%global lcms_version 1.18
%global sqlite_version 3.7.1

%global mozappdir   %{_libdir}/bluegriffon
%global tarballdir  mozilla-2.0
%global svnmain     0
%global svnlocales  0
%global prever      %nil

# gecko version, else to use bundled version
#global gecko_version   2.0.1-1

# Firefox version of sources used
%global srcversion      4.0.1

Summary:        The next-generation Web Editor
Summary(fr):    La nouvelle génération d'éditeur web
Name:           bluegriffon
Version:        1.1.1
%if %{?svnmain}
Release:        0.2.svn%{svnmain}%{?dist}
%else
Release:        1%{?dist}
%endif
URL:            http://bluegriffon.org/
License:        MPLv1.1 or GPLv2+ or LGPLv2+
Group:          Applications/Editors

Source0:        ftp://ftp.mozilla.org/pub/firefox/releases/%{version}/source/firefox-%{srcversion}.source.tar.bz2

%if %{?svnmain}
# svn export -r 553 http://sources.disruptive-innovations.com/bluegriffon/trunk bluegriffon
# tar cjf bluegriffon-553.tar.bz2 bluegriffon
Source1:        %{name}-%{svnmain}.tar.bz2
%else
# svn export http://sources.disruptive-innovations.com/bluegriffon/tags/1.1.1 bluegriffon
# tar cjf bluegriffon-1.1.1.tar.bz2 bluegriffon
Source1:        %{name}-%{version}%{?prever}.tar.bz2
%endif

%if %{?svnlocales}
# svn export -r 58 http://sources.disruptive-innovations.com/bluegriffon-l10n/trunk locales
# tar cjf bluegriffon-l10n-58.tar.bz2 locales
Source2:        %{name}-l10n-%{svnlocales}.tar.bz2
%else
# svn export http://sources.disruptive-innovations.com/bluegriffon-l10n/tags/1.1.1 locales
# tar cjf bluegriffon-l10n-1.1.1.tar.bz2 locales
Source2:        %{name}-l10n-%{version}%{?prever}.tar.bz2
%endif

Source10:       %{name}.sh.in
Source11:       %{name}.sh
Source12:       %{name}.desktop


# build patches
Patch0:         xulrunner-version.patch
Patch1:         mozilla-build.patch
Patch9:         mozilla-build-sbrk.patch
Patch12:        xulrunner-2.0-64bit-big-endian.patch
Patch13:        xulrunner-2.0-secondary-jit.patch
Patch14:        xulrunner-2.0-chromium-types.patch

# Fedora specific patches
Patch20:        mozilla-193-pkgconfig.patch
Patch21:        mozilla-libjpeg-turbo.patch
Patch23:        wmclass.patch
Patch24:        crashreporter-remove-static.patch

# Upstream patches
Patch32:        firefox-4.0-moz-app-launcher.patch
Patch33:        firefox-4.0-gnome3.patch
Patch34:        xulrunner-2.0-network-link-service.patch
Patch35:        xulrunner-2.0-NetworkManager09.patch
Patch36:        xulrunner-omnijar.patch

# BlueGriffon patches
Patch100:       bluegriffon-build.patch
Patch101:       bluegriffon-prefs.patch


BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires:  desktop-file-utils
BuildRequires:  yasm

%if 0%{?gecko_version:1}
%if %{fedora} >= 15
%global xulbin xulrunner
%global grecnf gre
%else
%global xulbin xulrunner2
%global grecnf gre2
BuildRequires:  gecko-devel = %{gecko_version}
Requires:       gecko-libs%{?_isa} = %{gecko_version}
%endif
%else
%if %{fedora} >= 13
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
BuildRequires:  mesa-libGL-devel
BuildRequires:  yasm
BuildRequires:  libcurl-devel
BuildRequires:  lcms-devel >= %{lcms_version}
%if %{fedora} >= 13
BuildRequires:  libvpx-devel
%endif
%endif

%description
BlueGriffon is a new WYSIWYG content editor for the World Wide Web.

Powered by Gecko, the rendering engine of Firefox 4, it's a modern
and robust solution to edit Web pages in conformance to the latest
Web Standards.

%description -l fr
BlueGriffon est un nouvel éditeur de page web WYSIWYG.

Basé sur Gecko, le moteur de rendu de Firefox 4, c'est une solution
moderne et fiable pour éditer des pages Web conformes aux dernières
normes w3c.


%prep
echo TARGET %{name}-%{version}-%{release}
%if 0%{?gecko_version:1}
echo use GECKO %{gecko_version}
%else
echo use Bundled GECKO
%endif
%setup -q -n %{tarballdir}

tar xjf %{SOURCE1}
tar xjf %{SOURCE2} --directory %{name}

sed -e 's/__RPM_VERSION_INTERNAL__/%{gecko_dir_ver}/' %{P:%%PATCH0} \
    > version.patch
%{__patch} -p1 -b --suffix .version --fuzz=0 < version.patch

%patch1  -p2 -b .build
%patch9  -p2 -b .sbrk
%patch12 -p2 -b .64bit-big-endian
%patch13 -p2 -b .secondary-jit
%patch14 -p2 -b .chromium-types

%patch20 -p2 -b .pk
%patch21 -p2 -b .jpeg-turbo
%patch23 -p1 -b .wmclass
%patch24 -p1 -b .static

%patch32 -p1 -b .moz-app-launcher
%patch33 -p1 -b .gnome3
%patch34 -p1 -b .network-link-service
%patch35 -p1 -b .NetworkManager09
%patch36 -p1 -b .omnijar

%patch100  -p0 -b .build
%patch101  -p0 -b .rpmprefs

# Patch provided in bluegriffon sources
patch -p1 <bluegriffon/config/content.patch


#See http://bluegriffon.org/pages/Build-BlueGriffon
cat <<EOF_MOZCONFIG > .mozconfig 
mk_add_options MOZ_OBJDIR=@TOPSRCDIR@

ac_add_options --enable-application=%{name}

# --with-system-png is disabled because Mozilla requires APNG support in libpng
#ac_add_options --with-system-png
ac_add_options --prefix="\$PREFIX"
ac_add_options --libdir="\$LIBDIR"
ac_add_options --disable-cpp-exceptions
%if %{fedora} >= 15
ac_add_options --enable-system-sqlite
%endif
%if %{fedora} >= 13
ac_add_options --with-system-nspr
ac_add_options --with-system-nss
%endif
%if %{fedora} >= 11
ac_add_options --enable-system-hunspell
%endif
%if %{fedora} >= 15
ac_add_options --enable-system-cairo
%endif
ac_add_options --enable-libnotify
ac_add_options --enable-system-lcms
ac_add_options --disable-necko-wifi
ac_add_options --with-system-jpeg
ac_add_options --with-system-zlib
ac_add_options --with-system-bz2
ac_add_options --with-pthreads
ac_add_options --disable-strip
ac_add_options --disable-activex
ac_add_options --disable-activex-scripting
ac_add_options --disable-tests
ac_add_options --disable-airbag
ac_add_options --enable-places
ac_add_options --enable-storage
ac_add_options --enable-shared
ac_add_options --disable-static
ac_add_options --disable-mochitest
ac_add_options --disable-installer
ac_add_options --disable-debug
ac_add_options --enable-optimize
ac_add_options --enable-xinerama
ac_add_options --enable-default-toolkit=cairo-gtk2
ac_add_options --disable-xprint
ac_add_options --enable-pango
ac_add_options --enable-svg
ac_add_options --enable-canvas
ac_add_options --enable-startup-notification
ac_add_options --disable-javaxpcom
ac_add_options --disable-crashreporter
ac_add_options --enable-safe-browsing
ac_add_options --disable-updater
ac_add_options --enable-gio
ac_add_options --disable-gnomevfs
EOF_MOZCONFIG

echo ""  >> .mozconfig
%if 0%{?gecko_version:1}
echo "ac_add_options --with-libxul-sdk=\
$(pkg-config --variable=sdkdir libxul)" >> .mozconfig
%endif


%build
MOZ_OPT_FLAGS=$(echo $RPM_OPT_FLAGS -fpermissive | \
                     %{__sed} -e 's/-Wall//' -e 's/-fexceptions/-fno-exceptions/g')
export CFLAGS=$MOZ_OPT_FLAGS
export CXXFLAGS=$MOZ_OPT_FLAGS

export PREFIX='%{_prefix}'
export LIBDIR='%{_libdir}'

MOZ_SMP_FLAGS=-j1
[ -z "$RPM_BUILD_NCPUS" ] && \
     RPM_BUILD_NCPUS="`/usr/bin/getconf _NPROCESSORS_ONLN`"
[ "$RPM_BUILD_NCPUS" -gt 1 ] && MOZ_SMP_FLAGS=-j$RPM_BUILD_NCPUS

MOZ_APP_DIR=%{_libdir}/%{name}

export LDFLAGS="-Wl,-rpath,${MOZ_APP_DIR}"
make -f client.mk build STRIP="/bin/true" MOZ_MAKE_FLAGS="$MOZ_SMP_FLAGS"


%install
%{__rm} -rf $RPM_BUILD_ROOT

# No Make install for now :(
mkdir -p $RPM_BUILD_ROOT/%{mozappdir}
tar --create --file - --dereference --directory=dist/bin --exclude xulrunner . \
  | tar --extract --file - --directory $RPM_BUILD_ROOT/%{mozappdir}

# Launcher
%if 0%{?gecko_version:1}
install -d -m 755 $RPM_BUILD_ROOT%{_bindir}
XULRUNNER_DIR=`pkg-config --variable=libdir libxul | %{__sed} -e "s,%{_libdir},,g"`
%{__cat} %{SOURCE10} | %{__sed} -e "s,XULRUNNER_DIRECTORY,$XULRUNNER_DIR,g" \
                     | %{__sed} -e "s,XULRUNNER_BIN,%{xulbin},g" \
		     | %{__sed} -e "s,GRE_CONFIG,%{grecnf},g"  \
  > $RPM_BUILD_ROOT%{_bindir}/%{name}
%{__chmod} 755 $RPM_BUILD_ROOT%{_bindir}/%{name}
%else
install -D -m 755 %{SOURCE11} $RPM_BUILD_ROOT%{_bindir}/%{name}
%endif

# Shortcut
desktop-file-install  \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications \
  --add-category Development \
  --add-category Network \
  %{SOURCE12}

# Icons
install -D -m 644  bluegriffon/app/icons/default16.png  $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/16x16/apps/%{name}.png
install -D -m 644  bluegriffon/app/icons/default32.png  $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/32x32/apps/%{name}.png
install -D -m 644  bluegriffon/app/icons/default48.png  $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/48x48/apps/%{name}.png
install -D -m 644  bluegriffon/app/icons/default50.png  $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/16x16/apps/%{name}.png
install -D -m 644  bluegriffon/app/icons/%{name}128.png $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/128x128/apps/%{name}.png

# Use the system hunspell dictionaries
%{__rm} -rf $RPM_BUILD_ROOT/%{mozappdir}/dictionaries
ln -s %{_datadir}/myspell $RPM_BUILD_ROOT%{mozappdir}/dictionaries


%post
update-desktop-database &> /dev/null || :
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
  %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi


%postun
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi
update-desktop-database &> /dev/null || :


%files
%defattr(-,root,root,-)
%{_bindir}/%{name}
%{mozappdir}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/16x16/apps/%{name}.png
%{_datadir}/icons/hicolor/32x32/apps/%{name}.png
%{_datadir}/icons/hicolor/48x48/apps/%{name}.png
%{_datadir}/icons/hicolor/128x128/apps/%{name}.png


%changelog
* Fri Jun 10 2011 Remi Collet <rpms@famillecollet.com> - 1.1.1-1
- BlueGriffon 1.1.1 "Gudea"

* Mon May  9 2011 Remi Collet <rpms@famillecollet.com> - 1.0-4
- BlueGriffon 1.0 "Zephyr" (tags/1.0 which is really 1.0 finale)
- patch default prefs to disable update and enable OS locale

* Wed May  4 2011 Remi Collet <rpms@famillecollet.com> - 1.0-3
- rebuild with bundled xulrunnner

* Wed May  4 2011 Remi Collet <rpms@famillecollet.com> - 1.0-2
- BlueGriffon 1.0 "Zephyr" (tags/1.0RC4 which is 1.0 finale)

* Sun May  1 2011 Remi Collet <rpms@famillecollet.com> - 1.0-1
- bluegriffon 1.0 (tags/1.0 + locales 58)

* Thu Apr 28 2011 Remi Collet <rpms@famillecollet.com> - 1.0-0.2.svn651
- bluegriffon 1.0pre1, svn 651, locales svn 56
- build against xulrunner 2.0.1
- add Gnome3 patch from Firefox

* Sun Apr 17 2011 Remi Collet <rpms@famillecollet.com> - 1.0-0.1.svn635
- bluegriffon 1.0pre1, svn 635, locales svn 47
- build against xulrunner 2.0.1 build1 candidate

* Mon Mar 29 2011 Remi Collet <rpms@famillecollet.com> - 0.9.1-1
- BlueGriffon 0.9.1 "Coffee Overflow"
  http://bluegriffon.org/post/2011/03/29/BlueGriffon-0.9.1-Coffee-Overflow

* Tue Mar 22 2011 Remi Collet <rpms@famillecollet.com> - 0.9.1-0.svn597.1
- rebuild against xulrunnner 2.0

* Sat Mar 19 2011 Remi Collet <rpms@famillecollet.com> - 0.9.1-0.svn597
- bluegriffon svn 597, locales svn 36
- rebuild against xulrunnner 2.0rc2

* Thu Mar 10 2011 Remi Collet <rpms@famillecollet.com> - 0.9-3.svn584
- bluegriffon svn 584, locales svn 33
- rebuild against xulrunnner 2.0rc1

* Sun Mar 06 2011 Remi Collet <rpms@famillecollet.com> - 0.9-3.svn580
- bluegriffon svn 580, locales svn 33

* Mon Feb 28 2011 Remi Collet <rpms@famillecollet.com> - 0.9-2
- rebuild against xulrunnner 2.0b12

* Fri Feb 23 2011 Remi Collet <rpms@famillecollet.com> - 0.9-1.1
- rebuild against xulrunnner 2.0b12 build 1

* Fri Feb 11 2011 Remi Collet <rpms@famillecollet.com> - 0.9-1
- BlueGriffon 0.9 "Cape Town" (svn = 560, locales = 25)
  http://bluegriffon.org/post/2011/02/11/BlueGriffon-0.9-Cape-Town

* Wed Feb 09 2011 Remi Collet <rpms@famillecollet.com> - 0.9-0.6.svn554
- bluegriffon svn 554

* Wed Feb 09 2011 Remi Collet <rpms@famillecollet.com> - 0.9-0.5.svn553
- bluegriffon svn 553, locales svn 23
- rebuild against xulrunnner 2.0b11

* Sat Feb 05 2011 Remi Collet <rpms@famillecollet.com> - 0.9-0.4.svn541
- rebuild

* Fri Feb 04 2011 Remi Collet <rpms@famillecollet.com> - 0.9-0.3.svn540
- add stuff to build against system xulrunner2

* Mon Jan 31 2011 Remi Collet <rpms@famillecollet.com> - 0.9-0.2.svn540
- split sources
- more patches from Firefox (fix rawhide build)
- add french sumnary/description

* Fri Jan 28 2011 Remi Collet <rpms@famillecollet.com> - 0.9-0.1.hg20110128
- first work on RPM - BlueGriffon 0.9rc1

