# remirepo/Fedora spec file for php-zendframework
#
# Copyright (c) 2015-2016 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    aeb432d59410cd9a4a68166738745387a9bf49ab
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     zendframework
%global gh_project   zf2
%global php_home     %{_datadir}/php

%global minver       2.5
%global maxver       3

Name:           php-%{gh_owner}
Version:        2.5.3
Release:        3%{?dist}
Summary:        Zend Framework

Group:          Development/Libraries
License:        BSD
URL:            http://framework.zend.com/
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{name}-%{version}-%{gh_short}.tar.gz

# Use our Autoloader
Patch0:         %{name}-autoload.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch:      noarch

# From composer, "require": {
#        "php": "^5.5 || ^7.0",
#        "zendframework/zend-authentication": "^2.5",
#        "zendframework/zend-barcode": "^2.5",
#        "zendframework/zend-cache": "^2.5",
#        "zendframework/zend-captcha": "^2.5",
#        "zendframework/zend-code": "^2.5",
#        "zendframework/zend-config": "^2.5",
#        "zendframework/zend-console": "^2.5",
#        "zendframework/zend-crypt": "^2.5",
#        "zendframework/zend-db": "^2.5",
#        "zendframework/zend-debug": "^2.5",
#        "zendframework/zend-di": "^2.5",
#        "zendframework/zend-dom": "^2.5",
#        "zendframework/zend-escaper": "^2.5",
#        "zendframework/zend-eventmanager": "^2.5",
#        "zendframework/zend-feed": "^2.5",
#        "zendframework/zend-file": "^2.5",
#        "zendframework/zend-filter": "^2.5",
#        "zendframework/zend-form": "^2.5",
#        "zendframework/zend-http": "^2.5",
#        "zendframework/zend-i18n": "^2.5",
#        "zendframework/zend-i18n-resources": "^2.5",
#        "zendframework/zend-inputfilter": "^2.5",
#        "zendframework/zend-json": "^2.5",
#        "zendframework/zend-loader": "^2.5",
#        "zendframework/zend-log": "^2.5",
#        "zendframework/zend-mail": "^2.5",
#        "zendframework/zend-math": "^2.5",
#        "zendframework/zend-memory": "^2.5",
#        "zendframework/zend-mime": "^2.5",
#        "zendframework/zend-modulemanager": "^2.5",
#        "zendframework/zend-mvc": "^2.5",
#        "zendframework/zend-navigation": "^2.5",
#        "zendframework/zend-paginator": "^2.5",
#        "zendframework/zend-permissions-acl": "^2.5",
#        "zendframework/zend-permissions-rbac": "^2.5",
#        "zendframework/zend-progressbar": "^2.5",
#        "zendframework/zend-serializer": "^2.5",
#        "zendframework/zend-server": "^2.5",
#        "zendframework/zend-servicemanager": "^2.5",
#        "zendframework/zend-session": "^2.5",
#        "zendframework/zend-soap": "^2.5",
#        "zendframework/zend-stdlib": "^2.5",
#        "zendframework/zend-tag": "^2.5",
#        "zendframework/zend-test": "^2.5",
#        "zendframework/zend-text": "^2.5",
#        "zendframework/zend-uri": "^2.5",
#        "zendframework/zend-validator": "^2.5",
#        "zendframework/zend-version": "^2.5",
#        "zendframework/zend-view": "^2.5",
#        "zendframework/zend-xmlrpc": "^2.5",
#        "zendframework/zendxml": "^1.0.1"
Requires:       php(language) >= 5.5
Requires:       php-composer(%{gh_owner}/zend-authentication)   >= %{minver}
Requires:       php-composer(%{gh_owner}/zend-authentication)   <  %{maxver}
Requires:       php-composer(%{gh_owner}/zend-barcode)          >= %{minver}
Requires:       php-composer(%{gh_owner}/zend-barcode)          <  %{maxver}
Requires:       php-composer(%{gh_owner}/zend-cache)            >= %{minver}
Requires:       php-composer(%{gh_owner}/zend-cache)            <  %{maxver}
Requires:       php-composer(%{gh_owner}/zend-captcha)          >= %{minver}
Requires:       php-composer(%{gh_owner}/zend-captcha)          <  %{maxver}
Requires:       php-composer(%{gh_owner}/zend-code)             >= %{minver}
Requires:       php-composer(%{gh_owner}/zend-code)             <  %{maxver}
Requires:       php-composer(%{gh_owner}/zend-config)           >= %{minver}
Requires:       php-composer(%{gh_owner}/zend-config)           <  %{maxver}
Requires:       php-composer(%{gh_owner}/zend-console)          >= %{minver}
Requires:       php-composer(%{gh_owner}/zend-console)          <  %{maxver}
Requires:       php-composer(%{gh_owner}/zend-crypt)            >= %{minver}
Requires:       php-composer(%{gh_owner}/zend-crypt)            <  %{maxver}
Requires:       php-composer(%{gh_owner}/zend-db)               >= %{minver}
Requires:       php-composer(%{gh_owner}/zend-db)               <  %{maxver}
Requires:       php-composer(%{gh_owner}/zend-debug)            >= %{minver}
Requires:       php-composer(%{gh_owner}/zend-debug)            <  %{maxver}
Requires:       php-composer(%{gh_owner}/zend-di)               >= %{minver}
Requires:       php-composer(%{gh_owner}/zend-di)               <  %{maxver}
Requires:       php-composer(%{gh_owner}/zend-dom)              >= %{minver}
Requires:       php-composer(%{gh_owner}/zend-dom)              <  %{maxver}
Requires:       php-composer(%{gh_owner}/zend-escaper)          >= %{minver}
Requires:       php-composer(%{gh_owner}/zend-escaper)          <  %{maxver}
Requires:       php-composer(%{gh_owner}/zend-eventmanager)     >= %{minver}
Requires:       php-composer(%{gh_owner}/zend-eventmanager)     <  %{maxver}
Requires:       php-composer(%{gh_owner}/zend-feed)             >= %{minver}
Requires:       php-composer(%{gh_owner}/zend-feed)             <  %{maxver}
Requires:       php-composer(%{gh_owner}/zend-file)             >= %{minver}
Requires:       php-composer(%{gh_owner}/zend-file)             <  %{maxver}
Requires:       php-composer(%{gh_owner}/zend-filter)           >= %{minver}
Requires:       php-composer(%{gh_owner}/zend-filter)           <  %{maxver}
Requires:       php-composer(%{gh_owner}/zend-form)             >= %{minver}
Requires:       php-composer(%{gh_owner}/zend-form)             <  %{maxver}
Requires:       php-composer(%{gh_owner}/zend-http)             >= %{minver}
Requires:       php-composer(%{gh_owner}/zend-http)             <  %{maxver}
Requires:       php-composer(%{gh_owner}/zend-i18n)             >= %{minver}
Requires:       php-composer(%{gh_owner}/zend-i18n)             <  %{maxver}
Requires:       php-composer(%{gh_owner}/zend-i18n-resources)   >= %{minver}
Requires:       php-composer(%{gh_owner}/zend-i18n-resources)   <  %{maxver}
Requires:       php-composer(%{gh_owner}/zend-inputfilter)      >= %{minver}
Requires:       php-composer(%{gh_owner}/zend-inputfilter)      <  %{maxver}
Requires:       php-composer(%{gh_owner}/zend-json)             >= %{minver}
Requires:       php-composer(%{gh_owner}/zend-json)             <  %{maxver}
Requires:       php-composer(%{gh_owner}/zend-loader)           >= %{minver}
Requires:       php-composer(%{gh_owner}/zend-loader)           <  %{maxver}
Requires:       php-composer(%{gh_owner}/zend-log)              >= %{minver}
Requires:       php-composer(%{gh_owner}/zend-log)              <  %{maxver}
Requires:       php-composer(%{gh_owner}/zend-mail)             >= %{minver}
Requires:       php-composer(%{gh_owner}/zend-mail)             <  %{maxver}
Requires:       php-composer(%{gh_owner}/zend-math)             >= %{minver}
Requires:       php-composer(%{gh_owner}/zend-math)             <  %{maxver}
Requires:       php-composer(%{gh_owner}/zend-memory)           >= %{minver}
Requires:       php-composer(%{gh_owner}/zend-memory)           <  %{maxver}
Requires:       php-composer(%{gh_owner}/zend-mime)             >= %{minver}
Requires:       php-composer(%{gh_owner}/zend-mime)             <  %{maxver}
Requires:       php-composer(%{gh_owner}/zend-modulemanager)    <  %{maxver}
Requires:       php-composer(%{gh_owner}/zend-modulemanager)    >= %{minver}
Requires:       php-composer(%{gh_owner}/zend-mvc)              >= %{minver}
Requires:       php-composer(%{gh_owner}/zend-mvc)              <  %{maxver}
Requires:       php-composer(%{gh_owner}/zend-navigation)       >= %{minver}
Requires:       php-composer(%{gh_owner}/zend-navigation)       <  %{maxver}
Requires:       php-composer(%{gh_owner}/zend-paginator)        >= %{minver}
Requires:       php-composer(%{gh_owner}/zend-paginator)        <  %{maxver}
Requires:       php-composer(%{gh_owner}/zend-permissions-acl)  >= %{minver}
Requires:       php-composer(%{gh_owner}/zend-permissions-acl)  <  %{maxver}
Requires:       php-composer(%{gh_owner}/zend-permissions-rbac) >= %{minver}
Requires:       php-composer(%{gh_owner}/zend-permissions-rbac) <  %{maxver}
Requires:       php-composer(%{gh_owner}/zend-progressbar)      >= %{minver}
Requires:       php-composer(%{gh_owner}/zend-progressbar)      <  %{maxver}
Requires:       php-composer(%{gh_owner}/zend-serializer)       >= %{minver}
Requires:       php-composer(%{gh_owner}/zend-serializer)       <  %{maxver}
Requires:       php-composer(%{gh_owner}/zend-server)           >= %{minver}
Requires:       php-composer(%{gh_owner}/zend-server)           <  %{maxver}
Requires:       php-composer(%{gh_owner}/zend-servicemanager)   >= %{minver}
Requires:       php-composer(%{gh_owner}/zend-servicemanager)   <  %{maxver}
Requires:       php-composer(%{gh_owner}/zend-session)          >= %{minver}
Requires:       php-composer(%{gh_owner}/zend-session)          <  %{maxver}
Requires:       php-composer(%{gh_owner}/zend-soap)             >= %{minver}
Requires:       php-composer(%{gh_owner}/zend-soap)             <  %{maxver}
Requires:       php-composer(%{gh_owner}/zend-stdlib)           >= %{minver}
Requires:       php-composer(%{gh_owner}/zend-stdlib)           <  %{maxver}
Requires:       php-composer(%{gh_owner}/zend-tag)              >= %{minver}
Requires:       php-composer(%{gh_owner}/zend-tag)              <  %{maxver}
Requires:       php-composer(%{gh_owner}/zend-test)             >= %{minver}
Requires:       php-composer(%{gh_owner}/zend-test)             <  %{maxver}
Requires:       php-composer(%{gh_owner}/zend-text)             >= %{minver}
Requires:       php-composer(%{gh_owner}/zend-text)             <  %{maxver}
Requires:       php-composer(%{gh_owner}/zend-uri)              >= %{minver}
Requires:       php-composer(%{gh_owner}/zend-uri)              <  %{maxver}
Requires:       php-composer(%{gh_owner}/zend-validator)        >= %{minver}
Requires:       php-composer(%{gh_owner}/zend-validator)        <  %{maxver}
Requires:       php-composer(%{gh_owner}/zend-version)          >= %{minver}
Requires:       php-composer(%{gh_owner}/zend-version)          <  %{maxver}
Requires:       php-composer(%{gh_owner}/zend-view)             >= %{minver}
Requires:       php-composer(%{gh_owner}/zend-view)             <  %{maxver}
Requires:       php-composer(%{gh_owner}/zend-xmlrpc)           >= %{minver}
Requires:       php-composer(%{gh_owner}/zend-xmlrpc)           <  %{maxver}
Requires:       php-composer(%{gh_owner}/zendxml)               >= 1.0.1
Requires:       php-composer(%{gh_owner}/zendxml)               <  2
# From composer, "suggest": {
#        "zendframework/zend-ldap": "zend-ldap component ^2.5, if you need LDAP features"
%if 0%{?fedora} >= 21
Suggests:       php-composer(%{gh_owner}/zend-ldap)             >= %{minver}
Suggests:       php-composer(%{gh_owner}/zend-ldap)             <  %{maxver}
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
# Composer
Provides:       php-composer(%{gh_owner}/%{gh_owner}) = %{version}


