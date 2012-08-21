%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%define pear_name Spreadsheet_Excel_Writer

Name:           php-pear-Spreadsheet-Excel-Writer
Version:        0.9.2
Release:        5%{?dist}
Summary:        Package for generating Excel spreadsheets

Group:          Development/Libraries
License:        LGPLv2+
URL:            http://pear.php.net/package/Spreadsheet_Excel_Writer
Source0:        http://pear.php.net/get/%{pear_name}-%{version}.tgz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  php-pear >= 1:1.4.9-1.2
Requires(post): %{__pear}
Requires(postun): %{__pear}
Provides:       php-pear(%{pear_name}) = %{version}
Requires:       php-pear(OLE) >= 0.5, php-common >= 4.1.0

%description
Spreadsheet_Excel_Writer was born as a porting of the
Spreadsheet::WriteExcel Perl module to PHP.
It allows writing of Excel spreadsheets without the need for COM objects.
It supports formulas, images (BMP) and all kinds of formatting for text
and cells.
It currently supports the BIFF5 format (Excel 5.0), so functionality
appeared in the latest Excel versions is not yet available.
 


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
rm -rf $RPM_BUILD_ROOT docdir
%{__pear} install --nodeps --packagingroot $RPM_BUILD_ROOT %{name}.xml



# Clean up unnecessary files
rm -rf $RPM_BUILD_ROOT%{pear_phpdir}/.??*

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
%{pear_xmldir}/%{name}.xml
%{pear_phpdir}/Spreadsheet




%changelog 
* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Dec 11 2009 David Nalley <david@gnsa.us> 0.9.2-2
- changed require on php to php-common
* Wed Dec 02 2009 David Nalley <david@gnsa.us> 0.9.2-1
- upgraded to latest release from upstream
- fixed php-pear-ole require
- uncommented clean section
* Sat Nov 28 2009 David Nalley <david@gnsa.us> 0.9.1-2
- fixed files section to include entire directory
- fixed require to reflect proper package name
* Fri Nov 27 2009 David Nalley <david@gnsa.us> 0.9.1-1
- Initial packaging

