# remirepo/fedora spec file for php-kukulich-fshl
#
# Copyright (c) 2015-2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    974c294ade5d76c0c16b6fe3fd3a584ba999b24f
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     kukulich
%global gh_project   fshl
%global php_home     %{_datadir}/php
%global ns_project   FSHL
%global with_tests   0%{!?_without_tests:1}

Name:           php-%{gh_owner}-%{gh_project}
Version:        2.1.0
Release:        4%{?dist}
Summary:        FSHL: fast syntax highlighter

Group:          Development/Libraries
License:        GPLv2+
URL:            http://fshl.kukulich.cz/
# git snashop to get upstream test suite
Source0:        %{name}-%{version}-%{gh_short}.tgz
Source1:        makesrc.sh

# https://github.com/kukulich/fshl/pull/13
Patch0:         %{name}-php71.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php-composer(theseer/autoload)
%if %{with_tests}
# For tests
BuildRequires:  php(language) >= 5.3
BuildRequires:  php-pcre
BuildRequires:  php-spl
BuildRequires:  php-composer(phpunit/phpunit)
%endif

# From composer.json, "require": {
#        "php": ">=5.3"
Requires:       php(language) >= 5.3
# From phpcompatinfo report for version 2.1.0
Requires:       php-pcre
Requires:       php-spl

Provides:       php-composer(%{gh_owner}/%{gh_project}) = %{version}


%description
FSHL is a free, open source, universal, fast syntax highlighter written in PHP.
A very fast parser performs syntax highlighting for few languages and produces
a HTML output.

To use this library, you just have to add, in your project:
  require_once '%{php_home}/%{ns_project}/autoload.php';


%prep
%setup -q -n %{gh_project}-%{gh_commit}
%patch0 -p1 -b .pr13


%build
: Generate a simple classmap autoloader
phpab --output %{ns_project}/autoload.php %{ns_project}


%install
rm -rf %{buildroot}

: Library
mkdir -p %{buildroot}%{php_home}
cp -pr %{ns_project} %{buildroot}%{php_home}/%{ns_project}


%check
%if %{with_tests}
: Switch to our autoloader
sed -e '/bootstrap/s:^.*$:require_once "%{buildroot}%{php_home}/%{ns_project}/autoload.php";:' \
    -i tests/%{ns_project}/*Test.php

ret=0
for cmd in php56 php70 php71 php; do
  if which $cmd; then
    $cmd %{_bindir}/phpunit --verbose tests || ret=1
  fi
done
exit $ret
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
%doc README.md
%{php_home}/%{ns_project}


%changelog
* Thu Feb 16 2017 Remi Collet <remi@fedoraproject.org> - 2.1.0-4
- open https://github.com/kukulich/fshl/issues/12 failed tests
- add patch from https://github.com/kukulich/fshl/pull/13
  workaround for failed test with PHP 7.1, fix FTBFS

* Wed Nov  4 2015 Remi Collet <remi@fedoraproject.org> - 2.1.0-2
- License is GPLv2+, from review #1277487

* Tue Oct 20 2015 Remi Collet <remi@fedoraproject.org> - 2.1.0-1
- initial package, version 2.1.0
