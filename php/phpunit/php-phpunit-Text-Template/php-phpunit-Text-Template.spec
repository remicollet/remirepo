# remirepo/fedora spec file for php-phpunit-Text-Template
#
# Copyright (c) 2010-2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    31f8b717e51d9a2afca6c9f046f5d69fc27c8686
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     sebastianbergmann
%global gh_project   php-text-template
%global php_home     %{_datadir}/php
%global pear_name    Text_Template
%global pear_channel pear.phpunit.de

Name:           php-phpunit-Text-Template
Version:        1.2.1
Release:        1%{?dist}
Summary:        Simple template engine

Group:          Development/Libraries
License:        BSD
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}-%{gh_short}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php(language) >= 5.3.3
BuildRequires:  %{_bindir}/phpab

# From composer.json
Requires:       php(language) >= 5.3.3
# From phpcompatinfo report for version 1.2.0
Requires:       php-spl

Provides:       php-composer(phpunit/php-text-template) = %{version}


%description
Simple template engine.


%prep
%setup -q -n %{gh_project}-%{gh_commit}

: Restore previous PSR-0 layout
mkdir -p Text/Template
mv src/Template.php Text/
rmdir src


%build
: Generate autoloader
%{_bindir}/phpab \
  --output  Text/Template/Autoload.php \
  --basedir Text/Template \
  Text


%install
rm -rf      %{buildroot}
mkdir -p    %{buildroot}%{php_home}
cp -pr Text %{buildroot}%{php_home}


%clean
rm -rf %{buildroot}


%post
if [ -x %{_bindir}/pear ]; then
   %{_bindir}/pear uninstall --nodeps --ignore-errors --register-only \
      %{pear_channel}/%{pear_name} >/dev/null || :
fi


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc README.md
%doc composer.json
%{php_home}/*


%changelog
* Sun Jun 21 2015 Remi Collet <remi@fedoraproject.org> - 1.2.1-1
- update to 1.2.1
- generate autoloader

* Sat Jun  7 2014 Remi Collet <remi@fedoraproject.org> - 1.2.0-4
- composer dependencies

* Wed Apr 30 2014 Remi Collet <remi@fedoraproject.org> - 1.2.0-3
- cleanup pear registry

* Tue Apr 29 2014 Remi Collet <remi@fedoraproject.org> - 1.2.0-2
- sources from github

* Thu Jan 30 2014 Remi Collet <remi@fedoraproject.org> - 1.2.0-1
- Update to 1.2.0

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Nov  1 2012 Remi Collet <remi@fedoraproject.org> - 1.1.4-1
- Version 1.1.4 (stable) - API 1.1.0 (stable)

* Sat Oct  6 2012 Remi Collet <remi@fedoraproject.org> - 1.1.3-1
- Version 1.1.3 (stable) - API 1.1.0 (stable)

* Mon Sep 24 2012 Remi Collet <remi@fedoraproject.org> - 1.1.2-1
- Version 1.1.2 (stable) - API 1.1.0 (stable)
- LICENSE is now provided in upstream tarball

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Nov 01 2011 Remi Collet <remi@fedoraproject.org> - 1.1.1-1
- Version 1.1.1 (stable) - API 1.1.0 (stable)
- raise dependencies, PEAR 1.9.4 and PHP 5.2.7

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Dec 05 2010 Remi Collet <Fedora@famillecollet.com> - 1.1.0-1
- Version 1.1.0 (stable) - API 1.1.0 (stable)
- remove README.mardown (which is only install doc)

* Fri Nov 05 2010 Remi Collet <Fedora@famillecollet.com> - 1.0.0-2
- fix URL

* Sun Sep 26 2010 Remi Collet <Fedora@famillecollet.com> - 1.0.0-1
- initial generated spec + clean
