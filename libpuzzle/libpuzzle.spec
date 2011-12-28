%global php_apiver	%((echo 0; php -i 2>/dev/null | sed -n 's/^PHP API => //p') | tail -1)
%{!?php_extdir:		%{expand: %%global php_extdir %(php-config --extension-dir)}}

Name:		libpuzzle
Version:	0.11
Release:	9%{?dist}
Summary:	Library to quickly find visually similar images (gif, png, jpg) 
Group:		System Environment/Libraries
License:	BSD
URL:		http://libpuzzle.pureftpd.org/project/libpuzzle
Source0:	http://download.pureftpd.org/pub/pure-ftpd/misc/libpuzzle/releases/%{name}-%{version}.tar.bz2
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	gd-devel

%description
The Puzzle library is designed to quickly find visually similar images
(gif, png, jpg), even if they have been resized, recompressed,
recolored or slightly modified. The library is free, lightweight yet
very fast, configurable, easy to use and it has been designed with
security in mind.

%package -n     php-%{name}
Summary:	PHP extension for %{name}
Group:		Development/Libraries
BuildRequires:	php-devel
Requires:	%{name} = %{version}-%{release}
Requires:       php(zend-abi) = %{php_zend_api}
Requires:       php(api) = %{php_core_api}

%description -n    php-%{name}
The %{name} native PHP extension for developing PHP applications that
use %{name}.

%package        devel
Summary:	Development files for %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q


%build
%{__cat} <<'EOF' >libpuzzle.ini
extension=libpuzzle.so
EOF

%configure --disable-static
%{__sed} -i.rpath -e 's|^\(hardcode_libdir_flag_spec=\).*|\1""|' libtool
%{__sed} -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
%{__make} %{?_smp_mflags}
%{__make} DESTDIR=%{_builddir}/%{name}-%{version} install INSTALL="install -p"

%{__cp} -ra php php-plain
iconv -f iso8859-1 -t utf-8 php-plain/examples/similar/similar.php > similar.php && mv -f similar.php php-plain/examples/similar/similar.php
cd php/libpuzzle
phpize

%ifarch x86_64 ppc64 sparc64 s390x
LDFLAGS="$LDFLAGS -L%{_builddir}/%{name}-%{version}/usr/lib64"; export LDFLAGS
%endif

%{__sed} -i.rpath -e 's|\$ld_runpath_switch\$ai_p||g' configure
%configure --with-libpuzzle=%{_builddir}/%{name}-%{version}/usr
%{__sed} -i.rpath -e 's|^\(hardcode_libdir_flag_spec=\).*|\1""|' libtool
%{__sed} -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
%{__make} %{?_smp_mflags}

cd -
%{__cp} php/libpuzzle/modules/%{name}.so php_%name.so
%{__rm} -rf php
%{__mv} php-plain php

%install
%{__rm} -rf %{buildroot}
%{__install} -p -D -m0755 php_%{name}.so %{buildroot}/%{php_extdir}/%{name}.so
%{__make} install DESTDIR=%{buildroot} INSTALL="install -p"
find %{buildroot} -name '*.la' -exec rm -f {} ';'
%{__mkdir_p} %{buildroot}%{_sysconfdir}/php.d
%{__install} -p -m0644 libpuzzle.ini %{buildroot}%{_sysconfdir}/php.d/libpuzzle.ini

%clean
%{__rm} -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING README THANKS
%{_libdir}/*.so.*
%{_mandir}/man8/*
%{_bindir}/*

%files -n php-%{name}
%defattr(-,root,root,-)
%doc README-PHP php/libpuzzle/{README,CREDITS,LICENSE} php/examples/similar/*.{sql,php}
%config(noreplace) %{_sysconfdir}/php.d/%{name}.ini
%{php_extdir}/%{name}.so

%files devel
%defattr(-,root,root,-)
%{_libdir}/*.so
%{_includedir}/*
%{_mandir}/man3/*

%changelog
* Fri Jul 15 2011 Andrew Colin Kissa <andrew@topdog.za.net> - 0.11-9
- Fix bugzilla #716003

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Aug 07 2009 Dennis Gilmore <dennis@ausil.us> - 0.11-7
- add sparc64 and s390x to the list of arches that use lib64

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jul 13 2009 Remi Collet <Fedora@FamilleCollet.com> - 0.11-5
- rebuild for new PHP 5.3.0 ABI (20090626)
- add PHP ABI check

* Sun Jun 21 2009 Andrew Colin Kissa <andrew@topdog.za.net> - 0.11-4
- Consistent use of macros

* Sun Jun 21 2009 Andrew Colin Kissa <andrew@topdog.za.net> - 0.11-3
- Fixes to issues raised by reviewer

* Thu Jun 18 2009 Andrew Colin Kissa <andrew@topdog.za.net> - 0.11-2
- Fix rpmlint issues

* Sun May 14 2009 Andrew Colin Kissa <andrew@topdog.za.net> - 0.11-1
- Initial release

