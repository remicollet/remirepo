# remirepo/Fedora spec file for php-zendframework-zend-view
#
# Copyright (c) 2015-2016 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global bootstrap    0
%global gh_commit    71b4ebd0c4c9a2d0e0438f9d3a435e08dd769ff8
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     zendframework
%global gh_project   zend-view
%global php_home     %{_datadir}/php
%global library      View
%if %{bootstrap}
%global with_tests   0%{?_with_tests:1}
%else
%global with_tests   0%{!?_without_tests:1}
%endif

Name:           php-%{gh_owner}-%{gh_project}
Version:        2.8.1
Release:        1%{?dist}
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
BuildRequires:  php(language) >= 5.5
BuildRequires:  php-date
BuildRequires:  php-dom
BuildRequires:  php-filter
BuildRequires:  php-pcre
BuildRequires:  php-spl
BuildRequires:  php-composer(%{gh_owner}/zend-eventmanager)     >= 2.5
BuildRequires:  php-composer(%{gh_owner}/zend-loader)           >= 2.5
BuildRequires:  php-composer(%{gh_owner}/zend-stdlib)           >= 2.5
# From composer, "require-dev": {
#        "zendframework/zend-authentication": "^2.5",
#        "zendframework/zend-cache": "^2.6.1",
#        "zendframework/zend-config": "^2.6",
#        "zendframework/zend-console": "^2.6",
#        "zendframework/zend-escaper": "^2.5",
#        "zendframework/zend-feed": "^2.7",
#        "zendframework/zend-filter": "^2.6.1",
#        "zendframework/zend-http": "^2.5.4",
#        "zendframework/zend-i18n": "^2.6",
#        "zendframework/zend-json": "^2.6.1",
#        "zendframework/zend-log": "^2.7",
#        "zendframework/zend-modulemanager": "^2.7.1",
#        "zendframework/zend-mvc": "^2.7 || ^3.0",
#        "zendframework/zend-navigation": "^2.5",
#        "zendframework/zend-paginator": "^2.5",
#        "zendframework/zend-permissions-acl": "^2.6",
#        "zendframework/zend-router": "^3.0.1",
#        "zendframework/zend-serializer": "^2.6.1",
#        "zendframework/zend-session": "^2.6.2",
#        "zendframework/zend-servicemanager": "^2.7.5 || ^3.0.3",
#        "zendframework/zend-uri": "^2.5",
#        "fabpot/php-cs-fixer": "1.7.*",
#        "phpunit/PHPUnit": "^4.5"
BuildRequires:  php-composer(%{gh_owner}/zend-authentication)   >= 2.5
BuildRequires:  php-composer(%{gh_owner}/zend-cache)            >= 2.6.1
BuildRequires:  php-composer(%{gh_owner}/zend-config)           >= 2.6
BuildRequires:  php-composer(%{gh_owner}/zend-console)          >= 2.6
BuildRequires:  php-composer(%{gh_owner}/zend-escaper)          >= 2.5
BuildRequires:  php-composer(%{gh_owner}/zend-feed)             >= 2.7
BuildRequires:  php-composer(%{gh_owner}/zend-filter)           >= 2.6.1
BuildRequires:  php-composer(%{gh_owner}/zend-http)             >= 2.5.4
BuildRequires:  php-composer(%{gh_owner}/zend-i18n)             >= 2.6
BuildRequires:  php-composer(%{gh_owner}/zend-json)             >= 2.6.1
BuildRequires:  php-composer(%{gh_owner}/zend-log)              >= 2.7
BuildRequires:  php-composer(%{gh_owner}/zend-modulemanager)    >= 2.7.1
BuildRequires:  php-composer(%{gh_owner}/zend-mvc)              >= 2.7
BuildRequires:  php-composer(%{gh_owner}/zend-navigation)       >= 2.5
BuildRequires:  php-composer(%{gh_owner}/zend-paginator)        >= 2.5
BuildRequires:  php-composer(%{gh_owner}/zend-permissions-acl)  >= 2.6
#BuildRequires:  php-composer(%{gh_owner}/zend-router)           >= 3.0.1
BuildRequires:  php-composer(%{gh_owner}/zend-serializer)       >= 2.6.1
BuildRequires:  php-composer(%{gh_owner}/zend-session)          >= 2.6.2
BuildRequires:  php-composer(%{gh_owner}/zend-servicemanager)   >= 2.7.5
BuildRequires:  php-composer(%{gh_owner}/zend-uri)              >= 2.5
BuildRequires:  php-composer(phpunit/phpunit)                   >= 4.5
# Autoloader
BuildRequires:  php-composer(%{gh_owner}/zend-loader)           >= 2.5
%endif

