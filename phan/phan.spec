# remirepo/fedora spec file for phan
#
# Copyright (c) 2016 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    ea92e93008491b780fbaf3e97487845e3f60c78f
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     etsy
#global gh_date      20150820
%global gh_project   phan
%global psr0         Phan
%global with_tests   0%{!?_without_tests:1}

Name:           %{gh_project}
Version:        0.6
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
BuildRequires:  php(language) >= 7.0
BuildRequires:  php-ast
BuildRequires:  php-sqlite3
BuildRequires:  php-composer(symfony/console) >= 2.8
BuildRequires:  php-reflection
BuildRequires:  php-pcntl
BuildRequires:  php-pcre
BuildRequires:  php-posix
BuildRequires:  php-spl
BuildRequires:  php-sysvmsg
BuildRequires:  php-sysvsem
# For tests, from composer.json "require-dev": {
#        "phpunit/phpunit": "~5",
#        "phpdocumentor/phpdocumentor": "dev-master",
#        "squizlabs/php_codesniffer": "^2.5"
BuildRequires:  php-composer(phpunit/phpunit) >= 5
%endif
# For autoloader
BuildRequires:  php-composer(fedora/autoloader)

# From composer.json, "require": {
#        "php": ">=7.0",
#        "ext-ast": "*",
#        "ext-sqlite3": "0.7-dev",
#        "symfony/console": "~2.3|~3.0"
Requires:       php(language) >= 7.0
Requires:       php-ast
Requires:       php-sqlite3
Requires:       php-composer(symfony/console) >= 2.3
# From phpcompatinfo report for 0.6
Requires:       php-cli
Requires:       php-reflection
Requires:       php-pcntl
Requires:       php-pcre
Requires:       php-posix
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
mkdir vendor
cat << 'EOF' | tee vendor/autoload.php
<?php
require '%{buildroot}%{_datadir}/php/%{psr0}/Bootstrap.php';
\Fedora\Autoloader\Autoload::addPsr4('Phan\\Tests\\', dirname(__DIR__).'/tests/Phan');
EOF

%{_bindir}/phpunit -d memory_limit=1G --bootstrap vendor/autoload.php --verbose
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
* Thu Nov 24 2016 Remi Collet <remi@fedoraproject.org> - 0.6-1
- initial package

