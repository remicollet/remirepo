# remirepo/fedora spec file for apigen
#
# Copyright (c) 2015-2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    3365433ea3433b0e5c8f763608f8e63cbedb2a3a
#global gh_date      20150728
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     ApiGen
%global gh_project   ApiGen
%global ns_vendor    ApiGen
%global c_project    apigen
%global with_tests   0%{!?_without_tests:1}

Name:           %{c_project}
Version:        4.1.2
%global specrel 3
Release:        %{?gh_date:0.%{specrel}.%{?prever}%{!?prever:%{gh_date}git%{gh_short}}}%{!?gh_date:%{specrel}}%{?dist}
Summary:        PHP source code API generator

Group:          Development/Libraries
License:        MIT
URL:            http://www.apigen.org/
Source0:        %{name}-%{version}-%{gh_short}.tgz
# pull a git snapshot to get test sutie
Source1:        makesrc.sh

# Use RPM autoloader
# and drop Herrera dependencies (only used for phar selfupdate command)
Patch0:         %{name}-rpm.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
%if %{with_tests}
BuildRequires:  php-composer(phpunit/phpunit)
BuildRequires:  php(language) >= 5.4
BuildRequires:  php-composer(nette/application) >= 2.2
BuildRequires:  php-composer(nette/bootstrap) >= 2.2
BuildRequires:  php-composer(nette/di) >= 2.2
BuildRequires:  php-composer(nette/neon) >= 2.2
BuildRequires:  php-composer(nette/mail) >= 2.2
BuildRequires:  php-composer(nette/robot-loader) >= 2.2
BuildRequires:  php-composer(nette/safe-stream) >= 2.2
BuildRequires:  php-composer(latte/latte) >= 2.2
BuildRequires:  php-composer(tracy/tracy) >= 2.2
BuildRequires:  php-composer(kukulich/fshl) >= 2.1
BuildRequires:  php-composer(andrewsville/php-token-reflection) >= 1.4
BuildRequires:  php-composer(michelf/php-markdown) >= 1.4
BuildRequires:  php-composer(kdyby/events) >= 2.0
BuildRequires:  php-composer(symfony/options-resolver) >= 2.6.1
BuildRequires:  php-composer(symfony/console) >= 2.6
BuildRequires:  php-composer(symfony/yaml) >= 2.6
BuildRequires:  php-composer(apigen/theme-default) >= 1.0.1
BuildRequires:  php-composer(apigen/theme-bootstrap) >= 1.1.2
BuildRequires:  php-iconv
BuildRequires:  php-mbstring
BuildRequires:  php-pcre
BuildRequires:  php-spl
BuildRequires:  php-tokenizer
BuildRequires:  php-zip
# Autoloader
BuildRequires:  php-composer(symfony/class-loader)
# from composer.json, "require-dev": {
#        "mockery/mockery": "~0.9",
#        "herrera-io/box": "~1.6"
# mockery 0.9.3 for autoloader
BuildRequires:  php-composer(mockery/mockery) >= 0.9.3
%endif

