%global libname pclzip

Name:      php-%{libname}
Version:   2.8.2
Release:   1%{?dist}
Summary:   Compression and extraction functions for Zip formatted archives

Group:     Development/Libraries
License:   LGPLv2
URL:       http://www.phpconcept.net/%{libname}
# %%{SOURCE0} gets set to "download.php?file=pclzip-2-8-2.tgz" (for example)
# so need to download the source file manually from
# http://www.phpconcept.net/pclzip/pclzip-downloads
#
# http://www.phpconcept.net/download.php?file=pclzip-VERSION_WTIH_DASHES_INSTEAD_OF_DOTS.tgz
Source0:   %{libname}-%(echo "%{version}" | sed 's/\./-/g').tgz

BuildArch: noarch

Requires:  php(language)
# phpcompatinfo (computed from version 2.8.2)
Requires:  php-date
Requires:  php-pcre
Requires:  php-zlib

%description
PclZip library offers compression and extraction functions for Zip formatted
archives (WinZip, PKZIP).

PclZip gives you the ability to manipulate zip formatted archives. You can
create an archive, list the content and extract all its content in the file
system.

PclZip defines an object class which represent a Zip Archive. This class
manages the archive properties and offers access method and actions on
the archive.


%prep
%setup -qc

# Fix wrong-file-end-of-line-encoding
sed -i 's/\r$//' *.*


%build
# Empty build section, nothing required


%install
mkdir -p %{buildroot}/%{_datadir}/php/%{libname}
cp -p *.php %{buildroot}/%{_datadir}/php/%{libname}/


%check
# No upstream tests


%files
%doc *.txt
%{_datadir}/php/%{libname}


%changelog
* Fri Jun 06 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 2.8.2-2
- Conditional %%{?dist}

* Thu May 29 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 2.8.2-1
- Initial package
