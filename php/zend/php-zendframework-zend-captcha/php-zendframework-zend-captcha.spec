# remirepo/Fedora spec file for php-zendframework-zend-captcha
#
# Copyright (c) 2015-2016 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global bootstrap    0
%global gh_commit    9a1197bc5b8aa4fad104c22f6d9b2a3d4bdda0c6
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     zendframework
%global gh_project   zend-captcha
%global php_home     %{_datadir}/php
%global library      Captcha
%if %{bootstrap}
%global with_tests   0%{?_with_tests:1}
%else
%global with_tests   0%{!?_without_tests:1}
%endif

Name:           php-%{gh_owner}-%{gh_project}
Version:        2.6.0
Release:        1%{?dist}
Summary:        Zend Framework %{library} component

Group:          Development/Libraries
License:        BSD
URL:            http://framework.zend.com/
Source0:        %{gh_commit}/%{name}-%{version}-%{gh_short}.tgz
Source1:        makesrc.sh

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch:      noarch
# Tests
%if %{with_tests}
BuildRequires:  php(language) >= 5.6
BuildRequires:  php-date
BuildRequires:  php-gd
BuildRequires:  php-spl
BuildRequires:  php-composer(%{gh_owner}/zend-math)             >= 2.5
BuildRequires:  php-composer(%{gh_owner}/zend-stdlib)           >= 2.5
# From composer, "require-dev": {
#        "zendframework/zend-session": "^2.6",
#        "zendframework/zend-text": "^2.6",
#        "zendframework/zend-validator": "^2.6",
#        "zendframework/zendservice-recaptcha": "*",
#        "squizlabs/php_codesniffer": "^2.3.1",
#        "phpunit/PHPUnit": "~4.8"
BuildRequires:  php-composer(%{gh_owner}/zend-session)          >= 2.6
BuildRequires:  php-composer(%{gh_owner}/zend-text)             >= 2.6
BuildRequires:  php-composer(%{gh_owner}/zend-validator)        >= 2.6
#BuildRequires:  php-composer(%%{gh_owner}/zendservice-recaptcha) >= 2.5
BuildRequires:  php-composer(phpunit/phpunit)                   >= 4.8
# Autoloader
BuildRequires:  php-composer(%{gh_owner}/zend-loader)           >= 2.5
%endif

# From composer, "require": {
#        "php": "^5.6 || ^7.0",
#        "zendframework/zend-math": "^2.6 || ^3.0",
#        "zendframework/zend-stdlib": "^2.7 || ^3.0"
Requires:       php(language) >= 5.6
%if ! %{bootstrap}
Requires:       php-composer(%{gh_owner}/zend-math)             >= 2.6
Requires:       php-composer(%{gh_owner}/zend-math)             <  4
Requires:       php-composer(%{gh_owner}/zend-stdlib)           >= 2.7
Requires:       php-composer(%{gh_owner}/zend-stdlib)           <  4
# From composer, "suggest": {
#        "zendframework/zend-i18n-resources": "Translations of captcha messages",
#        "zendframework/zend-session": "Zend\\Session component",
#        "zendframework/zend-text": "Zend\\Text component",
#        "zendframework/zend-validator": "Zend\\Validator component",
#        "zendframework/zendservice-recaptcha": "ZendService\\ReCaptcha component"
%if 0%{?fedora} >= 21
Suggests:       php-composer(%{gh_owner}/zend-i18n-resources)
Suggests:       php-composer(%{gh_owner}/zend-session)
Suggests:       php-composer(%{gh_owner}/zend-text)
Suggests:       php-composer(%{gh_owner}/zend-validator)
#Suggests:       php-composer(%%{gh_owner}/zendservice-recaptcha)
%endif
%endif
# From phpcompatinfo report for version 2.5.2
Requires:       php-date
Requires:       php-gd
Requires:       php-spl

Obsoletes:      php-ZendFramework2-%{library} < 2.5
Provides:       php-ZendFramework2-%{library} = %{version}
Provides:       php-composer(%{gh_owner}/%{gh_project}) = %{version}


%description
Zend\Captcha component is able to manage “Completely Automated Public
Turing test to tell Computers and Humans Apart” (CAPTCHA); it is used
as a challenge-response to ensure that the individual submitting
information is a human and not an automated process. Typically, a captcha
is used with form submissions where authenticated users are not necessary,
but you want to prevent spam submissions.

Documentation: https://zendframework.github.io/zend-captcha/


%prep
%setup -q -n %{gh_project}-%{gh_commit}


%build
# Empty build section, nothing required


%install
rm -rf %{buildroot}

mkdir -p   %{buildroot}%{php_home}/Zend/
cp -pr src %{buildroot}%{php_home}/Zend/%{library}


%check
%if %{with_tests}
mkdir vendor
cat << 'EOF' | tee vendor/autoload.php
<?php
require_once '%{php_home}/Zend/Loader/AutoloaderFactory.php';
Zend\Loader\AutoloaderFactory::factory(array(
    'Zend\Loader\StandardAutoloader' => array(
        'namespaces' => array(
           'ZendTest\\%{library}' => dirname(__DIR__).'/test/',
           'Zend\\%{library}'     => '%{buildroot}%{php_home}/Zend/%{library}'
))));
require_once '%{php_home}/Zend/autoload.php';
EOF

%{_bindir}/phpunit --include-path=%{buildroot}%{php_home}

if which php70; then
   php70 %{_bindir}/phpunit --include-path=%{buildroot}%{php_home}
fi
%else
: Test suite disabled
%endif


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE.md
%doc CONTRIBUTING.md README.md
%doc composer.json
%{php_home}/Zend/%{library}


%changelog
* Wed Jun 22 2016 Remi Collet <remi@fedoraproject.org> - 2.6.0-1
- update to 2.6.0
- raise dependency on PHP 5.6

* Tue Feb 23 2016 Remi Collet <remi@fedoraproject.org> - 2.5.4-1
- update to 2.5.4
- raise dependency on zend-math >= 2.6
- raise dependency on zend-stdlib >= 2.7

* Tue Feb 23 2016 Remi Collet <remi@fedoraproject.org> - 2.5.3-1
- update to 2.5.3

* Wed Nov 25 2015 Remi Collet <remi@fedoraproject.org> - 2.5.2-1
- update to 2.5.2
- raise dependency on PHP 5.5

* Tue Aug  4 2015 Remi Collet <remi@fedoraproject.org> - 2.5.1-1
- initial package
