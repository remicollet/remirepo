# remirepo/fedora spec file for php-phpmyadmin-shapefile
#
# Copyright (c) 2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#

##TODO next version will have tests back

%global gh_commit    cb650f2900c69c1f864715c29f40ef912e112f7e
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     phpmyadmin
%global gh_project   shapefile
%global with_tests   0%{!?_without_tests:1}
%global psr0         ShapeFile

Name:           php-%{gh_owner}-%{gh_project}
Version:        1.2
Release:        1%{?dist}
Summary:        ESRI ShapeFile library for PHP

Group:          Development/Libraries
License:        GPLv2+
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        %{name}-%{version}-%{gh_short}.tgz
Source1:        makesrc.sh

BuildArch:      noarch
%if %{with_tests}
BuildRequires:  php(language) >= 5.4
# For tests, from composer.json "require-dev": {
#        "phpunit/phpunit": "~5.2 || ~4.8"
BuildRequires:  php-composer(phpunit/phpunit) >= 4.8
%endif
# For autoloader
BuildRequires:  php-composer(fedora/autoloader)

# From composer.json, "require": {
#        "php": ">=5.4.0"
Requires:       php(language) >= 5.4
# From phpcompatinfo report for 1.2
#   nothing
# From composer.json, "suggest": {
#        "ext-dbase": "For dbf files parsing"
%if 0%{?fedora} >= 21
Suggests:       php-dbase
%endif
# For generated autoloader
Requires:       php-composer(fedora/autoloader)

# Composer
Provides:       php-composer(%{gh_owner}/%{gh_project}) = %{version}


%description
Currently the 2D and 3D variants except MultiPatch of the ShapeFile format
as defined in [1].

The library currently supports reading and editing of ShapeFiles and the
Associated information (DBF file). There are a lot of things that can be
improved in the code, if you are interested in developing, helping with the
documentation, making translations or offering new ideas please contact us.

[1] https://www.esri.com/library/whitepapers/pdfs/shapefile.pdf

Autoloader: %{_datadir}/php/%{psr0}/autoload.php


%prep
%setup -q -n %{gh_project}-%{gh_commit}


%build
: Create autoloader
cat <<'AUTOLOAD' | tee src/autoload.php
<?php
/* Autoloader for %{name} and its dependencies */
require_once '%{_datadir}/php/Fedora/Autoloader/autoload.php';

\Fedora\Autoloader\Autoload::addPsr4('%{psr0}\\', __DIR__);
AUTOLOAD


%install
: Library
mkdir -p   %{buildroot}%{_datadir}/php
cp -pr src %{buildroot}%{_datadir}/php/%{psr0}


%check
%if %{with_tests}
mkdir vendor
cat << 'EOF' | tee vendor/autoload.php
<?php
require '%{buildroot}%{_datadir}/php/%{psr0}/autoload.php';
EOF

# remirepo:11
run=0
ret=0
if which php56; then
   php56 %{_bindir}/phpunit --no-coverage || ret=1
   run=1
fi
if which php71; then
   php71 %{_bindir}/phpunit --no-coverage || ret=1
   run=1
fi
if [ $run -eq 0 ]; then
%{_bindir}/phpunit --no-coverage --verbose
# remirepo:2
fi
exit $ret
%else
: Test suite disabled
%endif


%files
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc composer.json
%doc *.md
%{_datadir}/php/%{psr0}


%changelog
* Sat Jan 21 2017 Remi Collet <remi@remirepo.net> - 1.2-1
- initial package

