# remirepo/fedora spec file for php-solarium
#
# Copyright (c) 2013-2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    06e957a9060afd200cd66fef61125108bd66874a
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     solariumphp
%global gh_project   solarium
%global with_tests   0%{!?_without_tests:1}

Name:           php-%{gh_project}
Summary:        Solarium PHP Solr client library
Version:        3.8.0
Release:        1%{?dist}

URL:            http://www.solarium-project.org/
License:        BSD
Group:          Development/Libraries
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}-%{gh_short}.tar.gz
Source1:        %{name}-autoload.php

# https://github.com/solariumphp/solarium/pull/479
# fix for PHP 5.3 (EPEL-6)
Patch0:         %{name}-pr479.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
%if %{with_tests}
# For tests
BuildRequires:  php(language) >= 5.3.2
BuildRequires:  php-composer(symfony/event-dispatcher) > 2.3
BuildRequires:  php-composer(fedora/autoloader)
# From composer.json, "require-dev": {
#        "phpunit/phpunit": "~3.7",
#        "squizlabs/php_codesniffer": "~1.4",
#        "zendframework/zendframework1": "~1.12",
#        "satooshi/php-coveralls": "~1.0",
#        "guzzlehttp/guzzle": "^3.8 || ^6.2"
BuildRequires:  php-composer(phpunit/phpunit) >= 3.7
%if 0%{?fedora}
BuildRequires:  php-guzzlehttp-guzzle6 >= 6.2
%else
BuildRequires:  php-guzzle-Guzzle >= 3.8
%endif
%endif

# From composer.json, "require": {
#        "php": ">=5.3.2",
#        "symfony/event-dispatcher": "~2.3|~3.0"
Requires:       php(language) >= 5.3.2
Requires:       php-composer(symfony/event-dispatcher) > 2.3
Requires:       php-composer(symfony/event-dispatcher) < 4
# From composer.json, "suggest": {
#        "minimalcode/search": "Query builder compatible with Solarium, allows simplified solr-query handling"
%if 0%{?fedora}> 21
Suggests:       php-composer(minimalcode/search)
%endif
# From phpcompatinfo report for version 3.7.0
Requires:       php-curl
Requires:       php-date
Requires:       php-json
Requires:       php-pcre
Requires:       php-spl
# php-http optional, and only v1 suppported.
# For our autoloader
Requires:       php-composer(fedora/autoloader)

Provides:       php-composer(solarium/solarium) = %{version}


%description
Solarium is a PHP Solr client library that accurately model Solr concepts.

Where many other Solr libraries only handle the communication with Solr,
Solarium also relieves you of handling all the complex Solr query parameters
using a well documented API.

Autoloader: %{_datadir}/php/Solarium/autoload.php

Documentation: http://wiki.solarium-project.org/


%prep
%setup -q -n %{gh_project}-%{gh_commit}
%patch0 -p1

rm examples/.gitignore

cp %{SOURCE1} library/Solarium/autoload.php


%build
# nothing to build


%install
mkdir -p %{buildroot}%{_datadir}/php
cp -pr library/Solarium %{buildroot}%{_datadir}/php/Solarium


%check
%if %{with_tests}
: Autoloader
mkdir vendor
cat << 'EOF' | tee vendor/autoload.php
<?php
require_once '%{buildroot}%{_datadir}/php/Solarium/autoload.php';
\Fedora\Autoloader\Dependencies::required(array(
    array(
        '%{_datadir}/php/Guzzle/autoload.php',
        '%{_datadir}/php/GuzzleHttp6/autoload.php',
    ),
));
EOF

: Run upstream test suite against installed library
# remirepo:11
run=0
ret=0
if which php56; then
   php56 %{_bindir}/phpunit || ret=1
   run=1
fi
if which php71; then
   php71 %{_bindir}/phpunit || ret=1
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


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc composer.json *.md examples
%{_datadir}/php/Solarium


%changelog
* Wed Feb  1 2017 Remi Collet <remi@fedoraproject.org> - 3.8.0-1
- update to 3.8.0
- open https://github.com/solariumphp/solarium/pull/479
  fix for PHP 5.3 in EL-6

* Fri Oct 28 2016 Remi Collet <remi@fedoraproject.org> - 3.7.0-1
- update to 3.7.0
- add optional dependency on minimalcode/search
- switch from symfony/class-loader to fedora/autoloader

* Tue May  3 2016 Remi Collet <remi@fedoraproject.org> - 3.6.0-1
- update to 3.6.0
- allow symfony 3

* Sat Dec 26 2015 Remi Collet <remi@fedoraproject.org> - 3.5.1-1
- update to 3.5.1

* Tue Dec 15 2015 Remi Collet <remi@fedoraproject.org> - 3.5.0-1.1
- update to 3.5.0
- add autoloader
- run test suite with both php 5 and 7 when available

* Mon Jun 15 2015 Remi Collet <remi@fedoraproject.org> - 3.4.1-1
- update to 3.4.1

* Tue Nov 18 2014 Remi Collet <remi@fedoraproject.org> - 3.3.0-2
- provide php-composer(solarium/solarium)
- fix license handling

* Mon Nov 17 2014 Remi Collet <remi@fedoraproject.org> - 3.3.0-1
- update to 3.3.0

* Sun Apr  6 2014 Remi Collet <remi@fedoraproject.org> - 3.2.0-1
- update to 3.2.0

* Sat Dec 28 2013 Remi Collet <remi@fedoraproject.org> - 3.1.2-2
- cleanups from review #1023879

* Mon Oct 28 2013 Remi Collet <remi@fedoraproject.org> - 3.1.2-1
- Initial packaging
