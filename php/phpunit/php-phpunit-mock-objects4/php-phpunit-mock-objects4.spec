# remirepo/fedora spec file for php-phpunit-mock-objects4
#
# Copyright (c) 2013-2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global bootstrap    1
# Github
%global gh_commit    eabce450df194817a7d7e27e19013569a903a2bf
#global gh_date      20150902
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_vendor    sebastianbergmann
%global gh_project   phpunit-mock-objects
# Packagist
%global pk_vendor    phpunit
%global pk_project   phpunit-mock-objects
# Namespace
%global ns_vendor    PHPUnit6
%global ns_top       Framework
%global ns_project   MockObject
%global php_home     %{_datadir}/php
%global ver_major    4
%global ver_minor    0
%global ver_patch    1
%global specrel      2
%if %{bootstrap}
%global with_tests   0%{?_with_tests:1}
%else
%global with_tests   0%{!?_without_tests:1}
%endif

Name:           php-%{pk_project}%{ver_major}
Version:        %{ver_major}.%{ver_minor}.%{ver_patch}
Release:        %{?gh_date:1%{specrel}.%{?prever}%{!?prever:%{gh_date}git%{gh_short}}}%{!?gh_date:%{specrel}}%{?dist}
Summary:        Mock Object library for PHPUnit

Group:          Development/Libraries
License:        BSD
URL:            https://github.com/%{gh_vendor}/%{gh_project}
Source0:        https://github.com/%{gh_vendor}/%{gh_project}/archive/%{gh_commit}/%{name}-%{version}-%{gh_short}.tar.gz

# Temporary workaround, under investigation
Patch0:         %{gh_project}-4.0.0-rpm.patch

BuildArch:      noarch
BuildRequires:  php-fedora-autoloader-devel
%if %{with_tests}
BuildRequires:  php(language) >= 7.0
BuildRequires:  php-composer(phpunit/php-text-template) >= 1.2
BuildRequires:  php-composer(doctrine/instantiator) >= 1.0.2
BuildRequires:  php-composer(sebastian/exporter) >= 3.0
# From composer.json, "require-dev": {
#        "phpunit/phpunit": "^6.0"
BuildRequires:  phpunit6
%endif

# From composer.json, "require": {
#        "php": "^7.0",
#        "phpunit/php-text-template": "^1.2",
#        "doctrine/instantiator": "^1.0.2",
#        "sebastian/exporter": "^3.0"
Requires:       php(language) >= 7.0
Requires:       php-composer(phpunit/php-text-template) >= 1.2
Requires:       php-composer(phpunit/php-text-template) <  2
Requires:       php-composer(doctrine/instantiator) >= 1.0.2
Requires:       php-composer(doctrine/instantiator) <  2
Requires:       php-composer(sebastian/exporter) >= 3.0
Requires:       php-composer(sebastian/exporter) <  4
# From composer.json, "suggest": {
#        "ext-soap": "*"
Requires:       php-soap
# From phpcompatinfo report for version 4.0.0
Requires:       php-reflection
Requires:       php-pcre
Requires:       php-spl
# Autoloader
Requires:       php-composer(fedora/autoloader)


Provides:       php-composer(%{pk_vendor}/%{pk_project}) = %{version}


%description
Mock Object library for PHPUnit

Autoloader: %{php_home}/%{ns_vendor}/%{ns_top}/%{ns_project}/autoload.php


%prep
%setup -q -n %{gh_project}-%{gh_commit}

%patch0 -p0
find . -name \*.orig -exec rm {} \; -print


%build
phpab \
  --template fedora \
  --output src/autoload.php \
  src

cat <<EOF | tee -a src/autoload.php
/* dependencies */
require_once 'Text/Template/Autoload.php';
require_once 'Doctrine/Instantiator/autoload.php';
require_once 'SebastianBergmann/Exporter3/autoload.php';
EOF


%install
mkdir -p   %{buildroot}%{php_home}/%{ns_vendor}/%{ns_top}
cp -pr src %{buildroot}%{php_home}/%{ns_vendor}/%{ns_top}/%{ns_project}


%if %{with_tests}
%check
mkdir vendor
phpab \
  --template fedora \
  --output vendor/autoload.php \
  tests/_fixture/

cat << 'EOF' | tee -a vendor/autoload.php
require_once '%{buildroot}%{php_home}/%{ns_vendor}/%{ns_top}/%{ns_project}/autoload.php';
EOF

ret=0
for cmd in php70 php71 php; do
  if which $cmd; then
    $cmd -d include_path=.:%{buildroot}%{php_home}:%{php_home} \
      %{_bindir}/phpunit6 --no-coverage --verbose
  fi
done
exit $ret
%endif


%files
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc *.md
%doc composer.json
%dir %{php_home}/%{ns_vendor}/
%dir %{php_home}/%{ns_vendor}/%{ns_top}/
     %{php_home}/%{ns_vendor}/%{ns_top}/%{ns_project}/


%changelog
* Mon Mar  6 2017 Remi Collet <remi@remirepo.net> - 4.0.1-2
- fix autoloader

