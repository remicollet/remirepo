# remirepo/Fedora spec file for php-zendframework-zend-loader
#
# Copyright (c) 2015-2016 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    c5fd2f071bde071f4363def7dea8dec7393e135c
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     zendframework
%global gh_project   zend-loader
%global php_home     %{_datadir}/php
%global library      Loader
%global with_tests   0%{!?_without_tests:1}

Name:           php-%{gh_owner}-%{gh_project}
Version:        2.5.1
Release:        3%{?dist}
Summary:        Zend Framework %{library} component

Group:          Development/Libraries
License:        BSD
URL:            https://framework.zend.com/
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{name}-%{version}-%{gh_short}.tar.gz
Source1:        %{name}-autoload.php

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch:      noarch
# Tests
%if %{with_tests}
BuildRequires:  php(language) >= 5.3.23
BuildRequires:  php-cli
%endif

# From composer, "require": {
#        "php": ">=5.3.23"
Requires:       php(language) >= 5.3.23
# From phpcompatinfo report for version 2.5.1
Requires:       php-pcre
Requires:       php-spl

Obsoletes:      php-ZendFramework2-%{library} < 2.5
Provides:       php-ZendFramework2-%{library} = %{version}
Provides:       php-composer(%{gh_owner}/%{gh_project}) = %{version}


%description
Zend\Loader provides different strategies for autoloading PHP classes.

You can include %{php_home}/Zend/autoload.php from
your application to use the Zend Framework.

Documentation: https://zendframework.github.io/%{gh_project}/


%prep
%setup -q -n %{gh_project}-%{gh_commit}

mv LICENSE.md LICENSE


%build
# Empty build section, nothing required


%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{php_home}/Zend
install -pm 644 %{SOURCE1} %{buildroot}%{php_home}/Zend/autoload.php

cp -pr src %{buildroot}%{php_home}/Zend/%{library}


%check
%if %{with_tests}
%{_bindir}/php -r '
    require "%{buildroot}%{php_home}/Zend/autoload.php";
    exit (class_exists("Zend\\Loader\\PluginClassLoader" ? 0 : 1));
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
%dir %{php_home}/Zend
     %{php_home}/Zend/autoload.php
     %{php_home}/Zend/%{library}


%changelog
* Mon May  2 2016 Remi Collet <remi@fedoraproject.org> - 2.5.1-3
- load dependencies out of Zend namespaces

* Tue Aug  4 2015 Remi Collet <remi@fedoraproject.org> - 2.5.1-1
- initial package
