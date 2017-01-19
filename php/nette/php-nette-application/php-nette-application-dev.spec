# remirepo/fedora spec file for php-nette-application
#
# Copyright (c) 2015-2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    3e30a1ec941717668bcdab336d690484700207cd
#global gh_date      20150728
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     nette
%global gh_project   application
%global ns_vendor    Nette
%global ns_project   Application
%global php_home     %{_datadir}/php
%global with_tests   0%{!?_without_tests:1}

Name:           php-%{gh_owner}-%{gh_project}
Version:        2.4.4
%global specrel 1
Release:        %{?gh_date:0.%{specrel}.%{?prever}%{!?prever:%{gh_date}git%{gh_short}}}%{!?gh_date:%{specrel}}%{?dist}
Summary:        Nette Application MVC Component

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
BuildRequires:  php-composer(%{gh_owner}/reflection) >= 2.2
BuildRequires:  php-composer(%{gh_owner}/utils) >= 2.4
BuildRequires:  php-pcre
BuildRequires:  php-reflection
BuildRequires:  php-spl
# From composer.json, "require-dev": {
#               "nette/tester": "~2.0",
#               "nette/di": "~2.4",
#               "nette/forms": "~2.4",
#               "nette/robot-loader": "~2.4.2 || ^3.0",
#               "nette/security": "~2.4",
#               "latte/latte": "^2.4.1",
#               "tracy/tracy": "^2.4",
#               "mockery/mockery": "^0.9.5"
BuildRequires:  php-composer(%{gh_owner}/tester) >= 2.0
BuildRequires:  php-composer(%{gh_owner}/di) >= 2.4
BuildRequires:  php-composer(%{gh_owner}/forms) >= 2.4
BuildRequires:  php-composer(%{gh_owner}/robot-loader) >= 2.4.2
BuildRequires:  php-composer(%{gh_owner}/security) >= 2.4
BuildRequires:  php-composer(latte/latte) >= 2.4.1
BuildRequires:  php-composer(tracy/tracy) >= 2.4
BuildRequires:  php-composer(mockery/mockery) >= 0.9.5
%endif

# from composer.json, "require": {
#        "php": ">=5.6.0"
#        "nette/component-model": "~2.3",
#        "nette/http": "~2.2",
#        "nette/reflection": "~2.2",
#        "nette/utils": "~2.4"
Requires:       php(language) >= 5.6
Requires:       php-composer(%{gh_owner}/component-model) >= 2.3
Requires:       php-composer(%{gh_owner}/component-model) <  3
Requires:       php-composer(%{gh_owner}/http) >= 2.2
Requires:       php-composer(%{gh_owner}/http) <  3
Requires:       php-composer(%{gh_owner}/reflection) >= 2.2
Requires:       php-composer(%{gh_owner}/reflection) <  3
Requires:       php-composer(%{gh_owner}/utils) >= 2.4
Requires:       php-composer(%{gh_owner}/utils) <  3
# from composer.json, "suggest": {
#       "nette/forms": "Allows to use Nette\\Application\\UI\\Form",
#       "latte/latte": "Allows using Latte in templates"
%if 0%{?fedora} > 21
Suggests:       php-composer(%{gh_owner}/forms)
Suggests:       php-composer(latte/latte)
%endif
# from phpcompatinfo report for version 2.4.0
Requires:       php-pcre
Requires:       php-reflection
Requires:       php-spl

Provides:       php-composer(%{gh_owner}/%{gh_project}) = %{version}


%description
Model-View-Controller is a software architecture that was created to
satisfy the need to separate utility code (controller) from application
logic code (model) and from code for displaying data (view) in applications
with graphical user interface. With this approach we make the application
better understandable, simplify future development and enable testing each
unit of the application separately.

To use this library, you just have to add, in your project:
  require_once '%{php_home}/%{ns_vendor}/%{ns_project}/autoload.php';


%prep
%setup -q -n %{gh_project}-%{gh_commit}

mv src/compatibility.php src/%{ns_project}/


%build
: Generate a classmap autoloader
phpab --output src/%{ns_project}/autoload.php src

