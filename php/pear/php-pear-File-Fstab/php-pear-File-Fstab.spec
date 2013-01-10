%{!?pear_metadir: %global pear_metadir %{pear_phpdir}}
%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name File_Fstab

Name:           php-pear-File-Fstab
Version:        2.0.3
Release:        1%{?dist}
Summary:        Read and write fstab files

Group:          Development/Libraries
License:        PHP
URL:            http://pear.php.net/package/File_Fstab
Source0:        http://pear.php.net/get/%{pear_name}-%{version}.tgz

# https://pear.php.net/bugs/bug.php?id=19781
Source1:        LICENSE

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php-pear(PEAR)

Requires(post): %{__pear}
Requires(postun): %{__pear}
Requires:       php-pear(PEAR)
Requires:       php-pcre

Provides:       php-pear(%{pear_name}) = %{version}


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

cp %{SOURCE1} LICENSE

cd %{pear_name}-%{version}
# https://pear.php.net/bugs/bug.php?id=19781
sed -e '/Makefile/d' \
    -e '/example.php/s/role="php"/role="doc"/' \
    ../package.xml >%{name}.xml


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


%clean
rm -rf %{buildroot}


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
%doc LICENSE
%doc %{pear_docdir}/%{pear_name}
%{pear_xmldir}/%{name}.xml
%{pear_phpdir}/File


%changelog
* Thu Jan 10 2013 Remi Collet <remi@fedoraproject.org> - 2.0.3-1
- initial package
