# remirepo/Fedora spec file for php-zendframework-zend-i18n-resources
#
# Copyright (c) 2015-2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global bootstrap    0
%global gh_commit    fe53e1c96654c4fc89975d14ed13ccbce6c08179
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     zendframework
%global gh_project   zend-i18n-resources
%global php_home     %{_datadir}/php
%global library      Translator
%if %{bootstrap}
%global with_tests   0%{?_with_tests:1}
%else
%global with_tests   0%{!?_without_tests:1}
%endif

Name:           php-%{gh_owner}-%{gh_project}
Version:        2.5.2
Release:        1%{?dist}
Summary:        Zend Framework %{library} component

Group:          Development/Libraries
License:        BSD
URL:            https://zendframework.github.io/%{gh_project}/
Source0:        %{gh_commit}/%{name}-%{version}-%{gh_short}.tgz
Source1:        makesrc.sh

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch:      noarch
# Tests
%if %{with_tests}
BuildRequires:  php(language) >= 5.5
BuildRequires:  php-cli
BuildRequires:  php-composer(%{gh_owner}/zend-loader)           >= 2.5
%endif

# From composer, "require": {
#        "php": ">=5.5"
Requires:       php(language) >= 5.5
# Autoloader
Requires:       php-composer(%{gh_owner}/zend-loader)           >= 2.5
# From phpcompatinfo report for version 2.5.1
# None

Provides:       php-composer(%{gh_owner}/%{gh_project}) = %{version}


%description
This "component" provides translation resources, specifically
for zendframework/zend-validate and zendframework/zend-captcha,
for use with zendframework/zend-i18n's Translator subcomponent.

Documentation: https://zendframework.github.io/%{gh_project}/


%prep
%setup -q -n %{gh_project}-%{gh_commit}

mv LICENSE.txt LICENSE


%build
# Empty build section, nothing required


%install
rm -rf %{buildroot}

mkdir -p         %{buildroot}%{php_home}/Zend/I18n
cp -pr src       %{buildroot}%{php_home}/Zend/I18n/%{library}
cp -pr languages %{buildroot}%{php_home}/Zend/I18n/languages


%check
%if %{with_tests}
mkdir vendor
cat << EOF | tee vendor/autoload.php
<?php
require_once '%{php_home}/Zend/Loader/AutoloaderFactory.php';
Zend\\Loader\\AutoloaderFactory::factory(array(
    'Zend\\Loader\\StandardAutoloader' => array(
        'namespaces' => array(
           'Zend\\\\I18n' => '%{buildroot}%{php_home}/Zend/I18n'
))));
require_once '%{php_home}/Zend/autoload.php';
EOF
php -r '
  require "vendor/autoload.php";
  use Zend\I18n\Translator\Resources;
  $fic = Resources::getBasePath().sprintf(Resources::getPatternForCaptcha(), "fr");
  echo realpath($fic)."\n";
  exit (file_exists($fic) ? 0 : 1);
'
%else
: Test suite disabled
%endif


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc *.md
%doc composer.json
%dir %{php_home}/Zend/I18n
     %{php_home}/Zend/I18n/%{library}
     %{php_home}/Zend/I18n/languages


%changelog
* Thu Aug  6 2015 Remi Collet <remi@fedoraproject.org> - 2.5.2-1
- version 2.5.2

* Tue Aug  4 2015 Remi Collet <remi@fedoraproject.org> - 2.5.1-1
* Tue Aug  4 2015 Remi Collet <remi@fedoraproject.org> - 2.5.1-1
- initial package
