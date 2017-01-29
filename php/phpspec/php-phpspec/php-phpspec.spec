# remirepo/fedora spec file for php-phpspec
#
# Copyright (c) 2015-2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    97246d90708cf98983d95d609bbe6f4b039b8600
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     phpspec
%global gh_project   phpspec
#global prever       beta3

Name:           php-phpspec
Version:        3.2.3
Release:        1%{?dist}
Summary:        Specification-oriented BDD framework for PHP

Group:          Development/Libraries
License:        MIT
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}%{?prever}-%{gh_short}.tar.gz

Source1:        %{gh_project}-autoload.php

# Use our autoloader
Patch0:         %{gh_project}-3-rpm.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php-composer(phpspec/prophecy)         >= 1.4
BuildRequires:  php-composer(phpspec/php-diff)         >= 1.0.0
BuildRequires:  php-composer(sebastian/exporter)       >= 1.0
BuildRequires:  php-composer(symfony/console)          >= 2.3.0
BuildRequires:  php-composer(symfony/event-dispatcher) >= 2.1
BuildRequires:  php-composer(symfony/finder)           >= 2.1
BuildRequires:  php-composer(symfony/process)          >= 2.6
BuildRequires:  php-composer(symfony/yaml)             >= 2.1
BuildRequires:  php-composer(doctrine/instantiator)    >= 1.0.1
# From composer.json, require-dev
#        "behat/behat":           "^3.1",
#        "symfony/filesystem":    "^3.0",
#        "phpunit/phpunit":       "^5.4",
#         "ciaranmcnulty/versionbasedtestskipper": "^0.2.1"
BuildRequires:  php-composer(symfony/filesystem)       >= 2.1
BuildRequires:  php-composer(phpunit/phpunit)          >= 5.4
# Autoloader
BuildRequires:  php-composer(fedora/autoloader)

# From composer.json, require
#        "php":                      "^5.6 || ^7.0",
#        "phpspec/prophecy":         "^1.5",
#        "phpspec/php-diff":         "^1.0.0",
#        "sebastian/exporter":       "^1.0 || ^2.0",
#        "symfony/console":          "^2.7 || ^3.0",
#        "symfony/event-dispatcher": "^2.7 || ^3.0",
#        "symfony/process":          "^2.7 || ^3.0",
#        "symfony/finder":           "^2.7 || ^3.0",
#        "symfony/yaml":             "^2.7 || ^3.0",
#        "doctrine/instantiator":    "^1.0.1"
#        "ext-tokenizer":            "*"

Requires:       php(language) >= 5.6
Requires:       php-composer(phpspec/prophecy)         >= 1.5
Requires:       php-composer(phpspec/prophecy)         <  2
Requires:       php-composer(phpspec/php-diff)         >= 1.0.0
Requires:       php-composer(phpspec/php-diff)         <  2
Requires:       php-composer(sebastian/exporter)       >= 1.0
Requires:       php-composer(sebastian/exporter)       <  3
Requires:       php-composer(symfony/console)          >= 2.7
Requires:       php-composer(symfony/console)          <  4
Requires:       php-composer(symfony/event-dispatcher) >= 2.7
Requires:       php-composer(symfony/event-dispatcher) <  4
Requires:       php-composer(symfony/finder)           >= 2.7
Requires:       php-composer(symfony/finder)           <  4
Requires:       php-composer(symfony/process)          >= 2.7
Requires:       php-composer(symfony/process)          <  4
Requires:       php-composer(symfony/yaml)             >= 2.7
Requires:       php-composer(symfony/yaml)             <  4
Requires:       php-composer(doctrine/instantiator)    >= 1.0.1
Requires:       php-composer(doctrine/instantiator)    <  2
Requires:       php-tokenizer
# Autoloader
Requires:       php-composer(fedora/autoloader)
# From phpcompatinfo report
Requires:       php-pcntl
Requires:       php-pcre
Requires:       php-reflection
Requires:       php-spl

# Composer
Provides:       php-composer(phpspec/phpspec) = %{version}
# The application
Provides:       phpspec = %{version}


%description
phpspec is a tool which can help you write clean and working PHP code
using behaviour driven development or BDD. BDD is a technique derived
from test-first development.

BDD is a technique used at story level and spec level. phpspec is a tool
for use at the spec level or SpecBDD. The technique is to first use a tool
like phpspec to describe the behaviour of an object you are about to write.
Next you write just enough code to meet that specification and finally you
refactor this code.


%prep
%setup -q -n %{gh_project}-%{gh_commit}

%patch0 -p0 -b .rpm

