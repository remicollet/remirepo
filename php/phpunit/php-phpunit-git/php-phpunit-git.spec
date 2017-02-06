# spec file for php-phpunit-git
#
# Copyright (c) 2013-2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    815bbbc963cf35e5413df195aa29df58243ecd24
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     sebastianbergmann
%global gh_project   git
%global php_home     %{_datadir}/php/SebastianBergmann
%global pear_name    Git
%global pear_channel pear.phpunit.de
%global with_tests   %{?_without_tests:1}%{!?_without_tests:0}

Name:           php-phpunit-git
Version:        2.1.4
Release:        1%{?dist}
Summary:        Simple wrapper for Git

Group:          Development/Libraries
License:        BSD
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php(language) >= 5.3.3
BuildRequires:  php-fedora-autoloader-devel

Requires:       git
# From composer.json
#      "php": ">=5.3.3"
Requires:       php(language) >= 5.3.3
# From phpcompatinfo report for 2.1.2
Requires:       php-date
Requires:       php-spl
# Autoloader
Requires:       php-composer(fedora/autoloader)

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
%{_bindir}/phpab \
  --template fedora \
  --output src/autoload.php \
  src


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
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc README.md
%doc composer.json
%dir %{php_home}
     %{php_home}/%{pear_name}


%changelog
* Mon Feb  6 2017 Remi Collet <remi@fedoraproject.org> - 2.1.4-1
- update to 2.1.4
- switch to fedora/autoloader

* Wed Jun 15 2016 Remi Collet <remi@fedoraproject.org> - 2.1.3-1
- update to 2.1.3

* Sun May 29 2016 Remi Collet <remi@fedoraproject.org> - 2.1.2-1
- update to 2.1.2

* Sun Feb 21 2016 Remi Collet <remi@fedoraproject.org> - 2.1.1-1
- update to 2.1.1

* Wed Feb 17 2016 Remi Collet <remi@fedoraproject.org> - 2.1.0-1
- update to 2.1.0

* Tue Apr  7 2015 Remi Collet <remi@fedoraproject.org> - 2.0.1-1
- update to 2.0.1

* Wed Mar 11 2015 Remi Collet <remi@fedoraproject.org> - 2.0.0-1
- update to 2.0.0
- fix license handling

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
