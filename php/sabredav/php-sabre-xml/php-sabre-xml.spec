# remirepo/fedora spec file for php-sabre-xml
#
# Copyright (c) 2016 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    f48d98c22a4a4bef76cabb5968ffaddbb2bb593e
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     fruux
%global gh_project   sabre-xml
%if 0%{?rhel} == 5
# Libxml seems too old
%global with_tests   0%{?_with_tests:1}
%else
%global with_tests   0%{!?_without_tests:1}
%endif

Name:           php-%{gh_project}
Summary:        XML library that you may not hate
Version:        1.4.2
Release:        1%{?dist}

URL:            https://github.com/%{gh_owner}/%{gh_project}
License:        BSD
Group:          Development/Libraries
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}-%{gh_short}.tar.gz
Source1:        %{name}-autoload.php

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
%if %{with_tests}
BuildRequires:  php(language) >= 5.4.1
BuildRequires:  php-xmlwriter
BuildRequires:  php-xmlreader
BuildRequires:  php-dom
BuildRequires:  php-composer(sabre/uri) >= 1.0
BuildRequires:  php-pcre
BuildRequires:  php-spl
# From composer.json, "require-dev": {
#        "sabre/cs": "~0.0.1",
#        "phpunit/phpunit" : "*"
BuildRequires:  php-composer(phpunit/phpunit)
# Autoloader
BuildRequires:  php-composer(symfony/class-loader)
%endif

# From composer.json, "require" : {
#        "php" : ">=5.4.1",
#        "ext-xmlwriter" : "*",
#        "ext-xmlreader" : "*",
#        "ext-dom" : "*",
#        "lib-libxml" : ">=2.6.20",
#        "sabre/uri" : "~1.0"
Requires:       php(language) >= 5.4.1
Requires:       php-xmlwriter
Requires:       php-xmlreader
Requires:       php-dom
Requires:       php-composer(sabre/uri) >= 1.0
Requires:       php-composer(sabre/uri) <  2
# From phpcompatinfo report for version 1.4.0
Requires:       php-pcre
Requires:       php-spl
# Autoloader
Requires:       php-composer(symfony/class-loader)

Provides:       php-composer(sabre/xml) = %{version}


%description
The sabre/xml library is a specialized XML reader and writer.

Autoloader: %{_datadir}/php/Sabre/Xml/autoload.php


%prep
%setup -q -n %{gh_project}-%{gh_commit}

cp %{SOURCE1} lib/autoload.php


%build
# nothing to build


%install
rm -rf %{buildroot}

# Install as a PSR-0 library
mkdir -p %{buildroot}%{_datadir}/php/Sabre
cp -pr lib %{buildroot}%{_datadir}/php/Sabre/Xml


%check
%if %{with_tests}
cd tests
cat << 'EOF' | tee bootstrap.php
<?php
require_once '%{buildroot}%{_datadir}/php/Sabre/Xml/autoload.php';
// Some extra classes
include __DIR__ . '/Sabre/Xml/Element/Mock.php';
include __DIR__ . '/Sabre/Xml/Element/Eater.php';
EOF

: Run upstream test suite against installed library
%{_bindir}/phpunit --verbose

if which php70; then
  php70 %{_bindir}/phpunit --verbose
fi
%else
: Skip upstream test suite
%endif


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc *md
%doc composer.json
%{_datadir}/php/Sabre/Xml


%changelog
* Fri May 20 2016 Remi Collet <remi@fedoraproject.org> - 1.4.2-1
- update to 1.4.2

* Tue Mar 29 2016 Remi Collet <remi@fedoraproject.org> - 1.4.1-1
- update to 1.4.1

* Fri Mar 11 2016 Remi Collet <remi@fedoraproject.org> - 1.4.0-1
- Initial packaging

