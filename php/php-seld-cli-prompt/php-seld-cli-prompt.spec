# spec file for php-seld-cli-prompt
#
# Copyright (c) 2015 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    fe114c7a6ac5cb0ce76932ae4017024d9842a49c
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     Seldaek
%global gh_project   cli-prompt

Name:           php-seld-cli-prompt
Version:        1.0.0
Release:        1%{?dist}
Summary:        Allows you to prompt for user input on the command line

Group:          Development/Libraries
License:        MIT
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}-%{gh_short}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php(language) >= 5.3

# From composer.json
#       "php": ">=5.3.0",
Requires:       php(language) >= 5.3.0
# From phpcompatifo report for 1.0.0
Requires:       php-pcre
Requires:       php-spl

Provides:       php-composer(seld/cli-prompt) = %{version}


%description
While prompting for user input using fgets() is quite easy, sometimes you
need to prompt for sensitive information. In these cases, the characters typed
in by the user should not be directly visible, and this is quite a pain to do
in a cross-platform way.


%prep
%setup -q -n %{gh_project}-%{gh_commit}


%build
# Nothing


%install
rm -rf       %{buildroot}
# Restore PSR-0 tree
mkdir -p     %{buildroot}%{_datadir}/php/Seld/CliPrompt
cp -pr src/* %{buildroot}%{_datadir}/php/Seld/CliPrompt/


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc README.md composer.json res/example.php
%{_datadir}/php/Seld


%changelog
* Mon May  4 2015 Remi Collet <remi@fedoraproject.org> - 1.0.0-1
- initial package