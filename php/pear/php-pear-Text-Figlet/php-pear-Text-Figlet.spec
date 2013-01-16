%{!?pear_metadir: %global pear_metadir %{pear_phpdir}}
%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name Text_Figlet

Name:           php-pear-Text-Figlet
Version:        1.0.2
Release:        1%{?dist}
Summary:        Render text using FIGlet fonts

Group:          Development/Libraries
License:        PHP
URL:            http://pear.php.net/package/Text_Figlet
Source0:        http://pear.php.net/get/%{pear_name}-%{version}.tgz
# https://pear.php.net/bugs/19788
Source1:        LICENSE

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php-pear(PEAR)

Requires(post): %{__pear}
Requires(postun): %{__pear}
Requires:       php-pcre
Requires:       php-zip
Requires:       php-pear(PEAR)

Provides:       php-pear(%{pear_name}) = %{version}


%description
Engine for use FIGlet fonts to rendering text


%prep
%setup -q -c

cp %{SOURCE1} .

cd %{pear_name}-%{version}
# Fix wrong-file-end-of-line-encoding
sed -e 's/\r//' -i docs/README.TXT
# Remove checksum for altered files
sed -e '/README.TXT/s/md5sum=.*name/name/' \
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
%dir %{pear_phpdir}/Text
%{pear_phpdir}/Text/Figlet.php
%{pear_datadir}/%{pear_name}


%changelog
* Wed Jan 16 2013 Remi Collet <remi@fedoraproject.org> - 1.0.2-1
- Initial package
