# spec file for php-phpunit-diff
#
# Copyright (c) 2013-2014 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/3.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    1e091702a5a38e6b4c1ba9ca816e3dd343df2e2d
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     sebastianbergmann
%global gh_project   diff
%global php_home     %{_datadir}/php/SebastianBergmann
%global pear_name    Diff
%global pear_channel pear.phpunit.de
# Circular dependency with phpunit
%global with_tests   %{?_with_tests:1}%{!?_with_tests:0}

Name:           php-phpunit-diff
Version:        1.1.0
Release:        4%{?dist}.1
Summary:        Diff implementation

Group:          Development/Libraries
License:        BSD
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php(language) >= 5.3.3
%if %{with_tests}
BuildRequires:  %{_bindir}/phpunit
%endif

# from composer.json
Requires:       php(language) >= 5.3.3
# from phpcompatinfo report for version 1.1.0
Requires:       php-pcre
Requires:       php-spl

Provides:       php-pear(%{pear_channel}/%{pear_name}) = %{version}
# Package have be renamed
Obsoletes:      php-phpunit-Diff < 1.1.0-2
Provides:       php-phpunit-Diff = %{version}-%{release}

%description
Diff implementation.


%prep
%setup -q -n %{gh_project}-%{gh_commit}


%build
# Empty build section, most likely nothing required.


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
%doc LICENSE README.md composer.json

%dir %{php_home}
%{php_home}/%{pear_name}



%changelog
* Wed Apr 30 2014 Remi Collet <remi@fedoraproject.org> - 1.1.0-4
- cleanup pear registry

* Wed Apr 23 2014 Remi Collet <remi@fedoraproject.org> - 1.1.0-3
- get sources from github
- run test suite when build --with tests

* Sun Oct 20 2013 Remi Collet <remi@fedoraproject.org> - 1.1.0-2
- rename to lowercase

* Thu Sep 12 2013 Remi Collet <remi@fedoraproject.org> - 1.1.0-1
- initial package
