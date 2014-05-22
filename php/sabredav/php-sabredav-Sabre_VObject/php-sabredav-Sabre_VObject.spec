%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global gh_commit   199b6ec87104b05e3013dfd5b90eafbbe4cf97dc
%global gh_short    %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner    fruux
%global gh_project  sabre-vobject
%global pear_name   Sabre_VObject
%global channelname pear.sabredav.org
%global reldate     2014-05-16

Name:           php-sabredav-Sabre_VObject
Version:        2.1.4
Release:        1%{?dist}
Summary:        An intuitive reader for iCalendar and vCard objects

Group:          Development/Libraries
License:        BSD
URL:            http://sabre.io/
# https://github.com/fruux/sabre-dav/issues/336
# Please update PEAR channel
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}.tar.gz
Source1:        %{name}.xml

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php-pear(PEAR)
BuildRequires:  php-channel(%{channelname})

Requires(post): %{__pear}
Requires(postun): %{__pear}

Requires:       php-mbstring
Requires:       php-pear(PEAR)
Requires:       php-channel(%{channelname})
Requires:       php-pear(%{channelname}/Sabre) >= 1.0.2

Provides:       php-pear(%{pear_name}) = %{version}
Provides:       php-pear(%{channelname}/%{pear_name}) = %{version}

%description
SabreDAV VObject plugin.

%prep
%setup -q -n %{gh_project}-%{gh_commit}

sed -e 's/@VERSION@/%{version}/' \
    -e 's/@RELDATE@/%{reldate}/' \
    %{SOURCE1} >%{name}.xml
mv lib/Sabre Sabre

# Check version
extver=$(sed -n "/VERSION/{s/.* '//;s/'.*$//;p}" Sabre/VObject/Version.php)
if test "x${extver}" != "x%{version}"; then
   : Error: Upstream version is ${extver}, expecting %{version}.
   exit 1
fi

# Check files
touch error.lst
for fic in $(find Sabre/VObject -type f)
do
  grep $fic %{name}.xml || echo -$fic >> error.lst
done

for fic in $(grep '<file' %{name}.xml | sed -e 's/.*name="//' -e 's/".*//')
do
  [ -f $fic ] || echo +$fic >> error.lst
done

if [ -s error.lst ]; then
  : Error in %{name}.xml
  cat error.lst
  exit 1
fi


%build
# Empty build section, most likely nothing required.


%install
%{__pear} install --nodeps --packagingroot %{buildroot} %{name}.xml

# Clean up unnecessary files
rm -rf %{buildroot}%{pear_metadir}/.??*

# Install XML package description
mkdir -p %{buildroot}%{pear_xmldir}
install -pm 644 %{name}.xml %{buildroot}%{pear_xmldir}


%post
%{__pear} install --nodeps --soft --force --register-only \
    %{pear_xmldir}/%{name}.xml >/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    %{__pear} uninstall --nodeps --ignore-errors --register-only \
        %{pear_name} >/dev/null || :
fi


%files
%defattr(-,root,root,-)
%doc %{pear_docdir}/%{pear_name}
%{pear_xmldir}/%{name}.xml
%{pear_phpdir}/Sabre/VObject


%changelog
* Thu May 22 2014 Remi Collet <RPMS@FamilleCollet.com> 2.1.4-1
- update to 2.1.4
- sources from github

* Thu Feb 20 2014 Remi Collet <RPMS@FamilleCollet.com> 2.1.3-2
- rebuild from SabreDAV-1.7.10 sources

* Sat Oct  5 2013 Remi Collet <RPMS@FamilleCollet.com> 2.1.3-1
- update to 2.1.3

* Wed Jun 19 2013 Remi Collet <RPMS@FamilleCollet.com> 2.1.0-1
- update to 2.1.0

* Tue May  7 2013 Remi Collet <RPMS@FamilleCollet.com> 2.0.7-1
- update to 2.0.7
  use our own package.xml as upstream doesn't use pear anymore

* Mon Nov 12 2012 Remi Collet <RPMS@FamilleCollet.com> 1.3.5-2
- backport for remi repo

* Wed Oct 31 2012 Joseph Marrero <jmarrero@fedoraproject.org> 1.3.5-2
- specified php version as pointed out by phpci
* Tue Oct 23 2012 Joseph Marrero <jmarrero@fedoraproject.org> 1.3.5-1
- update to latest version
- remove uncesary changes of directory
- change define to global
- fix documentation directory
- Fix description
* Thu Aug 30 2012 Felix Kaechele <heffer@fedoraproject.org> - 1.3.4-1
- update
* Fri Apr 06 2012 Felix Kaechele <heffer@fedoraproject.org> - 1.3.1-1
- initial package
