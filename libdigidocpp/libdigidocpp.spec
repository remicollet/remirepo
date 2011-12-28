%global build_perl_module   1
%global build_php_module    1
%global build_python_module 1

%global php_apiver  %((echo 0; php -i 2>/dev/null | sed -n 's/^PHP API => //p') | tail -1)
%{!?php_extdir: %{expand: %%global php_extdir %(php-config --extension-dir)}}

%if ! (0%{?fedora} > 12 || 0%{?rhel} > 5)
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%endif

Name:           libdigidocpp
Version:        0.3.0
Release:        9%{?dist}
Summary:        Library for creating and validating BDoc and DDoc containers

Group:          System Environment/Libraries
License:        LGPLv2+
URL:            http://code.google.com/p/esteid/
Source0:        http://esteid.googlecode.com/files/%{name}-%{version}.tar.bz2

BuildRequires:  cmake
BuildRequires:  libdigidoc-devel
BuildRequires:  libp11-devel
BuildRequires:  minizip-devel
BuildRequires:  openssl-devel
BuildRequires:  xml-security-c-devel
BuildRequires:  xsd

# Handle bindings
%if 0%{?build_perl_module}%{?build_php_module}%{?build_python_module}
BuildRequires:  swig
%endif
%if 0%{?build_perl_module}
BuildRequires:  perl-devel
%endif
%if 0%{?build_php_module}
BuildRequires:  php-devel
%endif
%if 0%{?build_python_module}
BuildRequires:  python2-devel
%endif

# Dynamically loaded libraries
Requires:       libdigidoc%{?_isa}
Requires:       opensc%{?_isa}

%description
libdigidocpp is a C++ library for reading, validating, and creating BDoc and
DDoc containers. These file formats are widespread in Estonia where they are
used for storing legally binding digital signatures.


%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       libdigidoc-devel
Requires:       libp11-devel
Requires:       openssl-devel
Requires:       xml-security-c-devel
Requires:       xsd

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%if 0%{?build_perl_module}
%package -n     perl-digidoc
Summary:        Perl bindings for %{name}
Group:          Development/Languages
Requires:       %{name} = %{version}-%{release}
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Obsoletes:      %{name}-perl < 0.3.0-1
Provides:       %{name}-perl = %{version}-%{release}

%{?perl_default_filter}

%description -n perl-digidoc
The perl-digidoc package contains Perl bindings for the %{name} library.
%endif


%if 0%{?build_php_module}
%package -n     php-digidoc
Summary:        PHP bindings for %{name}
Group:          Development/Languages
Requires:       %{name} = %{version}-%{release}
Requires:       php(zend-abi) = %{php_zend_api}
Requires:       php(api) = %{php_core_api}
Obsoletes:      %{name}-php < 0.3.0-1
Provides:       %{name}-php = %{version}-%{release}

# Don't want provides for php shared objects
%{?filter_provides_in: %filter_provides_in %{php_extdir}/.*\.so$}
%{?filter_setup}

%description -n php-digidoc
The php-digidoc package contains PHP bindings for the %{name} library.
%endif


%if 0%{?build_python_module}
%package -n     python-digidoc
Summary:        Python bindings for %{name}
Group:          Development/Languages
Requires:       %{name} = %{version}-%{release}
Obsoletes:      %{name}-python < 0.3.0-1
Provides:       %{name}-python = %{version}-%{release}

# Don't want provides for python shared objects
%{?filter_provides_in: %filter_provides_in %{python_sitearch}/.*\.so$}
%{?filter_setup}

%description -n python-digidoc
The python-digidoc package contains Python bindings for the %{name}
library.
%endif


%prep
%setup -q

# Remove bundled copy of minizip
rm -rf src/minizip/


%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake} ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
make install DESTDIR=$RPM_BUILD_ROOT -C %{_target_platform}


%check
# Minimal load test for the PHP extension
php -n \
    -d extension_dir=%{_target_platform}/src/php \
    -d extension=digidoc.so -m \
    | grep digidoc


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%doc AUTHORS COPYING NEWS README
%{_libdir}/*.so.*
%dir %{_sysconfdir}/digidocpp
%config(noreplace) %{_sysconfdir}/digidocpp/digidocpp.conf
%{_sysconfdir}/digidocpp/certs/
%{_sysconfdir}/digidocpp/schema/

%files devel
%{_includedir}/digidocpp/
%{_libdir}/pkgconfig/lib*.pc
%{_libdir}/*.so

%if 0%{?build_perl_module}
%files -n perl-digidoc
%{perl_vendorarch}/*
%{perl_vendorlib}/*
%endif

%if 0%{?build_php_module}
%files -n php-digidoc
%{php_extdir}/*
%{_datadir}/php/*
%{_sysconfdir}/php.d/digidoc.ini
%endif

%if 0%{?build_python_module}
%files -n python-digidoc
%{python_sitearch}/*
%endif


%changelog
* Wed Dec 28 2011 Remi Collet <remi@fedoraproject.org> - 0.3.0-9
- build against php 5.4

* Mon Jun 20 2011 Petr Sabata <contyk@redhat.com> - 0.3.0-9
- Perl mass rebuild
- Removing now obsolete Buildroot and defattr

* Fri Apr 15 2011 Kalev Lember <kalev@smartlink.ee> - 0.3.0-8
- Rebuilt for lib11 0.2.8 soname bump

* Wed Mar 16 2011 Antti Andreimann <Antti.Andreimann@mail.ee> 0.3.0-7
- Rebuilt with xml-security-c 1.6.0

* Thu Mar 10 2011 Kalev Lember <kalev@smartlink.ee> - 0.3.0-6
- Cleaned up php conditionals not needed in current Fedora releases

* Thu Mar 10 2011 Kalev Lember <kalev@smartlink.ee> - 0.3.0-5
- Rebuilt with xerces-c 3.1

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Oct 20 2010 Kalev Lember <kalev@smartlink.ee> - 0.3.0-3
- Updated descriptions for bindings subpackages, thanks to Sander Lepik.

* Tue Oct 12 2010 Kalev Lember <kalev@smartlink.ee> - 0.3.0-2
- Remove bundled minizip in prep

* Mon Oct 11 2010 Kalev Lember <kalev@smartlink.ee> - 0.3.0-1
- Update to 0.3.0
- Renamed binding subpackages to use <language>-digidoc naming scheme
- Filter shared object provides in private directories
- Added missing defattr lines
- Marked digidocpp.conf as noreplace

* Thu Jul 01 2010 Antti Andreimann <Antti.Andreimann@mail.ee> - 0.2.0-0.7.svn2811
- Added language bindings for Python, Perl and PHP

* Mon Mar 29 2010 Kalev Lember <kalev@smartlink.ee> - 0.2.0-0.6.svn2681
- Spec file clean up
- Updated summary
- Removed BR: pkcs11-helper-devel
- Removed libdigidoc++ obsoletes/provides
- Removed R: pkgconfig which is now automatically picked up by rpm
- Added AUTHORS and COPYING docs
- Cleaned up nightly build changelog entries

* Sat Feb 13 2010 Kalev Lember <kalev@smartlink.ee> - 0.2.0-0.4.svn2528
- rebuilt with new xerces-c 3.0 (F13)

* Thu Jan 21 2010 Kalev Lember <kalev@smartlink.ee> - 0.2.0-0.2.svn2454
- rebuilt with new libp11

* Sun Jun 14 2009 Kalev Lember <kalev@smartlink.ee> - 0.0.12-0.1.svn712
- Initial RPM release.
