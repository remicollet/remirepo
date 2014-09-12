Name: libxmp
Version: 4.2.8
Release: 1%{?dist}
Summary: A multi-format module playback library
Group: System Environment/Libraries
Source0: http://downloads.sourceforge.net/project/xmp/libxmp/%{version}/libxmp-%{version}.tar.gz
Provides: bundled(md5-plumb)
License: BSD and LGPLv2+ and MIT and Public Domain
URL: http://xmp.sourceforge.net/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
Libxmp is a library that renders module files to PCM data. It supports
over 90 mainstream and obscure module formats including Protracker (MOD),
Scream Tracker 3 (S3M), Fast Tracker II (XM), and Impulse Tracker (IT).

Many compressed module formats are supported, including popular Unix, DOS,
and Amiga file packers including gzip, bzip2, SQSH, Powerpack, etc.

%package devel
Summary: A multi-format module playback library development files
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
Libxmp is a library that renders module files to PCM data. It supports
over 90 mainstream and obscure module formats including Protracker (MOD),
Scream Tracker 3 (S3M), Fast Tracker II (XM), and Impulse Tracker (IT).

Many compressed module formats are supported, including popular Unix, DOS,
and Amiga file packers including gzip, bzip2, SQSH, Powerpack, etc.

This package contains the header and development library.

%prep
%setup -q
for file in docs/Changelog ; do
        iconv -f iso8859-1 -t utf8 -o $file.utf $file && touch -r $file $file.utf && mv $file.utf $file
done

%build
%configure
make V=1 %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}
install -Dpm644 docs/libxmp.3 %{buildroot}%{_mandir}/man3/libxmp.3
chmod 755 %{buildroot}%{_libdir}/libxmp.so.*

%check
make check %{?_smp_mflags}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc README docs/COPYING.LIB docs/Changelog docs/CREDITS
%{_libdir}/libxmp.so.*

%files devel
%defattr(-,root,root,-)
%doc docs/libxmp.html docs/libxmp.pdf docs/*.txt
%{_includedir}/xmp.h
%{_mandir}/man3/libxmp.3*
%{_libdir}/pkgconfig/libxmp.pc
%{_libdir}/libxmp.so

%changelog
* Fri Sep 12 2014 Remi Collet <remi@fedoraproject.org> - 4.2.8-1
- backport for remi repository

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Jul 16 2014 Dominik Mierzejewski <rpm@greysector.net> - 4.2.8-1
- update to 4.2.8 (http://sourceforge.net/projects/xmp/files/libxmp/4.2.8/Changelog/view)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Apr 27 2014 Dominik Mierzejewski <rpm@greysector.net> - 4.2.7-1
- update to 4.2.7 (http://sourceforge.net/projects/xmp/files/libxmp/4.2.7/Changelog/view)

* Sun Mar 02 2014 Dominik Mierzejewski <rpm@greysector.net> - 4.2.5-1
- update to 4.2.5 (http://sourceforge.net/projects/xmp/files/libxmp/4.2.5/Changelog/view)

* Mon Feb 24 2014 Dominik Mierzejewski <rpm@greysector.net> - 4.2.4-1
- update to 4.2.4 (http://sourceforge.net/projects/xmp/files/libxmp/4.2.4/Changelog/view)
- drop the list of files with licenses other than LGPLv2.1+,
  it's growing too much

* Mon Jan 13 2014 Dominik Mierzejewski <rpm@greysector.net> - 4.2.2-1
- update to 4.2.2

* Sun Nov 17 2013 Dominik Mierzejewski <rpm@greysector.net> - 4.2.0-1
- update to 4.2.0 (http://sourceforge.net/projects/xmp/files/libxmp/4.2.0/Changelog/view)
- add proper provides for bundled md5-plumb (version unknown)
- drop any mention of unzoo.c, it's gone from the source

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jun 04 2013 Dominik Mierzejewski <rpm@greysector.net> - 4.1.5-1
- update to 4.1.5
- require the same arch of main package for -devel subpackage

* Wed May 29 2013 Dominik Mierzejewski <rpm@greysector.net> - 4.1.4-1
- update to 4.1.4
- drop st02-ok sample from -devel doc (removed by upstream)
- review fixes

* Mon Apr 29 2013 Dominik Mierzejewski <rpm@greysector.net> - 4.1.1-1
- initial build based on xmp.spec
