# remirepo/fedora spec file for php-jeremeamia-superclosure
#
# Copyright (c) 2015-2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
# Github
%global gh_commit    443c3df3207f176a1b41576ee2a66968a507b3db
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     jeremeamia
%global gh_project   super_closure
# Packagist
%global pk_vendor    jeremeamia
%global pk_name      superclosure
# PSR-0 namespace
%global namespace    SuperClosure

Name:           php-%{pk_vendor}-%{pk_name}
Version:        2.3.0
Release:        1%{?dist}
Summary:        Serialize Closure objects, including their context and binding

Group:          Development/Libraries
License:        MIT
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        %{name}-%{version}-%{gh_short}.tgz
# Create git snapshot as tests are excluded from official tarball
Source1:        makesrc.sh
# Autoloader
Source2:        %{name}-autoload.php

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php(language) >= 5.4
BuildRequires:  php-composer(nikic/php-parser) >= 1.4
BuildRequires:  php-composer(symfony/polyfill-php56) >= 1.0
# From composer.json, "require-dev": {
#        "phpunit/phpunit": "^4.0|^5.0",
BuildRequires:  php-composer(phpunit/phpunit)  >= 4.0
# Autoloader
BuildRequires:  php-composer(fedora/autoloader)

# From composer.json, "require": {
#        "php": ">=5.4",
#        "nikic/php-parser": "^1.2|^2.0|^3.0",
#        "symfony/polyfill-php56": "^1.0"
# php-parser 1.4 for autoloader
Requires:       php(language) >= 5.4
Requires:       php-composer(nikic/php-parser) >= 1.4
Requires:       php-composer(nikic/php-parser) <  4
Requires:       php-composer(symfony/polyfill-php56) >= 1.0
Requires:       php-composer(symfony/polyfill-php56) <  2
# From phpcompatifo report for 2.1.0
Requires:       php-hash
Requires:       php-reflection
Requires:       php-spl
Requires:       php-tokenizer
# Autoloader
Requires:       php-composer(fedora/autoloader)

Provides:       php-composer(%{pk_vendor}/%{pk_name}) = %{version}


%description
Even though serializing closures is "not allowed" by PHP,
the SuperClosure library makes it possible

To use this library, you just have to add, in your project:
  require-once '%{_datadir}/php/%{namespace}/autoload.php';


%prep
%setup -q -n %{gh_project}-%{gh_commit}
install -pm 644 %{SOURCE2} src/autoload.php


%build
# Nothing


%install
rm -rf     %{buildroot}
# Restore PSR-0 tree
mkdir -p   %{buildroot}%{_datadir}/php
cp -pr src %{buildroot}%{_datadir}/php/%{namespace}


%check
mkdir vendor
cat << 'EOF' | tee vendor/autoload.php
<?php
require '%{buildroot}%{_datadir}/php/%{namespace}/autoload.php';
require dirname(__DIR__) . '/tests/Integ/Fixture/Collection.php';
require dirname(__DIR__) . '/tests/Integ/Fixture/Foo.php';
EOF

: Run the test suite
# remirepo:11
ret=0
run=0
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
# remirepo:1
fi


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE.md
%doc README.md composer.json
%{_datadir}/php/%{namespace}


%changelog
* Wed Dec  7 2016 Remi Collet <remi@fedoraproject.org> - 2.3.0-1
- update to 2.3.0
- switch to fedora/autoloader
- allow nikic/php-parser v3

* Sat May 21 2016 Remi Collet <remi@fedoraproject.org> - 2.2.0-3
- use nikic/php-parser v2 when available

* Sun Dec  6 2015 Remi Collet <remi@fedoraproject.org> - 2.2.0-1
- update to 2.2.0
- run test suite with both php 5 and 7 when available
- add dependency on symfony/polyfill-php56

* Tue Sep  1 2015 Remi Collet <remi@fedoraproject.org> - 2.1.0-1
- initial package
