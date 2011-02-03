# Separated plugins are supported on x86(64) only
%ifarch i386 i686 x86_64
%define separated_plugins 1
%else
%define separated_plugins 0
%endif

%define homepage http://start.fedoraproject.org/
%define default_bookmarks_file %{_datadir}/bookmarks/default-bookmarks.html
%define firefox_app_id \{ec8030f7-c20a-464f-9b0e-13a3a9e97384\}

%global shortname		firefox
%global internal_version	4
%global mycomment   		Beta 11 build2 candidate

%global mozappdir               %{_libdir}/%{shortname}-%{internal_version}
%global tarballdir              mozilla-central

# xulrunner_version matches the firefox package.
# xulrunner_version_max is first next incompatible xulrunner version
%define xulrunner_version       2.0-0.19
%define xulrunner_version_max   2.1

%define official_branding       1
%define build_langpacks         1
%define include_debuginfo       0

%if ! %{official_branding}
%define cvsdate 20080327
%define nightly .cvs%{cvsdate}
%else
%define prever  b11
%endif

Summary:        Mozilla Firefox Web browser
Name:           %{shortname}
Version:        4.0
Release:        0.22.beta11.build2%{?dist}
URL:            http://www.mozilla.org/projects/firefox/
License:        MPLv1.1 or GPLv2+ or LGPLv2+
Group:          Applications/Internet
Source0:        ftp://ftp.mozilla.org/pub/firefox/releases/%{version}%{?prever}/source/firefox-%{version}%{?prever}.source.tar.bz2
%if %{build_langpacks}
Source1:        firefox-langpacks-%{version}%{?prever}-20110203.tar.bz2
%endif
Source10:       firefox-mozconfig
Source11:       firefox-mozconfig-branded
Source12:       firefox-redhat-default-prefs.js
Source13:       firefox-mozconfig-debuginfo
Source20:       firefox.desktop
Source21:       firefox.sh.in
Source23:       firefox.1
# Not necessary
# Source100:      find-external-requires


#Build patches
Patch0:         firefox-version.patch

# Fedora patches
Patch11:        firefox-default.patch

# Upstream patches

%if %{official_branding}
# Required by Mozilla Corporation


%else
# Not yet approved by Mozillla Corporation


%endif

# ---------------------------------------------------

BuildRequires:  desktop-file-utils
BuildRequires:  system-bookmarks
BuildRequires:  xulrunner2-devel >= %{xulrunner_version}
# For WebM support
BuildRequires:	yasm

Requires:       xulrunner2 >= %{xulrunner_version}
Conflicts:      xulrunner2 >= %{xulrunner_version_max}
Requires:       system-bookmarks
Obsoletes:      mozilla <= 37:1.7.13
Provides:       webclient
%if %{name} == %{shortname}
Obsoletes:      firefox4
Provides:       firefox4 = %{version}-%{release}
%endif


# %%define _use_internal_dependency_generator 0
# %%define __find_requires %{SOURCE100}

# 10k of 11k files are in langpacks
%{?filter_setup:
%filter_provides_in %{mozappdir}/langpacks
%filter_requires_in %{mozappdir}/langpacks
%filter_setup
}


%description
Mozilla Firefox is an open-source web browser, designed for standards
compliance, performance and portability.

#---------------------------------------------------------------------

%prep
%setup -q -c
cd %{tarballdir}

sed -e 's/__RPM_VERSION_INTERNAL__/%{internal_version}/' %{P:%%PATCH0} \
    > version.patch
%{__patch} -p1 -b --suffix .version --fuzz=0 < version.patch
    

# For branding specific patches.

# Fedora patches
%patch11 -p2 -b .default

%if %{official_branding}
# Required by Mozilla Corporation

%else
# Not yet approved by Mozilla Corporation
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

%if %{official_branding}
%{__cat} %{SOURCE11} >> .mozconfig
%endif
%if %{include_debuginfo}
%{__cat} %{SOURCE13} >> .mozconfig
%endif

echo "ac_add_options --enable-system-lcms" >> .mozconfig

# Set up SDK path
echo "ac_add_options --with-libxul-sdk=\
`pkg-config --variable=sdkdir libxul`" >> .mozconfig

