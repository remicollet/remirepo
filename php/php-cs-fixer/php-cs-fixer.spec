# remirepo/fedora spec file for php-cs-fixer
#
# Copyright (c) 2016-2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    e0e33ce4eaf59ba77ead9ce45256692aa29ecb38
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
#global gh_date      20150717
%global gh_owner     FriendsOfPHP
%global gh_project   PHP-CS-Fixer
%global php_home     %{_datadir}/php
%global with_tests   0%{!?_without_tests:1}

Name:           php-cs-fixer
Version:        2.1.1
Release:        1%{?gh_date:.%{gh_date}git%{gh_short}}%{?dist}
Summary:        A tool to automatically fix PHP code style

Group:          Development/Tools
License:        MIT
URL:            https://github.com/%{gh_owner}/%{gh_project}
# git snapshot to get upstream test suite
Source0:        %{name}-%{version}-%{gh_short}.tgz
Source1:        makesrc.sh
Source2:        %{name}-autoload.php

# Use our autoloader
Patch0:         %{name}-autoload.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
%if %{with_tests}
# For tests
BuildRequires:  php(language) >= 5.4
BuildRequires:  php-tokenizer
BuildRequires:  php-composer(symfony/console)          >= 2.3
BuildRequires:  php-composer(symfony/event-dispatcher) >= 2.1
BuildRequires:  php-composer(symfony/filesystem)       >= 2.4
BuildRequires:  php-composer(symfony/finder)           >= 2.4
BuildRequires:  php-composer(symfony/polyfill-php55)   >= 1.3
BuildRequires:  php-composer(symfony/process)          >= 2.3
BuildRequires:  php-composer(symfony/stopwatch)        >= 2.5
BuildRequires:  php-composer(sebastian/diff)           >= 1.1
BuildRequires:  php-reflection
BuildRequires:  php-dom
BuildRequires:  php-json
BuildRequires:  php-pcre
BuildRequires:  php-phar
BuildRequires:  php-spl
BuildRequires:  php-xml
# From composer.json,     "require-dev": {
#        "gecko-packages/gecko-php-unit": "^2.0",
#        "justinrainbow/json-schema": "^5.0",
#        "phpunit/phpunit": "^4.5|^5",
#        "satooshi/php-coveralls": "^1.0",
#        "symfony/phpunit-bridge": "^3.2"
BuildRequires:  php-composer(gecko-packages/gecko-php-unit) >= 2.0
BuildRequires:  php-composer(justinrainbow/json-schema) >= 5
BuildRequires:  php-composer(phpunit/phpunit) >= 4.5
BuildRequires:  php-composer(symfony/phpunit-bridge)
# Autoloader
BuildRequires:  php-composer(fedora/autoloader)
%endif

# From composer.json,     "require": {
#        "php": "^5.3.6 || >=7.0 <7.2",
#        "ext-tokenizer": "*",
#        "sebastian/diff": "^1.1",
#        "symfony/console": "^2.3 || ^3.0",
#        "symfony/event-dispatcher": "^2.1 || ^3.0",
#        "symfony/filesystem": "^2.4 || ^3.0",
#        "symfony/finder": "^2.2 || ^3.0",
#        "symfony/polyfill-php54": "^1.0",
#        "symfony/polyfill-php55": "^1.3",
#        "symfony/polyfill-xml": "^1.3",
#        "symfony/process": "^2.3 || ^3.0",
#        "symfony/stopwatch": "^2.5 || ^3.0"
# use 5.4 to avoid polyfill
Requires:       php(language) >= 5.4
Requires:       php-tokenizer
Requires:       php-composer(sebastian/diff)           >= 1.1
Requires:       php-composer(symfony/console)          >= 2.3
Requires:       php-composer(symfony/event-dispatcher) >= 2.1
Requires:       php-composer(symfony/filesystem)       >= 2.4
Requires:       php-composer(symfony/finder)           >= 2.4
Requires:       php-composer(symfony/polyfill-php55)   >= 1.3
Requires:       php-composer(symfony/process)          >= 2.3
Requires:       php-composer(symfony/stopwatch)        >= 2.5
# From phpcompatinfo report for version 2.0.0
Requires:       php-cli
Requires:       php-reflection
Requires:       php-dom
Requires:       php-json
Requires:       php-pcre
Requires:       php-phar
Requires:       php-spl
Requires:       php-xml
# Autoloader
Requires:       php-composer(fedora/autoloader)

