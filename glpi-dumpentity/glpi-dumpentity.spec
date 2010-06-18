%define pluginname   dumpentity
%global svnrelease   100

Name:           glpi-dumpentity
Version:        1.2.0
%if 0%{?svnrelease}
Release:        0.1.svn%{svnrelease}%{?dist}
%else
Release:        1%{?dist}
%endif
Summary:        GLPI Plugin for entity export
Summary(fr):    Extension GLPI d'export d'entité

Group:          Applications/Internet
License:        GPLv2+
URL:            http://www.glpi-project.org/

%if 0%{?svnrelease}
# svn export -r 100 https://forge.indepnet.net/svn/dumpentity/trunk dumpentity
# tar czf glpi-dumpentity-1.2.0-100.tar.gz dumpentity
Source0:        glpi-dumpentity-%{version}-%{svnrelease}.tar.gz
%else
Source0:        https://forge.indepnet.net/attachments/download/523/glpi-dumpentity-1.1.2.tar.gz
%endif


BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

Requires:       glpi >= 0.78

%description
Plugin which allow to export data from a entity to CSV.

Designed to work with client using loadentity.

%description -l fr
Extension permettant de réaliser une exportation des données 
d'une entité en CSV.

Conçue pour fonctionner avec les clients utilisant loadentity.


%prep
%setup -q -c

# dos2unix to avoid rpmlint warnings
for doc in %{pluginname}/docs/* ; do
    sed -i -e 's/\r//' $doc
done
mv %{pluginname}/docs docs


%build
# empty build


%install
rm -rf %{buildroot} 

mkdir -p %{buildroot}/%{_datadir}/glpi/plugins
cp -ar %{pluginname} %{buildroot}/%{_datadir}/glpi/plugins/%{pluginname}


%clean
rm -rf %{buildroot} 

%files
%defattr(-,root,root,-)
%doc docs/*
%{_datadir}/glpi/plugins/%{pluginname}

%changelog
* Fri Jun 18 2010 Remi Collet <Fedora@FamilleCollet.com> - 1.2.0-0.1.svn100
- update to 1.2.0 for glpi 0.78 RC (svn snapshot)

* Mon Jul 20 2009 Remi Collet <RPMS@FamilleCollet.com> - 1.0.1-1
- update to 1.0.1 for glpi 0.72

* Sat Jul 12 2008 Remi Collet <RPMS@FamilleCollet.com> - 0.2-1
- update to 0.2 for glpi 0.71

* Wed Jan 02 2008 Remi Collet <RPMS@FamilleCollet.com> - 0.2-0.20080102
- new SVN snapshot
- requires GLPI >= 0.71

* Sun Nov 11 2007 Remi Collet <RPMS@FamilleCollet.com> - 0.1-0.20071111
- new SVN snapshot

* Wed Oct 24 2007 Remi Collet <RPMS@FamilleCollet.com> - 0.1-0.20071024
- new SVN snapshot

* Sat Oct 20 2007 Remi Collet <RPMS@FamilleCollet.com> - 0.1-0.20071020
- Initial RPM

