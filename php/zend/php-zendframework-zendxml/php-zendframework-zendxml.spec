# remirepo/Fedora spec file for php-zendframework-zendxml
#
# Copyright (c) 2015-2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global bootstrap    0
%global gh_commit    7b64507bc35d841c9c5802d67f6f87ef8e1a58c9
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     zendframework
%global gh_project   zendxml
%global php_home     %{_datadir}/php
%global library      ZendXml
%if %{bootstrap}
%global with_tests   0%{?_with_tests:1}
%else
%global with_tests   0%{!?_without_tests:1}
%endif

Name:           php-%{gh_owner}-%{gh_project}
Version:        1.0.2
Release:        2%{?dist}
Summary:        Zend Framework %{library} component

Group:          Development/Libraries
License:        BSD
URL:            https://framework.zend.com/
Source0:        %{gh_commit}/%{name}-%{version}-%{gh_short}.tgz
Source1:        makesrc.sh

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch:      noarch
# Tests
%if %{with_tests}
BuildRequires:  php(language) >= 5.3.3
BuildRequires:  php-simplexml
BuildRequires:  php-dom
BuildRequires:  php-libxml
BuildRequires:  php-pcre
BuildRequires:  php-spl
# From composer, "require-dev": {
#        "phpunit/phpunit": "^3.7 || ^4.0",
#        "squizlabs/php_codesniffer": "~1.5"
BuildRequires:  php-composer(phpunit/phpunit)                   >= 3.7
# Autoloader
BuildRequires:  php-composer(%{gh_owner}/zend-loader)
%endif

# From composer, "require": {
#        "php": "^5.3.3 || ^7.0"
Requires:       php(language) >= 5.3.3
# From phpcompatinfo report for version 1.0.1
Requires:       php-simplexml
Requires:       php-dom
Requires:       php-libxml
Requires:       php-pcre
Requires:       php-spl

Obsoletes:      php-ZendFramework2-%{library} < 2.5
Provides:       php-ZendFramework2-%{library} = 1:%{version}
Provides:       php-composer(%{gh_owner}/%{gh_project}) = %{version}


%description
An utility component for XML usage and best practices in PHP.


%prep
%setup -q -n %{gh_project}-%{gh_commit}

mv LICENSE.md LICENSE


%build
# Empty build section, nothing required


%install
rm -rf %{buildroot}

mkdir -p   %{buildroot}%{php_home}
cp -pr library/%{library} %{buildroot}%{php_home}/%{library}


%check
%if %{with_tests}
mkdir vendor
cat << 'EOF' | tee vendor/autoload.php
<?php
require_once '%{php_home}/Zend/Loader/AutoloaderFactory.php';
Zend\Loader\AutoloaderFactory::factory(array(
    'Zend\Loader\StandardAutoloader' => array(
        'fallback_autoloader' => true,
        'autoregister_zf' => true,
        'namespaces' => array(
            'ZendTest\\Xml' => dirname(__DIR__).'/tests/ZendXmlTest',
            '%{library}'    => '%{buildroot}%{php_home}/%{library}'
        )
    )
));
EOF
cd tests
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
%license LICENSE
%doc *.md
%doc composer.json
%{php_home}/%{library}


%changelog
* Sat Jun 11 2016 Shawn Iwinski <shawn@iwin.ski> - 1.0.2-2
- Allow F22 / EPEL7 / EPEL6 (ZF 2.4)

* Fri Feb  5 2016 Remi Collet <remi@fedoraproject.org> - 1.0.2-1
- update to 1.0.2

* Tue Aug  4 2015 Remi Collet <remi@fedoraproject.org> - 1.0.1-1
- initial package
