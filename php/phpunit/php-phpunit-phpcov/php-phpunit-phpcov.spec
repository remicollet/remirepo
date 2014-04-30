# spec file for php-phpunit-phpcov
#
# Copyright (c) 2013-2014 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/3.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    5e32a1355826e5e2e0e99b4e2d0762867f4a8181
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     sebastianbergmann
%global gh_project   phpcov
%global php_home     %{_datadir}/php/SebastianBergmann
%global pear_name    phpcov
%global pear_channel pear.phpunit.de
# not Ready
%global with_tests   %{?_with_tests:1}%{!?_with_tests:0}


Name:           php-phpunit-phpcov
Version:        2.0.0
Release:        1%{?dist}
Summary:        TextUI front-end for PHP_CodeCoverage

Group:          Development/Libraries
License:        BSD
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}.tar.gz

# Autoload template
Source1:        autoload.php.in

# Fix autoload for RPM
Patch0:         %{gh_project}-rpm.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php(language) >= 5.3.3
BuildRequires:  %{_bindir}/phpab
%if %{with_tests}
BuildRequires:  php-phpunit-PHPUnit >= 4.0
BuildRequires:  php-phpunit-PHP-CodeCoverage >= 2.0
BuildRequires:  php-phpunit-diff >= 1.1
BuildRequires:  php-phpunit-FinderFacade >= 1.1
BuildRequires:  php-phpunit-Version >= 1.0.3
BuildRequires:  php-symfony-console >= 2.2
%endif

# from composer.json
Requires:       php(language) >= 5.3.3
Requires:       php-phpunit-PHPUnit >= 4.0
Requires:       php-phpunit-PHP-CodeCoverage >= 2.0
Requires:       php-phpunit-diff >= 1.1
Requires:       php-phpunit-FinderFacade >= 1.1
Requires:       php-phpunit-Version >= 1.0.3
Requires:       php-symfony-console >= 2.2
# from phpcompatinfo report for version 1.1.0
Requires:       php-reflection
Requires:       php-spl

Provides:       php-pear(%{pear_channel}/%{pear_name}) = %{version}
# Project name
Provides:       phpcov = %{version}


%description
TextUI front-end for PHP_CodeCoverage.


%prep
%setup -q -n %{gh_project}-%{gh_commit}

%patch0 -p0 -b .rpm


%build
phpab \
  --output   src/autoload.php \
  --template %{SOURCE1} \
  src


%install
rm -rf     %{buildroot}
mkdir -p   %{buildroot}%{php_home}
cp -pr src %{buildroot}%{php_home}/PHPCOV

install -D -p -m 755 phpcov %{buildroot}%{_bindir}/phpcov


%if %{with_tests}
%check
phpunit \
   --bootstrap src/autoload.php \
   -d date.timezone=UTC \
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
%doc LICENSE README.md composer.json
%{php_home}/PHPCOV
%{_bindir}/phpcov


%changelog
* Wed Apr 30 2014 Remi Collet <remi@fedoraproject.org> - 2.0.0-1
- update to 2.0.0
- sources from github

* Thu Sep 12 2013 Remi Collet <remi@fedoraproject.org> - 1.1.0-1
- initial package
