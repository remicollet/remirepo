# remirepo/fedora spec file for php-phpspec-prophecy
#
# Copyright (c) 2015-2016 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global bootstrap    0
%global gh_commit    58a8137754bc24b25740d4281399a4a3596058e0
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
Version:        1.6.1
Release:        1%{?dist}
Summary:        Highly opinionated mocking framework for PHP

Group:          Development/Libraries
License:        MIT
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}.tar.gz

# Autoloader
Source1:        %{name}-autoload.php

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
%if %{with_tests}
# from composer.json, "require-dev": {
#        "phpspec/phpspec": "^2.0"
BuildRequires:  php-composer(phpspec/phpspec) >= 2.0
# For autoloader
BuildRequires:  php-composer(symfony/class-loader)
%endif

# from composer.json, "requires": {
#        "php":                               "^5.3|^7.0",
#        "phpdocumentor/reflection-docblock": "^2.0|^3.0.2",
#        "sebastian/comparator":              "^1.1",
#        "doctrine/instantiator":             "^1.0.2",
#        "sebastian/recursion-context":       "^1.0"
Requires:       php(language) >= 5.3
Requires:       php-composer(phpdocumentor/reflection-docblock) >= 2.0
Requires:       php-composer(phpdocumentor/reflection-docblock) <  4
Requires:       php-composer(sebastian/comparator)              >= 1.1
Requires:       php-composer(sebastian/comparator)              <  2
Requires:       php-composer(sebastian/recursion-context)       >= 1.0
Requires:       php-composer(sebastian/recursion-context)       <  2
# use 1.0.4 to ensure we have the autoloader
Requires:       php-composer(doctrine/instantiator)             >= 1.0.4
Requires:       php-composer(doctrine/instantiator)             <  2
# From phpcompatinfo report for version 1.1.0
Requires:       php-pcre
Requires:       php-reflection
Requires:       php-spl
# For autoloader
Requires:       php-composer(symfony/class-loader)

Provides:       php-composer(phpspec/prophecy) = %{version}


%description
Prophecy is a highly opinionated yet very powerful and flexible PHP object
mocking framework.

Though initially it was created to fulfil phpspec2 needs, it is flexible enough
to be used inside any testing framework out there with minimal effort.


%prep
%setup -q -n %{gh_project}-%{gh_commit}

cp %{SOURCE1} src/Prophecy/autoload.php


%build
# Nothing


%install
rm -rf       %{buildroot}
mkdir -p     %{buildroot}%{_datadir}/php
cp -pr src/* %{buildroot}%{_datadir}/php


%check
%if %{with_tests}
%{_bindir}/php \
  -d include_path=.:%{buildroot}%{_datadir}/php:%{_datadir}/php \
  %{_bindir}/phpspec \
  run --format pretty --verbose --no-ansi

if which php70; then
  php70 \
    -d include_path=.:%{buildroot}%{_datadir}/php:%{_datadir}/php \
    %{_bindir}/phpspec \
    run --format pretty --verbose --no-ansi || :
fi
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
* Tue Jun  7 2016 Remi Collet <remi@fedoraproject.org> - 1.6.1-1
- update to 1.6.1

* Mon Feb 15 2016 Remi Collet <remi@fedoraproject.org> - 1.6.0-1
- update to 1.6.0
- add dependency on sebastian/recursion-context
- run test suite with both PHP 5 and 7 when available
- ignore 1 failed spec with PHP 7
  open https://github.com/phpspec/prophecy/issues/258

* Wed Oct 28 2015 Remi Collet <remi@fedoraproject.org> - 1.5.0-2
- fix autolaoder, rely on include_path for symfony/class-loader

* Thu Aug 13 2015 Remi Collet <remi@fedoraproject.org> - 1.5.0-1
- update to 1.5.0

* Mon Jun 29 2015 Remi Collet <remi@fedoraproject.org> - 1.4.1-4
- use symfony/class-loader
- enable test suite

* Tue Apr 28 2015 Remi Collet <remi@fedoraproject.org> - 1.4.1-1
- update to 1.4.1

* Sun Mar 29 2015 Remi Collet <remi@fedoraproject.org> - 1.4.0-1
- update to 1.4.0
- add dependency on sebastian/comparator

* Fri Feb 13 2015 Remi Collet <remi@fedoraproject.org> - 1.3.1-1
- initial package
