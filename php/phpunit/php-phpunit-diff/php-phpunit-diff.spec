# spec file for php-phpunit-diff
#
# Copyright (c) 2013-2014 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/3.0/
#
# Please, preserve the changelog entries
#
%global bootstrap    0
%global gh_commit    5843509fed39dee4b356a306401e9dd1a931fec7
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     sebastianbergmann
%global gh_project   diff
%global php_home     %{_datadir}/php/SebastianBergmann
%global pear_name    Diff
%global pear_channel pear.phpunit.de
%if %{bootstrap}
%global with_tests   %{?_with_tests:1}%{!?_with_tests:0}
%else
%global with_tests   %{?_without_tests:0}%{!?_without_tests:1}
%endif

Name:           php-phpunit-diff
Version:        1.2.0
Release:        1%{?dist}
Summary:        Diff implementation

Group:          Development/Libraries
License:        BSD
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php(language) >= 5.3.3
BuildRequires:  %{_bindir}/phpab
%if %{with_tests}
BuildRequires:  php-phpunit-PHPUnit >= 4.2
%endif

# from composer.json
#      "php": ">=5.3.3"
Requires:       php(language) >= 5.3.3
# from phpcompatinfo report for version 1.1.0
Requires:       php-pcre
Requires:       php-spl

Provides:       php-composer(sebastian/diff) = %{version}

Provides:       php-pear(%{pear_channel}/%{pear_name}) = %{version}
# Package have be renamed
Obsoletes:      php-phpunit-Diff < 1.1.0-2
Provides:       php-phpunit-Diff = %{version}-%{release}


%description
Diff implementation.


%prep
%setup -q -n %{gh_project}-%{gh_commit}


%build
phpab \
  --output   src/autoload.php \
  src


%install
rm -rf     %{buildroot}
mkdir -p   %{buildroot}%{php_home}
cp -pr src %{buildroot}%{php_home}/%{pear_name}


%if %{with_tests}
%check
phpunit \
  --bootstrap src/autoload.php \
  -d date.timezone=UTC
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
%doc README.md composer.json

%dir %{php_home}
%{php_home}/%{pear_name}


%changelog
* Fri Oct  3 2014 Remi Collet <remi@fedoraproject.org> - 1.2.0-1
- update to 1.2.0
- run test suite during build
- generate autoload.php for compatibility
- fix license handling

* Wed Jun 25 2014 Remi Collet <remi@fedoraproject.org> - 1.1.0-6
- composer dependencies

* Wed Apr 30 2014 Remi Collet <remi@fedoraproject.org> - 1.1.0-4
- cleanup pear registry

* Wed Apr 23 2014 Remi Collet <remi@fedoraproject.org> - 1.1.0-3
- get sources from github
- run test suite when build --with tests

* Sun Oct 20 2013 Remi Collet <remi@fedoraproject.org> - 1.1.0-2
- rename to lowercase

* Thu Sep 12 2013 Remi Collet <remi@fedoraproject.org> - 1.1.0-1
- initial package
