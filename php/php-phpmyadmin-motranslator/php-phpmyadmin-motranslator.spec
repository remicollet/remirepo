# remirepo/fedora spec file for php-phpmyadmin-motranslator
#
# Copyright (c) 2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#

##TODO next version will have tests back

%global gh_commit    b5d5f9a0c1f6ed1127e7b766b3b506766becbb89
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     phpmyadmin
%global gh_project   motranslator
%global with_tests   0%{!?_without_tests:1}
%global ns_vendor    PhpMyAdmin
%global ns_project   MoTranslator

Name:           php-%{gh_owner}-%{gh_project}
Version:        3.0
Release:        1%{?dist}
Summary:        Translation API for PHP using Gettext MO files

Group:          Development/Libraries
License:        GPLv2+
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{name}-%{version}-%{?gh_short}.tar.gz

BuildArch:      noarch
%if %{with_tests}
BuildRequires:  php(language) >= 5.3
BuildRequires:  php-pcre
BuildRequires:  php-composer(symfony/expression-language) <  3
BuildRequires:  php-composer(symfony/expression-language) >= 2.8
# For tests, from composer.json "require-dev": {
#        "phpunit/phpunit": "~4.8 || ~5.1"
BuildRequires:  php-composer(phpunit/phpunit) >= 4.8
%endif
# For autoloader
BuildRequires:  php-composer(fedora/autoloader)

# From composer.json, "require": {
#        "php": ">=5.3.0",
#        "symfony/expression-language": "^3.1 || ^2.8"
Requires:       php-composer(symfony/expression-language) <  3
Requires:       php-composer(symfony/expression-language) >= 2.8
Requires:       php(language) >= 5.3
# From phpcompatinfo report for 1.2
Requires:       php-pcre
# For generated autoloader
Requires:       php-composer(fedora/autoloader)

# Composer
Provides:       php-composer(%{gh_owner}/%{gh_project}) = %{version}


%description
Translation API for PHP using Gettext MO files.

Features

* All strings are stored in memory for fast lookup
* Fast loading of MO files
* Low level API for reading MO files
* Emulation of Gettext API
* No use of eval() for plural equation

Limitations

* Not suitable for huge MO files which you don't want to store in memory
* Input and output encoding has to match (preferably UTF-8)

Autoloader: %{_datadir}/php/%{ns_vendor}/%{ns_project}/autoload.php


%prep
%setup -q -n %{gh_project}-%{gh_commit}


%build
: Create autoloader
cat <<'AUTOLOAD' | tee src/autoload.php
<?php
/* Autoloader for %{name} and its dependencies */
require_once '%{_datadir}/php/Fedora/Autoloader/autoload.php';

\Fedora\Autoloader\Autoload::addPsr4('%{ns_vendor}\\%{ns_project}\\', __DIR__);
\Fedora\Autoloader\Dependencies::required(array(
    '%{_datadir}/php/Symfony/Component/ExpressionLanguage/autoload.php'
));
AUTOLOAD


%install
: Library
mkdir -p   %{buildroot}%{_datadir}/php/%{ns_vendor}
cp -pr src %{buildroot}%{_datadir}/php/%{ns_vendor}/%{ns_project}


%check
%if %{with_tests}
mkdir vendor
cat << 'EOF' | tee vendor/autoload.php
<?php
require '%{buildroot}%{_datadir}/php/%{ns_vendor}/%{ns_project}/autoload.php';
EOF

# remirepo:11
run=0
ret=0
if which php56; then
   php56 %{_bindir}/phpunit --no-coverage || ret=1
   run=1
fi
if which php71; then
   php71 %{_bindir}/phpunit --no-coverage || ret=1
   run=1
fi
if [ $run -eq 0 ]; then
%{_bindir}/phpunit --no-coverage --verbose
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
%dir %{_datadir}/php/%{ns_vendor}/
     %{_datadir}/php/%{ns_vendor}/%{ns_project}


%changelog
* Mon Jan 23 2017 Remi Collet <remi@remirepo.net> - 3.0-1
- update to 3.0 with vendor namespace

* Sat Jan 21 2017 Remi Collet <remi@remirepo.net> - 2.2-1
- initial package

