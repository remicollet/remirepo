# spec file for php-bartlett-umlwriter
#
# Copyright (c) 2015 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    0fe1c3a19280e4cd9f136ff3347ae9d0110758ca
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
#global gh_date      20150303
%global gh_owner     llaville
%global gh_project   umlwriter
%global prever       RC1

Name:           php-bartlett-umlwriter
Version:        1.0.0
%global specrel 1
Release:        %{?gh_short:0.%{specrel}.%{?gh_date:%{gh_date}git%{gh_short}}%{?prever}}%{!?gh_short:%{specrel}}%{?dist}
Summary:        Create UML class diagrams from your PHP source

Group:          Development/Libraries
License:        BSD
URL:            http://php5.laurent-laville.org/umlwriter/
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}%{?prever}%{?gh_short:-%{gh_short}}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php(language) >= 5.3.0

# From composer.json
#    "require": {
#        "php": ">=5.3.0"
#    "suggest": {
#        "bartlett/php-reflect": "Reverse-engine compatible solution 1",
#        "andrewsville/php-token-reflection": "Reverse-engine compatible solution 2"
Requires:       php(language) >= 5.3.0
# Notice, we do not require Reflect to avoid circular dependencies

Provides:       php-composer(bartlett/umlwriter) = %{version}


%description
This tool wil generate UML class diagrams with all class,
interface and trait definitions in your PHP project.

* reverse-engine interchangeable (currently support Bartlett\Reflect
  and Andrewsville\TokenReflection)
* UML syntax processor interchangeable (currently support Graphviz
  and PlantUML)
* generates a class and its direct dependencies
* generates a namespace with all objects
* generates a full package with all namespaces and objects


%prep
%setup -q -n %{gh_project}-%{gh_commit}

sed -e 's/@package_version@/%{version}%{?prever}/' \
    -i $(find src -name \*.php)


%build
# Nothing


%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_datadir}/php
cp -pr src/Bartlett %{buildroot}%{_datadir}/php/Bartlett


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc composer.json README.* examples
%dir %{_datadir}/php/Bartlett
     %{_datadir}/php/Bartlett/UmlWriter


%changelog
* Tue Mar 24 2015 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.1.RC1
- Initial RPM package, version 1.0.0RC1