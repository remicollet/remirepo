# remirepo spec file for php-PsrLog, from Fedora:
#
# Fedora spec file for php-PsrLog
#
# Copyright (c) 2013-2016 Shawn Iwinski <shawn.iwinski@gmail.com>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve the changelog entries
#

%global github_owner     php-fig
%global github_name      log
%global github_version   1.0.2
%global github_commit    4ebe3a8bf773a19edfe0a84b6585ba3d401b724d

%global composer_vendor  psr
%global composer_project log

%{!?phpdir:  %global phpdir  %{_datadir}/php}

Name:      php-PsrLog
Version:   %{github_version}
Release:   2%{?dist}
Summary:   Common interface for logging libraries

Group:     Development/Libraries
License:   MIT
URL:       http://www.php-fig.org/psr/psr-3/
Source0:   https://github.com/%{github_owner}/%{github_name}/archive/%{github_commit}/%{name}-%{github_version}-%{github_commit}.tar.gz

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch
# For tests
BuildRequires:  php-cli
# Autoloader
BuildRequires:  php-composer(fedora/autoloader)

Requires:  php(language) >= 5.3.0
# phpcompatinfo requires (computed from version 1.0.1)
Requires:  php-date
Requires:  php-spl
# Autoloader
Requires:  php-composer(fedora/autoloader)

# php-{COMPOSER_VENDOR}-{COMPOSER_PROJECT}
Provides:  php-%{composer_vendor}-%{composer_project}           = %{version}-%{release}
# Composer
Provides:  php-composer(%{composer_vendor}/%{composer_project}) = %{version}


%description
This package holds all interfaces/classes/traits related to PSR-3 [1].

Note that this is not a logger of its own. It is merely an interface that
describes a logger. See the specification for more details.

[1] http://www.php-fig.org/psr/psr-3/


%prep
%setup -qn %{github_name}-%{github_commit}

: Create autoloader
cat <<'AUTOLOAD' | tee Psr/Log/autoload.php
<?php
/**
 * Autoloader for %{name} and its' dependencies
 * (created by %{name}-%{version}-%{release}).
 *
 * @return \Symfony\Component\ClassLoader\ClassLoader
 */

if (!class_exists('Fedora\\Autoloader\\Autoload', false)) {
    require_once '%{phpdir}/Fedora/Autoloader/autoload.php';
}

\Fedora\Autoloader\Autoload::addPsr4('Psr\\Log\\', __DIR__);
AUTOLOAD


%check
: Check if our autoloader works
php -r '
require "%{buildroot}%{_datadir}/php/Psr/Log/autoload.php";
$a = new Psr\Log\NullLogger();
echo "Ok\n";
exit(0);
'


%build
# Empty build section, nothing to build


%install
mkdir -p %{buildroot}%{_datadir}/php
cp -rp Psr %{buildroot}%{_datadir}/php/


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc README.md
%doc composer.json
%dir %{_datadir}/php/Psr
     %{_datadir}/php/Psr/Log


%changelog
* Fri Oct 21 2016 Remi Collet <remi@fedoraproject.org> - 1.0.2-2
- switch from symfony/class-loader to fedora/autoloader
- add minimal %%check for autoloader

* Mon Oct 10 2016 Remi Collet <remi@fedoraproject.org> 1.0.2-1
- update to 1.0.2

* Sun Sep 25 2016 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.0.1-1
- Updated to 1.0.1 (RHBZ #1377513)

* Mon Sep 19 2016 Remi Collet <remi@fedoraproject.org> 1.0.1-1
- update to 1.0.1

* Wed Jan 20 2016 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.0.0-9
- Added php-{COMPOSER_VENDOR}-{COMPOSER_PROJECT} ("php-psr-log") virtual provide
- %%license usage

* Mon Nov 16 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.0.0-8
- Added autoloader

* Sun Jun  8 2014 Remi Collet <remi@fedoraproject.org> 1.0.0-6
- backport rawhide changes.

* Sat Jun 07 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.0.0-6
- Replaced single-use %%composer_vendor and %%composer_project

* Sat Jun  7 2014 Remi Collet <remi@fedoraproject.org> 1.0.0-5
- backport rawhide changes.

* Fri Jun 06 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.0.0-5
- Updated URL
- Requires php-common => php(language)
- Added php-composer(%%{composer_vendor}/%%{composer_project}) virtual provide

* Wed Jan 23 2013 Remi Collet <remi@fedoraproject.org> 1.0.0-2
- backport 1.0.0 for remi repo.

* Tue Jan 22 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 1.0.0-2
- Updated URL
- Added php-date require

* Thu Jan 10 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 1.0.0-1
- Initial package
