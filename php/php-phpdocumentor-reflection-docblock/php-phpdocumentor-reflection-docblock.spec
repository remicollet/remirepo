# spec file for php-phpdocumentor-reflection-docblock
#
# Copyright (c) 2014-2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    d68dbdc53dc358a816f00b300704702b2eaff7b8
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     phpDocumentor
%global gh_project   ReflectionDocBlock
%global with_tests   %{?_without_tests:0}%{!?_without_tests:1}

Name:           php-phpdocumentor-reflection-docblock
Version:        2.0.4
Release:        1%{?dist}
Summary:        DocBlock parser

Group:          Development/Libraries
License:        MIT
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php(language) >= 5.3.3
BuildRequires:  php-phpunit-PHPUnit
BuildRequires:  php-theseer-autoload

# From composer.json, require
#        "php": ">=5.3.3"
# From composer.json, suggest
#        "dflydev/markdown": "1.0.*",
#        "erusev/parsedown": "~0.7"
Requires:       php(language) >= 5.3.3
# From phpcompatinfo report for 2.0.3
Requires:       php-pcre
Requires:       php-spl

Provides:       php-composer(phpdocumentor/reflection-docblock) = %{version}


%description
The ReflectionDocBlock component of phpDocumentor provides a DocBlock
parser that is fully compatible with the PHPDoc standard.

With this component, a library can provide support for annotations via
DocBlocks or otherwise retrieve information that is embedded in a DocBlock.


%prep
%setup -q -n %{gh_project}-%{gh_commit}


%build
phpab \
  --basedir src/phpDocumentor/Reflection/DocBlock \
  --output  src/phpDocumentor/Reflection/DocBlock/autoload.php \
  src/phpDocumentor/Reflection


%install
rm -rf       %{buildroot}
mkdir -p     %{buildroot}%{_datadir}/php
cp -pr src/* %{buildroot}%{_datadir}/php


%check
%if %{with_tests}
phpunit --bootstrap %{buildroot}%{_datadir}/php/phpDocumentor/Reflection/DocBlock/autoload.php
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
%{_datadir}/php/phpDocumentor


%changelog
* Wed Feb 11 2015 Remi Collet <remi@fedoraproject.org> - 2.0.4-1
- update to 2.0.4
- LICENSE is in upstream archive

* Tue Feb  3 2015 Remi Collet <remi@fedoraproject.org> - 2.0.3-2
- add LICENSE from upstream repository

* Fri Dec 19 2014 Remi Collet <remi@fedoraproject.org> - 2.0.3-1
- initial package
- open https://github.com/phpDocumentor/ReflectionDocBlock/issues/40
  for missing LICENSE file
