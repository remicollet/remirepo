# spec file for php-theseer-directoryscanner
#
# Copyright (c) 2014-2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    549aa9fdbc47d50365db42d9ade35fdef65f854c
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     theseer
%global gh_project   DirectoryScanner
%global php_home     %{_datadir}/php/TheSeer
%global pear_name    DirectoryScanner
%global pear_channel pear.netpirates.net

Name:           php-theseer-directoryscanner
Version:        1.3.2
Release:        1%{?dist}
Summary:        A recursive directory scanner and filter

Group:          Development/Libraries
License:        BSD
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php(language) >= 5.3.1
BuildRequires:  %{_bindir}/phpunit

# From composer.json
Requires:       php(language) >= 5.3.1
# From phpcompatinfo report for 1.3.0
Requires:       php-fileinfo
Requires:       php-spl

Provides:       php-composer(theseer/directoryscanner) = %{version}
Provides:       php-pear(%{pear_channel}/%{pear_name}) = %{version}


%description
A recursive directory scanner and filter.


%prep
%setup -q -n %{gh_project}-%{gh_commit}


%build
# Empty build section, most likely nothing required.


%install
rm -rf     %{buildroot}
mkdir -p   %{buildroot}%{php_home}
cp -pr src %{buildroot}%{php_home}/%{gh_project}


%check
ret=0
for cmd in php56 php70 php71 php; do
  if which $cmd; then
    $cmd %{_bindir}/phpunit \
         --bootstrap %{buildroot}%{php_home}/%{gh_project}/autoload.php \
         --verbose \
         --no-coverage || ret=1
  fi
done
exit $ret


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
%doc composer.json
%dir %{php_home}
%{php_home}/%{gh_project}


%changelog
* Fri Mar 10 2017 Remi Collet <remi@remirepo.net> - 1.3.2-1
- Update to 1.3.2 (no change)

* Tue Nov 25 2014 Remi Collet <remi@fedoraproject.org> - 1.3.1-1
- update to 1.3.1

* Tue Nov 25 2014 Remi Collet <remi@fedoraproject.org> - 1.3.0-3
- switch from pear to github sources
- enable test suite

* Sun Apr  6 2014 Remi Collet <remi@fedoraproject.org> - 1.3.0-1
- initial package, version 1.3.0
