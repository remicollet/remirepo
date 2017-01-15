# remirepo/fedora spec file for php-nette-php-generator
#
# Copyright (c) 2015-2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    3f317dc211953cc93e9efa61598dc074adc3b0de
#global gh_date      20150728
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     nette
%global gh_project   php-generator
%global ns_vendor    Nette
%global ns_project   PhpGenerator
%global php_home     %{_datadir}/php
%global with_tests   0%{!?_without_tests:1}

Name:           php-%{gh_owner}-%{gh_project}
Version:        2.5.0
%global specrel 1
Release:        %{?gh_date:0.%{specrel}.%{?prever}%{!?prever:%{gh_date}git%{gh_short}}}%{!?gh_date:%{specrel}}%{?dist}
Summary:        Nette PHP Generator

Group:          Development/Libraries
License:        BSD or GPLv2 or GPLv3
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        %{name}-%{version}-%{gh_short}.tgz
# pull a git snapshot to get test sutie
Source1:        makesrc.sh

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php-composer(theseer/autoload)
%if %{with_tests}
BuildRequires:  php(language) >= 5.6
BuildRequires:  php-pcre
BuildRequires:  php-reflection
BuildRequires:  php-composer(%{gh_owner}/utils)  >= 2.4
# From composer.json, "require-dev": {
#               "nette/tester": "~2.0",
#               "tracy/tracy": "^2.3"
# ignore tracy (pass without)
BuildRequires:  php-composer(%{gh_owner}/tester) >= 2.0
%endif

# from composer.json, "require": {
#               "php": ">=5.6.0",
#               "nette/utils": "~2.4"
Requires:       php(language) >= 5.6
Requires:       php-composer(%{gh_owner}/utils) >= 2.4
Requires:       php-composer(%{gh_owner}/utils) <  3
# from phpcompatinfo report for version 2.3.4
Requires:       php-pcre
Requires:       php-reflection

Provides:       php-composer(%{gh_owner}/%{gh_project}) = %{version}


%description
Generate PHP code with a simple programmatical API.

To use this library, you just have to add, in your project:
  require_once '%{php_home}/%{ns_vendor}/%{ns_project}/autoload.php';


%prep
%setup -q -n %{gh_project}-%{gh_commit}


%build
: Generate a classmap autoloader
phpab --output src/%{ns_project}/autoload.php src

cat << 'EOF' | tee -a src/%{ns_project}/autoload.php
// Dependencies
require_once '%{php_home}/%{ns_vendor}/Utils/autoload.php';
EOF


%install
rm -rf       %{buildroot}
mkdir -p     %{buildroot}%{php_home}/%{ns_vendor}
cp -pr src/* %{buildroot}%{php_home}/%{ns_vendor}/


%check
%if %{with_tests}
export LANG=fr_FR.utf8

: Generate autoloader
mkdir vendor
cat << 'EOF' | tee vendor/autoload.php
<?php
require_once '%{php_home}/Tester/autoload.php';
require_once '%{buildroot}%{php_home}/%{ns_vendor}/%{ns_project}/autoload.php';
EOF

: Run test suite in sources tree
# remirepo:11
ret=0
run=0
if which php56; then
   php56 %{_bindir}/nette-tester --colors 0 -p php56 -C tests -s || ret=1
   run=1
fi
if which php71; then
   php71 %{_bindir}/nette-tester --colors 0 -p php71 -C tests -s || ret=1
   run=1
fi
if [ $run -eq 0 ]; then
%{_bindir}/nette-tester --colors 0 -p php -C tests -s
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
%{php_home}/%{ns_vendor}/%{ns_project}


%changelog
* Sun Jan 15 2017 Remi Collet <remi@fedoraproject.org> - 2.5.0-1
- update to 2.5.0

* Tue Aug  2 2016 Remi Collet <remi@fedoraproject.org> - 2.4.1-1
- update to 2.4.1
- raise dependency on PHP >= 5.6
- raise dependency on nette/utils >= 2.4

* Mon Jun 20 2016 Remi Collet <remi@fedoraproject.org> - 2.3.6-1
- update to 2.3.6

* Thu Dec  3 2015 Remi Collet <remi@fedoraproject.org> - 2.3.5-1
- update to 2.3.5
- run test suite with both php 5 and 7 when available

* Tue Oct 20 2015 Remi Collet <remi@fedoraproject.org> - 2.3.4-1
- initial package
