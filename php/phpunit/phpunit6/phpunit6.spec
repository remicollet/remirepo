# remirepo/fedora spec file for phpunit6
#
# Copyright (c) 2010-2017 Remi Collet
#
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    9bd36d990884d8fb3313232e0002ed4cdf79f428
#global gh_date      20150927
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_vendor    sebastianbergmann
%global gh_project   phpunit
# Packagist
%global pk_vendor    phpunit
%global pk_project   phpunit
# Namespace
%global ns_vendor    PHPUnit6
%global php_home     %{_datadir}/php
%global ver_major    6
%global ver_minor    0
%global ver_patch    9
%global specrel      1

Name:           %{pk_project}%{ver_major}
Version:        %{ver_major}.%{ver_minor}.%{ver_patch}
Release:        %{?gh_date:1%{specrel}.%{?prever}%{!?prever:%{gh_date}git%{gh_short}}}%{!?gh_date:%{specrel}}%{?dist}
Summary:        The PHP Unit Testing framework

Group:          Development/Libraries
License:        BSD
URL:            https://github.com/%{gh_vendor}/%{gh_project}
Source0:        https://github.com/%{gh_vendor}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}-%{gh_short}.tar.gz

# Fix command for autoload
Patch0:         %{name}-rpm.patch

BuildArch:      noarch
BuildRequires:  php(language) >= 7.0
BuildRequires:  php-composer(myclabs/deep-copy) <  2
BuildRequires:  php-composer(myclabs/deep-copy) >= 1.3
BuildRequires:  php-composer(phpspec/prophecy) <  2
BuildRequires:  php-composer(phpspec/prophecy) >= 1.7
BuildRequires:  php-composer(phpunit/php-code-coverage) <  6
BuildRequires:  php-composer(phpunit/php-code-coverage) >= 5.0
BuildRequires:  php-composer(phpunit/php-file-iterator) <  2
BuildRequires:  php-composer(phpunit/php-file-iterator) >= 1.4
BuildRequires:  php-composer(phpunit/php-text-template) <  2
BuildRequires:  php-composer(phpunit/php-text-template) >= 1.2
BuildRequires:  php-composer(phpunit/php-timer) <  2
BuildRequires:  php-composer(phpunit/php-timer) >= 1.0.6
BuildRequires:  php-composer(phpunit/phpunit-mock-objects) <  5
BuildRequires:  php-composer(phpunit/phpunit-mock-objects) >= 4
BuildRequires:  php-composer(sebastian/comparator) <  3
BuildRequires:  php-composer(sebastian/comparator) >= 2.0
BuildRequires:  php-composer(sebastian/diff) <  2
BuildRequires:  php-composer(sebastian/diff) >= 1.2
BuildRequires:  php-composer(sebastian/environment) <  3
BuildRequires:  php-composer(sebastian/environment) >= 2.0
BuildRequires:  php-composer(sebastian/exporter) <  4
BuildRequires:  php-composer(sebastian/exporter) >= 3.0
BuildRequires:  php-composer(sebastian/global-state) <  3
BuildRequires:  php-composer(sebastian/global-state) >= 1.1
BuildRequires:  php-composer(sebastian/object-enumerator) <  4
BuildRequires:  php-composer(sebastian/object-enumerator) >= 3.0.2
BuildRequires:  php-composer(sebastian/resource-operations) <  2
BuildRequires:  php-composer(sebastian/resource-operations) >= 1.0
BuildRequires:  php-composer(sebastian/version) <  3
BuildRequires:  php-composer(sebastian/version) >= 2.0
BuildRequires:  php-dom
BuildRequires:  php-json
BuildRequires:  php-mbstring
BuildRequires:  php-xml
BuildRequires:  php-libxml
BuildRequires:  php-composer(phpunit/php-invoker) >= 1.1.0
# Autoloader
BuildRequires:  php-fedora-autoloader-devel

# From composer.json, "require": {
#        "php": "^7.0",
#        "ext-dom": "*",
#        "ext-json": "*",
#        "ext-libxml": "*",
#        "ext-mbstring": "*",
#        "ext-xml": "*",
#        "myclabs/deep-copy": "^1.3",
#        "phpspec/prophecy": "^1.7",
#        "phpunit/php-code-coverage": "^5.0",
#        "phpunit/php-file-iterator": "^1.4",
#        "phpunit/php-text-template": "^1.2",
#        "phpunit/php-timer": "^1.0.6",
#        "phpunit/phpunit-mock-objects": "^4.0",
#        "sebastian/comparator": "^2.0",
#        "sebastian/diff": "^1.2",
#        "sebastian/environment": "^2.0",
#        "sebastian/exporter": "^3.0",
#        "sebastian/global-state": "^1.1 || ^2.0",
#        "sebastian/object-enumerator": "^3.0.2",
#        "sebastian/resource-operations": "^1.0",
#        "sebastian/version": "^2.0",
Requires:       php(language) >= 7.0
Requires:       php-cli
Requires:       php-dom
Requires:       php-json
Requires:       php-libxml
Requires:       php-mbstring
Requires:       php-xml
Requires:       php-composer(myclabs/deep-copy) <  2
Requires:       php-composer(myclabs/deep-copy) >= 1.3
Requires:       php-composer(phpspec/prophecy) <  2
Requires:       php-composer(phpspec/prophecy) >= 1.7
Requires:       php-composer(phpunit/php-code-coverage) <  6
Requires:       php-composer(phpunit/php-code-coverage) >= 5.0
Requires:       php-composer(phpunit/php-file-iterator) <  2
Requires:       php-composer(phpunit/php-file-iterator) >= 1.4
Requires:       php-composer(phpunit/php-text-template) <  2
Requires:       php-composer(phpunit/php-text-template) >= 1.2
Requires:       php-composer(phpunit/php-timer) <  2
Requires:       php-composer(phpunit/php-timer) >= 1.0.6
Requires:       php-composer(phpunit/phpunit-mock-objects) <  5
Requires:       php-composer(phpunit/phpunit-mock-objects) >= 4.0
Requires:       php-composer(sebastian/comparator) <  3
Requires:       php-composer(sebastian/comparator) >= 2.0
Requires:       php-composer(sebastian/diff) <  2
Requires:       php-composer(sebastian/diff) >= 1.2
Requires:       php-composer(sebastian/environment) >= 2.0
Requires:       php-composer(sebastian/environment) <  3
Requires:       php-composer(sebastian/exporter) <  4
Requires:       php-composer(sebastian/exporter) >= 3.0
Requires:       php-composer(sebastian/global-state) <  3
Requires:       php-composer(sebastian/global-state) >= 1.1
Requires:       php-composer(sebastian/object-enumerator) <  4
Requires:       php-composer(sebastian/object-enumerator) >= 3.0.2
Requires:       php-composer(sebastian/resource-operations) <  2
Requires:       php-composer(sebastian/resource-operations) >= 1.0
Requires:       php-composer(sebastian/version) <  3
Requires:       php-composer(sebastian/version) >= 2.0
# From composer.json, "suggest": {
#        "phpunit/php-invoker": "^1.1",
#        "ext-xdebug": "*"
Requires:       php-composer(phpunit/php-invoker) >= 1.1
Requires:       php-composer(phpunit/php-invoker) <  2
# Autoloader
Requires:       php-composer(fedora/autoloader)
# From phpcompatinfo report for version 5.6.0
Requires:       php-reflection
Requires:       php-openssl
Requires:       php-pcntl
Requires:       php-pcre
Requires:       php-phar
Requires:       php-spl
%if 0%{?fedora} > 21
Recommends:     php-phpunit-dbunit3
%endif

