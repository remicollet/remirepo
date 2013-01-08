Name:		php-IDNA_Convert
Version:	0.8.0
Release:	1%{?dist}
Summary:	Provides conversion of internationalized strings to UTF8

Group:		Development/Libraries
License:	LGPLv2+
URL:		http://idnaconv.phlymail.de/
Source0:	http://phlymail.com/download/Goodies/idna_convert_080.zip

BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildArch:	noarch

Requires:	php-iconv
Requires:	php-mbstring
Requires:	php-pcre
Requires:	php-spl
Requires:	php-xml


%description
This converter allows you to transfer domain names between the encoded 
(Punycode) notation and the decoded (UTF-8) notation. 


%prep
%setup -qc


%build
#empty build string to placate rpmlint

%install
rm -rf ${buildroot}
%{__mkdir} -p %{buildroot}/%{_datadir}/php/IDNA_Convert
cp -a idna_convert.class.php %{buildroot}/%{_datadir}/php/IDNA_Convert/
cp -a transcode_wrapper.php %{buildroot}/%{_datadir}/php/IDNA_Convert
cp -a uctc.php %{buildroot}/%{_datadir}/php/IDNA_Convert



%clean
rm -rf ${buildroot}


%files
%defattr(-,root,root,-)
%{_datadir}/php/IDNA_Convert
%doc LICENCE ReadMe.txt example.php



%changelog
* Tue Jan  8 2013 Remi Collet <remi@fedoraproject.org> - 0.8.0-1
- update to 0.8.0
- fix php extension dependencies, #862770

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Apr 23 2009 David Nalley <david@gnsa.us> 0.6.3-2
- Corrected license to LGPLv2+ from LGPLv2

* Wed Apr 22 2009 David Nalley <david@gnsa.us> 0.6.3-1
- Initial packaging efforts
