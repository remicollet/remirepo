%{!?pear_metadir: %global pear_metadir %{pear_phpdir}}
%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name    content
%global pear_channel pear.horde.org

# TODO
# Tests are not ready
# config: provides one ?
# "horde-content" sub package with apache stuff

Name:           php-horde-content
Version:        2.0.1
Release:        1%{?dist}
Summary:        Tagging application

Group:          Development/Libraries
License:        BSD-2-Clause
URL:            http://pear.horde.org
Source0:        http://%{pear_channel}/get/%{pear_name}-%{version}.tgz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php-pear(PEAR)
BuildRequires:  php-channel(%{pear_channel})
BuildRequires:  php-pear(%{pear_channel}/Horde_Role) >= 1.0.0

Requires(post): %{__pear}
Requires(postun): %{__pear}
Requires:       php-pear(PEAR) >= 1.7.0
Requires:       php-channel(%{pear_channel})
Requires:       php-pear(%{pear_channel}/Horde_Role) >= 1.0.0
Requires:       php-pear(%{pear_channel}/Horde_Core) >= 2.0.0
Conflicts:      php-pear(%{pear_channel}/Horde_Core) >= 3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Date) >= 2.0.0
Conflicts:      php-pear(%{pear_channel}/Horde_Date) >= 3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Exception) >= 2.0.0
Conflicts:      php-pear(%{pear_channel}/Horde_Exception) >= 3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Db) >= 2.0.0
Conflicts:      php-pear(%{pear_channel}/Horde_Db) >= 3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Injector) >= 2.0.0
Conflicts:      php-pear(%{pear_channel}/Horde_Injector) >= 3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Rdo) >= 2.0.0
Conflicts:      php-pear(%{pear_channel}/Horde_Rdo) >= 3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Util) >= 2.0.0
Conflicts:      php-pear(%{pear_channel}/Horde_Util) >= 3.0.0
# Optionnal
Requires:       php-pear(%{pear_channel}/Horde_Argv) >= 2.0.0
Conflicts:      php-pear(%{pear_channel}/Horde_Argv) >= 3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Controller) >= 2.0.0
Conflicts:      php-pear(%{pear_channel}/Horde_Controller) >= 3.0.0
# TODO Horde_ElasticSearch >= 1.0.0

Provides:       php-pear(%{pear_channel}/%{pear_name}) = %{version}


%description
This application provides tagging support for the other Horde applications.


%prep
%setup -q -c -T
tar xif %{SOURCE0}

cd %{pear_name}-%{version}
(
echo "<Directory %{pear_hordedir}/%{pear_name}>"
cat %{pear_name}-%{version}/.htaccess
echo "</Directory>"
) | tee ../httpd.conf


# Don't install .po and .pot files
# Remove checksum for .mo, as we regenerate them
sed -e '/htaccess/d' \
    ../package.xml >%{name}.xml


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

# Install Apache configuration
install -Dpm 0644 ../httpd.conf %{buildroot}%{_sysconfdir}/httpd/conf.d/%{name}.conf

# Move configuration to /etc
mkdir -p %{buildroot}%{_sysconfdir}/horde
mv %{buildroot}%{pear_hordedir}/%{pear_name}/config \
   %{buildroot}%{_sysconfdir}/horde/%{pear_name}
ln -s %{_sysconfdir}/horde/%{pear_name} %{buildroot}%{pear_hordedir}/%{pear_name}/config


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
%config(noreplace) %{_sysconfdir}/httpd/conf.d/%{name}.conf
%attr(0770,apache,apache) %dir %{_sysconfdir}/horde/%{pear_name}
%attr(0660,apache,apache) %config(noreplace) %{_sysconfdir}/horde/%{pear_name}/*.php
%{pear_testdir}/%{pear_name}
%{_bindir}/content-object-add
%{_bindir}/content-object-delete
%{_bindir}/content-tag
%{_bindir}/content-tag-add
%{_bindir}/content-tag-delete
%{_bindir}/content-untag
%dir %{pear_hordedir}/%{pear_name}
%{pear_hordedir}/%{pear_name}/app
%{pear_hordedir}/%{pear_name}/config
%{pear_hordedir}/%{pear_name}/lib
%{pear_hordedir}/%{pear_name}/migration


%changelog
* Sun Nov 18 2012 Remi Collet <RPMS@FamilleCollet.com> - 2.0.1-1
- Initial package