# From composer, "require": {
#        "php": "^5.5 || ^7.0",
#        "zendframework/zend-eventmanager": "^2.6.2 || ^3.0",
#        "zendframework/zend-loader": "^2.5",
#        "zendframework/zend-stdlib": "^2.7 || ^3.0"
Requires:       php(language) >= 5.5
%if ! %{bootstrap}
Requires:       php-composer(%{gh_owner}/zend-eventmanager)     >= 2.6.2
Requires:       php-composer(%{gh_owner}/zend-eventmanager)     <  4
Requires:       php-composer(%{gh_owner}/zend-loader)           >= 2.5
Requires:       php-composer(%{gh_owner}/zend-loader)           <  3
Requires:       php-composer(%{gh_owner}/zend-stdlib)           >= 2.7
Requires:       php-composer(%{gh_owner}/zend-stdlib)           <  4
# From composer, "suggest": {
#        "zendframework/zend-authentication": "Zend\\Authentication component",
#        "zendframework/zend-escaper": "Zend\\Escaper component",
#        "zendframework/zend-feed": "Zend\\Feed component",
#        "zendframework/zend-filter": "Zend\\Filter component",
#        "zendframework/zend-http": "Zend\\Http component",
#        "zendframework/zend-i18n": "Zend\\I18n component",
#        "zendframework/zend-json": "Zend\\Json component",
#        "zendframework/zend-mvc": "Zend\\Mvc component",
#        "zendframework/zend-navigation": "Zend\\Navigation component",
#        "zendframework/zend-paginator": "Zend\\Paginator component",
#        "zendframework/zend-permissions-acl": "Zend\\Permissions\\Acl component",
#        "zendframework/zend-servicemanager": "Zend\\ServiceManager component",
#        "zendframework/zend-uri": "Zend\\Uri component"
%if 0%{?fedora} >= 21
Suggests:       php-composer(%{gh_owner}/zend-authentication)
Suggests:       php-composer(%{gh_owner}/zend-escaper)
Suggests:       php-composer(%{gh_owner}/zend-feed)
Suggests:       php-composer(%{gh_owner}/zend-filter)
Suggests:       php-composer(%{gh_owner}/zend-http)
Suggests:       php-composer(%{gh_owner}/zend-i18n)
Suggests:       php-composer(%{gh_owner}/zend-json)
Suggests:       php-composer(%{gh_owner}/zend-mvc)
Suggests:       php-composer(%{gh_owner}/zend-navigation)
Suggests:       php-composer(%{gh_owner}/zend-paginator)
Suggests:       php-composer(%{gh_owner}/zend-permissions-acl)
Suggests:       php-composer(%{gh_owner}/zend-servicemanager)
Suggests:       php-composer(%{gh_owner}/zend-uri)
%endif
%endif
# From phpcompatinfo report for version 2.6.0
Requires:       php-cli
Requires:       php-date
Requires:       php-dom
Requires:       php-filter
Requires:       php-pcre
Requires:       php-spl

Obsoletes:      php-ZendFramework2-%{library} < 2.5
Provides:       php-ZendFramework2-%{library} = %{version}
Provides:       php-composer(%{gh_owner}/%{gh_project}) = %{version}
# for zf_templatemap_generator command
Conflicts:      php-zendframework < 2.5.3-3


%description
Zend\View provides the “View” layer of Zend Framework 2’s MVC system.
It is a multi-tiered system allowing a variety of mechanisms for extension,
substitution, and more.

Documentation: https://zendframework.github.io/%{gh_project}/


%prep
%setup -q -n %{gh_project}-%{gh_commit}


%build
# Empty build section, nothing required


%install
rm -rf %{buildroot}

mkdir -p   %{buildroot}%{php_home}/Zend/
cp -pr src %{buildroot}%{php_home}/Zend/%{library}

# From composer.json,     "bin": [
#        "bin/templatemap_generator.php"
for i in bin/templatemap_generator.php
do   install -Dpm 755 $i %{buildroot}%{_bindir}/zf_$(basename $i .php)
done


%check
%if %{with_tests}
# Ignore test which requires router v3
rm test/Helper/UrlTest.php

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
run=0
ret=0
if which php56; then
   php56 %{_bindir}/phpunit --include-path=%{buildroot}%{php_home} || ret=1
   run=1
fi
if which php71; then
   php70 %{_bindir}/phpunit --include-path=%{buildroot}%{php_home} || ret=1
   run=1
fi
if [ $run -eq 0 ]; then
%{_bindir}/phpunit --include-path=%{buildroot}%{php_home} --verbose
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
%license LICENSE.md
%doc CONTRIBUTING.md README.md
%doc composer.json
%{php_home}/Zend/%{library}
%{_bindir}/zf_templatemap_generator


%changelog
* Fri Jul  1 2016 Remi Collet <remi@fedoraproject.org> - 2.8.1-1
- version 2.8.1

* Wed Jun 22 2016 Remi Collet <remi@fedoraproject.org> - 2.8.0-1
- version 2.8.0
- add zf_templatemap_generator (dropped from zf2)

* Thu May 12 2016 Remi Collet <remi@fedoraproject.org> - 2.7.0-1
- version 2.7.0

* Tue Apr 19 2016 Remi Collet <remi@fedoraproject.org> - 2.6.7-1
- version 2.6.7

* Mon Mar 21 2016 Remi Collet <remi@fedoraproject.org> - 2.6.5-1
- version 2.6.5

* Mon Mar 21 2016 Remi Collet <remi@fedoraproject.org> - 2.6.4-2
- add patch for zend-navigation issue, see:
  https://github.com/zendframework/zend-navigation/issues/23

* Thu Mar  3 2016 Remi Collet <remi@fedoraproject.org> - 2.6.4-1
- version 2.6.4

* Tue Feb 23 2016 Remi Collet <remi@fedoraproject.org> - 2.6.3-1
- version 2.6.3

* Fri Feb 19 2016 Remi Collet <remi@fedoraproject.org> - 2.6.2-1
- version 2.6.2

* Thu Feb 18 2016 Remi Collet <remi@fedoraproject.org> - 2.6.1-1
- version 2.6.1

* Thu Feb 18 2016 Remi Collet <remi@fedoraproject.org> - 2.6.0-1
- version 2.6.0
- raise dependency on zend-eventmanager >= 2.6.2
- raise dependency on zend-stdlib >= 2.7

* Wed Jan 20 2016 Remi Collet <remi@fedoraproject.org> - 2.5.3-1
- version 2.5.3

* Thu Aug  6 2015 Remi Collet <remi@fedoraproject.org> - 2.5.2-1
- version 2.5.2

* Tue Aug  4 2015 Remi Collet <remi@fedoraproject.org> - 2.5.1-1
- initial package
