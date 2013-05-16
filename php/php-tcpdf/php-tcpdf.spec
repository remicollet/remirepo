%global dl_version 6_0_016
%global real_name  tcpdf

Name:           php-tcpdf
Summary:        PHP class for generating PDF documents
Version:        6.0.016
Release:        1%{?dist}

URL:            http://www.tcpdf.org
License:        LGPLv3+
Group:          Development/Libraries

Source0:        http://downloads.sourceforge.net/%{real_name}/%{real_name}_%{dl_version}.zip

# Fix path for packaging (not upstreamable)
Patch0:         tcpdf-vendor.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php-cli
BuildRequires:  php-posix

Requires:       php(language) >= 5.2
Requires:       php-openssl
#imagick is optionnal (and conflicts with gmagick)
#Requires:       php-pecl(imagick)
Requires:       php-spl
Requires:       php-bcmath
Requires:       php-curl
Requires:       php-date
Requires:       php-gd
Requires:       php-hash
Requires:       php-mbstring
Requires:       php-mcrypt
Requires:       php-pcre
Requires:       php-posix
Requires:       php-tidy
Requires:       php-xml


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


%package dejavu-fonts
Summary:        DejaVu fonts for tcpdf
Group:          Development/Libraries
BuildRequires:  dejavu-lgc-sans-fonts
BuildRequires:  dejavu-lgc-sans-mono-fonts
BuildRequires:  dejavu-lgc-serif-fonts
BuildRequires:  dejavu-sans-fonts
BuildRequires:  dejavu-sans-mono-fonts
BuildRequires:  dejavu-serif-fonts
Requires:       %{name} = %{version}-%{release}
Requires:       dejavu-lgc-sans-fonts
Requires:       dejavu-lgc-sans-mono-fonts
Requires:       dejavu-lgc-serif-fonts
Requires:       dejavu-sans-fonts
Requires:       dejavu-sans-mono-fonts
Requires:       dejavu-serif-fonts

%description dejavu-fonts
This package allow to use system DejaVu fonts in TCPDF.

%package gnu-free-fonts
Summary:        GNU FreeFonts for tcpdf
Group:          Development/Libraries
%if 0%{?fedora} >= 11 || 0%{?rhel} >= 6
BuildRequires:  gnu-free-mono-fonts
BuildRequires:  gnu-free-sans-fonts
BuildRequires:  gnu-free-serif-fonts
Requires:       %{name} = %{version}-%{release}
Requires:       gnu-free-mono-fonts
Requires:       gnu-free-sans-fonts
Requires:       gnu-free-serif-fonts
%else
BuildRequires:  freefont
Requires:       freefont
%endif

%description gnu-free-fonts
This package allow to use system GNU FreeFonts in TCPDF.



%prep
%setup -qn %{real_name}

%patch0 -p1

: fix barcode examples
sed -e "s:dirname(__FILE__).'/../../:'tcpdf/:" \
    -i examples/barcodes/*php

: remove bundled fonts
rm -rf fonts/dejavu-fonts-ttf* fonts/freefont-*
for fic in fonts/*.z
do
  rm -f $fic ${fic/.z/.php}
done
ls fonts | sed -e 's|^|%{_datadir}/php/%{real_name}/fonts/|' >corefonts.lst


%build
: empty build section, nothing required


%install
rm -rf %{buildroot}
# Library
install -d     %{buildroot}%{_datadir}/php/%{real_name}
cp -a *.php    %{buildroot}%{_datadir}/php/%{real_name}/
cp -a include  %{buildroot}%{_datadir}/php/%{real_name}/
cp -a fonts    %{buildroot}%{_datadir}/php/%{real_name}/
install -d     %{buildroot}%{_datadir}/php/%{real_name}/images
install -m 0644 examples/images/_blank.png \
               %{buildroot}%{_datadir}/php/%{real_name}/images/

# Config
install -d     %{buildroot}%{_sysconfdir}/%{name}
install -m 0644 config/*.php \
               %{buildroot}%{_sysconfdir}/%{name}

# Tools
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
    --fonts $list \
    --link \
    --outpath %{buildroot}%{_datadir}/php/%{real_name}/fonts/


%clean
rm -rf %{buildroot}


%files -f corefonts.lst
%defattr(-,root,root,-)
%doc LICENSE.TXT README.TXT CHANGELOG.TXT examples
%{_bindir}/%{real_name}_addfont
%dir %{_datadir}/php/%{real_name}
%dir %{_datadir}/php/%{real_name}/fonts
%{_datadir}/php/%{real_name}/include
%{_datadir}/php/%{real_name}/images
%{_datadir}/php/%{real_name}/*php
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/*

%files dejavu-fonts
%defattr(-,root,root,-)
%{_datadir}/php/%{real_name}/fonts/dejavu*

%files gnu-free-fonts
%defattr(-,root,root,-)
%{_datadir}/php/%{real_name}/fonts/free*


%changelog
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

* Sun May 10 2013 Johan Cwiklinski <johan AT x-tnd DOT be> - 6.0.012-3
- Fix README.cache file permissions

* Fri May 10 2013 Remi Collet <remi@fedoraproject.org> - 6.0.012-2
- improve cache ownership, on folder per web server
- drop bundled fonts

* Thu May 09 2013 Johan Cwiklinski <johan AT x-tnd DOT be> - 6.0.012-1
- Initial packaging
