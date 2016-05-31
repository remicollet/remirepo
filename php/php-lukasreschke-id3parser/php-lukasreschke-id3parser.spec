# remirepo/fedora spec file for php-lukasreschke-id3parser
#
# Copyright (c) 2016 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    cd3ba6e8918cc30883f01a3c24281cfe23b8877a
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     LukasReschke
%global gh_project   ID3Parser
%global pk_owner     lukasreschke
%global pk_project   id3parser

Name:           php-%{pk_owner}-%{pk_project}
Version:        0.0.1
Release:        1%{?dist}
Summary:        ID3 parser library

Group:          Development/Libraries
# https://github.com/LukasReschke/ID3Parser/issues/1
License:        GPL+
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}-%{gh_short}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires:  php(language) >= 5.4
BuildRequires:  %{_bindir}/phpab
BuildRequires:  %{_bindir}/php

# From composer.json, "require": {
#        "php": ">=5.4"
Requires:       php(language) >= 5.4
# From phpcompatifo report for 0.0.1
Requires:       php-date
Requires:       php-iconv
Requires:       php-pcre
Requires:       php-xml
Requires:       php-zlib

Provides:       php-composer(%{pk_owner}/%{pk_project}) = %{version}


%description
This is a pure ID3 parser based upon getID3.
It supports the following ID3 versions inside MP3 files:

* ID3v1 (v1.0 & v1.1)
* ID3v2 (v2.2, v2.3 & v2.4)

Autoloader: %{_datadir}/php/%{gh_project}/autoload.php


%prep
%setup -q -n %{gh_project}-%{gh_commit}


%build
: Generate autoloader
%{_bindir}/phpab --output src/autoload.php src


%install
rm -rf     %{buildroot}
mkdir -p   %{buildroot}%{_datadir}/php
cp -pr src %{buildroot}%{_datadir}/php/%{gh_project}


%check
: Check our autoloader
%{_bindir}/php -r '
  require "%{buildroot}%{_datadir}/php/%{gh_project}/autoload.php";
  $analyzer = new \ID3Parser\ID3Parser();
'


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%doc README.md composer.json
%{_datadir}/php/%{gh_project}


%changelog
* Tue May 31 2016 Remi Collet <remi@fedoraproject.org> - 0.0.1-1
- initial package

