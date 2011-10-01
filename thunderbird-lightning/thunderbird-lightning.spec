%global nspr_version 4.8.8
%global nss_version 3.12.10
%global cairo_version 1.10.0
%global freetype_version 2.1.9
%global lcms_version 1.19
%global sqlite_version 3.6.22
%global libnotify_version 0.4
# Update these two as a pair
%global thunderbird_version 7.0
%global thunderbird_next_version 8.0
%global lightprever b7
# Compatible versions are listed in:
# comm-release/calendar/lightning/install.rdf.rej
# comm-release/calendar/providers/gdata/install.rdf.rej
%global moz_objdir objdir-tb
%global lightning_extname %{_libdir}/mozilla/extensions/{3550f703-e582-4d05-9a08-453d09bdfdc6}/{e2fda1a4-762b-4020-b5ad-a41df1933103}
%global gdata_extname %{_libdir}/mozilla/extensions/{3550f703-e582-4d05-9a08-453d09bdfdc6}/{a62ef8ec-5fdc-40c2-873c-223b8a6925cc}

# The tarball is pretty inconsistent with directory structure.
# Sometimes there is a top level directory.  That goes here.
#
# IMPORTANT: If there is no top level directory, this should be
# set to the cwd, ie: '.'
#define tarballdir .
%global tarballdir comm-release

%global mozappdir         %{_libdir}/%{name}

Name:           thunderbird-lightning
Summary:        The calendar extension to Thunderbird
Version:        1.0
Release:        0.50.%{lightprever}%{?dist}
URL:            http://www.mozilla.org/projects/calendar/lightning/
License:        MPLv1.1 or GPLv2+ or LGPLv2+
Group:          Applications/Productivity
#Someday lightning will produce a release we can use
Source0:        http://releases.mozilla.org/pub/mozilla.org/calendar/lightning/releases/1.0b7/source/lightning-1.0b7.source.tar.bz2
#Source0:        http://releases.mozilla.org/pub/mozilla.org/thunderbird/releases/%{thunderbird_version}/source/thunderbird-%{thunderbird_version}.source.tar.bz2
# This script will generate the language source below
Source1:        mklangsource.sh
Source2:        l10n-miramar.tar.bz2
# Config file for compilation
Source10:       thunderbird-mozconfig
# Finds requirements provided outside of the current file set
Source100:      find-external-requires


# Mozilla (XULRunner) patches
Patch0:         thunderbird-install-dir.patch
Patch8:         xulrunner-6.0-secondary-ipc.patch


BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
%if 0%{?fedora} >= 14
BuildRequires:  nspr-devel >= %{nspr_version}
BuildRequires:  nss-devel >= %{nss_version}
%endif
%if 0%{?fedora} > 15
BuildRequires:  nss-static
%endif
%if %{fedora} >= 15
# Library requirements (cairo-tee >= 1.10)
BuildRequires:  cairo-devel >= %{cairo_version}
%endif
BuildRequires:  libnotify-devel >= %{libnotify_version}
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
BuildRequires:  hunspell-devel
%if 0%{?fedora} >= 15
# Need SQLITE_SECURE_DELETE option
BuildRequires:  sqlite-devel >= %{sqlite_version}
%endif
BuildRequires:  startup-notification-devel
BuildRequires:  alsa-lib-devel
BuildRequires:  autoconf213
BuildRequires:  desktop-file-utils
BuildRequires:  libcurl-devel
BuildRequires:  python
BuildRequires:  yasm
BuildRequires:  mesa-libGL-devel
BuildRequires:  GConf2-devel
BuildRequires:  lcms-devel >= %{lcms_version}
%ifarch %{ix86} x86_64
BuildRequires:  wireless-tools-devel
%endif

Requires:       thunderbird >= %{thunderbird_version}
Obsoletes:      thunderbird-lightning-wcap <= 0.8
Provides:       thunderbird-lightning-wcap = %{version}-%{release}
AutoProv: 0
%global _use_internal_dependency_generator 0
%global __find_requires %{SOURCE100}


%description
Lightning brings the Sunbird calendar to the popular email client,
Mozilla Thunderbird. Since it's an extension, Lightning is tightly
integrated with Thunderbird, allowing it to easily perform email-related
calendaring tasks.


%prep
echo TARGET = %{name}-%{version}-%{release}
%setup -q -c -a 2

cd %{tarballdir}

lightprever=$(cat calendar/sunbird/config/version.txt)
if [ "$lightprever" != "%{version}%{lightprever}" ]; then
  echo Bad version, detected=$lightprever, expected=%{version}%{lightprever}
  exit 1
fi

%patch0  -p2 -b .dir
# Mozilla (XULRunner) patches
cd mozilla
%patch8 -p2 -b .secondary-ipc
cd ..

%{__rm} -f .mozconfig
#{__cp} %{SOURCE10} .mozconfig
cat %{SOURCE10} 		\
%if %{fedora} < 15
  | grep -v system-sqlite 	\
%endif
%if %{fedora} < 14
  | grep -v system-nss 		\
  | grep -v system-nspr 	\