# from composer.json, "require": {
#        "php": ">=5.4",
#        "nette/application": "~2.2",
#        "nette/bootstrap": "~2.2",
#        "nette/di": "~2.2",
#        "nette/neon": "~2.2",
#        "nette/mail": "~2.2",
#        "nette/robot-loader": "~2.2",
#        "nette/safe-stream": "~2.2",
#        "latte/latte": ">=2.2.0,<2.3.5",
#        "tracy/tracy": "~2.2",
#        "kukulich/fshl": "~2.1",
#        "andrewsville/php-token-reflection": "~1.4",
#        "michelf/php-markdown": "~1.4",
#        "kdyby/events": "~2.0",
#        "symfony/options-resolver": "~2.6.1",
#        "symfony/console": "~2.6",
#        "symfony/yaml": "~2.6",
#        "herrera-io/phar-update": "~2.0",
#        "apigen/theme-default": "~1.0.1",
#        "apigen/theme-bootstrap": "~1.1.2"
Requires:       php(language) >= 5.4
Requires:       php-composer(nette/application) >= 2.2
Requires:       php-composer(nette/application) <  3
Requires:       php-composer(nette/bootstrap) >= 2.2
Requires:       php-composer(nette/bootstrap) <  3
Requires:       php-composer(nette/di) >= 2.2
Requires:       php-composer(nette/di) <  3
Requires:       php-composer(nette/neon) >= 2.2
Requires:       php-composer(nette/neon) <  3
Requires:       php-composer(nette/mail) >= 2.2
Requires:       php-composer(nette/mail) <  3
Requires:       php-composer(nette/robot-loader) >= 2.2
Requires:       php-composer(nette/robot-loader) <  3
Requires:       php-composer(nette/safe-stream) >= 2.2
Requires:       php-composer(nette/safe-stream) <  3
Requires:       php-composer(latte/latte) >= 2.2
# Max version 2.3.5 ignored
Requires:       php-composer(latte/latte) <  3
Requires:       php-composer(tracy/tracy) >= 2.2
Requires:       php-composer(tracy/tracy) <  3
Requires:       php-composer(kukulich/fshl) >= 2.1
Requires:       php-composer(kukulich/fshl) <  3
Requires:       php-composer(andrewsville/php-token-reflection) >= 1.4
Requires:       php-composer(andrewsville/php-token-reflection) <  2
Requires:       php-composer(michelf/php-markdown) >= 1.4
Requires:       php-composer(michelf/php-markdown) <  2
Requires:       php-composer(kdyby/events) >= 2.0
#Requires:       php-composer(kdyby/events) <  3
Requires:       php-composer(symfony/options-resolver) >= 2.6.1
Requires:       php-composer(symfony/options-resolver) <  3
Requires:       php-composer(symfony/console) >= 2.6
Requires:       php-composer(symfony/console) <  3
Requires:       php-composer(symfony/yaml) >= 2.6
Requires:       php-composer(symfony/yaml) <  3
Requires:       php-composer(apigen/theme-default) >= 1.0.1
Requires:       php-composer(apigen/theme-default) <  1.1
Requires:       php-composer(apigen/theme-bootstrap) >= 1.1.2
Requires:       php-composer(apigen/theme-bootstrap) <  1.2
# from phpcompatinfo report for version 4.1.1
Requires:       php-cli
Requires:       php-iconv
Requires:       php-mbstring
Requires:       php-pcre
Requires:       php-spl
Requires:       php-tokenizer
Requires:       php-zip
# Autoloader
Requires:       php-composer(symfony/class-loader)

# composer name
Provides:       php-composer(%{c_project}/%{c_project}) = %{version}
# php namespaced name, used in other distro
Provides:       php-%{c_project} = %{version}


%description
Smart and Readable Documentation for your PHP project.


%prep
%setup -q -n %{gh_project}-%{gh_commit}

%patch0 -p1 -b .rpm

rm -r tests/Herrera
rm -r src/Herrera
rm    src/Command/SelfUpdateCommand.php

find src -name \*rpm -exec rm {} \;

if grep -ri herrera src ; then
  : Herrera libraries still used review the patch
  exit 1
fi


%build
# Nothing


%install
rm -rf     %{buildroot}
mkdir -p   %{buildroot}%{_datadir}/php
cp -pr src %{buildroot}%{_datadir}/php/%{ns_vendor}

install -Dpm 755 bin/%{name} %{buildroot}%{_bindir}/%{name}

%check
%if %{with_tests}
: ignore some test with nette 2.4 - deprecation messages
rm tests/Templating/Filters/Helpers/LinkBuilderTest.php
rm tests/DI/ApiGenExtensionTest.php

sed -e 's:@BUILDROOT@:%{buildroot}:' -i tests/bootstrap.php
: Run test suite
%{_bindir}/phpunit --verbose

if which php70; then
  php70 %{_bindir}/phpunit --verbose
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
%{_bindir}/%{name}
%{_datadir}/php/%{ns_vendor}


%changelog
* Thu Aug  4 2016 Remi Collet <remi@fedoraproject.org> - 4.1.2-3
- ignore test failed because of deprecation messages
- ignore kdyby/events max version

* Wed Apr 13 2016 Remi Collet <remi@fedoraproject.org> - 4.1.2-2
- fix from review #1277504:
- drop /usr/share/apigen directory ownership
- add dependency on php-cli
- raise dependency on symfony/yaml >= 2.6

* Mon Nov 30 2015 Remi Collet <remi@fedoraproject.org> - 4.1.2-1
- update to 4.1.2

* Thu Nov  5 2015 Remi Collet <remi@fedoraproject.org> - 4.1.1-3
- add upstream patch: add condition for expected type
  https://github.com/ApiGen/ApiGen/issues/631

* Tue Nov  3 2015 Remi Collet <remi@fedoraproject.org> - 4.1.1-2
- drop herrera from dependencies (only used for phar
  selfupdate command)

* Sun Nov  1 2015 Remi Collet <remi@fedoraproject.org> - 4.1.1-1
- initial package