%if 0%{?fedora} > 99
%global single 1
Obsoletes:      php-phpunit-PHPUnit < %{ver_major}
Provides:       php-phpunit-PHPUnit = %{version}
Provides:       %{pk_project}       = %{version}
Provides:       php-composer(%{pk_vendor}/%{pk_project}) = %{version}
%else
%global single 0
%endif

%description
PHPUnit is a programmer-oriented testing framework for PHP.
It is an instance of the xUnit architecture for unit testing frameworks.


%prep
%setup -q -n %{gh_project}-%{gh_commit}
%patch0 -p0 -b .rpm


%build
%{_bindir}/phpab \
  --template fedora \
  --output   src/autoload.php \
  src

# Rely on include_path as in PHPUnit dependencies
# TODO use template2 with fedora/autoloader 1.0.0
sed -e 's:/usr/share/php/::' -i src/autoload.php

cat << 'EOF' | tee -a src/autoload.php
/* dependencies */
require_once 'File/Iterator/Autoload.php';
require_once 'Text/Template/Autoload.php';
require_once 'SebastianBergmann/CodeCoverage5/autoload.php';
require_once 'PHP/Timer/Autoload.php';
require_once '%{ns_vendor}/Framework/MockObject/autoload.php';
require_once 'Prophecy/autoload.php';
require_once 'SebastianBergmann/Comparator2/autoload.php';
require_once 'SebastianBergmann/Diff/autoload.php';
require_once 'SebastianBergmann/Environment/autoload.php';
require_once 'SebastianBergmann/Exporter3/autoload.php';
require_once (stream_resolve_include_path('SebastianBergmann/GlobalState2/autoload.php') ?: 'SebastianBergmann/GlobalState/autoload.php');
require_once 'SebastianBergmann/ObjectEnumerator3/autoload.php';
require_once 'SebastianBergmann/ResourceOperations/autoload.php';
require_once 'SebastianBergmann/Version/autoload.php';
require_once 'DeepCopy/autoload.php';
require_once 'PHP/Invoker/Autoload.php';

// Extensions
\Fedora\Autoloader\Dependencies::optional([
    '%{php_home}/%{ns_vendor}/DbUnit/autoload.php',
]);
EOF
cat src/autoload.php

%{_bindir}/phpab \
  --output   tests/autoload.php \
  --exclude  '*/BankAccountTest2.php' \
  --exclude  '*/Regression/Trac/783/OneTest.php' \
  tests


%install
mkdir -p       %{buildroot}%{php_home}
cp -pr src     %{buildroot}%{php_home}/%{ns_vendor}

install -D -p -m 755 phpunit %{buildroot}%{_bindir}/%{name}
%if %{single}
ln -s %{name} %{buildroot}%{_bindir}/phpunit
%endif


%check
OPT="--testsuite=small --no-coverage"
sed -e 's:@PATH@:%{buildroot}%{php_home}/%{ns_vendor}:' -i tests/bootstrap.php

ret=0
for cmd in php70 php71 php; do
  if which $cmd; then
     $cmd -d include_path=.:%{buildroot}%{php_home}:%{php_home} ./phpunit $OPT --verbose || ret=1
  fi
done
exit $ret


%files
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc README.md ChangeLog-%{ver_major}.%{ver_minor}.md
%doc composer.json
%{_bindir}/%{name}
%if %{single}
%{_bindir}/phpunit
%endif
%{php_home}/%{ns_vendor}


%changelog
* Wed Mar 15 2017 Remi Collet <remi@remirepo.net> - 6.0.9-1
- Update to 6.0.9
- raise dependency on phpspec/prophecy 1.7
- raise dependency on sebastian/comparator 2.0
- raise dependency on sebastian/exporter 3.0
- raise dependency on sebastian/object-enumerator 3.0.2
- more explicit dependencies
- fix autoloader to only rely on include_path

* Fri Mar  3 2017 Remi Collet <remi@remirepo.net> - 6.0.8-2
- fix autoloader for dep. with multiple versions

* Thu Mar  2 2017 Remi Collet <remi@remirepo.net> - 6.0.8-1
- Update to 6.0.8

* Sun Feb 19 2017 Remi Collet <remi@fedoraproject.org> - 6.0.7-1
- update to 6.0.7

