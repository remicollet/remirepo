Name:        vsqlite++
Version:    0.3.9
Release:    3%{?dist}
Summary:    Well designed C++ sqlite 3.x wrapper library

Group:      Development/Libraries
License:    BSD
URL:        https://github.com/vinzenz/vsqlite--
Source0:    https://github.com/downloads/vinzenz/vsqlite--/%{name}-%{version}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  premake
BuildRequires:  boost-devel
BuildRequires:  sqlite-devel
BuildRequires:  libtool
BuildRequires:  doxygen
BuildRequires:  graphviz

%description
VSQLite++ is a C++ wrapper for sqlite3 using the C++ standard library and boost.
VSQLite++ is designed to be easy to use and focuses on simplicity.

%package devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description devel
This package contains development files for %{name}.

%package doc
%if 0%{?fedora} >= 12 || 0%{?rhel} >= 6
BuildArch:      noarch
%endif
Summary:        Development documentation for %{name}
Group:          Development/Libraries

%description doc
This package contains development documentation files for %{name}.

%prep
%setup -q

%build
%configure
sed -i -e 's! -shared ! -Wl,--as-needed\0!g' libtool
make %{?_smp_mflags}
doxygen Doxyfile

%install
# devel & base
install -p -m 755 -d %{buildroot}%{_libdir}
# devel only
install -p -m 755 -d %{buildroot}%{_includedir}/sqlite
install -m 644 include/sqlite/*.hpp %{buildroot}%{_includedir}/sqlite
# docs
install -p -m 755 -d %{buildroot}%{_docdir}

# build for all
make DESTDIR=%{buildroot} install

%post -p /sbin/ldconfig 
%postun -p /sbin/ldconfig

%files doc
%defattr(-,root,root,-)
%doc ChangeLog README COPYING examples/sqlite_wrapper.cpp html/*

%files devel
%defattr(-,root,root,-)
%doc ChangeLog README COPYING
%{_libdir}/libvsqlitepp.so
%{_includedir}/sqlite
# Don't add .la/.a to the package
%exclude %{_libdir}/libvsqlitepp.la
%exclude %{_libdir}/libvsqlitepp.a

%files
%defattr(-,root,root,-)
%doc ChangeLog README COPYING 
%{_libdir}/libvsqlitepp.so.*

%changelog
* Sat Oct 20 2012 Remi Collet <RPMS@FamilleCollet.com> - 0.3.9-3
- backport for remi repo

* Fri Sep 28 2012 Vinzenz Feenstra <evilissimo@gmail.com> - 0.3.9-3
- Documentation subpackage now noarch

* Wed Sep 26 2012 Vinzenz Feenstra <evilissimo@gmail.com> - 0.3.9-2
- Removed comment with macro - Not needed anymore

* Tue Sep 25 2012 Vinzenz Feenstra <evilissimo@gmail.com> - 0.3.9-1
- Updated to upstream vsqlite++-0.3.9
- Removing now obsolete ./autogen.sh call in prep
- Remove of unnecessary BuildRequires automake and autoconf
- Upstream renamed Changelog to ChangeLog - reflected changes
- Upstream renamed LICENSE to COPYING - reflected changes

* Tue Sep 25 2012 Vinzenz Feenstra <evilissimo@gmail.com> - 0.3.7-2
- Fix for %%description spelling 'ibrary' => 'library'
- Fix for unused libm dependency
- Include Changelog, README and LICENSE to devel
- Removed TODO, VERSION
- Removed duplicated lines in the install sectin
- New doc sub package for the html documentation and code example
- Removed static package
- Removed unnecessary ldconfig call on devel package
- One BuildRequires entry per line

* Tue Sep 25 2012 Vinzenz Feenstra <evilissimo@gmail.com> - 0.3.7-1
- Initial package

