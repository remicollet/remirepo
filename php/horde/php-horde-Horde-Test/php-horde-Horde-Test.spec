%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name    Horde_Test
%global pear_channel pear.horde.org

Name:           php-horde-Horde-Test
Version:        2.2.1
Release:        1%{?dist}
Summary:        Horde testing base classes

Group:          Development/Libraries
License:        LGPLv2
URL:            http://%{pear_channel}
Source0:        http://%{pear_channel}/get/%{pear_name}-%{version}.tgz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch:      noarch
BuildRequires:  php(language) >= 5.3.0
BuildRequires:  php-pear(PEAR) >= 1.7.0
BuildRequires:  php-channel(%{pear_channel})

Requires(post): %{__pear}
Requires(postun): %{__pear}
Requires:       php(language) >= 5.3.0
Requires:       php-dom
Requires:       php-json
Requires:       php-pcre
Requires:       php-pdo
Requires:       php-spl
BuildRequires:  php-pear(PEAR) >= 1.7.0
Requires:       php-channel(%{pear_channel})
Requires:       php-pear(%{pear_channel}/Horde_Support) >= 2.0.0
Conflicts:      php-pear(%{pear_channel}/Horde_Support) >= 3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Util) >= 2.0.0
Conflicts:      php-pear(%{pear_channel}/Horde_Util) >= 3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Cli) >= 2.0.0
Conflicts:      php-pear(%{pear_channel}/Horde_Cli) >= 3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Log) >= 2.0.0
Conflicts:      php-pear(%{pear_channel}/Horde_Log) >= 3.0.0
Requires:       php-pear(pear.phpunit.de/PHPUnit) >= 3.5.0

Provides:       php-pear(%{pear_channel}/%{pear_name}) = %{version}

%description
Horde-specific PHPUnit base classes.

%prep
%setup -q -c

cd %{pear_name}-%{version}
mv ../package.xml %{name}.xml


%build
cd %{pear_name}-%{version}
# Empty build section, most likely nothing required.


%install
cd %{pear_name}-%{version}
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
        %{pear_channel}/%{pear_name} >/dev/null || :
fi


%files
%defattr(-,root,root,-)
%doc %{pear_docdir}/%{pear_name}
%{pear_xmldir}/%{name}.xml
%{pear_phpdir}/Horde/Test


%changelog
* Wed Mar 06 2013 Remi Collet <remi@fedoraproject.org> - 2.2.1-1
- Update to 2.2.1

* Tue Feb 12 2013 Remi Collet <remi@fedoraproject.org> - 2.2.0-1
- Update to 2.2.0

* Sat Nov 17 2012 Remi Collet <RPMS@FamilleCollet.com> - 2.1.0-1
- Update to 2.1.0 for remi repo

* Thu Nov  1 2012 Remi Collet <RPMS@FamilleCollet.com> - 2.0.0-1
- Update to 2.0.0 for remi repo

* Mon Jun 25 2012 Nick Bebout <nb@fedoraproject.org> - 1.3.0-3
- Fix requires

* Wed Jun 20 2012 Nick Bebout <nb@fedoraproject.org> - 1.3.0-2
- Fix packaging issues

* Sat Jan 28 2012 Nick Bebout <nb@fedoraproject.org> - 1.3.0-1
- Initial package