* Wed Feb  8 2017 Remi Collet <remi@fedoraproject.org> - 6.0.6-2
- cleanup autoloader (Symfony no more used)
- fix autoloader for dbunit
- fix description

* Wed Feb  8 2017 Remi Collet <remi@fedoraproject.org> - 6.0.6-1
- update to 6.0.6

* Tue Feb  7 2017 Remi Collet <remi@fedoraproject.org> - 6.0.5-1
- rename to phpunit6
- move to /usr/share/php/PHPUnit6
- raise dependency on phpunit/php-code-coverage 5.0.0
- raise dependency on phpunit/phpunit-mock-objects 4.0.0
- change spec license to CC-BY-SA

* Tue Feb  7 2017 Remi Collet <remi@fedoraproject.org> - 5.7.11-2
- add max version for some build dependencies
- only allow Symfony 2
- handle redirect to composer installed PHPUnit v6

* Sun Feb  5 2017 Remi Collet <remi@fedoraproject.org> - 5.7.11-1
- update to 5.7.11
- raise dependency on sebastian/comparator 1.2.4
- raise dependency on sebastian/global-state 1.1

* Sat Jan 28 2017 Remi Collet <remi@fedoraproject.org> - 5.7.9-1
- update to 5.7.9

* Fri Jan 27 2017 Remi Collet <remi@fedoraproject.org> - 5.7.8-2
- add upstream patch

* Thu Jan 26 2017 Remi Collet <remi@fedoraproject.org> - 5.7.8-1
- update to 5.7.8
- temporary ignore testNoTestCases

* Thu Jan 26 2017 Remi Collet <remi@fedoraproject.org> - 5.7.7-1
- update to 5.7.7

* Mon Jan 23 2017 Remi Collet <remi@fedoraproject.org> - 5.7.6-1
- update to 5.7.6

* Thu Dec 29 2016 Remi Collet <remi@fedoraproject.org> - 5.7.5-1
- update to 5.7.5

* Wed Dec 14 2016 Remi Collet <remi@fedoraproject.org> - 5.7.4-1
- update to 5.7.4

* Fri Dec  9 2016 Remi Collet <remi@fedoraproject.org> - 5.7.3-1
- update to 5.7.3
- raise dependency on phpspec/prophecy 1.6.2

* Sun Dec  4 2016 Remi Collet <remi@fedoraproject.org> - 5.7.2-1
- update to 5.7.2

* Fri Dec  2 2016 Remi Collet <remi@fedoraproject.org> - 5.7.1-1
- update to 5.7.1

* Fri Dec  2 2016 Remi Collet <remi@fedoraproject.org> - 5.7.0-1
- update to 5.7.0

* Mon Nov 28 2016 Remi Collet <remi@fedoraproject.org> - 5.6.7-1
- update to 5.6.7

* Tue Nov 22 2016 Remi Collet <remi@fedoraproject.org> - 5.6.5-1
- update to 5.6.5
- raise dependency on sebastian/comparator 1.2.2
- raise dependency on sebastian/exporter 2.0
- raise dependency on sebastian/object-enumerator 2.0

* Mon Nov 14 2016 Remi Collet <remi@fedoraproject.org> - 5.6.3-1
- update to 5.6.3

