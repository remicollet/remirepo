# remirepo/fedora spec file for php-phpunit-PHP-CodeCoverage
#
# Copyright (c) 2013-2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#

%global bootstrap    0
%global gh_commit    c14196e64a78570034afd0b7a9f3757ba71c2a0a
#global gh_date      20150924
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     sebastianbergmann
%global gh_project   php-code-coverage
%global php_home     %{_datadir}/php
%global pear_name    PHP_CodeCoverage
%global pear_channel pear.phpunit.de
%global major        4.0
%global minor        4
%global specrel      1
%if %{bootstrap}
%global with_tests   %{?_with_tests:1}%{!?_with_tests:0}
%else
%global with_tests   %{?_without_tests:0}%{!?_without_tests:1}
%endif

Name:           php-phpunit-PHP-CodeCoverage
Version:        %{major}.%{minor}
Release:        %{?gh_date:0.%{specrel}.%{?prever}%{!?prever:%{gh_date}git%{gh_short}}}%{!?gh_date:%{specrel}}%{?dist}
Summary:        PHP code coverage information

Group:          Development/Libraries
License:        BSD
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}-%{gh_short}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php(language) >= 5.6
BuildRequires:  php-fedora-autoloader-devel
%if %{with_tests}
# From composer.json, "require-dev": {
#        "phpunit/phpunit": "^5.4",
#        "ext-xdebug": ">=2.1.4"
BuildRequires:  php-composer(phpunit/phpunit) >= 5.4
BuildRequires:  php-composer(sebastian/code-unit-reverse-lookup) >= 1
BuildRequires:  php-composer(sebastian/environment) >= 1.3.2
BuildRequires:  php-pecl-xdebug  >= 2.4.0
%endif

# From composer.json, require
#        "php": "^5.6 || ^7.0",
#        "phpunit/php-file-iterator": "~1.3",
#        "phpunit/php-token-stream": "^1.4.2",
#        "phpunit/php-text-template": "~1.2",
#        "sebastian/code-unit-reverse-lookup": "~1.0",
#        "sebastian/environment": "^1.3.2 || ^2.0",
#        "sebastian/version": "~1.0|~2.0"
Requires:       php(language) >= 5.6
Requires:       php-composer(phpunit/php-file-iterator) >= 1.3
Requires:       php-composer(phpunit/php-file-iterator) <  2
Requires:       php-composer(phpunit/php-token-stream) >= 1.4.2
Requires:       php-composer(phpunit/php-token-stream) <  2
Requires:       php-composer(phpunit/php-text-template) >= 1.2
Requires:       php-composer(phpunit/php-text-template) <  2
Requires:       php-composer(sebastian/code-unit-reverse-lookup) >= 1
Requires:       php-composer(sebastian/code-unit-reverse-lookup) <  2
Requires:       php-composer(sebastian/environment) >= 1.3.2
Requires:       php-composer(sebastian/environment) <  3
Requires:       php-composer(sebastian/version) >= 1.0
Requires:       php-composer(sebastian/version) <  3
# From composer.json, suggest
#        "ext-dom": "*",
#        "ext-xdebug": ">=2.4.0",
#        "ext-xmlwriter": "*"
Requires:       php-dom
Requires:       php-xmlwriter
# From phpcompatinfo report for version 4.0.4
Requires:       php-reflection
Requires:       php-date
Requires:       php-json
Requires:       php-spl
Requires:       php-tokenizer
# Autoloader
Requires:       php-composer(fedora/autoloader)

Provides:       php-composer(phpunit/php-code-coverage) = %{version}

# For compatibility with PEAR mode
Provides:       php-pear(%{pear_channel}/%{pear_name}) = %{version}


%description
Library that provides collection, processing, and rendering functionality
for PHP code coverage information.


%prep
%setup -q -n %{gh_project}-%{gh_commit}


%build
%{_bindir}/phpab \
  --template fedora \
  --output src/autoload.php \
  src

cat << 'EOF' | tee -a src/autoload.php
// Dependencies
require_once 'File/Iterator/Autoload.php';
require_once 'PHP/Token/Stream/Autoload.php';
require_once 'Text/Template/Autoload.php';
require_once 'SebastianBergmann/CodeUnitReverseLookup/autoload.php';
require_once 'SebastianBergmann/Environment/autoload.php';
require_once 'SebastianBergmann/Version/autoload.php';
EOF


%install
rm -rf     %{buildroot}
# Restore PSR-0 tree
mkdir -p   %{buildroot}%{php_home}/SebastianBergmann
cp -pr src %{buildroot}%{php_home}/SebastianBergmann/CodeCoverage


