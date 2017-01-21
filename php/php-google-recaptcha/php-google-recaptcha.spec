# remirepo/fedora spec file for php-google-recaptcha
#
# Copyright (c) 2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    2b7e00566afca82a38a1d3adb8e42c118006296e
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     google
%global gh_project   recaptcha
%global with_tests   0%{!?_without_tests:1}
%global psr0         ReCaptcha

Name:           php-%{gh_owner}-%{gh_project}
Version:        1.1.2
Release:        1%{?dist}
Summary:        reCAPTCHA PHP client library

Group:          Development/Libraries
License:        BSD
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        %{url}/archive/%{gh_commit}/%{name}-%{version}-%{?gh_short}.tar.gz

BuildArch:      noarch
%if %{with_tests}
BuildRequires:  php(language) >= 5.3.2
BuildRequires:  php-curl
BuildRequires:  php-json
BuildRequires:  php-pcre
BuildRequires:  php-spl
# For tests, from composer.json "require-dev": {
#        "phpunit/phpunit": "4.5.*"
BuildRequires:  php-composer(phpunit/phpunit) >= 4.5
%endif
# For autoloader
BuildRequires:  php-composer(fedora/autoloader)

# From composer.json, "require": {
#        "php": ">=5.3.2"
Requires:       php(language) >= 5.3.2
# From phpcompatinfo report for 1.1.2
Requires:       php-curl
Requires:       php-json
Requires:       php-pcre
Requires:       php-spl
# For generated autoloader
Requires:       php-composer(fedora/autoloader)

# Composer
Provides:       php-composer(%{gh_owner}/%{gh_project}) = %{version}


%description
reCAPTCHA PHP client library.

reCAPTCHA is a free CAPTCHA service that protect websites from spam and abuse.
This is Google authored code that provides plugins for third-party integration
with reCAPTCHA.

Autoloader: %{_datadir}/php/%{psr0}/autoload.php


%prep
%setup -q -n %{gh_project}-%{gh_commit}
rm src/autoload.php


%build
: Create autoloader
cat <<'AUTOLOAD' | tee src/%{psr0}/autoload.php
<?php
/* Autoloader for %{name} and its dependencies */
require_once '%{_datadir}/php/Fedora/Autoloader/autoload.php';

\Fedora\Autoloader\Autoload::addPsr4('%{psr0}\\', __DIR__);
AUTOLOAD


%install
: Library
mkdir -p           %{buildroot}%{_datadir}/php
cp -pr src/%{psr0} %{buildroot}%{_datadir}/php/%{psr0}


%check
%if %{with_tests}
BOOTSTRAP=%{buildroot}%{_datadir}/php/%{psr0}/autoload.php

# remirepo:11
run=0
ret=0
if which php56; then
   php56 %{_bindir}/phpunit --bootstrap=$BOOTSTRAP || ret=1
   run=1
fi
if which php71; then
   php71 %{_bindir}/phpunit --bootstrap=$BOOTSTRAP || ret=1
   run=1
fi
if [ $run -eq 0 ]; then
%{_bindir}/phpunit  --bootstrap=$BOOTSTRAP --verbose
# remirepo:2
fi
exit $ret
%else
: Test suite disabled
%endif


%files
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc composer.json
%doc *.md
%{_datadir}/php/%{psr0}


%changelog
* Sat Jan 21 2017 Remi Collet <remi@remirepo.net> - 1.1.2-1
- initial package

