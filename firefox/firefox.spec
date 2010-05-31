%define nspr_version 4.8
%define nss_version 3.12.3
%define cairo_version 1.8.8
%define lcms_version 1.18
%define freetype_version 2.1.9
%define sqlite_version 3.6.16

%define homepage http://start.fedoraproject.org/
%define default_bookmarks_file %{_datadir}/bookmarks/default-bookmarks.html
%define firefox_app_id \{ec8030f7-c20a-464f-9b0e-13a3a9e97384\}

%define internal_version 3.6

%define mozappdir            %{_libdir}/firefox-%{internal_version}

%define tarballdir mozilla-1.9.2

%define official_branding    1
%define build_langpacks      1

%if ! %{official_branding}
%define cvsdate 20080327
%define nightly .cvs%{cvsdate}
%endif

#define relcan plugin1
%define firefox firefox
%define mycomment  Beta (build6)

Summary:        Mozilla Firefox Web browser
Name:           firefox
Version:        3.6.4
Release:        0.3.build6%{?dist}
URL:            http://www.mozilla.org/projects/firefox/
License:        MPLv1.1 or GPLv2+ or LGPLv2+
Group:          Applications/Internet
%if %{official_branding}
## hg clone -u FIREFOX_3_6_3_RELEASE http://hg.mozilla.org/releases/mozilla-1.9.2
## tar cjf firefox-3.6.3.source.tar.bz2 --exclude .hg mozilla-1.9.2
%define tarball firefox-%{version}%{?relcan}.source.tar.bz2
%else
%define tarball firefox-3.1b3-source.tar.bz2
%endif
Source0:        %{tarball}
%if %{build_langpacks}
Source2:        firefox-langpacks-%{version}%{?relcan}-20100529.tar.bz2
%endif
Source12:       firefox-redhat-default-prefs.js
# firefox3.destop without translation to allow change name
Source20:       firefox3.desktop
Source21:       firefox36.sh.in
Source23:       firefox.1
Source100:      find-external-requires

Source200:      firefox-bookmarks.html

# build patches
Patch0:         firefox-version.patch
Patch1:         mozilla-build.patch
Patch3:         mozilla-jemalloc.patch
Patch4:         mozilla-about-firefox-version.patch
Patch5:         mozilla-jemalloc-526152.patch

# Fedora specific patches

# Upstream patches
Patch100:       mozilla-ps-pdf-simplify-operators.patch

# Remi specific patches
Patch200:       firefox-remi.patch


%if %{official_branding}
# Required by Mozilla Corporation


%else
# Not yet approved by Mozillla Corporation


%endif

# ---------------------------------------------------

BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
# BR from Firefox
BuildRequires:  zip
BuildRequires:  libIDL-devel
BuildRequires:  desktop-file-utils
BuildRequires:  gtk2-devel
BuildRequires:  gnome-vfs2-devel
BuildRequires:  libgnomeui-devel
BuildRequires:  krb5-devel
BuildRequires:  pango-devel
BuildRequires:  freetype-devel >= 2.1.9
BuildRequires:  libXt-devel
BuildRequires:  libXrender-devel
BuildRequires:  startup-notification-devel
%ifarch %{ix86} x86_64
BuildRequires:  wireless-tools-devel
%endif

# BR from Xulrunner
%if %{fedora} >= 11
BuildRequires:  sqlite-devel >= %{sqlite_version}
%endif
%if %{fedora} >= 11
BuildRequires:  nspr-devel >= %{nspr_version}
BuildRequires:  nss-devel >= %{nss_version}
BuildRequires:  hunspell-devel
BuildRequires:  cairo-devel >= %{cairo_version}
%endif
%if %{fedora} >= 10
BuildRequires:  libnotify-devel
%endif
%if %{fedora} >= 9
BuildRequires:  lcms-devel >= %{lcms_version}
%endif
%if %{fedora} >= 7
BuildRequires:  system-bookmarks
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

%if %{fedora} >= 7
Requires:       system-bookmarks
%endif
Obsoletes:      mozilla <= 37:1.7.13
Obsoletes:      firefox36
Provides:       webclient

