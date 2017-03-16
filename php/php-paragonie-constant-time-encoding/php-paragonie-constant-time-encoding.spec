# remirepo spec file for php-paragonie-constant-time-encoding, from:
#
# Fedora spec file for php-paragonie-constant-time-encoding
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#
%global composer_vendor         paragonie
%global composer_project        constant_time_encoding
%global composer_namespace      ParagonIE/ConstantTime

%global github_owner            paragonie
%global github_name             constant_time_encoding

%global commit0 d96e63b79a7135a65659ba5b1cb02826172bfedd
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})


Name:       php-%{composer_vendor}-constant-time-encoding
Version:    1.0.1
Release:    4%{?dist}
Summary:    Constant-Time Character Encoding in PHP Projects

Group:      System Environment/Libraries
License:    MIT

URL:        https://github.com/%{github_owner}/%{github_name}
Source0:    %{url}/archive/%{commit0}.tar.gz#/%{name}-%{shortcommit0}.tar.gz

BuildArch:  noarch

BuildRequires:  php(language) >= 5.3.0
BuildRequires:  php-mbstring
BuildRequires:  php-spl
BuildRequires:  php-pcre
BuildRequires:  php-composer(fedora/autoloader)
BuildRequires:  php-composer(paragonie/random_compat)
BuildRequires:  %{_bindir}/phpunit

Requires:   php(language) >= 5.3.0
Requires:   php-mbstring
Requires:   php-spl
Requires:   php-composer(fedora/autoloader)

Provides:   php-composer(%{composer_vendor}/%{composer_project}) = %{version}

%description
Based on the constant-time base64 implementation made by Steve "Sc00bz" 
Thomas, this library aims to offer character encoding functions that do not 
leak information about what you are encoding/decoding via processor cache 
misses.

%prep
%setup -n %{github_name}-%{commit0}

%build
cat <<'AUTOLOAD' | tee src/autoload.php
<?php
require_once '%{_datadir}/php/Fedora/Autoloader/autoload.php';

\Fedora\Autoloader\Autoload::addPsr4('ParagonIE\\ConstantTime\\', __DIR__);
AUTOLOAD

%install
mkdir -p %{buildroot}%{_datadir}/php/%{composer_namespace}
cp -pr src/* %{buildroot}%{_datadir}/php/%{composer_namespace}

%check
mkdir vendor
cat << 'EOF' | tee vendor/autoload.php
<?php
require_once '%{buildroot}%{_datadir}/php/%{composer_namespace}/autoload.php';
require_once '%{_datadir}/php/random_compat/autoload.php';
EOF

ret=0
for cmd in php php56 php70 php71; do
  if which $cmd; then
    $cmd %{_bindir}/phpunit --no-coverage --verbose || ret=1
  fi
done
exit $ret


%files
%dir %{_datadir}/php/ParagonIE
%{_datadir}/php/%{composer_namespace}
%doc README.md composer.json
%{!?_licensedir:%global license %%doc}
%license LICENSE.txt

%changelog
* Thu Mar 16 2017 Remi Collet <remi@remirepo.net> - 1.0.1-4
- backport for remi repository

* Wed Mar 15 2017 François Kooman <fkooman@tuxed.net> - 1.0.1-4
- own parent directory
- remove Requires paragonie/random_compat, only needed for build
- BuildRequire php-pcre
- rework check autoloader

* Mon Mar 13 2017 François Kooman <fkooman@tuxed.net> - 1.0.1-3
- better follow SourceURL package guidelines for GH

* Mon Feb 13 2017 François Kooman <fkooman@tuxed.net> - 1.0.1-2
- add random_compat as dependency to be able to run tests on PHP < 7

* Mon Feb 13 2017 François Kooman <fkooman@tuxed.net> - 1.0.1-1
- initial package
