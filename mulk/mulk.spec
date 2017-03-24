Name:		mulk
Version:	0.6.0
Release:	1%{?dist}
Summary:	Non-interactive multi-connection network downloader

Group:		Applications/Internet
License:	GPLv3
URL:		http://mulk.sourceforge.net/
Source0:	http://downloads.sourceforge.net/project/mulk/mulk/mulk%200.6.0/mulk-0.6.0.tar.gz
Patch1:		mulk-0.6.0-curl.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	gettext curl-devel uriparser-devel libtidy-devel
Requires:	curl uriparser

%description
Multi-connection command line tool for downloading Internet sites with image
filtering and Metalink support. Similar to wget and cURL, but it manages up
to 50 simultaneous and parallel links. Main features are: HTML code parsing,
recursive fetching, Metalink retrieving, segmented download and image filtering
by width and height. It is based on libcurl, liburiparser, libtidy, libmetalink
and libcrypto. 


%prep
%setup -q
%patch1 -p1


%build
%configure --disable-metalink
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
%find_lang %{name}


%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig


%files -f %{name}.lang
%defattr(-,root,root,-)
%{_bindir}/mulk
%{_libdir}/libmulk.la
%{_libdir}/libmulk.so.0
%{_libdir}/libmulk.so.0.0.0
%doc
%{_mandir}/man1/mulk.1.gz




%changelog
* Sun Mar 04 2012 Steve Mokris <smokris@softpixel.com> 0.6.0-1
- Initial version of the package





%package devel
Summary:	Non-interactive multi-connection network downloader
Group:		Development/Libraries

%description devel
Multi-connection command line tool for downloading Internet sites with image
filtering and Metalink support. Similar to wget and cURL, but it manages up
to 50 simultaneous and parallel links. Main features are: HTML code parsing,
recursive fetching, Metalink retrieving, segmented download and image filtering
by width and height. It is based on libcurl, liburiparser, libtidy, libmetalink
and libcrypto. 

%files devel
%defattr(-,root,root,-)
%{_includedir}/mulk/mulk.h
%{_libdir}/libmulk.a
%{_libdir}/libmulk.so
