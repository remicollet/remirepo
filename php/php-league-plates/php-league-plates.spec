# remirepo/fedora spec file for php-league-plates
#
# Copyright (c) 2016 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
# Github
%global gh_commit    2d8569e9f140a70d6a05db38006926f7547cb802
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     thephpleague
%global gh_project   plates
# Packagist
%global pk_vendor    league
%global pk_name      plates
# PSR-0 namespace
%global ns_vendor    League
%global ns_project   Plates

Name:           php-%{pk_vendor}-%{pk_name}
Version:        3.1.1
Release:        1%{?dist}
Summary:        Native PHP template system

Group:          Development/Libraries
License:        MIT
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        %{name}-%{version}-%{gh_short}.tgz
# Create git snapshot as tests are excluded from official tarball
Source1:        makesrc.sh
# Autoloader
Source2:        %{name}-autoload.php

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php-pcre
BuildRequires:  php-spl
# From composer.json, "require-dev": {
#        "phpunit/phpunit": "~4.0",
#        "mikey179/vfsStream": "~1.4.0",
#        "squizlabs/php_codesniffer": "~1.5"
BuildRequires:  php-composer(phpunit/phpunit) >= 4.0
BuildRequires:  php-composer(mikey179/vfsStream) >= 0.9
# Autoloader
BuildRequires:  php-composer(symfony/class-loader)

# From phpcompatifo report for 3.1.1
Requires:       php-pcre
Requires:       php-spl
# Autoloader
Requires:       php-composer(symfony/class-loader)

Provides:       php-composer(%{pk_vendor}/%{pk_name}) = %{version}


%description
Plates is a native PHP template system that's fast, easy to use and easy
to extend. It's inspired by the excellent Twig template engine and strives
to bring modern template language functionality to native PHP templates.
Plates is designed for developers who prefer to use native PHP templates
over compiled template languages, such as Twig or Smarty.

Autoloader: %{_datadir}/php/%{ns_vendor}/%{ns_project}/autoload.php


%prep
%setup -q -n %{gh_project}-%{gh_commit}

install -pm 644 %{SOURCE2} src/autoload.php


%build
# Nothing


%install
rm -rf     %{buildroot}

# Restore PSR-0 tree
mkdir -p   %{buildroot}%{_datadir}/php/%{ns_vendor}
cp -pr src %{buildroot}%{_datadir}/php/%{ns_vendor}/%{ns_project}


%check
: Generate a simple autoloader
mkdir vendor
cat << 'EOF' | tee vendor/autoload.php
<?php
// Installed library
require '%{buildroot}%{_datadir}/php/%{ns_vendor}/%{ns_project}/autoload.php';

// Dependency
require_once '%{_datadir}/php/org/bovigo/vfs/autoload.php';
EOF

: Run upstream test suite
%{_bindir}/phpunit --verbose

if which php70
then php70 %{_bindir}/phpunit --verbose
fi


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc *.md
%doc composer.json
%{_datadir}/php/%{ns_vendor}


%changelog
* Thu Apr  7 2016 Remi Collet <remi@fedoraproject.org> - 3.1.1-1
- initial package, version 3.1.1

