# remirepo/fedora spec file for php-nette-tester
#
# Copyright (c) 2015-2016 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    7d29c02f3216a1c4debe4c6475830b5884786922
%global gh_date      20160714
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     nette
%global gh_project   tester
%global php_home     %{_datadir}/php
%global with_tests   0%{!?_without_tests:1}

Name:           php-nette-tester
Version:        2.0.0
%global specrel 1
Release:        %{?gh_date:0.%{specrel}.%{?prever}%{!?prever:%{gh_date}git%{gh_short}}}%{!?gh_date:%{specrel}}%{?dist}
Summary:        An easy-to-use PHP unit testing framework

Group:          Development/Libraries
License:        BSD or GPLv2 or GPLv3
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        %{name}-%{version}-%{gh_short}.tgz
Source1:        makesrc.sh

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php-composer(theseer/autoload)
%if %{with_tests}
BuildRequires:  php(language) >= 5.4
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
%if 0%{?fedora} >= 24
BuildRequires:  glibc-langpack-fr
%endif
%endif

# from composer.json
#        "php": ">=5.4.0"
Requires:       php(language) >= 5.4
# from phpcompatinfo report for version 2.0.0
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
# NOTICE: -C seems to doesn't work for tester itself
cat /etc/php.ini /etc/php.d/*ini >php.ini
export LANG=fr_FR.utf8

# remirepo:13
ret=0
run=0
if which php56; then
   cat /opt/remi/php56/root/etc/php.ini /opt/remi/php56/root/etc/php.d/*ini >php.ini
   php56 src/tester.php --colors 0 -p php56 -c ./php.ini tests -s || ret=1
   run=1
fi
if which php71; then
   cat /etc/opt/remi/php71/php.ini /etc/opt/remi/php71/php.d/*ini >php.ini
   php71 src/tester.php --colors 0 -p php71 -c ./php.ini tests -s || ret=1
   run=1
fi
if [ $run -eq 0 ]; then
php src/tester.php --colors 0 -p php -c ./php.ini tests -s
# remirepo:2
fi
exit $ret
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
* Tue Aug  2 2016 Remi Collet <remi@fedoraproject.org> - 2.0.0-0.1.20160414git7d29c02
- update to 2.0.0-dev

* Sun Mar 20 2016 Remi Collet <remi@fedoraproject.org> - 1.7.1-1
- update to 1.7.1
- sources from git snapshot
  open https://github.com/nette/tester/issues/297
- add BR glibc-langpack-fr on F24+

* Fri Feb 12 2016 Remi Collet <remi@fedoraproject.org> - 1.7.0-1
- update to 1.7.0
- run test suite with both PHP 5 and 7 when available

* Tue Nov  3 2015 Remi Collet <remi@fedoraproject.org> - 1.6.1-1
- update to 1.6.1

* Tue Oct 20 2015 Remi Collet <remi@fedoraproject.org> - 1.6.0-1
- initial package
