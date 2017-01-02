# remirepo/fedora spec file for php-zetacomponents-unit-test
#
# Copyright (c) 2015-2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#

%global gh_commit    075742e2ad692c58da4dc593518a4d110f7eb822
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     zetacomponents
%global gh_project   UnitTest
%global cname        unit-test
%global ezcdir       %{_datadir}/php/ezc

Name:           php-%{gh_owner}-%{cname}
Version:        1.0.2
Release:        2%{?dist}
Summary:        Zeta UnitTest Component

Group:          Development/Libraries
License:        ASL 2.0
URL:            http://zetacomponents.org/
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}-%{gh_short}.tar.gz

# https://github.com/zetacomponents/UnitTest/pull/5
Patch0:         %{name}-pr5.patch
# Upstream
Patch1:         %{name}-upstream.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  %{_bindir}/phpab

# From phpcompatinfo report for 1.0.2
Requires:       php(language) > 5.3
Requires:       php-pcre
Requires:       php-reflection
Requires:       php-spl
Requires:       php-composer(phpunit/phpunit)
# Also use Exception for Base, skipped to avoid circular dep.

Provides:       php-composer(%{gh_owner}/%{cname}) = %{version}


%description
UnitTest is an internal component which extends PhpUnit to facilitate test
running and reports of the components themselves.

For this reason, there is no tutorial for this component. If you really want
to use it for some reason it's sane to expect some community support on IRC or
the mailing list.


%prep
%setup -q -n %{gh_project}-%{gh_commit}

%patch0 -p1
%patch1 -p1


%build
: Generate a simple autoloader
%{_bindir}/phpab \
   --output src/autoloader.php \
   src


%install
rm -rf   %{buildroot}
mkdir -p %{buildroot}%{ezcdir}/autoload

: The library
cp -pr src \
       %{buildroot}%{ezcdir}/%{gh_project}
: For ezcBase autoloader
cp -pr src/*_autoload.php \
       %{buildroot}%{ezcdir}/autoload


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE* CREDITS
%doc ChangeLog
%doc composer.json
%doc docs design
%dir %{ezcdir}
%dir %{ezcdir}/autoload
     %{ezcdir}/autoload/*_autoload.php
     %{ezcdir}/%{gh_project}


%changelog
* Thu Jun  4 2015 Remi Collet <remi@fedoraproject.org> - 1.0.2-2
- add upstream patch for LICENSE file

* Wed Jun  3 2015 Remi Collet <remi@fedoraproject.org> - 1.0.2-1
- initial package
- open https://github.com/zetacomponents/UnitTest/issues/4 License
- open https://github.com/zetacomponents/UnitTest/pull/5 phpunit 4