%description
Zend Framework is an open source framework for developing web applications
and services using PHP.

This package is a metapackage aggregating most of the components.

Documentation: https://zendframework.github.io/


%prep
%setup -q -n %{gh_project}-%{gh_commit}

%patch0 -p0 -b .rpm


%build
# Empty build section, nothing required


%install
rm -rf %{buildroot}

# From composer.json,     "bin": [
#        "bin/classmap_generator.php",
#        "bin/pluginmap_generator.php",
#        "bin/templatemap_generator.php"

for i in bin/classmap_generator.php bin/pluginmap_generator.php
do   install -Dpm 755 $i %{buildroot}%{_bindir}/zf_$(basename $i .php)
done


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE.md
%doc CHANGELOG.md CONTRIBUTING.md README.md
%doc composer.json
%{_bindir}/zf_classmap_generator
%{_bindir}/zf_pluginmap_generator


%changelog
* Wed Jun 22 2016 Remi Collet <remi@fedoraproject.org> - 2.5.3-3
- drop zf_templatemap_generator command (moved in zend-view)

* Thu Jan 28 2016 Remi Collet <remi@fedoraproject.org> - 2.5.3-1
- update to 2.5.3
- raise max components version from 2.6 to 3

* Thu Aug  6 2015 Remi Collet <remi@fedoraproject.org> - 2.5.2-1
- initial package
