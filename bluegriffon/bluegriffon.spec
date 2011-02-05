%global nspr_version 4.8.7
%global nss_version 3.12.9
%global cairo_version 1.10
%global freetype_version 2.1.9
%global lcms_version 1.18
%global sqlite_version 3.7.1

%global mozappdir   %{_libdir}/bluegriffon
%global tarballdir  mozilla-central
%global svnmain     541
%global svnlocales  13

%global withxulrunner           1
%global xulrunner_version       2.0-0.20
%global xulrunner_version_max   2.1
%global srcversion              4.0b11

Summary:        The next-generation Web Editor
Summary(fr):    La nouvelle génération d'éditeur web
Name:           bluegriffon
Version:        0.9
Release:        0.4.svn%{svnmain}%{?dist}
URL:            http://bluegriffon.org/
License:        MPLv1.1 or GPLv2+ or LGPLv2+
Group:          Applications/Editors

Source0:        ftp://ftp.mozilla.org/pub/firefox/releases/%{version}/source/firefox-%{srcversion}.source.tar.bz2

# svn checkout http://sources.disruptive-innovations.com/bluegriffon/trunk bluegriffon
# tar cjf bluegriffon-541.tar.bz2 --exclude .svn bluegriffon
Source1:        %{name}-%{svnmain}.tar.bz2

# svn checkout http://sources.disruptive-innovations.com/bluegriffon-l10n locales
# tar cjf bluegriffon-l10n-13.tar.bz2 --exclude .svn locales
Source2:        %{name}-l10n-%{svnlocales}.tar.bz2

Source10:       %{name}.sh.in
Source11:       %{name}.sh
Source12:       %{name}.desktop

Patch1:         firefox4-build.patch
Patch2:         firefox4-build-sbrk.patch
Patch3:         mozilla-malloc.patch
Patch4:         firefox4-libjpeg-turbo.patch
Patch5:         mozilla-notify.patch

Patch12:        xulrunner-2.0-64bit-big-endian.patch
Patch13:        xulrunner-2.0-secondary-jit.patch
Patch14:        xulrunner-2.0-chromium-types.patch
Patch15:        xulrunner-2.0-system-cairo.patch
Patch16:        xulrunner-2.0-system-cairo-tee.patch
Patch17:        xulrunner-2.0-os2cc.patch

BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires:  desktop-file-utils
BuildRequires:  system-bookmarks
BuildRequires:  yasm

%if %{withxulrunner}
BuildRequires:  xulrunner2-devel >= %{xulrunner_version}
Requires:       xulrunner2 >= %{xulrunner_version}
Conflicts:      xulrunner2 >= %{xulrunner_version_max}
%else
BuildRequires:  zip
BuildRequires:  libIDL-devel
BuildRequires:  gtk2-devel
BuildRequires:  gnome-vfs2-devel
BuildRequires:  libgnomeui-devel
BuildRequires:  krb5-devel
BuildRequires:  pango-devel
BuildRequires:  freetype-devel >= 2.1.9
BuildRequires:  libXt-devel
BuildRequires:  libXrender-devel
BuildRequires:  startup-notification-devel
BuildRequires:  wireless-tools-devel

# BR from Xulrunner
%if %{fedora} >= 15
BuildRequires:  sqlite-devel >= %{sqlite_version}
%endif
%if %{fedora} >= 14
BuildRequires:  nspr-devel >= %{nspr_version}
BuildRequires:  nss-devel >= %{nss_version}
%endif
%if %{fedora} >= 11
BuildRequires:  hunspell-devel
%endif
%if %{fedora} >= 15
BuildRequires:  cairo-devel >= %{cairo_version}
%endif
%if %{fedora} >= 10
BuildRequires:  libnotify-devel
%endif
%if %{fedora} >= 9
BuildRequires:  lcms-devel >= %{lcms_version}
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
BuildRequires:  startup-notification-devel
BuildRequires:  alsa-lib-devel
BuildRequires:  autoconf213
BuildRequires:  mesa-libGL-devel

%if 0%{?fedora} >= 14
Requires:       nss >= %{nss_version}
Requires:       nspr >= %{nspr_version}
%endif
%if %{fedora} >= 9
BuildRequires:  lcms-devel >= %{lcms_version}
%endif
# endif %{withxulrunner}
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
%setup -q -n %{tarballdir}

tar xjf %{SOURCE1}
tar xjf %{SOURCE2} --directory %{name}

patch -p1 < bluegriffon/config/content.patch

%patch1  -p2 -b .build
%patch2  -p2 -b .sbrk
%patch3  -p2 -b .malloc
%if %{fedora} >= 14
%patch4  -p2 -b .jpeg-turbo
%endif
%if %{fedora} >= 15
# when libnotify >= 0.7.0
%patch5 -p1 -b .notify
%endif

%patch12 -p2 -b .64bit-big-endian
%patch13 -p2 -b .secondary-jit
%patch14 -p2 -b .chromium-types
%if %{fedora} >= 15
%patch15 -p1 -b .system-cairo
%patch16 -p1 -b .system-cairo-tee
%endif
%patch17 -p1 -b .os2cc

%if 0%{?fedora} >= 15
# For xulrunner-2.0-system-cairo-tee.patch
autoconf-2.13
%endif

#See http://bluegriffon.org/pages/Build-BlueGriffon
cat <<EOF_MOZCONFIG > .mozconfig 
mk_add_options MOZ_OBJDIR=@TOPSRCDIR@

ac_add_options --enable-application=%{name}

# --with-system-png is disabled because Mozilla requires APNG support in libpng
#ac_add_options --with-system-png
ac_add_options --prefix="\$PREFIX"
ac_add_options --libdir="\$LIBDIR"
%if %{fedora} >= 15
ac_add_options --enable-system-sqlite
%endif
%if %{fedora} >= 14
ac_add_options --with-system-nspr
ac_add_options --with-system-nss
%endif
%if %{fedora} >= 11
ac_add_options --enable-system-hunspell
%endif
%if %{fedora} >= 15
ac_add_options --enable-system-cairo
%endif
%if %{fedora} >= 10
ac_add_options --enable-libnotify
%else
ac_add_options --disable-libnotify
%endif
%if %{fedora} >= 9
ac_add_options --enable-system-lcms
%endif
%ifarch ppc ppc64
ac_add_options --disable-necko-wifi
ac_add_options --disable-ipc
%endif
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
ac_add_options --enable-optimize="\$MOZ_OPT_FLAGS"
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
EOF_MOZCONFIG

%if %{withxulrunner}
echo "ac_add_options --enable-libxul"  >> .mozconfig
echo "ac_add_options --with-libxul-sdk=\
$(pkg-config --variable=sdkdir libxul)" >> .mozconfig
%endif


%build
export MOZ_OPT_FLAGS=$(echo $RPM_OPT_FLAGS | \
   %{__sed} -e 's/-Wall//' -e 's/-fexceptions//g')

export CFLAGS=$MOZ_OPT_FLAGS
export CXXFLAGS="$MOZ_OPT_FLAGS -fpermissive"

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
%if %{withxulrunner}
install -d -m 755 $RPM_BUILD_ROOT%{_bindir}
XULRUNNER_DIR=`pkg-config --variable=libdir libxul | %{__sed} -e "s,%{_libdir},,g"`
%{__cat} %{SOURCE10} | %{__sed} -e "s,XULRUNNER_DIRECTORY,$XULRUNNER_DIR,g" > \
  $RPM_BUILD_ROOT%{_bindir}/%{name}
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