%define _use_internal_dependency_generator 0
%define __find_requires %{SOURCE100}

%description
Mozilla Firefox is an open-source web browser, designed for standards
compliance, performance and portability.

#---------------------------------------------------------------------

%prep
%if %{build_langpacks}
[ -f %{SOURCE2} ] || exit 1
%endif
%setup -q -c
cd %{tarballdir}

sed -e 's/__RPM_VERSION_INTERNAL__/%{internal_version}/' %{P:%%PATCH0} \
    > version.patch
%{__patch} -p1 -b --suffix .version --fuzz=0 < version.patch

%patch1  -p1 -b .build
%patch3  -p1 -b .jemalloc
%patch4  -p1 -b .about-firefox-version
%patch5  -p1 -b .jemalloc-526152

%patch100 -p1 -b .ps-pdf-simplify-operators

%patch200 -p1 -b .remi

%{__rm} -f .mozconfig

cat <<EOF_MOZCONFIG | tee .mozconfig 
. \$topsrcdir/browser/config/mozconfig

# --with-system-png is disabled because Mozilla requires APNG support in libpng
#ac_add_options --with-system-png
ac_add_options --prefix="\$PREFIX"
ac_add_options --libdir="\$LIBDIR"
%if %{fedora} >= 11
ac_add_options --enable-system-sqlite
%endif
%if %{fedora} >= 11
## Not working since plugin version.... ac_add_options --with-system-nspr
ac_add_options --with-system-nss
ac_add_options --enable-system-hunspell
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
%endif
ac_add_options --with-system-jpeg
ac_add_options --with-system-zlib
ac_add_options --with-system-bz2
ac_add_options --with-pthreads
ac_add_options --disable-strip
ac_add_options --disable-tests
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
#ac_add_options --enable-extensions=default,python/xpcom
%if %{official_branding}
ac_add_options --enable-official-branding
%endif

export BUILD_OFFICIAL=1
export MOZILLA_OFFICIAL=1
mk_add_options BUILD_OFFICIAL=1
mk_add_options MOZILLA_OFFICIAL=1
EOF_MOZCONFIG

#---------------------------------------------------------------------

%build
cd %{tarballdir}

# Mozilla builds with -Wall with exception of a few warnings which show up
# everywhere in the code; so, don't override that.
MOZ_OPT_FLAGS=$(echo $RPM_OPT_FLAGS | %{__sed} -e 's/-Wall//')
export CFLAGS=$MOZ_OPT_FLAGS
export CXXFLAGS=$MOZ_OPT_FLAGS

export PREFIX='%{_prefix}'
export LIBDIR='%{_libdir}'

MOZ_SMP_FLAGS=-j1
%ifnarch ppc ppc64 s390 s390x
[ -z "$RPM_BUILD_NCPUS" ] && \
     RPM_BUILD_NCPUS="`/usr/bin/getconf _NPROCESSORS_ONLN`"
[ "$RPM_BUILD_NCPUS" -gt 1 ] && MOZ_SMP_FLAGS=-j2
%endif

INTERNAL_GECKO=%{internal_version}
MOZ_APP_DIR=%{_libdir}/%{name}-${INTERNAL_GECKO}

export LDFLAGS="-Wl,-rpath,${MOZ_APP_DIR}"
make -f client.mk build STRIP="/bin/true" MOZ_MAKE_FLAGS="$MOZ_SMP_FLAGS"

#---------------------------------------------------------------------

%install
%{__rm} -rf $RPM_BUILD_ROOT
cd %{tarballdir}

DESTDIR=$RPM_BUILD_ROOT make install

%{__mkdir_p} $RPM_BUILD_ROOT{%{_libdir},%{_bindir},%{_datadir}/applications}

sed -e 's/^Name=.*/Name=Firefox %{version}%{?relcan} %{?mycomment}/' \
    -e "s/firefox/%{name}/" \
    %{SOURCE20} | tee %{name}.desktop

desktop-file-install --vendor mozilla \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications \
  --add-category WebBrowser \
  --add-category Network \
  --delete-original %{name}.desktop 

