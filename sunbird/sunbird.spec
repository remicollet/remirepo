%define nspr_version 4.8
%define nss_version 3.12.3.99
%define cairo_version 1.8.8
%define dbus_glib_version 0.6
%define sqlite_version 3.6.22
%define lcms_version 1.19

%bcond_without lightning
%ifarch ppc
%if 0%{?rhel}
%define with_lightning %{nil}
%endif
%endif

%define version_internal 1.0b2
%define progdir %{_libdir}/%{name}-%{version_internal}pre
%define thunderbird_internal 3.1
%define thunderbird_version  3.1.2
%define libnotify_version 0.4
%define thundir %{_libdir}/thunderbird-%{thunderbird_internal}

# This is to filter unwanted provides, that should be provided only by gecko-devel
%define _use_internal_dependency_generator 0
%define __find_requires %{SOURCE100} %{buildroot}

Name:           sunbird
Version:        1.0
Release:        0.28%{?dist}
Summary:        Calendar application built upon Mozilla toolkit

Group:          Applications/Productivity
License:        MPLv1.1 or GPLv2+ or LGPLv2+
URL:            http://www.mozilla.org/projects/calendar/sunbird/
#Source0:        http://releases.mozilla.org/pub/mozilla.org/calendar/sunbird/releases/%{version}/source/lightning-sunbird-%{version}-source.tar.bz2
Source0:        thunderbird-%{thunderbird_version}.source.tar.bz2
Source1:        sunbird.desktop
Source2:        sunbird-l10n.tar
#sunbird-langpacks-0.9.tar.gz
#Source3:        mozilla-extension-update.sh
# This is used just for langpacks.
# TODO: build them!
Source4:        http://releases.mozilla.org/pub/mozilla.org/calendar/lightning/releases/1.0b2/linux-i686/lightning.xpi
Source5:        http://releases.mozilla.org/pub/mozilla.org/calendar/lightning/releases/1.0b2/linux-i686/gdata-provider.xpi
Source100:      find-external-requires

# Pulled from Thunderbird
Patch0:         mozilla-jemalloc.patch
# Fixes gcc complain that nsFrame::delete is protected
Patch1:         xulrunner-1.9.2.1-build.patch

# Ours
Patch10:        sunbird-1.0-libical.patch
Patch11:        sunbird-1.0-uilocale.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  libIDL-devel
BuildRequires:  desktop-file-utils
BuildRequires:  libgnomeui-devel
BuildRequires:  krb5-devel
BuildRequires:  pango-devel >= 1.22
BuildRequires:  freetype-devel >= 2.1.9
BuildRequires:  libXt-devel
BuildRequires:  libXrender-devel
BuildRequires:  desktop-file-utils
%if 0%{?fedora} >= 11
BuildRequires:  nspr-devel >= %{nspr_version}
BuildRequires:  nss-devel >= %{nss_version}
%endif
BuildRequires:  dbus-glib-devel >= %{dbus_glib_version}
BuildRequires:  libpng-devel, libjpeg-devel, gtk2-devel
BuildRequires:  zlib-devel, gzip, zip, unzip
BuildRequires:  GConf2-devel
BuildRequires:  gnome-vfs2-devel
BuildRequires:  libical-devel
BuildRequires:  zip
BuildRequires:  autoconf213
BuildRequires:  alsa-lib-devel
%if 0%{fedora} >= 11
BuildRequires:  cairo-devel >= %{cairo_version}
Requires:       nspr >= %{nspr_version}
Requires:       nss >= %{nss_version}
%endif
%if 0%{?fedora} >= 13
BuildRequires:  sqlite-devel >= %{sqlite_version}
%endif
%if %{fedora} >= 10
BuildRequires:  libnotify-devel >= %{libnotify_version}
%endif
%if %{fedora} >= 9
BuildRequires:  lcms-devel >= %{lcms_version}
%endif
%ifarch %{ix86} x86_64
BuildRequires:  wireless-tools-devel
%endif


Requires(post):  desktop-file-utils
Requires(postun): desktop-file-utils

AutoProv: 0

%description
Mozilla Sunbird is a cross-platform calendar application, built upon
Mozilla Toolkit. It brings Mozilla-style ease-of-use to your
calendar, without tying you to a particular storage solution.


%if %with lightning
%package -n thunderbird-lightning
Summary:        The calendar extension to Thunderbird
Group:          Applications/Productivity
Requires:       thunderbird >= %{thunderbird_version}
Obsoletes:      thunderbird-lightning-wcap <= 0.8
Provides:       thunderbird-lightning-wcap = %{version}-%{release}
AutoProv: 0