Provides:       php-composer(friendsofphp/php-cs-fixer) = %{version}


%description
The PHP Coding Standards Fixer tool fixes most issues in your code when you
want to follow the PHP coding standards as defined in the PSR-1 and PSR-2
documents and many more.

If you are already using a linter to identify coding standards problems in
your code, you know that fixing them by hand is tedious, especially on large
projects. This tool does not only detect them, but also fixes them for you.


%prep
%setup -q -n %{gh_project}-%{gh_commit}
%patch0 -p1 -b .rpm

cp %{SOURCE2} src/autoload.php


%build
# Empty build section, most likely nothing required.


%install
rm -rf %{buildroot}

: Library
mkdir -p   %{buildroot}%{php_home}
cp -pr src %{buildroot}%{php_home}/PhpCsFixer

: Command
install -Dpm755 %{name} %{buildroot}%{_bindir}/%{name}


%check
%if %{with_tests}
mkdir vendor
cat << 'EOF' | tee vendor/autoload.php
<?php
require_once '%{php_home}/GeckoPackages/PHPUnit/autoload.php';
require_once '%{php_home}/Symfony/Bridge/PhpUnit/autoload.php';
require_once '%{php_home}/JsonSchema5/autoload.php';
require_once '%{buildroot}%{php_home}/PhpCsFixer/autoload.php';
\Fedora\Autoloader\Autoload::addPsr4('PhpCsFixer\\Tests\\', dirname(__DIR__) . '/tests');
EOF


# remirepo:11
run=0
ret=0
if which php56; then
   php56 %{_bindir}/phpunit
   run=1
fi
if which php71; then
   php71 %{_bindir}/phpunit
   run=1
fi
if [ $run -eq 0 ]; then
# see https://github.com/FriendsOfPHP/PHP-CS-Fixer/blob/master/.travis.yml
if php -r 'exit (version_compare(PHP_VERSION, "5.6", "<") ? 0 : 1);'; then
  export SKIP_LINT_TEST_CASES=1
fi

%{_bindir}/phpunit --verbose
# remirepo:2
fi
exit $ret
%else
: Test suite disabled
%endif


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc composer.json
%doc *.md *.rst
%{php_home}/PhpCsFixer
%{_bindir}/%{name}


%changelog
* Fri Mar  3 2017 Remi Collet <remi@remirepo.net> - 2.1.1-1
- Update to 2.1.1

* Sat Feb 11 2017 Remi Collet <remi@fedoraproject.org> - 2.1.0-1
- update to 2.1.0
- add dependency on symfony/polyfill-php55 (for EPEL-7)

* Thu Feb  9 2017 Remi Collet <remi@fedoraproject.org> - 2.0.1-1
- update to 2.0.1

* Thu Dec  1 2016 Remi Collet <remi@fedoraproject.org> - 2.0.0-1
- update to 2.0.0

* Tue Nov 29 2016 Remi Collet <remi@fedoraproject.org> - 1.13.0-1
- update to 1.13.0

* Tue Nov 15 2016 Remi Collet <remi@fedoraproject.org> - 1.12.4-1
- update to 1.12.4

* Sun Oct 30 2016 Remi Collet <remi@fedoraproject.org> - 1.12.3-1
- update to 1.12.3
- switch from symfony/class-loader to fedora/autoloader

* Tue Sep 27 2016 Remi Collet <remi@fedoraproject.org> - 1.12.2-1
- update to 1.12.2

* Fri Sep  9 2016 Remi Collet <remi@fedoraproject.org> - 1.12.1-1
- initial package, version 1.12.1

