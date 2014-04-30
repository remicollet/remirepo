# spec file for php-phpunit-Text-Template
#
# Copyright (c) 2010-2014 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/3.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    206dfefc0ffe9cebf65c413e3d0e809c82fbf00a
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     sebastianbergmann
%global gh_project   php-text-template
%global php_home     %{_datadir}/php
%global pear_name    Text_Template
%global pear_channel pear.phpunit.de
# Circular dependency with phpunit
%global with_tests   %{?_with_tests:1}%{!?_with_tests:0}

Name:           php-phpunit-Text-Template
Version:        1.2.0
Release:        3%{?dist}
Summary:        Simple template engine

Group:          Development/Libraries
License:        BSD
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php(language) >= 5.3.3

# From composer.json
Requires:       php(language) >= 5.3.3
# From phpcompatinfo report for version 1.2.0
Requires:       php-spl

# For compatibility with PEAR mode
Provides:       php-pear(%{pear_channel}/%{pear_name}) = %{version}

%description
Simple template engine.


%prep
%setup -q -n %{gh_project}-%{gh_commit}

rm Text/Template/Autoload.php.in


%build
# Empty build section, most likely nothing required.

# If upstream drop Autoload.php, command to generate it
#phpab \
#  --output   Text/Template/Autoload.php \
#  --template Text/Template/Autoload.php.in \
#  Text


%install
rm -rf      %{buildroot}
mkdir -p    %{buildroot}%{php_home}
cp -pr Text %{buildroot}%{php_home}


%clean
rm -rf %{buildroot}


%post
if [ -x %{_bindir}/pear ]; then
   %{_bindir}/pear uninstall --nodeps --ignore-errors --register-only \
      %{pear_channel}/%{pear_name} >/dev/null
fi


%files
%defattr(-,root,root,-)
%doc ChangeLog.md README.md LICENSE composer.json
%{php_home}/*


%changelog
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
