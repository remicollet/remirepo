%{!?pear_metadir: %global pear_metadir %{pear_phpdir}}
%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name Net_LDAP2

Name:           php-pear-Net-LDAP2
Version:        2.1.0
Release:        1%{?dist}
Summary:        Object oriented interface for searching and manipulating LDAP-entries

Group:          Development/Libraries
License:        LGPLv3 License
URL:            http://pear.php.net/package/Net_LDAP2
Source0:        http://pear.php.net/get/%{pear_name}-%{version}.tgz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php-pear(PEAR)

Requires(post): %{__pear}
Requires(postun): %{__pear}
Requires:       php-pear(PEAR)
Provides:       php-pear(Net_LDAP2) = %{version}

%description
Net_LDAP2 is the successor of Net_LDAP which is a clone of Perls Net::LDAP
                object interface to directory servers. It does contain most
of Net::LDAPs
                features but has some own too.
                 With Net_LDAP2 you have:
                 * A simple object-oriented interface to connections,
searches entries and filters.
                 * Support for TLS and LDAP v3.
                 * Simple modification, deletion and creation of LDAP
entries.
                 * Support for schema handling.

                 Net_LDAP2 layers itself on top of PHP's existing ldap
extensions.

%prep
%setup -q -c
[ -f package2.xml ] || mv package.xml package2.xml
mv package2.xml %{pear_name}-%{version}/%{name}.xml

cd %{pear_name}-%{version}


%build
cd %{pear_name}-%{version}
# Empty build section, most likely nothing required.


%install
cd %{pear_name}-%{version}
rm -rf $RPM_BUILD_ROOT
%{__pear} install --nodeps --packagingroot $RPM_BUILD_ROOT %{name}.xml

# Clean up unnecessary files
rm -rf $RPM_BUILD_ROOT%{pear_metadir}/.??*

# Install XML package description
mkdir -p $RPM_BUILD_ROOT%{pear_xmldir}
install -pm 644 %{name}.xml $RPM_BUILD_ROOT%{pear_xmldir}


%clean
rm -rf $RPM_BUILD_ROOT


%post
%{__pear} install --nodeps --soft --force --register-only \
    %{pear_xmldir}/%{name}.xml >/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    %{__pear} uninstall --nodeps --ignore-errors --register-only \
        pear.php.net/%{pear_name} >/dev/null || :
fi


%files
%defattr(-,root,root,-)
%doc %{pear_docdir}/%{pear_name}


%{pear_xmldir}/%{name}.xml
# Expand this as needed to avoid owning dirs owned by our dependencies
# and to avoid unowned dirs
%{pear_phpdir}/Net/LDAP2/Entry.php
%{pear_phpdir}/Net/LDAP2/Filter.php
%{pear_phpdir}/Net/LDAP2/RootDSE.php
%{pear_phpdir}/Net/LDAP2/Schema.php
%{pear_phpdir}/Net/LDAP2/Search.php
%{pear_phpdir}/Net/LDAP2/Util.php
%{pear_phpdir}/Net/LDAP2/LDIF.php
%{pear_phpdir}/Net/LDAP2/SchemaCache.interface.php
%{pear_phpdir}/Net/LDAP2/SimpleFileSchemaCache.php
%{pear_phpdir}/Net/LDAP2.php

%{pear_testdir}/Net_LDAP2


%changelog
