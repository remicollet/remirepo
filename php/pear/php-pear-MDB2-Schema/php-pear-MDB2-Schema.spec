# remirepo spec file for php-pear-DB, from
#
# Fedora spec file for php-pear-DB
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please, preserve the changelog entries
#
%{!?__pear: %global __pear %{_bindir}/pear}
%global ClassName MDB2_Schema

Name:           php-pear-MDB2-Schema
Version:        0.8.6
Release:        1%{?dist}
Summary:        Database Abstraction Layer

Group:          Development/Libraries
License:        BSD
URL:            http://pear.php.net/package/MDB2_Schema
Source0:        http://pear.php.net/get/%{ClassName}-%{version}.tgz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php-pear-MDB2

Requires(post): %{__pear}
Requires(postun): %{__pear}
# from package.xml, mandatory
Requires:       php-pear(MDB2) >= 2.5.0
Requires:       php-pear(XML_Parser) >= 1.2.8
# from package.xml, optional
Requires:       php-pear(XML_Serializer) >= 0.18.0
Requires:       php-pear(HTML_Template_IT) >= 1.3.0
# not available php-pear(XML_DTD) >= 0.5.1

# from phpcompatinfo
Requires:       php-pcre
Requires:       php-xml
Requires:       php-pear(PEAR)

Provides:       php-pear(%{ClassName}) = %{version}
Provides:       php-composer(pear/mdb2_schema) = %{version}


%description
XML based database schema manager

%prep
%setup -qc

cd %{ClassName}-%{version}
sed -e 's/role="www"/role="doc"/' \
    -e 's/role="data"/role="doc"/' \
    ../package.xml >%{name}.xml


%build
cd %{ClassName}-%{version}
# Empty build section, most likely nothing required.


%install
rm -rf %{buildroot}

cd %{ClassName}-%{version}
%{__pear} install --nodeps --packagingroot %{buildroot} %{name}.xml

# Clean up unnecessary files
rm -rf %{buildroot}%{pear_metadir}/.??*

# Install XML package description
install -d %{buildroot}%{pear_xmldir}
install -pm 644 %{name}.xml %{buildroot}%{pear_xmldir}


%post
%{__pear} install --nodeps --soft --force --register-only \
    %{pear_xmldir}/%{name}.xml >/dev/null ||:

%postun
if [ "$1" -eq "0" ]; then
    %{__pear} uninstall --nodeps --ignore-errors --register-only \
        %{ClassName} >/dev/null ||:
fi


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc %{pear_docdir}/%{ClassName}
%{pear_xmldir}/%{name}.xml
%{pear_testdir}/%{ClassName}
%{pear_phpdir}/MDB2/Schema*
%{_bindir}/mdb2_*


%changelog
* Thu Nov 26 2015 Remi Collet <remi@fedoraproject.org> - 0.8.6-1
- Update to 0.8.6
- add composer provide
- add mdb2_schematool command

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.5-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Aug  7 2013 Remi Collet <remi@fedoraproject.org> - 0.8.5-6
- define metadir, fix FTBFS #914363
- rename MDB2_Schema to php-pear-MDB2-Schema.xml
- remove not packaged files from package.xml
- keep doc in /usr/share/doc/pear
- add explicit dependencies

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Aug 14 2012 Remi Collet <remi@fedoraproject.org> - 0.8.5-4
- rebuilt for new pear_testdir

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Feb 24 2011 Nick Bebout <nb@fedoraproject.org> 0.8.5-1
- Update to latest release

* Thu Jul 22 2010 Chris Adams <cmadams@hiwaay.net> 0.8.0-1
- initial build
