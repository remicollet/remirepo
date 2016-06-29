# remirepo/Fedora spec file for php-zendframework
#
# Copyright (c) 2015-2016 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    7fb89c778508c3969b04d478c6f02a5a54e3bbd2
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     zendframework
%global gh_project   zendframework
%global php_home     %{_datadir}/php

Name:           php-%{gh_owner}
Version:        3.0.0
Release:        1%{?dist}
Summary:        Zend Framework

Group:          Development/Libraries
License:        BSD
URL:            https://framework.zend.com/
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{name}-%{version}-%{gh_short}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch:      noarch

# From composer, "require": {
#        "php": "^5.6 || ^7.0",
#        "zendframework/zend-authentication": "^2.5.3",
#        "zendframework/zend-barcode": "^2.6",
#        "zendframework/zend-cache": "^2.7.1",
#        "zendframework/zend-captcha": "^2.6",
#        "zendframework/zend-code": "^3.0.2",
#        "zendframework/zend-config": "^2.6",
#        "zendframework/zend-console": "^2.6",
#        "zendframework/zend-crypt": "^3.0",
#        "zendframework/zend-db": "^2.8.1",
#        "zendframework/zend-debug": "^2.5.1",
#        "zendframework/zend-di": "^2.6.1",
#        "zendframework/zend-diactoros": "^1.3.5",
#        "zendframework/zend-dom": "^2.6",
#        "zendframework/zend-escaper": "^2.5.1",
#        "zendframework/zend-eventmanager": "^3.0.1",
#        "zendframework/zend-feed": "^2.7",
#        "zendframework/zend-file": "^2.7",
#        "zendframework/zend-filter": "^2.7.1",
#        "zendframework/zend-form": "^2.9",
#        "zendframework/zend-http": "^2.5.4",
#        "zendframework/zend-hydrator": "^2.2.1",
#        "zendframework/zend-i18n": "^2.7.3",
#        "zendframework/zend-i18n-resources": "^2.5.2",
#        "zendframework/zend-inputfilter": "^2.7.2",
#        "zendframework/zend-json": "^3.0",
#        "zendframework/zend-json-server": "^3.0",
#        "zendframework/zend-loader": "^2.5.1",
#        "zendframework/zend-log": "^2.9",
#        "zendframework/zend-mail": "^2.7.1",
#        "zendframework/zend-math": "^3.0",
#        "zendframework/zend-memory": "^2.5.2",
#        "zendframework/zend-mime": "^2.6",
#        "zendframework/zend-modulemanager": "^2.7.2",
#        "zendframework/zend-mvc": "^3.0.1",
#        "zendframework/zend-mvc-console": "^1.1.9",
#        "zendframework/zend-mvc-form": "^1.0",
#        "zendframework/zend-mvc-i18n": "^1.0",
#        "zendframework/zend-mvc-plugins": "^1.0.1",
#        "zendframework/zend-navigation": "^2.8.1",
#        "zendframework/zend-paginator": "^2.7",
#        "zendframework/zend-permissions-acl": "^2.6",
#        "zendframework/zend-permissions-rbac": "^2.5.1",
#        "zendframework/zend-progressbar": "^2.5.2",
#        "zendframework/zend-psr7bridge": "^0.2.2",
#        "zendframework/zend-serializer": "^2.8",
#        "zendframework/zend-server": "^2.7.0",
#        "zendframework/zend-servicemanager": "^3.1",
#        "zendframework/zend-servicemanager-di": "^1.1",
#        "zendframework/zend-session": "^2.7.1",
#        "zendframework/zend-soap": "^2.6",
#        "zendframework/zend-stdlib": "^3.0.1",
#        "zendframework/zend-stratigility": "^1.2.1",
#        "zendframework/zend-tag": "^2.6.1",
#        "zendframework/zend-test": "^3.0.1",
#        "zendframework/zend-text": "^2.6",
#        "zendframework/zend-uri": "^2.5.2",
#        "zendframework/zend-validator": "^2.8",
#        "zendframework/zend-view": "^2.8",
#        "zendframework/zend-xml2json": "^3.0",
#        "zendframework/zend-xmlrpc": "^2.6",
#        "zendframework/zendxml": "^1.0.2"
Requires:       php(language) >= 5.6
Requires:       php-composer(%{gh_owner}/zend-authentication)    >= 2.5.3
Requires:       php-composer(%{gh_owner}/zend-authentication)    <  3
Requires:       php-composer(%{gh_owner}/zend-barcode)           >= 2.6
Requires:       php-composer(%{gh_owner}/zend-barcode)           <  3
Requires:       php-composer(%{gh_owner}/zend-cache)             >= 2.7.1
Requires:       php-composer(%{gh_owner}/zend-cache)             <  3
Requires:       php-composer(%{gh_owner}/zend-captcha)           >= 2.6
Requires:       php-composer(%{gh_owner}/zend-captcha)           <  3
Requires:       php-composer(%{gh_owner}/zend-code)              >= 3.0.2
Requires:       php-composer(%{gh_owner}/zend-code)              <  4
Requires:       php-composer(%{gh_owner}/zend-config)            >= 2.6
Requires:       php-composer(%{gh_owner}/zend-config)            <  3
Requires:       php-composer(%{gh_owner}/zend-console)           >= 2.6
Requires:       php-composer(%{gh_owner}/zend-console)           <  3
Requires:       php-composer(%{gh_owner}/zend-crypt)             >= 3.0
Requires:       php-composer(%{gh_owner}/zend-crypt)             <  4
Requires:       php-composer(%{gh_owner}/zend-db)                >= 2.8.1
Requires:       php-composer(%{gh_owner}/zend-db)                <  3
Requires:       php-composer(%{gh_owner}/zend-debug)             >= 2.5.1
Requires:       php-composer(%{gh_owner}/zend-debug)             <  3
Requires:       php-composer(%{gh_owner}/zend-di)                >= 2.6.1
Requires:       php-composer(%{gh_owner}/zend-di)                <  3
Requires:       php-composer(%{gh_owner}/zend-diactoros)         >= 1.3.5
Requires:       php-composer(%{gh_owner}/zend-diactoros)         <  2
Requires:       php-composer(%{gh_owner}/zend-dom)               >= 2.6
Requires:       php-composer(%{gh_owner}/zend-dom)               <  3
Requires:       php-composer(%{gh_owner}/zend-escaper)           >= 2.5.1
Requires:       php-composer(%{gh_owner}/zend-escaper)           <  3
Requires:       php-composer(%{gh_owner}/zend-eventmanager)      >= 3.0.1
Requires:       php-composer(%{gh_owner}/zend-eventmanager)      <  4
Requires:       php-composer(%{gh_owner}/zend-feed)              >= 2.7
Requires:       php-composer(%{gh_owner}/zend-feed)              <  3
Requires:       php-composer(%{gh_owner}/zend-file)              >= 2.7
Requires:       php-composer(%{gh_owner}/zend-file)              <  3
Requires:       php-composer(%{gh_owner}/zend-filter)            >= 2.7.1
Requires:       php-composer(%{gh_owner}/zend-filter)            <  3
Requires:       php-composer(%{gh_owner}/zend-form)              >= 2.9
Requires:       php-composer(%{gh_owner}/zend-form)              <  3
Requires:       php-composer(%{gh_owner}/zend-http)              >= 2.5.4
Requires:       php-composer(%{gh_owner}/zend-http)              <  3
Requires:       php-composer(%{gh_owner}/zend-hydrator)          >= 2.2.1
Requires:       php-composer(%{gh_owner}/zend-hydrator)          <  3
Requires:       php-composer(%{gh_owner}/zend-i18n)              >= 2.7.3
Requires:       php-composer(%{gh_owner}/zend-i18n)              <  3
Requires:       php-composer(%{gh_owner}/zend-i18n-resources)    >= 2.5.2
Requires:       php-composer(%{gh_owner}/zend-i18n-resources)    <  3
Requires:       php-composer(%{gh_owner}/zend-inputfilter)       >= 2.7.2
Requires:       php-composer(%{gh_owner}/zend-inputfilter)       <  3
Requires:       php-composer(%{gh_owner}/zend-json)              >= 3.0
Requires:       php-composer(%{gh_owner}/zend-json)              <  4
Requires:       php-composer(%{gh_owner}/zend-json-server)       >= 3.0
Requires:       php-composer(%{gh_owner}/zend-json-server)       <  4
Requires:       php-composer(%{gh_owner}/zend-loader)            >= 2.5.1
Requires:       php-composer(%{gh_owner}/zend-loader)            <  3
Requires:       php-composer(%{gh_owner}/zend-log)               >= 2.9
Requires:       php-composer(%{gh_owner}/zend-log)               <  3
Requires:       php-composer(%{gh_owner}/zend-mail)              >= 2.7.1
Requires:       php-composer(%{gh_owner}/zend-mail)              <  3
Requires:       php-composer(%{gh_owner}/zend-math)              >= 3.0
Requires:       php-composer(%{gh_owner}/zend-math)              <  4
Requires:       php-composer(%{gh_owner}/zend-memory)            >= 2.5.2
Requires:       php-composer(%{gh_owner}/zend-memory)            <  3
Requires:       php-composer(%{gh_owner}/zend-mime)              >= 2.6
Requires:       php-composer(%{gh_owner}/zend-mime)              <  3
Requires:       php-composer(%{gh_owner}/zend-modulemanager)     >= 2.7.2
Requires:       php-composer(%{gh_owner}/zend-modulemanager)     <  3
Requires:       php-composer(%{gh_owner}/zend-mvc)               >= 3.0.1
Requires:       php-composer(%{gh_owner}/zend-mvc)               <  4
Requires:       php-composer(%{gh_owner}/zend-mvc-console)       >= 1.1.9
Requires:       php-composer(%{gh_owner}/zend-mvc-console)       <  2
Requires:       php-composer(%{gh_owner}/zend-mvc-form)          >= 1.0
Requires:       php-composer(%{gh_owner}/zend-mvc-form)          <  2
Requires:       php-composer(%{gh_owner}/zend-mvc-i18n)          >= 1.0
Requires:       php-composer(%{gh_owner}/zend-mvc-i18n)          <  2
Requires:       php-composer(%{gh_owner}/zend-mvc-plugins)       >= 1.0.1
Requires:       php-composer(%{gh_owner}/zend-mvc-plugins)       <  2
Requires:       php-composer(%{gh_owner}/zend-navigation)        >= 2.8.1
Requires:       php-composer(%{gh_owner}/zend-navigation)        <  3
Requires:       php-composer(%{gh_owner}/zend-paginator)         >= 2.7
Requires:       php-composer(%{gh_owner}/zend-paginator)         <  3
Requires:       php-composer(%{gh_owner}/zend-permissions-acl)   >= 2.6
Requires:       php-composer(%{gh_owner}/zend-permissions-acl)   <  3
Requires:       php-composer(%{gh_owner}/zend-permissions-rbac)  >= 2.5.1
Requires:       php-composer(%{gh_owner}/zend-permissions-rbac)  <  3
Requires:       php-composer(%{gh_owner}/zend-progressbar)       >= 2.5.2
Requires:       php-composer(%{gh_owner}/zend-progressbar)       <  3
Requires:       php-composer(%{gh_owner}/zend-psr7bridge)        >= 0.2.2
Requires:       php-composer(%{gh_owner}/zend-psr7bridge)        <  1
Requires:       php-composer(%{gh_owner}/zend-serializer)        >= 2.8
Requires:       php-composer(%{gh_owner}/zend-serializer)        <  3
Requires:       php-composer(%{gh_owner}/zend-server)            >= 2.7
Requires:       php-composer(%{gh_owner}/zend-server)            <  3
Requires:       php-composer(%{gh_owner}/zend-servicemanager)    >= 3.1
Requires:       php-composer(%{gh_owner}/zend-servicemanager)    <  4
Requires:       php-composer(%{gh_owner}/zend-servicemanager-di) >= 1.1
Requires:       php-composer(%{gh_owner}/zend-servicemanager-di) <  2
Requires:       php-composer(%{gh_owner}/zend-session)           >= 2.7.1
Requires:       php-composer(%{gh_owner}/zend-session)           <  3
Requires:       php-composer(%{gh_owner}/zend-soap)              >= 2.6
Requires:       php-composer(%{gh_owner}/zend-soap)              <  3
Requires:       php-composer(%{gh_owner}/zend-stdlib)            >= 3.0.1
Requires:       php-composer(%{gh_owner}/zend-stdlib)            <  4
Requires:       php-composer(%{gh_owner}/zend-stratigility)      >= 1.2.1
Requires:       php-composer(%{gh_owner}/zend-stratigility)      <  2
Requires:       php-composer(%{gh_owner}/zend-tag)               >= 2.6.1
Requires:       php-composer(%{gh_owner}/zend-tag)               <  3
Requires:       php-composer(%{gh_owner}/zend-test)              >= 3.0.1
Requires:       php-composer(%{gh_owner}/zend-test)              <  4
Requires:       php-composer(%{gh_owner}/zend-text)              >= 2.6
Requires:       php-composer(%{gh_owner}/zend-text)              <  3
Requires:       php-composer(%{gh_owner}/zend-uri)               >= 2.5.2
Requires:       php-composer(%{gh_owner}/zend-uri)               <  3
Requires:       php-composer(%{gh_owner}/zend-validator)         >= 2.8
Requires:       php-composer(%{gh_owner}/zend-validator)         <  3
Requires:       php-composer(%{gh_owner}/zend-view)              >= 2.8
Requires:       php-composer(%{gh_owner}/zend-view)              <  3
Requires:       php-composer(%{gh_owner}/zend-xml2json)          >= 3.0
Requires:       php-composer(%{gh_owner}/zend-xml2json)          <  4
Requires:       php-composer(%{gh_owner}/zend-xmlrpc)            >= 2.6
Requires:       php-composer(%{gh_owner}/zend-xmlrpc)            <  3
Requires:       php-composer(%{gh_owner}/zendxml)                >= 1.0.2
Requires:       php-composer(%{gh_owner}/zendxml)                <  2
# From composer, "suggest": {
#        "zendframework/zend-ldap": "zend-ldap component ^2.7.1, if you need LDAP features"
%if 0%{?fedora} >= 21
Suggests:       php-composer(%{gh_owner}/zend-ldap)              >= 2.7.1
Suggests:       php-composer(%{gh_owner}/zend-ldap)              <  3
%endif
# From phpcompatinfo report for version 2.5.2
Requires:       php-cli
Requires:       php-date
Requires:       php-pcre
Requires:       php-spl

