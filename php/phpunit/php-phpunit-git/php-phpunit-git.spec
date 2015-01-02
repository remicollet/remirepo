# spec file for php-phpunit-git
#
# Copyright (c) 2013-2015 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/3.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    a99fbc102e982c1404041ef3e4d431562b29bcba
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     sebastianbergmann
%global gh_project   git
%global php_home     %{_datadir}/php/SebastianBergmann
%global pear_name    Git
%global pear_channel pear.phpunit.de
%global with_tests   %{?_without_tests:1}%{!?_without_tests:0}

Name:           php-phpunit-git
Version:        1.2.0
Release:        7%{?dist}
Summary:        Simple wrapper for Git

Group:          Development/Libraries
License:        BSD
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php(language) >= 5.3.3

Requires:       git
# From composer.json
#      "php": ">=5.3.3"
Requires:       php(language) >= 5.3.3
# From phpcompatinfo report for 1.2.0
Requires:       php-spl

Provides:       php-composer(sebastian/git) = %{version}

# For compatibility with pear mode
Provides:       php-pear(%{pear_channel}/%{pear_name}) = %{version}
# Package have be renamed
Obsoletes:      php-phpunit-Git < 1.2.0-3
Provides:       php-phpunit-Git = %{version}-%{release}


%description
Simple PHP wrapper for Git.


%prep
%setup -q -n %{gh_project}-%{gh_commit}


%build
# If upstream drop autoload
#phpab \
#  --output src/autoload.php \
#  src


%install
rm -rf     %{buildroot}
mkdir -p   %{buildroot}%{php_home}
cp -pr src %{buildroot}%{php_home}/%{pear_name}


%clean
rm -rf %{buildroot}


%post
if [ -x %{_bindir}/pear ]; then
   %{_bindir}/pear uninstall --nodeps --ignore-errors --register-only \
      %{pear_channel}/%{pear_name} >/dev/null || :
fi


%files
%defattr(-,root,root,-)
%doc LICENSE
%doc README.md
%dir %{php_home}
     %{php_home}/%{pear_name}


%changelog
* Wed Jun 25 2014 Remi Collet <remi@fedoraproject.org> - 1.2.0-7
- composer dependencies

* Wed Apr 30 2014 Remi Collet <remi@fedoraproject.org> - 1.2.0-5
- sources from github
- cleanup pear registry

* Sun Oct 20 2013 Remi Collet <remi@fedoraproject.org> - 1.2.0-4
- properly obsoletes old name

* Sun Oct 20 2013 Remi Collet <remi@fedoraproject.org> - 1.2.0-3
- rename to lowercase

* Tue Oct  1 2013 Remi Collet <remi@fedoraproject.org> - 1.2.0-2
- own /usr/share/pear/SebastianBergmann/Git

* Wed Aug 28 2013 Remi Collet <remi@fedoraproject.org> - 1.2.0-1
- initial package