%description -n thunderbird-lightning
Lightning brings the Sunbird calendar to the popular email client,
Mozilla Thunderbird. Since it's an extension, Lightning is tightly
integrated with Thunderbird, allowing it to easily perform email-related
calendaring tasks.

%define lightning_extname \{e2fda1a4-762b-4020-b5ad-a41df1933103\}
%define gdata_extname \{a62ef8ec-5fdc-40c2-873c-223b8a6925cc\}
%endif


%prep
%setup -n comm-1.9.2 -q -a 2
%patch0 -p0 -b .jemalloc
%patch1 -p1 -b .protected
%patch10 -p0 -b .libical
%patch11 -p0 -b .uilocale

find . -name '*.cpp' -o -name '*.h' |xargs chmod -x


%build
cat >.mozconfig <<EOF
ac_add_options --disable-crashreporter
ac_add_options --disable-debug
ac_add_options --disable-installer
ac_add_options --disable-install-strip
ac_add_options --disable-strip
ac_add_options --disable-tests
ac_add_options --disable-updater
ac_add_options --disable-xprint
ac_add_options --enable-application=calendar
ac_add_options --enable-calendar
ac_add_options --enable-canvas
ac_add_options --enable-default-toolkit=cairo-gtk2
ac_add_options --enable-optimize="$(echo $RPM_OPT_FLAGS |sed -e 's/-O2/-Os/;s/-Wall//')"
ac_add_options --enable-pango
ac_add_options --enable-svg
%if %{fedora} >= 11
ac_add_options --enable-system-cairo
%endif
ac_add_options --enable-xinerama
ac_add_options --libdir="%{_libdir}"
ac_add_options --prefix="%{_prefix}"
ac_add_options --with-pthreads
ac_add_options --with-system-jpeg
%if %{fedora} >= 11
ac_add_options --with-system-nspr
ac_add_options --with-system-nss
%endif
ac_add_options --with-system-zlib
%if %{fedora} >= 10
ac_add_options --enable-libnotify
%else
ac_add_options --disable-libnotify
%endif
%if %{fedora} >= 11
ac_add_options --enable-system-lcms
%endif
%if %{fedora} >= 13
ac_add_options --enable-system-sqlite
%endif
%ifarch ppc ppc64
ac_add_options --disable-necko-wifi
%endif
EOF

make -f client.mk build


%install
rm -rf $RPM_BUILD_ROOT

