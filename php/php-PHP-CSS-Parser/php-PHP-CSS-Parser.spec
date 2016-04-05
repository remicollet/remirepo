# spec file for php-PHP-CSS-Parser
#
# Copyright (c) 2013-2016 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global gh_commit  546b2b93733165cb27c7cef0ccc8e66384d1d833
%global gh_short   %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner   sabberworm
%global gh_project PHP-CSS-Parser

Name:           php-%{gh_project}
Summary:        A Parser for CSS Files
Version:        7.0.2
Release:        1%{?dist}
License:        MIT
Group:          Development/Libraries

URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}%{?gh_short:-%{gh_short}}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
# For tests
BuildRequires:  %{_bindir}/phpunit

# From phpcompatinfo for version 7.0.2
Requires:       php-iconv
Requires:       php-mbstring
Requires:       php-pcre

Provides:       php-composer(sabberworm/php-css-parser) = %{version}


%description
PHP CSS Parser: a Parser for CSS Files written in PHP.
Allows extraction of CSS files into a data structure, manipulation
of said structure and output as (optimized) CSS.


%prep
%setup -q -n %{gh_project}-%{gh_commit}


%build
# nothing to build


%install
mkdir -p %{buildroot}%{_datadir}/php
cp -pr lib/Sabberworm %{buildroot}%{_datadir}/php/Sabberworm


%check
cd tests
%{_bindir}/phpunit --bootstrap bootstrap.php .

if which php70; then
   php70 %{_bindir}/phpunit --bootstrap bootstrap.php .
fi


%files
%defattr(-,root,root,-)
# LICENSE is in the README.md file
%doc *md
%{_datadir}/php/Sabberworm


%changelog
* Tue Mar  5 2016 Remi Collet <remi@fedoraproject.org> - 7.0.2-1
- update to 7.0.2
- run test suite with both PHP 5 and 7 when available

* Tue Jan 13 2015 Remi Collet <remi@fedoraproject.org> - 6.0.0-1.20141009giteb29754
- update to 6.0.0 + fix for PHP 5.3
- add provides php-composer(sabberworm/php-css-parser)

* Mon Apr 28 2014 Remi Collet <remi@fedoraproject.org> - 5.1.2-1
- update to 5.1.2

* Thu Feb 20 2014 Remi Collet <remi@fedoraproject.org> - 5.1.1-2
- add upstream patch (required by Horde_Css_Parser)

* Mon Oct 28 2013 Remi Collet <remi@fedoraproject.org> - 5.1.1-1
- update to 5.1.1 (no change, only documentation)

* Sun Oct 27 2013 Remi Collet <remi@fedoraproject.org> - 5.1.0-1
- update to 5.1.0

* Fri Aug 23 2013 Remi Collet <remi@fedoraproject.org> - 5.0.8-1
- update to 5.0.8

* Wed Jun 19 2013 Remi Collet <remi@fedoraproject.org> - 5.0.6-1
- update to 5.0.6

* Fri May 31 2013 Remi Collet <remi@fedoraproject.org> - 5.0.5-1
- Initial packaging
