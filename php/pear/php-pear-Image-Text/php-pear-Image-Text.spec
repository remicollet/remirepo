%{!?pear_metadir: %global pear_metadir %{pear_phpdir}}
%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name Image_Text

Name:           php-pear-Image-Text
Version:        0.6.1
Release:        1%{?dist}
Summary:        Advanced text manipulations in images

Group:          Development/Libraries
License:        PHP
URL:            http://pear.php.net/package/Image_Text
# remove tests which use non-free stuff (fonts)
# pear download Image_Text-%{version}
# ./strip.sh %{version}
Source0:        %{pear_name}-%{version}-strip.tgz
Source1:        strip.sh
# https://pear.php.net/bugs/19789
Source2:        LICENSE

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php-pear(PEAR)

Requires(post): %{__pear}
Requires(postun): %{__pear}
Requires:       php-gd
Requires:       php-pcre
Requires:       php-pear(PEAR)

Provides:       php-pear(Image_Text) = %{version}


%description
Image_Text provides a comfortable interface to text manipulations in GD
images. Beside common Freetype2 functionality it offers to handle texts
in a graphic- or office-tool like way. For example it allows alignment of
texts inside a text box, rotation (around the top left corner of a text
box or it's center point) and the automatic measurizement of the optimal
font size for a given text box.


%prep
%setup -q -c

cp %{SOURCE2} LICENSE

cd %{pear_name}-%{version}
# remove README (how to install and run test)
# remove make_doc*.sh (packaging stuff)
sed -e '/README/d' \
    -e '/make_doc/d' \
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
%dir %{pear_phpdir}/Image
%{pear_phpdir}/Image/Text.php


%changelog
* Wed Jan 16 2013 Remi Collet <remi@fedoraproject.org> - 0.6.1-1
- Initial package
