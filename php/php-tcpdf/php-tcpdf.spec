%global dl_version 6_0_013
%global real_name  tcpdf

Name:           php-tcpdf
Summary:        PHP class for generating PDF documents
Version:        6.0.013
Release:        2%{?dist}

URL:            http://www.tcpdf.org
License:        LGPLv3+
Group:          Development/Libraries

Source0:        http://downloads.sourceforge.net/%{real_name}/%{real_name}_%{dl_version}.zip
Source1:        %{real_name}_addfont.php

Patch0:         %{name}_badpath.patch
Patch1:         %{name}_config.patch
# https://sourceforge.net/p/tcpdf/patches/63/ - allow to use system fonts
Patch2:         %{name}_sysfonts.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php-cli

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
%patch0 -p1 -b .badpath
%patch1 -p1 -b .config
%patch2 -p1 -b .sysfonts

: globally fix permissions, always broken...
find ./ -type d -exec chmod 755 {} \;
find ./ -type f -exec chmod 644 {} \;

: remove bundled fonts
rm -rf fonts/dejavu-fonts-ttf* fonts/freefont-*
for fic in fonts/*.z
do
  rm -f $fic ${fic/.z/.php}
done
ls fonts | sed -e 's|^|%{_datadir}/php/%{real_name}/fonts/|' >corefonts.lst

: remove composer
rm -f composer.json

: langs are not config...
mv config/lang .

: move certs in examples
mv config/cert examples/

: some files are relevant for examples only
mv cache  examples/cache
mv config/tcpdf_config_alt.php examples/


: change examples include paths
sed -i examples/*.php examples/barcodes/*.php \
    -e "s|../config/cert/|./cert/|" \
    -e "s|../config/lang|%{_datadir}/php/%{real_name}/lang|g" \
    -e "s|../%{real_name}.php|%{real_name}/%{real_name}.php|" \
    -e "s|../config/%{real_name}_config_alt.php|%{real_name}_config_alt.php|" \
    -e "s|../cache/|cache/|" \
    -e "s|../images/|images/|" \
    -e "s|dirname(__FILE__).'/../../|'%{real_name}/|"

: wrong end-of-line encoding
sed -i 's/\r//' \
    lang/bul.php \
    images/bug.eps \
    images/tiger.ai \
    images/pelican.ai

: non UTF8 files
pushd examples
iconv -f iso8859-1 -t utf-8 example_030.php > example_030.php.conv \
   && mv -f example_030.php.conv example_030.php
popd

cat >README.cache <<EOF
This folder contains a sub-folder per user uid.

If the user running PHP doesn't appear here, you need to create it.
  mkdir <useruid>
  chown <useruid> <useruid>

EOF


%build
: empty build section, nothing required


%install
rm -rf %{buildroot}
# Library
install -d     %{buildroot}%{_datadir}/php/%{real_name}
cp -a *.php    %{buildroot}%{_datadir}/php/%{real_name}/
cp -a images   %{buildroot}%{_datadir}/php/%{real_name}/
cp -a include  %{buildroot}%{_datadir}/php/%{real_name}/
cp -a fonts    %{buildroot}%{_datadir}/php/%{real_name}/
cp -a lang     %{buildroot}%{_datadir}/php/%{real_name}/

# Config
install -d         %{buildroot}%{_sysconfdir}/%{name}
cp -a config/*.php %{buildroot}%{_sysconfdir}/%{name}

# Cache
install -d %{buildroot}%{_localstatedir}/cache/%{name}
install -m 0644 README.cache %{buildroot}%{_localstatedir}/cache/%{name}/README

# Tools
install -d %{buildroot}%{_bindir}
install -m 0755 %{SOURCE1} %{buildroot}%{_bindir}/%{real_name}_addfont.php

# Fonts
cd %{buildroot}%{_datadir}/php/%{real_name}/fonts

php -d include_path=%{buildroot}%{_datadir}/php:. \
    %{SOURCE1} \
    /usr/share/fonts/dejavu/*ttf \
%if 0%{?fedora} >= 11 || 0%{?rhel} >= 6
    /usr/share/fonts/gnu-free/*ttf \
%else
    /usr/share/fonts/freefont/*ttf \
%endif
    --link \
    --out %{buildroot}%{_datadir}/php/%{real_name}/fonts


%post
# We don't want to require "httpd" in case PHP is used with some other web
# server or without any, but we do want the owner of this directory to default
# to apache for a working "out of the box" experience on the most common setup.

for server in apache lighttpd nginx
do
  uid=$(getent passwd $server | cut -d: -f3)
  if [ -n "$uid" ]
  then
    cache=%{_var}/cache/%{name}/$uid
    if [ ! -d $cache ]
    then
      mkdir -p $cache
      chown $uid $cache
    fi
  fi
done


%clean
rm -rf %{buildroot}


%files -f corefonts.lst
%defattr(-,root,root,-)
%doc LICENSE.TXT README.TXT CHANGELOG.TXT doc/* examples
%{_bindir}/%{real_name}_addfont.php
%dir %{_datadir}/php/%{real_name}
%dir %{_datadir}/php/%{real_name}/fonts
%{_datadir}/php/%{real_name}/images
%{_datadir}/php/%{real_name}/include
%{_datadir}/php/%{real_name}/lang
%{_datadir}/php/%{real_name}/*php
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/*
%{_localstatedir}/cache/%{name}

%files dejavu-fonts
%defattr(-,root,root,-)
%{_datadir}/php/%{real_name}/fonts/dejavu*

%files gnu-free-fonts
%defattr(-,root,root,-)
%{_datadir}/php/%{real_name}/fonts/free*


%changelog
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
