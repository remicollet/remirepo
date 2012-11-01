%{!?pear_metadir: %global pear_metadir %{pear_phpdir}}
%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name    Horde_Url
%global pear_channel pear.horde.org

Name:           php-horde-Horde-Url
Version:        2.0.0
Release:        1%{?dist}
Summary:        Horde Url class

Group:          Development/Libraries
License:        LGPLv2+
URL:            http://pear.horde.org
Source0:        http://pear.horde.org/get/%{pear_name}-%{version}.tgz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch:      noarch
BuildRequires:  php-pear
BuildRequires:  php-channel(%{pear_channel})

Requires(post): %{__pear}
Requires(postun): %{__pear}
Requires:       php-pear(%{pear_channel}/Horde_Exception) >= 2.0.0
Conflicts:      php-pear(%{pear_channel}/Horde_Exception) >= 3.0.0
Requires:       php(language) >= 5.3.0
Requires:       php-channel(%{pear_channel})

Provides:       php-pear(%{pear_channel}/%{pear_name}) = %{version}


%description
This class represents a single URL and provides methods for manipulating
URLs.

%prep
%setup -q -c
%setup -q -c -T
tar xif %{SOURCE0}

cd %{pear_name}-%{version}
mv ../package.xml %{name}.xml


%build
cd %{pear_name}-%{version}
# Empty build section, most likely nothing required.

%install
cd %{pear_name}-%{version}
rm -rf %{buildroot}
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
%{pear_xmldir}/%{name}.xml
%{pear_phpdir}/Horde/Url
%{pear_phpdir}/Horde/Url.php
%{pear_testdir}/Horde_Url
%doc %{pear_docdir}/Horde_Url

%changelog
* Thu Nov  1 2012 Remi Collet <RPMS@FamilleCollet.com> - 2.0.0-1
- Update to 2.0.0 for remi repo

* Tue Aug 14 2012 Remi Collet <remi@fedoraproject.org> - 1.0.2-3
- rebuilt for new pear_testdir

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jun 16 2012 Remi Collet <RPMS@FamilleCollet.com> - 1.0.2-1
- Upgrade to 1.0.2, backport for remi repo

* Thu Jun 14 2012 Nick Bebout <nb@fedoraproject.org> - 1.0.2-1
- Upgrade to 1.0.2

* Mon Feb 20 2012 Remi Collet <RPMS@FamilleCollet.com> - 1.0.0-1
- backport for remi repo

* Sat Jan 28 2012 Nick Bebout <nb@fedoraproject.org> - 1.0.0-1
- Initial package
