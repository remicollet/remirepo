# remirepo/fedora spec file for php-tedivm-jshrink
#
# Copyright (c) 2015-2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    688527a2e854d7935f24f24c7d5eb1b604742bf9
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     tedious
#global gh_date      20150820
%global gh_project   JShrink
%global c_vendor     tedivm
%global c_project    jshrink
%global with_tests   0%{!?_without_tests:1}
%global psr0         JShrink

Name:           php-%{c_vendor}-%{c_project}
Version:        1.1.0
Release:        1%{?gh_date?%{gh_date}git%{gh_short}}%{?dist}
Summary:        Javascript Minifier built in PHP

Group:          Development/Libraries
License:        BSD
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}-%{?gh_short}.tar.gz

Source1:        %{name}-autoload.php

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
%if %{with_tests}
BuildRequires:  php(language) >= 5.3.0
BuildRequires:  php-date
BuildRequires:  php-pcre
BuildRequires:  php-spl
# For tests, from composer.json "require-dev": {
#      "phpunit/phpunit": "4.0.*",
#      "fabpot/php-cs-fixer": "0.4.0",
#      "satooshi/php-coveralls": "dev-master"
BuildRequires:  php-composer(phpunit/phpunit) >= 4
%endif
# For autoloader
BuildRequires:  php-composer(symfony/class-loader)

# From composer.json, "require": {
#    "php": ">=5.3.0"
Requires:       php(language) >= 5.3.0
# From phpcompatinfo report for 1.1.0
Requires:       php-date
Requires:       php-pcre
Requires:       php-spl
# Autoloader
Requires:       php-composer(symfony/class-loader)

# Composer
Provides:       php-composer(%{c_vendor}/%{c_project}) = %{version}


%description
JShrink is a php class that minifies javascript so that it can be delivered
to the client quicker. This code can be used by any product looking to minify
their javascript on the fly (although caching the results is suggested for
performance reasons). Unlike many other products this is not a port into php
but a native application, resulting in better performance.

To use this library, you just have to add, in your project:
  require_once '%{_datadir}/php/%{psr0}/autoload.php';


%prep
%setup -q -n %{gh_project}-%{gh_commit}

cp %{SOURCE1} src/%{psr0}/autoload.php


%build


%install
rm -rf       %{buildroot}
mkdir -p     %{buildroot}%{_datadir}/php
cp -pr src/* %{buildroot}%{_datadir}/php


%check
%if %{with_tests}
mkdir vendor
cat << 'EOF' | tee tests/bootstrap.php
<?php
require '%{buildroot}%{_datadir}/php/%{psr0}/autoload.php';
EOF

%{_bindir}/phpunit --verbose
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


%changelog
* Tue Oct 27 2015 Remi Collet <remi@fedoraproject.org> - 1.1.0-1
- initial package