%global gh_commit    10246f167713d0bd0b74540ca81e4caf30b72157
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     sebastianbergmann
%global gh_project   phpdcd
%global php_home     %{_datadir}/php/SebastianBergmann
%global pear_name    phpdcd
%global pear_channel pear.phpunit.de
%global with_tests   %{?_without_tests:0}%{!?_without_tests:1}

Name:           php-phpunit-phpdcd
Version:        1.0.2
Release:        1%{?dist}
Summary:        Dead Code Detector (DCD) for PHP code

Group:          Development/Libraries
License:        BSD
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}.tar.gz

# Autoload template
Source1:        Autoload.php.in

# Fix for RPM, use autoload
Patch0:         %{gh_project}-rpm.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php(language) >= 5.3.3
BuildRequires:  %{_bindir}/phpab
%if %{with_tests}
BuildRequires:  %{_bindir}/phpunit
BuildRequires:  php-phpunit-FinderFacade >= 1.1.0
BuildRequires:  php-phpunit-Version >= 1.0.3
BuildRequires:  php-symfony-console >= 2.2.0
BuildRequires:  php-phpunit-PHP-Timer >= 1.0.4
BuildRequires:  php-phpunit-PHP-TokenStream >= 1.1.3
%endif

# From composer.json
Requires:       php(language) >= 5.3.3
Requires:       php-phpunit-FinderFacade >= 1.1.0
Requires:       php-phpunit-Version >= 1.0.3
Requires:       php-symfony-console >= 2.2.0
Requires:       php-phpunit-PHP-Timer >= 1.0.4
Requires:       php-phpunit-PHP-TokenStream >= 1.1.3
# From phpcompatinfo report for version 1.0.2
Requires:       php-pcre
Requires:       php-spl


%description
phpdcd is a Dead Code Detector (DCD) for PHP code. It scans a PHP project
for all declared functions and methods and reports those as being "dead 
code" that are not called at least once.


%prep
%setup -q -n %{gh_project}-%{gh_commit}

%patch0 -p1 -b .rpm


%build
phpab \
  --output   src/Autoload.php \
  --template %{SOURCE1} \
  src


%install
rm -rf     %{buildroot}
mkdir -p   %{buildroot}%{php_home}
cp -pr src %{buildroot}%{php_home}/PHPDCD

install -D -p -m 755 phpdcd %{buildroot}%{_bindir}/phpdcd


%if %{with_tests}
%check
phpunit \
   --bootstrap src/Autoload.php \
   -d date.timezone=UTC \
   tests
%endif


%clean
rm -rf $RPM_BUILD_ROOT


%post
if [ -x %{_bindir}/pear ]; then
   %{_bindir}/pear uninstall --nodeps --ignore-errors --register-only \
      %{pear_channel}/%{pear_name} >/dev/null || :
fi


%files
%defattr(-,root,root,-)
%doc LICENSE README.md composer.json
%{php_home}/PHPDCD
%{_bindir}/phpdcd


%changelog
* Sun May  4 2014 Remi Collet <remi@fedoraproject.org> - 1.0.2-1
- update to 1.0.2
- sources from github
- run test suite during build

* Sat Mar 31 2012 Remi Collet <RPMS@FamilleCollet.com> - 0.9.3-1
- upstream 0.9.3, rebuild for remi repository

* Sat Mar 24 2012 Christof Damian <christof@damian.net> - 0.9.3-1
- upstream 0.9.3

* Tue Feb 23 2010 Remi Collet <RPMS@FamilleCollet.com> 0.9.2-1
- rebuild for remi repository

* Thu Feb 4 2010 Christof Damian <christof@damian.net> 0.9.2-1
- initial packaging

