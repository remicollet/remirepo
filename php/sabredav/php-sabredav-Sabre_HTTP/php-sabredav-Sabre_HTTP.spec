%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name %(echo %{name} | sed -e 's/^php-sabredav-//' -e 's/-/_/g')
%global channelname pear.sabredav.org

Name:           php-sabredav-Sabre_HTTP
Version:        1.6.4
Release:        3%{?dist}
Summary:        HTTP component for the SabreDAV WebDAV framework for PHP

Group:          Development/Libraries
License:        BSD
URL:            http://code.google.com/p/sabredav
Source0:        http://pear.sabredav.org/get/%{pear_name}-%{version}.tgz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php-pear(PEAR)
BuildRequires:  php-channel(%{channelname})

Requires(post): %{__pear}
Requires(postun): %{__pear}
Requires:       php-pear(PEAR)
Requires:       php-channel(%{channelname})
Requires:       php-pear(%{channelname}/Sabre)

Provides:       php-pear(%{pear_name}) = %{version}
Provides:       php-pear(%{channelname}/%{pear_name}) = %{version}

%description
Sabre_HTTP allows for a central interface to deal with Sabre.

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
%doc %{pear_docdir}/%{pear_name}
%{pear_xmldir}/%{pear_name}.xml
%{pear_phpdir}/Sabre/HTTP


%changelog
* Mon Nov 12 2012 Remi Collet <RPMS@FamilleCollet.com> 1.6.4-3
- backport for remi repo

* Wed Oct 31 2012 Joseph Marrero <jmarrero@fedoraproject.org> - 1.6.4-3
- specified php required version pointed out by phpci
* Sun Oct 12 2012 Joseph Marrero <jmarrero@fedoraproject.org> - 1.6.4-2
- Fixed Description
* Sun Oct 12 2012 Joseph Marrero <jmarrero@fedoraproject.org> - 1.6.4-1
- Version Bump to 1.6.4
- Add necesary deps and Clean up
- Fix documentation path
- remove not needed steps 
- Fixed Description
* Fri Apr 06 2012 Felix Kaechele <heffer@fedoraproject.org> - 1.6.0-1
- initial package
