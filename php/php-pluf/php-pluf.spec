%global shortname pluf
%global git b1fed2e6d592d18527cfff6e78a5e14058708173
%global shortgit b1fed2e

Name:           php-pluf
Version:        1.0
Release:        3.git%{shortgit}%{?dist}
Summary:        PHP WebApp Framework

Group:          Development/Libraries
License:        LGPLv2+
URL:            http://www.pluf.org/
# The source for this package was pulled from upstream's git.Use the
# following commands to generate the archive:
# wget http://projects.ceondo.com/p/pluf/source/download/b1fed2e6d592d18527cfff6e78a5e14058708173 -O pluf-b1fed2e6d592d18527cfff6e78a5e14058708173.zip
Source0:        %{shortname}-%{git}.zip

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

Requires:       php(language) >= 5.2.4
Requires:       php-gd
Requires:       php-mbstring
Requires:       php-mysql
Requires:       php-pgsql
Requires:       php-pear(Mail)
Requires:       php-pear(Mail_Mime)


%description
Simple, elegant and easy for people used to Django but in PHP5 so easy to deploy
all over the world.


%prep
%setup -qn %{shortname}-%{git}
rm -f src/Pluf/.htaccess


%build
# empty build section, nothing required


%install
rm -rf %{buildroot}
install -d %{buildroot}%{_datadir}/php/pluf
cp -a src/* %{buildroot}%{_datadir}/php/pluf


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc CONTRIBUTORS COPYING apps
%{_datadir}/php/pluf


%changelog
* Wed Dec 19 2012 Remi Collet <RPMS@FamilleCollet.com> - 1.0-3.gitb1fed2e
- backport for remi repo.

* Tue Dec 04 2012 Guillaume Kulakowski <guillaume DOT kulakowski AT fedoraproject DOT org> - 1.0-3.gitb1fed2e
- Update from git to satisfy Indefero dependancy https://bugzilla.redhat.com/show_bug.cgi?id=575956

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jun 25 2011 Guillaume Kulakowski <guillaume DOT kulakowski AT fedoraproject DOT org> - 1.0-1
- Initial packaging
