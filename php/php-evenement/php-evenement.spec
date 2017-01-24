# remirepo spec file for php-evenement, from:
#
# Fedora spec file for php-evenement
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#
Name:       php-evenement
Version:    2.0.0
Release:    3%{?dist}
BuildArch:  noarch

License:    MIT
Summary:    Événement is a very simple event dispatching library for PHP
URL:        https://github.com/igorw/evenement
Source0:    %{url}/archive/v%{version}.tar.gz
# https://github.com/igorw/evenement/pull/33
Patch0:     0000-Fix-a-test-to-catch-TypeError-instead-of-Exception.patch

BuildRequires: phpunit
BuildRequires: php-composer(fedora/autoloader)

Requires:      php(language) >= 5.4.0
# This is for the autoloader
Requires:      php-composer(fedora/autoloader)

Provides:      php-composer(evenement/evenement) = %{version}


%description
Événement is a very simple event dispatching library for PHP.

It has the same design goals as Silex and Pimple, to empower the user
while staying concise and simple.

It is very strongly inspired by the EventEmitter API found in node.js.

Autoloader:    %{_datadir}/php/Evenement/autoload.php


%prep
%setup -q -n evenement-%{version}

%patch0 -p1

: Create autoloader
cat <<'AUTOLOAD' | tee src/Evenement/autoload.php
<?php
/**
 * Autoloader for %{name} and its' dependencies
 * (created by %{name}-%{version}-%{release}).
 */
require_once '%{_datadir}/php/Fedora/Autoloader/autoload.php';

\Fedora\Autoloader\Autoload::addPsr4('Evenement\\', __DIR__);
AUTOLOAD


%install
install -d -p -m 0755 %{buildroot}/%{_datadir}/php

cp -a -r src/Evenement %{buildroot}/%{_datadir}/php/


%check
: Create tests autoloader
cat <<'AUTOLOAD' | tee autoload.php
<?php
require_once '%{buildroot}%{_datadir}/php/Evenement/autoload.php';
\Fedora\Autoloader\Autoload::addPsr4('Evenement\\Tests\\', __DIR__.'/tests/Evenement/Tests');
AUTOLOAD

# remirepo:11
run=0
ret=0
if which php56; then
   php56 %{_bindir}/phpunit --bootstrap autoload.php || ret=1
   run=1
fi
if which php71; then
   php71 %{_bindir}/phpunit --bootstrap autoload.php || ret=1
   run=1
fi
if [ $run -eq 0 ]; then
phpunit --bootstrap autoload.php
# remirepo:2
fi
exit $ret


%files
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc CHANGELOG.md composer.json README.md
%{_datadir}/php/Evenement


%changelog
* Tue Jan 24 2017 Remi Collet <remi@remirepo.net> - 2.0.0-3
- backport for remi repo

* Tue Jan 24 2017 Randy Barlow <bowlofeggs@fedoraproject.org> - 2.0.0-3
- Update the patch to work for PHP 5 and PHP 7.

* Tue Jan 17 2017 Shawn Iwinski <shawn@iwin.ski> - 2.0.0-2
- Use php-composer(fedora/autoloader) instead of php-composer(symfony/class-loader)
- Install to %%{_datadir}/php/Evenement instead of %%{_datadir}/php/Evenement/Evenement

* Sat Jan 14 2017 Randy Barlow <bowlofeggs@fedoraproject.org> - 2.0.0-1
- Initial release.
