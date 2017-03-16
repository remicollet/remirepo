# remirepo/fedora spec file for phan
#
# Copyright (c) 2016-2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    eadb20b627f97a7ce5bf3353e86f9820e34fa61c
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     etsy
#global gh_date      20150820
%global gh_project   phan
%global psr0         Phan
%global with_tests   0%{!?_without_tests:1}

Name:           %{gh_project}
Version:        0.9.1
Release:        1%{?gh_date?%{gh_date}git%{gh_short}}%{?dist}
Summary:        A static analyzer for PHP

Group:          Development/Libraries
License:        MIT
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}-%{?gh_short}.tar.gz

# Use fedora autoloader
Source1:        %{name}-autoload.php
Patch0:         %{name}-autoload.patch

BuildArch:      noarch
%if %{with_tests}
BuildRequires:  php(language) >= 7.1
BuildRequires:  php-ast >= 0.1.4
BuildRequires:  php-composer(symfony/console) >= 2.8
BuildRequires:  php-reflection
BuildRequires:  php-pcntl
BuildRequires:  php-pcre
BuildRequires:  php-posix
BuildRequires:  php-spl
BuildRequires:  php-sysvmsg
BuildRequires:  php-sysvsem
# For tests, from composer.json "require-dev": {
#        "phpunit/phpunit": "^5.7.2"
BuildRequires:  php-composer(phpunit/phpunit) >= 5.7.2
%endif
# For autoloader
BuildRequires:  php-composer(fedora/autoloader)

# From composer.json, "require": {
#        "php": "~7.1.0",
#        "ext-ast": "^0.1.4",
#        "symfony/console": "~2.3|~3.0"
Requires:       php(language) >= 7.1
Requires:       php-ast >= 0.1.4
Requires:       php-composer(symfony/console) >= 2.3
# From phpcompatinfo report for 0.8.0
Requires:       php-cli
Requires:       php-reflection
Requires:       php-pcntl
Requires:       php-pcre
Requires:       php-posix
Requires:       php-readline
Requires:       php-spl
Requires:       php-sysvmsg
Requires:       php-sysvsem
# For autoloader
Requires:       php-composer(fedora/autoloader)

# Composer
Provides:       php-composer(%{gh_owner}/%{gh_project}) = %{version}


%description
Phan is a static analyzer that looks for common issues and will verify type
compatibility on various operations when type information is available or can
be deduced. Phan does not make any serious attempt to understand flow control
and narrow types based on conditionals.


%prep
%setup -q -n %{gh_project}-%{gh_commit}

%patch0 -p1
cp %{SOURCE1} src/%{psr0}/autoload.php


%build
: Nothing to build


%install
: Library
mkdir -p           %{buildroot}%{_datadir}/php
cp -pr src/%{psr0} %{buildroot}%{_datadir}/php/%{psr0}

: Relocated tools
cp -pr src/*php    %{buildroot}%{_datadir}/php/%{psr0}/
install -Dpm 755 src/phan.php %{buildroot}%{_datadir}/php/%{psr0}/phan.php
install -Dpm 755 src/prep.php %{buildroot}%{_datadir}/php/%{psr0}/prep.php

: Commands
mkdir -p %{buildroot}%{_bindir}
ln -s ../share/php/%{psr0}/phan.php %{buildroot}%{_bindir}/phan
ln -s ../share/php/%{psr0}/prep.php %{buildroot}%{_bindir}/phan-prep


%check
%if %{with_tests}
cat << 'EOF' | tee tests/autoload.php
<?php
require '%{buildroot}%{_datadir}/php/%{psr0}/Bootstrap.php';
\Fedora\Autoloader\Autoload::addPsr4('Phan\\Tests\\', __DIR__ . '/Phan');
EOF

%{_bindir}/phpunit -d memory_limit=1G --bootstrap tests/autoload.php --verbose


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
%{_datadir}/php/%{psr0}
%{_bindir}/phan*


%changelog
* Thu Mar 16 2017 Remi Collet <remi@remirepo.net> - 0.9.1-1
- Update to 0.9.1
- raise dependency on PHP 7.1
- raise dependency on ast 0.1.4

* Fri Jan 27 2017 Remi Collet <remi@remirepo.net> - 0.8.3-1
- update to 0.8.3

* Thu Jan 26 2017 Remi Collet <remi@remirepo.net> - 0.8.2-1
- update to 0.8.2

* Wed Jan 25 2017 Remi Collet <remi@fedoraproject.org> - 0.8.0-1
- update to 0.8.0

* Fri Dec  9 2016 Remi Collet <remi@fedoraproject.org> - 0.7-1
- update to 0.7

* Thu Nov 24 2016 Remi Collet <remi@fedoraproject.org> - 0.6-1
- initial package

