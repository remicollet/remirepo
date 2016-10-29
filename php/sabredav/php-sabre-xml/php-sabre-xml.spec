# remirepo/fedora spec file for php-sabre-xml
#
# Copyright (c) 2016 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    59b20e5bbace9912607481634f97d05a776ffca7
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
Version:        1.5.0
Release:        2%{?dist}

URL:            https://github.com/%{gh_owner}/%{gh_project}
License:        BSD
Group:          Development/Libraries
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}-%{gh_short}.tar.gz
Source1:        %{name}-autoload.php

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
%if %{with_tests}
BuildRequires:  php(language) >= 5.5.5
BuildRequires:  php-xmlwriter
BuildRequires:  php-xmlreader
BuildRequires:  php-dom
BuildRequires:  php-composer(sabre/uri) >= 1.0
BuildRequires:  php-pcre
BuildRequires:  php-spl
# From composer.json, "require-dev": {
#        "sabre/cs": "~1.0.0",
#        "phpunit/phpunit" : "*"
BuildRequires:  php-composer(phpunit/phpunit)
# Autoloader
BuildRequires:  php-composer(fedora/autoloader)
%endif

# From composer.json, "require" : {
#        "php" : ">=5.5.5",
#        "ext-xmlwriter" : "*",
#        "ext-xmlreader" : "*",
#        "ext-dom" : "*",
#        "lib-libxml" : ">=2.6.20",
#        "sabre/uri" : ">=1.0,<3.0.0"
Requires:       php(language) >= 5.5.5
Requires:       php-xmlwriter
Requires:       php-xmlreader
Requires:       php-dom
Requires:       php-composer(sabre/uri) >= 1.0
Requires:       php-composer(sabre/uri) <  3
# From phpcompatinfo report for version 1.4.0
Requires:       php-pcre
Requires:       php-spl
# Autoloader
Requires:       php-composer(fedora/autoloader)

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
mkdir vendor
cat << 'EOF' | tee vendor/autoload.php
<?php
require_once '%{buildroot}%{_datadir}/php/Sabre/Xml/autoload.php';
// Tests
require_once '%{_datadir}/php/Symfony/Component/ClassLoader/Psr4ClassLoader.php';
\Fedora\Autoloader\Autoload::addPsr4('Sabre\\Xml\\', dirname(__DIR__).'/tests/Sabre/Xml/');
EOF
cd tests

: Run upstream test suite against installed library
# remirepo:11
ret=0
run=0
if which php71; then
   php71 %{_bindir}/phpunit || ret=1
   run=1
fi
if which php56; then
   php56 %{_bindir}/phpunit || ret=1
   run=1
fi
if [ $run -eq 0 ]; then
%{_bindir}/phpunit --verbose
# remirepo:2
fi
exit $ret
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
* Sat Oct 29 2016 Remi Collet <remi@fedoraproject.org> - 1.5.0-2
- switch from symfony/class-loader to fedora/autoloader

* Mon Oct 10 2016 Remi Collet <remi@fedoraproject.org> - 1.5.0-1
- update to 1.5.0
- raise dependency on PHP 5.5

* Fri May 20 2016 Remi Collet <remi@fedoraproject.org> - 1.4.2-1
- update to 1.4.2

* Tue Mar 29 2016 Remi Collet <remi@fedoraproject.org> - 1.4.1-1
- update to 1.4.1

* Fri Mar 11 2016 Remi Collet <remi@fedoraproject.org> - 1.4.0-1
- Initial packaging

