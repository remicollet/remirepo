#
# RPM spec file for php-gliph
#
# Copyright (c) 2013-2014 Shawn Iwinski <shawn.iwinski@gmail.com>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%global github_owner     sdboyer
%global github_name      gliph
%global github_version   0.1.6
%global github_commit    9e2d52e22747c1410aa434a40b5f763c2755c4c8

%global composer_vendor  sdboyer
%global composer_project gliph

%global lib_name         Gliph

# "php": ">=5.3"
%global php_min_ver      5.3.0

Name:      php-%{composer_project}
Version:   %{github_version}
Release:   1%{?github_release}%{?dist}
Summary:   A graph library for PHP

Group:     Development/Libraries
License:   MIT
URL:       https://github.com/%{github_owner}/%{github_name}
Source0:   %{url}/archive/%{github_commit}/%{name}-%{version}-%{github_commit}.tar.gz

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch

# composer.json
Requires:  php(language) >= %{php_min_ver}
# phpcompatinfo (computed from version 0.1.6)
Requires:  php-spl

# Composer
Provides:  php-composer(%{composer_vendor}/%{composer_project}) = %{version}

%description
Gliph is a graph library for PHP. It provides graph building blocks and
data structures for use by other PHP applications. It is (currently) designed
for use with in-memory graphs, not for interaction with a graph database like
Neo4J (http://neo4j.org/).


%prep
%setup -qn %{github_name}-%{github_commit}


%build
# Empty build section, nothing to build


%install
rm -rf %{buildroot}
mkdir -pm 0755 %{buildroot}%{_datadir}/php
cp -rp src/%{lib_name} %{buildroot}%{_datadir}/php/


%check
# As of version 0.1.5, "phpunit.xml.dist" and "/tests" are git export-ignored
# therefore the RPM source tarball does not contain tests. Upstream will be
# contacted to revert the git export-ignore so tests may be run here.


%clean
rm -rf %{buildroot}


%{!?_licensedir:%global license %%doc}

%files
%defattr(-,root,root,-)
%license LICENSE
%doc README.md composer.json
%{_datadir}/php/%{lib_name}


%changelog
* Sat Jul 19 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 0.1.6-1
- Updated to 0.1.6 (BZ #1119424)
- Added "php-composer(sdboyer/gliph)" virtual provide

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