%if %{with_tests}
%check
if ! php -v | grep Xdebug
then EXT="-d zend_extension=xdebug.so"
fi

cat << 'EOF' | tee tests/bootstrap.php
<?php
require '%{buildroot}%{php_home}/SebastianBergmann/CodeCoverage/autoload.php';
require __DIR__ . '/TestCase.php';
define('TEST_FILES_PATH', __DIR__ . '/_files/');
EOF

# remirepo:18
run=0
ret=0
if which php56; then
  php56 $EXT \
    -d include_path=.:%{buildroot}%{php_home}:%{php_home} \
    %{_bindir}/phpunit \
        --configuration build || ret=1
  run=1
fi
if which php71; then
  php71 $EXT \
    -d serialize_precision=14 \
    -d include_path=.:%{buildroot}%{php_home}:%{php_home} \
    %{_bindir}/phpunit \
        --configuration build || ret=1
  run=1
fi
if [ $run -eq 0 ]; then
%{_bindir}/php $EXT \
    -d serialize_precision=14 \
    -d include_path=.:%{buildroot}%{php_home}:%{php_home} \
    %{_bindir}/phpunit \
        --configuration build \
        --verbose || : ignore
# remirepo:2
fi
#exit $ret
%endif


%clean
rm -rf %{buildroot}


%post
if [ -x %{_bindir}/pear ]; then
   %{_bindir}/pear uninstall --nodeps --ignore-errors --register-only \
      %{pear_channel}/%{pear_name} >/dev/null || :
fi


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc CONTRIBUTING.md README.md composer.json
%doc ChangeLog-%{major}.md
%{php_home}/SebastianBergmann/CodeCoverage


%changelog
* Wed Dec 21 2016 Remi Collet <remi@fedoraproject.org> - 4.0.4-1
- Update to 4.0.4
- ignore test suite for now
  https://github.com/sebastianbergmann/php-code-coverage/issues/495

* Mon Nov 28 2016 Remi Collet <remi@fedoraproject.org> - 4.0.3-1
- Update to 4.0.3

* Wed Nov 23 2016 Remi Collet <remi@fedoraproject.org> - 4.0.2-2
- set serialize_precision=14 for the test suite
  to fix FTBFS with PHP 7.1

* Tue Nov  1 2016 Remi Collet <remi@fedoraproject.org> - 4.0.2-1
- Update to 4.0.2
- switch to fedora-autoloader

* Tue Jul 26 2016 Remi Collet <remi@fedoraproject.org> - 4.0.1-1
- Update to 4.0.1

* Fri Jun  3 2016 Remi Collet <remi@fedoraproject.org> - 4.0.0-1
- Update to 4.0.0
- namespace changed from PHP to SebastianBergmann
- raise build dependency on phpunit >= 5.4

* Sat May 28 2016 Remi Collet <remi@fedoraproject.org> - 3.3.3-1
- Update to 3.3.3

* Wed May 25 2016 Remi Collet <remi@fedoraproject.org> - 3.3.2-1
- Update to 3.3.2

* Wed May  4 2016 Remi Collet <remi@fedoraproject.org> - 3.3.1-2
- add upstream patch for environment 1.3.6
  https://github.com/sebastianbergmann/php-code-coverage/pull/435

* Fri Apr  8 2016 Remi Collet <remi@fedoraproject.org> - 3.3.1-1
- Update to 3.3.1

* Thu Mar  3 2016 Remi Collet <remi@fedoraproject.org> - 3.3.0-1
- Update to 3.3.0

* Thu Feb 18 2016 Remi Collet <remi@fedoraproject.org> - 3.2.1-1
- Update to 3.2.1
- raise dependency on php-token-stream >= 1.4.2

* Sat Feb 13 2016 Remi Collet <remi@fedoraproject.org> - 3.2.0-1
- Update to 3.2.0
- add dependency on sebastian/code-unit-reverse-lookup

* Thu Feb  4 2016 Remi Collet <remi@fedoraproject.org> - 3.1.1-1
- Update to 3.1.1
- allow sebastian/version ~2.0
- drop autoloader template

* Mon Jan 11 2016 Remi Collet <remi@fedoraproject.org> - 3.1.0-1
- Update to 3.1.0

* Fri Nov 13 2015 Remi Collet <remi@fedoraproject.org> - 3.0.2-1
- Update to 3.0.2
- run test suite with both PHP 5 and 7 when available

* Wed Oct  7 2015 Remi Collet <remi@fedoraproject.org> - 3.0.1-1
- Update to 3.0.1

* Fri Oct  2 2015 Remi Collet <remi@fedoraproject.org> - 3.0.0-1
- Update to 3.0.0

