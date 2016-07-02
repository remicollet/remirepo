# remirepo/Fedora spec file for php-zendframework-zend-expressive-template
#
# Copyright (c) 2016 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global bootstrap    0
%global gh_commit    2aac4050ebcf9a2c883dc23cf74671da02a66a7b
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     zendframework
%global gh_project   zend-expressive-template
%global php_home     %{_datadir}/php
%global library      Expressive
%global sublib       Template
%if %{bootstrap}
%global with_tests   0%{?_with_tests:1}
%else
%global with_tests   0%{!?_without_tests:1}
%endif

Name:           php-%{gh_owner}-%{gh_project}
Version:        1.0.3
Release:        2%{?dist}
Summary:        %{sublib} subcomponent for %{library}

Group:          Development/Libraries
License:        BSD
URL:            https://framework.zend.com/
Source0:        %{gh_commit}/%{name}-%{version}-%{gh_short}.tgz
Source1:        makesrc.sh

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch:      noarch
# Tests
%if %{with_tests}
BuildRequires:  php(language) >= 5.5
BuildRequires:  php-spl
# From composer, "require-dev": {
#        "phpunit/phpunit": "^4.7",
#        "squizlabs/php_codesniffer": "^2.3"
BuildRequires:  php-composer(phpunit/phpunit)                   >= 4.7
# Autoloader
BuildRequires:  php-composer(%{gh_owner}/zend-loader)           >= 2.5
%endif

# From composer, "require": {
#        "php": ">=5.5"
Requires:       php(language) >= 5.5
# From phpcompatinfo report for version 1.0.3
Requires:       php-spl
%if ! %{bootstrap}
# From composer, "suggest": {
#        "zendframework/zend-expressive-platesrenderer": "^0.1 to use the Plates template renderer",
#        "zendframework/zend-expressive-twigrenderer": "^0.1 to use the Twig template renderer",
#        "zendframework/zend-expressive-zendviewrenderer": "^0.1 to use the zend-view PhpRenderer template renderer"
%if 0%{?fedora} >= 21
Suggests:       php-composer(%{gh_owner}/zend-expressive-platesrenderer)
Suggests:       php-composer(%{gh_owner}/zend-expressive-twigrenderer)
Suggests:       php-composer(%{gh_owner}/zend-expressive-zendviewrenderer)
%endif
# Autoloader
Requires:       php-composer(%{gh_owner}/zend-loader)           >= 2.5
%endif

Provides:       php-composer(%{gh_owner}/%{gh_project}) = %{version}


%description
Template subcomponent for Expressive

This package provides the following classes, interfaces, and traits:

* TemplateRendererInterface, a generic interface for providing template rendering capabilities.
* TemplatePath, a value object describing a (optionally) namespaced path in which templates reside; the TemplateRendererInterface returns these.
* ArrayParametersTrait provides helper methods you can mix in to implementations for normalizing template parameters to an array.
* DefaultParamsTrait provides helper methods you can mix in to implementations for aggregating default parameters as well as merging global, template-specific, and provided parameters when rendering.

We currently support and provide the following routing integrations:

* Plates: php-zendframework-zend-expressive-platesrenderer
* Twig: php-zendframework-zend-expressive-twigrenderer
* ZF2 PhpRenderer: php-zendframework-zend-expressive-zendviewrenderer

Documentation: http://zend-expressive.readthedocs.io/


%prep
%setup -q -n %{gh_project}-%{gh_commit}

mv LICENSE.md LICENSE


%build
# Empty build section, nothing required


%install
rm -rf %{buildroot}

mkdir -p   %{buildroot}%{php_home}/Zend/%{library}
cp -pr src %{buildroot}%{php_home}/Zend/%{library}/%{sublib}


%check
%if %{with_tests}
mkdir vendor
cat << 'EOF' | tee vendor/autoload.php
<?php
define('RPM_BUILDROOT', '%{buildroot}%{php_home}/Zend');

require_once '%{php_home}/Zend/Loader/AutoloaderFactory.php';
Zend\Loader\AutoloaderFactory::factory(array(
    'Zend\Loader\StandardAutoloader' => array(
        'namespaces' => array(
           'ZendTest\\%{library}\\%{sublib}' => dirname(__DIR__).'/test/',
           'Zend\\%{library}\\%{sublib}'     => '%{buildroot}%{php_home}/Zend/%{library}/%{sublib}'
))));
require_once '%{php_home}/Zend/autoload.php';
EOF

# remirepo:11
run=0
ret=0
if which php56; then
   php56 %{_bindir}/phpunit || ret=1
   run=1
fi
if which php71; then
   php70 %{_bindir}/phpunit || ret=1
   run=1
fi
if [ $run -eq 0 ]; then
%{_bindir}/phpunit --verbose
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
%license LICENSE
%doc *.md
%doc composer.json
%dir %{php_home}/Zend/%{library}/
     %{php_home}/Zend/%{library}/%{sublib}/


%changelog
* Sat Jul  2 2016 Remi Collet <remi@fedoraproject.org> - 1.2.0-2
- cleanup

* Fri Jul  1 2016 Remi Collet <remi@fedoraproject.org> - 1.2.0-1
- initial package

