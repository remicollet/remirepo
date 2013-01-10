%{!?pear_metadir: %global pear_metadir %{pear_phpdir}}
%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name File_Fstab

Name:           php-pear-File-Fstab
Version:        2.0.3
Release:        1%{?dist}
Summary:        Read and write fstab files

Group:          Development/Libraries
License:        PHP License v3.0
URL:            http://pear.php.net/package/File_Fstab
Source0:        http://pear.php.net/get/%{pear_name}-%{version}.tgz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php-pear(PEAR)

Requires(post): %{__pear}
Requires(postun): %{__pear}
Requires:       php-pear(PEAR)
Requires:       php-pear(PEAR)
Requires:       php-pear(PEAR) >= 1.4.0b1
Provides:       php-pear(File_Fstab) = %{version}

%description
File_Fstab is an easy-to-use package which can read & write UNIX fstab
files. It presents a pleasant object-oriented interface to the fstab.
Features:
* Supports blockdev, label, and UUID specification of mount device.
* Extendable to parse non-standard fstab formats by defining a new Entry
class for that format.
* Easily examine and set mount options for an entry.
* Stable, functional interface.
* Fully documented with PHPDoc.

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



%{pear_xmldir}/%{name}.xml
# Expand this as needed to avoid owning dirs owned by our dependencies
# and to avoid unowned dirs
%{pear_phpdir}/File/Fstab.php
%{pear_phpdir}/File/Fstab/Entry.php
%{pear_phpdir}/example.php
%{pear_datadir}/File_Fstab



%changelog
