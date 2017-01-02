# remirepo/Fedora spec file for php-zendframework-zend-mvc-form
#
# Copyright (c) 2016-2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    28bf47ce6661fd71f1b8d68f9b6bc8f841f6aeb0
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     zendframework
%global gh_project   zend-mvc-form

Name:           php-%{gh_owner}-%{gh_project}
Version:        1.0.0
Release:        2%{?dist}
Summary:        Zend Framework Mvc-Form component

Group:          Development/Libraries
License:        BSD
URL:            https://framework.zend.com/
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{name}-%{version}-%{gh_short}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch:      noarch

# From composer, "require": {
#        "php": "^5.6 || ^7.0",
#        "zendframework/zend-code": "^2.6.3 || ^3.0.2",
#        "zendframework/zend-form": "^2.8.4",
#        "zendframework/zend-i18n": "^2.7.2"
Requires:       php(language) >= 5.6
Requires:       php-composer(%{gh_owner}/zend-code)               >= 2.6.3
Requires:       php-composer(%{gh_owner}/zend-code)               <  4
Requires:       php-composer(%{gh_owner}/zend-form)               >= 2.8.4
Requires:       php-composer(%{gh_owner}/zend-form)               <  3
Requires:       php-composer(%{gh_owner}/zend-i18n)               >= 2.7.2
Requires:       php-composer(%{gh_owner}/zend-i18n)               <  3

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

mv LICENSE.md LICENSE


%build
# Empty build section, nothing required


%install
# Nothing


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc *.md
%doc composer.json


%changelog
* Tue Jul 26 2016 Remi Collet <remi@fedoraproject.org> - 1.0.0-2
- fix summary

* Wed Jun 29 2016 Remi Collet <remi@fedoraproject.org> - 1.0.0-1
- initial package

