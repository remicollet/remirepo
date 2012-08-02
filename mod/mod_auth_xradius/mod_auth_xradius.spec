Summary:        Apache module that provides authentication against RADIUS Servers
Name:           mod_auth_xradius
Version:        0.4.6
Release:        16%{?dist}
Group:          System Environment/Daemons
URL:            http://www.outoforder.cc/projects/httpd/mod_auth_xradius/
License:        ASL 2.0
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0:        http://www.outoforder.cc/downloads/mod_auth_xradius/mod_auth_xradius-%{version}.tar.bz2
Source1:        auth_xradius.conf

Patch0:         %{name}-%{version}-memcache.patch
Patch1:         %{name}-%{version}-ha.patch
Patch2:         %{name}-%{version}-unixd.patch
Patch3:         %{name}-%{version}-share_libxradius.patch
Patch4:         %{name}-%{version}-libnss_libxradius.patch

BuildRequires:  apr-util-devel
BuildRequires:  httpd-devel
BuildRequires:  libtool
BuildRequires:  nspr-devel
BuildRequires:  nss-devel >= 3.12.5

%description
Apache module that provides high performance authentication against
RFC 2865 RADIUS Servers.

%package -n libxradius
Summary:        Development files for libxradius
Group:          Development/Libraries

%description -n libxradius
This is a library to generate RADIUS authentication request.

%package -n libxradius-devel
Summary:        Development files for libxradius
Group:          Development/Libraries
Requires:       libxradius%{?_isa} = %{version}-%{release}

%description -n libxradius-devel
The libradius-devel package contains libraries and header files for
developing applications that use libradius.

%prep
%setup -q
%patch0 -p1 -b .memcache
%patch1 -p1 -b .ha
# only for httpd 2.4
%patch2 -p1 -b .unixd
%patch3 -p1 -b .share_libxradius
%patch4 -p1 -b .libnss_libxradius

autoreconf -fvi


%build

%configure --localstatedir=/var/lib \
        --with-apxs=%{_sbindir}/apxs

make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install

# Install the radius library documentation
mkdir -p %{buildroot}%{_mandir}/man3
mkdir -p %{buildroot}%{_mandir}/man5
install -p -m644 libradius/libradius.3 %{buildroot}%{_mandir}/man3/libxradius.3
install -p -m644 libradius/radius.conf.5 %{buildroot}%{_mandir}/man5/radius.conf.5

# Install the apache module documentation
mkdir -p %{buildroot}%{_sysconfdir}/httpd/conf.d
mkdir -p %{buildroot}%{_libdir}/httpd/modules
install -p -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/httpd/conf.d/


%clean
rm -rf %{buildroot}

%post -n libxradius -p /sbin/ldconfig

%postun -n libxradius -p /sbin/ldconfig


%files
%doc README LICENSE NOTICE
%{_libdir}/httpd/modules/*.so
%config(noreplace) %{_sysconfdir}/httpd/conf.d/*.conf

%files -n libxradius
%defattr(-,root,root,-)
%doc README
%{_libdir}/libxradius.so.*
%{_mandir}/man5/radius.conf.5.*

%files -n libxradius-devel
%defattr(-,root,root,-)
%{_libdir}/libxradius.so
%{_mandir}/man3/libxradius.3.*
%{_includedir}/*.h


%changelog
* Thu Aug 23 2012 Remi Collet <RPMS@FamilleCollet.com> - 0.4.6-16
- backport for remi repo

* Mon Jul 23 2012 Simone Caronni <negativo17@gmail.com> - 0.4.6-16
- Fixed libxradius-devel requirement.

* Fri Jul 13 2012 Simone Caronni <negativo17@gmail.com> - 0.4.6-15
- Merged the 2 libnss patches into one.
- Fixed typo "xss_init_nss" in libnss patch.
- Removed _isa from BuildRequires.

* Fri Jul 13 2012 Stephen Gallagher <sgallagh@redhat.com> - 0.4.6-14
- Fix NSS initialization routines.

* Thu Jun 14 2012 Simone Caronni <negativo17@gmail.com> - 0.4.6-13
- Added libnss patch to libxradius.

* Tue Jun 12 2012 Simone Caronni <negativo17@gmail.com> - 0.4.6-12
- Added libnss patch to libxradius.

* Tue Jun 12 2012 Simone Caronni <negativo17@gmail.com> - 0.4.6-11
- Update memcache patch.
- Update libxradius patch.
- Swap automake17 BR with libtool.
- Use autoreconf instead of the 1.7 patched autogen.sh.

* Mon Jun 11 2012 Stephen Gallagher <sgallagh@redhat.com> - 0.4.6-10
- Rename subpackage to libxradius.
- Rename manpages and shared object.
- Properly link mod_auth_xradius with libxradius.
- Remove libradius makefile.

* Wed May 30 2012 Simone Caronni <negativo17@gmail.com> - 0.4.6-9
- First attempt in creating subpackages for libradius.
- Removed patch to rename radius calls.
- Removed macros for system commands.
- Used buildroot macro in a consistent way.

* Wed May 30 2012 Simone Caronni <negativo17@gmail.com> - 0.4.6-8
- Renamed libradius calls (xrad_ -> rad_) to use external library.

* Wed May 30 2012 Simone Caronni <negativo17@gmail.com> - 0.4.6-7
- Remove libmd BR.
- Reworked memcache patch.
- Updated patch for removing libradius.

* Mon May 21 2012 Simone Caronni <negativo17@gmail.com> - 0.4.6-6
- Strip out libmd and libradius.
- Remove libradius from sources.
- Added conditional for Fedora >= 18 patch.

* Wed May 15 2012 Simone Caronni <negativo17@gmail.com> - 0.4.6-5
- Added Provides for bundled md5 library.
- Added BSD license for bundled libradius library.

* Wed May 15 2012 Simone Caronni <negativo17@gmail.com> - 0.4.6-4
- Modified default configuration pointing only to localhost.
- Added patch for rawhide.

* Wed May 10 2012 Simone Caronni <negativo17@gmail.com> - 0.4.6-3
- First build based off rutgers.edu package.

* Thu Jul 22 2010 Orcan Ogetbil <orcan@nbcs.rutgers.edu> 0.4.6-2.ru
- Fixes in the .conf file
