#	The original source of this package contains a font with a forbidden
#		license.
#	The attached source tarball does not contain this font and has been
#		produced from the original by executing the following commands:
#
#	wget http://web135.srv3.sysproserver.de/milki.erphesfurt.de./captcha/captcha-%{version}.tgz
#	tar xzf captcha-%{version}.tgz
#	rm -f captcha-%{version}/MyUnderwood.*
#	tar czf captcha-%{version}.nofont.tar.gz captcha-%{version}
#
#	SHA1 sums:
#	facfe0f57adddd4e278852abd5499177f03a0c1f captcha-2.3.tgz
#	5387d2972766d5109cb4ae8572350a2229a89705 captcha-2.3.nofont.tar.gz

%if 0%{?fedora} >= 9 || 0%{?rhel} >= 6
%global fontdir		%{_datadir}/fonts/dejavu
%else
%global fontdir		%{_datadir}/fonts/freefont
%endif

Name:		php-captchaphp
Summary:	PHP very user-friendly CAPTCHA solution
Version:	2.3
Release:	1%{?dist}

#	Public Domain or any FOSS License, see README
#	We're choosing MIT because it is universally compatible with other FOSS 
#		licenses.
License:	Public Domain or MIT

Group:		System Environment/Libraries
URL:		http://freshmeat.net/projects/captchaphp/
Source0:	captcha-%{version}.nofont.tar.gz
Patch1:		captcha-2.3-24pre.patch
Requires:	php-gd >= 4.3.2
Requires:	%{fontdir}
Buildarch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root

%description
  This PHP script provides a very user-friendly CAPTCHA solution.
You can easily embed it into your <form> generation scripts to
prevent spam-bot access.

It strives to be accessible and implements an arithmetic riddle
as alternative for visually impaired users. It does not require
cookies, but makes use of "AJAX" to give users visual feedback
for solving the CAPTCHA. It grants access fuzzily (when single
letters were outguessed) instead of frustrating people. And it
can be customized rather easily.


#-------------------------------------------------------------------------------
%prep
#-------------------------------------------------------------------------------

%setup -q -n captcha-%{version}
%patch1 -p 1


#-------------------------------------------------------------------------------
%build
#-------------------------------------------------------------------------------

#	Replace the font path by our (arbitrary) default font directory.

sed -i -e "/CAPTCHA_FONT_DIR/s#,.*#, '%{fontdir}/');#" captcha.php


#-------------------------------------------------------------------------------
%install
#-------------------------------------------------------------------------------

rm -rf "${RPM_BUILD_ROOT}"

#	Install directory.

install -p -d -m 755 "${RPM_BUILD_ROOT}/%{_datadir}/php/captchaphp/"


#	Install file.

install -p -m 644 captcha.php "${RPM_BUILD_ROOT}/%{_datadir}/php/captchaphp/"


#-------------------------------------------------------------------------------
%clean
#-------------------------------------------------------------------------------

rm -rf "${RPM_BUILD_ROOT}"


#-------------------------------------------------------------------------------
%files
#-------------------------------------------------------------------------------

%defattr(-, root, root, -)
%doc README index.php
%{_datadir}/php/captchaphp


#-------------------------------------------------------------------------------
%changelog
#-------------------------------------------------------------------------------

* Sat Jul 17 2011 Remi Collet <RPMS@FamilleCollet.com> - 2.3-1
- rebuild for remi repository

* Tue May  3 2011 Patrick Monnerat <pm@datasphere.ch> 2.3-1
- New upstream release.
- Patch "24pre" to apply pre 2.4 updates.

* Wed Mar  9 2011 Remi Collet <RPMS@FamilleCollet.com> - 2.2-2.1
- switch to freefont for EPEL <= 5

* Mon Jul  5 2010 Remi Collet <RPMS@FamilleCollet.com> - 2.2-2
- rebuild for remi repository

* Mon Jun 14 2010 Patrick Monnerat <pm@datasphere.ch> 2.2-2
- Using MIT license.

* Tue May 25 2010 Patrick Monnerat <pm@datasphere.ch> 2.2-1
- New upstream release.

* Mon Jul 13 2009 Patrick Monnerat <pm@datasphere.ch> 2.0-3
- Depends on font directory rather than font package: this circumvents the
  font package name change done between F10 and F11.

* Tue Jun 23 2009 Patrick Monnerat <pm@datasphere.ch> 2.0-2
- Move class files to a package-specific sub-directory.
- Get rid of build dependence on "ed".

* Mon Jun  8 2009 Patrick Monnerat <pm@datasphere.ch> 2.0-1
- Initial RPM spec file.
- Patch "nodeferror" to allow predefining CAPTCHA_* constants without
  issuing an error at include time.
- Patch "https" to detect SSL use automatically.
- Patch "undef" to fix an undefined index error.
- Patch "directcall" to improve direct call detection.
- Patch "translatable" to make module translatable through the use of
  additional CAPTCHA_* defines for texts.
- Font included in original package has an incompatible license: thus it
  is not packaged. Instead, we use a reasonable default ttf font package and
  directory.
