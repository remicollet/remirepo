# spec file for php-theseer-fxsl
#
# Copyright (c) 2014-2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#

%global gh_commit    a9246376c713156e55c080782d4104bb07d4b899
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     theseer
%global gh_project   fXSL
%global php_home     %{_datadir}/php/TheSeer

Name:           php-theseer-fxsl
Version:        1.1.1
Release:        1%{?dist}
Summary:        An XSL wrapper / extension to the PHP XSLTProcessor

Group:          Development/Libraries
License:        BSD
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php(language) >= 5.3.3
# For test
BuildRequires:  %{_bindir}/phpunit
BuildRequires:  php-dom
BuildRequires:  php-libxml
BuildRequires:  php-xsl

# From composer.json, requires
#    "php" : ">=5.3.3",
#    "ext-libxml" : "*",
#    "ext-dom" : "*",
#    "ext-xsl" : "*"
Requires:       php(language) >= 5.3.3
Requires:       php-dom
Requires:       php-libxml
Requires:       php-xsl
# From phpcompatinfo report for version 1.1.0
Requires:       php-reflection
Requires:       php-spl

Provides:       php-composer(theseer/fxsl) = %{version}
Provides:       php-pear(pear.netpirates.net/fXSL) = %{version}


%description
The classes provided by this library extend the standard XSLTProcessor to use
exceptions at all occasions of errors instead of PHP warnings, notices or semi
completed transformations.

They also add various custom methods and shortcuts for convinience and to allow
a nicer API to implement callbacks to the PHP stack.


%prep
%setup -q -n %{gh_project}-%{gh_commit}


%build
# Empty build section, most likely nothing required.


%install
rm -rf     %{buildroot}
mkdir -p   %{buildroot}%{php_home}
cp -pr src %{buildroot}%{php_home}/%{gh_project}


%check
phpunit


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc readme.markdown composer.json sample
%{php_home}/%{gh_project}


%changelog
* Fri Nov 28 2014 Remi Collet <remi@fedoraproject.org> - 1.1.1-1
- update to 1.1.1 (no change)
- add upstream LICENSE file

* Thu Nov 27 2014 Remi Collet <remi@fedoraproject.org> - 1.1.0-1
- Initial packaging, version 1.1.0
- open https://github.com/theseer/fXSL/issues/5 - License