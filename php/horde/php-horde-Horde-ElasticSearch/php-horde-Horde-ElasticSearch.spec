%{!?pear_metadir: %global pear_metadir %{pear_phpdir}}
%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name Horde_ElasticSearch

Name:           php-horde-Horde-ElasticSearch
Version:        1.0.2
Release:        1%{?dist}
Summary:        Horde ElasticSearch client

Group:          Development/Libraries
License:        BSD-2-Clause
URL:            http://pear.horde.org/package/Horde_ElasticSearch
Source0:        http://pear.horde.org/get/%{pear_name}-%{version}.tgz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php-pear(PEAR)

Requires(post): %{__pear}
Requires(postun): %{__pear}
Requires:       php-pear(PEAR)
Requires:       php-pear(pear.horde.org/Horde_Exception) >= 2.0.0
Requires:       php-pear(pear.horde.org/Horde_Exception) < 3.0.0alpha1
Requires:       php-pear(pear.horde.org/Horde_Http) >= 2.0.0
Requires:       php-pear(pear.horde.org/Horde_Http) < 3.0.0alpha1
Requires:       php-pear(PEAR) >= 1.7.0
Provides:       php-pear(pear.horde.org/Horde_ElasticSearch) = %{version}
BuildRequires:  php-channel(pear.horde.org)
Requires:       php-channel(pear.horde.org)

%description
Lightweight API for ElasticSearch (http://www.elasticsearch.org/).

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
        pear.horde.org/%{pear_name} >/dev/null || :
fi


%files
%defattr(-,root,root,-)
%doc %{pear_docdir}/%{pear_name}


%{pear_xmldir}/%{name}.xml
# Expand this as needed to avoid owning dirs owned by our dependencies
# and to avoid unowned dirs
%{pear_phpdir}/Horde/ElasticSearch/Client.php
%{pear_phpdir}/Horde/ElasticSearch/Exception.php
%{pear_phpdir}/Horde/ElasticSearch/Index.php
%{pear_phpdir}/Horde/ElasticSearch/Type.php




%changelog
