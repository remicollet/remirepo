# remirepo/fedora spec file for php-phpspec
#
# Copyright (c) 2015-2016 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    531d00ee76e9ae98279ed4dbb2419e5e0f7fb82d
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     phpspec
%global gh_project   phpspec
#global prever       beta3

Name:           php-phpspec
Version:        2.5.1
Release:        1%{?dist}
Summary:        Specification-oriented BDD framework for PHP

Group:          Development/Libraries
License:        MIT
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}%{?prever}-%{gh_short}.tar.gz

Source1:        %{gh_project}-autoload.php

# Use our autoloader
Patch0:         %{gh_project}-rpm.patch

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
#         "behat/behat":           "^3.0.11",
#         "symfony/filesystem":    "~2.1|~3.0",
#         "phpunit/phpunit":       "~4.4"
#         "phpunit/phpunit":       "~4.4",
#         "ciaranmcnulty/versionbasedtestskipper": "^0.2.1"
BuildRequires:  php-composer(symfony/filesystem)       >= 2.1
BuildRequires:  php-composer(phpunit/phpunit)          >= 4.4
# For our autoloader
BuildRequires:  php-composer(symfony/class-loader)

# From composer.json, require
#         "php":                      ">=5.3.3",
#         "phpspec/prophecy":         "~1.4",
#         "phpspec/php-diff":         "~1.0.0",
#         "sebastian/exporter":       "~1.0",
#         "symfony/console":          "~2.3|~3.0",
#         "symfony/event-dispatcher": "~2.1|~3.0",
#         "symfony/process":          "^2.6|~3.0",
#         "symfony/finder":           "~2.1|~3.0",
#         "symfony/yaml":             "~2.1|~3.0",
#         "doctrine/instantiator":    "^1.0.1"
#         "ext-tokenizer":            "*"

Requires:       php(language) >= 5.3.3
Requires:       php-composer(phpspec/prophecy)         >= 1.4
Requires:       php-composer(phpspec/prophecy)         <  2
Requires:       php-composer(phpspec/php-diff)         >= 1.0.0
Requires:       php-composer(phpspec/php-diff)         <  2
Requires:       php-composer(sebastian/exporter)       >= 1.0
Requires:       php-composer(sebastian/exporter)       <  2
Requires:       php-composer(symfony/console)          >= 2.3.0
Requires:       php-composer(symfony/console)          <  4
Requires:       php-composer(symfony/event-dispatcher) >= 2.1
Requires:       php-composer(symfony/event-dispatcher) <  4
Requires:       php-composer(symfony/finder)           >= 2.1
Requires:       php-composer(symfony/finder)           <  4
Requires:       php-composer(symfony/process)          >= 2.6
Requires:       php-composer(symfony/process)          <  4
Requires:       php-composer(symfony/yaml)             >= 2.1
Requires:       php-composer(symfony/yaml)             <  4
Requires:       php-composer(doctrine/instantiator)    >= 1.0.1
Requires:       php-composer(doctrine/instantiator)    <  2
Requires:       php-tokenizer
# For our autoloader
Requires:       php-composer(symfony/class-loader)
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
if which php70; then
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
