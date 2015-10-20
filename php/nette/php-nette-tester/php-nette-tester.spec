# remirepo/fedora spec file for php-nette-tester
#
# Copyright (c) 2015 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    e4cd7409ee25b6c16bc80717ef58abe4cb589cff
#global gh_date      20150728
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     nette
%global gh_project   tester
%global php_home     %{_datadir}/php
%global with_tests   0%{!?_without_tests:1}

Name:           php-nette-tester
Version:        1.6.0
%global specrel 1
Release:        %{?gh_date:0.%{specrel}.%{?prever}%{!?prever:%{gh_date}git%{gh_short}}}%{!?gh_date:%{specrel}}%{?dist}
Summary:        An easy-to-use PHP unit testing framework

Group:          Development/Libraries
License:        BSD or GPLv2 or GPLv3
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}-%{gh_short}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php(language) >= 5.3
BuildRequires:  php-composer(theseer/autoload)
%if %{with_tests}
BuildRequires:  php-cli
BuildRequires:  php-date
BuildRequires:  php-dom
BuildRequires:  php-libxml
BuildRequires:  php-pcntl
BuildRequires:  php-pcre
BuildRequires:  php-posix
BuildRequires:  php-reflection
BuildRequires:  php-simplexml
BuildRequires:  php-spl
BuildRequires:  php-tokenizer
%endif

# from composer.json
#        "php": ">=5.3.0"
Requires:       php(language) >= 5.3
# from phpcompatinfo report for version 1.0.0: nothing
Requires:       php-cli
Requires:       php-date
Requires:       php-dom
Requires:       php-libxml
Requires:       php-pcntl
Requires:       php-pcre
Requires:       php-posix
Requires:       php-reflection
Requires:       php-simplexml
Requires:       php-spl
Requires:       php-tokenizer

Provides:       php-composer(%{gh_owner}/%{gh_project}) = %{version}


%description
Nette Tester is a productive and enjoyable unit testing framework.
It's used by the Nette Framework and is capable of testing any PHP code.


%prep
%setup -q -n %{gh_project}-%{gh_commit}

: Rename as "tester" seems too generic
mv src/tester nette-tester

: Fix runner path in launcher
sed -e "s:__DIR__:'%{php_home}/Tester':" -i nette-tester


%build
: Generate a classmap autoloader
phpab --output src/autoload.php src


%install
rm -rf     %{buildroot}
mkdir -p   %{buildroot}%{php_home}
cp -pr src %{buildroot}%{php_home}/Tester

install -Dpm 755 nette-tester %{buildroot}%{_bindir}/nette-tester


%check
%if %{with_tests}
: Generate configuration
cat /etc/php.ini /etc/php.d/*ini >php.ini
export LANG=fr_FR.utf8

: Run test suite in sources tree
php src/tester.php --colors 0 -p php -c ./php.ini tests -s
%else
: Test suite disabled
%endif


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license license.md
%doc readme.md contributing.md
%doc composer.json
%{php_home}/Tester
%{_bindir}/nette-tester


%changelog
* Tue Oct 20 2015 Remi Collet <remi@fedoraproject.org> - 1.6.0-1
- initial package