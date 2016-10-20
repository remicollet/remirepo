# remirepo/fedora spec file for php-composer-spdx-licenses
#
# Copyright (c) 2015-2016 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    96c6a07b05b716e89a44529d060bc7f5c263cb13
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
#global gh_date      20150717
%global gh_owner     composer
%global gh_project   spdx-licenses
%global php_home     %{_datadir}/php
%global with_tests   0%{!?_without_tests:1}

Name:           php-composer-spdx-licenses
Version:        1.1.5
Release:        2%{?gh_date:.%{gh_date}git%{gh_short}}%{?dist}
Summary:        SPDX licenses list and validation library

Group:          Development/Libraries
License:        MIT
URL:            https://github.com/%{gh_owner}/%{gh_project}
# git snapshot to get upstream test suite
Source0:        %{name}-%{version}-%{gh_short}.tgz
Source1:        makesrc.sh
Source2:        %{name}-autoload.php

# Resources path
Patch0:         %{name}-rpm.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
%if %{with_tests}
# For tests
BuildRequires:  php(language) >= 5.3.2
BuildRequires:  php-json
BuildRequires:  php-pcre
BuildRequires:  php-spl
# From composer.json, "require-dev": {
#        "phpunit/phpunit": "phpunit/phpunit": "^4.5 || ^5.0.5",
#        "phpunit/phpunit-mock-objects": "2.3.0 || ^3.0"
BuildRequires:  php-composer(phpunit/phpunit) >= 4.5
BuildRequires:  php-composer(phpunit/phpunit-mock-objects) >= 2.3
# Autoloader
BuildRequires:  php-composer(fedora/autoloader)
%endif

# From composer.json, "require": {
#        "php": "^5.3.2 || ^7.0",
Requires:       php(language) >= 5.3.2
# From phpcompatinfo report for version 1.0.0 (SpdxLicenses.php only)
Requires:       php-json
Requires:       php-pcre
Requires:       php-spl
# Autoloader
Requires:       php-composer(fedora/autoloader)

Provides:       php-composer(%{gh_owner}/%{gh_project}) = %{version}


%description
SPDX licenses list and validation library.

Originally written as part of composer/composer,
now extracted and made available as a stand-alone library.


%prep
%setup -q -n %{gh_project}-%{gh_commit}

%patch0 -p0
cp %{SOURCE2} src/autoload.php


%build
# Empty build section, most likely nothing required.


%install
rm -rf %{buildroot}

: Library
pushd src
for fic in *
do
  if ! grep $fic ../.gitattributes; then
    install -Dpm 0644 $fic %{buildroot}%{php_home}/Composer/Spdx/$fic
  fi
done
popd

: Resources
cp -pr res   %{buildroot}%{_datadir}/%{name}


%check
%if %{with_tests}
export BUILDROOT_SPDX=%{buildroot}

# remirepo:15
run=0
ret=0
if which php56; then
   php56 %{_bindir}/phpunit \
      --bootstrap %{buildroot}%{php_home}/Composer/Spdx/autoload.php \
      --verbose
   run=1
fi
if which php71; then
   php71 %{_bindir}/phpunit \
      --bootstrap %{buildroot}%{php_home}/Composer/Spdx/autoload.php \
      --verbose
   run=1
fi
if [ $run -eq 0 ]; then
%{_bindir}/phpunit \
    --bootstrap %{buildroot}%{php_home}/Composer/Spdx/autoload.php \
    --verbose
# remirepo:2
fi
exit $ret
%else
: Test suite disabled
%endif


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc composer.json
%doc *.md
%dir %{php_home}/Composer
     %{php_home}/Composer/Spdx
%{_datadir}/%{name}


%changelog
* Thu Oct 20 2016 Remi Collet <remi@fedoraproject.org> - 1.1.5-2
- switch from symfony/class-loader to fedora/autoloader

* Wed Sep 28 2016 Remi Collet <remi@fedoraproject.org> - 1.1.5-1
- version 1.1.5 (new licenses)

* Wed May  4 2016 Remi Collet <remi@fedoraproject.org> - 1.1.4-1
- version 1.1.4 (new licenses)

* Fri Mar 25 2016 Remi Collet <remi@fedoraproject.org> - 1.1.3-1
- version 1.1.3 (new licenses)
- run test suite with both PHP 5 and 7 when available

* Mon Oct  5 2015 Remi Collet <remi@fedoraproject.org> - 1.1.2-1
- version 1.1.2 (new licenses)

* Tue Sep  8 2015 Remi Collet <remi@fedoraproject.org> - 1.1.1-1
- version 1.1.1

* Mon Jul 20 2015 Remi Collet <remi@fedoraproject.org> - 1.1.0-2
- fix permissions

* Fri Jul 17 2015 Remi Collet <remi@fedoraproject.org> - 1.1.0-1
- version 1.1.0

* Fri Jul 17 2015 Remi Collet <remi@fedoraproject.org> - 1.0.0-1.20150717git572abf7
- new snapshot (issue #6 fixed, uneeded dep on justinrainbow/json-schema)

* Fri Jul 17 2015 Remi Collet <remi@fedoraproject.org> - 1.0.0-1.20150716git96c33d0
- initial package, version 1.0.0 + pr4
