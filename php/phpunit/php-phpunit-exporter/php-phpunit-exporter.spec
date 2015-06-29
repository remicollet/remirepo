# spec file for php-phpunit-exporter
#
# Copyright (c) 2013-2015 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global bootstrap    0
%global gh_commit    84839970d05254c73cde183a721c7af13aede943
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     sebastianbergmann
%global gh_project   exporter
%global php_home     %{_datadir}/php/SebastianBergmann/
%global pear_name    Exporter
%global pear_channel pear.phpunit.de
%if %{bootstrap}
%global with_tests   %{?_with_tests:1}%{!?_with_tests:0}
%else
%global with_tests   %{?_without_tests:0}%{!?_without_tests:1}
%endif

Name:           php-phpunit-exporter
Version:        1.2.0
Release:        1%{?dist}
Summary:        Export PHP variables for visualization

Group:          Development/Libraries
License:        BSD
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php(language) >= 5.3.3
BuildRequires:  %{_bindir}/phpab
%if %{with_tests}
BuildRequires:  %{_bindir}/phpunit
BuildRequires:  php-composer(sebastian/recursion-context) >= 1.0
%endif

# from composer.json
#         "php": ">=5.3.3"
#         "sebastian/recursion-context": "~1.0"
Requires:       php(language) >= 5.3.3
Requires:       php-composer(sebastian/recursion-context) >= 1.0
Requires:       php-composer(sebastian/recursion-context) <  2
# from phpcompatinfo report for version 1.0.0
Requires:       php-hash
Requires:       php-pcre
Requires:       php-spl

Provides:       php-composer(sebastian/exporter) = %{version}

# For compatibility, to drop when no more required
# Currently used by phpcpd and phploc
Provides:       php-pear(%{pear_channel}/%{pear_name}) = %{version}

# Package have be renamed
Obsoletes:      php-phpunit-Exporter < 1.0.0-2
Provides:       php-phpunit-Exporter = %{version}


%description
Provides the functionality to export PHP variables for visualization.


%prep
%setup -q -n %{gh_project}-%{gh_commit}


%build
# Generate the Autoloader (which was part of the Pear package)
phpab --output src/autoload.php src

# Rely on include_path as in PHPUnit dependencies
cat <<EOF | tee -a src/autoload.php
// Dependency' autoloader
require_once 'SebastianBergmann/RecursionContext/autoload.php';
EOF


%install
rm -rf     %{buildroot}
mkdir -p   %{buildroot}%{php_home}
cp -pr src %{buildroot}%{php_home}/Exporter


%if %{with_tests}
%check
phpunit \
  --include-path %{buildroot}%{_datadir}/php \
  --bootstrap %{buildroot}%{php_home}/Exporter/autoload.php
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
%doc README.md composer.json
%{!?_licensedir:%global license %%doc}
%license LICENSE
%{php_home}/Exporter


%changelog
* Fri Jan 30 2015 Remi Collet <remi@fedoraproject.org> - 1.2.0-1
- update to 1.2.0

* Sat Jan 24 2015 Remi Collet <remi@fedoraproject.org> - 1.1.0-1
- update to 1.1.0
- add dependency on sebastian/recursion-context

* Sun Oct  5 2014 Remi Collet <remi@fedoraproject.org> - 1.0.2-1
- update to 1.0.2
- enable test suite

* Fri Jul 18 2014 Remi Collet <remi@fedoraproject.org> - 1.0.1-4
- add composer dependencies

* Wed Apr 30 2014 Remi Collet <remi@fedoraproject.org> - 1.0.1-2
- cleanup pear registry

* Sun Apr  6 2014 Remi Collet <remi@fedoraproject.org> - 1.0.1-1
- update to 1.0.1
- get sources from github
- run test suite when build --with tests

* Sun Oct 20 2013 Remi Collet <remi@fedoraproject.org> - 1.0.0-2
- rename to lowercase

* Thu Sep 12 2013 Remi Collet <remi@fedoraproject.org> - 1.0.0-1
- initial package