# set up the firefox start script
%{__rm} -rf $RPM_BUILD_ROOT%{_bindir}/firefox
%{__cat} %{SOURCE21} | %{__sed} -e 's,FIREFOX_VERSION,%{internal_version},g' > \
  $RPM_BUILD_ROOT%{_bindir}/%{name}
%{__chmod} 755 $RPM_BUILD_ROOT%{_bindir}/%{name}

# set up our default preferences
%{__cat} %{SOURCE12} | %{__sed} \
	-e 's,FIREFOX_RPM_VR,fc%{fedora},g' \
	-e 's/Fedora/Remi/' > rh-default-prefs

# resolves bug #461880
%{__cat} > $RPM_BUILD_ROOT/%{mozappdir}/browserconfig.properties << EOF
browser.startup.homepage=%{homepage}
EOF

# Export correct locale
%{__cat} > $RPM_BUILD_ROOT/%{mozappdir}/defaults/pref/firefox-l10n.js << EOF
pref("general.useragent.locale", "chrome://global/locale/intl.properties");
EOF
%{__chmod} 644 $RPM_BUILD_ROOT/%{mozappdir}/defaults/pref/firefox-l10n.js

# place the preferences
%{__cp} rh-default-prefs $RPM_BUILD_ROOT/%{mozappdir}/defaults/pref/all-redhat.js
%{__rm} rh-default-prefs

# set up our default bookmarks
%{__rm} -f $RPM_BUILD_ROOT/%{mozappdir}/defaults/profile/bookmarks.html
%if %{fedora} >= 7
ln -s %{default_bookmarks_file} $RPM_BUILD_ROOT/%{mozappdir}/defaults/profile/bookmarks.html
%else
%{__cp} %{SOURCE200} $RPM_BUILD_ROOT/%{mozappdir}/defaults/profile/bookmarks.html
%endif

%{__install} -p -D -m 644 %{SOURCE23} $RPM_BUILD_ROOT%{_mandir}/man1/firefox.1

%{__rm} -f $RPM_BUILD_ROOT/%{mozappdir}/firefox-config

#cd $RPM_BUILD_ROOT/%{mozappdir}/chrome
#find . -name "*" -type d -maxdepth 1 -exec %{__rm} -rf {} \;
#cd -

#%{__cat} > $RPM_BUILD_ROOT/%{mozappdir}/defaults/pref/firefox-l10n.js << EOF
#pref("general.useragent.locale", "chrome://global/locale/intl.properties");
#EOF
#%{__chmod} 644 $RPM_BUILD_ROOT/%{mozappdir}/defaults/pref/firefox-l10n.js

%{__cp} other-licenses/branding/%{firefox}/default16.png \
        $RPM_BUILD_ROOT/%{mozappdir}/icons/
%{__mkdir_p} $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/16x16/apps
%{__cp} other-licenses/branding/%{firefox}/default16.png \
        $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/16x16/apps/%{name}.png
%{__mkdir_p} $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/22x22/apps
%{__cp} other-licenses/branding/%{firefox}/default22.png \
        $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/22x22/apps/%{name}.png
%{__mkdir_p} $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/24x24/apps
%{__cp} other-licenses/branding/%{firefox}/default24.png \
        $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/24x24/apps/%{name}.png
%{__mkdir_p} $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/32x32/apps
%{__cp} other-licenses/branding/%{firefox}/default32.png \
        $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/32x32/apps/%{name}.png
%{__mkdir_p} $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/48x48/apps
%{__cp} other-licenses/branding/%{firefox}/default48.png \
        $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/48x48/apps/%{name}.png
%{__mkdir_p} $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/256x256/apps
%{__cp} other-licenses/branding/%{firefox}/default256.png \
        $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/256x256/apps/%{name}.png

