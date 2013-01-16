%{!?pear_metadir: %global pear_metadir %{pear_phpdir}}
%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name Image_Text

Name:           php-pear-Image-Text
Version:        0.6.1
Release:        1%{?dist}
Summary:        Image_Text - Advanced text maipulations in images

Group:          Development/Libraries
License:        PHP License
URL:            http://pear.php.net/package/Image_Text
Source0:        http://pear.php.net/get/%{pear_name}-%{version}.tgz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php-pear(PEAR)

Requires(post): %{__pear}
Requires(postun): %{__pear}
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
%doc %{pear_docdir}/%{pear_name}


%{pear_xmldir}/%{name}.xml
# Expand this as needed to avoid owning dirs owned by our dependencies
# and to avoid unowned dirs
%{pear_phpdir}/Image/Text.php
%{pear_phpdir}/tests/testimages/5x10-gradient.jpg
%{pear_phpdir}/tests/testimages/5x10-gradient.png
%{pear_phpdir}/tests/testimages/5x10-red-254.jpg
%{pear_phpdir}/tests/testimages/5x10-red-254.png
%{pear_phpdir}/tests/testimages/5x10-red-index.png
%{pear_phpdir}/tests/testimages/5x10-red.png
%{pear_phpdir}/tests/testimages/10x5-red.png
%{pear_phpdir}/tests/testimages/10x5-white-grey.png
%{pear_phpdir}/tests/testimages/10x5-white-index.png
%{pear_phpdir}/tests/testimages/10x5-white.png
%{pear_phpdir}/tests/testimages/test-background-red.png
%{pear_phpdir}/tests/testimages/test-background-transparent.png
%{pear_phpdir}/tests/testimages/test-construct.png
%{pear_datadir}/Image_Text
%{pear_testdir}/Image_Text


%changelog
