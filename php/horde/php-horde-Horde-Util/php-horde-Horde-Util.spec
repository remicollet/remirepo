%{!?pear_metadir: %global pear_metadir %{pear_phpdir}}
%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name    Horde_Util
%global pear_channel pear.horde.org

Name:           php-horde-Horde-Util
Version:        2.0.0
Release:        3%{?dist}
Summary:        Horde Utility Libraries

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
Requires:       php(language) >= 5.3.0
Requires:       php-xml
Requires:       php-mbstring
Requires:       php-channel(%{pear_channel})

Provides:       php-pear(%{pear_channel}/%{pear_name}) = %{version}

%description
These classes provide functionality useful for all kind of applications.

%prep
%setup -q -c -T
tar xif %{SOURCE0}

cd %{pear_name}-%{version}
mv ../package.xml %{name}.xml


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
        pear.horde.org/%{pear_name} >/dev/null || :
fi


%files
%defattr(-,root,root,-)
%doc %{pear_docdir}/%{pear_name}
%{pear_xmldir}/%{name}.xml
%{pear_phpdir}/Horde/Array
%{pear_phpdir}/Horde/Array.php
%{pear_phpdir}/Horde/Domhtml.php
%{pear_phpdir}/Horde/String.php
%{pear_phpdir}/Horde/Util.php
%{pear_phpdir}/Horde/Variables.php
%{pear_testdir}/Horde_Util


%changelog
* Thu Nov  1 2012 Remi Collet <RPMS@FamilleCollet.com> - 2.0.0-1
- Update to 2.0.0 for remi repo

* Tue Aug 14 2012 Remi Collet <remi@fedoraproject.org> - 1.4.0-3
- rebuilt for new pear_testdir

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 17 2012 Remi Collet <RPMS@FamilleCollet.com> - 1.4.0-1
- Upgrade to 1.4.0, backport for remi repo

* Thu Jul 12 2012 Nick Bebout <nb@fedoraproject.org> - 1.4.0-1
- Update to 1.4.0

* Sat Jun 16 2012 Remi Collet <RPMS@FamilleCollet.com> - 1.3.1-1
- Upgrade to 1.3.1, backport for remi repo

* Thu Jun 14 2012 Nick Bebout <nb@fedoraproject.org> - 1.3.1-1
- Update to 1.3.1

* Thu Mar 22 2012 Remi Collet <RPMS@FamilleCollet.com> - 1.3.0-1
- update to 1.3.0, backport for remi repo

* Wed Mar 21 2012 Nick Bebout <nb@fedoraproject.org> - 1.3.0-1
- Update to 1.3.0

* Mon Feb 20 2012 Remi Collet <RPMS@FamilleCollet.com> - 1.2.0-1
- backport for remi repo

* Sat Jan 28 2012 Nick Bebout <nb@fedoraproject.org> - 1.2.0-1
- Initial package
