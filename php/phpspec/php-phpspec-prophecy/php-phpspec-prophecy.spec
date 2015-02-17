# spec file for php-phpspec-prophecy
#
# Copyright (c) 2015 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global bootstrap    1
%global gh_commit    9ca52329bcdd1500de24427542577ebf3fc2f1c9
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     phpspec
%global gh_project   prophecy
%if %{bootstrap}
# no test because of circular dependency with phpspec
%global with_tests   %{?_with_tests:1}%{!?_with_tests:0}
%else
%global with_tests   %{?_without_tests:0}%{!?_without_tests:1}
%endif

Name:           php-phpspec-prophecy
Version:        1.3.1
Release:        1%{?dist}
Summary:        Highly opinionated mocking framework for PHP

Group:          Development/Libraries
License:        MIT
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  %{_bindir}/phpab
%if %{with_tests}
BuildRequires:  %{_bindir}/phpspec
%endif

# from composer.json, requires
#        "phpdocumentor/reflection-docblock": "~2.0",
#        "doctrine/instantiator":             "~1.0,>=1.0.2"
Requires:       php-composer(phpdocumentor/reflection-docblock) >= 2.0
Requires:       php-composer(phpdocumentor/reflection-docblock) <  3
# use 1.0.4 to ensure we have the autoloader
Requires:       php-composer(doctrine/instantiator)             >= 1.0.4
Requires:       php-composer(doctrine/instantiator)             <  2
# From phpcompatinfo report for version 1.1.0
Requires:       php(language) >= 5.3.0
Requires:       php-pcre
Requires:       php-reflection
Requires:       php-spl

Provides:       php-composer(phpspec/prophecy) = %{version}


%description
Prophecy is a highly opinionated yet very powerful and flexible PHP object
mocking framework.

Though initially it was created to fulfil phpspec2 needs, it is flexible enough
to be used inside any testing framework out there with minimal effort.


%prep
%setup -q -n %{gh_project}-%{gh_commit}


%build
: Generate a simple autoloader
%{_bindir}/phpab --output src/Prophecy/autoload.php src/Prophecy

cat <<EOF | tee -a src/Prophecy/autoload.php
// Dependencies' autoloaders
require_once 'Doctrine/Instantiator/autoload.php';
require_once 'phpDocumentor/Reflection/DocBlock/autoload.php';
EOF


%install
rm -rf       %{buildroot}
mkdir -p     %{buildroot}%{_datadir}/php
cp -pr src/* %{buildroot}%{_datadir}/php


%check
%if %{with_tests}
%{_bindir}/php \
  -d include_path=.:%{buildroot}%{_datadir}/php:/usr/share/php \
  %{_bindir}/phpspec \
  run --format pretty --verbose --no-ansi
%else
: Test suite disabled
%endif


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc *.md
%doc composer.json
%{_datadir}/php/Prophecy


%changelog
* Fri Feb 13 2015 Remi Collet <remi@fedoraproject.org> - 1.3.1-1
- initial package