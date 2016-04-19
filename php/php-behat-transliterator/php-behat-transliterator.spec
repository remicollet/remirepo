# remirepo/fedora spec file for php-behat-transliterator
#
# Copyright (c) 2016 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    868e05be3a9f25ba6424c2dd4849567f50715003
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     Behat
%global gh_project   Transliterator
%global pk_owner     behat
%global pk_project   transliterator

Name:           php-%{pk_owner}-%{pk_project}
Version:        1.1.0
Release:        1%{?dist}
Summary:        String transliterator

Group:          Development/Libraries
License:        MIT
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{name}-%{version}-%{gh_short}.tar.gz

# Autoloader
Source1:        %{name}-autoload.php

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php(language) >= 5.3.3
BuildRequires:  php-mbstring
BuildRequires:  php-pcre
# For test
BuildRequires:  php-composer(phpunit/phpunit)
# Autoloader
BuildRequires:  php-composer(symfony/class-loader)

# From composer.json
#        "php": ">=5.3.3"
Requires:       php(language) >= 5.3.3
# From phpcompatifo report for 1.1.0
Requires:       php-mbstring
Requires:       php-pcre
# Autoloader
Requires:       php-composer(symfony/class-loader)

Provides:       php-composer(%{pk_owner}/%{pk_project}) = %{version}


%description
Behat Transliterator provides transliteration utilities for PHP.

Transliteration data are ported from the Perl Text-Unidecode module.

Autoloader: %{_datadir}/php/Behat/Transliterator/autoload.php


%prep
%setup -q -n %{gh_project}-%{gh_commit}

cp %{SOURCE1} src//Behat/Transliterator/autoload.php


%build
# Nothing


%install
rm -rf           %{buildroot}

mkdir -p         %{buildroot}%{_datadir}/php
cp -pr src/Behat %{buildroot}%{_datadir}/php/Behat


%check
%{_bindir}/phpunit \
    --bootstrap %{buildroot}%{_datadir}/php/Behat/Transliterator/autoload.php \
    --verbose

if which php70; then
  php70 %{_bindir}/phpunit \
    --bootstrap %{buildroot}%{_datadir}/php/Behat/Transliterator/autoload.php \
    --verbose
fi

%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc *.md
%doc composer.json
%dir %{_datadir}/php/Behat
     %{_datadir}/php/Behat/Transliterator


%changelog
* Tue Apr 19 2016 Remi Collet <remi@fedoraproject.org> - 1.1.0-1
- initial package, version 1.1.0

