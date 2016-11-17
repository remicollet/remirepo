# remirepo/fedora spec file for php-phpunit-comparator
#
# Copyright (c) 2014-2016 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global bootstrap    0
%global gh_commit    ce2bda23a56456f19e35d98241446b581f648c14
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     sebastianbergmann
%global gh_project   comparator
%global php_home     %{_datadir}/php
%global ns_vendor    SebastianBergmann
%global ns_project   Comparator
%if %{bootstrap}
%global with_tests   %{?_with_tests:1}%{!?_with_tests:0}
%else
%global with_tests   %{?_without_tests:0}%{!?_without_tests:1}
%endif

Name:           php-phpunit-comparator
Version:        1.2.1
Release:        1%{?dist}
Summary:        Compare PHP values for equality

Group:          Development/Libraries
License:        BSD
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}-%{gh_short}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php(language) >= 5.3.3
BuildRequires:  php-fedora-autoloader-devel
%if %{with_tests}
# from composer.json, "require-dev": {
#        "phpunit/phpunit": "~4.4"
BuildRequires:  php-composer(phpunit/phpunit) >= 4.4
%endif

# from composer.json
#        "php": ">=5.3.3",
#        "sebastian/diff": "~1.2",
#        "sebastian/exporter": "~1.2"
Requires:       php(language) >= 5.3.3
Requires:       php-composer(sebastian/diff)  >= 1.2
Requires:       php-composer(sebastian/diff)  <  2
Requires:       php-composer(sebastian/exporter) >= 1.2
Requires:       php-composer(sebastian/exporter) <  2
# from phpcompatinfo report for version 1.0.0
Requires:       php-date
Requires:       php-dom
Requires:       php-spl
# Autoloader
Requires:       php-composer(fedora/autoloader)

Provides:       php-composer(sebastian/comparator) = %{version}


%description
This component provides the functionality to compare PHP values for equality.

Autoloader: %{php_home}/%{ns_vendor}/%{ns_project}/autoload.php


%prep
%setup -q -n %{gh_project}-%{gh_commit}


%build
# Generate the Autoloader
phpab --template fedora --output src/autoload.php src

# Rely on include_path as in PHPUnit dependencies
cat <<EOF | tee -a src/autoload.php

// Dependencies' autoloaders
require_once '%{ns_vendor}/Diff/autoload.php';
require_once '%{ns_vendor}/Exporter/autoload.php';
EOF


%install
rm -rf     %{buildroot}
mkdir -p   %{buildroot}%{php_home}/%{ns_vendor}
cp -pr src %{buildroot}%{php_home}/%{ns_vendor}/%{ns_project}


%check
%if %{with_tests}
sed -e '/vendor/d' -i tests/bootstrap.php
sed -e '/log/d' phpunit.xml.dist >phpunit.xml

# remirepo:13
run=0
ret=0
if which php56; then
  php56 -d include_path=.:%{buildroot}%{php_home}:%{php_home} \
  %{_bindir}/phpunit || ret=1
   run=1
fi
if which php71; then
  php71 -d include_path=.:%{buildroot}%{php_home}:%{php_home} \
  %{_bindir}/phpunit || ret=1
   run=1
fi
if [ $run -eq 0 ]; then
%{_bindir}/php -d include_path=.:%{buildroot}%{php_home}:%{php_home} \
%{_bindir}/phpunit --verbose
# remirepo:2
fi
exit $ret
%else
: bootstrap build with test suite disabled
%endif


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc README.md composer.json
%{!?_licensedir:%global license %%doc}
%license LICENSE

%{php_home}/%{ns_vendor}/%{ns_project}


%changelog
* Thu Nov 17 2016 Remi Collet <remi@fedoraproject.org> - 1.2.1-1
- update to 1.2.1
- switch to fedora/autoloader

* Sun Jul 26 2015 Remi Collet <remi@fedoraproject.org> - 1.2.0-1
- update to 1.2.0

* Mon Jun 29 2015 Remi Collet <remi@fedoraproject.org> - 1.1.1-3
- manage dependencies in autoloader

* Fri Jan 30 2015 Remi Collet <remi@fedoraproject.org> - 1.1.1-1
- update to 1.1.1
- raise dependency on sebastian/diff >= 1.2
- raise dependency on sebastian/exporter >= 1.2

* Thu Dec  4 2014 Remi Collet <remi@fedoraproject.org> - 1.1.0-1
- update to 1.1.0

* Sun Oct  5 2014 Remi Collet <remi@fedoraproject.org> - 1.0.1-1
- update to 1.0.1
- enable test suite

* Fri Jul 18 2014 Remi Collet <remi@fedoraproject.org> - 1.0.0-2
- add composer dependencies

* Sat May  3 2014 Remi Collet <remi@fedoraproject.org> - 1.0.0-1
- initial package
