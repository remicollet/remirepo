# remirepo/fedora spec file for php-phpunit-FinderFacade
#
# Copyright (c) 2012-2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    2a6f7f57efc0aa2d23297d9fd9e2a03111a8c0b9
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     sebastianbergmann
%global gh_project   finder-facade
%global php_home     %{_datadir}/php
%global pear_name    FinderFacade
%global pear_channel pear.phpunit.de
%global with_tests   %{?_without_tests:0}%{!?_without_tests:1}

Name:           php-phpunit-FinderFacade
Version:        1.2.1
Release:        1%{?dist}
Summary:        Wrapper for Symfony Finder component

Group:          Development/Libraries
License:        BSD
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}-%{gh_short}.tar.gz
# Autoloader template
Source1:        autoload.php.in

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php(language) >= 5.3.3
BuildRequires:  %{_bindir}/phpab
%if %{with_tests}
BuildRequires:  %{_bindir}/phpunit
BuildRequires:  php-composer(theseer/fdomdocument) >= 1.3
BuildRequires:  php-composer(symfony/finder) >=  2.3
BuildRequires:  php-composer(symfony/class-loader)
%endif

# From composer.json "require": {
#        "theseer/fdomdocument": "~1.3",
#        "symfony/finder": "~2.3|~3.0"
Requires:       php(language) >= 5.3.3
Requires:       php-composer(theseer/fdomdocument) >= 1.3
Requires:       php-composer(theseer/fdomdocument) <  2
Requires:       php-composer(symfony/finder) >=  2.3
Requires:       php-composer(symfony/finder) <   4
# From phpcompatinfo report for version 1.2.1
Requires:       php-ctype
# For our autoloader
Requires:       php-composer(symfony/class-loader)

Provides:       php-composer(sebastian/finder-facade) = %{version}
# For compatibility with PEAR mode
Provides:       php-pear(%{pear_channel}/%{pear_name}) = %{version}


%description
Convenience wrapper for Symfony's Finder component.


%prep
%setup -q -n %{gh_project}-%{gh_commit}


%build
phpab \
  --output   src/autoload.php \
  --template %{SOURCE1} \
  src


%install
rm -rf     %{buildroot}
mkdir -p   %{buildroot}%{php_home}/SebastianBergmann
cp -pr src %{buildroot}%{php_home}/SebastianBergmann/FinderFacade


%if %{with_tests}
%check
%{_bindir}/php \
    -d include_path=.:%{buildroot}%{php_home}:%{php_home} \
    %{_bindir}/phpunit \
        --bootstrap %{buildroot}%{php_home}/SebastianBergmann/FinderFacade/autoload.php \
        --verbose tests

if which php70; then
php70 \
    -d include_path=.:%{buildroot}%{php_home}:%{php_home} \
    %{_bindir}/phpunit \
        --bootstrap %{buildroot}%{php_home}/SebastianBergmann/FinderFacade/autoload.php \
        --verbose tests
fi
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
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc README.md
%doc composer.json
%dir %{php_home}/SebastianBergmann
     %{php_home}/SebastianBergmann/FinderFacade


%changelog
* Wed Feb 17 2016 Remi Collet <remi@fedoraproject.org> - 1.2.1-1
- update to 1.2.1
- run test suite with both PHP 5 and 7 when available

* Mon Jun 29 2015 Remi Collet <remi@fedoraproject.org> - 1.2.0-3
- switch to $fedoraClassLoader autoloader

* Thu Jun  4 2015 Remi Collet <remi@fedoraproject.org> - 1.2.0-2
- use $sfuloader

* Thu Jun  4 2015 Remi Collet <remi@fedoraproject.org> - 1.2.0-1
- upgrade to 1.2.0
- raise dependency on symfony/finder 2.3
- generate autoloader (dropped upstream)
- fix license handling

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