* Fri Oct  2 2015 Remi Collet <remi@fedoraproject.org> - 3.0.0-0
- Update to 3.0.0, boostrap build

* Mon Sep 14 2015 Remi Collet <remi@fedoraproject.org> - 3.0.0-0.1.20150924git12259bb
- rebuild (not boostrap)

* Mon Sep 14 2015 Remi Collet <remi@fedoraproject.org> - 3.0.0-0.0.20150924git12259bb
- update to 3.0.0-dev
- raise dependency on PHP >= 5.6
- bootstrap build

* Mon Sep 14 2015 Remi Collet <remi@fedoraproject.org> - 2.2.3-1
- update to 2.2.3

* Tue Aug  4 2015 Remi Collet <remi@fedoraproject.org> - 2.2.2-1
- update to 2.2.2
- raise dependency on sebastian/environment ^1.3.2

* Sun Aug  2 2015 Remi Collet <remi@fedoraproject.org> - 2.2.1-1
- update to 2.2.1 (no change)
- raise dependency on sebastian/environment ~1.3.1

* Sat Aug  1 2015 Remi Collet <remi@fedoraproject.org> - 2.2.0-1
- update to 2.2.0
- raise dependency on sebastian/environment ~1.3

* Sun Jul 26 2015 Remi Collet <remi@fedoraproject.org> - 2.1.9-1
- update to 2.1.9 (only cleanup)

* Mon Jul 13 2015 Remi Collet <remi@fedoraproject.org> - 2.1.8-1
- update to 2.1.8

* Thu Jul  2 2015 Remi Collet <remi@fedoraproject.org> - 2.1.7-2
- fix autoloader

* Tue Jun 30 2015 Remi Collet <remi@fedoraproject.org> - 2.1.7-1
- update to 2.1.7

* Fri Jun 19 2015 Remi Collet <remi@fedoraproject.org> - 2.1.6-1
- update to 2.1.6

* Tue Jun  9 2015 Remi Collet <remi@fedoraproject.org> - 2.1.5-1
- update to 2.1.5

* Sun Jun  7 2015 Remi Collet <remi@fedoraproject.org> - 2.1.4-1
- update to 2.1.4

* Wed Jun  3 2015 Remi Collet <remi@fedoraproject.org> - 2.1.3-1
- update to 2.1.3

* Mon Jun  1 2015 Remi Collet <remi@fedoraproject.org> - 2.1.2-1
- update to 2.1.2

* Sun May 31 2015 Remi Collet <remi@fedoraproject.org> - 2.1.1-1
- update to 2.1.1

* Mon May 25 2015 Remi Collet <remi@fedoraproject.org> - 2.0.17-1
- update to 2.0.17

* Mon Apr 13 2015 Remi Collet <remi@fedoraproject.org> - 2.0.16-1
- update to 2.0.16

* Sun Jan 25 2015 Remi Collet <remi@fedoraproject.org> - 2.0.15-1
- update to 2.0.15

* Fri Dec 26 2014 Remi Collet <remi@fedoraproject.org> - 2.0.14-1
- update to 2.0.14

* Wed Dec  3 2014 Remi Collet <remi@fedoraproject.org> - 2.0.13-1
- update to 2.0.13

* Tue Dec  2 2014 Remi Collet <remi@fedoraproject.org> - 2.0.12-1
- update to 2.0.12

* Thu Sep  4 2014 Remi Collet <remi@fedoraproject.org> - 2.0.11-2
- add BR on php-pecl-xdebug (thanks to Koschei)

* Sun Aug 31 2014 Remi Collet <remi@fedoraproject.org> - 2.0.11-1
- update to 2.0.11
- raise dependency on phpunit/php-token-stream ~1.3
- enable tests during build
- drop optional dependency on XDebug

* Mon Aug 11 2014 Remi Collet <remi@fedoraproject.org> - 2.0.10-1
- update to 2.0.10
- fix license handling

* Mon Jul 07 2014 Remi Collet <remi@fedoraproject.org> - 2.0.9-1
- update to 2.0.9

* Wed Jun 25 2014 Remi Collet <remi@fedoraproject.org> - 2.0.8-3
- composer dependencies

* Tue May 27 2014 Remi Collet <remi@fedoraproject.org> - 2.0.8-1
- update to 2.0.8

* Wed Apr 30 2014 Remi Collet <remi@fedoraproject.org> - 2.0.6-1
- update to 2.0.6

* Wed Apr 30 2014 Remi Collet <remi@fedoraproject.org> - 2.0.5-2
- cleanup pear registry

