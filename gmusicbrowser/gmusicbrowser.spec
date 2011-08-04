Name:      gmusicbrowser
Summary:   Jukebox for large collections of music files
Version:   1.1.7
Release:   2%{?dist}
License:   GPLv3+
Group:     Applications/Multimedia

URL:       http://gmusicbrowser.org/
Source0:   http://gmusicbrowser.org/download/%{name}-%{version}.tar.gz

Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch

BuildRequires:    desktop-file-utils
BuildRequires:    perl-devel
Requires(post):   desktop-file-utils
Requires(postun): desktop-file-utils

# Optionnal Deps and not detected
Requires:         perl(Gtk2::TrayIcon), perl(Locale::gettext) >= 1.04, perl(GStreamer)
Requires:         vorbis-tools, flac123, alsa-utils 
%if 0%{?fedora} < 14
Requires:         perl(Gtk2::MozEmbed)
%else
Requires:         perl(Gtk2::WebKit)
%endif


# We need to keep perl(Gtk2) perl(Gtk2::MozEmbed) perl(Gtk2::Notify)
# perl(Gtk2::Pango) perl(Gtk2::TrayIcon) perl(Gtk2::WebKit)

# RPM 4.8 style:
%{?filter_setup:
%filter_from_provides /perl(/d
%filter_from_requires /perl(simple_http)/d
%filter_from_requires /perl(gmusicbrowser/d
%filter_from_requires /perl(Layout::Label)/d
%filter_from_requires /perl(SongArray)/d
%filter_from_requires /perl(Gtk2::B/d
%filter_from_requires /perl(Gtk2::C/d
%filter_from_requires /perl(Gtk2::D/d
%filter_from_requires /perl(Gtk2::E/d
%filter_from_requires /perl(Gtk2::F/d
%filter_from_requires /perl(Gtk2::H/d
%filter_from_requires /perl(Gtk2::L/d
%filter_from_requires /perl(Gtk2::Notebook)/d
%filter_from_requires /perl(Gtk2::O/d
%filter_from_requires /perl(Gtk2::ProgressBar)/d
%filter_from_requires /perl(Gtk2::S/d
%filter_from_requires /perl(Gtk2::ToggleButton)/d
%filter_from_requires /perl(Gtk2::V/d
%filter_from_requires /perl(Gtk2::W/d
}
%{?perl_default_filter}

# RPM 4.9 style:
# Filter underspecified dependencies
%global __provides_exclude %{?__provides_exclude:__provides_exclude|}^perl\\(
%global __requires_exclude %{?__requires_exclude:__requires_exclude|}^perl\\(simple_http\\)
%global __requires_exclude %__requires_exclude|^perl\\(gmusicbrowser
%global __requires_exclude %__requires_exclude|^perl\\(Layout::Label\\)
%global __requires_exclude %__requires_exclude|^perl\\(SongArray)
%global __requires_exclude %__requires_exclude|^perl\\(Gtk2::B
%global __requires_exclude %__requires_exclude|^perl\\(Gtk2::C
%global __requires_exclude %__requires_exclude|^perl\\(Gtk2::D
%global __requires_exclude %__requires_exclude|^perl\\(Gtk2::E
%global __requires_exclude %__requires_exclude|^perl\\(Gtk2::F
%global __requires_exclude %__requires_exclude|^perl\\(Gtk2::H
%global __requires_exclude %__requires_exclude|^perl\\(Gtk2::L
%global __requires_exclude %__requires_exclude|^perl\\(Gtk2::Notebook\\)
%global __requires_exclude %__requires_exclude|^perl\\(Gtk2::O
%global __requires_exclude %__requires_exclude|^perl\\(Gtk2::ProgressBar\\)
%global __requires_exclude %__requires_exclude|^perl\\(Gtk2::S
%global __requires_exclude %__requires_exclude|^perl\\(Gtk2::ToggleButton\\)
%global __requires_exclude %__requires_exclude|^perl\\(Gtk2::V
%global __requires_exclude %__requires_exclude|^perl\\(Gtk2::W


%description
Jukebox for large collections of music files
Uses gstreamer, mpg321/ogg123/flac123  or mplayer for playback
Main features :
- customizable window layouts
- artist/album lock : easily restrict playlist to current artist/album
- easy access to related songs (same artist/album/title)
- simple mass-tagging and mass-renaming
- support multiple genres for each song
- customizable labels can be set for each song
- filters with unlimited nesting of conditions
- customizable weighted random mode


%prep
%setup -q


%build
# Empty


%install
rm -rf %{buildroot}

make install \
   prefix=%{_prefix} \
   DESTDIR=%{buildroot}

rm -f %{buildroot}/%{_prefix}/lib/menu/gmusicbrowser

desktop-file-install --vendor="" \
   --dir=%{buildroot}%{_datadir}/applications/ \
   %{buildroot}/%{_datadir}/applications/%{name}.desktop

%find_lang %{name}


%clean
rm -rf %{buildroot}


%post
update-desktop-database &> /dev/null ||:


%postun
update-desktop-database &> /dev/null ||:


%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS COPYING README NEWS layout_doc.html
%{_bindir}/%{name}
%{_datadir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_mandir}/man1/%{name}*
%{_datadir}/icons/%{name}.png
%{_datadir}/icons/large/%{name}.png
%{_datadir}/icons/mini/%{name}.png


%changelog
* Thu Aug 04 2011 Remi Collet <Fedora@FamilleCollet.com> - 1.1.7-2
- only requires perl(Gtk2::MozEmbed) on fedora < 15
  else requires perl(Gtk2::WebKit)
- fix filter for RPM 4.9

* Sun Mar 20 2011 Remi Collet <Fedora@FamilleCollet.com> - 1.1.7-1.1
- missing BR on perl-devel for filter

* Sun Mar 20 2011 Remi Collet <Fedora@FamilleCollet.com> - 1.1.7-1
- update to development version 1.1.7

* Sun Feb 20 2011 Remi Collet <Fedora@FamilleCollet.com> - 1.1.6-1
- update to 1.1.6
- fix URL and filter (hope this is temporary)

* Sun Dec 26 2010 Remi Collet <Fedora@FamilleCollet.com> - 1.1.6-0.1
- update to development version 1.1.6

* Wed Apr 21 2010 Remi Collet <Fedora@FamilleCollet.com> - 1.1.5-0.1
- update to development version 1.1.5

* Mon Feb 01 2010 Remi Collet <Fedora@FamilleCollet.com> - 1.1.4-0.1
- update to development version 1.1.4

* Sat Sep 26 2009 Remi Collet <Fedora@FamilleCollet.com> - 1.1.3-0.1
- update to development version 1.1.3

* Sun Sep 06 2009 Remi Collet <Fedora@FamilleCollet.com> - 1.1.2-0.1
- update to development version 1.1.2

* Sun Apr 26 2009 Remi Collet <Fedora@FamilleCollet.com> - 1.1.1-0.1
- update to development version 1.1.1

* Sun Apr 12 2009 Remi Collet <Fedora@FamilleCollet.com> - 1.0.1-2
- From review (#485961)
- preserve timestamp
- own all directory
- missing Requires
- fix license

* Tue Feb 17 2009 Remi Collet <Fedora@FamilleCollet.com> - 1.0.1-1
- Initial Fedora RPM from Quentin Sculo spec

