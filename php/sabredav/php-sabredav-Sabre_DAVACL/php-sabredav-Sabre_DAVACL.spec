%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name %(echo %{name} | sed -e 's/^php-sabredav-//' -e 's/-/_/g')
%global channelname pear.sabredav.org

Name:           php-sabredav-Sabre_DAVACL
Version:        1.6.0
Release:        3%{?dist}
Summary:        RFC3744 implementation for SabreDAV

License:        BSD
URL:            http://code.google.com/p/sabredav
Source0:        http://pear.sabredav.org/get/%{pear_name}-%{version}.tgz

BuildArch:      noarch
BuildRequires:  php-pear(PEAR)
BuildRequires:  php-channel(%{channelname})

Requires(post): %{__pear}
Requires(postun): %{__pear}

Requires:       php-common >= 5.1
Requires:       php-pdo
Requires:       php-xml
Requires:       php-pear(PEAR)
Requires:       php-channel(%{channelname})
Requires:       php-pear(%{channelname}/Sabre)
Requires:       php-pear(%{channelname}/Sabre_DAV)

Provides:       php-pear(%{pear_name}) = %{version}
Provides:       php-pear(%{channelname}/%{pear_name}) = %{version}

%description
DAVACL plugin for SabreDAV.

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
rm -rf $RPM_BUILD_ROOT%{pear_phpdir}/.??*

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
%doc %{pear_docdir}/%{pear_name}
%{pear_xmldir}/%{pear_name}.xml
%{pear_phpdir}/Sabre/DAVACL


%changelog
* Wed Oct 31 2012 Joseph Marrero <jmarrero@fedoraproject.org> 1.6.0-3
- added required dep pointed out by phpci
* Tue Oct 23 2012 Joseph Marrero <jmarrero@fedoraproject.org> 1.6.0-2
- remove uncesary changes of directory
- change define to global
- fix documentation directory
- Fix description
* Fri Apr 06 2012 Felix Kaechele <heffer@fedoraproject.org> - 1.6.0-1
- initial package
