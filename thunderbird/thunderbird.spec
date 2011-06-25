%define nspr_version 4.8.6
%define nss_version 3.12.8
%define cairo_version 1.8.8
%define freetype_version 2.1.9
%define lcms_version 1.19
%define sqlite_version 3.6.22
%define libnotify_version 0.4
%define build_langpacks 1
%define thunderbird_app_id \{3550f703-e582-4d05-9a08-453d09bdfdc6\} 

# The tarball is pretty inconsistent with directory structure.
# Sometimes there is a top level directory.  That goes here.
#
# IMPORTANT: If there is no top level directory, this should be 
# set to the cwd, ie: '.'
#%define tarballdir .
%define tarballdir comm-1.9.2

%define official_branding 1
# enable crash reporter only for iX86
%ifarch %{ix86} x86_64
%define enable_mozilla_crashreporter 1
%else
%define enable_mozilla_crashreporter 0
%endif

%define version_internal  3.1
%define mozappdir         %{_libdir}/%{name}-%{version_internal}

Summary:        Mozilla Thunderbird mail/newsgroup client
Name:           thunderbird
Version:        3.1.11
Release:        1%{?dist}
URL:            http://www.mozilla.org/projects/thunderbird/
License:        MPLv1.1 or GPLv2+ or LGPLv2+
Group:          Applications/Internet
%if %{official_branding}
%define tarball thunderbird-%{version}.source.tar.bz2
%else
%define tarball thunderbird-3.1rc1.source.tar.bz2
%endif
Source0:        %{tarball}
%if %{build_langpacks}
Source1:        thunderbird-langpacks-%{version}-20110625.tar.bz2
%endif

Source10:       thunderbird-mozconfig
Source11:       thunderbird-mozconfig-branded
Source12:       thunderbird-redhat-default-prefs.js
Source13:       thunderbird-mozconfig-debuginfo
Source20:       thunderbird.desktop
Source21:       thunderbird.sh.in
Source100:      find-external-requires

# Mozilla (XULRunner) patches
Patch0:         thunderbird-version.patch
Patch1:         thunderbird-default.patch
Patch2:         mozilla-jemalloc.patch
Patch3:         xulrunner-1.9.2.1-build.patch
Patch4:         mozilla-libjpeg-turbo.patch
Patch5:         mozilla-missing-cflags.patch
Patch6:         mozilla-build-s390.patch
Patch7:         crashreporter-remove-static.patch
Patch9:         xulrunner-2.0-os2cc.patch

%if %{official_branding}
# Required by Mozilla Corporation

%else
# Not yet approved by Mozillla Corporation

%endif

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
%if 0%{?fedora} >= 12
BuildRequires:  nspr-devel >= %{nspr_version}
%endif
%if 0%{?fedora} >= 13
BuildRequires:  nss-devel >= %{nss_version}
%endif
%if %{fedora} >= 11
BuildRequires:  cairo-devel >= %{cairo_version}
%endif
BuildRequires:  libnotify-devel >= %{libnotify_version}
BuildRequires:  libpng-devel
BuildRequires:  libjpeg-devel
BuildRequires:  zip
BuildRequires:  bzip2-devel
BuildRequires:  zlib-devel, gzip, zip, unzip
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
%if 0%{?fedora} >= 11
BuildRequires:  hunspell-devel
%endif
%if 0%{?fedora} >= 15
# Need SQLITE_SECURE_DELETE option
BuildRequires:  sqlite-devel >= %{sqlite_version}
%endif
BuildRequires:  startup-notification-devel
BuildRequires:  alsa-lib-devel
BuildRequires:  autoconf213
BuildRequires:  desktop-file-utils
BuildRequires:  libcurl-devel
BuildRequires:  GConf2-devel

Requires:       mozilla-filesystem
%if 0%{?fedora} >= 12
Requires:       nspr >= %{nspr_version}
%endif
%if 0%{?fedora} >= 13
Requires:       nss >= %{nss_version}
%endif
%if 0%{?fedora} >= 15
Requires:       sqlite >= %{sqlite_version}
%endif
%if 0%{?fedora} >= 11
BuildRequires:  lcms-devel >= %{lcms_version}
%endif
%ifarch %{ix86} x86_64
BuildRequires:  wireless-tools-devel
%endif

Obsoletes:      thunderbird3

AutoProv: 0
%define _use_internal_dependency_generator 0
%define __find_requires %{SOURCE100}

%description
Mozilla Thunderbird is a standalone mail and newsgroup client.

%if %{enable_mozilla_crashreporter}
%global moz_debug_prefix %{_prefix}/lib/debug
%global moz_debug_dir %{moz_debug_prefix}%{mozappdir}
%global uname_m %(uname -m)
%global symbols_file_name %{name}-%{version}.en-US.%{_os}-%{uname_m}.crashreporter-symbols.zip
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


%prep
echo CIBLE = %{name}-%{version}-%{release}
[ -f %{SOURCE1} ] || exit 1
%setup -q -c

