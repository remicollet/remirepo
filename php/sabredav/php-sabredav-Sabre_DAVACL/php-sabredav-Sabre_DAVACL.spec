%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name   Sabre_DAVACL
%global channelname pear.sabredav.org
%global mainver     1.8.5

Name:           php-sabredav-Sabre_DAVACL
Version:        1.8.4
Release:        1%{?dist}
Summary:        RFC3744 implementation for SabreDAV

Group:          Development/Libraries
License:        BSD
URL:            http://code.google.com/p/sabredav
# https://github.com/fruux/sabre-dav/issues/336
# Please update PEAR channel
Source0:        http://sabredav.googlecode.com/files/SabreDAV-%{mainver}.zip
Source1:        %{name}.xml

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php-pear(PEAR)
BuildRequires:  php-channel(%{channelname})

Requires(post): %{__pear}
Requires(postun): %{__pear}

Requires:       php-pdo
Requires:       php-xml
Requires:       php-pear(PEAR)
Requires:       php-channel(%{channelname})
Requires:       php-pear(%{channelname}/Sabre)     >= 1.0.1
Requires:       php-pear(%{channelname}/Sabre_DAV) >= 1.8.0

Provides:       php-pear(%{pear_name}) = %{version}
Provides:       php-pear(%{channelname}/%{pear_name}) = %{version}

%description
DAVACL plugin for SabreDAV.


%prep
%setup -q -n SabreDAV

cp %{SOURCE1} .
mv lib/Sabre Sabre

# Check version
extver=$(sed -n "/VERSION/{s/.* '//;s/'.*$//;p}" Sabre/DAVACL/Version.php)
if test "x${extver}" != "x%{version}"; then
   : Error: Upstream version is ${extver}, expecting %{version}.
   exit 1
fi

# Check files
touch error.lst
for fic in $(find Sabre/DAVACL -type f)
do
  grep $fic %{name}.xml || echo $fic >> error.lst
done

if [ -s error.lst ]; then
  : Missing in %{name}.xml
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
%{pear_phpdir}/Sabre/DAVACL


%changelog
* Tue May  7 2013 Remi Collet <RPMS@FamilleCollet.com> 1.8.4-1
- update to 1.8.4
  use our own package.xml as upstream doesn't use pear anymore

* Mon Nov 12 2012 Remi Collet <RPMS@FamilleCollet.com> 1.6.0-3
- backport for remi repo

* Wed Oct 31 2012 Joseph Marrero <jmarrero@fedoraproject.org> 1.6.0-3
- added required dep pointed out by phpci
* Tue Oct 23 2012 Joseph Marrero <jmarrero@fedoraproject.org> 1.6.0-2
- remove uncesary changes of directory
- change define to global
- fix documentation directory
- Fix description
* Fri Apr 06 2012 Felix Kaechele <heffer@fedoraproject.org> - 1.6.0-1
- initial package
