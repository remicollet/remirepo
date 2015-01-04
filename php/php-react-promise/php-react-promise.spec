#
# RPM spec file for php-react-promise
#
# Copyright (c) 2014-2015 Shawn Iwinski <shawn.iwinski@gmail.com>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%global github_owner     reactphp
%global github_name      promise
%global github_version   2.2.0
%global github_commit    365fcee430dfa4ace1fbc75737ca60ceea7eeeef

%global composer_vendor  react
%global composer_project promise

# "php": ">=5.4.0"
%global php_min_ver 5.4.0

# Build using "--without tests" to disable tests
%global with_tests %{?_without_tests:0}%{!?_without_tests:1}

%{!?phpdir:     %global phpdir     %{_datadir}/php}
%{!?__phpunit:  %global __phpunit  %{_bindir}/phpunit}

Name:          php-%{composer_vendor}-%{composer_project}
Version:       %{github_version}
Release:       1%{?github_release}%{?dist}
Summary:       A lightweight implementation of CommonJS Promises/A for PHP

Group:         Development/Libraries
License:       MIT
URL:           https://github.com/%{github_owner}/%{github_name}
Source0:       %{url}/archive/%{github_commit}/%{name}-%{github_version}-%{github_commit}.tar.gz

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:     noarch
%if %{with_tests}
BuildRequires: %{__phpunit}
# composer.json
BuildRequires: php(language) >= %{php_min_ver}
# phpcompatinfo (computed from version 2.2.0)
BuildRequires: php-json
BuildRequires: php-reflection
BuildRequires: php-spl
%endif

# composer.json
Requires:      php(language) >= %{php_min_ver}
# phpcompatinfo (computed from version 2.2.0)
Requires:      php-json
Requires:      php-reflection
Requires:      php-spl

# Composer
Provides:      php-composer(%{composer_vendor}/%{composer_project}) = %{version}

%description
A lightweight implementation of CommonJS Promises/A [1] for PHP.

[1] http://wiki.commonjs.org/wiki/Promises/A


%prep
%setup -qn %{github_name}-%{github_commit}


%build
# Empty build section, nothing required


%install
rm -rf %{buildroot}
mkdir -pm 0755 %{buildroot}%{phpdir}/React/Promise
cp -rp src/* %{buildroot}%{phpdir}/React/Promise/


%check
%if %{with_tests}
# Create bootstrap
cat > bootstrap.php <<'BOOTSTRAP'
<?php

spl_autoload_register(function ($class) {
    $src = str_replace('\\', '/', $class).'.php';

    if (!@include_once $src) {
        $psr4_class = str_replace('React\\Promise\\', '', $class);
        $psr4_src = str_replace('\\', '/', $psr4_class).'.php';

        @include_once $psr4_src;
    }
});

require_once '%{buildroot}%{phpdir}/React/Promise/functions.php';
BOOTSTRAP

%{__phpunit} \
    --bootstrap ./bootstrap.php \
    --include-path %{buildroot}%{phpdir}:./tests
%else
: Tests skipped
%endif


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc *.md composer.json
%dir %{phpdir}/React
     %{phpdir}/React/Promise


%changelog
* Sun Jan 04 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 2.2.0-1
- Updated to 2.2.0 (BZ #1178411)

* Fri Oct 31 2014 Remi Collet <remi@fedoraproject.org> - 2.1.0-1
- backport 2.1.0 for remi repo.

* Mon Oct 27 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 2.1.0-1
- Updated to 2.1.0

* Wed Oct 15 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 2.0.0-1
- Initial package
