Summary:    A portable abstraction library for DVD decryption
Name:       libdvdcss
Version:    1.2.12
Release:    1%{?dist}
License:    GPLv2+
Group:      System Environment/Libraries
Source:     http://www.videolan.org/pub/videolan/libdvdcss/%{version}/libdvdcss-%{version}.tar.bz2
URL:        http://www.videolan.org/libdvdcss/

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)


%description
This is a portable abstraction library for DVD decryption which is used by
the VideoLAN project, a full MPEG2 client/server solution.  You will need
to install this package in order to have encrypted DVD playback with the
VideoLAN client and the Xine navigation plugin.


%package devel
Summary:     Header files and development libraries for %{name}
Group:       Development/Libraries
Requires:    %{name} = %{version}-%{release}
Requires:    pkgconfig

%description devel
This package contains the header files and development libraries
for %{name}. If you like to develop programs using %{name}, 
you will need to install %{name}-devel.


%prep
%setup -q


%build
%configure
make %{_smp_mflags}


%install
rm -rf %{buildroot}
make  install DESTDIR=%{buildroot}


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING ChangeLog README
%exclude %{_libdir}/%{name}.a
%exclude %{_libdir}/%{name}.la
%{_libdir}/%{name}.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/dvdcss
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/%{name}.pc


%changelog
* Mon Mar 12 2012 Remi Collet <RPMS@famillecollet.com> - 1.2.12-1
- Update to 1.2.12

* Sat Feb 18 2012 Remi Collet <RPMS@famillecollet.com> - 1.2.11-2
- If unsure, assume the drive is of RPC-I type

* Mon Nov 22 2011 Remi Collet <RPMS@famillecollet.com> - 1.2.11-1
- Update to 1.2.11

* Sat Oct 16 2010 Remi Collet <RPMS@famillecollet.com> - 1.2.10-1
- F-14 rebuild

* Sun Sep 28 2008 Axel Thimm <Axel.Thimm@ATrpms.net> - 1.2.10-4
- Update to 1.2.10.

* Tue Sep 12 2006 Axel Thimm <Axel.Thimm@ATrpms.net> - 1.2.9-3
- Update to 1.2.9.

* Sun Aug  3 2003 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Update to 1.2.8.

* Wed Jun 25 2003 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Update to 1.2.7.

* Mon Mar 31 2003 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Rebuilt for Red Hat Linux 9.
- Exclude .la file.

* Tue Mar 11 2003 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Update to 1.2.6.

* Mon Feb  3 2003 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Update to 1.2.5.

* Fri Nov 15 2002 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Update to 1.2.4.

* Mon Oct 21 2002 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Update to 1.2.3.

* Thu Sep 26 2002 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Rebuilt for Red Hat Linux 8.0.

* Mon Aug 12 2002 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Update to 1.2.2.

* Mon Jun  3 2002 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Update to 1.2.1.

* Fri May 24 2002 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Update to 1.2.0.

* Thu May  2 2002 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Rebuilt against Red Hat Linux 7.3.
- Added the %%{?_smp_mflags} expansion.

* Mon Apr  8 2002 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Update to 1.1.1.

* Sun Nov  4 2001 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Changed to the Ogle patched version of the lib.

* Mon Oct 22 2001 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Initial RPM release.
- Decided to put libdvdcss in a separate package since both videolan and the
  xine DVD menu plugin use it.