echo > ../%{name}.lang
%if %{build_langpacks}
# Install langpacks
%{__mkdir_p} $RPM_BUILD_ROOT/%{mozappdir}/langpacks
%{__tar} xjf %{SOURCE2}
for langpack in `ls firefox-langpacks/*.xpi`; do
  language=`basename $langpack .xpi`
  extensiondir=$RPM_BUILD_ROOT/%{mozappdir}/langpacks/langpack-$language@firefox.mozilla.org
  %{__mkdir_p} $extensiondir
  unzip $langpack -d $extensiondir
  find $extensiondir -type f | xargs chmod 644

  tmpdir=`mktemp -d %{name}.XXXXXXXX`
  langtmp=$tmpdir/%{name}/langpack-$language
  %{__mkdir_p} $langtmp
  jarfile=$extensiondir/chrome/$language.jar
  unzip $jarfile -d $langtmp

  sed -i -e "s|browser.startup.homepage.*$|browser.startup.homepage=%{homepage}|g;" \
         $langtmp/locale/browser-region/region.properties

  find $langtmp -type f | xargs chmod 644
  %{__rm} -rf $jarfile
  cd $langtmp
  zip -r -D $jarfile locale
  cd -
  %{__rm} -rf $tmpdir

  language=`echo $language | sed -e 's/-/_/g'`
  extensiondir=`echo $extensiondir | sed -e "s,^$RPM_BUILD_ROOT,,"`
  echo "%%lang($language) $extensiondir" >> ../%{name}.lang
done
%{__rm} -rf firefox-langpacks
%endif # build_langpacks

# System extensions
%{__mkdir_p} $RPM_BUILD_ROOT%{_datadir}/mozilla/extensions/%{firefox_app_id}
%{__mkdir_p} $RPM_BUILD_ROOT%{_libdir}/mozilla/extensions/%{firefox_app_id}

# Copy over the LICENSE
%{__install} -p -c -m 644 LICENSE $RPM_BUILD_ROOT/%{mozappdir}

%if %{fedora} >= 7
# Use the system hunspell dictionaries
%{__rm} -rf $RPM_BUILD_ROOT/%{mozappdir}/dictionaries
ln -s %{_datadir}/myspell $RPM_BUILD_ROOT%{mozappdir}/dictionaries
%endif

# ghost files
touch $RPM_BUILD_ROOT/%{mozappdir}/components/compreg.dat
touch $RPM_BUILD_ROOT/%{mozappdir}/components/xpti.dat

# jemalloc shows up sometimes, but it's not needed here, it's in XR
#%{__rm} -f $RPM_BUILD_ROOT/%{mozappdir}/libjemalloc.so

