# remirepo/fedora spec file for php-nette-deprecated
#
# Copyright (c) 2015-2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    fde8fea8e3f1960ea6bcca03a996300b0ca41762
#global gh_date      20150728
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     nette
%global gh_project   deprecated
%global ns_vendor    Nette
%global ns_project   Deprecated
%global php_home     %{_datadir}/php
%global with_tests   0%{!?_without_tests:1}

Name:           php-%{gh_owner}-%{gh_project}
Version:        2.4.0
%global specrel 2
Release:        %{?gh_date:0.%{specrel}.%{?prever}%{!?prever:%{gh_date}git%{gh_short}}}%{!?gh_date:%{specrel}}%{?dist}
Summary:        APIs and features removed from Nette Framework

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
BuildRequires:  php-fileinfo
BuildRequires:  php-spl
BuildRequires:  php-tokenizer
# From composer.json, "require-dev": {
#        "nette/application": "^2.2",
#        "nette/bootstrap": "^2.2.1",
#        "nette/caching": "^2.2",
#        "nette/forms": "^2.2",
#        "nette/mail": "^2.2",
#        "nette/robot-loader": "^2.2",
#        "nette/safe-stream": "^2.2",
#        "nette/utils": "^2.2",
#        "nette/security": "^2.2",
#        "latte/latte": "^2.2",
#        "tracy/tracy": "^2.2",
#        "nette/tester": "^1.1"
BuildRequires:  php-composer(%{gh_owner}/application) >= 2.2
BuildRequires:  php-composer(%{gh_owner}/bootstrap) >= 2.2.1
BuildRequires:  php-composer(%{gh_owner}/caching) >= 2.2
BuildRequires:  php-composer(%{gh_owner}/forms) >= 2.2
BuildRequires:  php-composer(%{gh_owner}/mail) >= 2.2
BuildRequires:  php-composer(%{gh_owner}/robot-loader) >= 2.2
BuildRequires:  php-composer(%{gh_owner}/safe-stream) >= 2.2
BuildRequires:  php-composer(%{gh_owner}/utils) >= 2.2
BuildRequires:  php-composer(%{gh_owner}/security) >= 2.2
BuildRequires:  php-composer(latte/latte) >= 2.2
BuildRequires:  php-composer(tracy/tracy) >= 2.2
BuildRequires:  php-composer(%{gh_owner}/tester) >= 1.1
%endif

# from phpcompatinfo report for version 2.4.0
Requires:       php-fileinfo
Requires:       php-spl
Requires:       php-tokenizer

Provides:       php-composer(%{gh_owner}/%{gh_project}) = %{version}


%description
%{summary}.

To use this library, you just have to add, in your project:
  require_once '%{php_home}/%{ns_vendor}/%{ns_project}/autoload.php';


%prep
%setup -q -n %{gh_project}-%{gh_commit}

mkdir src/%{ns_project}


%build
: Generate a classmap autoloader
phpab --output src/%{ns_project}/autoload.php src

cat << 'EOF' | tee -a src/%{ns_project}/autoload.php
require_once dirname(__DIR__) . '/loader.php';
EOF


%install
rm -rf       %{buildroot}
mkdir -p     %{buildroot}%{php_home}/%{ns_vendor}
cp -pr src/* %{buildroot}%{php_home}/%{ns_vendor}/


%check
%if %{with_tests}
export LANG=fr_FR.utf8

: Generate autoloader
mkdir -p vendor/nette/tester
ln -s %{php_home}/Tester vendor/nette/tester/Tester
cat << 'EOF' | tee vendor/autoload.php
<?php
require_once '%{php_home}/%{ns_vendor}/Application/autoload.php';
require_once '%{php_home}/%{ns_vendor}/Bootstrap/autoload.php';
require_once '%{php_home}/%{ns_vendor}/Caching/autoload.php';
require_once '%{php_home}/%{ns_vendor}/Forms/autoload.php';
require_once '%{php_home}/%{ns_vendor}/Mail/autoload.php';
require_once '%{php_home}/%{ns_vendor}/RobotLoader/autoload.php';
require_once '%{php_home}/%{ns_vendor}/SafeStream/autoload.php';
require_once '%{php_home}/%{ns_vendor}/Security/autoload.php';
require_once '%{php_home}/%{ns_vendor}/Utils/autoload.php';
require_once '%{php_home}/Latte/autoload.php';
require_once '%{php_home}/Tracy/autoload.php';
require_once '%{php_home}/Tester/autoload.php';
require_once '%{buildroot}%{php_home}/%{ns_vendor}/%{ns_project}/autoload.php';
EOF

php -r 'require "vendor/autoload.php";'

: Run test suite in sources tree
# remirepo:11
run=0
ret=0
if which php56; then
   php56 %{_bindir}/nette-tester --colors 0 -p php56 -C tests -s
   run=1
fi
if which php70; then
   php70 %{_bindir}/nette-tester --colors 0 -p php70 -C tests -s
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
%{php_home}/%{ns_vendor}


%changelog
* Fri Aug  5 2016 Remi Collet <remi@fedoraproject.org> - 2.4.0-2
- fix test suite autoloader

* Thu Aug  4 2016 Remi Collet <remi@fedoraproject.org> - 2.4.0-1
- update to 2.4.0
- add dependency on nette/security >= 2.2

* Sun Nov  8 2015 Remi Collet <remi@fedoraproject.org> - 2.3.2-1
- update to 2.3.2

* Sun Nov  1 2015 Remi Collet <remi@fedoraproject.org> - 2.3.1-2
- improve installation tree to avoid file conflicts
  with nette/utils and nette/nette

* Sat Oct 31 2015 Remi Collet <remi@fedoraproject.org> - 2.3.1-1
- initial package