# make install is bogus
# copy tree, break symlinks
mkdir -p $RPM_BUILD_ROOT%{progdir}
cp -rL mozilla/dist/bin/* $RPM_BUILD_ROOT%{progdir}
mkdir $RPM_BUILD_ROOT%{_bindir}
mv $RPM_BUILD_ROOT%{progdir}/%{name} $RPM_BUILD_ROOT%{_bindir}/%{name}

desktop-file-install --vendor="fedora"                  \
        --dir=$RPM_BUILD_ROOT%{_datadir}/applications/  \
        %{SOURCE1}

# Icon
mkdir -p $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/128x128/apps
cp $RPM_BUILD_ROOT%{progdir}/chrome/icons/default/default128.png \
        $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/128x128/apps/%{name}.png

# Install langpacks
mkdir -p $RPM_BUILD_ROOT%{progdir}/extensions
ls sunbird-l10n/*.xpi |while read PACK
do
        LANGUAGE=$(echo $PACK |sed 's,sunbird-l10n/sunbird-%{version_internal}pre.\(.*\).langpack.xpi,\1,')
        DIR=$RPM_BUILD_ROOT%{progdir}/extensions/langpack-$LANGUAGE@sunbird.mozilla.org
        mkdir -p $DIR
        unzip -qod $DIR $PACK
        find $DIR -type f |xargs chmod 0644

        # Fix #441500
        sed 's/\r//g' $DIR/install.rdf |awk '/^$/ {next} {print}' >lala
        touch -r $DIR/install.rdf lala
        mv lala $DIR/install.rdf

done

# GData provider for sunbird
mkdir -p $RPM_BUILD_ROOT%{progdir}/extensions/%{gdata_extname}
touch $RPM_BUILD_ROOT%{progdir}/extensions/%{gdata_extname}/chrome.manifest
unzip -qod $RPM_BUILD_ROOT%{progdir}/extensions/%{gdata_extname} \
        mozilla/dist/xpi-stage/gdata-provider.xpi

%if %with lightning
# Avoid "Chrome Registration Failed" message on first startup and extension installation
touch $RPM_BUILD_ROOT%{progdir}/extensions/%{lightning_extname}/chrome.manifest
touch $RPM_BUILD_ROOT%{progdir}/extensions/%{gdata_extname}/chrome.manifest

# Lightning and GData provider for it
%{__mkdir_p} $RPM_BUILD_ROOT%{thundir}/extensions/%{lightning_extname}
unzip -qod   $RPM_BUILD_ROOT%{thundir}/extensions/%{lightning_extname} mozilla/dist/xpi-stage/lightning.xpi

%{__mkdir_p} $RPM_BUILD_ROOT%{thundir}/extensions/%{gdata_extname}
unzip -qod   $RPM_BUILD_ROOT%{thundir}/extensions/%{gdata_extname} mozilla/dist/xpi-stage/gdata-provider.xpi
#install -p -m 755 %{SOURCE3} $RPM_BUILD_ROOT%{_libdir}/thunderbird-lightning/mozilla-extension-update.sh

# Unpack lightning language packs, except en_US
unzip -l %{SOURCE4} '*.jar' |
        awk '/-[^\/]*\.jar/ && !/en-US/ {print $4}' |
        xargs unzip -qod $RPM_BUILD_ROOT%{thundir}/extensions/%{lightning_extname} %{SOURCE4}

# Register them
ls $RPM_BUILD_ROOT%{thundir}/extensions/%{lightning_extname}/chrome |
        sed -n '/en-US/n;s/\(\([^-]*\)-\(.*\)\.jar\)/locale \2 \3 jar:chrome\/\1!\/locale\/\3\/\2\//p' \
        >>$RPM_BUILD_ROOT%{thundir}/extensions/%{lightning_extname}/chrome.manifest

# Unpack lightning language packs, except en_US
unzip -l %{SOURCE5} '*.jar' |
        awk '/-[^\/]*\.jar/ && !/en-US/ {print $4}' |
        xargs unzip -qod $RPM_BUILD_ROOT%{thundir}/extensions/%{gdata_extname} %{SOURCE5}

# Register them
ls $RPM_BUILD_ROOT%{thundir}/extensions/%{gdata_extname}/chrome |
        sed -n '/en-US/n;s/\(\([^-]*\)-\(.*\)\.jar\)/locale \2 \3 jar:chrome\/\1!\/locale\/\3\/\2\//p' \
        >>$RPM_BUILD_ROOT%{thundir}/extensions/%{gdata_extname}/chrome.manifest
%endif

# Permissions fixup
find $RPM_BUILD_ROOT -name '*.xpm' -o -name '*.js' |
        xargs chmod 0644 mozilla/LICENSE
find $RPM_BUILD_ROOT -name '*.so' |xargs chmod 0755

%clean
rm -rf $RPM_BUILD_ROOT


%post
update-desktop-database %{_datadir}/applications
touch --no-create %{_datadir}/icons/hicolor
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
        %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi


%postun
update-desktop-database %{_datadir}/applications
touch --no-create %{_datadir}/icons/hicolor
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
        %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi


%if %with lightning
%pre -n thunderbird-lightning
# Remomve link from previous installation
if [ -L %{mozappdir}/extensions/%{lightning_extname} ]; then
    %{__rm} %{mozappdir}/extensions/%{lightning_extname}
fi
if [ -L %{mozappdir}/extensions/%{gdata_extname} ]; then
    %{__rm} %{mozappdir}/extensions/%{gdata_extname}
fi
%endif


%files
%defattr(-,root,root,-)
%doc mozilla/LEGAL mozilla/LICENSE mozilla/README.txt
%{progdir}
%{_bindir}/sunbird
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/128x128/apps/sunbird.png


%if %with lightning
%files -n thunderbird-lightning
%doc mozilla/LEGAL mozilla/LICENSE mozilla/README.txt
%defattr(-,root,root,-)
%{thundir}/extensions/%{lightning_extname}
%{thundir}/extensions/%{gdata_extname}
%endif


%changelog
* Fri Aug 06 2010 Remi Collet <rpms@famillecollet.com> 1.0-0.28
- Rebuild against Thunderbird 3.1.2
- add fixlang.php

* Wed Jul 21 2010 Remi Collet <rpms@famillecollet.com> 1.0-0.27
- Rebuild against Thunderbird 3.1.1

* Sat Jul 10 2010 Remi Collet <rpms@famillecollet.com> 1.0-0.26.b2pre
- remove link mecanism as thundebird dir is now stable (see #608511)
- add locales from 1.0b2

* Sat Jun 25 2010 Remi Collet <rpms@famillecollet.com> 1.0-0.25.b2pre
- Rebuild for remi repo

* Thu Jun 24 2010 Jan Horak <jhorak@redhat.com> - 1.0-0.25.b2pre
- Rebuild against Thunderbird 3.1

* Tue Jun 22 2010 Jan Horak <jhorak@redhat.com> - 1.0-0.24.b2pre
- Fixed Thunderbird requires version

* Tue Jun 22 2010 Jan Horak <jhorak@redhat.com> - 1.0-0.23.b2pre
- Rebuild against Thunderbird 3.1 RC2

* Tue Mar 30 2010 Remi Collet <rpms@famillecollet.com> 1.0-0.21.20090916hg.fc#.remi
- Rebuild for Fedora <= 10

* Tue Mar 30 2010 Jan Horak <jhorak@redhat.com> - 1.0-0.21.20090916hg
- Rebuild against new Thunderbird

* Mon Mar  1 2010 Remi Collet <rpms@famillecollet.com> 1.0-0.20.20090916hg.fc#.remi
- Rebuild for Fedora <= 10

* Mon Mar  1 2010 Jan Horak <jhorak@redhat.com> - 1.0-0.20.20090916hg
- Rebuild against new Thunderbird

* Thu Feb 25 2010 Remi Collet <rpms@famillecollet.com> 1.0-0.19.20090916hg.fc#.remi
- Rebuild for Fedora <= 10

* Thu Feb 25 2010 Jan Horak <jhorak@redhat.com> - 1.0-0.19.20090916hg
- Rebuild against new Thunderbird

* Thu Jan 21 2010 Remi Collet <rpms@famillecollet.com> 1.0-0.17.20090916hg.fc#.remi
- Rebuild for Fedora <= 10

* Thu Jan 21 2010 Jan Horak <jhorak@redhat.com> - 1.0-0.17.20090916hg
- Rebuild against new Thunderbird

* Wed Nov 25 2009 Remi Collet <rpms@famillecollet.com> 1.0-0.14.20090916hg.fc#.remi
- Rebuild for Fedora <= 10

* Wed Nov 25 2009 Jan Horak <jhorak@redhat.com> - 1.0-0.14.20090916hg
- Rebuild against new Thunderbird

* Thu Sep 24 2009 Remi Collet <rpms@famillecollet.com> 1.0-0.7.20090715hg.fc#.remi
- Rebuild for Fedora <= 10

* Tue Sep 22 2009 Jan Horak <jhorak@redhat.com> - 1.0-0.7.20090715hg
- Sync up with Thunderbird

* Sun Aug 16 2009 Remi Collet <rpms@famillecollet.com> 1.0-0.5.20090715hg.fc#.remi
- Rebuild for Fedora <= 10

* Sun Jun 28 2009 Lubomir Rintel <lkundrak@v3.sk> - 1.0-0.5.20090715hg
- Sync up with Thunderbird

* Sun Jun 28 2009 Lubomir Rintel <lkundrak@v3.sk> - 1.0-0.5.20090513hg
- Sync up with Thunderbird
- Enable the Google Data Provider

* Sat May 02 2009 Remi Collet <rpms@famillecollet.com> 1.0-0.2.20090302hg.fc#.remi
- Rebuild for Fedora <= 10

* Wed Apr 29 2009 Lubomir Rintel <lkundrak@v3.sk> - 1.0-0.2.20090302hg
- Fix the permissions for real now

* Tue Apr 28 2009 Lubomir Rintel <lkundrak@v3.sk> - 1.0-0.1.20090302hg
- Update to version matching current Thunderbird

* Sun Mar 1 2009 Lubomir Rintel <lkundrak@v3.sk> 0.9-6
- Fix build with GCC 4.4

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Nov 24 2008 Lubomir Rintel <lkundrak@v3.sk> 0.9-4
- Disable lightning on EL-5 ppc, since there's no Desktop with thunderbird
- Fix summary

* Thu Oct 2 2008 Lubomir Rintel <lkundrak@v3.sk> 0.9-3
- Attempt to fix the libical patch's timezone problem

* Wed Sep 24 2008 Lubomir Rintel <lkundrak@v3.sk> 0.9-2
- Fix problem with symbol visibility and newer gcc I introduced with libical patch

* Tue Sep 23 2008 Lubomir Rintel <lkundrak@v3.sk> 0.9-1
- 0.9 GOLD
- Fix use of system nss and nspr4
- Link against system libical (#459923)
- Add language packs for lightning (#449770)

* Sun Aug 24 2008 Lubomir Rintel <lkundrak@v3.sk> 0.9-0.3.20080824cvs
- Newer snapshot closer to RC
- New langpacks
- Fix install root path

* Mon Aug 11 2008 Lubomir Rintel <lkundrak@v3.sk> 0.9-0.2.20080807cvs
- Get rid of relative symlinks
- Remove lignthing's libcalbasecomps.so provide
- Fix dependencies of scriptlets

* Sun Aug 10 2008 Lubomir Rintel <lkundrak@v3.sk> 0.9-0.1.20080807cvs
- First attempt at 0.9, CVS snapshot close to first RC
- Rewrite the requires generation, for it suffered bitrot

* Mon May 19 2008 Lubomir Rintel <lkundrak@v3.sk> 0.8-4
- Rebuild for new hunspell

* Tue Apr 08 2008 Lubomir Kundrak <lkundrak@redhat.com> 0.8-3
- Really fix lightning dependencies (#441340)
- Fix "da" and "it" lanugage packs (#441500)

* Mon Apr 07 2008 Lubomir Kundrak <lkundrak@redhat.com> 0.8-2
- Blacklist dependencies of lightning on files included in tb (#441340)
- Fix the extension update scriptlet escaping

* Fri Apr 04 2008 Lubomir Kundrak <lkundrak@redhat.com> 0.8-1
- 0.8 GA

* Fri Apr 04 2008 Lubomir Kundrak <lkundrak@redhat.com> 0.8-0.3.cvs20080331
- Translations

* Tue Apr 01 2008 Lubomir Kundrak <lkundrak@redhat.com> 0.8-0.2.cvs20080331
- Unbreak dependencies (hopefully)
- Try concurrent builds again, they seem to work now

* Tue Apr 01 2008 Lubomir Kundrak <lkundrak@redhat.com> 0.8-0.1.cvs20080331
- Corrected license tag to mention all the applicable Licenses
- Use libxul from XULrunner
- Post 0.8 Release Candidate 1
- Obsolete wcap subpackage -- got merged into mainline lightning

* Sun Mar 09 2008 Lubomir Kundrak <lkundrak@redhat.com> 0.7-10
- Parralel makes were failing unpredictably

* Thu Feb 28 2008 Lubomir Kundrak <lkundrak@redhat.com> 0.7-9
- Try to use the correct locale (#436693)

* Mon Jan 21 2008 Lubomir Kundrak <lkundrak@redhat.com> 0.7-8
- Streamlined BuildRequires a bit
- Do not provide stuff that has to be provided by firefox
- Do not require what's in our fileset
- Removed redundant and useless Source0 without upstream

* Thu Jan 03 2008 Lubomir Kundrak <lkundrak@redhat.com> 0.7-7
- Add patch to correct build with FORTIFY_SOURCE
- Replace the name in .desktop file with a more descriptive one
- Add translations to .desktop file

* Sun Dec 30 2007 Aurelien Bompard <abompard@fedoraproject.org> 0.7-6
- disable updater

* Tue Dec 11 2007 Aurelien Bompard <abompard@fedoraproject.org> 0.7-5
- fix debuginfo package

* Tue Oct 30 2007 Aurelien Bompard <abompard@fedoraproject.org> 0.7-4
- rename the mozilla-lightning subpackage to thunderbird-lightning
  since it's a thunderbird extension
- create a "chrome.manifest" file to avoid "Chrome Registration Failed" message

* Mon Oct 29 2007 Aurelien Bompard <abompard@fedoraproject.org> 0.7-3
- be even more complicated: build the wcap-enabler extension
  (really, it's just cut'n'paste)

* Mon Oct 29 2007 Aurelien Bompard <abompard@fedoraproject.org> 0.7-2
- split the lightning package
- use scriptlets and triggers based on the mugshot package

* Sat Oct 27 2007 Aurelien Bompard <abompard@fedoraproject.org> 0.7-1
- version 0.7

* Tue Sep 11 2007 Aurelien Bompard <abompard@fedoraproject.org> 0.5-3
- minor spec cleanups
- build the Lightning extension
- add an option to build with official branding

* Sun Sep 09 2007 Aurelien Bompard <abompard@fedoraproject.org> 0.5-2
- fix icon

* Wed Jul 25 2007 Aurelien Bompard <abompard@fedoraproject.org> 0.5-1
- initial release
