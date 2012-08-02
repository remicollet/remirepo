%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name CodeGen_PECL

Summary:           Tool to generate PECL extensions from an XML description
Name:              php-pear-CodeGen-PECL
Version:           1.1.3
Release:           6%{?dist}
License:           PHP
Group:             Development/Languages
URL:               http://pear.php.net/package/%{pear_name}
Source:            http://pear.php.net/get/%{pear_name}-%{version}.tgz
Patch0:            php-pear-CodeGen-PECL-1.1.3-php54.patch
Requires:          php-common >= 5.0.0, php-pear(CodeGen) >= 1.0.7
Requires(post):    %{__pear}
Requires(postun):  %{__pear}
Provides:          php-pear(%{pear_name}) = %{version}
BuildRequires:     php-pear >= 1:1.4.9-1.2, php-pear(CodeGen) >= 1.0.7
BuildArch:         noarch
BuildRoot:         %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
CodeGen_PECL (formerly known as PECL_Gen) is a pure PHP replacement for
the ext_skel shell script that comes with the PHP 4 source. It reads in
configuration options, function prototypes and code fragments from an
XML description file and then generates a complete ready-to-compile PECL
extension.

%prep
%setup -qc
%patch0 -p0 -b .php54

# Package is V2
cd %{pear_name}-%{version}
mv -f ../package.xml %{name}.xml

%build
cd %{pear_name}-%{version}
# Empty build section, most likely nothing required.

%install
rm -rf $RPM_BUILD_ROOT
cd %{pear_name}-%{version}
%{__pear} install --nodeps --packagingroot $RPM_BUILD_ROOT %{name}.xml

# Clean up unnecessary files
rm -rf $RPM_BUILD_ROOT%{pear_phpdir}/.??*

# Install XML package description
install -d $RPM_BUILD_ROOT%{pear_xmldir}
install -p -m 644 %{name}.xml $RPM_BUILD_ROOT%{pear_xmldir}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%{__pear} install --nodeps --soft --force --register-only %{pear_xmldir}/%{name}.xml >/dev/null || :

%postun
if [ $1 -eq 0 ]; then
  %{__pear} uninstall --nodeps --ignore-errors --register-only %{pear_name} >/dev/null || :
fi

%files
%defattr(-,root,root,-)
%doc %{pear_docdir}/%{pear_name}
%{_bindir}/pecl-gen
%{pear_xmldir}/%{name}.xml
%{pear_phpdir}/CodeGen/PECL/

%changelog
* Thu Aug 02 2012 Remi Collet <RPMS@FamilleCollet.com> - 1.1.3-6
- doc in /usr/share/doc/pear
- backport for remi repo

* Sun Jul 22 2012 Robert Scheck <robert@fedoraproject.org> 1.1.3-6
- Added patch to generate PHP 5.4 compilable C code

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 28 2011 Remi Collet <RPMS@FamilleCollet.com> - 1.1.3-3
- rebuild for remi repo

* Thu Feb 24 2011 Robert Scheck <robert@fedoraproject.org> 1.1.3-3
- Changed requirements to php-common/-pear(PEAR) (#662257 #c2)

* Sat Dec 11 2010 Robert Scheck <robert@fedoraproject.org> 1.1.3-2
- Corrected dependencies to match Fedora Packaging Guidelines

* Sat Dec 11 2010 Robert Scheck <robert@fedoraproject.org> 1.1.3-1
- Upgrade to 1.1.3
- Initial spec file for Fedora and Red Hat Enterprise Linux
