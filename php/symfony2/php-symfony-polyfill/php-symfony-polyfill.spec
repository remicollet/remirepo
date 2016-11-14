# remirepo spec file for php-symfony-polyfill
#
# Fedora spec file for php-symfony-polyfill
#
# Copyright (c) 2015-2016 Shawn Iwinski <shawn@iwin.ski>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%global github_owner     symfony
%global github_name      polyfill
%global github_version   1.3.0
%global github_commit    385d033a8e1d8778446d699ecbd886480716eba7

%global composer_vendor  symfony
%global composer_project polyfill

# "php": ">=5.3.3"
%global php_min_ver 5.3.3
# "paragonie/random_compat": "~1.0|~2.0"
%global paragonie_random_compat_min_ver 1.0
%global paragonie_random_compat_max_ver 3.0

# Build using "--without tests" to disable tests
%global with_tests 0%{!?_without_tests:1}

%{!?phpdir:  %global phpdir  %{_datadir}/php}

Name:          php-%{composer_vendor}-%{composer_project}
Version:       %{github_version}
Release:       1%{?github_release}%{?dist}
Summary:       Symfony polyfills backporting features to lower PHP versions

Group:         Development/Libraries
License:       MIT
URL:           https://github.com/%{github_owner}/%{github_name}
Source0:       %{url}/archive/%{github_commit}/%{name}-%{github_version}-%{github_commit}.tar.gz

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:     noarch
# Autoloader
BuildRequires: php-fedora-autoloader-devel
# Tests
%if %{with_tests}
BuildRequires: php-composer(phpunit/phpunit)
## composer.json
BuildRequires: php(language) >= %{php_min_ver}
BuildRequires: php-composer(ircmaxell/password-compat)
BuildRequires: php-composer(paragonie/random_compat) >= %{paragonie_random_compat_min_ver}
## phpcompatinfo (computed from version 1.3.0)
BuildRequires: php-hash
BuildRequires: php-json
BuildRequires: php-ldap
BuildRequires: php-mbstring
BuildRequires: php-pcre
BuildRequires: php-reflection
BuildRequires: php-spl
%endif

# composer.json
Requires:      php(language) >= %{php_min_ver}
Requires:      php-composer(ircmaxell/password-compat)
Requires:      php-composer(paragonie/random_compat) >= %{paragonie_random_compat_min_ver}
Requires:      php-composer(paragonie/random_compat) <  %{paragonie_random_compat_max_ver}
# phpcompatinfo (computed from version 1.3.0)
Requires:      php-hash
Requires:      php-json
Requires:      php-mbstring
Requires:      php-pcre
Requires:      php-reflection
Requires:      php-spl
# Autoloader
Requires:      php-composer(fedora/autoloader)

# Composer
Provides:      php-composer(%{composer_vendor}/%{composer_project})       = %{version}
Provides:      php-composer(%{composer_vendor}/%{composer_project}-util)  = %{version}
Provides:      php-composer(%{composer_vendor}/%{composer_project}-php54) = %{version}
Provides:      php-composer(%{composer_vendor}/%{composer_project}-php55) = %{version}
Provides:      php-composer(%{composer_vendor}/%{composer_project}-php56) = %{version}
Provides:      php-composer(%{composer_vendor}/%{composer_project}-php70) = %{version}
Provides:      php-composer(%{composer_vendor}/%{composer_project}-php71) = %{version}

%description
%{summary}.

Autoloader: %{phpdir}/Symfony/Polyfill/autoload.php


%prep
%setup -qn %{github_name}-%{github_commit}

: Docs
mkdir -p docs/{Php54,Php55,Php56,Php70,Php71,Util}
mv *.md composer.json docs/
mv src/Php54/{*.md,composer.json} docs/Php54/
mv src/Php55/{*.md,composer.json} docs/Php55/
mv src/Php56/{*.md,composer.json} docs/Php56/
mv src/Php70/{*.md,composer.json} docs/Php70/
mv src/Php71/{*.md,composer.json} docs/Php71/
mv src/Util/{*.md,composer.json}  docs/Util/

: Remove unneeded polyfills
rm -rf {src,tests}/{Apcu,Iconv,Intl,Mbstring,Xml}


%build
: Create autoloader classmap
%{_bindir}/phpab --template fedora --tolerant --output src/autoload.php src/
cat src/autoload.php

: Create autoloader
cat <<'AUTOLOAD' | tee -a src/autoload.php

\Fedora\Autoloader\Dependencies::required(array(
    __DIR__ . '/Php54/bootstrap.php',
    __DIR__ . '/Php55/bootstrap.php',
    __DIR__ . '/Php56/bootstrap.php',
    __DIR__ . '/Php70/bootstrap.php',
    __DIR__ . '/Php71/bootstrap.php',
    '%{phpdir}/password_compat/password.php',
    '%{phpdir}/random_compat/autoload.php',
));
AUTOLOAD


%install
rm -rf     %{buildroot}

: Library
mkdir -p %{buildroot}%{phpdir}/Symfony/Polyfill
cp -rp src/* %{buildroot}%{phpdir}/Symfony/Polyfill/


%check
%if %{with_tests}
# remirepo:11
run=0
ret=0
if which php56; then
   php56 %{_bindir}/phpunit --bootstrap %{buildroot}%{phpdir}/Symfony/Polyfill/autoload.php
   run=1
fi
if which php71; then
   php71 %{_bindir}/phpunit --bootstrap %{buildroot}%{phpdir}/Symfony/Polyfill/autoload.php
   run=1
fi
if [ $run -eq 0 ]; then
%{_bindir}/phpunit --verbose \
    --bootstrap %{buildroot}%{phpdir}/Symfony/Polyfill/autoload.php
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
%doc docs/*
%dir %{phpdir}/Symfony
     %{phpdir}/Symfony/Polyfill
%exclude %{phpdir}/Symfony/Polyfill/*/LICENSE


%changelog
* Mon Nov 14 2016 Remi Collet <remi@fedoraproject.org> - 1.3.0-1
- Updated to 1.3.0
- provide php-composer(symfony/polyfill-php71)
- switch to fedora/autoloader

* Thu Jun 16 2016 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.2.0-1
- Updated to 1.2.0 (RHBZ #1301791)

* Tue Apr 12 2016 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.1.1-1
- Updated to 1.1.1 (RHBZ #1301791)

* Tue Dec 29 2015 Shawn Iwinski <shawn@iwin.ski> - 1.0.1-1
- update to 1.0.1

* Mon Dec 07 2015 Shawn Iwinski <shawn@iwin.ski> - 1.0.0-3
- Fixed Util docs
- Added "%%dir %%{phpdir}/Symfony" to %%files

* Sun Dec 06 2015 Shawn Iwinski <shawn@iwin.ski> - 1.0.0-2
- Always include ALL polyfills

* Sun Dec  6 2015 Remi Collet <remi@remirepo.net> - 1.0.0-1
- provide everything for all PHP version
- add backport stuff

* Wed Nov 25 2015 Shawn Iwinski <shawn@iwin.ski> - 1.0.0-1
- Initial package
