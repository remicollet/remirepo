# spec file for php-phpspec
#
# Copyright (c) 2015 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    9727d75919a00455433e867565bc022f0b985a39
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     phpspec
%global gh_project   phpspec

Name:           php-phpspec
Version:        2.2.0
Release:        1%{?dist}
Summary:        Specification-oriented BDD framework for PHP

Group:          Development/Libraries
License:        MIT
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}.tar.gz

Source1:        %{gh_project}-autoload.php

# Use our autoloader
Patch0:         %{gh_project}-rpm.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  %{_bindir}/phpunit
BuildRequires:  php-composer(phpspec/prophecy)         >= 1.4
BuildRequires:  php-composer(phpspec/php-diff)         >= 1.0.0
BuildRequires:  php-composer(sebastian/exporter)       >= 1.0
BuildRequires:  php-composer(symfony/console)          >= 2.3.0
BuildRequires:  php-composer(symfony/event-dispatcher) >= 2.1
BuildRequires:  php-composer(symfony/finder)           >= 2.1
BuildRequires:  php-composer(symfony/process)          >= 2.1
BuildRequires:  php-composer(symfony/yaml)             >= 2.1
BuildRequires:  php-composer(doctrine/instantiator)    >= 1.0.1
BuildRequires:  php-composer(symfony/class-loader)
# From composer.json, require-dev
BuildRequires:  php-composer(symfony/filesystem)       >= 2.1

# From composer.json, require
#         "php":                      ">=5.3.3",
#         "phpspec/prophecy":         "~1.4",
#         "phpspec/php-diff":         "~1.0.0",
#         "sebastian/exporter":       "~1.0",
#         "symfony/console":          "~2.3",
#         "symfony/event-dispatcher": "~2.1",
#         "symfony/finder":           "~2.1",
#         "symfony/process":          "~2.1",
#         "symfony/yaml":             "~2.1",
#         "doctrine/instantiator":    "^1.0.1"
Requires:       php(language) >= 5.3.3
Requires:       php-composer(phpspec/prophecy)         >= 1.4
Requires:       php-composer(phpspec/prophecy)         <  2
Requires:       php-composer(phpspec/php-diff)         >= 1.0.0
Requires:       php-composer(phpspec/php-diff)         <  2
Requires:       php-composer(sebastian/exporter)       >= 1.0
Requires:       php-composer(sebastian/exporter)       <  2
Requires:       php-composer(symfony/console)          >= 2.3.0
Requires:       php-composer(symfony/console)          <  3
Requires:       php-composer(symfony/event-dispatcher) >= 2.1
Requires:       php-composer(symfony/event-dispatcher) <  3
Requires:       php-composer(symfony/finder)           >= 2.1
Requires:       php-composer(symfony/finder)           <  3
Requires:       php-composer(symfony/process)          >= 2.1
Requires:       php-composer(symfony/process)          <  3
Requires:       php-composer(symfony/yaml)             >= 2.1
Requires:       php-composer(symfony/yaml)             <  3
Requires:       php-composer(doctrine/instantiator)    >= 1.0.1
Requires:       php-composer(doctrine/instantiator)    <  2
# For our autoloader
Requires:       php-composer(symfony/class-loader)
# From phpcompatinfo report
Requires:       php-pcntl
Requires:       php-pcre
Requires:       php-reflection
Requires:       php-spl
Requires:       php-tokenizer

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
%{_bindir}/php \
  -d include_path=.:src:/usr/share/php \
  bin/phpspec \
  run --format pretty --verbose --no-ansi

%{_bindir}/phpunit \
  --verbose \
  --bootstrap src/PhpSpec/autoload.php


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
* Sun Apr 19 2015 Remi Collet <remi@fedoraproject.org> - 2.2.0-1
- update to 2.2.0
- raise dependency on phpspec/prophecy 1.4

* Tue Feb 17 2015 Remi Collet <remi@fedoraproject.org> - 2.1.1-1
- initial package