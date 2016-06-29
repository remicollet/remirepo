# remirepo/Fedora spec file for php-zendframework-zend-mvc-plugins
#
# Copyright (c) 2016 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    b00cda46b0a95cbd32ea0743d6d7dc3fd2263f1b
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     zendframework
%global gh_project   zend-mvc-plugins

Name:           php-%{gh_owner}-%{gh_project}
Version:        1.0.1
Release:        1%{?dist}
Summary:        Zend Framework Mvc-%{library} component

Group:          Development/Libraries
License:        BSD
URL:            http://framework.zend.com/
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{name}-%{version}-%{gh_short}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch:      noarch

# From composer, "require": {
#        "php": "^5.6 || ^7.0",
#        "zendframework/zend-mvc-plugin-fileprg": "^1.0",
#        "zendframework/zend-mvc-plugin-flashmessenger": "^1.0",
#        "zendframework/zend-mvc-plugin-identity": "^1.0",
#        "zendframework/zend-mvc-plugin-prg": "^1.0"
Requires:       php(language) >= 5.6
Requires:       php-composer(%{gh_owner}/zend-mvc-plugin-fileprg)        >= 1.0
Requires:       php-composer(%{gh_owner}/zend-mvc-plugin-fileprg)        <  2
Requires:       php-composer(%{gh_owner}/zend-mvc-plugin-flashmessenger) >= 1.0
Requires:       php-composer(%{gh_owner}/zend-mvc-plugin-flashmessenger) <  2
Requires:       php-composer(%{gh_owner}/zend-mvc-plugin-identity)       >= 1.0
Requires:       php-composer(%{gh_owner}/zend-mvc-plugin-identity)       <  2
Requires:       php-composer(%{gh_owner}/zend-mvc-plugin-prg)            >= 1.0
Requires:       php-composer(%{gh_owner}/zend-mvc-plugin-prg)            <  2

Provides:       php-composer(%{gh_owner}/%{gh_project}) = %{version}


%description
zend-mvc-form is a metapackage that provides a single package for installing
all packages necessary to fully use zend-form under zend-mvc, including:

* zendframework/zend-code
* zendframework/zend-form
* zendframework/zend-i18n

i18n integration: this package only requires zend-i18n, and not zend-mvc-i18n.
This is to allow providing the bare minimum required to use zend-form, as its
base view helper extends from the base zend-i18n view helper. If you want to
provide translations for your form elements, please install zend-mvc-i18n as
well.


%prep
%setup -q -n %{gh_project}-%{gh_commit}


%build
# Empty build section, nothing required


%install
# Nothing


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE.md
%doc CHANGELOG.md README.md
%doc composer.json


%changelog
* Wed Jun 29 2016 Remi Collet <remi@fedoraproject.org> - 1.0.1-1
- initial package

