Name:		php-simplepie
Version:	1.3.1
Release:	2%{?dist}
Summary:	Simple RSS Library in PHP

Group:		Development/Libraries
License:	BSD
URL:		http://simplepie.org/
Source0:	http://simplepie.org/downloads/simplepie_%{version}.zip

BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildArch:	noarch
BuildRequires:	php-phpunit-PHPUnit

Requires:	php-IDNA_Convert
Requires:	php-curl
Requires:	php-date
Requires:	php-dom
Requires:	php-iconv
Requires:	php-libxml
Requires:	php-mbstring
Requires:	php-pcre
Requires:	php-pdo
Requires:	php-reflection
Requires:	php-xml
# Optional: memcache, xmlreader, zlib

%description
SimplePie is a very fast and easy-to-use class, written in PHP, that puts the 
'simple' back into 'really simple syndication'. Flexible enough to suit 
beginners and veterans alike, SimplePie is focused on speed, ease of use, 
compatibility and standards compliance.

%prep
%setup -qn simplepie-simplepie-e9472a1
chmod -x demo/cli_test.php
chmod -x demo/for_the_demo/mediaplayer_readme.htm


%build
#non-empty build section to quell the belching that rpmlint does with an empty build


%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/%{_datadir}/php/
cp -ar library %{buildroot}/%{_datadir}/php/%{name}

sed -e '/__FILE__/s/\..*$/;/' autoloader.php \
    > %{buildroot}/%{_datadir}/php/%{name}/autoloader.php


%check
phpunit .


%clean
rm -rf  %{buildroot}


%files
%defattr(-,root,root,-)
%doc LICENSE.txt demo
%{_datadir}/php/%{name}


%changelog
* Sun Dec 16 2012 Remi Collet <remi@fedoraproject.org> - 1.3.1-2
- really install library
- provides autoloader.php
- run tests

* Wed Dec 12 2012 Nick Bebout <nb@fedoraproject.org> - 1.3.1-1
- Update to 1.3.1

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Aug 30 2011 Adam Williamson <awilliam@redhat.com> - 1.2-1
- bump to 1.2 (a mere two years late!)

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Apr 23 2009 David Nalley <david@gnsa.us> 1.1.3-3
- used version macro in source url
- stopped using two different macros for buildroot
- stopped using macro for mkdir
- moved chmods to immediately after setup in prep
- removed line that rm compatibility_test
- used a single line to copy create.php and simplepie.inc
* Thu Apr 23 2009 David Nalley <david@gnsa.us> 1.1.3-2
- Removed php asa requires since php-IDNA_convert pulls it in
* Wed Apr 22 2009 David Nalley <david@gnsa.us> 1.1.3-1
- Initial packaging efforts

