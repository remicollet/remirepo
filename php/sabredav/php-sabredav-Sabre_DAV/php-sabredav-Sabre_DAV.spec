%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name   Sabre_DAV
%global channelname pear.sabredav.org
%global mainver     1.8.6
%global reldate     2013-06-18

Name:           php-sabredav-Sabre_DAV
Version:        1.8.6
Release:        2%{?dist}
Summary:        Sabre_DAV is a WebDAV framework for PHP

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

Requires:       php-common >= 5.1
Requires:       php-pear(PEAR)
Requires:       php-channel(%{channelname})
Requires:       php-xml
Requires:       php-mbstring
Requires:       php-pdo
Requires:       php-pear(%{channelname}/Sabre)      >= 1.0.1
Requires:       php-pear(%{channelname}/Sabre_HTTP) >= 1.8.1

Provides:       php-pear(%{pear_name}) = %{version}
Provides:       php-pear(%{channelname}/%{pear_name}) = %{version}

%description
SabreDAV allows you to easily add WebDAV support to a PHP application. SabreDAV
is meant to cover the entire standard.


%prep
%setup -q -n SabreDAV

sed -e 's/@VERSION@/%{version}/' \
    -e 's/@RELDATE@/%{reldate}/' \
    %{SOURCE1} >%{name}.xml
mv lib/Sabre Sabre

# Check version
extver=$(sed -n "/VERSION/{s/.* '//;s/'.*$//;p}" Sabre/DAV/Version.php)
if test "x${extver}" != "x%{version}"; then
   : Error: Upstream version is ${extver}, expecting %{version}.
   exit 1
fi

# Check files
touch error.lst
for fic in $(find Sabre/DAV -type f)
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
%doc %doc %{pear_docdir}/%{pear_name}
%{pear_xmldir}/%{name}.xml
%{pear_phpdir}/Sabre/DAV


%changelog
* Thu Sep 12 2013 Remi Collet <RPMS@FamilleCollet.com> 1.8.6-2
- fix roles

* Wed Jun 19 2013 Remi Collet <RPMS@FamilleCollet.com> 1.8.6-1
- update to 1.8.6

* Tue May  7 2013 Remi Collet <RPMS@FamilleCollet.com> 1.8.5-1
- update to 1.8.5
  use our own package.xml as upstream doesn't use pear anymore

* Wed May  1 2013 Remi Collet <RPMS@FamilleCollet.com> 1.6.5-4
- sync with rawhide, backport for remi repo

* Sun Apr 28 2013 Joseph Marrero <jmarrero@fedoraproject.org> - 1.6.5-4
- added security patch that fixes bugs 951568 951569 951562
- added --ignore-errors flag to pear install macro to accept the patch

* Mon Nov 12 2012 Remi Collet <RPMS@FamilleCollet.com> 1.6.5-1
- backport for remi repo

* Wed Oct 31 2012 Joseph Marrero <jmarrero@fedoraproject.org> - 1.6.5-1
- updated to 1.6.5
- Added the required deps pointed by phpci
* Sun Oct 14 2012 Joseph Marrero <jmarrero@fedoraproject.org> - 1.6.4-4
- fixed documentation path
- fixed wrong versions on the changelog
- cleaned up dependencies
- added php-common dependency
* Wed Oct 03 2012 Joseph Marrero <jmarrero@fedoraproject.org> - 1.6.4-3
- removed unneeded %%BUILDROOT 
- removed extra changes of directory
- replaced %%define with global
* Wed Oct 03 2012 Joseph Marrero <jmarrero@fedoraproject.org> - 1.6.4-2
- update to latest upstream version
* Fri Apr 06 2012 Felix Kaechele <heffer@fedoraproject.org> - 1.6.1-1
- initial package
