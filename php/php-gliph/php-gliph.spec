%global github_owner   sdboyer
%global github_name    gliph
%global github_version 0.1.5
%global github_commit  f57d0416c63697336bcfea54f96d2c1f3c8cc6a5

%global lib_name       Gliph
%global php_min_ver    5.3.0

Name:          php-%{github_name}
Version:       %{github_version}
Release:       1%{?dist}
Summary:       A graph library for PHP

Group:         Development/Libraries
License:       MIT
URL:           https://github.com/%{github_owner}/%{github_name}
Source0:       %{url}/archive/%{github_commit}/%{name}-%{version}-%{github_commit}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:     noarch

Requires:      php(language) >= %{php_min_ver}
# phpcompatinfo
Requires:      php-spl

%description
Gliph is a graph library for PHP. It provides graph building blocks and
data structures for use by other PHP applications. It is (currently) designed
for use with in-memory graphs, not for interaction with a graph database like
Neo4J (http://neo4j.org/).


%prep
%setup -q -n %{github_name}-%{github_commit}


%build
# Empty build section, nothing to build


%install
rm -rf %{buildroot}
mkdir -p -m 755 %{buildroot}%{_datadir}/php
cp -rp src/%{lib_name} %{buildroot}%{_datadir}/php/


%check
# As of version 0.1.5, "phpunit.xml.dist" and "/tests" are git export-ignored
# therefore the RPM source tarball does not contain tests. Upstream will be
# contacted to revert the git export-ignore so tests may be run here.


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc LICENSE README.md composer.json
%{_datadir}/php/%{lib_name}


%changelog
* Thu Nov  7 2013 Remi Collet <rpms@famillecollet.com> 0.1.5-1
- backport 0.1.5 for remi repo

* Wed Nov 06 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 0.1.5-1
- Updated to 0.1.5
- Removed tests (git export-ignored upstream)

* Thu Oct 24 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 0.1.4-1.20131024git8da23c6
- Updated to latest snapshot (commit 8da23c6397354e9acc7a7e6f8d2a782fdf21ab54)
  which includes LICENSE
- "php-common" -> "php(language)"
- Added PHPUnit min/max versions

* Wed Oct 23 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 0.1.4-1
- Initial package
