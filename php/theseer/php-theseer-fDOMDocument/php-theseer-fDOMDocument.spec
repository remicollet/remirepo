# remirepo/fedora spec file for php-theseer-fDOMDocument
#
# Copyright (c) 2013-2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#

%global gh_commit    d9ad139d6c2e8edf5e313ffbe37ff13344cf0684
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     theseer
%global gh_project   fDOMDocument
%global php_home     %{_datadir}/php/TheSeer
%global pear_name    fDOMDocument
%global pear_channel pear.netpirates.net

Name:           php-theseer-fDOMDocument
Version:        1.6.1
Release:        1%{?dist}
Summary:        An Extension to PHP standard DOM

Group:          Development/Libraries
License:        BSD
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}-%{gh_short}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php(language) >= 5.3.3
# For test
BuildRequires:  %{_bindir}/phpunit
BuildRequires:  php-dom
BuildRequires:  php-libxml

# From composer.json, requires
#        "php": ">=5.3.3",
#        "ext-dom": "*",
#        "lib-libxml": "*"
Requires:       php(language) >= 5.3.3
Requires:       php-dom
Requires:       php-libxml
# From phpcompatinfo report for version 1.6.0
Requires:       php-pcre
Requires:       php-spl

Provides:       php-pear(%{pear_channel}/%{pear_name}) = %{version}
Provides:       php-composer(theseer/fdomdocument) = %{version}


%description
An Extension to PHP's standard DOM to add various convenience methods
and exceptions by default


%prep
%setup -q -n %{gh_project}-%{gh_commit}


%build
# Empty build section, most likely nothing required.


%install
rm -rf     %{buildroot}
mkdir -p   %{buildroot}%{php_home}
cp -pr src %{buildroot}%{php_home}/%{gh_project}


%check
phpunit


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
%doc README.md composer.json
%{php_home}/%{gh_project}


%changelog
* Thu May 28 2015 Remi Collet <remi@fedoraproject.org> - 1.6.1-1
- Update to 1.6.1

* Wed Nov 26 2014 Remi Collet <remi@fedoraproject.org> - 1.6.0-2
- switch from pear to github sources

* Sun Sep 14 2014 Remi Collet <remi@fedoraproject.org> - 1.6.0-1
- Update to 1.6.0
- provide php-composer(theseer/fdomdocument)

* Wed Feb 19 2014 Remi Collet <remi@fedoraproject.org> - 1.5.0-1
- Update to 1.5.0

* Sat Dec 21 2013 Remi Collet <remi@fedoraproject.org> - 1.4.3-1
- Update to 1.4.3 (stable)

* Sun Jun 30 2013 Remi Collet <remi@fedoraproject.org> - 1.4.2-1
- Update to 1.4.2

* Sun Apr 28 2013 Remi Collet <remi@fedoraproject.org> - 1.4.1-1
- Update to 1.4.1

* Fri Apr 26 2013 Remi Collet <remi@fedoraproject.org> - 1.4.0-1
- Update to 1.4.0

* Sun Oct 28 2012 Remi Collet <remi@fedoraproject.org> - 1.3.2-1
- Version 1.3.2 (stable) - API 1.3.0 (stable)
- run test units

* Thu Oct 11 2012 Remi Collet <remi@fedoraproject.org> - 1.3.1-1
- Version 1.3.1 (stable) - API 1.3.0 (stable)
- Initial packaging