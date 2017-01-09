# remirepo/Fedora spec file for php-tcpdf
#
# Copyright (c) 2013-2017 Remi Collet, Johan Cwiklinski
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
# see https://github.com/tecnickcom/TCPDF/releases
%global gh_commit    009f2304c3a9c8152b89a5321a8825f250911dc3
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     tecnickcom
%global gh_project   TCPDF
%global real_name    tcpdf

Name:           php-tcpdf
Summary:        PHP class for generating PDF documents and barcodes
Version:        6.2.13
Release:        1%{?dist}

URL:            http://www.tcpdf.org
License:        LGPLv3+
Group:          Development/Libraries

Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}-%{?gh_short}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php-cli
BuildRequires:  php-fedora-autoloader-devel

Requires:       php(language) >= 5.3
# From phpcompatinfo report form version 6.2.10
Requires:       php-bcmath
Requires:       php-curl
Requires:       php-date
Requires:       php-gd
Requires:       php-hash
Requires:       php-json
Requires:       php-mbstring
Requires:       php-openssl
Requires:       php-pcre
Requires:       php-posix
Requires:       php-tidy
Requires:       php-xml
Requires:       php-zlib
# imagick is optionnal (and conflicts with gmagick)
# Autoloader
Requires:       php-composer(fedora/autoloader)

# Old name for compatibility
Provides:       php-composer(tecnick.com/tcpdf) = %{version}
# New name
Provides:       php-composer(tecnickcom/tcpdf)  = %{version}


%description
PHP class for generating PDF documents.

* no external libraries are required for the basic functions;
* all standard page formats, custom page formats, custom margins and units
  of measure;
* UTF-8 Unicode and Right-To-Left languages;
* TrueTypeUnicode, OpenTypeUnicode, TrueType, OpenType, Type1 and CID-0 fonts;
* font subsetting;
* methods to publish some XHTML + CSS code, Javascript and Forms;
* images, graphic (geometric figures) and transformation methods;
* supports JPEG, PNG and SVG images natively, all images supported by GD
  (GD, GD2, GD2PART, GIF, JPEG, PNG, BMP, XBM, XPM) and all images supported
  via ImagMagick (http: www.imagemagick.org/www/formats.html)
* 1D and 2D barcodes: CODE 39, ANSI MH10.8M-1983, USD-3, 3 of 9, CODE 93,
  USS-93, Standard 2 of 5, Interleaved 2 of 5, CODE 128 A/B/C, 2 and 5 Digits
  UPC-Based Extention, EAN 8, EAN 13, UPC-A, UPC-E, MSI, POSTNET, PLANET,
  RMS4CC (Royal Mail 4-state Customer Code), CBC (Customer Bar Code),
  KIX (Klant index - Customer index), Intelligent Mail Barcode, Onecode,
  USPS-B-3200, CODABAR, CODE 11, PHARMACODE, PHARMACODE TWO-TRACKS,
  Datamatrix ECC200, QR-Code, PDF417;
* ICC Color Profiles, Grayscale, RGB, CMYK, Spot Colors and Transparencies;
* automatic page header and footer management;
* document encryption up to 256 bit and digital signature certifications;
* transactions to UNDO commands;
* PDF annotations, including links, text and file attachments;
* text rendering modes (fill, stroke and clipping);
* multiple columns mode;
* no-write page regions;
* bookmarks and table of content;
* text hyphenation;
* text stretching and spacing (tracking/kerning);
* automatic page break, line break and text alignments including justification;
* automatic page numbering and page groups;
* move and delete pages;
* page compression (requires php-zlib extension);
* XOBject templates;
* PDF/A-1b (ISO 19005-1:2005) support.

By default, TCPDF uses the GD library which is know as slower than ImageMagick
solution. You can optionally install php-pecl-imagick; TCPDF will use it.


%package dejavu-lgc-sans-fonts
Summary:        DejaVu LGC sans-serif fonts for tcpdf
Group:          Development/Libraries
BuildRequires:  dejavu-lgc-sans-fonts
Requires:       %{name} = %{version}-%{release}
Requires:       dejavu-lgc-sans-fonts

