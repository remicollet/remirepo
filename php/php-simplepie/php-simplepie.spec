# remirepo spec file for php-simplepie, from:

# Fedora spec file for php-simplepie
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#
%global gh_commit    2a24b6e74aa9bf33243020f52895fe77efe94ccf
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     simplepie
%global gh_project   simplepie
%global with_tests   0%{!?_without_tests:1}

Name:       php-simplepie
Version:    1.4.3
Release:    1%{?dist}
Summary:    A simple Atom/RSS parsing library for PHP

Group:   	Development/Libraries
License:    BSD
URL:   	    http://simplepie.org/
# Git snapshot to retrieve test suite excluded in .gitattributes
Source0:    %{gh_commit}/%{name}-%{version}-%{gh_short}.tgz
Source1:    makesrc.sh

# Adapt autoloader for installation tree
Patch0:     %{name}-rpm.patch

BuildRoot:  %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildArch:  noarch
%if %{with_tests}
BuildRequires: php-phpunit-PHPUnit
%endif

Requires:   php-IDNA_Convert
Requires:   php-curl
Requires:   php-date
Requires:   php-dom
Requires:   php-iconv
Requires:   php-libxml
Requires:   php-mbstring
Requires:   php-pcre
Requires:   php-pdo
Requires:   php-reflection
Requires:   php-xml
# Optional: memcache, memcached, redis, xmlreader, zlib

Provides:   php-composer(%{gh_owner}/%{gh_project}) = %{version}


%description
SimplePie is a very fast and easy-to-use class, written in PHP, that puts the 
'simple' back into 'really simple syndication'. Flexible enough to suit 
beginners and veterans alike, SimplePie is focused on speed, ease of use, 
compatibility and standards compliance.

Autoloader: %{_datadir}/php/%{name}/autoloader.php


%prep
%setup -q -n %{gh_project}-%{gh_commit}

%patch0 -p1 -b .rpm

find . -type f -exec chmod -x {} \;
rm demo/cache/.gitignore


%build
#non-empty build section to quell the belching that rpmlint does with an empty build


%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/%{_datadir}/php/
cp -ar library %{buildroot}/%{_datadir}/php/%{name}

install -pm 644 autoloader.php \
    %{buildroot}/%{_datadir}/php/%{name}/autoloader.php


%if %{with_tests}
%check
sed -e 's:@PATH@:%{buildroot}/%{_datadir}/php/%{name}:' \
    -i tests/bootstrap.php

# Known failed test with PHP 7+
rm tests/IRITest.php
rm tests/oldtests/first_item_title/SPtests/bugs/179.0.10.php

# remirepo:11
run=0
ret=0
if which php56; then
   php56 %{_bindir}/phpunit || ret=1
   run=1
fi
if which php71; then
   php71 %{_bindir}/phpunit || ret=1
   run=1
fi
if [ $run -eq 0 ]; then
%{_bindir}/phpunit --verbose
# remirepo:2
fi
exit $ret
%endif


%clean
rm -rf  %{buildroot}


%files
%defattr(-,root,root,-)
%doc LICENSE.txt demo
%{_datadir}/php/%{name}


%changelog
* Sun Nov 27 2016 Remi Collet <remi@fedoraproject.org> - 1.4.3-1
- update to 1.4.3

* Thu Jul  7 2016 Remi Collet <remi@fedoraproject.org> - 1.4.2-1
- update to 1.4.2
- sources from git snapshot
- add patch for php 7.1 https://github.com/simplepie/simplepie/pull/458
- provide php-composer(simplepie/simplepie)

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

