# remirepo spec file for php-getid3, from:
#
# Fedora spec file for php-getid3
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#
%global gh_commit    b9a8564e56bdcc294dc7ade32a7f67885bed3778
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     JamesHeinrich
%global gh_project   getID3
%global pk_owner     james-heinrich
%global pk_project   getid3

Name:      php-%{pk_project}
Version:   1.9.13
Release:   1%{?dist}
Epoch:     1
License:   LGPLv3+
Summary:   The PHP media file parser
Group:     Development/Libraries
URL:       http://www.getid3.org/
Source0:   https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}-%{gh_short}.tar.gz

BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: php-fedora-autoloader-devel

# from composer.json
#        "php": ">=5.3.0"
Requires:  php(language) >= 5.3.0
# from phpcompatinfo for version 1.9.12
Requires:  php-simplexml
Requires:  php-ctype
Requires:  php-date
Requires:  php-exif
Requires:  php-gd
Requires:  php-iconv
Requires:  php-libxml
Requires:  php-pcre
Requires:  php-xml
# Optional: dba, mysql, mysqli, sqlite3, rar
# Autoloader
Requires:  php-composer(fedora/autoloader)

Provides:  php-composer(%{pk_owner}/%{pk_project}) = %{version}


%description
getID3() is a PHP script that extracts useful information 
(such as ID3 tags, bitrate, playtime, etc.) from MP3s & 
other multimedia file formats (Ogg, WMA, WMV, ASF, WAV, AVI, 
AAC, VQF, FLAC, MusePack, Real, QuickTime, Monkey's Audio, MIDI and more).

Autoloader: %{_datadir}/php/getid3/autoload.php


%prep
%setup -q -n %{gh_project}-%{gh_commit}



%build
# From composer.json, "autoload": {
#        "classmap": ["getid3/getid3.php"]
%{_bindir}/phpab --template fedora --output getid3/autoload.php getid3/getid3.php


%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{_datadir}/php
cp -a getid3 %{buildroot}%{_datadir}/php/


%check
php -r '
require "%{buildroot}%{_datadir}/php/getid3/autoload.php";
$ok = class_exists("getID3");
echo "Autoload " . ($ok ? "Ok\n" : "fails\n");
exit ($ok ? 0 : 1);
'


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license licenses license.txt
%doc changelog.txt dependencies.txt readme.txt structure.txt demos
%doc composer.json
%{_datadir}/php/getid3


%changelog
* Thu Dec 15 2016 Remi Collet <remi@fedoraproject.org> - 1:1.9.13-1
- update to 1.9.13
- use new URL http://www.getid3.org/
- use sources from github
- switch to fedora/autoloader
- add minimal check for autoloader

* Mon Mar 21 2016 Remi Collet <remi@fedoraproject.org> - 1:1.9.12-1
- update to 1.9.12
- add simple classmap autoloader

* Fri Dec 19 2014 Remi Collet <remi@fedoraproject.org> - 1:1.9.9-1
- new release 1.9.9

* Thu Aug 21 2014 Remi Collet <remi@fedoraproject.org> - 1:1.9.8-2
- fix minimal PHP version
- add explicit dependencies for all php extensions
- fix license handling
- provides php-composer(james-heinrich/getid3)

* Wed Aug 20 2014 Adam Williamson <awilliam@redhat.com> - 1:1.9.8-1
- new release 1.9.8

* Sun Sep  8 2013 Remi Collet <RPMS@famillecollet.com> - 1:1.9.7-1
- backport 1.9.7 for remi repo

* Sun Sep 08 2013 Roma <roma@lcg.ufrj.br> - 1:1.9.7-1
- Updated to 1.9.7
- Changed license to LGPLv3+

* Sun Nov 25 2012 Remi Collet <RPMS@famillecollet.com> - 1:1.9.3-1
- backport 1.9.3 for remi repo

* Sun Oct 07 2012 Paulo Roma <roma@lcg.ufrj.br> - 1:1.9.3-1
- Downgraded to latest stable version.
- Got needed extensions by using:
  phpci print --recursive --report extension /usr/share/php/getid3/
- Added BR php-gd.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.0b5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.0b5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild


* Fri Jul 31 2009 Paulo Roma <roma@lcg.ufrj.br> 2.0.0b5-2
- Updated ampache patch.

* Thu Jun 04 2009 Paulo Roma <roma@lcg.ufrj.br> 2.0.0b5-1
- Updated to 2.0.0b5
- Patched with ampache fixes.

* Thu Jun 04 2009 Paulo Roma <roma@lcg.ufrj.br> 1.7.9-1
- Initial spec file.
