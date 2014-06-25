# spec file for php-phpunit-FinderFacade
#
# Copyright (c) 2012-2014 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/3.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    1e396fda3449fce9df032749fa4fa2619e0347e0
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     sebastianbergmann
%global gh_project   finder-facade
%global php_home     %{_datadir}/php
%global pear_name    FinderFacade
%global pear_channel pear.phpunit.de
%global with_tests   %{?_without_tests:0}%{!?_without_tests:1}

Name:           php-phpunit-FinderFacade
Version:        1.1.0
Release:        6%{?dist}
Summary:        Wrapper for Symfony Finder component

Group:          Development/Libraries
License:        BSD
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php(language) >= 5.3.3
%if %{with_tests}
BuildRequires:  php-pear-PHPUnit >= 3.7.0
BuildRequires:  php-theseer-fDOMDocument >= 1.3.1
BuildRequires:  php-symfony-finder >= 2.2.0
%endif

# From composer.json
#      "theseer/fdomdocument": ">=1.3.1",
#      "symfony/finder": ">=2.2.0"
Requires:       php(language) >= 5.3.3
Requires:       php-theseer-fDOMDocument >= 1.3.1
Requires:       php-symfony-finder >= 2.2.0
# From phpcompatinfo report
Requires:       php-ctype
Requires:       php-spl

Provides:       php-composer(sebastian/finder-facade) = %{version}

# For compatibility with PEAR mode
Provides:       php-pear(%{pear_channel}/%{pear_name}) = %{version}


%description
Convenience wrapper for Symfony's Finder component.


%prep
%setup -q -n %{gh_project}-%{gh_commit}

rm src/autoload.php.in


%build
# Empty build section, most likely nothing required.

# If upstream drop Autoload.php, command to generate it.
#phpab \
#  --output   src/autoload.php \
#  --template src/autoload.php.in \
#  src


%install
rm -rf     %{buildroot}
mkdir -p   %{buildroot}%{php_home}/SebastianBergmann
cp -pr src %{buildroot}%{php_home}/SebastianBergmann/FinderFacade


%if %{with_tests}
%check
phpunit \
  -d date.timezone=UTC \
  --bootstrap src/autoload.php \
  tests
%endif


%clean
rm -rf %{buildroot}


%post
if [ -x %{_bindir}/pear ]; then
   %{_bindir}/pear uninstall --nodeps --ignore-errors --register-only \
      %{pear_channel}/%{pear_name} >/dev/null || :
fi


%files
%defattr(-,root,root,-)
%doc ChangeLog.md README.md LICENSE composer.json
%dir %{php_home}/SebastianBergmann
     %{php_home}/SebastianBergmann/FinderFacade


%changelog
* Wed Jun 25 2014 Remi Collet <remi@fedoraproject.org> - 1.1.0-6
- composer dependencies

* Wed Apr 30 2014 Remi Collet <remi@fedoraproject.org> - 1.1.0-4
- cleanup pear registry

* Tue Apr 29 2014 Remi Collet <remi@fedoraproject.org> - 1.1.0-3
- sources from github
- run tests during build

* Thu May 30 2013 Remi Collet <remi@fedoraproject.org> - 1.1.0-1
- Update to 1.1.0

* Mon May 27 2013 Remi Collet <remi@fedoraproject.org> - 1.0.7-1
- Update to 1.0.7 (no change)

* Wed Mar  6 2013 Remi Collet <remi@fedoraproject.org> - 1.0.6-2
- upstream patch for Finder 2.2.0 compatibility

* Thu Jan 10 2013 Remi Collet <remi@fedoraproject.org> - 1.0.6-1
- Version 1.0.6 (stable) - API 1.0.1 (stable)

* Thu Oct 11 2012 Remi Collet <remi@fedoraproject.org> - 1.0.5-1
- Version 1.0.5 (stable) - API 1.0.1 (stable)
- Initial packaging