cat << 'EOF' | tee -a src/%{ns_project}/autoload.php
// Dependencies
foreach (array(
    '%{php_home}/%{ns_vendor}/ComponentModel/autoload.php' => true,
    '%{php_home}/%{ns_vendor}/Http/autoload.php'           => true,
    '%{php_home}/%{ns_vendor}/Reflection/autoload.php'     => true,
    '%{php_home}/%{ns_vendor}/Utils/autoload.php'          => true,
    // Optional
    '%{php_home}/%{ns_vendor}/Forms/autoload.php'          => false,
    '%{php_home}/Latte/autoload.php'                       => false,
    ) as $dep => $mandatory) {
    if ($mandatory || file_exists($dep)) require_once($dep);
}

require_once __DIR__ . '/compatibility.php';
EOF


%install
rm -rf       %{buildroot}
mkdir -p     %{buildroot}%{php_home}/%{ns_vendor}
cp -pr src/* %{buildroot}%{php_home}/%{ns_vendor}/


%check
%if %{with_tests}
: Ignore failed test - under investigation
rm tests/Bridges.DI/ApplicationExtension.scan.phpt
%if 0%{?rhel} == 6
rm tests/Application/MicroPresenter.response.phpt
%endif

export LANG=fr_FR.utf8

: Generate autoloader
mkdir vendor
cat << 'EOF' | tee vendor/autoload.php
<?php
require_once '%{php_home}/Tester/autoload.php';
require_once '%{php_home}/%{ns_vendor}/DI/autoload.php';
require_once '%{php_home}/%{ns_vendor}/RobotLoader/autoload.php';
require_once '%{php_home}/%{ns_vendor}/Security/autoload.php';
require_once '%{php_home}/Mockery/autoload.php';
require_once '%{buildroot}%{php_home}/%{ns_vendor}/%{ns_project}/autoload.php';
EOF

: Run test suite in sources tree
# remirepo:11
run=0
ret=0
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
%{php_home}/%{ns_vendor}/Bridges


%changelog
* Thu Jan 19 2017 Remi Collet <remi@fedoraproject.org> - 2.4.4-1
- update to 2.4.4

* Wed Dec 21 2016 Remi Collet <remi@fedoraproject.org> - 2.4.3-1
- update to 2.4.3

* Tue Sep 27 2016 Remi Collet <remi@fedoraproject.org> - 2.4.2-1
- update to 2.4.2

* Thu Aug  4 2016 Remi Collet <remi@fedoraproject.org> - 2.4.1-2
- fix autoloader

* Thu Aug  4 2016 Remi Collet <remi@fedoraproject.org> - 2.4.1-1
- update to 2.4.1
- raise dependency on PHP >= 5.6
- raise dependency on nette/utils >= 2.4
- raise dependency on nette/component-model >= 2.3
- drop dependency on nette/security

* Mon Jun 20 2016 Remi Collet <remi@fedoraproject.org> - 2.3.13-1
- update to 2.3.12

* Mon May 30 2016 Remi Collet <remi@fedoraproject.org> - 2.3.12-3
- add upstream patch for tests, fix FTBFS, thanks Koschei

* Thu Apr 14 2016 Remi Collet <remi@fedoraproject.org> - 2.3.12-2
- don't use include_once in autoloader

* Wed Apr  6 2016 Remi Collet <remi@fedoraproject.org> - 2.3.12-1
- update to 2.3.12

* Sat Feb 20 2016 Remi Collet <remi@fedoraproject.org> - 2.3.11-1
- update to 2.3.11

* Fri Feb 12 2016 Remi Collet <remi@fedoraproject.org> - 2.3.10-1
- update to 2.3.10

* Wed Jan 20 2016 Remi Collet <remi@fedoraproject.org> - 2.3.9-1
- update to 2.3.9
- raise dependency on latte ~2.3.9

* Thu Dec  3 2015 Remi Collet <remi@fedoraproject.org> - 2.3.8-1
- update to 2.3.8
- run test suite with both php 5 and 7 when available

* Fri Oct 30 2015 Remi Collet <remi@fedoraproject.org> - 2.3.7-1
- initial package
