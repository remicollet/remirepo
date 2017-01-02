# remirepo/fedora spec file for php-hamcrest
#
# Copyright (c) 2015-2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    b37020aa976fa52d3de9aa904aa2522dc518f79c
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     hamcrest
%global gh_project   hamcrest-php
%global with_tests   0%{!?_without_tests:1}

Name:           php-hamcrest
Version:        1.2.2
Release:        1%{?dist}
Summary:        PHP port of Hamcrest Matchers

Group:          Development/Libraries
License:        BSD
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}-%{gh_short}.tar.gz

# Use generated autoloader instead of composer one
Patch0:         bootstrap-autoload.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php-composer(theseer/autoload)
%if %{with_tests}
BuildRequires:  php-composer(phpunit/phpunit)
# composer.json
#      "php": ">=5.3.2"
BuildRequires:  php(language) >= 5.3.2
# From phpcompatinfo report for 1.2.2
BuildRequires:  php-dom
BuildRequires:  php-pcre
BuildRequires:  php-spl
%endif

Requires:       php(language) >= 5.3.2
# From phpcompatinfo report for 1.2.2
Requires:       php-dom
Requires:       php-pcre
Requires:       php-spl

Provides:       php-composer(hamcrest/hamcrest-php) = %{version}


%description
Hamcrest is a matching library originally written for Java,
but subsequently ported to many other languages.

%{name} is the official PHP port of Hamcrest and essentially follows
a literal translation of the original Java API for Hamcrest,
with a few Exceptions, mostly down to PHP language barriers.

To use this library, you just have to add, in your project:
  require_once '%{_datadir}/php/Hamcrest/autoload.php';


%prep
%setup -q -n %{gh_project}-%{gh_commit}

%patch0 -p0 -b .rpm

# Move to Library tree
mv hamcrest/Hamcrest.php hamcrest/Hamcrest/Hamcrest.php


%build
# Library autoloader
%{_bindir}/phpab \
    --output hamcrest/Hamcrest/autoload.php \
    hamcrest/Hamcrest

cat << 'EOF' | tee -a hamcrest/Hamcrest/autoload.php

// Functions
require __DIR__ . '/Hamcrest.php';
EOF

# Test suite autoloader
%{_bindir}/phpab \
    --output tests/autoload.php \
    --exclude '*Test.php' \
    tests


%install
rm -rf            %{buildroot}
mkdir -p          %{buildroot}%{_datadir}/php
cp -pr hamcrest/* %{buildroot}%{_datadir}/php


%check
%if %{with_tests}
cd tests
%{_bindir}/phpunit --verbose
%else
: Test suite disabled
%endif


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE.txt
%doc CHANGES.txt README.md TODO.txt
%doc composer.json
%{_datadir}/php/Hamcrest


%changelog
* Thu Oct 15 2015 Remi Collet <remi@fedoraproject.org> - 1.2.2-1
- update to 1.2.2

* Mon Jan  5 2015 Remi Collet <remi@fedoraproject.org> - 1.2.0-1
- initial package