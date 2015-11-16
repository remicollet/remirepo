# remirepo spec file for php-PsrLog, from Fedora:
#
# RPM spec file for php-PsrLog
#
# Copyright (c) 2013-2015 Shawn Iwinski <shawn.iwinski@gmail.com>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve the changelog entries
#

%global github_owner   php-fig
%global github_name    log
%global github_version 1.0.0
%global github_commit  fe0936ee26643249e916849d48e3a51d5f5e278b

%{!?phpdir:  %global phpdir  %{_datadir}/php}

Name:      php-PsrLog
Version:   %{github_version}
Release:   8%{?dist}
Summary:   Common interface for logging libraries

Group:     Development/Libraries
License:   MIT
URL:       http://www.php-fig.org/psr/psr-3/
Source0:   https://github.com/%{github_owner}/%{github_name}/archive/%{github_commit}/%{name}-%{github_version}-%{github_commit}.tar.gz

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch

Requires:  php(language) >= 5.3.0
# phpcompatinfo requires (computed from version 1.0.0)
Requires:  php-date
Requires:  php-spl

Provides:  php-composer(psr/log) = %{version}

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
 * (created by %{name}-%{version}-%{release})
 *
 * @return \Symfony\Component\ClassLoader\ClassLoader
 */

if (!isset($fedoraClassLoader) || !($fedoraClassLoader instanceof \Symfony\Component\ClassLoader\ClassLoader)) {
    if (!class_exists('Symfony\\Component\\ClassLoader\\ClassLoader', false)) {
        require_once '%{phpdir}/Symfony/Component/ClassLoader/ClassLoader.php';
    }

    $fedoraClassLoader = new \Symfony\Component\ClassLoader\ClassLoader();
    $fedoraClassLoader->register();
}

$fedoraClassLoader->addPrefix('Psr\\Log\\', dirname(dirname(__DIR__)));

return $fedoraClassLoader;
AUTOLOAD


%build
# Empty build section, nothing to build


%install
mkdir -pm 0755 %{buildroot}%{_datadir}/php
cp -rp Psr %{buildroot}%{_datadir}/php/


%files
%defattr(-,root,root,-)
%doc LICENSE README.md composer.json
%dir %{_datadir}/php/Psr
     %{_datadir}/php/Psr/Log


%changelog
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