cp %{SOURCE1} src/PhpSpec/autoload.php


%build
# Nothing


%install
# No namespace, so use a package specific dir
rm -rf             %{buildroot}
mkdir -p           %{buildroot}%{_datadir}/php
cp -pr src/PhpSpec %{buildroot}%{_datadir}/php/PhpSpec

install -Dpm755 bin/phpspec %{buildroot}%{_bindir}/phpspec


%check
export LANG=en_GB.utf8

# Ignore this test which use bossa/phpspec2-expect
rm spec/PhpSpec/Message/CurrentExampleTrackerSpec.php

# remirepo:26
run=0
if which php56; then
  php56 \
    -d include_path=.:%{buildroot}%{_datadir}/php \
    bin/phpspec \
      run --format pretty --verbose --no-ansi

  php56 %{_bindir}/phpunit \
    --verbose \
    --bootstrap %{buildroot}%{_datadir}/php/PhpSpec/autoload.php

  run=1
fi
if which php71; then
  php71 \
    -d include_path=.:%{buildroot}%{_datadir}/php \
    bin/phpspec \
      run --format pretty --verbose --no-ansi

  php71 %{_bindir}/phpunit \
    --verbose \
    --bootstrap %{buildroot}%{_datadir}/php/PhpSpec/autoload.php

  run=1
fi
if [ $run -eq 0 ]; then
%{_bindir}/php \
  -d include_path=.:%{buildroot}%{_datadir}/php \
  bin/phpspec \
    run --format pretty --verbose --no-ansi

%{_bindir}/phpunit \
  --verbose \
  --bootstrap %{buildroot}%{_datadir}/php/PhpSpec/autoload.php
# remirepo:2
fi

%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc README.* CHANGES.*
%doc composer.json
%{_bindir}/phpspec
%{_datadir}/php/PhpSpec


%changelog
* Sun Jan 29 2017 Remi Collet <remi@fedoraproject.org> - 3.2.3-1
- update to 3.2.3

* Tue Dec  6 2016 Remi Collet <remi@fedoraproject.org> - 3.2.2-1
- update to 3.2.2

* Mon Dec  5 2016 Remi Collet <remi@fedoraproject.org> - 3.2.1-1
- update to 3.2.1

* Mon Nov 28 2016 Remi Collet <remi@fedoraproject.org> - 3.2.0-1
- update to 3.2.0

* Tue Nov 22 2016 Remi Collet <remi@fedoraproject.org> - 3.1.1-2
- ignore sebastian/exporter max version
- switch to fedora/autoloader

* Tue Sep 27 2016 Remi Collet <remi@fedoraproject.org> - 3.1.1-1
- update to 3.1.1

* Mon Sep 19 2016 Remi Collet <remi@fedoraproject.org> - 3.1.0-1
- update to 3.1.0

* Mon Jul 18 2016 Remi Collet <remi@fedoraproject.org> - 3.0.0-1
- update to 3.0.0
- raise dependency on php ^5.6 || ^7.0
- raise dependency on phpspec/prophecy ^1.5
- raise dependency on symfony/console ^2.7 || ^3.0

* Mon Jul 18 2016 Remi Collet <remi@fedoraproject.org> - 2.5.1-1
- update to 2.5.1

* Mon Mar 21 2016 Remi Collet <remi@fedoraproject.org> - 2.5.0-1
- update to 2.5.0

* Sat Jan  2 2016 Remi Collet <remi@fedoraproject.org> - 2.4.1-1
- update to 2.4.1

* Sun Nov 29 2015 Remi Collet <remi@fedoraproject.org> - 2.4.0-1
- update to 2.4.0
- allow to use symfony 3.0

* Wed Oct 28 2015 Remi Collet <remi@fedoraproject.org> - 2.3.0-1
- update to 2.3.0

* Thu Aug 13 2015 Remi Collet <remi@fedoraproject.org> - 2.3.0-0.1.beta1
- update to 2.3.0beta3

* Mon Jun 29 2015 Remi Collet <remi@fedoraproject.org> - 2.2.1-3
- switch to $fedoraClassLoader autoloader
- ensure /usr/share/php is in include_path

* Sat May 30 2015 Remi Collet <remi@fedoraproject.org> - 2.2.1-1
- update to 2.2.1

* Sun Apr 19 2015 Remi Collet <remi@fedoraproject.org> - 2.2.0-1
- update to 2.2.0
- raise dependency on phpspec/prophecy 1.4

* Tue Feb 17 2015 Remi Collet <remi@fedoraproject.org> - 2.1.1-1
- initial package
