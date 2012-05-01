%global		date	2012.04.27
%global		live_soversion 0

Name:		live555
Version:	0
Release:	0.36.%{date}%{?dist}
Summary:	Live555.com streaming libraries

Group:		System Environment/Libraries
License:	LGPLv2+
URL:		http://live555.com/liveMedia/
Source0:	http://live555.com/liveMedia/public/live.%{date}.tar.gz
Patch0:		live.2012.04.27-shared.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Provides: live555date%{_isa} = %{date}
# Packages using live555 must Requires this:
#{?live555date:Requires: live555date%{_isa} = %{live555date}}


%description
This code forms a set of C++ libraries for multimedia streaming, 
using open standard protocols (RTP/RTCP, RTSP, SIP). These 
libraries - which can be compiled for Unix (including Linux and Mac OS X), 
Windows, and QNX (and other POSIX-compliant systems) - can be used 
to build streaming applications.
The libraries can also be used to stream, receive, and process MPEG, 
H.263+ or JPEG video, and several audio codecs. They can easily be 
extended to support additional (audio and/or video) codecs, and can 
also be used to build basic RTSP or SIP clients and servers, and have 
been used to add streaming support to existing media player applications.

%package	devel
Summary:	Development files for live555.com streaming libraries
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Obsoletes:	live-devel < 0-0.19.2008.04.03
Provides:	live-devel = %{version}-%{release}

%description	devel
This code forms a set of C++ libraries for multimedia streaming, 
using open standard protocols (RTP/RTCP, RTSP, SIP). These 
libraries - which can be compiled for Unix (including Linux and Mac OS X), 
Windows, and QNX (and other POSIX-compliant systems) - can be used 
to build streaming applications.
The libraries can also be used to stream, receive, and process MPEG, 
H.263+ or JPEG video, and several audio codecs. They can easily be 
extended to support additional (audio and/or video) codecs, and can 
also be used to build basic RTSP or SIP clients and servers, and have 
been used to add streaming support to existing media player applications.

%package	tools
Summary:	RTSP streaming tools using live555.com streaming libraries
Group:		Applications/Multimedia
Requires:	%{name} = %{version}-%{release}
Obsoletes:	live-tools < 0-0.19.2008.04.03
Provides:	live-tools = %{version}-%{release}

%description	tools
This code forms a set of C++ libraries for multimedia streaming, 
using open standard protocols (RTP/RTCP, RTSP, SIP). These 
libraries - which can be compiled for Unix (including Linux and Mac OS X), 
Windows, and QNX (and other POSIX-compliant systems) - can be used 
to build streaming applications.
The libraries can also be used to stream, receive, and process MPEG, 
H.263+ or JPEG video, and several audio codecs. They can easily be 
extended to support additional (audio and/or video) codecs, and can 
also be used to build basic RTSP or SIP clients and servers, and have 
been used to add streaming support to existing media player applications.

This package contains the live555.com streaming server
(live555MediaServer), the example programs (openRTSP, playSIP, sapWatch,
vobStreamer) and a variety of test tools.

%package	static
Summary:	Static libraries for %{name}
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description	static
The %{name}-static package contains static libraries for
developing applications that use %{name}.

%prep
%setup -q -n live
install -pm 0644 config.linux config.linux.static
%patch0 -p1 -b .shared


%build
./genMakefiles %{_target_os}.static
make %{?_smp_mflags} CFLAGS="$RPM_OPT_FLAGS"
mv $(find BasicUsageEnvironment groupsock liveMedia UsageEnvironment -name "*.a" ) $(pwd)
make clean

./genMakefiles %{_target_os}
make CFLAGS="$RPM_OPT_FLAGS -fPIC -DPIC" SO_VERSION="%{live_soversion}"

