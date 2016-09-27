# remirepo spec file for php-twig-extensions, from
#
# Fedora spec file for php-twig-extensions
#
# Copyright (c) 2014-2016 Shawn Iwinski <shawn.iwinski@gmail.com>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%global github_owner     twigphp
%global github_name      Twig-extensions
%global github_version   1.4.0
%global github_commit    531eaf4b9ab778b1d7cdd10d40fc6aa74729dfee

%global composer_vendor  twig
%global composer_project extensions

# "symfony/translation": "~2.3"
%global symfony_min_ver  2.3
%global symfony_max_ver  3.0
# "twig/twig": "~1.20|~2.0"
%global twig_min_ver     1.20
%global twig_max_ver     3.0

# Build using "--without tests" to disable tests
%global with_tests 0%{!?_without_tests:1}

%{!?phpdir:  %global phpdir  %{_datadir}/php}

Name:          php-%{composer_vendor}-%{composer_project}
Version:       %{github_version}
Release:       1%{?dist}
Summary:       Twig extensions

Group:         Development/Libraries
License:       MIT
URL:           http://twig.sensiolabs.org/doc/extensions/index.html
Source0:       https://github.com/%{github_owner}/%{github_name}/archive/%{github_commit}/%{name}-%{github_version}-%{github_commit}.tar.gz

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:     noarch
# Tests
%if %{with_tests}
BuildRequires: php-composer(phpunit/phpunit)
## composer.json
BuildRequires: php-composer(symfony/translation) >= %{symfony_min_ver}
BuildRequires: php-composer(twig/twig)           >= %{twig_min_ver}
## phpcompatinfo (computed from version 1.4.0)
BuildRequires: php-date
BuildRequires: php-mbstring
BuildRequires: php-pcre
BuildRequires: php-spl
%endif

# composer.json
Requires:      php-composer(twig/twig)           >= %{twig_min_ver}
Requires:      php-composer(twig/twig)           <  %{twig_max_ver}
# composer.json: optional
Requires:      php-composer(symfony/translation) >= %{symfony_min_ver}
Requires:      php-composer(symfony/translation) <  %{symfony_max_ver}
# phpcompatinfo (computed from version 1.4.0)
Requires:      php-mbstring
Requires:      php-pcre
Requires:      php-spl

# Composer
Provides:      php-composer(%{composer_vendor}/%{composer_project}) = %{version}

%description
Common additional features for Twig that do not directly belong in core Twig.


%prep
%setup -qn %{github_name}-%{github_commit}

: Create autoloader
cat <<'AUTOLOAD' | tee lib/Twig/Extensions/autoload.php
<?php
/**
 * Autoloader for %{name} and its' dependencies
 *
 * Created by %{name}-%{version}-%{release}
 */

require_once __DIR__ . '/Autoloader.php';
Twig_Extensions_Autoloader::register();

require_once '%{phpdir}/Twig/autoload.php';
AUTOLOAD


%build
# Empty build section, nothing required


%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{phpdir}
cp -rp lib/* %{buildroot}%{phpdir}/


%check
%if %{with_tests}
# remirepo:11
run=0
ret=0
if which php56; then
   php56 %{_bindir}/phpunit --bootstrap %{buildroot}%{phpdir}/Twig/Extensions/autoload.php || ret=1
   run=1
fi
if which php71; then
   php71 %{_bindir}/phpunit --bootstrap %{buildroot}%{phpdir}/Twig/Extensions/autoload.php || ret=1
   run=1
fi
if [ $run -eq 0 ]; then
%{_bindir}/phpunit --verbose \
    --bootstrap %{buildroot}%{phpdir}/Twig/Extensions/autoload.php
# remirepo:2
fi
exit $ret
%else
: Tests skipped
%endif


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc README.rst
%doc composer.json
%doc doc
%{phpdir}/Twig/Extensions


%changelog
* Sun Sep 25 2016 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.4.0-1
- Updated to 1.4.0 (RHBZ #1378643)

* Fri Sep 23 2016 Remi Collet <remi@fedoraproject.org> - 1.4.0-1
- update to 1.4.0

* Mon Oct 12 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.3.0-1
- Updated to 1.3.0 (RHBZ #1256169)
- "php-phpunit-PHPUnit" build dependency changed to "php-composer(phpunit/phpunit)"
- "twig/twig" dependency version changed from "~1.12" to "~1.20|~2.0"

* Fri Nov 14 2014 Remi Collet <remi@fedoraproject.org> - 1.2.0-2
- backport for remi repo, add EL-5 stuff

* Thu Nov 13 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.2.0-2
- Conditional %%{?dist}
- Removed color turn off and default timezone for phpunit
- Removed "%%dir %%{phpdir}/Twig" from %%files

* Sun Nov 02 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.2.0-1
- Initial package