%description dejavu-lgc-sans-fonts
This package allow to use system DejaVu LGC sans-serif variable-width
font faces in TCPDF.

%package dejavu-lgc-sans-mono-fonts
Summary:        DejaVu LGC mono-spaced fonts for tcpdf
Group:          Development/Libraries
BuildRequires:  dejavu-lgc-sans-mono-fonts
Requires:       %{name} = %{version}-%{release}
Requires:       dejavu-lgc-sans-mono-fonts

%description dejavu-lgc-sans-mono-fonts
This package allow to use system DejaVu LGC sans-serif mono-spaced
font faces in TCPDF.

%package dejavu-lgc-serif-fonts
Summary:        DejaVu LGC serif fonts for tcpdf
Group:          Development/Libraries
BuildRequires:  dejavu-lgc-serif-fonts
Requires:       %{name} = %{version}-%{release}
Requires:       dejavu-lgc-serif-fonts

%description dejavu-lgc-serif-fonts
This package allow to use system DejaVu LGC serif variable-width
font faces in TCPDF.

%package dejavu-sans-fonts
Summary:        DejaVu sans-serif fonts for tcpdf
Group:          Development/Libraries
BuildRequires:  dejavu-sans-fonts
Requires:       %{name} = %{version}-%{release}
Requires:       dejavu-sans-fonts
# previous metapackage
Obsoletes:      php-tcpdf-dejavu-fonts < 6.0.051
Provides:       php-tcpdf-dejavu-fonts = %{version}-%{release}

%description dejavu-sans-fonts
This package allow to use system DejaVu sans-serif variable-width
font faces in TCPDF.

%package dejavu-sans-mono-fonts
Summary:        DejaVu mono-spaced fonts for tcpdf
Group:          Development/Libraries
BuildRequires:  dejavu-sans-mono-fonts
Requires:       %{name} = %{version}-%{release}
Requires:       dejavu-sans-mono-fonts

%description dejavu-sans-mono-fonts
This package allow to use system DejaVu sans-serif mono-spaced
font faces in TCPDF.

%package dejavu-serif-fonts
Summary:        DejaVu serif fonts for tcpdf
Group:          Development/Libraries
BuildRequires:  dejavu-serif-fonts
Requires:       %{name} = %{version}-%{release}
Requires:       dejavu-serif-fonts

%description dejavu-serif-fonts
This package allow to use system DejaVu serif variable-width
font faces in TCPDF.

%package gnu-free-mono-fonts
Summary:        GNU FreeFonts mono-spaced for tcpdf
Group:          Development/Libraries
%if 0%{?fedora} >= 11 || 0%{?rhel} >= 6
BuildRequires:  gnu-free-mono-fonts
Requires:       gnu-free-mono-fonts
%else
BuildRequires:  freefont
Requires:       freefont
%endif
Requires:       %{name} = %{version}-%{release}

%description gnu-free-mono-fonts
This package allow to use system GNU FreeFonts mono-spaced font faces in TCPDF.

%package gnu-free-sans-fonts
Summary:        GNU FreeFonts sans-serif for tcpdf
Group:          Development/Libraries
%if 0%{?fedora} >= 11 || 0%{?rhel} >= 6
BuildRequires:  gnu-free-sans-fonts
Requires:       gnu-free-sans-fonts
%else
BuildRequires:  freefont
Requires:       freefont
%endif
Requires:       %{name} = %{version}-%{release}
# previous metapackage
Obsoletes:      php-tcpdf-gnu-free-fonts < 6.0.051
Provides:       php-tcpdf-gnu-free-fonts = %{version}-%{release}

%description gnu-free-sans-fonts
This package allow to use system GNU FreeFont sans-serif font faces in TCPDF.

%package gnu-free-serif-fonts
Summary:        GNU FreeFonts serif for tcpdf
Group:          Development/Libraries
%if 0%{?fedora} >= 11 || 0%{?rhel} >= 6
BuildRequires:  gnu-free-serif-fonts
Requires:       gnu-free-serif-fonts
%else
BuildRequires:  freefont
Requires:       freefont
%endif
Requires:       %{name} = %{version}-%{release}

%description gnu-free-serif-fonts
This package allow to use system GNU FreeFont serif font faces in TCPDF.