sed -e "s/^Name=.*/Name=Thunderbird %{version} %{?relcan}/" \
    -e "s/thunderbird/%{name}/" \
    %{SOURCE20} | tee %{name}.desktop

cd %{tarballdir}

sed -e 's/__RPM_VERSION_INTERNAL__/%{version_internal}/' %{P:%%PATCH0} \
    > version.patch
%{__patch} -p1 -b --suffix .version --fuzz=0 < version.patch

# Mozilla (XULRunner) patches
cd mozilla
%patch1 -p2 -b .default-application
%patch2 -p1 -b .jemalloc
%patch3 -p2 -b .protected
%if %{fedora} >= 14
%patch4 -p2 -b .turbo
%endif
%patch5 -p2 -b .mozcflags
%ifarch s390
%patch6 -p1 -b .s390
%endif
%patch7 -p2 -b .static
%patch9 -p1 -b .os2cc
cd ..

%if %{official_branding}
# Required by Mozilla Corporation

%else
# Not yet approved by Mozillla Corporation

%endif

%{__rm} -f .mozconfig
#{__cp} %{SOURCE10} .mozconfig
cat %{SOURCE10} 		\
%if %{fedora} < 15
  | grep -v system-sqlite 	\
%endif
%if %{fedora} < 13
  | grep -v system-nss 		\
%endif
%if %{fedora} < 12
  | grep -v system-nspr 	\
%endif
%if %{fedora} < 11
  | grep -v system-hunspell	\
%endif
%if %{fedora} < 11
  | grep -v system-cairo 	\
%endif
%ifarch %{ix86} x86_64
  | grep -v disable-necko-wifi 	\
%endif
  | tee .mozconfig

cat <<EOF | tee -a .mozconfig
ac_add_options --enable-libnotify
%if %{fedora} >= 11
ac_add_options --enable-system-lcms
%endif
%if %{fedora} >= 15
ac_add_options --enable-system-sqlite
%endif
EOF

%if %{official_branding}
%{__cat} %{SOURCE11} >> .mozconfig
%endif
%if %{enable_mozilla_crashreporter}
%{__cat} %{SOURCE13} >> .mozconfig
%endif

#===============================================================================

%build
cd %{tarballdir}

INTERNAL_GECKO=%{version_internal}
MOZ_APP_DIR=%{mozappdir}

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

%define moz_make_flags -j1
%ifarch ppc ppc64 s390 s390x
%define moz_make_flags -j1
%else
%define moz_make_flags %{?_smp_mflags}
%endif

export LDFLAGS="-Wl,-rpath,%{mozappdir}"
export MAKE="gmake %{moz_make_flags}"
make -f client.mk build

# create debuginfo for crash-stats.mozilla.com
%if %{enable_mozilla_crashreporter}
make buildsymbols
%endif

#===============================================================================

%install
%{__rm} -rf $RPM_BUILD_ROOT
cd %{tarballdir}

INTERNAL_GECKO=%{version_internal}

INTERNAL_APP_NAME=%{name}-${INTERNAL_GECKO}
MOZ_APP_DIR=%{_libdir}/${INTERNAL_APP_NAME}

DESTDIR=$RPM_BUILD_ROOT make install

# install icons
for s in 16 22 24 32 48 256; do
    %{__mkdir_p} $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/${s}x${s}/apps
    %{__cp} -p other-licenses/branding/%{name}/mailicon${s}.png \
               $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/${s}x${s}/apps/thunderbird.png
done


desktop-file-install --vendor mozilla \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications \
  --add-category Network \
  --add-category Email \
  ../%{name}.desktop


# set up the thunderbird start script
rm -f $RPM_BUILD_ROOT/%{_bindir}/thunderbird
%{__cat} %{SOURCE21} | %{__sed} -e 's,TBIRD_VERSION,%{version_internal},g' > \
  $RPM_BUILD_ROOT%{_bindir}/thunderbird
%{__chmod} 755 $RPM_BUILD_ROOT/%{_bindir}/thunderbird

# set up our default preferences
%{__cat} %{SOURCE12} | %{__sed} -e 's,Fedora,Remi,g' \
                                -e 's,THUNDERBIRD_RPM_VR,fc%{fedora},g' > \
        $RPM_BUILD_ROOT/rh-default-prefs
%{__install} -D $RPM_BUILD_ROOT/rh-default-prefs $RPM_BUILD_ROOT/%{mozappdir}/greprefs/all-remi.js
%{__install} -D $RPM_BUILD_ROOT/rh-default-prefs $RPM_BUILD_ROOT/%{mozappdir}/defaults/pref/all-remi.js
%{__rm} $RPM_BUILD_ROOT/rh-default-prefs

%{__rm} -f $RPM_BUILD_ROOT%{_bindir}/thunderbird-config

# own mozilla plugin dir (#135050)
%{__mkdir_p} $RPM_BUILD_ROOT%{_libdir}/mozilla/plugins

