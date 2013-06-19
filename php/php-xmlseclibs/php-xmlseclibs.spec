Name:		php-xmlseclibs
Version:	1.3.1
Release:	1%{?dist}
Summary:	PHP library for XML Security

Group:		Development/Libraries
License:	BSD
URL:		http://code.google.com/p/xmlseclibs/
Source0:	https://xmlseclibs.googlecode.com/files/xmlseclibs-%{version}.tar.gz
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

Requires:	php-mcrypt
Requires:	php-dom
Requires:	php-hash
Requires:	php-libxml
Requires:	php-openssl

BuildRequires:	php-pear
BuildRequires:	php-mcrypt
BuildRequires:	php-dom
BuildRequires:	php-hash
BuildRequires:	php-libxml
BuildRequires:	php-openssl

BuildArch:	noarch

%description
xmlseclibs is a library written in PHP for working with XML Encryption and 
Signatures. 

%prep
%setup -q -n xmlseclibs

%build


%install
rm -rf $RPM_BUILD_ROOT

mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/php/xmlseclibs
cp -pr xmlseclibs.php ${RPM_BUILD_ROOT}%{_datadir}/php/xmlseclibs/

%clean
rm -rf $RPM_BUILD_ROOT

%check
%{__pear} \
   run-tests \
   -i "-d include_path=%{buildroot}%{pear_phpdir}:%{pear_phpdir}" \
   tests | tee ../tests.log
# pear doesn't set return code
if grep -q "FAILED TESTS" ../tests.log; then
  for fic in tests/*.diff; do
    cat $fic; echo -e "\n"
  done
  exit 1
fi

%files
%defattr(-,root,root,-)
%doc CHANGELOG.txt LICENSE
%{_datadir}/php/xmlseclibs


%changelog
* Wed Jun 19 2013 Remi Collet <RPMS@FamilleCollet.com> - 1.3.1-1
- backport 1.3.1 from remi repo

* Wed Jun 19 2013 F. Kooman <fkooman@tuxed.net> - 1.3.1-1
- update to 1.3.1 addressing all packaging issues

* Tue Jun 18 2013 F. Kooman <fkooman@tuxed.net> - 1.3.0-6
- add more dependencies listed by phpci output

* Tue Jun 18 2013 F. Kooman <fkooman@tuxed.net> - 1.3.0-5
- add mcrypt BuildRequires 

* Tue Jun 18 2013 F. Kooman <fkooman@tuxed.net> - 1.3.0-4
- add PEAR dependency to be able to run tests

* Tue Jun 18 2013 F. Kooman <fkooman@tuxed.net> - 1.3.0-3
- updates for package review 
- run tests

* Fri Jun 07 2013 F. Kooman <fkooman@tuxed.net> - 1.3.0-2
- add patch to support more signature methods, required by simplesamlphp 1.11.0

* Sat Feb 18 2012 F. Kooman <fkooman@tuxed.net> - 1.3.0-1
- initial package