* Fri Mar  3 2017 Remi Collet <remi@remirepo.net> - 4.0.1-1
- Update to 4.0.1
- raise dependency on sebastian/exporter 3.0

* Tue Feb  7 2017 Remi Collet <remi@remirepo.net> - 4.0.0-1
- rename to php-phpunit-mock-objects4
- move to /usr/share/php/PHPUnit6/Framework/MockObject

* Fri Dec  9 2016 Remi Collet <remi@fedoraproject.org> - 3.4.3-1
- Update to 3.4.3

* Sun Nov 27 2016 Remi Collet <remi@fedoraproject.org> - 3.4.2-1
- Update to 3.4.2

* Tue Nov 22 2016 Remi Collet <remi@fedoraproject.org> - 3.4.1-1
- Update to 3.4.1 (no change)
- allow sebastian/exporter 2.0
- switch to fedora/autoloader

* Mon Oct 10 2016 Remi Collet <remi@fedoraproject.org> - 3.4.0-1
- Update to 3.4.0

* Tue Oct  4 2016 Remi Collet <remi@fedoraproject.org> - 3.3.1-1
- Update to 3.3.1

* Mon Oct  3 2016 Remi Collet <remi@fedoraproject.org> - 3.3.0-1
- Update to 3.3.0

* Wed Sep  7 2016 Remi Collet <remi@fedoraproject.org> - 3.2.7-1
- Update to 3.2.7

* Wed Aug 31 2016 Remi Collet <remi@fedoraproject.org> - 3.2.6-1
- Update to 3.2.6

* Sun Jun 12 2016 Remi Collet <remi@fedoraproject.org> - 3.2.3-1
- Update to 3.2.3

* Sat Jun  4 2016 Remi Collet <remi@fedoraproject.org> - 3.2.1-1
- Update to 3.2.1 (no change)
- ensure cannot be installed with old PHPUnit

* Fri Jun  3 2016 Remi Collet <remi@fedoraproject.org> - 3.2.0-1
- Update to 3.2.0
- raise build dependency on phpunit >= 5.4

* Thu Apr 21 2016 Remi Collet <remi@fedoraproject.org> - 3.1.3-1
- Update to 3.1.3

* Thu Mar 24 2016 Remi Collet <remi@fedoraproject.org> - 3.1.2-1
- Update to 3.1.2

* Wed Mar 23 2016 Remi Collet <remi@fedoraproject.org> - 3.1.0-1
- Update to 3.1.0

* Tue Dec  8 2015 Remi Collet <remi@fedoraproject.org> - 3.0.6-1
- Update to 3.0.6

* Tue Dec  8 2015 Remi Collet <remi@fedoraproject.org> - 3.0.5-1
- Update to 3.0.5

* Wed Nov 18 2015 Remi Collet <remi@fedoraproject.org> - 3.0.4-1
- Update to 3.0.4

* Sun Oct 18 2015 Remi Collet <remi@fedoraproject.org> - 3.0.3-1
- Update to 3.0.3

* Fri Oct 16 2015 Remi Collet <remi@fedoraproject.org> - 3.0.2-1
- Update to 3.0.2

* Wed Oct 14 2015 Remi Collet <remi@fedoraproject.org> - 3.0.1-1
- Update to 3.0.1

* Fri Oct  2 2015 Remi Collet <remi@fedoraproject.org> - 3.0.0-1
- Update to 3.0.0

* Mon Sep 14 2015 Remi Collet <remi@fedoraproject.org> - 3.0.0-0.1.20150902git4f526b7
- update to 3.0.0-dev
- raise dependency on PHP >= 5.6

* Fri Aug 21 2015 Remi Collet <remi@fedoraproject.org> - 2.3.7-1
- update to 2.3.7

* Sun Jul 26 2015 Remi Collet <remi@fedoraproject.org> - 2.3.6-1
- update to 2.3.6 (only cleanup)

* Sat Jul  4 2015 Remi Collet <remi@fedoraproject.org> - 2.3.5-1
- update to 2.3.5

* Thu Jul  2 2015 Remi Collet <remi@fedoraproject.org> - 2.3.4-2
- fix autoloader

* Thu Jun 11 2015 Remi Collet <remi@fedoraproject.org> - 2.3.4-1
- update to 2.3.4

* Fri May 29 2015 Remi Collet <remi@fedoraproject.org> - 2.3.3-1
- update to 2.3.3

* Thu May 28 2015 Remi Collet <remi@fedoraproject.org> - 2.3.2-1
- update to 2.3.2

* Thu Apr  2 2015 Remi Collet <remi@fedoraproject.org> - 2.3.1-1
- update to 2.3.1

* Fri Oct  3 2014 Remi Collet <remi@fedoraproject.org> - 2.3.0-1
- update to 2.3.0 for PHPUnit 4.3.0
- drop dependency on ocramius/instantiator
- add depencency on doctrine/instantiator

* Fri Oct  3 2014 Remi Collet <remi@fedoraproject.org> - 2.3.0-0
- bootstrap build

