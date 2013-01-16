%{!?pear_metadir: %global pear_metadir %{pear_phpdir}}
%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name Text_CAPTCHA

Name:           php-pear-Text-CAPTCHA
Version:        0.4.3
Release:        1%{?dist}
Summary:        Generation of CAPTCHAs

Group:          Development/Libraries
License:        BSD License
URL:            http://pear.php.net/package/Text_CAPTCHA
Source0:        http://pear.php.net/get/%{pear_name}-%{version}.tgz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php-pear(PEAR)

Requires(post): %{__pear}
Requires(postun): %{__pear}
Requires:       php-pear(PEAR)
Requires:       php-pear(Text_Password)
Requires:       php-pear(PEAR) >= 1.4.0b1
Provides:       php-pear(Text_CAPTCHA) = %{version}

%description
Implementation of CAPTCHAs (completely automated public Turing test to tell
computers and humans apart)

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
%{pear_phpdir}/Text/CAPTCHA/Driver/Equation.php
%{pear_phpdir}/Text/CAPTCHA/Driver/Figlet.php
%{pear_phpdir}/Text/CAPTCHA/Driver/Image.php
%{pear_phpdir}/Text/CAPTCHA/Driver/Numeral.php
%{pear_phpdir}/Text/CAPTCHA/Driver/Word.php
%{pear_phpdir}/Text/CAPTCHA.php




%changelog
