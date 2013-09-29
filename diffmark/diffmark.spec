Name:       diffmark
Version:    0.10
Release:    1%{?dist}
Summary:    XML diff and merge
Group:      Applications/Text
# The library code has it's own license
# Parts of lib/lcs.hh is from Perl Algorithm::Diff module (GPL+ or Artistic)
# The build scripts are GPLv2+
License:    diffmark and GPLv2+ and (GPL+ or Artistic)
URL:        http://www.mangrove.cz/%{name}/
Source0:    %{url}%{name}-%{version}.tar.gz
# Superfluous RPATH in programs
Patch0:     %{name}-0.09-remove_rpath.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  libxml2-devel
# Because of diffmark-0.08-remove_rpath.patch:
# And to update config.sub to support aarch64, bug #925255:
BuildRequires: autoconf, automake, libtool

%description
This is a XML diff and merge package. It consists of a shared library and
two utilities: dm and dm-merge. 

%package        devel
Summary:        Development files for %{name} library
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
Header files and libraries for developing applications that use %{name}.

%prep
%setup -q
%patch0 -p1 -b .rpath
# automake -i -f to support aarch64, bug #925255
libtoolize --force && autoreconf -i -f

%build
%configure --disable-static
make %{?_smp_mflags}

%install
make install "DESTDIR=$RPM_BUILD_ROOT"
find "$RPM_BUILD_ROOT" -name '*.la' -exec rm -f {} +

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc COPYING doc/*.html README 
%{_bindir}/*
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/*
%{_libdir}/*.so

%changelog
* Sun Sep 29 2013 Remi Collet <remi@fedoraproject.org> - 0.10-1
- rebuild for remi repo

* Wed Mar 27 2013 Petr Pisar <ppisar@redhat.com> - 0.10-5
- Update config.sub to support aarch64 (bug #925255)

* Mon Nov 21 2011 Petr Pisar <ppisar@redhat.com> - 0.10-1
- 0.10 bump

* Tue Nov 15 2011 Petr Pisar <ppisar@redhat.com> - 0.09-1
- 0.09 bump

* Thu Oct 27 2011 Petr Pisar <ppisar@redhat.com> - 0.08-1
- Version 0.08 packaged


