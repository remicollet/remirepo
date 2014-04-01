# spec file for php-phpunit-environment
#
# Copyright (c) 2014 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/3.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    79517609ec01139cd7e9fded0dd7ce08c952ef6a
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     sebastianbergmann
%global gh_project   environment
%global php_home     %{_datadir}/php/SebastianBergmann
%global with_tests   %{?_without_tests:0}%{!?_without_tests:1}

Name:           php-phpunit-environment
Version:        1.0.0
Release:        1%{?dist}
Summary:        Handle HHVM/PHP environments

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

Requires:       php(language) >= 5.3.3


%description
This component provides functionality that helps writing PHP code that
has runtime-specific (PHP / HHVM) execution paths.


%prep
%setup -q -n %{gh_project}-%{gh_commit}

: Create trivial PSR0 autoloader
cat <<EOF | tee psr0.php
<?php
spl_autoload_register(function (\$class) {
    \$crt = 'SebastianBergmann\\\\Environment\\\\';
    if (strpos(\$class, \$crt) === 0) {
        \$file = 'src/'.substr(\$class, strlen(\$crt)).'.php';
    } else {
        \$file = \$class.'.php';
    }
    \$file = str_replace('\\\\', '/', \$file);
    include \$file;
});
EOF


%build
# Empty build section, most likely nothing required.


%install
rm -rf     %{buildroot}
mkdir -p   %{buildroot}%{php_home}
cp -pr src %{buildroot}%{php_home}/Environment


%if %{with_tests}
%check
phpunit --bootstrap psr0.php
%endif


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc LICENSE README.md composer.json
%dir %{php_home}
%{php_home}/Environment


%changelog
* Tue Apr  1 2014 Remi Collet <remi@fedoraproject.org> - 1.0.0-1
- initial package