* Tue Apr 29 2014 Remi Collet <remi@fedoraproject.org> - 2.0.5-1
- update to 2.0.5
- sources from github

* Tue Apr 01 2014 Remi Collet <remi@fedoraproject.org> - 1.2.17-1
- Update to 1.2.17

* Tue Feb 25 2014 Remi Collet <remi@fedoraproject.org> - 1.2.16-1
- Update to 1.2.16

* Mon Feb 03 2014 Remi Collet <remi@fedoraproject.org> - 1.2.15-1
- Update to 1.2.15

* Fri Jan 31 2014 Remi Collet <remi@fedoraproject.org> - 1.2.14-1
- Update to 1.2.14
- raise dependency on Text_Template 1.2.0

* Tue Sep 10 2013 Remi Collet <remi@fedoraproject.org> - 1.2.13-1
- Update to 1.2.13

* Mon Jul 08 2013 Remi Collet <remi@fedoraproject.org> - 1.2.12-1
- Update to 1.2.12

* Fri May 24 2013 Remi Collet <remi@fedoraproject.org> - 1.2.11-1
- Update to 1.2.11

* Mon May 13 2013 Remi Collet <remi@fedoraproject.org> - 1.2.10-1
- Update to 1.2.10

* Tue Feb 26 2013 Remi Collet <remi@fedoraproject.org> - 1.2.9-1
- Update to 1.2.9

* Thu Feb 14 2013 Remi Collet <remi@fedoraproject.org> - 1.2.8-1
- Update to 1.2.8

* Sun Dec  2 2012 Remi Collet <remi@fedoraproject.org> - 1.2.7-1
- Version 1.2.7 (stable) - API 1.2.0 (stable)

* Thu Oct 18 2012 Remi Collet <remi@fedoraproject.org> - 1.2.6-1
- Version 1.2.6 (stable) - API 1.2.0 (stable)

* Sun Oct  7 2012 Remi Collet <remi@fedoraproject.org> - 1.2.5-1
- Version 1.2.5 (stable) - API 1.2.0 (stable)

* Sat Oct  6 2012 Remi Collet <remi@fedoraproject.org> - 1.2.3-1
- Version 1.2.3 (stable) - API 1.2.0 (stable)

* Fri Sep 21 2012 Remi Collet <remi@fedoraproject.org> - 1.2.2-1
- Version 1.2.2 (stable) - API 1.2.0 (stable)

* Thu Sep 20 2012 Remi Collet <remi@fedoraproject.org> - 1.2.1-1
- Version 1.2.1 (stable) - API 1.2.0 (stable)
- raise dependency: php 5.3.3, PHP_TokenStream 1.1.3

* Wed Aug 01 2012 Remi Collet <remi@fedoraproject.org> - 1.1.3-1
- Version 1.1.3 (stable) - API 1.1.0 (stable)

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Feb 23 2012 Remi Collet <remi@fedoraproject.org> - 1.1.2-1
- Version 1.1.2 (stable) - API 1.1.0 (stable)

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Nov 04 2011 Remi Collet <remi@fedoraproject.org> - 1.1.1-1
- Version 1.1.1 (stable) - API 1.1.0 (stable)

* Tue Nov 01 2011 Remi Collet <remi@fedoraproject.org> - 1.1.0-1
- Version 1.1.0 (stable) - API 1.1.0 (stable)
- no more phpcov script in bindir

* Fri Aug 19 2011 Remi Collet <remi@fedoraproject.org> - 1.0.5-1
- Version 1.0.5 (stable) - API 1.0.3 (stable)
- remove PEAR hack (only needed for EPEL)
- raise PEAR dependency to 1.9.2

* Tue May  3 2011 Remi Collet <Fedora@famillecollet.com> - 1.0.4-2
- rebuild for doc in /usr/share/doc/pear

* Wed Feb 16 2011 Remi Collet <Fedora@famillecollet.com> - 1.0.4-1
- Version 1.0.4 (stable) - API 1.0.3 (stable)
- LICENSE CHANGELOG now provided by upstream

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jan 02 2011 Remi Collet <Fedora@famillecollet.com> - 1.0.3-1
- Version 1.0.3 (stable) - API 1.0.3 (stable)

* Wed Nov 17 2010 Remi Collet <Fedora@famillecollet.com> - 1.0.2-1
- Version 1.0.2 (stable) - API 1.0.0 (stable)

* Thu Nov 04 2010 Remi Collet <Fedora@famillecollet.com> - 1.0.0-1.1
- lower PEAR dependency to allow f13 and el6 build
- fix URL

* Sun Sep 26 2010 Remi Collet <Fedora@famillecollet.com> - 1.0.0-1
- initial generated spec + clean

