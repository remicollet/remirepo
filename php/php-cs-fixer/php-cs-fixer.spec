# remirepo/fedora spec file for php-cs-fixer
#
# Copyright (c) 2016 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    d33ee60f3d3e6152888b7f3a385f49e5c43bf1bf
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
#global gh_date      20150717
%global gh_owner     FriendsOfPHP
%global gh_project   PHP-CS-Fixer
%global php_home     %{_datadir}/php
%global with_tests   0%{!?_without_tests:1}

Name:           php-cs-fixer
Version:        1.12.1
Release:        1%{?gh_date:.%{gh_date}git%{gh_short}}%{?dist}
Summary:        A tool to automatically fix PHP code style

Group:          Development/Libraries
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
BuildRequires:  php(language) >= 5.3.6
BuildRequires:  php-tokenizer
BuildRequires:  php-composer(symfony/console)          >= 2.3
BuildRequires:  php-composer(symfony/event-dispatcher) >= 2.1
BuildRequires:  php-composer(symfony/filesystem)       >= 2.1
BuildRequires:  php-composer(symfony/finder)           >= 2.1
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
#        "phpunit/phpunit": "^4.5|^5",
#        "satooshi/php-coveralls": "^1.0"
BuildRequires:  php-composer(phpunit/phpunit) >= 4.5
# Autoloader
BuildRequires:  php-composer(symfony/class-loader)
%endif

# From composer.json,     "require": {
#        "php": "^5.3.6 || >=7.0 <7.2",
#        "ext-tokenizer": "*",
#        "symfony/console": "^2.3 || ^3.0",
#        "symfony/event-dispatcher": "^2.1 || ^3.0",
#        "symfony/filesystem": "^2.1 || ^3.0",
#        "symfony/finder": "^2.1 || ^3.0",
#        "symfony/process": "^2.3 || ^3.0",
#        "symfony/stopwatch": "^2.5 || ^3.0",
#        "sebastian/diff": "^1.1"
Requires:       php(language) >= 5.3.6
Requires:       php-tokenizer
Requires:       php-composer(symfony/console)          >= 2.3
Requires:       php-composer(symfony/event-dispatcher) >= 2.1
Requires:       php-composer(symfony/filesystem)       >= 2.1
Requires:       php-composer(symfony/finder)           >= 2.1
Requires:       php-composer(symfony/process)          >= 2.3
Requires:       php-composer(symfony/stopwatch)        >= 2.5
Requires:       php-composer(sebastian/diff)           >= 1.1
# From phpcompatinfo report for version 1.12.1
Requires:       php-cli
Requires:       php-reflection
Requires:       php-dom
Requires:       php-json
Requires:       php-pcre
Requires:       php-phar
Requires:       php-spl
Requires:       php-xml
# Autoloader
Requires:       php-composer(symfony/class-loader)

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

cp %{SOURCE2} Symfony/CS/autoload.php


%build
# Empty build section, most likely nothing required.


%install
rm -rf %{buildroot}

: Library
mkdir -p       %{buildroot}%{php_home}
cp -pr Symfony %{buildroot}%{php_home}/Symfony

: Command
install -Dpm755 %{name} %{buildroot}%{_bindir}/%{name}


%check
%if %{with_tests}
mkdir vendor
ln -s %{buildroot}%{php_home}/Symfony/CS/autoload.php vendor/

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
%{php_home}/Symfony/CS
%exclude %{php_home}/Symfony/CS/Tests
%exclude %{php_home}/Symfony/CS/Resources
%{_bindir}/%{name}


%changelog
* Fri Sep  9 2016 Remi Collet <remi@fedoraproject.org> - 1.12.1-1
- initial package, version 1.12.1

