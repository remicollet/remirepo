# spec file for php-andrewsville-php-token-reflection
#
# Copyright (c) 2015-2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    e6d0ac2baf66cdf154be34c3d2a2aa1bd4b426ee
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     Andrewsville
%global gh_project   PHP-Token-Reflection
%global with_tests   %{?_without_tests:0}%{!?_without_tests:1}

Name:           php-andrewsville-php-token-reflection
Version:        1.4.0
Release:        5%{?dist}
Summary:        Library emulating the PHP internal reflection

Group:          Development/Libraries
License:        BSD
URL:            https://github.com/%{gh_owner}/%{gh_project}
# https://github.com/Andrewsville/PHP-Token-Reflection/issues/68
# run mksrc.sh to create the tarball from a git snapshot
Source0:        %{name}-%{version}-%{gh_short}.tgz
Source1:        makesrc.sh

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php(language) >= 5.3
# Autoloader
BuildRequires:  php-composer(fedora/autoloader)
%if %{with_tests}
BuildRequires:  %{_bindir}/phpunit
%endif

# From composer.json
#       "php": ">=5.3.0",
#       "ext-tokenizer": "*"
Requires:       php(language) >= 5.3
Requires:       php-tokenizer
# From phpcompatifo report for 1.4.0
Requires:       php-pcre
Requires:       php-phar
Requires:       php-reflection
Requires:       php-spl
# Autoloader
Requires:       php-composer(fedora/autoloader)

Provides:       php-composer(andrewsville/php-token-reflection) = %{version}


%description
This library emulates the PHP reflection model using the tokenized PHP source.

Autoloader: %{_datadir}/php/TokenReflection/autoload.php


%prep
%setup -q -n %{gh_project}-%{gh_commit}


%build
cat << 'EOF' | tee TokenReflection/autoload.php
<?php
/* Autoloader for andrewsville/php-token-reflection and its dependencies */

require_once '/usr/share/php/Fedora/Autoloader/autoload.php';

\Fedora\Autoloader\Autoload::addPsr4('TokenReflection\\', __DIR__);
EOF


%install
rm -rf                 %{buildroot}
mkdir -p               %{buildroot}%{_datadir}/php
cp -pr TokenReflection %{buildroot}%{_datadir}/php/TokenReflection


%if %{with_tests}
%check
: run test suite
%{_bindir}/phpunit --bootstrap %{buildroot}%{_datadir}/php/TokenReflection/autoload.php \
  tests || : results ignored for now, known upstream issues
%endif


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE.md
%doc README.md composer.json
%{_datadir}/php/TokenReflection


%changelog
* Mon Oct 31 2016 Remi Collet <remi@fedoraproject.org> - 1.4.0-5
- add autoloader using fedora/autoloader

* Mon May  4 2015 Remi Collet <remi@fedoraproject.org> - 1.4.0-2
- add mksrc.sh as source1, per review comment #1207591

* Tue Mar 31 2015 Remi Collet <remi@fedoraproject.org> - 1.4.0-1
- initial package
