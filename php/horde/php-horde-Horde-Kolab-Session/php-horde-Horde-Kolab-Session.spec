%{!?pear_metadir: %global pear_metadir %{pear_phpdir}}
%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name    Horde_Kolab_Session
%global pear_channel pear.horde.org

Name:           php-horde-Horde-Kolab-Session
Version:        2.0.1
Release:        1%{?dist}
Summary:        A package managing an active Kolab session

Group:          Development/Libraries
License:        LGPLv2
URL:            http://%{pear_channel}/
Source0:        http://%{pear_channel}/get/%{pear_name}-%{version}.tgz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php(language) >= 5.3.0
BuildRequires:  php-pear(PEAR) >= 1.7.0
BuildRequires:  php-channel(%{pear_channel})
# To run unit tests
BuildRequires:  php-pear(%{pear_channel}/Horde_Test) >= 2.1.0
BuildRequires:  php-pear(%{pear_channel}/Horde_Imap_Client) >= 2.0.0
BuildRequires:  php-pear(%{pear_channel}/Horde_Kolab_Server) >= 2.0.0

Requires(post): %{__pear}
Requires(postun): %{__pear}
Requires:       php(language) >= 5.3.0

Requires:       php-pear(PEAR) >= 1.7.0
Requires:       php-channel(%{pear_channel})
Requires:       php-pear(%{pear_channel}/Horde_Exception) >= 2.0.0
Conflicts:      php-pear(%{pear_channel}/Horde_Exception) >= 3.0.0
# Optional
Requires:       php-pear(%{pear_channel}/Horde_Imap_Client) >= 2.0.0
Conflicts:      php-pear(%{pear_channel}/Horde_Imap_Client) >= 3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Kolab_Server) >= 2.0.0
Conflicts:      php-pear(%{pear_channel}/Horde_Kolab_Server) >= 3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Log) >= 2.0.0
Conflicts:      php-pear(%{pear_channel}/Horde_Log) >= 3.0.0

Provides:       php-pear(%{pear_channel}/%{pear_name}) = %{version}


%description
This package stores Kolab specific user data in the session.

%prep
%setup -q -c
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


%check
src=$(pwd)/%{pear_name}-%{version}
cd %{pear_name}-%{version}/test/$(echo %{pear_name} | sed -e s:_:/:g)
phpunit \
    -d include_path=$src/lib:.:%{pear_phpdir} \
    -d date.timezone=UTC \
    .


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
%{pear_phpdir}/Horde/Kolab/Session
%{pear_phpdir}/Horde/Kolab/Session.php
%{pear_testdir}/%{pear_name}


%changelog
* Thu Mar 28 2013 Remi Collet <RPMS@FamilleCollet.com> - 2.0.1-1
- initial package
