# remirepo spec file for php-deepend-Mockery, from
#
# Fedora spec file for php-deepend-Mockery
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#
%global gh_commit    4de7969f4664da3cef1ccd83866c9f59378c3371
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     padraic
%global gh_project   mockery
%global with_tests   0%{!?_without_tests:1}

Name:           php-deepend-Mockery
Version:        0.9.7
Release:        1%{?dist}
Summary:        Mockery is a simple but flexible PHP mock object framework

Group:          Development/Libraries
License:        BSD
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}-%{gh_short}.tar.gz

# Autoloader
Source1:        %{gh_project}-autoload.php

# Use our autoloader
Patch0:         %{gh_project}-tests.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
%if %{with_tests}
# From composer.json, "require-dev": {
#        "phpunit/phpunit": "~4.0"
BuildRequires:  php-composer(phpunit/phpunit) >= 4.0
BuildRequires:  php(language) >= 5.3.2
BuildRequires:  php-composer(hamcrest/hamcrest-php) >= 1.1
# Autoloader
BuildRequires:  php-composer(fedora/autoloader)
%endif

# From composer.json, "require": {
#        "php": ">=5.3.2",
#        "lib-pcre": ">=7.0",
#        "hamcrest/hamcrest-php": "~1.1"
Requires:       php(language) >= 5.3.2
Requires:       php-composer(hamcrest/hamcrest-php) >= 1.1
Requires:       php-composer(hamcrest/hamcrest-php) <  2
# From phpcompatinfo report for version 0.9.7
Requires:       php-pcre
Requires:       php-spl
Requires:       php-reflection
# Autoloader
Requires:       php-composer(fedora/autoloader)

Provides:       php-composer(mockery/mockery) = %{version}
Provides:       php-pear(pear.survivethedeepend.com/Mockery) = %{version}
Obsoletes:      php-channel-deepend <= 1.3


%description
Mockery is a simple but flexible PHP mock object framework for use in unit 
testing. It is inspired by Ruby's flexmock and Java's Mockito, borrowing 
elements from both of their APIs.

To use this library, you just have to add, in your project:
  require_once '%{_datadir}/php/Mockery/autoload.php';


%prep
%setup -q -n %{gh_project}-%{gh_commit}

cp %{SOURCE1} library/Mockery/autoload.php
%patch0 -p0 -b .rpm


%build
# Empty build section, most likely nothing required.


%install
rm -rf %{buildroot}

mkdir -p %{buildroot}/%{_datadir}/php
cp -rp library/* %{buildroot}/%{_datadir}/php/


%clean
rm -rf %{buildroot}


%check
%if %{with_tests}
: Use installed tree and our autoloader
sed -e 's:@BUILD@:%{buildroot}/%{_datadir}/php:' -i tests/Bootstrap.php

: Run upstream test suite
# remirepo:11
run=0
ret=0
if which php56; then
   php56 %{_bindir}/phpunit || ret=1
   run=1
fi
if which php71; then
   php71 %{_bindir}/phpunit || ret=1
   run=1
fi
if [ $run -eq 0 ]; then
%{_bindir}/phpunit --verbose
# remirepo:2
fi
exit $ret
%endif


%post
if [ -x %{_bindir}/pear ]; then
  %{_bindir}/pear uninstall --nodeps --ignore-errors --register-only \
    pear.survivethedeepend.com/Mockery >/dev/null || :
fi


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc README.md docs
%doc composer.json
%{_datadir}/php/Mockery/
%{_datadir}/php/Mockery.php


%changelog
* Fri Dec 23 2016 Remi Collet <remi@fedoraproject.org> - 0.9.7-1
- Update to 0.9.7

* Sat Nov 26 2016 Remi Collet <remi@fedoraproject.org> - 0.9.6-1
- Update to 0.9.6
- switch to fedora/autoloader

* Tue Jun 14 2016 Remi Collet <remi@fedoraproject.org> - 0.9.5-1
- Update to 0.9.5

* Fri Oct 16 2015 Remi Collet <remi@fedoraproject.org> - 0.9.3-1
- downgrade to 0.9.3

* Fri Oct 16 2015 Remi Collet <remi@fedoraproject.org> - 0.9.4-1
- Update to 0.9.4
- add autoloader using symfony/class-loader
- add dependency on hamcrest/hamcrest-php
- run test suite
- use github archive from commit reference

* Wed Jul 16 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.9.1-2
- fixed requires (Remi)
- add script which will delete older pear package if installed (Remi)
- fix provides/obsoletes (Remi)

* Tue Jul 15 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.9.1-1
- update to 0.9.1 (RHBZ #1119451)

* Tue Feb 11 2014 Remi Collet <remi@fedoraproject.org> - 0.9.0-1
- Update to 0.9.0

* Fri Apr 19 2013 Remi Collet <remi@fedoraproject.org> - 0.8.0-1
- Update to 0.8.0 (backport)

* Thu Apr 18 2013 Christof Damian <christof@damian.net> - 0.8.0-1
- upstream 0.8.0

* Sun Mar 04 2012 Remi Collet <RPMS@FamilleCollet.com> - 0.7.2-1
- upstream 0.7.2, rebuild for remi repository

* Sun Mar  4 2012 Christof Damian <christof@damian.net> - 0.7.2-1
- upstream 0.7.2

* Tue Jul 27 2010 Remi Collet <RPMS@FamilleCollet.com> - 0.6.3-2
- rebuild for remi repository

* Tue Jul 27 2010 Christof Damian <christof@damian.net> - 0.6.3-2
- add license and readme file from github

* Fri May 28 2010 Christof Damian <christof@damian.net> - 0.6.0-1
- initial packaging


