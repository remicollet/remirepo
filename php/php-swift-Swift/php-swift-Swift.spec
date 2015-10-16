# remirepo spec file for php-swift-Swift, from
#
# Fedora spec file for php-swift-Swift
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#
%global gh_commit    0697e6aa65c83edf97bb0f23d8763f94e3f11421
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     swiftmailer
%global gh_project   swiftmailer
%global with_tests   0%{!?_without_tests:1}
%global php_home     %{_datadir}/php

Name:           php-swift-Swift
Version:        5.4.1
Release:        1%{?dist}
Summary:        Free Feature-rich PHP Mailer

Group:          Development/Libraries
License:        MIT
URL:            http://www.swiftmailer.org/
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}-%{gh_short}.tar.gz

# Upstream patches
# Fix test bootstrap and disable gc to avoid segfault
Patch0:         %{gh_project}-upstream.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
%if %{with_tests}
BuildRequires:  php-composer(phpunit/phpunit)
BuildRequires:  php-composer(theseer/autoload)
# From composer.json, "require-dev": {
#        "mockery/mockery": "~0.9.1,<0.9.4"
BuildRequires:  php-composer(mockery/mockery) >= 0.9.1
BuildRequires:  php-composer(mockery/mockery) <  0.9.4
%endif

# From composer.json, "require": {
#        "php": ">=5.3.3"
Requires:       php(language) >= 5.3.3
# from phpcompatinfo report on version 5.4.1
Requires:       php-bcmath
Requires:       php-ctype
Requires:       php-date
Requires:       php-hash
Requires:       php-iconv
Requires:       php-mbstring
Requires:       php-mcrypt
Requires:       php-mhash
Requires:       php-openssl
Requires:       php-pcre
Requires:       php-reflection
Requires:       php-simplexml
Requires:       php-spl

# Single package in this channel
Obsoletes:      php-channel-swift <= 1.3

Provides:       php-composer(swiftmailer/swiftmailer) = %{version}
Provides:       php-pear(pear.swiftmailer.org/Swift) = %{version}


%description
Swift Mailer integrates into any web app written in PHP 5, offering a 
flexible and elegant object-oriented approach to sending emails with 
a multitude of features.

To use this library, you just have to add, in your project:
  require_once '%{php_home}/Swift/swift_required.php';



%prep
%setup -q -n %{gh_project}-%{gh_commit}

%patch0 -p1

mv lib/swift_required_pear.php lib/swift_required.php
rm lib/swiftmailer_generate_mimes_config.php


%build
# Empty build section, most likely nothing required.


%install
rm -rf %{buildroot}

mkdir -p                   %{buildroot}/%{php_home}/Swift
cp -p lib/*.php            %{buildroot}/%{php_home}/Swift/
cp -pr lib/classes/*       %{buildroot}/%{php_home}/Swift/
cp -pr lib/dependency_maps %{buildroot}/%{php_home}/Swift/


%check
%if %{with_tests}
: Use installed tree and autoloader
mkdir vendor
%{_bindir}/phpab --output vendor/autoload.php tests
cat << 'EOF' | tee -a vendor/autoload.php
require_once '%{buildroot}/%{php_home}/Swift/swift_required.php';
require_once '/usr/share/php/Mockery/autoload.php';
EOF

: Run upstream test suite
%{_bindir}/phpunit --exclude smoke --verbose
%endif



%clean
rm -rf %{buildroot}


%post
if [ -x %{_bindir}/pear ]; then
  %{_bindir}/pear uninstall --nodeps --ignore-errors --register-only \
    pear.swiftmailer.org/Swift >/dev/null || :
fi


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc CHANGES README
%doc doc
%doc composer.json
%{php_home}/Swift


%changelog
* Fri Oct 16 2015 Remi Collet <remi@fedoraproject.org> - 5.4.1-1
- update to 5.4.1
- sources from github, pear channel is dead
- provide php-composer(swiftmailer/swiftmailer)
- add BR on mockery/mockery
- fix license handling

* Tue Mar 18 2014 Remi Collet <remi@fedoraproject.org> - 5.1.0-1
- Update to 5.1.0 (stable)
- add dependencies on bcmath, mcrypt and mhash

* Tue Dec 03 2013 Remi Collet <remi@fedoraproject.org> - 5.0.3-1
- Update to 5.0.3 (stable)

* Fri Aug 30 2013 Remi Collet <remi@fedoraproject.org> - 5.0.2-1
- Update to 5.0.2

* Tue Jun 18 2013 Remi Collet <remi@fedoraproject.org> - 5.0.1-1
- Update to 5.0.1

* Sat May 25 2013 Remi Collet <remi@fedoraproject.org> - 5.0.0-1
- Update to 5.0.0 (relicense under MIT)

* Thu Apr 11 2013 Remi Collet <remi@fedoraproject.org> - 4.3.1-1
- Update to 4.3.1

* Tue Jan  8 2013 Remi Collet <RPMS@FamilleCollet.com> - 4.3.0-1
- upstream 4.3.0

* Fri Oct 26 2012 Remi Collet <RPMS@FamilleCollet.com> - 4.2.2-1
- upstream 4.2.2

* Tue Jul 17 2012 Remi Collet <RPMS@FamilleCollet.com> - 4.2.1-1
- upstream 4.2.1, backport for remi repository

* Fri Jul 13 2012 Christof Damian <christof@damian.net> - 4.2.1-1
- upstream 4.2.1

* Sun Apr 29 2012 Remi Collet <RPMS@FamilleCollet.com> - 4.1.7-1
- upstream 4.1.7, rebuild for remi repository

* Sat Apr 28 2012 Christof Damian <christof@damian.net> - 4.1.7-1
- upstream 4.1.7

* Sat Mar 31 2012 Remi Collet <RPMS@FamilleCollet.com> - 4.1.6-1
- upstream 4.1.6, rebuild for remi repository

* Sat Mar 24 2012 Christof Damian <christof@damian.net> - 4.1.6-1
- upstream 4.1.6

* Sun Mar 04 2012 Remi Collet <RPMS@FamilleCollet.com> - 4.1.5-1
- upstream 4.1.5, rebuild for remi repository

* Sat Mar  3 2012 Christof Damian <christof@damian.net> - 4.1.5-1
- upstream 4.1.5

* Tue Nov 01 2011 Remi Collet <RPMS@FamilleCollet.com> - 4.1.3-1
- rebuild for remi repository

* Fri Oct 28 2011 Christof Damian <christof@damian.net> - 4.1.3-1
- upstream 4.1.3

* Sat Jul 16 2011 Remi Collet <RPMS@FamilleCollet.com> - 4.1.1-1
- rebuild for remi repository
- doc in /usr/share/doc/pear

* Fri Jul 15 2011 Christof Damian <christof@damian.net> - 4.1.1-1
- upstream 4.1.1

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu May 13 2010 Remi Collet <RPMS@FamilleCollet.com> - 4.0.6-1
- rebuild for remi repository

* Wed May 12 2010 Christof Damian <christof@damian.net> - 4.0.6-1
- upstream 4.0.6 (bugfixes)

* Tue Dec 1 2009 Christof Damian <christof@damian.net> 4.0.5-1
- initial rpm