# Remi : this appears on Fedora <= 10
%{__rm} -f $RPM_BUILD_ROOT/%{mozappdir}/*.chk


#---------------------------------------------------------------------

%clean
%{__rm} -rf $RPM_BUILD_ROOT

#---------------------------------------------------------------------

%pre
echo -e "\nWARNING : This %{name} RPM is not an official Fedora build and it"
echo -e "overrides the official one. Don't file bugs on Fedora Project.\n"
echo -e "Use dedicated forums http://forums.famillecollet.com/\n"

%if %{?fedora}%{!?fedora:99} <= 10
echo -e "WARNING : Fedora %{fedora} is now EOL :"
echo -e "You should consider upgrading to a supported release.\n"
%endif

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

%preun
# is it a final removal?
if [ $1 -eq 0 ]; then
  %{__rm} -rf %{mozappdir}/components
  %{__rm} -rf %{mozappdir}/extensions
  %{__rm} -rf %{mozappdir}/langpacks
  %{__rm} -rf %{mozappdir}/plugins
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files -f %{name}.lang
%defattr(-,root,root,-)
%{_bindir}/%{name}
%{_mandir}/man1/*
%dir %{_datadir}/mozilla/extensions/%{firefox_app_id}
%dir %{_libdir}/mozilla/extensions/%{firefox_app_id}
%{_datadir}/applications/mozilla-%{name}.desktop
%dir %{mozappdir}
%doc %{mozappdir}/LICENSE
%doc %{mozappdir}/README.txt
%{mozappdir}/*.properties
%{mozappdir}/chrome
%dir %{mozappdir}/components
%ghost %{mozappdir}/components/compreg.dat
%ghost %{mozappdir}/components/xpti.dat
%{mozappdir}/components/*.so
%{mozappdir}/components/*.xpt
%attr(644, root, root) %{mozappdir}/blocklist.xml
%attr(644, root, root) %{mozappdir}/components/*.js
%attr(644, root, root) %{mozappdir}/components/components.list
%{mozappdir}/defaults
%{mozappdir}/greprefs
%{mozappdir}/dictionaries
%dir %{mozappdir}/extensions
%{mozappdir}/extensions/{972ce4c6-7e08-4474-a285-3208198ce6fd}
%dir %{mozappdir}/langpacks
%{mozappdir}/icons
%{mozappdir}/searchplugins
%{mozappdir}/firefox
%{mozappdir}/firefox-bin
%{mozappdir}/modules
%{mozappdir}/plugins
%{mozappdir}/res
%{mozappdir}/*.so
%{mozappdir}/plugin-container
%{mozappdir}/mozilla-xremote-client
%{mozappdir}/platform.ini
%{mozappdir}/run-mozilla.sh
%{mozappdir}/application.ini
%{mozappdir}/.autoreg
# XXX See if these are needed still
%{mozappdir}/update*
%exclude %{mozappdir}/removed-files
%exclude %{_includedir}/firefox-%{internal_version}
%exclude %{_libdir}/firefox-devel-%{internal_version}
%exclude %{_datadir}/idl/firefox-%{internal_version}
%{_datadir}/icons/hicolor/16x16/apps/%{name}.png
%{_datadir}/icons/hicolor/22x22/apps/%{name}.png
%{_datadir}/icons/hicolor/24x24/apps/%{name}.png
%{_datadir}/icons/hicolor/256x256/apps/%{name}.png
%{_datadir}/icons/hicolor/32x32/apps/%{name}.png
%{_datadir}/icons/hicolor/48x48/apps/%{name}.png

#---------------------------------------------------------------------

%changelog
* Sat May 29 2010 Remi Collet <rpms@famillecollet.com> - 3.6.4-0.3.build6
- update to Firefox 3.6.4 Beta (build6)

* Fri May 14 2010 Remi Collet <rpms@famillecollet.com> - 3.6.4-0.2.build4
- update to Firefox 3.6.4 Beta (build4)

* Thu May 13 2010 Remi Collet <rpms@famillecollet.com> - 3.6.4-0.1.build3
- update to Firefox 3.6.4 Beta (build3)

* Sat Apr 10 2010 Remi Collet <rpms@famillecollet.com> - 3.6.3-2.plugin1
- update to Firefox "lorentz" 3.6.3plugin1

* Fri Apr 02 2010 Remi Collet <rpms@famillecollet.com> - 3.6.3-1
- Update to Firefox 3.6.3 (sources from mercurial)

* Tue Mar 23 2010 Remi Collet <rpms@famillecollet.com> - 3.6.2-1
- Update to Firefox 3.6.2

* Thu Mar 18 2010 Remi Collet <rpms@famillecollet.com> - 3.6.2-0.3.build3
- Update to Firefox 3.6.2 Candidate Build 3

* Mon Mar 15 2010 Remi Collet <rpms@famillecollet.com> - 3.6.2-0.1.build1
- Update to Firefox 3.6.2 Candidate Build 1

* Thu Jan 21 2010 Remi Collet <rpms@famillecollet.com> - 3.6-1
- Update to Firefox 3.6 Finale

* Sat Jan 09 2010 Remi Collet <rpms@famillecollet.com> - 3.6-0.5.rc1
- Update to Firefox 3.6 Release Candidate 1

* Thu Dec 17 2009 Remi Collet <rpms@famillecollet.com> - 3.6-0.4.beta5
- Update to Firefox 3.6 Beta 5

* Thu Nov 26 2009 Remi Collet <rpms@famillecollet.com> - 3.6-0.4.beta4
- Update to Firefox 3.6 Beta 4

* Wed Nov 18 2009 Remi Collet <rpms@famillecollet.com> - 3.6-0.3.beta3
- Update to Firefox 3.6 Beta 3
- switch from firefox36 to firefox

* Tue Nov 10 2009 Remi Collet <rpms@famillecollet.com> - 3.6-0.2.beta2
- Update to Firefox 3.6 Beta 2

* Fri Nov  6 2009 Remi Collet <rpms@famillecollet.com> - 3.6-0.1.beta1
- Update to Firefox 3.6 Beta 1

* Thu Nov  5 2009 Remi Collet <rpms@famillecollet.com> - 3.5.5-1
- Update to Firefox 3.5.5 Final Release

* Thu Nov  5 2009 Jan Horak <jhorak@redhat.com> - 3.5.5-1
- Update to 3.5.5

* Wed Oct 28 2009 Remi Collet <rpms@famillecollet.com> - 3.5.4-1
- Update to Firefox 3.5.4 Final Release

* Mon Oct 26 2009 Jan Horak <jhorak@redhat.com> - 3.5.4-1
- Update to 3.5.4

* Wed Sep 9 2009 Remi Collet <rpms@famillecollet.com> - 3.5.3-1
- Update to Firefox 3.5.3 Final Release

* Mon Sep  7 2009 Jan Horak <jhorak@redhat.com> - 3.5.3-1
- Updated to 3.5.3.

* Thu Aug 6 2009 Martin Stransky <stransky@redhat.com> - 3.5.2-3
- Fix for #437596 - Firefox needs to register proper name
  for session restore.

* Tue Aug 4 2009 Remi Collet <rpms@famillecollet.com> - 3.5.2-1
- Update to Firefox 3.5.2 Final Release

* Mon Aug 3 2009 Martin Stransky <stransky@redhat.com> - 3.5.2-2
- Updated to 3.5.2.

* Fri Jul 24 2009 Jan Horak <jhorak@redhat.com> - 3.5.1-3
- Adjust icons cache update according to template

* Fri Jul 17 2009 Remi Collet <rpms@famillecollet.com> - 3.5.1-1
- Update to Firefox 3.5.1 Final Release

* Fri Jul 17 2009 Remi Collet <rpms@famillecollet.com> - 3.5.1-0.1.build1
- Update to Firefox 3.5.1 build1

* Wed Jun 30 2009 Remi Collet <rpms@famillecollet.com> - 3.5-1
- Update to Firefox 3.5 Final Release

* Wed Jun 27 2009 Remi Collet <rpms@famillecollet.com> - 3.5-0.27.rc3
- Update to Firefox 3.5 RC3

* Wed Jun 24 2009 Remi Collet <rpms@famillecollet.com> - 3.5-0.26.rc3.build2
- Update to Firefox 3.5 RC3 build2

* Fri Jun 19 2009 Remi Collet <rpms@famillecollet.com> - 3.5-0.26.rc2
- Update to Firefox 3.5 RC2

* Thu Jun 18 2009 Remi Collet <rpms@famillecollet.com> - 3.5-0.25.rc2.build2
- Update to Firefox 3.5 RC2 build2

* Wed Jun 17 2009 Remi Collet <rpms@famillecollet.com> - 3.5-0.24.rc1
- Update to Firefox 3.5 RC1

* Tue Jun 16 2009 Remi Collet <rpms@famillecollet.com> - 3.5-0.23.rc1.build2
- Update to Firefox 3.5 RC1 build2

* Sun Jun 14 2009 Remi Collet <rpms@famillecollet.com> - 3.5-0.22.rc1.build1
- Update to Firefox 3.5 RC1 build1

* Thu Jun 11 2009 Remi Collet <rpms@famillecollet.com> - 3.5-0.21.beta99
- Update to Firefox 3.5 Beta 99 (Preview)

* Tue Apr 28 2009 Remi Collet <rpms@famillecollet.com> - 3.5-0.2.beta4
- Update to Firefox 3.5 Beta 4

* Fri Apr 24 2009 Remi Collet <rpms@famillecollet.com> - 3.5-0.1.beta4
- Update to 3.5b4 build1
- use system-nss only if Fedora >= 11 (3.12.3)

* Thu Apr 23 2009 Remi Collet <rpms@famillecollet.com> - 3.1-0.1.beta3
- First Firefox 3.1 build from rawhide xulrunner + firefox spec

