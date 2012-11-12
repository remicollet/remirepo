%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name %(echo %{name} | sed -e 's/^php-sabredav-//' -e 's/-/_/g')
%global channelname pear.sabredav.org

Name:           php-sabredav-Sabre
Version:        1.0.0
Release:        6%{?dist}
Summary:        Base for Sabre_DAV packages

License:        BSD
URL:            http://code.google.com/p/sabredav
Source0:        http://pear.sabredav.org/get/%{pear_name}-%{version}.tgz

BuildRoot:        %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php-pear(PEAR)
BuildRequires:  php-channel(%{channelname})

Requires:       php-pear(PEAR)
Requires:       php-common >= 5.1
Requires:       php-pdo
Requires:       php-xml
Requires:       php-mbstring

Requires(post): %{__pear}
Requires(postun): %{__pear}
Requires:       php-channel(%{channelname})

Provides:       php-pear(%{pear_name}) = %{version}
Provides:       php-pear(%{channelname}/%{pear_name}) = %{version}

%description
The Base SabreDAV package provides some functionality used by all packages.

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
%{pear_phpdir}/%{pear_name}


%changelog
* Mon Nov 12 2012 Remi Collet <RPMS@FamilleCollet.com> 1.3-3
- backport for remi repo

* Wed Oct 31 2012 Joseph Marrero <jmarrero@fedoraproject.org> - 1.0.0-6
- Added the requirements deps asked by phpci
* Sun Oct 14 2012 Joseph Marrero <jmarrero@fedoraproject.org> - 1.0.0-5
- Fixed Description
* Sun Oct 14 2012 Joseph Marrero <jmarrero@fedoraproject.org> - 1.0.0-4
- Fixed Documentation directory
- Added phpci pointed requirements wich are all in php-common
- Dependencies Clean up
* Wed Oct 03 2012 Joseph Marrero <jmarrero@fedoraproject.org> - 1.0.0-3
- removed uneaded remove of %%BUILDROOT 
- changed %%define for global
- removed extra changes of directory
* Wed Oct 03 2012 Joseph Marrero <jmarrero@fedoraproject.org> - 1.0.0-2
- Change Description to be more specific to diferenciate from Sabre_DAV package
* Fri Apr 06 2012 Felix Kaechele <heffer@fedoraproject.org> - 1.0.0-1
- initial package
