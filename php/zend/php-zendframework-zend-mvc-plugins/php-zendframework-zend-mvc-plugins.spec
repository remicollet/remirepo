# remirepo/Fedora spec file for php-zendframework-zend-mvc-plugins
#
# Copyright (c) 2016-2017 Remi Collet
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
Release:        2%{?dist}
Summary:        Zend Framework Mvc-Plugins component

Group:          Development/Libraries
License:        BSD
URL:            https://framework.zend.com/
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
zend-mvc-plugins is a metapackage that provides a single package for
installing all official zend-mvc plugins shipped as separate packages
under the zendframework organization. Currently, these include:

* zendframework/zend-mvc-plugin-fileprg
* zendframework/zend-mvc-plugin-flashmessenger
* zendframework/zend-mvc-plugin-identity
* zendframework/zend-mvc-plugin-prg


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
* Tue Jul 26 2016 Remi Collet <remi@fedoraproject.org> - 1.0.1-2
- fix summary and description

* Wed Jun 29 2016 Remi Collet <remi@fedoraproject.org> - 1.0.1-1
- initial package

