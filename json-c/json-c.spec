Name:		json-c
Version:	0.10
Release:	1%{?dist}
Summary:	A JSON implementation in C
Group:		Development/Libraries
License:	MIT
URL:		https://github.com/json-c/json-c/wiki
Source0:	https://github.com/downloads/%{name}/%{name}/%{name}-%{version}.tar.gz
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)


%description
JSON-C implements a reference counting object model that allows you to easily
construct JSON objects in C, output them as JSON formatted strings and parse
JSON formatted strings back into the C representation of JSON objects.

%package devel
Summary:	Development headers and library for json-c
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	pkgconfig

%description devel
This package contains the development headers and library for json-c.


%package doc
Summary:	Reference manual for json-c
Group:		Documentation
BuildArch:	noarch

%description doc
This package contains the reference manual for json-c.

%prep
%setup -q

for doc in ChangeLog; do
 iconv -f iso-8859-1 -t utf8 $doc > $doc.new &&
 touch -r $doc $doc.new &&
 mv $doc.new $doc
done

%build
%configure --enable-shared --disable-static
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
# Get rid of la files
rm -rf %{buildroot}%{_libdir}/*.la

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING NEWS README README.html
%{_libdir}/libjson.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/json/
%{_libdir}/libjson.so
%{_libdir}/pkgconfig/json.pc

%files doc
%defattr(-,root,root,-)
%doc doc/html/*

%changelog
* Sat Nov 24 2012 Jiri Pirko <jpirko@redhat.com> - 0.10-1
- update to 0.10
- new upstream URL

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jan 23 2012 Jiri Pirko <jpirko@redhat.com> - 0.9-4
- add json_tokener_parse_verbose, and return NULL on parser errors

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Apr 06 2010 Jussi Lehtola <jussilehtola@fedoraproject.org> - 0.9-1
- First release.
