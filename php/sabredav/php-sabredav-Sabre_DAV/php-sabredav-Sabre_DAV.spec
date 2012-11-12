%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name %(echo %{name} | sed -e 's/^php-sabredav-//' -e 's/-/_/g')
%global channelname pear.sabredav.org

Name:           php-sabredav-Sabre_DAV
Version:        1.6.5
Release:        1%{?dist}
Summary:        Sabre_DAV is a WebDAV framework for PHP

License:        BSD
URL:            http://code.google.com/p/sabredav
Source0:        http://pear.sabredav.org/get/%{pear_name}-%{version}.tgz

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
Requires:       php-pear(%{channelname}/Sabre)
Requires:       php-pear(%{channelname}/Sabre_HTTP)

Provides:       php-pear(%{pear_name}) = %{version}
Provides:       php-pear(%{channelname}/%{pear_name}) = %{version}

%description
SabreDAV allows you to easily add WebDAV support to a PHP application. SabreDAV
is meant to cover the entire standard.


%prep
%setup -q -c
[ -f package2.xml ] || mv package.xml package2.xml
mv package2.xml %{pear_name}-%{version}/%{pear_name}.xml


%build
# Empty build section, most likely nothing required.


%install
cd %{pear_name}-%{version}
%{__pear} install --nodeps --packagingroot $RPM_BUILD_ROOT %{pear_name}.xml

# Clean up unnecessary files
rm -rf $RPM_BUILD_ROOT%{pear_metadir}/.??*

# Install XML package description
mkdir -p $RPM_BUILD_ROOT%{pear_xmldir}
install -pm 644 %{pear_name}.xml $RPM_BUILD_ROOT%{pear_xmldir}


%post
%{__pear} install --nodeps --soft --force --register-only \
    %{pear_xmldir}/%{pear_name}.xml >/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    %{__pear} uninstall --nodeps --ignore-errors --register-only \
        %{pear_name} >/dev/null || :
fi


%files
%defattr(-,root,root,-)
%doc %doc %{pear_docdir}/%{pear_name}
%{pear_xmldir}/%{pear_name}.xml
%{pear_phpdir}/Sabre/DAV


%changelog
* Mon Nov 12 2012 Remi Collet <RPMS@FamilleCollet.com> 1.3-3
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
