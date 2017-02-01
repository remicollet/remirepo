# remirepo/Fedora spec file for php-zendframework-zend-http
#
# Copyright (c) 2015-2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global bootstrap    0
%global gh_commit    09f4d279f46d86be63171ff62ee0f79eca878678
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     zendframework
%global gh_project   zend-http
%global php_home     %{_datadir}/php
%global library      Http
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
URL:            https://zendframework.github.io/%{gh_project}/
Source0:        %{gh_commit}/%{name}-%{version}-%{gh_short}.tgz
Source1:        makesrc.sh

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch:      noarch
# Tests
%if %{with_tests}
BuildRequires:  php(language) >= 5.5
BuildRequires:  php-ctype
BuildRequires:  php-curl
BuildRequires:  php-date
BuildRequires:  php-fileinfo
BuildRequires:  php-openssl
BuildRequires:  php-pcre
BuildRequires:  php-spl
BuildRequires:  php-zlib
BuildRequires:  php-composer(%{gh_owner}/zend-loader)           >= 2.5
BuildRequires:  php-composer(%{gh_owner}/zend-stdlib)           >= 2.5
BuildRequires:  php-composer(%{gh_owner}/zend-uri)              >= 2.5
BuildRequires:  php-composer(%{gh_owner}/zend-validator)        >= 2.5
# From composer, "require-dev": {
#        "phpunit/PHPUnit": "~4.0",
#        "zendframework/zend-config": "^2.5",
#        "zendframework/zend-coding-standard": "~1.0.0"
BuildRequires:  php-composer(%{gh_owner}/zend-config)           >= 2.5
BuildRequires:  php-composer(phpunit/phpunit)                   >= 4.0
# Autoloader
BuildRequires:  php-composer(%{gh_owner}/zend-loader)           >= 2.5
%endif

# From composer, "require": {
#        "php": "^5.5 || ^7.0",
#        "zendframework/zend-loader": "~2.5",
#        "zendframework/zend-stdlib": "^2.5 || ^3.0",
#        "zendframework/zend-uri": "~2.5",
#        "zendframework/zend-validator": "~2.5"
Requires:       php(language) >= 5.5
%if ! %{bootstrap}
Requires:       php-composer(%{gh_owner}/zend-loader)           >= 2.5
Requires:       php-composer(%{gh_owner}/zend-loader)           <  3
Requires:       php-composer(%{gh_owner}/zend-stdlib)           >= 2.5
Requires:       php-composer(%{gh_owner}/zend-stdlib)           <  4
Requires:       php-composer(%{gh_owner}/zend-uri)              >= 2.5
Requires:       php-composer(%{gh_owner}/zend-uri)              <  3
Requires:       php-composer(%{gh_owner}/zend-validator)        >= 2.5
Requires:       php-composer(%{gh_owner}/zend-validator)        <  3
%endif
# From phpcompatinfo report for version 2.5.1
Requires:       php-ctype
Requires:       php-curl
Requires:       php-date
Requires:       php-fileinfo
Requires:       php-openssl
Requires:       php-pcre
Requires:       php-spl
Requires:       php-zlib

Obsoletes:      php-ZendFramework2-%{library} < 2.5
Provides:       php-ZendFramework2-%{library} = %{version}
Provides:       php-composer(%{gh_owner}/%{gh_project}) = %{version}


%description
Zend\Http is a primary foundational component of Zend Framework.
Since much of what PHP does is web-based, specifically HTTP,
it makes sense to have a performant, extensible, concise and
consistent API to do all things HTTP.

Documentation: https://zendframework.github.io/%{gh_project}/


%prep
%setup -q -n %{gh_project}-%{gh_commit}

mv LICENSE.md LICENSE


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

# remirepo:11
ret=0
run=0
if which php56; then
   php56 %{_bindir}/phpunit || ret=1
   run=1
fi
if which php71; then
   php71 %{_bindir}/phpunit || ret=1
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
%{php_home}/Zend/%{library}


%changelog
* Wed Feb  1 2017 Remi Collet <remi@fedoraproject.org> - 2.6.0-1
- version 2.6.0

* Mon Aug  8 2016 Remi Collet <remi@fedoraproject.org> - 2.5.5-1
- version 2.5.5

* Fri Feb  5 2016 Remi Collet <remi@fedoraproject.org> - 2.5.4-1
- version 2.5.4

* Tue Sep 15 2015 Remi Collet <remi@fedoraproject.org> - 2.5.3-1
- version 2.5.3

* Thu Aug  6 2015 Remi Collet <remi@fedoraproject.org> - 2.5.2-1
- version 2.5.2

* Tue Aug  4 2015 Remi Collet <remi@fedoraproject.org> - 2.5.1-1
- initial package