* Mon Oct 31 2016 Remi Collet <remi@fedoraproject.org> - 5.6.2-2
- fix autoloader (don't use symfony one for symfony components)

* Tue Oct 25 2016 Remi Collet <remi@fedoraproject.org> - 5.6.2-1
- update to 5.6.2 (no change)
- switch to fedora/autoloader

* Fri Oct  7 2016 Remi Collet <remi@fedoraproject.org> - 5.6.1-1
- update to 5.6.1

* Fri Oct  7 2016 Remi Collet <remi@fedoraproject.org> - 5.6.0-1
- update to 5.6.0
- drop dependency on php-tidy

* Mon Oct  3 2016 Remi Collet <remi@fedoraproject.org> - 5.5.7-1
- Update to 5.5.7 (no change)
- sources from github

* Mon Oct  3 2016 Remi Collet <remi@fedoraproject.org> - 5.5.6-1
- Update to 5.5.6
- sources from a git snapshot

* Wed Sep 21 2016 Remi Collet <remi@fedoraproject.org> - 5.5.5-1
- Update to 5.5.5

* Wed Aug 31 2016 Remi Collet <remi@fedoraproject.org> - 5.5.4-1
- Update to 5.5.4

* Fri Aug  5 2016 Remi Collet <remi@fedoraproject.org> - 5.5.0-1
- Update to 5.5.0

* Tue Jul 26 2016 Remi Collet <remi@fedoraproject.org> - 5.4.8-1
- Update to 5.4.8 (no change)
- raise dependency on phpunit/php-code-coverage >= 4.0.1

* Thu Jul 21 2016 Remi Collet <remi@fedoraproject.org> - 5.4.7-1
- Update to 5.4.7

* Thu Jun 16 2016 Remi Collet <remi@fedoraproject.org> - 5.4.6-1
- Update to 5.4.6 (no change)

* Wed Jun 15 2016 Remi Collet <remi@fedoraproject.org> - 5.4.5-1
- Update to 5.4.5

* Thu Jun  9 2016 Remi Collet <remi@fedoraproject.org> - 5.4.4-1
- Update to 5.4.4

* Fri Jun  3 2016 Remi Collet <remi@fedoraproject.org> - 5.4.2-1
- Update to 5.4.2

* Fri Jun  3 2016 Remi Collet <remi@fedoraproject.org> - 5.4.0-1
- Update to 5.4.0
- raise dependency on phpunit/php-code-coverage >= 4.0
- raise dependency on phpunit/phpunit-mock-objects >= 3.2

* Wed May 11 2016 Remi Collet <remi@fedoraproject.org> - 5.3.4-1
- Update to 5.3.4

* Wed Apr 13 2016 Remi Collet <remi@fedoraproject.org> - 5.3.2-1
- Update to 5.3.2

* Thu Apr  7 2016 Remi Collet <remi@fedoraproject.org> - 5.3.1-1
- Update to 5.3.1

* Fri Apr  1 2016 Remi Collet <remi@fedoraproject.org> - 5.3.0-1
- Update to 5.3.0
- add dependency on sebastian/object-enumerator
- raise dependency on phpunit/phpunit-mock-objects >= 3.1

* Tue Mar 15 2016 Remi Collet <remi@fedoraproject.org> - 5.2.12-1
- Update to 5.2.12

* Mon Mar 14 2016 Remi Collet <remi@fedoraproject.org> - 5.2.11-1
- Update to 5.2.11

* Thu Mar  3 2016 Remi Collet <remi@fedoraproject.org> - 5.2.10-1
- Update to 5.2.10
- raise dependency on phpunit/php-code-coverage >= 3.3.0

* Fri Feb 19 2016 Remi Collet <remi@fedoraproject.org> - 5.2.9-1
- Update to 5.2.9

* Thu Feb 18 2016 Remi Collet <remi@fedoraproject.org> - 5.2.8-1
- Update to 5.2.8
- raise dependency on phpunit/php-code-coverage >= 3.2.1

* Tue Feb 16 2016 Remi Collet <remi@fedoraproject.org> - 5.2.6-1
- Update to 5.2.6

* Sat Feb 13 2016 Remi Collet <remi@fedoraproject.org> - 5.2.5-1
- Update to 5.2.5
- raise dependency on phpunit/php-code-coverage >= 3.2

* Thu Feb 11 2016 Remi Collet <remi@fedoraproject.org> - 5.2.4-1
- Update to 5.2.4
- lower dependency on phpunit/php-code-coverage >= 3.0

* Sun Feb  7 2016 Remi Collet <remi@fedoraproject.org> - 5.2.2-1
- Update to 5.2.2

* Fri Feb  5 2016 Remi Collet <remi@fedoraproject.org> - 5.2.1-1
- Update to 5.2.1

* Fri Feb  5 2016 Remi Collet <remi@fedoraproject.org> - 5.2.0-1
- Update to 5.2.0
- raise dependency on phpunit/php-code-coverage >= 3.1

* Tue Feb  2 2016 Remi Collet <remi@fedoraproject.org> - 5.1.7-1
- Update to 5.1.7

* Fri Jan 29 2016 Remi Collet <remi@fedoraproject.org> - 5.1.6-1
- Update to 5.1.6

* Fri Jan 29 2016 Remi Collet <remi@fedoraproject.org> - 5.1.5-1
- Update to 5.1.5

* Mon Jan 11 2016 Remi Collet <remi@fedoraproject.org> - 5.1.4-1
- Update to 5.1.4

* Thu Dec 10 2015 Remi Collet <remi@fedoraproject.org> - 5.1.3-1
- Update to 5.1.3
- obsolete php-phpunit-PHPUnit-Selenium

* Mon Dec  7 2015 Remi Collet <remi@fedoraproject.org> - 5.1.2-1
- Update to 5.1.2

* Thu Dec  3 2015 Remi Collet <remi@fedoraproject.org> - 5.1.0-1
- Update to 5.1.0

* Mon Nov 30 2015 Remi Collet <remi@fedoraproject.org> - 5.0.10-1
- Update to 5.0.10
- run test suite with both PHP 5 and 7 when available

* Wed Nov 11 2015 Remi Collet <remi@fedoraproject.org> - 5.0.9-1
- Update to 5.0.9

* Fri Oct 23 2015 Remi Collet <remi@fedoraproject.org> - 5.0.8-1
- Update to 5.0.8 (no change)

* Thu Oct 22 2015 Remi Collet <remi@fedoraproject.org> - 5.0.7-1
- Update to 5.0.7

* Wed Oct 14 2015 Remi Collet <remi@fedoraproject.org> - 5.0.6-1
- Update to 5.0.6

* Mon Oct 12 2015 Remi Collet <remi@fedoraproject.org> - 5.0.5-1
- Update to 5.0.5

* Wed Oct  7 2015 Remi Collet <remi@fedoraproject.org> - 5.0.4-1
- Update to 5.0.4

* Fri Oct  2 2015 Remi Collet <remi@fedoraproject.org> - 5.0.3-1
- Update to 5.0.3 (no change)

* Fri Oct  2 2015 Remi Collet <remi@fedoraproject.org> - 5.0.2-1
- Update to 5.0.2

* Tue Sep 29 2015 Remi Collet <remi@fedoraproject.org> - 5.0.0-0.1.20150927gite3b3f36
- update to 5.0.0-dev
- raise dependency on PHP >= 5.6
- raise dependency on phpunit/php-code-coverage ~3.0
- raise dependency on phpunit/phpunit-mock-objects ~3.0
- add dependency on sebastian/resource-operations ~1.0
- add dependency on myclabs/deep-copy ~1.3

* Sun Sep 27 2015 Remi Collet <remi@fedoraproject.org> - 4.8.9-2
- add --atleast-version command option, backported from 5.0

* Mon Sep 21 2015 Remi Collet <remi@fedoraproject.org> - 4.8.9-1
- Update to 4.8.9

* Sun Sep 20 2015 Remi Collet <remi@fedoraproject.org> - 4.8.8-1
- Update to 4.8.8

* Mon Sep 14 2015 Remi Collet <remi@fedoraproject.org> - 4.8.7-1
- Update to 4.8.7 (no change)

* Tue Aug 25 2015 Remi Collet <remi@fedoraproject.org> - 4.8.6-1
- Update to 4.8.6

* Fri Aug 21 2015 Remi Collet <remi@fedoraproject.org> - 4.8.5-1
- Update to 4.8.5 (no change)

* Sat Aug 15 2015 Remi Collet <remi@fedoraproject.org> - 4.8.4-1
- Update to 4.8.4

* Mon Aug 10 2015 Remi Collet <remi@fedoraproject.org> - 4.8.3-1
- Update to 4.8.3

* Fri Aug  7 2015 Remi Collet <remi@fedoraproject.org> - 4.8.2-1
- Update to 4.8.2

* Fri Aug  7 2015 Remi Collet <remi@fedoraproject.org> - 4.8.1-1
- Update to 4.8.1 (no change)

* Fri Aug  7 2015 Remi Collet <remi@fedoraproject.org> - 4.8.0-1
- Update to 4.8.0
- raise dependency on sebastian/environment 1.3
- rely on include_path for all dependencies
- add Changelog in documentation

* Mon Jul 13 2015 Remi Collet <remi@fedoraproject.org> - 4.7.7-1
- Update to 4.7.7 (no change)

* Tue Jun 30 2015 Remi Collet <remi@fedoraproject.org> - 4.7.6-1
- Update to 4.7.6

* Tue Jun 30 2015 Remi Collet <remi@fedoraproject.org> - 4.7.5-2
- use $fedoraClassLoader autoloader

* Sun Jun 21 2015 Remi Collet <remi@fedoraproject.org> - 4.7.5-1
- Update to 4.7.5

* Thu Jun 18 2015 Remi Collet <remi@fedoraproject.org> - 4.7.4-1
- Update to 4.7.4
- raise dependency on phpunit/php-timer >= 1.0.6

* Thu Jun 11 2015 Remi Collet <remi@fedoraproject.org> - 4.7.3-1
- Update to 4.7.3

* Sun Jun  7 2015 Remi Collet <remi@fedoraproject.org> - 4.7.2-1
- Update to 4.7.2

* Fri Jun  5 2015 Remi Collet <remi@fedoraproject.org> - 4.7.1-1
- Update to 4.7.1
- raise dependency on phpunit/php-code-coverage ~2.1
- improve autoloader

* Wed Jun  3 2015 Remi Collet <remi@fedoraproject.org> - 4.6.10-1
- Update to 4.6.10

* Fri May 29 2015 Remi Collet <remi@fedoraproject.org> - 4.6.9-1
- Update to 4.6.9

* Thu May 28 2015 Remi Collet <remi@fedoraproject.org> - 4.6.8-1
- Update to 4.6.8 (no change)

* Tue May 26 2015 Remi Collet <remi@fedoraproject.org> - 4.6.7-3
- ensure compatibility with SCL

* Tue May 26 2015 Remi Collet <remi@fedoraproject.org> - 4.6.7-2
- detect and redirect to composer installed version #1157910

* Mon May 25 2015 Remi Collet <remi@fedoraproject.org> - 4.6.7-1
- Update to 4.6.7 (no change)

* Thu Apr 30 2015 Remi Collet <remi@fedoraproject.org> - 4.6.6-1
- Update to 4.6.6

* Wed Apr 29 2015 Remi Collet <remi@fedoraproject.org> - 4.6.5-1
- Update to 4.6.5

* Fri Apr 17 2015 Remi Collet <remi@fedoraproject.org> - 4.6.4-2
- keep upstream shebang with /usr/bin/env (for SCL)

* Mon Apr 13 2015 Remi Collet <remi@fedoraproject.org> - 4.6.4-1
- Update to 4.6.4

* Tue Apr  7 2015 Remi Collet <remi@fedoraproject.org> - 4.6.2-1
- Update to 4.6.2

* Fri Apr  3 2015 Remi Collet <remi@fedoraproject.org> - 4.6.1-1
- Update to 4.6.1

* Fri Apr  3 2015 Remi Collet <remi@fedoraproject.org> - 4.6.0-1
- Update to 4.6.0
- raise dependencies on file-iterator 1.4 and diff 1.2

* Sun Mar 29 2015 Remi Collet <remi@fedoraproject.org> - 4.5.1-1
- Update to 4.5.1

* Fri Feb 13 2015 Remi Collet <remi@fedoraproject.org> - 4.5.0-1
- Update to 4.5.0
- add dependency on phpspec/prophecy
- raise dependencies on sebastian/comparator >= 1.1,
  sebastian/environment >= 1.2, sebastian/exporter >= 1.2
  and doctrine/instantiator >= 1.0.4 (for autoloader file)

* Tue Jan 27 2015 Remi Collet <remi@fedoraproject.org> - 4.4.5-1
- Update to 4.4.5 (no change)

* Tue Jan 27 2015 Remi Collet <remi@fedoraproject.org> - 4.4.4-2
- add dependency on sebastian/recursion-context

* Sun Jan 25 2015 Remi Collet <remi@fedoraproject.org> - 4.4.4-1
- Update to 4.4.4

* Sun Jan 18 2015 Remi Collet <remi@fedoraproject.org> - 4.4.2-1
- Update to 4.4.2

* Sun Dec 28 2014 Remi Collet <remi@fedoraproject.org> - 4.4.1-1
- Update to 4.4.1

* Fri Dec  5 2014 Remi Collet <remi@fedoraproject.org> - 4.4.0-1
- Update to 4.4.0
- add dependency on sebastian/global-state

* Tue Nov 11 2014 Remi Collet <remi@fedoraproject.org> - 4.3.5-1
- Update to 4.3.5
- define date.timezone in phpunit command to avoid warning

* Sat Oct 25 2014 Remi Collet <remi@fedoraproject.org> - 4.3.4-1
- Update to 4.3.4
- raise dependency on phpunit/php-file-iterator >= 1.3.2

* Fri Oct 17 2014 Remi Collet <remi@fedoraproject.org> - 4.3.3-1
- Update to 4.3.3

* Thu Oct 16 2014 Remi Collet <remi@fedoraproject.org> - 4.3.2-1
- Update to 4.3.2

* Wed Oct  8 2014 Remi Collet <remi@fedoraproject.org> - 4.3.1-2
- new upstream patch for "no colors" patch
- raise dependency on sebastian/environment >= 1.1

* Mon Oct  6 2014 Remi Collet <remi@fedoraproject.org> - 4.3.1-1
- Update to 4.3.1 (no change)

* Mon Oct  6 2014 Remi Collet <remi@fedoraproject.org> - 4.3.0-2
- only enable colors when output to a terminal (from 4.4)
- open https://github.com/sebastianbergmann/phpunit/pull/1458

* Fri Oct  3 2014 Remi Collet <remi@fedoraproject.org> - 4.3.0-1
- Update to 4.3.0
- drop dependencies on ocramius/instantiator and ocramius/lazy-map
- add dependency on doctrine/instantiator
- raise dependency on phpunit/phpunit-mock-objects >= 2.3

* Sun Sep 14 2014 Remi Collet <remi@fedoraproject.org> - 4.2.6-1
- Update to 4.2.6 (no change)

* Sun Sep  7 2014 Remi Collet <remi@fedoraproject.org> - 4.2.5-1
- Update to 4.2.5 (no change)

* Sun Aug 31 2014 Remi Collet <remi@fedoraproject.org> - 4.2.4-1
- Update to 4.2.4

* Thu Aug 28 2014 Remi Collet <remi@fedoraproject.org> - 4.2.3-1
- Update to 4.2.3

* Mon Aug 18 2014 Remi Collet <remi@fedoraproject.org> - 4.2.2-1
- Update to 4.2.2

* Sun Aug 17 2014 Remi Collet <remi@fedoraproject.org> - 4.2.1-1
- Update to 4.2.1

* Mon Aug 11 2014 Remi Collet <remi@fedoraproject.org> - 4.2.0-1
- Update to 4.2.0
- raise dependency on phpunit/phpunit-mock-objects >= 2.2
- add dependency on ocramius/instantiator, ocramius/lazy-map
  and symfony/class-loader

* Fri Jul 18 2014 Remi Collet <remi@fedoraproject.org> - 4.1.4-1
- Update to 4.1.4
- composer dependencies
- add missing documentation and license

* Fri Jun 13 2014 Remi Collet <remi@fedoraproject.org> - 4.1.3-1
- Update to 4.1.3

* Sat Jun  7 2014 Remi Collet <remi@fedoraproject.org> - 4.1.2-1
- Update to 4.1.2 (no change)
- improve test suite bootstraping
- add composer provide

* Mon May 26 2014 Remi Collet <remi@fedoraproject.org> - 4.1.1-1
- Update to 4.1.1

* Tue May  6 2014 Remi Collet <remi@fedoraproject.org> - 4.1.0-2
- fix some autoload issues

* Sat May  3 2014 Remi Collet <remi@fedoraproject.org> - 4.1.0-1
- Update to 4.1.0

* Wed Apr 30 2014 Remi Collet <remi@fedoraproject.org> - 4.0.18-2
- cleanup pear registry

* Tue Apr 29 2014 Remi Collet <remi@fedoraproject.org> - 4.0.18-1
- update to 4.0.18
- sources from github

* Tue Apr 22 2014 Remi Collet <remi@fedoraproject.org> - 3.7.35-2
- remove message about deprecated PEAR channel

* Tue Apr 22 2014 Remi Collet <remi@fedoraproject.org> - 3.7.35-1
- Update to 3.7.35

* Sun Apr 06 2014 Remi Collet <remi@fedoraproject.org> - 3.7.34-1
- Update to 3.7.34

* Tue Feb 25 2014 Remi Collet <remi@fedoraproject.org> - 3.7.32-1
- Update to 3.7.32 (no change)

* Mon Feb 03 2014 Remi Collet <remi@fedoraproject.org> - 3.7.31-1
- Update to 3.7.31 (no change)

* Fri Jan 31 2014 Remi Collet <remi@fedoraproject.org> - 3.7.30-1
- Update to 3.7.30

* Wed Jan 15 2014 Remi Collet <remi@fedoraproject.org> - 3.7.29-1
- Update to 3.7.29 (stable)

* Thu Oct 17 2013 Remi Collet <remi@fedoraproject.org> - 3.7.28-1
- Update to 3.7.28
- add Spec license header
- open https://github.com/sebastianbergmann/phpunit/issues/1029

* Mon Sep 16 2013 Remi Collet <remi@fedoraproject.org> - 3.7.27-1
- Update to 3.7.27 (no change)

* Fri Sep 13 2013 Remi Collet <remi@fedoraproject.org> - 3.7.26-1
- Update to 3.7.26 (no change)

* Tue Sep 10 2013 Remi Collet <remi@fedoraproject.org> - 3.7.25-1
- Update to 3.7.25 (no change)

* Tue Aug 20 2013 Remi Collet <remi@fedoraproject.org> - 3.7.24-1
- Update to 3.7.24

* Mon Aug 05 2013 Remi Collet <remi@fedoraproject.org> - 3.7.23-1
- Update to 3.7.23
- raise dependency on phpunit/PHP_Timer 1.0.4

* Mon Jul 08 2013 Remi Collet <remi@fedoraproject.org> - 3.7.22-1
- Update to 3.7.22

* Fri May 24 2013 Remi Collet <remi@fedoraproject.org> - 3.7.21-1
- Update to 3.7.21

* Mon May 13 2013 Remi Collet <remi@fedoraproject.org> - 3.7.20-1
- Update to 3.7.20

* Mon Mar 25 2013 Remi Collet <remi@fedoraproject.org> - 3.7.19-1
- Update to 3.7.19
- requires pear.symfony.com/Yaml >= 2.0.0, <= 2.2.99

* Fri Mar 08 2013 Remi Collet <remi@fedoraproject.org> - 3.7.18-1
- Update to 3.7.18

* Thu Mar 07 2013 Remi Collet <remi@fedoraproject.org> - 3.7.17-1
- Update to 3.7.17

* Wed Mar 06 2013 Remi Collet <remi@fedoraproject.org> - 3.7.16-1
- Update to 3.7.16

* Tue Mar 05 2013 Remi Collet <remi@fedoraproject.org> - 3.7.15-1
- Update to 3.7.15

* Thu Feb 14 2013 Remi Collet <remi@fedoraproject.org> - 3.7.14-1
- Update to 3.7.14

* Sun Jan 13 2013 Remi Collet <remi@fedoraproject.org> - 3.7.13-1
- Version 3.7.13 (stable) - API 3.7.0 (stable)

* Thu Jan 10 2013 Remi Collet <remi@fedoraproject.org> - 3.7.12-1
- Version 3.7.12 (stable) - API 3.7.0 (stable)

* Wed Jan  9 2013 Remi Collet <remi@fedoraproject.org> - 3.7.11-1
- Version 3.7.11 (stable) - API 3.7.0 (stable)

* Sun Dec  2 2012 Remi Collet <remi@fedoraproject.org> - 3.7.10-1
- Version 3.7.10 (stable) - API 3.7.0 (stable)

* Wed Nov 07 2012 Remi Collet <remi@fedoraproject.org> - 3.7.9-1
- Version 3.7.9 (stable) - API 3.7.0 (stable)

* Thu Oct 18 2012 Remi Collet <remi@fedoraproject.org> - 3.7.8-1
- Version 3.7.8 (stable) - API 3.7.0 (stable)

* Thu Oct 11 2012 Remi Collet <remi@fedoraproject.org> - 3.7.7-1
- Version 3.7.7 (stable) - API 3.7.0 (stable)

* Sun Oct  7 2012 Remi Collet <remi@fedoraproject.org> - 3.7.6-1
- Version 3.7.6 (stable) - API 3.7.0 (stable)

* Sat Oct  6 2012 Remi Collet <remi@fedoraproject.org> - 3.7.5-1
- Version 3.7.5 (stable) - API 3.7.0 (stable)

* Sat Oct  6 2012 Remi Collet <remi@fedoraproject.org> - 3.7.4-1
- Version 3.7.4 (stable) - API 3.7.0 (stable)
- add Conflicts for max version of PHP_CodeCoverage and PHPUnit_MockObject

* Thu Sep 20 2012 Remi Collet <remi@fedoraproject.org> - 3.7.1-1
- Version 3.7.1 (stable) - API 3.7.0 (stable)
- raise dependencies: php 5.3.3, PHP_CodeCoverage 1.2.1,
  PHP_Timer 1.0.2, Yaml 2.1.0 (instead of YAML from symfony 1)

* Sat Aug 04 2012 Remi Collet <remi@fedoraproject.org> - 3.6.12-1
- Version 3.6.12 (stable) - API 3.6.0 (stable)

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.6.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 07 2012 Remi Collet <remi@fedoraproject.org> - 3.6.11-1
- Version 3.6.11 (stable) - API 3.6.0 (stable)

* Fri Jan 27 2012 Remi Collet <remi@fedoraproject.org> - 3.6.10-1
- Version 3.6.10 (stable) - API 3.6.0 (stable)
- raise PHP_Invokers >= 1.1.0

* Tue Jan 24 2012 Remi Collet <remi@fedoraproject.org> - 3.6.9-1
- Version 3.6.9 (stable) - API 3.6.0 (stable)

* Sat Jan 21 2012 Remi Collet <remi@fedoraproject.org> - 3.6.8-1
- Version 3.6.8 (stable) - API 3.6.0 (stable)

* Thu Jan 05 2012 Remi Collet <remi@fedoraproject.org> - 3.6.7-1
- Version 3.6.7 (stable) - API 3.6.0 (stable)

* Mon Jan 02 2012 Remi Collet <remi@fedoraproject.org> - 3.6.6-1
- Version 3.6.6 (stable) - API 3.6.0 (stable)

* Mon Dec 19 2011 Remi Collet <remi@fedoraproject.org> - 3.6.5-1
- Version 3.6.5 (stable) - API 3.6.0 (stable)

* Sat Nov 26 2011 Remi Collet <remi@fedoraproject.org> - 3.6.4-1
- Version 3.6.4 (stable) - API 3.6.0 (stable)

* Fri Nov 11 2011 Remi Collet <remi@fedoraproject.org> - 3.6.3-1
- Version 3.6.3 (stable) - API 3.6.0 (stable)

* Fri Nov 04 2011 Remi Collet <remi@fedoraproject.org> - 3.6.2-1
- Version 3.6.2 (stable) - API 3.6.0 (stable)

* Tue Nov 01 2011 Remi Collet <remi@fedoraproject.org> - 3.6.0-1
- Version 3.6.0 (stable) - API 3.6.0 (stable)

* Fri Aug 19 2011 Remi Collet <remi@fedoraproject.org> - 3.5.15-1
- Version 3.5.15 (stable) - API 3.5.7 (stable)
- raise PEAR dependency to 1.9.3

* Fri Jun 10 2011 Remi Collet <Fedora@famillecollet.com> - 3.5.14-1
- Version 3.5.14 (stable) - API 3.5.7 (stable)

* Tue May  3 2011 Remi Collet <Fedora@famillecollet.com> - 3.5.13-2
- rebuild for doc in /usr/share/doc/pear

* Tue Mar  8 2011 Remi Collet <Fedora@famillecollet.com> - 3.5.13-1
- Version 3.5.13 (stable) - API 3.5.7 (stable)
- remove PEAR hack (only needed for EPEL)
- raise PEAR dependency to 1.9.2
- remove duplicate dependency (YAML)

* Thu Feb 24 2011 Remi Collet <Fedora@famillecollet.com> - 3.5.12-1
- Version 3.5.12 (stable) - API 3.5.7 (stable)

* Wed Feb 16 2011 Remi Collet <Fedora@famillecollet.com> - 3.5.11-1
- Version 3.5.11 (stable) - API 3.5.7 (stable)
- new dependency on php-pear(XML_RPC2)

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.5.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan 20 2011 Remi Collet <Fedora@famillecollet.com> - 3.5.10-1
- Version 3.5.10 (stable) - API 3.5.7 (stable)

* Tue Jan 18 2011 Remi Collet <Fedora@famillecollet.com> - 3.5.9-1
- Version 3.5.9 (stable) - API 3.5.7 (stable)

* Tue Jan 11 2011 Remi Collet <Fedora@famillecollet.com> - 3.5.7-1
- Version 3.5.7 (stable) - API 3.5.7 (stable)
- README, CHANGELOG and LICENSE are now in the tarball

* Mon Dec 20 2010 Remi Collet <Fedora@famillecollet.com> - 3.5.6-1
- Version 3.5.6 (stable) - API 3.5.4 (stable)
- move README.mardown to README (was Changelog, now links to doc)
- add CHANGELOG
- not more doc provided by upstream

* Mon Nov 22 2010 Remi Collet <Fedora@famillecollet.com> - 3.5.5-1
- Version 3.5.5 (stable) - API 3.5.4 (stable)

* Wed Nov 17 2010 Remi Collet <Fedora@famillecollet.com> - 3.5.4-1
- Version 3.5.4 (stable) - API 3.5.4 (stable)

* Wed Oct 27 2010 Remi Collet <Fedora@famillecollet.com> - 3.5.3-1
- Update to 3.5.3
- new requires and new packages for extensions of PHPUnit
  PHPUnit_MockObject, PHPUnit_Selenium, DbUnit
- lower PEAR dependency to allow el6 build
- define timezone during build

* Thu Jul 22 2010 Remi Collet <Fedora@famillecollet.com> - 3.4.15-1
- Update to 3.4.15

* Sat Jun 19 2010 Remi Collet <Fedora@famillecollet.com> - 3.4.14-1
- Update to 3.4.14

* Sat May 22 2010 Remi Collet <Fedora@famillecollet.com> - 3.4.13-1
- Update to 3.4.13
- add README.markdown (Changelog)

* Wed Apr 07 2010 Remi Collet <Fedora@famillecollet.com> - 3.4.12-1
- Update to 3.4.12

* Thu Feb 18 2010 Remi Collet <Fedora@famillecollet.com> - 3.4.11-1.1
- Update to 3.4.11

* Wed Feb 10 2010 Remi Collet <Fedora@famillecollet.com> - 3.4.10-1
- Update to 3.4.10

* Sun Jan 24 2010 Remi Collet <Fedora@famillecollet.com> - 3.4.9-1
- Update to 3.4.9

* Sat Jan 16 2010 Remi Collet <Fedora@famillecollet.com> - 3.4.7-1
- Update to 3.4.7
- rename from php-pear-PHPUnit to php-phpunit-PHPUnit
- update dependencies (PEAR 1.8.1, YAML, php-soap)

* Sat Sep 12 2009 Christopher Stone <chris.stone@gmail.com> 3.3.17-1
- Upstream sync

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.16-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat May 02 2009 Remi Collet <Fedora@famillecollet.com> - 3.3.16-1
- Upstream sync
- Fix requires (remove hint) and raise PEAR version to 1.7.1
- rename %%{pear_name}.xml to %%{name}.xml

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov  8 2008 Christopher Stone <chris.stone@gmail.com> 3.3.4-1
- Upstream sync

* Thu Oct 23 2008 Christopher Stone <chris.stone@gmail.com> 3.3.2-1
- Upstream sync
- Remove no longer needed Obsolete/Provides

* Thu Oct 09 2008 Christopher Stone <chris.stone@gmail.com> 3.3.1-1
- Upstream sync

* Thu Oct 09 2008 Christopher Stone <chris.stone@gmail.com> 3.2.21-1
- Upstream sync
- Add php-xml to Requires (bz #464758)

* Thu May 22 2008 Christopher Stone <chris.stone@gmail.com> 3.2.19-1
- Upstream sync

* Thu Feb 21 2008 Christopher Stone <chris.stone@gmail.com> 3.2.15-1
- Upstream sync

* Wed Feb 13 2008 Christopher Stone <chris.stone@gmail.com> 3.2.13-1
- Upstream sync

* Sun Nov 25 2007 Christopher Stone <chris.stone@gmail.com> 3.2.1-1
- Upstream sync

* Sat Sep 08 2007 Christopher Stone <chris.stone@gmail.com> 3.1.8-1
- Upstream sync

* Sun May 06 2007 Christopher Stone <chris.stone@gmail.com> 3.0.6-1
- Upstream sync

* Thu Mar 08 2007 Christopher Stone <chris.stone@gmail.com> 3.0.5-3
- Fix testdir
- Fix Provides version

* Wed Mar 07 2007 Christopher Stone <chris.stone@gmail.com> 3.0.5-2
- Add Obsoletes/Provides for php-pear(PHPUnit2)
- Requires php-pear(PEAR) >= 1.5.0
- Own %%{pear_testdir}/%%{pear_name}
- Remove no longer needed manual channel install
- Simplify %%doc
- Only unregister old phpunit on upgrade

* Mon Feb 26 2007 Christopher Stone <chris.stone@gmail.com> 3.0.5-1
- Upstream sync

* Wed Feb 21 2007 Christohper Stone <chris.stone@gmail.com> 3.0.4-1
- Upstream sync

* Mon Jan 29 2007 Christopher Stone <chris.stone@gmail.com> 3.0.3-1
- Upstream sync

* Sun Jan 14 2007 Christopher Stone <chris.stone@gmail.com> 3.0.2-1
- Upstream sync

* Fri Jan 05 2007 Christopher Stone <chris.stone@gmail.com> 3.0.1-1
- Upstream sync

* Wed Dec 27 2006 Christopher Stone <chris.stone@gmail.com> 3.0.0-1
- Initial Release