%prep
%setup -q -n %{gh_project}-%{gh_commit}

: remove bundled fonts
rm -rf fonts/dejavu-fonts-ttf* fonts/freefont-* fonts/ae_fonts_*
for fic in fonts/*.z
do
  rm -f $fic ${fic/.z/.php}
done
ls fonts | sed -e 's|^|%{_datadir}/php/%{real_name}/fonts/|' >corefonts.lst


%build
: empty build section, nothing required


%install
rm -rf %{buildroot}
: Library
install -d     %{buildroot}%{_datadir}/php/%{real_name}
cp -a *.php    %{buildroot}%{_datadir}/php/%{real_name}/
cp -a include  %{buildroot}%{_datadir}/php/%{real_name}/
cp -a fonts    %{buildroot}%{_datadir}/php/%{real_name}/
install -d     %{buildroot}%{_datadir}/php/%{real_name}/images
install -m 0644 examples/images/_blank.png \
               %{buildroot}%{_datadir}/php/%{real_name}/images/

: Autoloader
php -d memory_limit=2G\
  %{_bindir}/phpab \
    --template fedora \
    --output %{buildroot}%{_datadir}/php/%{real_name}/autoload.php \
    %{buildroot}%{_datadir}/php/%{real_name}

: Configuration
install -d     %{buildroot}%{_sysconfdir}/%{name}
install -m 0644 config/*.php \
               %{buildroot}%{_sysconfdir}/%{name}

: Tools
install -d %{buildroot}%{_bindir}
install -m 0755 tools/%{real_name}_addfont.php \
           %{buildroot}%{_bindir}/%{real_name}_addfont

# Fonts
list=""
for ttf in \
    /usr/share/fonts/dejavu/*ttf \
%if 0%{?fedora} >= 11 || 0%{?rhel} >= 6
    /usr/share/fonts/gnu-free/*ttf \
%else
    /usr/share/fonts/freefont/*ttf \
%endif
; do
   list=$ttf${list:+,${list}}
done
php tools/tcpdf_addfont.php \
    --addcbbox \
    --flags 32 \
    --fonts $list \
    --link \
    --outpath %{buildroot}%{_datadir}/php/%{real_name}/fonts/


%check
php -r 'require "%{buildroot}%{_datadir}/php/%{real_name}/autoload.php";
  printf("%{name} version %s\n", $ver=TCPDF_STATIC::getTCPDFVersion());
  exit ($ver === "%{version}" ? 0 : 1);
'


%clean
rm -rf %{buildroot}


%files -f corefonts.lst
%defattr(-,root,root,-)
%doc README.md CHANGELOG.TXT examples
%doc composer.json
%{!?_licensedir:%global license %%doc}
%license LICENSE.TXT
%{_bindir}/%{real_name}_addfont
%dir %{_datadir}/php/%{real_name}
%dir %{_datadir}/php/%{real_name}/fonts
%{_datadir}/php/%{real_name}/include
%{_datadir}/php/%{real_name}/images
%{_datadir}/php/%{real_name}/*php
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/*

%files dejavu-lgc-sans-fonts
%defattr(-,root,root,-)
%{_datadir}/php/%{real_name}/fonts/dejavulgcsans*
%exclude %{_datadir}/php/%{real_name}/fonts/dejavulgcsansmono*

%files dejavu-lgc-sans-mono-fonts
%defattr(-,root,root,-)
%{_datadir}/php/%{real_name}/fonts/dejavulgcsansmono*

%files dejavu-lgc-serif-fonts
%defattr(-,root,root,-)
%{_datadir}/php/%{real_name}/fonts/dejavulgcserif*

%files dejavu-sans-fonts
%defattr(-,root,root,-)
%{_datadir}/php/%{real_name}/fonts/dejavusans*
%exclude %{_datadir}/php/%{real_name}/fonts/dejavusansmono*

%files dejavu-sans-mono-fonts
%defattr(-,root,root,-)
%{_datadir}/php/%{real_name}/fonts/dejavusansmono*

%files dejavu-serif-fonts
%defattr(-,root,root,-)
%{_datadir}/php/%{real_name}/fonts/dejavuserif*

%files gnu-free-mono-fonts
%defattr(-,root,root,-)
%{_datadir}/php/%{real_name}/fonts/freemono*

%files gnu-free-sans-fonts
%defattr(-,root,root,-)
%{_datadir}/php/%{real_name}/fonts/freesans*

%files gnu-free-serif-fonts
%defattr(-,root,root,-)
%{_datadir}/php/%{real_name}/fonts/freeserif*


%changelog
* Mon Jan  9 2017 Remi Collet <remi@fedoraproject.org> - 6.2.13-1
- update to 6.2.13
- add classmap autoloader using fedora/autoloader

* Sun Sep 13 2015 Remi Collet <remi@fedoraproject.org> - 6.2.12-1
- update to 6.2.12
- provide php-composer(tecnickcom/tcpdf)

* Mon Aug  3 2015 Remi Collet <remi@fedoraproject.org> - 6.2.11-1
- update to 6.2.11

* Wed Jul 29 2015 Remi Collet <remi@fedoraproject.org> - 6.2.10-1
- update to 6.2.10
- sources from github (instead of sourceforge)
- drop dependency on php-mcrypt

* Sat Jun 27 2015 Remi Collet <remi@fedoraproject.org> - 6.2.9-1
- update to 6.2.9

* Thu Apr 30 2015 Remi Collet <remi@fedoraproject.org> - 6.2.8-1
- update to 6.2.8

* Wed Apr 29 2015 Remi Collet <remi@fedoraproject.org> - 6.2.7-1
- update to 6.2.7

* Thu Jan 29 2015 Remi Collet <remi@fedoraproject.org> - 6.2.6-1
- update to 6.2.6

* Tue Jan 13 2015 Remi Collet <remi@fedoraproject.org> - 6.2.4-1
- update to 6.2.4

* Wed Dec 10 2014 Remi Collet <remi@fedoraproject.org> - 6.1.1-1
- update to 6.1.1

* Thu Nov 27 2014 Remi Collet <remi@fedoraproject.org> - 6.0.099-1
- update to 6.0.099

* Mon Nov 10 2014 Remi Collet <remi@fedoraproject.org> - 6.0.098-1
- update to 6.0.098

* Tue Oct 21 2014 Remi Collet <remi@fedoraproject.org> - 6.0.097-1
- update to 6.0.097

* Sun Oct  5 2014 Remi Collet <remi@fedoraproject.org> - 6.0.095-1
- update to 6.0.095

* Thu Oct  2 2014 Remi Collet <remi@fedoraproject.org> - 6.0.094-1
- update to 6.0.094

* Fri Sep  5 2014 Remi Collet <remi@fedoraproject.org> - 6.0.093-1
- update to 6.0.093

* Fri Aug 15 2014 Remi Collet <remi@fedoraproject.org> - 6.0.091-1
- update to 6.0.091
- provide php-composer(tecnick.com/tcpdf)

* Thu Jul 17 2014 Remi Collet <remi@fedoraproject.org> - 6.0.089-1
- update to 6.0.089

* Mon Jun 23 2014 Remi Collet <remi@fedoraproject.org> - 6.0.086-1
- update to 6.0.086

* Tue May 27 2014 Remi Collet <remi@fedoraproject.org> - 6.0.082-1
- update to 6.0.082
- include cbbox metrics in fonts metadata

* Sat May 10 2014 Remi Collet <remi@fedoraproject.org> - 6.0.077-1
- update to 6.0.077

* Mon Apr 28 2014 Remi Collet <remi@fedoraproject.org> - 6.0.072-1
- update to 6.0.072

* Tue Apr  8 2014 Remi Collet <remi@fedoraproject.org> - 6.0.064-1
- update to 6.0.064

* Sun Apr  6 2014 Remi Collet <remi@fedoraproject.org> - 6.0.063-1
- update to 6.0.063

* Thu Feb 20 2014 Remi Collet <remi@fedoraproject.org> - 6.0.061-1
- update to 6.0.061

* Tue Feb  4 2014 Remi Collet <remi@fedoraproject.org> - 6.0.059-1
- update to 6.0.059

* Tue Jan 28 2014 Remi Collet <remi@fedoraproject.org> - 6.0.057-1
- update to 6.0.057

* Tue Jan 21 2014 Remi Collet <remi@fedoraproject.org> - 6.0.055-1
- update to 6.0.055

* Sun Jan  5 2014 Remi Collet <remi@fedoraproject.org> - 6.0.053-1
- update to 6.0.053

* Sat Dec  7 2013 Remi Collet <remi@fedoraproject.org> - 6.0.051-1
- update to 6.0.051
- drop the dejavu-fonts and gnu-free-fonts metapackage

* Thu Nov 28 2013 Remi Collet <remi@fedoraproject.org> - 6.0.049-1
- update to 6.0.049
- fix but with same PNG image included twice, #1035392

* Thu Nov 21 2013 Remi Collet <remi@fedoraproject.org> - 6.0.047-1
- update to 6.0.047

* Mon Nov 11 2013 Remi Collet <remi@fedoraproject.org> - 6.0.044-1
- update to 6.0.044

* Sun Oct 27 2013 Remi Collet <remi@fedoraproject.org> - 6.0.042-1
- update to 6.0.042

* Wed Oct 16 2013 Remi Collet <remi@fedoraproject.org> - 6.0.039-1
- update to 6.0.039

* Mon Oct  7 2013 Remi Collet <remi@fedoraproject.org> - 6.0.038-1
- update to 6.0.038

* Tue Oct  1 2013 Remi Collet <remi@fedoraproject.org> - 6.0.037-1
- update to 6.0.037

* Sat Sep 28 2013 Remi Collet <remi@fedoraproject.org> - 6.0.035-1
- update to 6.0.035

* Tue Sep 24 2013 Remi Collet <remi@fedoraproject.org> - 6.0.033-1
- update to 6.0.033

* Thu Sep 19 2013 Remi Collet <remi@fedoraproject.org> - 6.0.031-1
- update to 6.0.031

* Fri Sep 13 2013 Remi Collet <remi@fedoraproject.org> - 6.0.025-1
- update to 6.0.025

* Mon Sep  2 2013 Johan Cwiklinski <johan AT x-tnd DOT be> - 6.0.024-1
- update to 6.0.024

* Tue Aug  6 2013 Remi Collet <remi@fedoraproject.org> - 6.0.023-1
- update to 6.0.023

* Wed Jun 19 2013 Remi Collet <remi@fedoraproject.org> - 6.0.020-1
- update to 6.0.020

* Sat Jun  1 2013 Remi Collet <remi@fedoraproject.org> - 6.0.018-1
- update to 6.0.018
- barcode examples now works out of the box

* Sat May 18 2013 Remi Collet <remi@fedoraproject.org> - 6.0.017-2
- split fonts, 1 subpackage per font package

* Sat May 18 2013 Remi Collet <remi@fedoraproject.org> - 6.0.017-1
- update to 6.0.017

* Thu May 16 2013 Remi Collet <remi@fedoraproject.org> - 6.0.016-1
- update to 6.0.016
- add /usr/share/php/tcpdf/images dir

* Wed May 15 2013 Remi Collet <remi@fedoraproject.org> - 6.0.015-1
- update to 6.0.015
- clean spec (upstream changes for packaging)
- drop .php suffix from tools

* Tue May 14 2013 Remi Collet <remi@fedoraproject.org> - 6.0.014-1
- update to 6.0.014
- drop patch merged upstream

* Mon May 13 2013 Remi Collet <remi@fedoraproject.org> - 6.0.013-2
- split fonts in sub-packages

* Mon May 13 2013 Remi Collet <remi@fedoraproject.org> - 6.0.013-1
- update to 6.0.013
- use available system TTF fonts

* Sun May 12 2013 Johan Cwiklinski <johan AT x-tnd DOT be> - 6.0.012-3
- Fix README.cache file permissions

* Fri May 10 2013 Remi Collet <remi@fedoraproject.org> - 6.0.012-2
- improve cache ownership, on folder per web server
- drop bundled fonts

* Thu May 09 2013 Johan Cwiklinski <johan AT x-tnd DOT be> - 6.0.012-1
- Initial packaging