# own extension directories
%{__mkdir_p} $RPM_BUILD_ROOT%{_datadir}/mozilla/extensions/%{thunderbird_app_id}
%{__mkdir_p} $RPM_BUILD_ROOT%{_libdir}/mozilla/extensions/%{thunderbird_app_id}

# Install langpacks
%{__rm} -f %{name}.lang # Delete for --short-circuit option
touch %{name}.lang
%if %{build_langpacks}
%{__mkdir_p} $RPM_BUILD_ROOT%{mozappdir}/langpacks
%{__tar} xjf %{SOURCE1}
for langpack in `ls thunderbird-langpacks/*.xpi`; do
  language=`basename $langpack .xpi`
  extensiondir=$RPM_BUILD_ROOT%{mozappdir}/langpacks/langpack-$language@thunderbird.mozilla.org
  %{__mkdir_p} $extensiondir
  unzip $langpack -d $extensiondir
  find $extensiondir -type f | xargs chmod 644

  tmpdir=`mktemp -d %{name}.XXXXXXXX`
  langtmp=$tmpdir/%{name}/langpack-$language
  %{__mkdir_p} $langtmp
  jarfile=$extensiondir/chrome/$language.jar
  unzip $jarfile -d $langtmp

  find $langtmp -type f | xargs chmod 644
  %{__rm} -rf $jarfile
  cd $langtmp
  zip -r -D $jarfile locale
  %{__rm} -rf locale
  cd -
  %{__rm} -rf $tmpdir

  language=`echo $language | sed -e 's/-/_/g'`
  extensiondir=`echo $extensiondir | sed -e "s,^$RPM_BUILD_ROOT,,"`
  echo "%%lang($language) $extensiondir" >> %{name}.lang
done
%{__rm} -rf thunderbird-langpacks
%endif # build_langpacks

# Copy over the LICENSE
cd mozilla
install -c -m 644 LICENSE $RPM_BUILD_ROOT%{mozappdir}
cd -

# Use the system hunspell dictionaries
%{__rm} -rf $RPM_BUILD_ROOT/%{mozappdir}/dictionaries
ln -s %{_datadir}/myspell $RPM_BUILD_ROOT%{mozappdir}/dictionaries

# ghost files
%{__mkdir_p} $RPM_BUILD_ROOT%{mozappdir}/components
touch $RPM_BUILD_ROOT%{mozappdir}/components/compreg.dat
touch $RPM_BUILD_ROOT%{mozappdir}/components/xpti.dat

# Add debuginfo for crash-stats.mozilla.com 
%if %{enable_mozilla_crashreporter}
%{__mkdir_p} $RPM_BUILD_ROOT/%{moz_debug_dir}
%{__cp} mozilla/dist/%{symbols_file_name} $RPM_BUILD_ROOT/%{moz_debug_dir}
%endif


# RC - provide account type
[ -f   $RPM_BUILD_ROOT%{mozappdir}/isp/gmail.rdf ] || \
  install -m 644 mailnews/base/ispdata/gmail.rdf    $RPM_BUILD_ROOT%{mozappdir}/isp/

[ -f   $RPM_BUILD_ROOT%{mozappdir}/isp/movemail.rdf ] || \
  install -m 644 mailnews/base/ispdata/movemail.rdf $RPM_BUILD_ROOT%{mozappdir}/isp/

[ -f      $RPM_BUILD_ROOT%{mozappdir}/isp/rss.rdf ] || \
  install -m 644 mail/extensions/newsblog/rss.rdf   $RPM_BUILD_ROOT%{mozappdir}/isp/

