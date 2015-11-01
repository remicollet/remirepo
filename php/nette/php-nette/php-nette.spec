# remirepo/fedora spec file for php-nette
#
# Copyright (c) 2015 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    40b55666b78d7ec6272c46e94f15e4f36bd583e2
#global gh_date      20150728
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     nette
%global gh_project   nette
%global ns_vendor    Nette
%global php_home     %{_datadir}/php
%global with_tests   0%{!?_without_tests:1}

Name:           php-%{gh_project}
Version:        2.3.7
%global specrel 1
Release:        %{?gh_date:0.%{specrel}.%{?prever}%{!?prever:%{gh_date}git%{gh_short}}}%{!?gh_date:%{specrel}}%{?dist}
Summary:        Nette Framework

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
BuildRequires:  php-cli
BuildRequires:  php-composer(%{gh_owner}/application)     >= 2.3.7
BuildRequires:  php-composer(%{gh_owner}/bootstrap)       >= 2.3.3
BuildRequires:  php-composer(%{gh_owner}/caching)         >= 2.3.3
BuildRequires:  php-composer(%{gh_owner}/component-model) >= 2.2.4
BuildRequires:  php-composer(%{gh_owner}/database)        >= 2.3.7
BuildRequires:  php-composer(%{gh_owner}/deprecated)      >= 2.3.1
BuildRequires:  php-composer(%{gh_owner}/di)              >= 2.3.6
BuildRequires:  php-composer(%{gh_owner}/finder)          >= 2.3.1
BuildRequires:  php-composer(%{gh_owner}/forms)           >= 2.3.5
BuildRequires:  php-composer(%{gh_owner}/http)            >= 2.3.3
BuildRequires:  php-composer(%{gh_owner}/mail)            >= 2.3.3
BuildRequires:  php-composer(%{gh_owner}/neon)            >= 2.3.3
BuildRequires:  php-composer(%{gh_owner}/php-generator)   >= 2.3.4
BuildRequires:  php-composer(%{gh_owner}/reflection)      >= 2.3.1
BuildRequires:  php-composer(%{gh_owner}/robot-loader)    >= 2.3.1
BuildRequires:  php-composer(%{gh_owner}/safe-stream)     >= 2.3.1
BuildRequires:  php-composer(%{gh_owner}/security)        >= 2.3.1
BuildRequires:  php-composer(%{gh_owner}/tokenizer)       >= 2.2.1
BuildRequires:  php-composer(%{gh_owner}/utils)           >= 2.3.6
BuildRequires:  php-composer(latte/latte)                 >= 2.3.6
BuildRequires:  php-composer(tracy/tracy)                 >= 2.3.5
%endif
# from composer.json, "require": {
#        "nette/application": "2.3.7",
#        "nette/bootstrap": "2.3.3",
#        "nette/caching": "2.3.3",
#        "nette/component-model": "2.2.4",
#        "nette/database": "2.3.7",
#        "nette/deprecated": "2.3.1",
#        "nette/di": "2.3.6",
#        "nette/finder": "2.3.1",
#        "nette/forms": "2.3.5",
#        "nette/http": "2.3.3",
#        "nette/mail": "2.3.3",
#        "nette/neon": "2.3.3",
#        "nette/php-generator": "2.3.4",
#        "nette/reflection": "2.3.1",
#        "nette/robot-loader": "2.3.1",
#        "nette/safe-stream": "2.3.1",
#        "nette/security": "2.3.1",
#        "nette/tokenizer": "2.2.1",
#        "nette/utils": "2.3.6",
#        "latte/latte": "2.3.6",
#        "tracy/tracy": "2.3.5"
# Strict version ignored on purpose
Requires:       php-composer(%{gh_owner}/application)     >= 2.3.7
Requires:       php-composer(%{gh_owner}/bootstrap)       >= 2.3.3
Requires:       php-composer(%{gh_owner}/caching)         >= 2.3.3
Requires:       php-composer(%{gh_owner}/component-model) >= 2.2.4
Requires:       php-composer(%{gh_owner}/database)        >= 2.3.7
Requires:       php-composer(%{gh_owner}/deprecated)      >= 2.3.1
Requires:       php-composer(%{gh_owner}/di)              >= 2.3.6
Requires:       php-composer(%{gh_owner}/finder)          >= 2.3.1
Requires:       php-composer(%{gh_owner}/forms)           >= 2.3.5
Requires:       php-composer(%{gh_owner}/http)            >= 2.3.3
Requires:       php-composer(%{gh_owner}/mail)            >= 2.3.3
Requires:       php-composer(%{gh_owner}/neon)            >= 2.3.3
Requires:       php-composer(%{gh_owner}/php-generator)   >= 2.3.4
Requires:       php-composer(%{gh_owner}/reflection)      >= 2.3.1
Requires:       php-composer(%{gh_owner}/robot-loader)    >= 2.3.1
Requires:       php-composer(%{gh_owner}/safe-stream)     >= 2.3.1
Requires:       php-composer(%{gh_owner}/security)        >= 2.3.1
Requires:       php-composer(%{gh_owner}/tokenizer)       >= 2.2.1
Requires:       php-composer(%{gh_owner}/utils)           >= 2.3.6
Requires:       php-composer(latte/latte)                 >= 2.3.6
Requires:       php-composer(tracy/tracy)                 >= 2.3.5
# from phpcompatinfo report for version 2.3.7: nothing

