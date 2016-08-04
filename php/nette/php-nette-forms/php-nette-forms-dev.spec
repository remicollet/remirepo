# remirepo/fedora spec file for php-nette-forms
#
# Copyright (c) 2015-2016 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    57295d16f8e90173465735eb6be49a1e3ce614bd
#global gh_date      20150728
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     nette
%global gh_project   forms
%global ns_vendor    Nette
%global ns_project   Forms
%global php_home     %{_datadir}/php
%global with_tests   0%{!?_without_tests:1}

Name:           php-%{gh_owner}-%{gh_project}
Version:        2.4.1
%global specrel 1
Release:        %{?gh_date:0.%{specrel}.%{?prever}%{!?prever:%{gh_date}git%{gh_short}}}%{!?gh_date:%{specrel}}%{?dist}
Summary:        Nette Forms: greatly facilitates web forms

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
BuildRequires:  php-composer(%{gh_owner}/component-model) >= 2.3
BuildRequires:  php-composer(%{gh_owner}/http) >= 2.2
BuildRequires:  php-composer(%{gh_owner}/utils) >= 2.4
BuildRequires:  php-pcre
BuildRequires:  php-spl
# From composer.json, "require-dev": {
#        "nette/di": "~2.4",
#        "nette/tester": "~2.0"
#        "latte/latte": "~2.4"
#        "tracy/tracy": "~2.4"
BuildRequires:  php-composer(%{gh_owner}/di) >= 2.4
BuildRequires:  php-composer(%{gh_owner}/tester) >= 2.0
BuildRequires:  php-composer(latte/latte) >= 2.4
BuildRequires:  php-composer(tracy/tracy) >= 2.4
%endif

# from composer.json, "require": {
#        "php": ">=5.6.0"
#        "nette/component-model": "~2.3",
#        "nette/http": "~2.2",
#        "nette/utils": "~2.4"
Requires:       php(language) >= 5.6
Requires:       php-composer(%{gh_owner}/component-model) >= 2.3
Requires:       php-composer(%{gh_owner}/component-model) <  3
Requires:       php-composer(%{gh_owner}/http) >= 2.2
Requires:       php-composer(%{gh_owner}/http) <  3
Requires:       php-composer(%{gh_owner}/utils) >= 2.4
Requires:       php-composer(%{gh_owner}/utils) <  3
# from phpcompatinfo report for version 2.4.1
Requires:       php-pcre
Requires:       php-spl

Provides:       php-composer(%{gh_owner}/%{gh_project}) = %{version}


%description
Nette\Forms greatly facilitates creating and processing web forms.
What it can really do?
- validate sent data both client-side (JavaScript) and server-side
- provide high level of security
- multiple render modes
- translations, i18n

To use this library, you just have to add, in your project:
  require_once '%{php_home}/%{ns_vendor}/%{ns_project}/autoload.php';


%prep
%setup -q -n %{gh_project}-%{gh_commit}


%build
: Generate a classmap autoloader
phpab --output src/%{ns_project}/autoload.php src

cat << 'EOF' | tee -a src/%{ns_project}/autoload.php
// Dependencies
require_once '%{php_home}/%{ns_vendor}/ComponentModel/autoload.php';
require_once '%{php_home}/%{ns_vendor}/Http/autoload.php';
require_once '%{php_home}/%{ns_vendor}/Utils/autoload.php';
EOF


%install
rm -rf       %{buildroot}

mkdir -p     %{buildroot}%{php_home}/%{ns_vendor}
cp -pr src/* %{buildroot}%{php_home}/%{ns_vendor}/

# Notice: don't install assets, only used in tests
rm -rf       %{buildroot}%{php_home}/%{ns_vendor}/assets


%check
%if %{with_tests}
: Generate configuration
cat /etc/php.ini /etc/php.d/*ini   >php.ini
echo 'session.save_path = "/tmp"' >>php.ini
export LANG=fr_FR.utf8

: Generate autoloader
mkdir vendor
cat << 'EOF' | tee vendor/autoload.php
<?php
require_once '%{php_home}/Tester/autoload.php';
require_once '%{php_home}/Latte/autoload.php';
require_once '%{php_home}/Tracy/autoload.php';
require_once '%{php_home}/%{ns_vendor}/DI/autoload.php';
require_once '%{buildroot}%{php_home}/%{ns_vendor}/%{ns_project}/autoload.php';
EOF

: Run test suite in sources tree
# remirepo:15
run=0
ret=0
if which php56; then
   cat /opt/remi/php56/root/etc/php.ini /opt/remi/php56/root/etc/php.d/*ini >php.ini
   echo 'session.save_path = "/tmp"' >>php.ini
   php56 %{_bindir}/nette-tester --colors 0 -p php56 -c ./php.ini tests -s
   run=1
fi
if which php70; then
   cat /etc/opt/remi/php70/php.ini /etc/opt/remi/php70/php.d/*ini >php.ini
   echo 'session.save_path = "/tmp"' >>php.ini
   php70 %{_bindir}/nette-tester --colors 0 -p php70 -c ./php.ini tests -s
   run=1
fi
if [ $run -eq 0 ]; then
%{_bindir}/nette-tester --colors 0 -p php -c ./php.ini tests -s
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
%doc src/assets
%doc examples
%{php_home}/%{ns_vendor}/%{ns_project}
%{php_home}/%{ns_vendor}/Bridges


%changelog
* Thu Aug  4 2016 Remi Collet <remi@fedoraproject.org> - 2.4.1-1
- update to 2.4.1
- raise dependency on PHP >= 5.6
- raise dependency on nette/utils >= 2.4
- raise dependency on nette/component-model >= 2.3

* Fri Jul  1 2016 Remi Collet <remi@fedoraproject.org> - 2.3.10-1
- update to 2.3.10
- raise dependency on nette/utils ~2.3.10

* Wed Jun  1 2016 Remi Collet <remi@fedoraproject.org> - 2.3.9-1
- update to 2.3.9

* Sat Feb 20 2016 Remi Collet <remi@fedoraproject.org> - 2.3.8-1
- update to 2.3.8

* Wed Jan 20 2016 Remi Collet <remi@fedoraproject.org> - 2.3.7-1
- update to 2.3.7
- run test suite with both php 5 and 7 when available

* Tue Oct 20 2015 Remi Collet <remi@fedoraproject.org> - 2.3.6-1
- initial package
