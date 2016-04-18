# remirepo/fedora spec file for php-seld-cli-prompt
#
# Copyright (c) 2015-2016 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    8cbe10923cae5bcd7c5a713f6703fc4727c8c1b4
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     Seldaek
%global gh_project   cli-prompt

Name:           php-seld-cli-prompt
Version:        1.0.2
Release:        1%{?dist}
Summary:        Allows you to prompt for user input on the command line

Group:          Development/Libraries
License:        MIT
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}-%{gh_short}.tar.gz

# Autoloader
Source1:        %{gh_project}-autoload.php

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php(language) >= 5.3
# For test
BuildRequires:  php-cli
# Autoloader
BuildRequires:  php-composer(symfony/class-loader)

# From composer.json
#       "php": ">=5.3.0",
Requires:       php(language) >= 5.3.0
# From phpcompatifo report for 1.0.0
Requires:       php-pcre
Requires:       php-spl
# Autoloader
Requires:       php-composer(symfony/class-loader)

Provides:       php-composer(seld/cli-prompt) = %{version}


%description
While prompting for user input using fgets() is quite easy, sometimes you
need to prompt for sensitive information. In these cases, the characters typed
in by the user should not be directly visible, and this is quite a pain to do
in a cross-platform way.

To use this library, you just have to add, in your project:
  require_once '%{_datadir}/php/Seld/CliPrompt/autoload.php';


%prep
%setup -q -n %{gh_project}-%{gh_commit}

cp %{SOURCE1} src/autoload.php


%build
# Nothing


%install
rm -rf       %{buildroot}
# Restore PSR-0 tree
mkdir -p     %{buildroot}%{_datadir}/php/Seld/CliPrompt
cp -pr src/* %{buildroot}%{_datadir}/php/Seld/CliPrompt/


%check
: Check if our autoloader works
php -r '
require "%{buildroot}%{_datadir}/php/Seld/CliPrompt/autoload.php";
$a = new \Seld\CliPrompt\CliPrompt();
echo "Ok\n";
exit(0);
'


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc README.md composer.json res/example.php
%{_datadir}/php/Seld


%changelog
* Mon Apr 18 2016 Remi Collet <remi@fedoraproject.org> - 1.0.2-1
- update to 1.0.2

* Sun Jan 10 2016 Remi Collet <remi@fedoraproject.org> - 1.0.1-1
- update to 1.0.1

* Wed Oct 14 2015 Remi Collet <remi@fedoraproject.org> - 1.0.0-3
- add autoloader

* Mon May  4 2015 Remi Collet <remi@fedoraproject.org> - 1.0.0-1
- initial package
