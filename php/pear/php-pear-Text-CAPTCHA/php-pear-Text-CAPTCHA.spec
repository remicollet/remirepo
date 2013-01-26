%{!?pear_metadir: %global pear_metadir %{pear_phpdir}}
%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name Text_CAPTCHA

Name:           php-pear-Text-CAPTCHA
Version:        0.4.5
Release:        1%{?dist}
Summary:        Generation of CAPTCHAs

Group:          Development/Libraries
License:        BSD
URL:            http://pear.php.net/package/Text_CAPTCHA
Source0:        http://pear.php.net/get/%{pear_name}-%{version}.tgz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php-pear(PEAR)

Requires(post): %{__pear}
Requires(postun): %{__pear}
Requires:       php-gd
Requires:       php-pear(PEAR)
Requires:       php-pear(Text_Password)
# Optional
Requires:       php-pear(Numbers_Words)
Requires:       php-pear(Text_Figlet)
Requires:       php-pear(Image_Text)

Provides:       php-pear(%{pear_name}) = %{version}

%description
Implementation of CAPTCHAs (completely automated public Turing test to tell
computers and humans apart)


%prep
%setup -q -c

cd %{pear_name}-%{version}
# fix wrong-file-end-of-line-encoding
sed -e 's/\r//' -i examples/CAPTCHA_Word_test.php
# remove checksum for altered file
sed -e '/CAPTCHA_Word_test.php/s/md5sum.*name/name/' \
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
%doc %{pear_docdir}/%{pear_name}
%{pear_xmldir}/%{name}.xml
%{pear_phpdir}/Text/CAPTCHA
%{pear_phpdir}/Text/CAPTCHA.php


%changelog
* Sat Jan 26 2013 Remi Collet <remi@fedoraproject.org> - 0.4.5-1
- Version 0.4.4 (alpha) - API 0.4.0 (alpha) - no change

* Fri Jan 25 2013 Remi Collet <remi@fedoraproject.org> - 0.4.4-1
- Version 0.4.4 (alpha) - API 0.4.0 (alpha)
- LICENSE is now provided by upstream

* Wed Jan 16 2013 Remi Collet <remi@fedoraproject.org> - 0.4.3-1
- Initial package
