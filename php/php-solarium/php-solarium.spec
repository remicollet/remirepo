# Spec file for php-solarium
#
# Copyright (c) 2013 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/3.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    0766401cce7831548e0c213b71bafcb717d1c9ec
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     basdenooijer
%global gh_project   solarium
%global with_tests   %{?_without_tests:0}%{!?_without_tests:1}

Name:           php-%{gh_project}
Summary:        Solarium PHP Solr client library
Version:        3.1.2
Release:        1%{?dist}

URL:            http://www.solarium-project.org/
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}.tar.gz
License:        BSD
Group:          Development/Libraries

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
%if %{with_tests}
# For tests
BuildRequires:  php(language) >= 5.3.2
BuildRequires:  php-cli
BuildRequires:  php-pear(pear.phpunit.de/PHPUnit)
BuildRequires:  php-pear(pear.symfony.com/EventDispatcher) > 2.1
%endif

# From composer.json
Requires:       php(language) >= 5.3.2
Requires:       php-pear(pear.symfony.com/EventDispatcher) > 2.1
# From phpcompatinfo report for version 3.1.2
Requires:       php-curl
Requires:       php-date
Requires:       php-json
Requires:       php-pcre
Requires:       php-spl


%description
Solarium is a PHP Solr client library that accurately model Solr concepts.

Where many other Solr libraries only handle the communication with Solr,
Solarium also relieves you of handling all the complex Solr query parameters
using a well documented API.

Documentation: http://wiki.solarium-project.org/


%prep
%setup -q -n %{gh_project}-%{gh_commit}

rm examples/.gitignore

: Create trivial PSR0 autoloader
cat <<EOF | tee psr0.php
<?php
spl_autoload_register(function (\$class) {
    \$file = str_replace('\\\\', '/', \$class).'.php';
    @include \$file;
});
EOF

: Create phpunit configuration file
cat <<EOF | tee phpunit.xml
<?xml version="1.0" encoding="UTF-8"?>
<phpunit bootstrap="psr0.php">
    <testsuites>
       <testsuite name="Solarium">
         <directory suffix="Test.php">tests</directory>
       </testsuite>
    </testsuites>
</phpunit>
EOF


%build
# nothing to build


%install
mkdir -p %{buildroot}%{_datadir}/php
cp -pr library/Solarium %{buildroot}%{_datadir}/php/Solarium


%check
%if %{with_tests}
phpunit \
  -d include_path=%{buildroot}%{_datadir}/php:./tests:$(php -r 'echo ini_get("include_path");') \
  -d date.timezone=UTC
%else
: Skip test suite
%endif


%files
%defattr(-,root,root,-)
%doc composer.json COPYING README.md examples
%{_datadir}/php/Solarium


%changelog
* Mon Oct 28 2013 Remi Collet <remi@fedoraproject.org> - 3.1.2-1
- Initial packaging
