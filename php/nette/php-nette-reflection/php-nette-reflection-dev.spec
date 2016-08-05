# remirepo/fedora spec file for php-nette-reflection
#
# Copyright (c) 2015-2016 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    1922f2502e5d2bf6be51859721855e8e72ebde96
#global gh_date      20150728
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     nette
%global gh_project   reflection
%global ns_vendor    Nette
%global ns_project   Reflection
%global php_home     %{_datadir}/php
%global with_tests   0%{!?_without_tests:1}

Name:           php-%{gh_owner}-%{gh_project}
Version:        2.4.0
%global specrel 1
Release:        %{?gh_date:0.%{specrel}.%{?prever}%{!?prever:%{gh_date}git%{gh_short}}}%{!?gh_date:%{specrel}}%{?dist}
Summary:        Nette PHP Reflection Component

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
BuildRequires:  php-tokenizer
BuildRequires:  php-pcre
BuildRequires:  php-reflection
BuildRequires:  php-composer(%{gh_owner}/caching) >= 2.2
BuildRequires:  php-composer(%{gh_owner}/utils) >= 2.4
# From composer.json, "require-dev": {
#               "nette/di": "~2.3",
#               "nette/tester": "~2.0",
#               "tracy/tracy": "^2.3"
BuildRequires:  php-composer(%{gh_owner}/di) >= 2.3
BuildRequires:  php-composer(%{gh_owner}/tester) >= 2.0
BuildRequires:  php-composer(tracy/tracy) >= 2.3
%endif

# from composer.json, "require": {
#        "php": ">=5.6.0"
#        "ext-tokenizer": "*",
#        "nette/caching": "~2.2",
#        "nette/utils": "~2.4"
Requires:       php(language) >= 5.6
Requires:       php-tokenizer
Requires:       php-composer(%{gh_owner}/caching) >= 2.2
Requires:       php-composer(%{gh_owner}/caching) <  3
Requires:       php-composer(%{gh_owner}/utils) >= 2.4
Requires:       php-composer(%{gh_owner}/utils) <  3
# from phpcompatinfo report for version 2.3.1
Requires:       php-reflection
Requires:       php-pcre

Provides:       php-composer(%{gh_owner}/%{gh_project}) = %{version}


%description
If you need to find every information about any class, reflection is the
right tool to do it. You can easily find out which methods does any class
have, what parameters do those methods accept, etc.

Nette\Object simplifies access to class' self-reflection with method
getReflection(), returning a Nette\Reflection\ClassType object.

To use this library, you just have to add, in your project:
  require_once '%{php_home}/%{ns_vendor}/%{ns_project}/autoload.php';


%prep
%setup -q -n %{gh_project}-%{gh_commit}


%build
: Generate a classmap autoloader
phpab --output src/%{ns_project}/autoload.php src

cat << 'EOF' | tee -a src/%{ns_project}/autoload.php
// Dependencies
require_once '%{php_home}/%{ns_vendor}/Caching/autoload.php';
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
require_once '%{php_home}/%{ns_vendor}/DI/autoload.php';
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
%{php_home}/%{ns_vendor}/Bridges/ReflectionDI


%changelog
* Thu Aug  4 2016 Remi Collet <remi@fedoraproject.org> - 2.4.0-1
- update to 2.4.0
- raise dependency on PHP >= 5.6
- raise dependency on nette/utils >= 2.4

* Sat Apr  2 2016 Remi Collet <remi@fedoraproject.org> - 2.3.2-1
- update to 2.3.2
- run test suite with both php 5 and 7 when available

* Tue Oct 20 2015 Remi Collet <remi@fedoraproject.org> - 2.3.1-1
- initial package
