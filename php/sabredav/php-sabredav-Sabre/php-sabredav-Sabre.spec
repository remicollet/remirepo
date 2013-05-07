%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name   Sabre
%global channelname pear.sabredav.org
%global origver     1.0.0

Name:           php-sabredav-Sabre
Version:        1.0.1
Release:        1%{?dist}
Summary:        Base for Sabre_DAV packages

Group:          Development/Libraries
License:        BSD
URL:            http://code.google.com/p/sabredav
Source0:        http://pear.sabredav.org/get/%{pear_name}-%{origver}.tgz

# https://github.com/fruux/sabre-dav/issues/336
# Please update PEAR channel
# Fix autoload to use namespace and force version
Patch0:         %{name}.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php-pear(PEAR)
BuildRequires:  php-channel(%{channelname})

Requires:       php-pear(PEAR)
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
cd %{pear_name}-%{origver}
mv ../package.xml %{name}.xml

# Fix autoload to use namespace and force version
%patch0 -p0


%build
# Empty build section, most likely nothing required.


%install
cd %{pear_name}-%{origver}
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
%{pear_phpdir}/%{pear_name}


%changelog
* Tue May  7 2013 Remi Collet <RPMS@FamilleCollet.com> 1.8.5-1
- update to 1.0.1 (use namespace)
  use our own package.xml as upstream doesn't use pear anymore

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
