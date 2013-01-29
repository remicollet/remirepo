%{!?pear_metadir: %global pear_metadir %{pear_phpdir}}
%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name    Horde_Editor
%global pear_channel pear.horde.org

Name:           php-horde-Horde-Editor
Version:        2.0.2
Release:        1%{?dist}
Summary:        Horde Editor API

Group:          Development/Libraries
License:        LGPLv2
URL:            http://pear.horde.org
Source0:        http://%{pear_channel}/get/%{pear_name}-%{version}.tgz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php-common >= 5.3.0
BuildRequires:  php-pear(PEAR) >= 1.7.0
BuildRequires:  php-channel(%{pear_channel})
BuildRequires:  php-pear(%{pear_channel}/Horde_Role) >= 1.0.0

Requires(post): %{__pear}
Requires(postun): %{__pear}
Requires:       ckeditor
Requires:       php-common >= 5.3.0
Requires:       php-pear(PEAR) >= 1.7.0
Requires:       php-channel(%{pear_channel})
Requires:       php-pear(%{pear_channel}/Horde_Role) >= 1.0.0
Requires:       php-pear(%{pear_channel}/Horde_Browser) >= 2.0.0
Conflicts:      php-pear(%{pear_channel}/Horde_Browser) >= 3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Exception) >= 2.0.0
Conflicts:      php-pear(%{pear_channel}/Horde_Exception) >= 3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Serialize) >= 2.0.0
Conflicts:      php-pear(%{pear_channel}/Horde_Serialize) >= 3.0.0

Provides:       php-pear(%{pear_channel}/%{pear_name}) = %{version}


%description
The Horde_Editor package provides an API to generate the code necessary for
embedding javascript RTE editors in a web page.


%prep
%setup -q -c

cd %{pear_name}-%{version}
sed -e '/name="js/d' \
    ../package.xml >%{name}.xml

if [ ! -d  js/ckeditor ]; then
   : Check js/ckeditor path
   exit 1
fi

%build
cd %{pear_name}-%{version}
# Empty build section, most likely nothing required.


%install
rm -rf %{buildroot}
cd %{pear_name}-%{version}
%{__pear} install --nodeps --packagingroot %{buildroot} %{name}.xml

# Clean up unnecessary files
rm -rf %{buildroot}%{pear_metadir}/.??*

# Install XML package description
mkdir -p %{buildroot}%{pear_xmldir}
install -pm 644 %{name}.xml %{buildroot}%{pear_xmldir}


%clean
rm -rf %{buildroot}


%post
%{__pear} install --nodeps --soft --force --register-only \
    %{pear_xmldir}/%{name}.xml >/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    %{__pear} uninstall --nodeps --ignore-errors --register-only \
        %{pear_channel}/%{pear_name} >/dev/null || :
fi


%files
%defattr(-,root,root,-)
%doc %{pear_docdir}/%{pear_name}
%{pear_xmldir}/%{name}.xml
%{pear_phpdir}/Horde/Editor
%{pear_phpdir}/Horde/Editor.php


%changelog
* Tue Jan 29 2013 Remi Collet <RPMS@FamilleCollet.com> - 2.0.2-1
- Update to 2.0.2 for remi repo
- drop merged patch for http://bugs.horde.org/ticket/11950

* Thu Jan 24 2013 Remi Collet <remi@fedoraproject.org> - 2.0.1-2
- use Alias for system JS

* Sat Jan 12 2013 Remi Collet <remi@fedoraproject.org> - 2.0.1-1
- Initial package
