%global php_apiver	%((echo 0; php -i 2>/dev/null | sed -n 's/^PHP API => //p') | tail -1)
%{!?php_extdir:		%{expand: %%global php_extdir %(php-config --extension-dir)}}

Name:		php-facedetect
Version:	1.0.1
Release:	4%{?dist}
Summary:	PHP extension to access the OpenCV library
Group:		Development/Languages
License:	PHP
URL:		http://www.xarg.org/project/php-facedetect/
Source0:	http://www.xarg.org/download/facedetect-%{version}.tar.gz
# patch to work around DSOlinkage issues introduced in F-13
Patch1:		facedetect-dso-link-workaround.patch
# Fix code to work with opencv 2.2.0
Patch2:		facedetect-1.0.1-opencv-2.2.0.patch
# https://github.com/infusion/PHP-Facedetect/pull/5
Patch3:         facedetect-php54.patch


BuildRequires:	php-devel opencv-devel >= 2.2.0
Requires:	opencv
Requires:	php(zend-abi) = %{php_zend_api}
Requires:	php(api) = %{php_core_api}

%description
This extension provides a PHP implementation of the OpenCV library.
The extension offers two new functions. In principle, they differ
only by their return value. The first returns only the number of
faces found on the given image and the other an associative array
of their coordinates.


%prep
%setup -q -n facedetect
%patch1 -p1
%patch2 -p1
%patch3 -p1 -b .php54

%{__cat} <<'EOF' >facedetect.ini
extension=facedetect.so
EOF
sed -i 's/\r//' CREDITS

%build
phpize
%configure
make %{?_smp_mflags}

%install 
make install INSTALL_ROOT=$RPM_BUILD_ROOT INSTALL="install -p" 
install -p -D -m0644 facedetect.ini $RPM_BUILD_ROOT%{_sysconfdir}/php.d/facedetect.ini

%check
# No test provided by upstream, so
# minimal load test for the PHP extension
php -n \
    -d extension_dir=modules \
    -d extension=facedetect.so -m \
    | grep facedetect

%files
%doc CREDITS
%config(noreplace) %{_sysconfdir}/php.d/facedetect.ini
%{php_extdir}/facedetect.so

%changelog
* Wed Dec 28 2011 Remi Collet <remi@fedoraproject.org> - 1.0.1-4
- build against php 5.4
- add patch for php 5.4
- add minimal load test

* Wed Aug 31 2011 Rex Dieter <rdieter@fedoraproject.org> 1.0.1-4
- rebuild (opencv)

* Tue May 10 2011 Tom Callaway <spot@fedoraproject.org> - 1.0.1-3
- Clean up spec
- Fix code to work with OpenCV 2.2.0

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 10 2011 Andrew Colin Kissa <andrew@topdog.za.net> - 1.0.1-1
- Bump up to latest upstream
- Rebuild with new opencv

* Wed Jun 30 2010 Andrew Colin Kissa <andrew@topdog.za.net> - 1.0.0-6
- Rebuild with new opencv

* Mon Mar 04 2010 Andrew Colin Kissa <andrew@topdog.za.net> - 1.0.0-5
- Explicit requires opencv

* Mon Mar 01 2010 Andrew Colin Kissa <andrew@topdog.za.net> - 1.0.0-4
- Patch to build with new DSO linkage Change
- Rebuild with new opencv

* Sun Nov 29 2009 Andrew Colin Kissa <andrew@topdog.za.net> - 1.0.0-3
- Rebuild with new opencv

* Thu Jul 30 2009 Andrew Colin Kissa <andrew@topdog.za.net> - 1.0.0-2
- Fix macros

* Wed Jul 22 2009 Andrew Colin Kissa <andrew@topdog.za.net> - 1.0.0-1
- Initial package