rm -rf $RPM_BUILD_ROOT%{mozappdir}/isp/en-US
rm -rf $RPM_BUILD_ROOT%{mozappdir}/*.chk


#===============================================================================

%clean
%{__rm} -rf $RPM_BUILD_ROOT

#===============================================================================

%pre
echo -e "\nWARNING : This %{name} RPM is not an official Fedora build and it"
echo -e "overrides the official one. Don't file bugs on Fedora Project."
echo -e "Use dedicated forums http://forums.famillecollet.com/\n"

%if %{?fedora}%{!?fedora:99} <= 13
echo -e "WARNING : Fedora %{fedora} is now EOL :"
echo -e "You should consider upgrading to a supported release.\n"
%endif

#===============================================================================

%post
update-desktop-database &> /dev/null || :
touch --no-create %{_datadir}/icons/hicolor
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
  %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi

#===============================================================================

%postun
update-desktop-database &> /dev/null || :
touch --no-create %{_datadir}/icons/hicolor
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
  %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi

#===============================================================================

%files -f %{tarballdir}/%{name}.lang
%defattr(-,root,root,-)
%attr(755,root,root) %{_bindir}/%{name}
%attr(644,root,root) %{_datadir}/applications/mozilla-%{name}.desktop
%dir %{_datadir}/mozilla/extensions/%{thunderbird_app_id}
%dir %{_libdir}/mozilla/extensions/%{thunderbird_app_id}
%dir %{mozappdir}
%doc %{mozappdir}/LICENSE
%{mozappdir}/chrome
%dir %{mozappdir}/components
%ghost %{mozappdir}/components/compreg.dat
%ghost %{mozappdir}/components/xpti.dat
%{mozappdir}/components/components.list
%{mozappdir}/components/*.so
%{mozappdir}/components/*.xpt
%attr(644,root,root) %{mozappdir}/components/*.js
%{mozappdir}/defaults
%{mozappdir}/dictionaries
%dir %{mozappdir}/extensions
%{mozappdir}/extensions/{972ce4c6-7e08-4474-a285-3208198ce6fd}
%dir %{mozappdir}/langpacks
%{mozappdir}/greprefs
%{mozappdir}/isp
%{mozappdir}/mozilla-xremote-client
%{mozappdir}/res
%{mozappdir}/run-mozilla.sh
%{mozappdir}/thunderbird-bin
%{mozappdir}/thunderbird
%{mozappdir}/*.so
%dir %{mozappdir}/modules
%{mozappdir}/modules/*.jsm
%{mozappdir}/modules/*.js
%dir %{mozappdir}/modules/gloda
%{mozappdir}/modules/gloda/*.js
%dir %{mozappdir}/modules/activity
%{mozappdir}/modules/activity/*.js
%{mozappdir}/README.txt
%{mozappdir}/platform.ini
%{mozappdir}/application.ini
%{mozappdir}/blocklist.xml
%exclude %{mozappdir}/removed-files
%{_datadir}/icons/hicolor/16x16/apps/thunderbird.png
%{_datadir}/icons/hicolor/22x22/apps/thunderbird.png
%{_datadir}/icons/hicolor/24x24/apps/thunderbird.png
%{_datadir}/icons/hicolor/256x256/apps/thunderbird.png
%{_datadir}/icons/hicolor/32x32/apps/thunderbird.png
%{_datadir}/icons/hicolor/48x48/apps/thunderbird.png
%if %{enable_mozilla_crashreporter}
%{mozappdir}/crashreporter
%{mozappdir}/crashreporter.ini
%{mozappdir}/Throbber-small.gif
%endif

#===============================================================================

%changelog
* Sat Jun 25 2011 Remi Collet <rpms@famillecollet.com> 3.1.11-1
- Thunderbird 3.1.10

* Tue Jun 21 2011 Jan Horak <jhorak@redhat.com> - 3.1.11-1
- Update to 3.1.11

* Sat Apr 30 2011 Remi Collet <rpms@famillecollet.com> 3.1.10-1
- Thunderbird 3.1.10

* Thu Apr 28 2011 Jan Horak <jhorak@redhat.com> - 3.1.10-1
- Update to 3.1.10

* Thu Apr 21 2011 Christopher Aillon <caillon@redhat.com> - 3.1.9-7
- Make gvfs-open launch a compose window (salimma)
- Spec file cleanups (salimma, caillon)
- Split out mozilla crashreporter symbols to its own debuginfo package (caillon)

* Fri Apr  1 2011 Orion Poplawski <orion@cora.nwra.com> - 3.1.9-5
- Enable startup notification

* Mon Mar  7 2011 Jan Horak <jhorak@redhat.com> - 3.1.9-1
- Update to 3.1.9

* Sat Mar  5 2011 Remi Collet <rpms@famillecollet.com> 3.1.9-1
- Thunderbird 3.1.9

* Wed Mar  2 2011 Remi Collet <rpms@famillecollet.com> 3.1.8-3
- sync with f14

* Tue Mar  1 2011 Jan Horak <jhorak@redhat.com> - 3.1.8-3
- Update to 3.1.8

* Tue Mar  1 2011 Remi Collet <rpms@famillecollet.com> 3.1.8-1
- Thunderbird 3.1.8
- sync with f13/f14, build for old fedora, with lightning langpack
- disable lightning which is broken (previous still works)

* Mon Jan  3 2011 Jan Horak <jhorak@redhat.com> - 3.1.7-3
- Mozilla crash reporter enabled

* Fri Dec 10 2010 Remi Collet <rpms@famillecollet.com> 3.1.7-2
- Thunderbird 3.1.7 
- sync with rawhide, build for old fedora, with lightning langpack

* Thu Dec  9 2010 Jan Horak <jhorak@redhat.com> - 3.1.7-2
- Fixed useragent

* Thu Dec  9 2010 Jan Horak <jhorak@redhat.com> - 3.1.7-1
- Update to 3.1.7

* Sat Nov 27 2010 Remi Collet <fedora@famillecollet.com> - 3.1.6-8
- fix cairo + nspr required version
- lightning: fix thunderbird version required
- lightning: fix release (b3pre)
- lightning: clean install

* Sat Nov 27 2010 Remi Collet <rpms@famillecollet.com> 3.1.6-2
- sync with rawhide for lightning

* Mon Nov 22 2010 Jan Horak <jhorak@redhat.com> - 3.1.6-7
- Added x-scheme-handler/mailto to thunderbird.desktop file

* Mon Nov  8 2010 Jan Horak <jhorak@redhat.com> - 3.1.6-4
- Added libnotify patch
- Removed dependency on static libraries

* Fri Oct 29 2010 Jan Horak <jhorak@redhat.com> - 3.1.6-2
- Move thunderbird-lightning extension from Sunbird package to Thunderbird

* Thu Oct 28 2010 Remi Collet <rpms@famillecollet.com> 3.1.6-1
- Thunderbird 3.1.6

* Wed Oct 27 2010 Jan Horak <jhorak@redhat.com> - 3.1.6-1
- Update to 3.1.6

* Tue Oct 19 2010 Remi Collet <rpms@famillecollet.com> 3.1.5-1
- Thunderbird 3.1.5

* Tue Oct 19 2010 Jan Horak <jhorak@redhat.com> - 3.1.5-1
- Update to 3.1.5

* Thu Sep 16 2010 Remi Collet <rpms@famillecollet.com> 3.1.4-1
- Thunderbird 3.1.4

* Tue Sep 07 2010 Remi Collet <rpms@famillecollet.com> 3.1.3-1
- Thunderbird 3.1.3
- disable system nspr (version 4.8.6 required not yet available)

* Fri Aug 06 2010 Remi Collet <rpms@famillecollet.com> 3.1.2-1
- Thunderbird 3.1.2

* Fri Aug  6 2010 Jan Horak <jhorak@redhat.com> - 3.1.2-1
- Update to 3.1.2
- Disable updater

* Wed Jul 21 2010 Remi Collet <rpms@famillecollet.com> 3.1.1-1
- Thunderbird 3.1.1

* Fri Jun 25 2010 Remi Collet <rpms@famillecollet.com> 3.1-1
- update to 3.1 finale
- add poor workaround for extensions

* Thu Jun 24 2010 Jan Horak <jhorak@redhat.com> - 3.1-1
- Thunderbird 3.1

* Fri Jun 11 2010 Jan Horak <jhorak@redhat.com> - 3.1-0.3.rc2
- TryExec added to desktop file

* Thu Jun 10 2010 Remi Collet <rpms@famillecollet.com> 3.1-0.2.rc2
- update to 3.1rc2

* Mon May 31 2010 Remi Collet <rpms@famillecollet.com> 3.1-0.1.rc1
- update to 3.1rc1
- sync with rawhide and backport to old fedora

* Tue May 25 2010 Christopher Aillon <caillon@redhat.com> 3.1-0.1.rc1
- Thunderbird 3.1 RC1

* Fri Apr 30 2010 Jan Horak <jhorak@redhat.com> - 3.0.4-3
- Fix for mozbz#550455

* Tue Apr 13 2010 Martin Stransky <stransky@redhat.com> - 3.0.4-2
- Fixed langpacks (#580444)

* Tue Mar 30 2010 Remi Collet <rpms@famillecollet.com> 3.0.4-1.fc#.remi
- update to 3.0.4
- sync with F12 and backport to old fedora

* Tue Mar 30 2010 Jan Horak <jhorak@redhat.com> - 3.0.4-1
- Update to 3.0.4

* Sat Mar 06 2010 Kalev Lember <kalev@smartlink.ee> - 3.0.3-2
- Own extension directories (#532132)

* Mon Mar  1 2010 Remi Collet <rpms@famillecollet.com> 3.0.3-1.fc#.remi
- update to 3.0.3
- sync with F12 and backport to old fedora

* Mon Mar  1 2010 Jan Horak <jhorak@redhat.com> - 3.0.3-1
- Update to 3.0.3

* Thu Feb 25 2010 Remi Collet <rpms@famillecollet.com> 3.0.2-1.fc#.remi
- update to 3.0.2
- sync with F12 and backport to old fedora

* Thu Feb 25 2010 Jan Horak <jhorak@redhat.com> - 3.0.2-1
- Update to 3.0.2

* Thu Jan 21 2010 Remi Collet <rpms@famillecollet.com> 3.0.1-1.fc#.remi
- update to 3.0.1 
- sync with F12 and backport to old fedora

* Wed Jan 20 2010 Martin Stransky <stransky@redhat.com> - 3.0.1-1
- Update to 3.0.1

* Wed Dec 09 2009 Remi Collet <rpms@famillecollet.com> 3.0-4.fc#.remi
- update to 3.0 - backport to old fedora

* Wed Dec  9 2009 Jan Horak <jhorak@redhat.com> - 3.0-4
- Update to 3.0

* Wed Dec 02 2009 Remi Collet <rpms@famillecollet.com> 3.0-3.12.rc2.fc#.remi
- update to 3.0 RC2

* Wed Nov 25 2009 Remi Collet <rpms@famillecollet.com> 3.0-3.12.rc1.fc#.remi
- update to 3.0 RC1 (sync with F12)

* Wed Nov 25 2009 Jan Horak <jhorak@redhat.com> - 3.0-3.12.rc1
- Sync with Mozilla latest RC1 build

* Sat Nov 21 2009 Remi Collet <rpms@famillecollet.com> 3.0-3.11.rc1.fc#.remi
- update to 3.0 RC1 (sync with F12)

* Thu Nov 19 2009 Jan Horak <jhorak@redhat.com> - 3.0-3.11.rc1
- Update to 3.0 RC1

* Thu Sep 24 2009 Remi Collet <rpms@famillecollet.com> 3.0-2.7.b4.fc#.remi
- update to 3.0 beta4 (sync with F11)

* Thu Sep 17 2009 Jan Horak <jhorak@redhat.com> - 3.0-2.7
- Update to 3.0 beta4

* Tue Jul 21 2009 Remi Collet <rpms@famillecollet.com> 3.0-2.5.b3.fc#.remi
- update to 3.0 beta3 (sync with F11)

* Sat Jul 18 2009 Remi Collet <rpms@famillecollet.com> 3.0-0.3.b3.build1.fc#.remi
- update to 3.0 beta3 build1

* Thu Jul 16 2009 Jan Horak <jhorak@redhat.com> - 3.0-2.5
- Update to 3.0 beta3

* Sun May 17 2009 Remi Collet <rpms@famillecollet.com> 3.0-0.2.b2.fc#.remi
- rebuild with thunderbird-imap-startup-crash.patch

* Sun Mar 15 2009 Remi Collet <rpms@famillecollet.com> 3.0-0.b2.fc#.remi
- Update to 3.0 beta2 (named thunderbird3)

* Mon Mar  2 2009 Jan Horak <jhorak@redhat.com> - 3.0-1.beta2
- Update to 3.0 beta2
- Added Patch2 to build correctly when building with --enable-shared option 

* Thu Jan 01 2009 Remi Collet <rpms@famillecollet.com> 2.0.0.19-1.fc#.remi
- Update to 2.0.0.19

* Sat Dec 20 2008 Remi Collet <rpms@famillecollet.com> 2.0.0.19-0.build1.fc10.remi
- Update to 2.0.0.19 build1

* Thu Nov 20 2008 Remi Collet <rpms@famillecollet.com> 2.0.0.18-1.fc#.remi
- Update to 2.0.0.18 

* Mon Nov 10 2008 Remi Collet <rpms@famillecollet.com> 2.0.0.18-0.build1.fc10.remi
- Update to 2.0.0.18 build1

* Thu Sep 25 2008 Remi Collet <rpms@famillecollet.com> 2.0.0.17-1.fc#.remi
- Update to 2.0.0.17

* Mon Sep 15 2008 Remi Collet <rpms@famillecollet.com> 2.0.0.17-0.build1.fc9.remi
- Update to 2.0.0.17 (build1)

* Wed Jul 16 2008 Remi Collet <rpms@famillecollet.com> 2.0.0.16-1.fc#.remi
- Update to 2.0.0.16

* Sun May 04 2008 Remi Collet <rpms@famillecollet.com> 2.0.0.14-1.fc9.remi
- rebuild
- obsoletes thunderbird-langpack-fr

* Thu May  1 2008 Christopher Aillon <caillon@redhat.com> - 2.0.0.14-1
- Update to 2.0.0.14
- Use the system dictionaries

* Mon Apr  7 2008 Christopher Aillon <caillon@redhat.com> 2.0.0.12-4
- Add %%lang attributes to langpacks

* Sat Mar 15 2008 Christopher Aillon <caillon@redhat.com> 2.0.0.12-3
- Avoid conflict between gecko debuginfos

* Mon Mar 03 2008 Martin Stransky <stransky@redhat.com> 2.0.0.12-2
- Updated starting script (#426331)

* Thu Feb 28 2008 Remi Collet <rpms@famillecollet.com> 2.0.0.12-1.fc8.remi.1
- SECAlgorithmID.patch
- add EOL warning for older Fedora version

* Tue Feb 26 2008 Christopher Aillon <caillon@redhat.com> 2.0.0.12-1
- Update to 2.0.0.12
- Fix up icon location and some scriptlets

* Tue Feb 26 2008 Remi Collet <rpms@famillecollet.com> 2.0.0.12-1.fc8.remi
- 2.0.0.12 final + sync with rawhide

* Tue Feb 26 2008 Christopher Aillon <caillon@redhat.com> 2.0.0.12-1
- Update to 2.0.0.12
- Fix up icon location and some scriptlets

* Sun Dec  9 2007 Christopher Aillon <caillon@redhat.com> 2.0.0.9-2
- Fix some rpmlint warnings
- Drop some old patches and obsoletes

* Thu Nov 15 2007 Christopher Aillon <caillon@redhat.com> 2.0.0.9-1
- Update to 2.0.0.9

* Wed Nov 14 2007 Remi Collet <rpms@famillecollet.com> 2.0.0.9-1.fc8.remi
- 2.0.0.9 final

* Sun Nov 04 2007 Remi Collet <rpms@famillecollet.com> 2.0.0.9-0.1.rc1.fc8.remi
- 2.0.0.9 RC1

* Thu Nov 02 2007 Remi Collet <rpms@famillecollet.com> 2.0.0.6-6.fc8.remi
- F8 rebuild

* Wed Sep 26 2007 Martin Stransky <stransky@redhat.com> 2.0.0.6-6
- Fixed #242657 - firefox -g doesn't work

* Tue Sep 25 2007 Christopher Aillon <caillon@redhat.com> 2.0.0.6-5
- Removed hardcoded MAX_PATH, PATH_MAX and MAXPATHLEN macros

* Tue Sep 11 2007 Christopher Aillon <caillon@redhat.com> 2.0.0.6-4
- Fix crashes when using GTK+ themes containing a gtkrc which specify 
  GtkOptionMenu::indicator_size and GtkOptionMenu::indicator_spacing

* Mon Sep 10 2007 Martin Stransky <stransky@redhat.com> 2.0.0.6-3
- added fix for #246248 - firefox crashes when searching for word "do"

* Mon Aug 13 2007 Christopher Aillon <caillon@redhat.com> 2.0.0.6-2
- Update the license tag

* Sat Aug 11 2007 Remi Collet <rpms@famillecollet.com> 2.0.0.6-1.fc#.remi
- rebuild

* Wed Aug  8 2007 Christopher Aillon <caillon@redhat.com> 2.0.0.6-1
- Update to 2.0.0.6
- Own the application directory (#244901)

* Fri Jul 20 2007 Remi Collet <rpms@famillecollet.com> 2.0.0.5-1.fc#.remi
- 2.0.0.5 final

* Fri Jun 15 2007 Remi Collet <rpms@famillecollet.com> 2.0.0.4-1.fc#.remi
- 2.0.0.4 final

* Wed Jun 06 2007 Remi Collet <rpms@famillecollet.com> 2.0.0.4-0.rc1.fc7.remi
- F7 build, rewind release, out enigmail

* Sat May 05 2007 Remi Collet <rpms@famillecollet.com> 2.0.0.0-1.fc7.remi
- F7 build, rewind release, out enigmail
- use %%lang for langpacks

* Sat May 05 2007 Remi Collet <rpms@famillecollet.com> 2.0.0.0-3.fc#.remi
- ppc build
- bug : enigmail still in thunderbird package

* Sun Apr 22 2007 Remi Collet <rpms@famillecollet.com> 2.0.0.0-2.fc#.remi
- add gmail, movemail and rss account wizard

* Thu Apr 19 2007 Christopher Aillon <caillon@redhat.com> 2.0.0.0-1
- Update to 2.0.0.0 Final

* Thu Apr 19 2007 Remi Collet <rpms@famillecollet.com> 2.0.0.0-1.fc#.remi
- changes from rawhide SRPM
- update to 2.0.0.0 final
- split enigmail and update to 0.95.0

* Fri Apr 13 2007 Christopher Aillon <caillon@redhat.com> 2.0.0.0-0.5.rc1
- Fix the desktop file
- Clean up the files list
- Remove the default client stuff from the pref window

* Thu Apr 12 2007 Christopher Aillon <caillon@redhat.com> 2.0.0.0-0.4.rc1
- Rebuild into Fedora

* Wed Apr 11 2007 Christopher Aillon <caillon@redhat.com> 2.0.0.0-0.3.rc1
- Update langpacks

* Fri Apr 06 2007 Remi Collet <rpms@famillecollet.com> 2.0.0.0-0.4.rc1.fc6.remi
- change desktop entry name

* Fri Apr 06 2007 Remi Collet <rpms@famillecollet.com> 2.0.0.0-0.3.rc1.fc6.remi
- update to 2.0.0.0rc1

* Thu Apr  5 2007 Christopher Aillon <caillon@redhat.com> 2.0.0.0-0.2.rc1
- Build option tweaks
- Bring the install section to parity with Firefox's

* Thu Apr  5 2007 Christopher Aillon <caillon@redhat.com> 2.0.0.0-0.1.rc1
- Update to 2.0.0.0 RC1

* Thu Mar 08 2007 Remi Collet <rpms@famillecollet.com> 2.0-0.2.b2.fc6.remi
- update to enigmail 0.94.3 (security update)

* Sun Jan 28 2007 Remi Collet <rpms@famillecollet.com> 2.0-0.1.b2.fc6.remi
- First 2.0b2 build

* Sun Jan 28 2007 Remi Collet <rpms@famillecollet.com> 1.5.0.9-3.fc6.remi.1
- add upstream dnd-nograb.patch

* Sat Jan 27 2007 Remi Collet <rpms@famillecollet.com> 1.5.0.9-3.fc6.remi
- update enigmail-0.94.2

* Sun Dec 24 2006 Remi Collet <rpms@famillecollet.com> 1.5.0.9-2.fc6.remi
- add enigmail, thanks Suse.

* Thu Dec 21 2006 Behdad Esfahbod <besfahbo@redhat.com> 1.5.0.9-5
- Added firefox-1.5-pango-underline.patch

* Thu Dec 21 2006 Remi Collet <rpms@famillecollet.com> 1.5.0.9-1.fc4.remi
- rebuild for FC4 from official FC6 SRPM.

* Wed Dec 20 2006 Behdad Esfahbod <besfahbo@redhat.com> 1.5.0.9-4
- Added firefox-1.5-pango-justified-range.patch

* Tue Dec 19 2006 Behdad Esfahbod <besfahbo@redhat.com> 1.5.0.9-3
- Added firefox-1.5-pango-cursor-position-more.patch

* Tue Dec 19 2006 Christopher Aillon <caillon@redhat.com> 1.5.0.9-1
- Update to 1.5.0.9
- Take firefox's pango fixes
- Don't offer to import...nothing.

* Wed Nov  8 2006 Remi Collet <rpms@famillecollet.com> 1.5.0.8-1.fc4.remi
- rebuild for FC4 from official FC5 SRPM.

* Tue Nov  7 2006 Christopher Aillon <caillon@redhat.com> 1.5.0.8-1
- Update to 1.5.0.8
- Allow choosing of download directory
- Take the user to the correct directory from the Download Manager.
- Patch to add support for printing via pango from Behdad.
- Sync up default invisible character with GTK+

* Sat Sep 16 2006 Remi Collet <rpms@famillecollet.com> 1.5.0.7-1.fc4.remi
- rebuild for FC4 from official FC5 SRPM.

* Wed Sep 13 2006 Christopher Aillon <caillon@redhat.com> - 1.5.0.7-1
- Update to 1.5.0.7

* Tue Aug 08 2006 Kai Engert <kengert@redhat.com> - 1.5.0.5-1.1
- Update to 1.5.0.5
- Use dist tag

* Fri Jun 27 2006 Remi Collet <RPMS@FamilleCollet.com> - 1.5.0.5-1.fc{4,5}.remi
- Update to 1.5.0.5 (32 langpacks, new : ga-IE)

* Mon Jun 12 2006 Kai Engert <kengert@redhat.com> - 1.5.0.4-1.1.fc5
- Update to 1.5.0.4
- Fix desktop-file-utils requires

* Fri Jun 02 2006 Remi Collet <RPMS@FamilleCollet.com> - 1.5.0.4-1.fc{4,5}.remi
- Update to 1.5.0.4

* Thu Apr 20 2006 Remi Collet <RPMS@FamilleCollet.com> - 1.5.0.2-1.fc5.remi
- rebuild for FC5 and for FUN

* Thu Apr 20 2006 Remi Collet <RPMS@FamilleCollet.com> - 1.5.0.2-1.fc4.remi
- Update to 1.5.0.2

* Wed Apr 19 2006 Christopher Aillon <caillon@redhat.com> - 1.5.0.2-1.1.fc5
- Update to 1.5.0.2

* Sat Mar 04 2006 Remi Collet <RPMS@FamilleCollet.com> - 1.5-3.fc4.remi
- rebuild for FC4
- provide a default icon, see #177823

* Fri Feb 10 2006 Christopher Aillon <caillon@redhat.com> - 1.5-3
- Add dumpstack.patch
- Improve the langpack install stuff

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.5-2.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Jan 27 2006 Christopher Aillon <caillon@redhat.com> - 1.5-2
- Add some langpacks back in
- Stop providing MozillaThunderbird

* Thu Jan 12 2006 Christopher Aillon <caillon@redhat.com> - 1.5-1
- Official 1.5 release is out

* Thu Jan 12 2006 Remi Collet <remi.collet@univ-reims.fr> - 1.5-1.fc4.remi
- Update to 1.5 (finale)

* Fri Dec 23 2005 Remi Collet <remi.collet@univ-reims.fr> - 1.5-0.2.fc4.remi
- Update to 1.5 rc2

* Sun Dec 18 2005 Remi Collet <remi.collet@univ-reims.fr> - 1.5-0.1.fc4.remi
- rebuild for FC4
- disable system nspr

* Mon Nov 28 2005 Christopher Aillon <caillon@redhat.com> - 1.5-0.5.1.rc1
- Fix issue with popup dialogs and other actions causing lockups

* Sat Nov  5 2005 Christopher Aillon <caillon@redhat.com> 1.5-0.5.0.rc1
- Update to 1.5 rc1

* Sat Oct  8 2005 Christopher Aillon <caillon@redhat.com> 1.5-0.5.0.beta2
- Update to 1.5 beta2

* Wed Sep 28 2005 Christopher Aillon <caillon@redhat.com> 1.5-0.5.0.beta1
- Update to 1.5 beta1
- Bring the install phase of the spec file up to speed
