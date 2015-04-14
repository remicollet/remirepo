# spec file for php-phpunit-PHP-Invoker
#
# Copyright (c) 2011-2015 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    8696484458cb43eed025ab46260846de5b74655c
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     sebastianbergmann
%global gh_project   php-invoker
%global php_home     %{_datadir}/php
%global pear_name    PHP_Invoker
%global pear_channel pear.phpunit.de
# Circular dependency with phpunit
%global with_tests   %{?_with_tests:1}%{!?_with_tests:0}

Name:           php-phpunit-PHP-Invoker
Version:        1.1.3
Release:        6%{?dist}
Summary:        Utility class for invoking callables with a timeout

Group:          Development/Libraries
License:        BSD
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php(language) >= 5.2.7
%if %{with_tests}
BuildRequires:  %{_bindir}/phpunit
%endif

# From composer.json
#        "php": ">=5.2.7",
#        "phpunit/php-timer": ">=1.0.4",
#        "ext-pcntl": "*"
Requires:       php(language) >= 5.2.7
Requires:       php-composer(phpunit/php-timer) >= 1.0.4
Requires:       php-pcntl
# From phpcompatinfo report for version 1.0.5
Requires:       php-spl

Provides:       php-composer(phpunit/php-invoker) = %{version}

# For compatibility with PEAR mode
Provides:       php-pear(%{pear_channel}/%{pear_name}) = %{version}


%description
Utility class for invoking callables with a timeout.


%prep
%setup -q -n %{gh_project}-%{gh_commit}

rm PHP/Invoker/Autoload.php.in


%build
# Empty build section, most likely nothing required.

# If upstream drop Autoload.php, command to generate it
# phpab \
#   --output PHP/Invoker/Autoload.php \
#   --template PHP/Invoker/Autoload.php.in \
#   PHP


%install
rm -rf     %{buildroot}
mkdir -p   %{buildroot}%{php_home}
cp -pr PHP %{buildroot}%{php_home}


%if %{with_tests}
%check
phpunit \
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
%doc README.markdown ChangeLog.markdown composer.json
%{!?_licensedir:%global license %%doc}
%license LICENSE

%{php_home}/*


%changelog
* Fri Jul 18 2014 Remi Collet <remi@fedoraproject.org> - 1.1.3-6
- add composer dependencies

* Wed Apr 30 2014 Remi Collet <remi@fedoraproject.org> - 1.1.3-4
- cleanup pear registry

* Wed Apr 23 2014 Remi Collet <remi@fedoraproject.org> - 1.1.3-3
- get sources from github
- run test suite when build --with tests

* Tue Jul 16 2013 Remi Collet <remi@fedoraproject.org> - 1.1.3-1
- Update to 1.1.3 (stable) - API 1.1.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Oct  6 2012 Remi Collet <remi@fedoraproject.org> - 1.1.2-1
- Update to 1.1.2 (stable) - API 1.1.0

* Mon Sep 24 2012 Remi Collet <remi@fedoraproject.org> - 1.1.1-1
- Update to 1.1.1 (stable) - API 1.1.0

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jan 24 2012 Remi Collet <remi@fedoraproject.org> - 1.1.0-1
- Update to 1.1.0 (stable) - API 1.1.0
- now requires PHP_Timer

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Nov 26 2011 Remi Collet <remi@fedoraproject.org> - 1.0.1-1
- Update to 1.0.1 (stable) - API 1.0.0

* Tue Nov 01 2011 Remi Collet <remi@fedoraproject.org> - 1.0.0-3
- fix provides

* Tue Nov 01 2011 Remi Collet <remi@fedoraproject.org> - 1.0.0-2
- new tarball, with documentation

* Tue Nov 01 2011 Remi Collet <remi@fedoraproject.org> - 1.0.0-1
- initial generated RPM by pear make-rpm-spec + cleanups