%if !%{?separated_plugins}
echo "ac_add_options --disable-ipc" >> .mozconfig
%endif

#---------------------------------------------------------------------

%build
cd %{tarballdir}

# Mozilla builds with -Wall with exception of a few warnings which show up
# everywhere in the code; so, don't override that.
#
# Disable C++ exceptions since Mozilla code is not exception-safe
#
MOZ_OPT_FLAGS=$(echo $RPM_OPT_FLAGS | \
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

INTERNAL_GECKO=%{internal_version}
MOZ_APP_DIR=%{_libdir}/%{shortname}-${INTERNAL_GECKO}

export LDFLAGS="-Wl,-rpath,${MOZ_APP_DIR}"
make -f client.mk build STRIP="/bin/true" MOZ_MAKE_FLAGS="$MOZ_SMP_FLAGS" MOZ_SERVICES_SYNC="1"

# create debuginfo for crash-stats.mozilla.com
%if %{include_debuginfo}
#cd %{moz_objdir}
make buildsymbols
%endif

#---------------------------------------------------------------------

%install
cd %{tarballdir}

INTERNAL_GECKO=%{internal_version}

INTERNAL_APP_NAME=%{shortname}-${INTERNAL_GECKO}
MOZ_APP_DIR=%{_libdir}/${INTERNAL_APP_NAME}

DESTDIR=$RPM_BUILD_ROOT make install

%{__mkdir_p} $RPM_BUILD_ROOT{%{_libdir},%{_bindir},%{_datadir}/applications}

sed -e 's/^Name=.*/Name=Firefox %{version} %{?mycomment}/' \
    -e "s/firefox/%{name}/" \
    %{SOURCE20} | tee %{name}.desktop

desktop-file-install --vendor mozilla \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications \
  --delete-original %{name}.desktop 

# set up the firefox start script
%{__rm} -rf $RPM_BUILD_ROOT%{_bindir}/%{shortname}
XULRUNNER_DIR=`pkg-config --variable=libdir libxul | %{__sed} -e "s,%{_libdir},,g"`
%{__cat} %{SOURCE21} | %{__sed} -e 's,FIREFOX_VERSION,%{internal_version},g' \
		     | %{__sed} -e "s,XULRUNNER_DIRECTORY,$XULRUNNER_DIR,g"  \
		     | %{__sed} -e "s,FIREFOXBIN,%{name},g" > \
  $RPM_BUILD_ROOT%{_bindir}/%{name}
%{__chmod} 755 $RPM_BUILD_ROOT%{_bindir}/%{name}

# Remove binary stub from xulrunner
%{__rm} -rf $RPM_BUILD_ROOT/%{mozappdir}/%{shortname}

# set up our default preferences - (change Vendor to Remi, requested by upstream)
%{__cat} %{SOURCE12} | %{__sed} -e 's,FIREFOX_RPM_VR,%{version}-%{release},g' -e 's,Fedora,Remi,g' | tee rh-default-prefs

# resolves bug #461880
%{__cat} > $RPM_BUILD_ROOT/%{mozappdir}/browserconfig.properties << EOF
browser.startup.homepage=%{homepage}
EOF

# Export correct locale
%{__cat} > $RPM_BUILD_ROOT/%{mozappdir}/defaults/preferences/firefox-l10n.js << EOF
pref("general.useragent.locale", "chrome://global/locale/intl.properties");
EOF
%{__chmod} 644 $RPM_BUILD_ROOT/%{mozappdir}/defaults/preferences/firefox-l10n.js

# place the preferences
%{__cp} rh-default-prefs $RPM_BUILD_ROOT/%{mozappdir}/defaults/preferences/all-remi.js
%{__rm} rh-default-prefs

# set up our default bookmarks
%{__rm} -f $RPM_BUILD_ROOT/%{mozappdir}/defaults/profile/bookmarks.html
ln -s %{default_bookmarks_file} $RPM_BUILD_ROOT/%{mozappdir}/defaults/profile/bookmarks.html

%{__install} -p -D -m 644 %{SOURCE23} $RPM_BUILD_ROOT%{_mandir}/man1/%{name}.1

%{__rm} -f $RPM_BUILD_ROOT/%{mozappdir}/firefox-config

%{__cp} other-licenses/branding/%{shortname}/default16.png \
        $RPM_BUILD_ROOT/%{mozappdir}/icons/
%{__mkdir_p} $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/16x16/apps
%{__cp} other-licenses/branding/%{shortname}/default16.png \
        $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/16x16/apps/%{name}.png
%{__mkdir_p} $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/22x22/apps
%{__cp} other-licenses/branding/%{shortname}/default22.png \
        $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/22x22/apps/%{name}.png
%{__mkdir_p} $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/24x24/apps
%{__cp} other-licenses/branding/%{shortname}/default24.png \
        $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/24x24/apps/%{name}.png
%{__mkdir_p} $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/32x32/apps
%{__cp} other-licenses/branding/%{shortname}/default32.png \
        $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/32x32/apps/%{name}.png
%{__mkdir_p} $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/48x48/apps
%{__cp} other-licenses/branding/%{shortname}/default48.png \
        $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/48x48/apps/%{name}.png
%{__mkdir_p} $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/256x256/apps
%{__cp} other-licenses/branding/%{shortname}/default256.png \
        $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/256x256/apps/%{name}.png

echo > ../%{name}.lang
%if %{build_langpacks}
# Install langpacks
%{__mkdir_p} $RPM_BUILD_ROOT/%{mozappdir}/langpacks
%{__tar} xjf %{SOURCE1}
for langpack in `ls firefox-langpacks/*.xpi`; do
  language=`basename $langpack .xpi`
  extensiondir=$RPM_BUILD_ROOT/%{mozappdir}/langpacks/langpack-$language@firefox.mozilla.org
  %{__mkdir_p} $extensiondir
  unzip -q $langpack -d $extensiondir
  find $extensiondir -type f | xargs chmod 644

  sed -i -e "s|browser.startup.homepage.*$|browser.startup.homepage=%{homepage}|g;" \
         $extensiondir/chrome/$language/locale/branding/browserconfig.properties

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

# ghost files
touch $RPM_BUILD_ROOT/%{mozappdir}/components/compreg.dat
touch $RPM_BUILD_ROOT/%{mozappdir}/components/xpti.dat

# Enable crash reporter for Firefox application
%if %{include_debuginfo}
sed -i -e "s/\[Crash Reporter\]/[Crash Reporter]\nEnabled=1/" $RPM_BUILD_ROOT/%{mozappdir}/application.ini
%endif

#---------------------------------------------------------------------

%pre
echo -e "\nWARNING : This %{name} %{version} %{mycomment} RPM is not an official"
echo -e "Fedora build and it overrides the official one. Don't file bugs on Fedora Project.\n"
echo -e "Use dedicated forums http://forums.famillecollet.com/\n"

%if %{?fedora}%{!?fedora:99} <= 12
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

%if %{name} == %{shortname}
%preun
# is it a final removal?
if [ $1 -eq 0 ]; then
  %{__rm} -rf %{mozappdir}/components
  %{__rm} -rf %{mozappdir}/extensions
  %{__rm} -rf %{mozappdir}/langpacks
  %{__rm} -rf %{mozappdir}/plugins
fi
%endif


%files -f %{name}.lang
%defattr(-,root,root,-)
%{_bindir}/%{name}
%doc %{_mandir}/man1/*
%dir %{_datadir}/mozilla/extensions/%{firefox_app_id}
%dir %{_libdir}/mozilla/extensions/%{firefox_app_id}
%{_datadir}/applications/mozilla-%{name}.desktop
%dir %{mozappdir}
%doc %{mozappdir}/LICENSE
%doc %{mozappdir}/README.txt
%{mozappdir}/*.properties
%{mozappdir}/chrome
%{mozappdir}/chrome.manifest
%dir %{mozappdir}/components
%ghost %{mozappdir}/components/compreg.dat
%ghost %{mozappdir}/components/xpti.dat
%{mozappdir}/components/*.so
%{mozappdir}/components/*.xpt
# %{mozappdir}/components/browser.manifest
%{mozappdir}/components/components.manifest
%{mozappdir}/components/interfaces.manifest
%attr(644, root, root) %{mozappdir}/blocklist.xml
%attr(644, root, root) %{mozappdir}/components/*.js
%{mozappdir}/defaults
%dir %{mozappdir}/extensions
%{mozappdir}/extensions/{972ce4c6-7e08-4474-a285-3208198ce6fd}
%if %{build_langpacks}
%dir %{mozappdir}/langpacks
%endif
%{mozappdir}/icons
%{mozappdir}/searchplugins
%{mozappdir}/run-mozilla.sh
%{mozappdir}/application.ini
%dir %{mozappdir}/modules
%{mozappdir}/modules/distribution.js
%{mozappdir}/modules/openLocationLastURL.jsm
%{mozappdir}/modules/NetworkPrioritizer.jsm
%{mozappdir}/modules/NetworkHelper.jsm
%{mozappdir}/modules/PlacesUIUtils.jsm
%{mozappdir}/modules/stylePanel.jsm
%{mozappdir}/modules/tabview/
%{mozappdir}/modules/services-sync/
%{mozappdir}/modules/services-crypto/WeaveCrypto.js
%{mozappdir}/modules/domplate.jsm
%{mozappdir}/modules/PropertyPanel.jsm
%{mozappdir}/modules/HUDService.jsm
%exclude %{mozappdir}/removed-files
%{_datadir}/icons/hicolor/16x16/apps/%{name}.png
%{_datadir}/icons/hicolor/22x22/apps/%{name}.png
%{_datadir}/icons/hicolor/24x24/apps/%{name}.png
%{_datadir}/icons/hicolor/256x256/apps/%{name}.png
%{_datadir}/icons/hicolor/32x32/apps/%{name}.png
%{_datadir}/icons/hicolor/48x48/apps/%{name}.png

%if %{include_debuginfo}
#%{mozappdir}/crashreporter
%{mozappdir}/crashreporter-override.ini
#%{mozappdir}/Throbber-small.gif
#%{mozappdir}/plugin-container
%endif

#---------------------------------------------------------------------

%changelog
* Thu Feb 03 2011 Remi Collet <RPMS@FamilleCollet.com> - 4.0-0.22.beta11.build2
- 4.0b11 build2 candidate

* Wed Feb 02 2011 Remi Collet <RPMS@FamilleCollet.com> - 4.0-0.21.beta10
- sync with rawhide, use system xulrunner2

* Tue Jan 25 2011 Christopher Aillon <caillon@redhat.com> - 4.0-0.13b10
- Firefox 4.0 Beta 10

* Fri Jan 14 2011 Christopher Aillon <caillon@redhat.com> - 4.0-0.12b9
- Firefox 4.0 Beta 9

* Thu Jan 6 2011 Dan Horák <dan[at]danny.cz> - 4.0-0.11b8
- disable ipc on non-x86 arches to match xulrunner

* Thu Jan 6 2011 Martin Stransky <stransky@redhat.com> - 4.0-0.10b8
- application.ini permission check fix

* Thu Jan 6 2011 Martin Stransky <stransky@redhat.com> - 4.0-0.9b8
- Fixed rhbz#667477 - broken launch script

* Tue Jan 4 2011 Martin Stransky <stransky@redhat.com> - 4.0-0.8b8
- Fixed rhbz#664877 - Cannot read application.ini

* Tue Dec 21 2010 Martin Stransky <stransky@redhat.com> - 4.0-0.7b8
- Update to Beta 8
- Fixed rhbz#437608 - When prelink is installed, 
  rpm builds are garbage

* Wed Dec  8 2010 Christopher Aillon <caillon@redhat.com> - 4.0-0.6b7
- Use official branding since this is an official beta
- Fix Tab Candy/Panorama (#658573)

* Thu Nov 11 2010 Jan Horak <jhorak@redhat.com> - 4.0b7-1
- Update to 4.0b7
- Added x-scheme-handler to firefox.desktop

* Wed Sep 29 2010 jkeating - 4.0-0.4b6
- Rebuilt for gcc bug 634757

* Tue Sep 21 2010 Martin Stransky <stransky@redhat.com> - 4.0-0.3.b6
- Update to 4.0 Beta 6

* Tue Sep  7 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 4.0-0.2.b4
- get package building and mostly functional

* Mon Aug 30 2010 Martin Stransky <stransky@redhat.com> - 4.0-0.1.b4
- Update to 4.0 Beta 4

