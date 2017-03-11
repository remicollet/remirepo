# remirepo spec file for php-akamai-open-edgegrid-client, from:
#
# Fedora spec file for php-akamai-open-edgegrid-client
#
# Copyright (c) 2016 Shawn Iwinski <shawn@iwin.ski>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%global github_owner     akamai-open
%global github_name      AkamaiOPEN-edgegrid-php-client
%global github_version   1.0.0
%global github_commit    cb8ba9da0f0bf6a3fcdc12057f4fd0f5d995d6cb
%global github_prerelease beta1
%global github_release    .%{github_prerelease}

%global composer_vendor  akamai-open
%global composer_project edgegrid-client

# "php": ">=5.5"
%global php_min_ver 5.5
# "akamai-open/edgegrid-auth": "^1.0.0@beta"
%global akamai_open_edgegrid_auth_min_ver 1.0
%global akamai_open_edgegrid_auth_max_ver 2.0
# "guzzlehttp/guzzle": "^6.1.1"
%global guzzle_min_ver 6.1.1
%global guzzle_max_ver 7.0
# "monolog/monolog": "^1.15"
%global monolog_min_ver 1.15
%global monolog_max_ver 2.0
# "psr/log": "^1.0"
#     NOTE: Min version not 1.0 because autoloader required
%global psr_log_min_ver 1.0.1
%global psr_log_max_ver 2.0

# Build using "--without tests" to disable tests
%global with_tests 0%{!?_without_tests:1}

%{!?phpdir:  %global phpdir  %{_datadir}/php}

Name:          php-%{composer_vendor}-%{composer_project}
Version:       %{github_version}
Release:       0.1%{?github_release}%{?dist}
Summary:       Implements the Akamai {OPEN} EdgeGrid Authentication

Group:         Development/Libraries
License:       ASL 2.0
URL:           https://github.com/%{github_owner}/%{github_name}
Source0:       %{url}/archive/%{github_commit}/%{name}-%{github_version}-%{github_commit}.tar.gz

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:     noarch
# Autoloader
BuildRequires: php-fedora-autoloader-devel
# Library version value and autoloader check
BuildRequires: php-cli
## composer.json
BuildRequires: php-composer(akamai-open/edgegrid-auth) <  %{akamai_open_edgegrid_auth_max_ver}
BuildRequires: php-composer(akamai-open/edgegrid-auth) >= %{akamai_open_edgegrid_auth_min_ver}
BuildRequires: php-composer(guzzlehttp/guzzle) <  %{guzzle_max_ver}
BuildRequires: php-composer(guzzlehttp/guzzle) >= %{guzzle_min_ver}
BuildRequires: php-composer(monolog/monolog) <  %{monolog_max_ver}
BuildRequires: php-composer(monolog/monolog) >= %{monolog_min_ver}
BuildRequires: php-composer(psr/log) <  %{psr_log_max_ver}
BuildRequires: php-composer(psr/log) >= %{psr_log_min_ver}
# Tests
%if %{with_tests}
## composer.json
BuildRequires: php(language) >= %{php_min_ver}
BuildRequires: php-composer(phpunit/phpunit)
## phpcompatinfo (computed from version 1.0.0beta1)
BuildRequires: php-json
BuildRequires: php-pcre
BuildRequires: php-reflection
%endif

# composer.json
Requires:      php(language) >= %{php_min_ver}
Requires:      php-composer(akamai-open/edgegrid-auth) <  %{akamai_open_edgegrid_auth_max_ver}
Requires:      php-composer(akamai-open/edgegrid-auth) >= %{akamai_open_edgegrid_auth_min_ver}
Requires:      php-composer(guzzlehttp/guzzle) <  %{guzzle_max_ver}
Requires:      php-composer(guzzlehttp/guzzle) >= %{guzzle_min_ver}
Requires:      php-composer(monolog/monolog) <  %{monolog_max_ver}
Requires:      php-composer(monolog/monolog) >= %{monolog_min_ver}
Requires:      php-composer(psr/log) <  %{psr_log_max_ver}
Requires:      php-composer(psr/log) >= %{psr_log_min_ver}
# phpcompatinfo (computed from version 1.0.0beta1)
Requires:      php-json
Requires:      php-pcre
# Autoloader
Requires:      php-composer(fedora/autoloader)

# Composer
Provides:      php-composer(%{composer_vendor}/%{composer_project}) = %{version}

%description
Akamai {OPEN} EdgeGrid Authentication [1] Client for PHP

This library implements the Akamai {OPEN} EdgeGrid Authentication scheme on top
of Guzzle [2], as both a drop-in replacement client, and middleware.

For more information visit the Akamai {OPEN} Developer Community [3].

Autoloader: %{phpdir}/Akamai/Open/EdgeGrid/autoload-client.php

