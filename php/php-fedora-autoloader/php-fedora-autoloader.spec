#
# Fedora spec file for php-fedora-autoloader
#
# Copyright (c) 2016 Shawn Iwinski <shawn@iwin.ski>
#                    Remi Collet <remi@fedoraproject.org>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%global github_owner     php-fedora
%global github_name      autoloader
%global github_version   0.1.1
%global github_commit    816e4e59061c592f7480a00c6cd9c16067811c1e

%global composer_vendor  fedora
%global composer_project autoloader

# "php": ">= 5.3.3"
%global php_min_ver 5.3.3
# "theseer/autoload": "^1.22"
%global phpab_min_ver 1.22
%global phpab_max_ver 2.0

# Build using "--without tests" to disable tests
%global with_tests 0%{!?_without_tests:1}

%{!?phpdir:  %global phpdir  %{_datadir}/php}
%global  phpab_template_dir  %{phpdir}/TheSeer/Autoload/templates/ci

Name:          php-%{composer_vendor}-%{composer_project}
Version:       %{github_version}
Release:       1%{?github_release}%{?dist}
Summary:       Fedora Autoloader

Group:         Development/Libraries
License:       MIT
URL:           https://github.com/%{github_owner}/%{github_name}
Source0:       %{url}/archive/%{github_commit}/%{name}-%{github_version}-%{github_commit}.tar.gz

BuildArch:     noarch
# Tests
%if %{with_tests}
## composer.json
BuildRequires: php(language) >= %{php_min_ver}
BuildRequires: php-composer(phpunit/phpunit)
BuildRequires: php-composer(theseer/autoload) >= %{phpab_min_ver}
## phpcompatinfo (computed from version 0.1.0)
BuildRequires: php-spl
%endif

# composer.json
Requires:      php(language) >= %{php_min_ver}
# phpcompatinfo (computed from version 0.1.0)
Requires:      php-spl

# Composer
Provides:      php-composer(%{composer_vendor}/%{composer_project}) = %{version}

%description
Static PSR-4 [1], PSR-0 [2], and classmap autoloader.  Includes loader for
required and optional dependencies.

[1] http://www.php-fig.org/psr/psr-4/
[2] http://www.php-fig.org/psr/psr-0/

# ------------------------------------------------------------------------------


%package devel

Summary: %{name} devel

Requires: %{name} = %{version}-%{release}
Requires: php-composer(theseer/autoload) >= %{phpab_min_ver}
Requires: php-composer(theseer/autoload) <  %{phpab_max_ver}

%description devel
Provides needed tools to build other packages:
- phpab fedora template


# ------------------------------------------------------------------------------


%prep
%setup -qn %{github_name}-%{github_commit}

: Set PHP directory in phpab template
sed "s#___AUTOLOAD_PATH___#'%{phpdir}/Fedora/Autoloader'#" \
    -i res/phpab/fedora.php.tpl


%build
# Empty build section, nothing to build


%install
: Main
mkdir -p %{buildroot}%{phpdir}/Fedora/Autoloader/Test
cp -rp src/* %{buildroot}%{phpdir}/Fedora/Autoloader/
cp -rp tests/* %{buildroot}%{phpdir}/Fedora/Autoloader/Test/

: Devel
mkdir -p %{buildroot}%{phpab_template_dir}
cp -p res/phpab/fedora.php.tpl %{buildroot}%{phpab_template_dir}/


%check
%if %{with_tests}
%{_bindir}/phpunit --verbose
%else
: Tests skipped
%endif


%files
%{!?_licensedir:%global license %%doc}
%license LICENSE
%dir %{phpdir}/Fedora
     %{phpdir}/Fedora/Autoloader
%exclude %{phpdir}/Fedora/Autoloader/Test

%files devel
%doc *.md
%doc composer.json
%{phpab_template_dir}/fedora.php.tpl


%changelog
* Wed Oct 19 2016 Shawn Iwinski <shawn@iwin.ski> - 0.1.1-1
- Update to 0.1.1
- Fix phpab template
- Move docs to devel subpackage

* Wed Oct 19 2016 Shawn Iwinski <shawn@iwin.ski> - 0.1.0-1
- Initial package