%install
rm -rf $RPM_BUILD_ROOT
install -dm 755 $RPM_BUILD_ROOT{%{_libdir},%{_bindir}}
for i in BasicUsageEnvironment groupsock liveMedia UsageEnvironment ; do
  install -dm 755 $RPM_BUILD_ROOT%{_includedir}/$i
  install -pm 644 $i/include/*.h* $RPM_BUILD_ROOT%{_includedir}/$i/
  install -pm 644 lib${i}.a $RPM_BUILD_ROOT%{_libdir}/lib${i}.a
  install -pm 755 $i/lib${i}.so $RPM_BUILD_ROOT%{_libdir}/lib${i}.so.%{date}
  ln -sf lib${i}.so.%{date} $RPM_BUILD_ROOT%{_libdir}/lib${i}.so.%{live_soversion}
  ln -sf lib${i}.so.%{date} $RPM_BUILD_ROOT%{_libdir}/lib${i}.so
done

install -pm755 mediaServer/live555MediaServer $RPM_BUILD_ROOT%{_bindir}
install -pm755 proxyServer/live555ProxyServer $RPM_BUILD_ROOT%{_bindir}
pushd testProgs
for i in \
  MPEG2TransportStreamIndexer \
  openRTSP \
  playSIP \
  sapWatch \
  testAMRAudioStreamer \
  testMP3Receiver \
  testMP3Streamer \
  testMPEG1or2AudioVideoStreamer \
  testMPEG1or2AudioVideoToDarwin \
  testMPEG1or2ProgramToTransportStream \
  testMPEG1or2Splitter \
  testMPEG1or2VideoReceiver \
  testMPEG1or2VideoStreamer \
  testMPEG2TransportStreamTrickPlay \
  testMPEG2TransportStreamer \
  testMPEG4VideoStreamer \
  testMPEG4VideoToDarwin \
  testOnDemandRTSPServer \
  testRelay \
  testWAVAudioStreamer \
  vobStreamer \
; do
  install -pm755 $i $RPM_BUILD_ROOT%{_bindir}
done
popd

#RPM Macros support
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/rpm
cat > $RPM_BUILD_ROOT%{_sysconfdir}/rpm/macros.live555 << EOF
# live555 RPM Macros
%live555date	%{date}
EOF
touch -r COPYING $RPM_BUILD_ROOT%{_sysconfdir}/rpm/macros.live555


%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_libdir}/libBasicUsageEnvironment.so.*
%{_libdir}/libgroupsock.so.*
%{_libdir}/libliveMedia.so.*
%{_libdir}/libUsageEnvironment.so.*

%files tools
%defattr(-,root,root,-)
%{_bindir}/*

%files devel
%defattr(-,root,root,-)
%doc COPYING README
%config %{_sysconfdir}/rpm/macros.live555
%{_libdir}/libBasicUsageEnvironment.so
%{_libdir}/libgroupsock.so
%{_libdir}/libliveMedia.so
%{_libdir}/libUsageEnvironment.so
%{_includedir}/BasicUsageEnvironment/
%{_includedir}/groupsock/
%{_includedir}/liveMedia/
%{_includedir}/UsageEnvironment/

%files static
%defattr(-,root,root,644)
%{_libdir}/libBasicUsageEnvironment*.a
%{_libdir}/libgroupsock*.a
%{_libdir}/libliveMedia*.a
%{_libdir}/libUsageEnvironment*.a

%changelog
* Tue May 01 2012 Remi Collet <RPMS@FamilleCollet.com> - 0-0.36.2012.04.27
- update to 2012.04.27, rebuild for remi repo
- add /usr/bin/live555ProxyServer

* Fri Mar 02 2012 Nicolas Chauvet <kwizart@gmail.com> - 0-0.36.2012.02.04
- Rebuilt for c++ ABI breakage

* Sun Feb 19 2012 Nicolas Chauvet <kwizart@gmail.com> - 0-0.35.2012.02.04
- Update to 2012.02.04

* Wed Jan 25 2012 Nicolas Chauvet <kwizart@gmail.com> - 0-0.34.2012.01.25
- Update to 2012.01.25
- Drop merged patch
- Back to LGPLv+2 license

* Mon Sep 19 2011 Nicolas Chauvet <kwizart@gmail.com> - 0-0.32.2011.09.02
- Update to 2011.09.02
- Reorder patches
- Add live-cloexec.patch and live-intptr.patch (rebased) from Rémi.

* Tue Jan 25 2011 Nicolas Chauvet <kwizart@gmail.com> - 0-0.30.2011.01.24
- Update to 2011.01.24
- Update live555 patches from Rémi.
- Use RPM macro to workaround inconsistent ABI dependency.

* Tue Jun 22 2010 Nicolas Chauvet <kwizart@gmail.com> - 0-0.28.2010.06.22
- Update to 2010.06.22

* Sat May  1 2010 Nicolas Chauvet <kwizart@fedoraproject.org> - 0-0.27.2010.04.09
- Update to 2010.04.09
- Add patches from Rémi Denis-Courmont - provided as GPLv2+
- Distribute live555 as GPLv2+

* Thu Jan 28 2010 Nicolas Chauvet <kwizart@fedoraproject.org> - 0-0.26.2010.01.22
- Update to 2010.01.22
  Fix multicast with openRTSP

* Sat Jan 16 2010 Nicolas Chauvet <kwizart@fedoraproject.org> - 0-0.25.2010.01.16
- Update to 2010.01.16
- Update patch for shared library

* Mon Aug 17 2009 kwizart < kwizart at gmail.com > - 0-0.24.2009.07.28
- 2009.07.28
- Revert circle dependency (prefer undefined non_weak_symbol)
- Disable static libraries compiled with fpic.
- Use c++ to link - BZ #564

* Fri Apr 17 2009 kwizart < kwizart at gmail.com > - 0-0.23.2009.04.07
- Unified patches. (unrelevant fixes dropped).

* Tue Apr 07 2009 Dominik Mierzejewski <rpm[AT]greysector.net> - 0-0.22.2009.04.07
- 2009.04.07
- use new debian patchset

* Sun Mar 29 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 0-0.21.2008.07.25
- rebuild for new F11 features

* Sun Aug 17 2008 Dominik Mierzejewski <rpm[AT]greysector.net> - 0-0.20.2008.07.25
- 2008.07.25
- devel-static -> static, per Fedora guidelines
- specfile whitespace cosmetics
- made tools depend on specific version until we have a stable ABI
- added proper obsoletes/provides to devel
- made -tools binaries installation independent of umask

* Mon May  5 2008 kwizart < kwizart at gmail.com > - 0-0.19.2008.04.03
- Rename package from live to live555 
  (live555-devel-static provides live-devel for compat)
- Enable shared build
- Split static pic and nopic into devel-static

* Sun Apr 06 2008 Dominik Mierzejewski <rpm[AT]greysector.net> - 0-0.18.2008.04.03
- 2008.04.03

* Sun Feb 24 2008 Dominik Mierzejewski <rpm[AT]greysector.net> - 0-0.17.2008.02.08
- 2008.02.08
- added tools subpackage

* Sat Dec 01 2007 Dominik Mierzejewski <rpm[AT]greysector.net> - 0-0.16.2007.11.18
- 2007.11.18
- fix CVE-2007-6036 (bug #1728)
- fix license tag
- store changelog.txt locally, because the one on the website is constantly updated

* Sun May 17 2007 Dominik Mierzejewski <rpm[AT]greysector.net> - 0-0.15.2007.04.24a
- 2007.04.24a
- use Debian patches

* Mon Sep 25 2006 Dams <anvil[AT]livna.org> - 0-0.13.2006.08.07%{?dist}
- Release bump

* Fri Aug 18 2006 Ville Skyttä <ville.skytta at iki.fi> - 0-0.12.2006.08.07
- changelog.txt changed upstream :(

* Thu Aug 10 2006 Ville Skyttä <ville.skytta at iki.fi> - 0-0.11.2006.08.07
- 2006.08.07.
- Drop no longer needed live Obsoletes and Provides.
- Install into usual system locations, ship both PIC and non-PIC libs
  (from Debian).

* Thu Jun 22 2006 Ville Skyttä <ville.skytta at iki.fi> - 0-0.11.2006.06.22
- 2006.06.22.
- Re-enable parallel make.

* Thu Mar 09 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- switch to new release field
- add another 0 for switch cvs -> release

* Tue Feb 28 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- add dist

* Thu Feb 23 2006 Ville Skyttä <ville.skytta at iki.fi> 0-0.lvn.11.2006.02.15
- Update to 2006.02.15.

* Mon Jan 16 2006 Adrian Reber <adrian@lisas.de> - 0-0.lvn.11.2006.01.05
- Updated to 2006.01.05
- Drop Epoch

* Tue Aug  9 2005 Ville Skyttä <ville.skytta at iki.fi> 0:0-0.lvn.10.2005.08.09
- 2005.08.09.
- Rename binary package to -devel.
- Ship changelog.txt.
- Clean up unused stuff from specfile.

* Tue Dec 28 2004 Dams <anvil[AT]livna.org> - 0:0-0.lvn.10.2004.12.23
- Updated to version 2004.12.23

* Fri Nov 12 2004 Dams <anvil[AT]livna.org> - 0:0-0.lvn.9.2004.11.11a
- Updated to version 2004.11.11a

* Thu May 20 2004 Dams <anvil[AT]livna.org> - 0:0-0.lvn.8.2004.05.19
- Added Source1:changelog.txt

* Thu May 20 2004 Dams <anvil[AT]livna.org> - 0:0-0.lvn.7.2004.05.19
- Updated version
- URL in Source0

* Sun Apr  4 2004 Dams <anvil[AT]livna.org> 0:0-0.lvn.6.2004.03.31
- Removed testprograms package

* Wed Mar 31 2004 Dams <anvil[AT]livna.org> 0:0-0.lvn.5.2004.03.31
- Updated version 2004-03-31

* Wed Jan  7 2004 Dams <anvil[AT]livna.org> 0:0-0.fdr.4.2003.11.25
- Patch from Marius to make makefile honor rpm optflags
- Removed URL in Source0

* Wed Jan  7 2004 Dams <anvil[AT]livna.org> 0:0-0.fdr.3.2003.11.25
- Removed all .o files

* Fri Dec 12 2003 Dams <anvil[AT]livna.org> 0:0-0.fdr.2.2003.11.25
- Snipped the devel pacakge. 

* Fri Dec 12 2003 Dams <anvil[AT]livna.org> 0:0-0.fdr.1.2003.11.25
- Version-Release respecting fedora.us guidelines
- Spec file cleanup. 

* Sat Nov 29 2003 Peter Backlund <peter dot backlund at home dot se> - 0:0.0.2003.11.25-0.fdr.1
- Added 0.0. to version, to allow for upgrade to 0.x/1.x release
 
* Sat Nov 29 2003 Peter Backlund <peter dot backlund at home dot se> - 0:2003.11.25-0.fdr.1
- New upstream release

* Sun Nov 16 2003 Peter Backlund <peter dot backlund at home dot se> - 0:2003.11.14-0.fdr.2
- Removed unnecessary BuildReq.
- Removed smp job macro.
- Replaced sed with perl.

* Fri Nov 14 2003 Peter Backlund <peter dot backlund at home dot se> - 0:2003.11.14-0.fdr.1
- Initial RPM release.