# v1 and v2 cannot be installed at the same time
Conflicts: php-ZendFramework < 2
# Rename
Obsoletes:      php-ZendFramework2        < 2.5
Obsoletes:      php-ZendFramework2-common < 2.5
Provides:       php-ZendFramework2        = %{version}
Provides:       php-ZendFramework2-common = %{version}
# Removed component
Obsoletes:      php-zendframework-zend-version < 2.5.2

# Composer
Provides:       php-composer(%{gh_owner}/%{gh_project}) = %{version}


%description
Zend Framework is an open source framework for developing web applications
and services using PHP.

This package is a metapackage aggregating most of the components.

Documentation: https://zendframework.github.io/


%prep
%setup -q -n %{gh_project}-%{gh_commit}


%build
# Empty build section, nothing required


%install
# Nothing

%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE.md
%doc CHANGELOG.md CONDUCT.md CONTRIBUTING.md README.md
%doc composer.json


%changelog
* Wed Jun 29 2016 Remi Collet <remi@fedoraproject.org> - 3.0.0-1
- Zend Framework 3
- drop dependency on zend-version
- add dependencies on zend-diactoros, zend-hydrator,
  zend-json-server, zend-mvc-console, zend-mvc-form,
  zend-mvc-i18n, zend-mvc-plugins, zend-psr7bridge,
  zend-servicemanager-di, zend-stratigility, zend-xml2json

* Wed Jun 22 2016 Remi Collet <remi@fedoraproject.org> - 2.5.3-3
- drop zf_templatemap_generator command (moved in zend-view)

* Thu Jan 28 2016 Remi Collet <remi@fedoraproject.org> - 2.5.3-1
- update to 2.5.3
- raise max components version from 2.6 to 3

* Thu Aug  6 2015 Remi Collet <remi@fedoraproject.org> - 2.5.2-1
- initial package
