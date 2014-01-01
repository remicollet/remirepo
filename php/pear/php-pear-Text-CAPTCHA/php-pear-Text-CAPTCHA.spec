# spec file for php-pear-Text-CAPTCHA
#
# Copyright (c) 2013-2014 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/3.0/
#
# Please, preserve the changelog entries
#
%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name Text_CAPTCHA

Name:           php-pear-Text-CAPTCHA
Version:        0.5.0
Release:        1%{?dist}
Summary:        Generation of CAPTCHAs

Group:          Development/Libraries
License:        BSD
URL:            http://pear.php.net/package/Text_CAPTCHA
# remove tests which use non-free stuff (fonts)
# pear download Text_CAPTCHA-%{version}
# ./strip.sh %{version}
Source0:        %{pear_name}-%{version}-strip.tgz
Source1:        strip.sh

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php-pear(PEAR)

Requires(post): %{__pear}
Requires(postun): %{__pear}
Requires:       php-gd
Requires:       php-pear(PEAR)
Requires:       php-pear(Text_Password) >= 1.1.1
# Optional
Requires:       php-pear(Numbers_Words)
Requires:       php-pear(Text_Figlet)
Requires:       php-pear(Image_Text) >= 0.7.0

Provides:       php-pear(%{pear_name}) = %{version}

%description
Implementation of CAPTCHAs (completely automated public Turing test to tell
computers and humans apart)


%prep
%setup -q -c

cd %{pear_name}-%{version}
mv ../package.xml %{name}.xml


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
* Wed Aug 07 2013 Remi Collet <remi@fedoraproject.org> - 0.5.0-1
- Update to 0.5.0
- strip sources from non-free stuff (fonts)

* Mon Mar 18 2013 Remi Collet <remi@fedoraproject.org> - 0.4.6-1
- Version 0.4.6 (alpha) - API 0.4.0 (alpha)

* Sat Jan 26 2013 Remi Collet <remi@fedoraproject.org> - 0.4.5-1
- Version 0.4.5 (alpha) - API 0.4.0 (alpha) - no change

* Fri Jan 25 2013 Remi Collet <remi@fedoraproject.org> - 0.4.4-1
- Version 0.4.4 (alpha) - API 0.4.0 (alpha)
- LICENSE is now provided by upstream

* Wed Jan 16 2013 Remi Collet <remi@fedoraproject.org> - 0.4.3-1
- Initial package