* Sun Sep  7 2014 Remi Collet <remi@fedoraproject.org> - 2.2.1-1
- update to 2.2.1
- enable test suite

* Mon Aug 11 2014 Remi Collet <remi@fedoraproject.org> - 2.2.0-1
- update to 2.2.0
- add dependency on ocramius/instantiator
- fix license handling

* Mon Jul 07 2014 Remi Collet <remi@fedoraproject.org> - 2.1.5-1
- update to 2.1.5

* Thu Jun 12 2014 Remi Collet <remi@fedoraproject.org> - 2.1.4-1
- update to 2.1.4
- add upstream patch to fix unserialize issue
  https://github.com/sebastianbergmann/phpunit-mock-objects/pull/176

* Sat Jun  7 2014 Remi Collet <remi@fedoraproject.org> - 2.1.3-1
- update to 2.1.3

* Sat Jun  7 2014 Remi Collet <remi@fedoraproject.org> - 2.1.2-1
- update to 2.1.2

* Fri Jun  6 2014 Remi Collet <remi@fedoraproject.org> - 2.1.1-1
- update to 2.1.1

* Fri May 30 2014 Remi Collet <remi@fedoraproject.org> - 2.1.0-3
- upstream fix for php 5.4.29 and 5.5.13

* Tue May  6 2014 Remi Collet <remi@fedoraproject.org> - 2.1.0-2
- workaround to autoload issue during check

* Sat May  3 2014 Remi Collet <remi@fedoraproject.org> - 2.1.0-1
- update to 2.1.0 for PHPUnit 4.1

* Wed Apr 30 2014 Remi Collet <remi@fedoraproject.org> - 2.0.5-2
- cleanup pear registry

* Tue Apr 29 2014 Remi Collet <remi@fedoraproject.org> - 2.0.5-1
- update to 2.0.5
- sources from gthub
- run tests when build --with tests option

* Sun Jan 13 2013 Remi Collet <remi@fedoraproject.org> - 1.2.3-1
- Version 1.2.3 (stable) - API 1.2.0 (stable)

* Mon Nov  5 2012 Remi Collet <remi@fedoraproject.org> - 1.2.2-1
- Version 1.2.2 (stable) - API 1.2.0 (stable)

* Sat Oct  6 2012 Remi Collet <remi@fedoraproject.org> - 1.2.1-1
- Version 1.2.1 (stable) - API 1.2.0 (stable)

* Thu Sep 20 2012 Remi Collet <remi@fedoraproject.org> - 1.2.0-1
- Version 1.2.0 (stable) - API 1.2.0 (stable)
- raise dependencies: php 5.3.3, PHPUnit 3.7.0

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jan 19 2012 Remi Collet <remi@fedoraproject.org> - 1.1.1-1
- Version 1.1.1 (stable) - API 1.1.0 (stable)

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Nov 01 2011 Remi Collet <remi@fedoraproject.org> - 1.1.0-1
- Version 1.1.0 (stable) - API 1.1.0 (stable)

* Fri Jun 10 2011 Remi Collet <Fedora@famillecollet.com> - 1.0.9-1
- Version 1.0.9 (stable) - API 1.0.4 (stable)
- remove PEAR hack (only needed for EPEL)
- raise PEAR dependency to 1.9.2

* Tue May  3 2011 Remi Collet <Fedora@famillecollet.com> - 1.0.8-2
- rebuild for doc in /usr/share/doc/pear

* Wed Feb 16 2011 Remi Collet <Fedora@famillecollet.com> - 1.0.8-1
- Version 1.0.8 (stable) - API 1.0.4 (stable)

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Feb 05 2011 Remi Collet <Fedora@famillecollet.com> - 1.0.7-1
- Version 1.0.7 (stable) - API 1.0.4 (stable)

* Tue Jan 18 2011 Remi Collet <Fedora@famillecollet.com> - 1.0.6-1
- Version 1.0.6 (stable) - API 1.0.4 (stable)

* Tue Jan 18 2011 Remi Collet <Fedora@famillecollet.com> - 1.0.5-1
- Version 1.0.5 (stable) - API 1.0.4 (stable)
- CHANGELOG and LICENSE are now in the tarball

* Mon Nov 22 2010 Remi Collet <Fedora@famillecollet.com> - 1.0.3-1
- Version 1.0.3 (stable) - API 1.0.3 (stable)

* Wed Nov 17 2010 Remi Collet <Fedora@famillecollet.com> - 1.0.2-1
- Version 1.0.2 (stable) - API 1.0.0 (stable)

* Fri Nov 05 2010 Remi Collet <Fedora@famillecollet.com> - 1.0.1-2
- lower PEAR dependency to allow el6 build
- fix URL

* Mon Oct 25 2010 Remi Collet <Fedora@famillecollet.com> - 1.0.1-1
- Version 1.0.1 (stable) - API 1.0.0 (stable)

* Sun Sep 26 2010 Remi Collet <Fedora@famillecollet.com> - 1.0.0-1
- initial generated spec + clean