Provides:       php-composer(%{gh_owner}/%{gh_project}) = %{version}


%description
Nette Framework is a popular tool for PHP web development
It is designed to be as usable and as friendly as possible.
It focuses on security and performance and is definitely one
of the safest PHP frameworks.

Nette Framework speaks your language and helps you to easily build better websites.
Cache accelerates your application by storing data, once hardly retrieved,
for future use.

To use this library, you just have to add, in your project:
  require_once '%{php_home}/%{ns_vendor}/autoload.php';


%prep
%setup -q -n %{gh_project}-%{gh_commit}


%build
: Generate a classmap autoloader
phpab --output Nette/autoload.php Nette

cat << 'EOF' | tee -a Nette/autoload.php
// Dependencies
require_once '%{php_home}/%{ns_vendor}/Application/autoload.php';
require_once '%{php_home}/%{ns_vendor}/Bootstrap/autoload.php';
require_once '%{php_home}/%{ns_vendor}/Caching/autoload.php';
require_once '%{php_home}/%{ns_vendor}/ComponentModel/autoload.php';
require_once '%{php_home}/%{ns_vendor}/Database/autoload.php';
require_once '%{php_home}/%{ns_vendor}/DI/autoload.php';
require_once '%{php_home}/%{ns_vendor}/Finder/autoload.php';
require_once '%{php_home}/%{ns_vendor}/Forms/autoload.php';
require_once '%{php_home}/%{ns_vendor}/Http/autoload.php';
require_once '%{php_home}/%{ns_vendor}/Mail/autoload.php';
require_once '%{php_home}/%{ns_vendor}/Neon/autoload.php';
require_once '%{php_home}/%{ns_vendor}/PhpGenerator/autoload.php';
require_once '%{php_home}/%{ns_vendor}/Reflection/autoload.php';
require_once '%{php_home}/%{ns_vendor}/RobotLoader/autoload.php';
require_once '%{php_home}/%{ns_vendor}/SafeStream/autoload.php';
require_once '%{php_home}/%{ns_vendor}/Security/autoload.php';
require_once '%{php_home}/%{ns_vendor}/Tokenizer/autoload.php';
require_once '%{php_home}/%{ns_vendor}/Utils/autoload.php';
require_once '%{php_home}/Latte/autoload.php';
require_once '%{php_home}/Tracy/autoload.php';
require_once '%{php_home}/%{ns_vendor}/Deprecated/autoload.php';
EOF


%install
rm -rf              %{buildroot}
mkdir -p            %{buildroot}%{php_home}
cp -pr %{ns_vendor} %{buildroot}%{php_home}/%{ns_vendor}


%check
%if %{with_tests}
php -r '
require "%{buildroot}%{php_home}/%{ns_vendor}/autoload.php";
printf("%s version %s, %s\n", Nette\Framework::NAME, Nette\Framework::VERSION, Nette\Framework::REVISION);
exit(version_compare(Nette\Framework::VERSION, "%{version}") ? 1 : 0);
'
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
* Sun Nov  1 2015 Remi Collet <remi@fedoraproject.org> - 2.3.7-1
- initial package