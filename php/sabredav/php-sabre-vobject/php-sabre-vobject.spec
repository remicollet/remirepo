# remirepo/fedora spec file for php-sabre-vobject
#
# Copyright (c) 2013-2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    129d80533a9ec0d9cacfb50b51180c34edb6874c
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     fruux
%global gh_project   sabre-vobject
%global with_tests   %{?_without_tests:0}%{!?_without_tests:1}

Name:           php-%{gh_project}
Summary:        Library to parse and manipulate iCalendar and vCard objects
Version:        3.5.3
Release:        2%{?dist}

URL:            http://sabre.io/vobject/
License:        BSD
Group:          Development/Libraries
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}-%{gh_short}.tar.gz
Source1:        %{name}-autoload.php

# replace composer autloader
Patch0:         %{gh_project}-bin.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
%if %{with_tests}
BuildRequires:  php-composer(phpunit/phpunit)
BuildRequires:  php(language) >= 5.3.1
BuildRequires:  php-mbstring
BuildRequires:  php-date
BuildRequires:  php-json
BuildRequires:  php-pcre
BuildRequires:  php-spl
BuildRequires:  php-xml
# Autoloader
BuildRequires:  php-composer(fedora/autoloader)
%endif

# From composer.json
#        "php"          : ">=5.3.1",
#        "ext-mbstring" : "*"
Requires:       php(language) >= 5.3.1
Requires:       php-mbstring
# From phpcompatinfo report for version 3.4.5
Requires:       php-cli
Requires:       php-date
Requires:       php-json
Requires:       php-pcre
Requires:       php-spl
Requires:       php-xml
# Autoloader
Requires:       php-composer(fedora/autoloader)

Provides:       php-composer(sabre/vobject) = %{version}


%description
The VObject library allows you to easily parse and manipulate iCalendar
and vCard objects using PHP. The goal of the VObject library is to create
a very complete library, with an easy to use API.

This project is a spin-off from SabreDAV, where it has been used for several
years. The VObject library has 100% unittest coverage.

Autoloader: %{_datadir}/php/Sabre/VObject/autoload.php


%prep
%setup -q -n %{gh_project}-%{gh_commit}

%patch0 -p1 -b .rpm
cp %{SOURCE1} lib/autoload.php


%build
# nothing to build


%install
# Install as a PSR-0 library
mkdir -p %{buildroot}%{_datadir}/php/Sabre
cp -pr lib %{buildroot}%{_datadir}/php/Sabre/VObject

# Install the commands
install -Dpm 0755 bin/vobject \
         %{buildroot}/%{_bindir}/vobject
install -Dpm 0755 bin/generate_vcards \
         %{buildroot}/%{_bindir}/generate_vcards


%check
%if %{with_tests}
: Fix bootstrap
cd tests
sed -e 's:@BUILDROOT@:%{buildroot}:' -i bootstrap.php

: Run upstream test suite against installed library
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
%else
: Skip upstream test suite
%endif


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc *md
%doc composer.json
%{_datadir}/php/Sabre
%{_bindir}/vobject
%{_bindir}/generate_vcards


%changelog
* Sat Oct 29 2016 Remi Collet <remi@fedoraproject.org> - 3.5.3-3
- switch from symfony/class-loader to fedora/autoloader

* Fri Oct  7 2016 Remi Collet <remi@fedoraproject.org> - 3.5.3-1
- update to 3.5.3

* Tue Apr 26 2016 Remi Collet <remi@fedoraproject.org> - 3.5.2-1
- update to 3.5.2

* Thu Apr  7 2016 Remi Collet <remi@fedoraproject.org> - 3.5.1-1
- update to 3.5.1

* Fri Mar 11 2016 Remi Collet <remi@fedoraproject.org> - 3.5.0-1
- update to 3.5.0

* Wed Feb 24 2016 Remi Collet <remi@fedoraproject.org> - 3.4.6-1
- update to 3.4.6

* Wed Jul 16 2014 Remi Collet <remi@fedoraproject.org> - 3.2.4-1
- update to 3.2.4

* Wed Jun 18 2014 Remi Collet <remi@fedoraproject.org> - 3.2.3-1
- update to 3.2.3
- add provides php-composer(sabre/vobject)
- url is now http://sabre.io/vobject/

* Fri May  9 2014 Remi Collet <remi@fedoraproject.org> - 3.2.2-1
- update to 3.2.2

* Tue May  6 2014 Remi Collet <remi@fedoraproject.org> - 3.2.1-1
- update to 3.2.1

* Sun Apr  6 2014 Remi Collet <remi@fedoraproject.org> - 3.2.0-1
- update to 3.2.0

* Thu Feb 20 2014 Remi Collet <remi@fedoraproject.org> - 3.1.3-1
- update to 3.1.3

* Tue Dec 31 2013 Remi Collet <remi@fedoraproject.org> - 2.1.3-1
- Initial packaging