%endif
%if %{fedora} < 15
  | grep -v enable-system-cairo    \
%endif
%ifarch %{ix86} x86_64
  | grep -v disable-necko-wifi 	\
%endif
  | tee .mozconfig

cat <<EOF | tee -a .mozconfig
ac_add_options --enable-libnotify
ac_add_options --enable-system-lcms
%if %{fedora} >= 15
ac_add_options --enable-system-sqlite
%endif
%if %{fedora} < 14
ac_add_options --disable-libjpeg-turbo
%endif
EOF

# Fix permissions
find -name \*.js | xargs chmod -x

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

%global moz_make_flags -j1
%ifarch ppc ppc64 s390 s390x
%global moz_make_flags -j1
%else
%global moz_make_flags %{?_smp_mflags}
%endif

export LDFLAGS="-Wl,-rpath,%{mozappdir}"
export MAKE="gmake %{moz_make_flags}"
make -f client.mk build STRIP=/bin/true

# Package l10n files
cd objdir-tb/calendar/lightning
make AB_CD=all L10N_XPI_NAME=lightning-all repack-clobber-all
grep -v 'osx' ../../../calendar/locales/shipped-locales | while read lang x
do
   make AB_CD=all L10N_XPI_NAME=lightning-all libs-$lang
done

#===============================================================================

%install
rm -rf $RPM_BUILD_ROOT
cd %{tarballdir}

# Avoid "Chrome Registration Failed" message on first startup and extension installation
mkdir -p $RPM_BUILD_ROOT%{lightning_extname}
touch $RPM_BUILD_ROOT%{lightning_extname}/chrome.manifest
mkdir -p $RPM_BUILD_ROOT%{gdata_extname}
touch $RPM_BUILD_ROOT%{gdata_extname}/chrome.manifest

# Lightning and GData provider for it
unzip -qod $RPM_BUILD_ROOT%{lightning_extname} objdir-tb/mozilla/dist/xpi-stage/lightning-all.xpi
unzip -qod $RPM_BUILD_ROOT%{gdata_extname} objdir-tb/mozilla/dist/xpi-stage/gdata-provider.xpi

# Fix up permissions
find $RPM_BUILD_ROOT -name \*.so | xargs chmod 0755

#===============================================================================

%clean
%{__rm} -rf $RPM_BUILD_ROOT

#===============================================================================

%files
%defattr(-,root,root,-)
%doc %{tarballdir}/mozilla/LEGAL %{tarballdir}/mozilla/LICENSE %{tarballdir}/mozilla/README.txt
%{lightning_extname}
%{gdata_extname}

#===============================================================================

%changelog
* Sat Oct 01 2011 Remi Collet <rpms@famillecollet.com> 1.0-0.50.b7
- Use lightning 1.0b7 source for TB 7
- sync with rawhide

* Wed Sep 28 2011 Orion Poplawski <orion@cora.nwra.com> - 1.0-0.50.b7
- Use lightning 1.0b7 source for TB 7
- Update l10n source
- Drop tbver patch

* Wed Aug 17 2011 Remi Collet <rpms@famillecollet.com> 1.0-0.48.b5pre
- Update to 1.0b5pre from Thunderbird 6.0 sources

* Wed Jul 20 2011 Remi Collet <rpms@famillecollet.com> 1.0-0.47.b4
- add patch for wcap bug https://bugzilla.mozilla.org/668153

* Tue Jul 19 2011 Remi Collet <rpms@famillecollet.com> 1.0-0.46.b4
- add langpacks

* Tue Jul 19 2011 Remi Collet <rpms@famillecollet.com> 1.0-0.45.b4
- rebuild for remi repo (and fix release)

* Tue Jul 19 2011 Dan Horák <dan[at]danny.cz> - 1.0-0.45.b3pre
- add xulrunner patches for secondary arches

* Mon Jul 18 2011 Jan Horak <jhorak@redhat.com> - 1.0-0.44.b3pre
- Require nss-static only for Fedora 16+

* Thu Jul 14 2011 Jan Horak <jhorak@redhat.com> - 1.0-0.43.b3pre
- Update to thunderbird 5 source
- Removed obsolete patches
- Adopted mozconfig from thunderbird package

* Tue Jun 28 2011 Orion Poplawski <orion@cora.nwra.com> 1.0-0.42.b3pre
- Update to thunderbird 3.1.11 source
- Drop notify patch, fixed upstream
- Change BR nss-devel to nss-static (Bug 717246)
- Add BR python

* Mon Apr 11 2011 Orion Poplawski <orion@cora.nwra.com> 1.0-0.41.b3pre
- Fix debuginfo builds
- Remove official branding sections
- Don't unpack the .xpi

* Wed Apr 6 2011 Orion Poplawski <orion@cora.nwra.com> 1.0-0.40.b3pre
- Fixup some file permissions
- Minor review cleanups

* Mon Apr 4 2011 Orion Poplawski <orion@cora.nwra.com> 1.0-0.39.b3pre
- Initial packaging, based on thunderbird 3.1.9