[1] https://developer.akamai.com/introduction/Client_Auth.html
[2] https://github.com/guzzle/guzzle
[3] https://developer.akamai.com/


%prep
%setup -qn %{github_name}-%{github_commit}

: Remove CLI
rm -f src/Cli.php


%build
: Create autoloader
%{_bindir}/phpab --template fedora --output src/autoload-client.php src/

cat <<'AUTOLOAD' | tee -a src/autoload-client.php

\Fedora\Autoloader\Dependencies::required(array(
    '%{phpdir}/Akamai/Open/EdgeGrid/autoload-auth.php',
    '%{phpdir}/GuzzleHttp6/autoload.php',
    '%{phpdir}/Monolog/autoload.php',
    '%{phpdir}/Psr/Log/autoload.php',
));
AUTOLOAD


%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{phpdir}/Akamai/Open
cp -rp src %{buildroot}%{phpdir}/Akamai/Open/EdgeGrid


%check
: Library version value and autoloader check
%{_bindir}/php -r '
    require_once "%{buildroot}%{phpdir}/Akamai/Open/EdgeGrid/autoload-client.php";
    $version = \Akamai\Open\EdgeGrid\Client::VERSION;
    echo "Version $version (expected %{version}%{?github_prerelease})\n";
    exit(version_compare("%{version}%{?github_prerelease}", "$version", "=") ? 0 : 1);
'

%if %{with_tests}
: Create tests bootstrap
cat <<'BOOTSTRAP' | tee bootstrap.php
<?php
require_once '%{buildroot}%{phpdir}/Akamai/Open/EdgeGrid/autoload-client.php';
\Fedora\Autoloader\Autoload::addPsr4('Akamai\\Open\\EdgeGrid\\Tests\\', __DIR__.'/tests');
BOOTSTRAP

: Upstream tests
RETURN_CODE=0
for PHP_EXEC in php php56 php70 php71; do
    if which $PHP_EXEC; then
       $PHP_EXEC %{_bindir}/phpunit --bootstrap bootstrap.php || RETURN_CODE=1
    fi
done
exit $RETURN_CODE
%else
: Tests skipped
%endif


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc *.md
%doc composer.json
%{phpdir}/Akamai/Open/EdgeGrid/autoload-client.php
%{phpdir}/Akamai/Open/EdgeGrid/Client.php
%{phpdir}/Akamai/Open/EdgeGrid/Exception
%{phpdir}/Akamai/Open/EdgeGrid/Exception.php
%{phpdir}/Akamai/Open/EdgeGrid/Handler


%changelog
* Sat Mar 11 2017 Shawn Iwinski <shawn@iwin.ski> - 1.0.0-0.1.beta1
- Update to 1.0.0beta1 (RHBZ #1408816)
- Added max versions to BuildRequires dependencies
- Removed compat autoloader

* Tue Dec 27 2016 Remi Collet <remi@remirepo.net> - 0.6.4-1
- update to 0.6.4 (no change)

* Mon Dec 26 2016 Shawn Iwinski <shawn@iwin.ski> - 0.6.3-1
- Update to 0.6.3 (RHBZ #1408612)

* Sun Dec 25 2016 Remi Collet <remi@remirepo.net> - 0.6.3-1
- update to 0.6.3

* Sat Dec 24 2016 Shawn Iwinski <shawn@iwin.ski> - 0.6.2-2
- Minor spec-only modifications

* Thu Dec 22 2016 Remi Collet <remi@remirepo.net> - 0.6.2-1
- update to 0.6.2
- Use php-composer(fedora/autoloader)

* Wed Dec 07 2016 Shawn Iwinski <shawn@iwin.ski> - 0.6.1-1
- Updated to 0.6.1 (RHBZ #1392697)

* Wed Nov 02 2016 Shawn Iwinski <shawn@iwin.ski> - 0.6.0-1
- Updated to 0.6.0 (RHBZ #1382986)
- Autoloader changed from Symfony ClassLoader to phpab classmap

* Sun Sep 25 2016 Shawn Iwinski <shawn@iwin.ski> - 0.5.0-1
- Updated to 0.5.0 (RHBZ #1376273)

* Sun Sep 11 2016 Shawn Iwinski <shawn@iwin.ski> - 0.4.6-1
- Updated to 0.4.6 (RHBZ #1371149)

* Sat Jul 23 2016 Shawn Iwinski <shawn@iwin.ski> - 0.4.5-1
- Updated to 0.4.5 (RHBZ #1333785)
- Added library version value and autoloader check

* Fri Apr 15 2016 Remi Collet <remi@remirepo.net> - 0.4.4-1
- backport for remi repository

* Tue Apr 12 2016 Shawn Iwinski <shawn@iwin.ski> - 0.4.4-1
- Initial package
