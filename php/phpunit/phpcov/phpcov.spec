# spec file for phpcov
#
# Copyright (c) 2013-2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    7deaf8868283d8f18b131093cd39211ad159b3ac
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     sebastianbergmann
%global gh_project   phpcov
%global php_home     %{_datadir}/php
%global with_tests   0%{!?_without_tests:1}
# Packagist
%global pk_vendor    phpunit
%global pk_project   phpcov
# Namespace
%global ns_vendor    SebastianBergmann
%global ns_project   PHPCOV


Name:           %{pk_project}
Version:        4.0.0
Release:        1%{?dist}
Summary:        CLI frontend for PHP_CodeCoverage

Group:          Development/Libraries
License:        BSD
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}-%{gh_short}.tar.gz

# Fix autoload for RPM
Patch0:         %{gh_project}-rpm.patch

BuildArch:      noarch
BuildRequires:  php(language) >= 7.0
BuildRequires:  php-fedora-autoloader-devel
%if %{with_tests}
BuildRequires:  phpunit6
BuildRequires:  php-composer(phpunit/php-code-coverage) <  6
BuildRequires:  php-composer(phpunit/php-code-coverage) >= 5.0
BuildRequires:  php-composer(sebastian/diff) <  2
BuildRequires:  php-composer(sebastian/diff) >= 1.1
BuildRequires:  php-composer(sebastian/finder-facade) <  2
BuildRequires:  php-composer(sebastian/finder-facade) >= 1.1
BuildRequires:  php-composer(sebastian/version) <  3
BuildRequires:  php-composer(sebastian/version) >= 2.0
BuildRequires:  php-composer(symfony/console) >= 2.8
BuildRequires:  php-pecl(Xdebug)
%endif

# from composer.json
#        "php": "^7.0",
#        "phpunit/phpunit": "^6.0",
#        "phpunit/php-code-coverage": "^5.0",
#        "sebastian/diff": "^1.1",
#        "sebastian/finder-facade": "^1.1",
#        "sebastian/version": "^2.0",
#        "symfony/console": "^3"
Requires:       php(language) >= 7.0
Requires:       phpunit6
Requires:       php-composer(phpunit/php-code-coverage) <  6
Requires:       php-composer(phpunit/php-code-coverage) >= 5.0
Requires:       php-composer(sebastian/diff) <  2
Requires:       php-composer(sebastian/diff) >= 1.1
Requires:       php-composer(sebastian/finder-facade) <  2
Requires:       php-composer(sebastian/finder-facade) >= 1.1
Requires:       php-composer(sebastian/version) <  3
Requires:       php-composer(sebastian/version) >= 2.0
Requires:       php-composer(symfony/console) <  4
# temporarily ignore min version
Requires:       php-composer(symfony/console) >= 2.8
# from phpcompatinfo report for version 4.0.0
# none

%if 0%{?fedora} >= 25
Obsoletes:      php-phpunit-phpcov < 4
Provides:       php-phpunit-phpcov = %{version}
%else
Conflicts:      php-phpunit-phpcov < 4
%endif
Provides:       php-composer(%{pk_vendoir}/%{pk_project}) = %{version}


%description
%{pk_project} is a command-line frontend for the PHP_CodeCoverage library.


%prep
%setup -q -n %{gh_project}-%{gh_commit}

%patch0 -p0 -b .rpm


%build
phpab \
  --template fedora \
  --output   src/autoload.php \
  src

cat << 'EOF' | tee -a src/autoload.php
// Dependencies
\Fedora\Autoloader\Dependencies::required([
    '%{php_home}/PHPUnit6/autoload.php',
    '%{php_home}/%{ns_vendor}/CodeCoverage5/autoload.php',
    '%{php_home}/%{ns_vendor}/Diff/autoload.php',
    '%{php_home}/%{ns_vendor}/FinderFacade/autoload.php',
    '%{php_home}/%{ns_vendor}/Version/autoload.php',
    [
        '%{php_home}/Symfony3/Component/Console/autoload.php',
        '%{php_home}/Symfony/Component/Console/autoload.php',
    ]
]);
EOF


%install
mkdir -p   %{buildroot}%{php_home}/%{ns_vendor}
cp -pr src %{buildroot}%{php_home}/%{ns_vendor}/%{ns_project}

install -D -p -m 755 %{pk_project} %{buildroot}%{_bindir}/%{pk_project}


%check
%if %{with_tests}
mkdir vendor
ln -s %{buildroot}%{php_home}/%{ns_vendor}/%{ns_project}/autoload.php vendor/autoload.php

%{_bindir}/phpunit6 --verbose
%else
: Test suite skipped
%endif


%files
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc README.md
%doc composer.json
%{php_home}/%{ns_vendor}/%{ns_project}
%{_bindir}/%{pk_project}


%changelog
* Wed Feb  8 2017 Remi Collet <remi@fedoraproject.org> - 4.0.0-1
- rename to phpcov
- update to 4.0.0
- change dependencies to PHPUnit v6

* Fri Jun  3 2016 Remi Collet <remi@fedoraproject.org> - 3.1.0-1
- Update to 3.1.0
- raise dependency on phpunit/php-code-coverage >= 4.0
- drop the autoloader template, simply generate it

* Mon Apr 18 2016 Remi Collet <remi@fedoraproject.org> - 3.0.0-3
- allow sebastian/version 2.0

* Sat Jan  9 2016 Remi Collet <remi@fedoraproject.org> - 3.0.0-1
- update to 3.0.0
- raise minimal PHP version to 5.6
- raise dependencies on phpunit ~5.0, php-code-coverage ~3.0
- allow symfony 3
- run test suite with both PHP 6 and 7 when available

* Mon Oct  5 2015 Remi Collet <remi@fedoraproject.org> - 2.0.2-1
- update to 2.0.2
- allow PHPUnit 5

* Wed Jun 25 2014 Remi Collet <remi@fedoraproject.org> - 2.0.1-1
- update to 2.0.1
- composer dependencies

* Wed Apr 30 2014 Remi Collet <remi@fedoraproject.org> - 2.0.0-1
- update to 2.0.0
- sources from github

* Thu Sep 12 2013 Remi Collet <remi@fedoraproject.org> - 1.1.0-1
- initial package
