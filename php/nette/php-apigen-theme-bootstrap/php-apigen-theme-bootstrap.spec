# remirepo/fedora spec file for php-apigen-theme-bootstrap
#
# Copyright (c) 2015-2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global bootstrap    1
%global gh_commit    55a35b4a3a9a5fcaa6a8fc43fb304983cab98c6c
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
#global gh_date      20150717
%global gh_owner     ApiGen
%global gh_project   ThemeBootstrap

%global composer_vendor  apigen
%global composer_project theme-bootstrap

Name:          php-%{composer_vendor}-%{composer_project}
Version:       1.1.3
Release:       1%{?github_release}%{?dist}
Summary:       Twitter Bootstrap Theme for Apigen

Group:         Development/Libraries
License:       MIT
URL:           http://www.apigen.org/
Source0:       https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{name}-%{version}-%{gh_short}.tar.gz

BuildArch:     noarch
BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# From composer.json, "require": {
#       "latte/latte": "~2.2"
Requires:      php-composer(latte/latte) >= 2.2
Requires:      php-composer(latte/latte) <  3
# For tree ownership
%if ! %{bootstrap}
Requires:      php-composer(%{composer_vendor}/apigen)
%endif

# Composer
Provides:      php-composer(%{composer_vendor}/%{composer_project}) = %{version}


%description
%{summary}.


%prep
%setup -qn %{gh_project}-%{gh_commit}


%build
# Empty build section, nothing to build


%install
rm -rf   %{buildroot}

mkdir -p   %{buildroot}%{_datadir}/%{composer_vendor}/themes
cp -rp src %{buildroot}%{_datadir}/%{composer_vendor}/themes/%{composer_project}


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc *.md
%doc composer.json
%if %{bootstrap}
%dir %{_datadir}/%{composer_vendor}
%dir %{_datadir}/%{composer_vendor}/themes
%endif
%{_datadir}/%{composer_vendor}/themes/%{composer_project}


%changelog
* Fri Oct 30 2015 Remi Collet <remi@fedoraproject.org> - 1.1.3-1
- Initial package, version 1.1.3