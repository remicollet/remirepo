%{!?pear_metadir: %global pear_metadir %{pear_phpdir}}
%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name Text_Password

# TODO tests are not compatible with recent PHPUnit (ok in svn)

Name:           php-pear-Text-Password
Version:        1.1.1
Release:        1%{?dist}
Summary:        Creating passwords with PHP

Group:          Development/Libraries
License:        PHP
URL:            http://pear.php.net/package/Text_Password
Source0:        http://pear.php.net/get/%{pear_name}-%{version}.tgz
# https://pear.php.net/bugs/19787
Source1:        LICENSE

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php-pear(PEAR)

Requires(post): %{__pear}
Requires(postun): %{__pear}
Requires:       php-pear(PEAR)

Provides:       php-pear(%{pear_name}) = %{version}


%description
Text_Password allows one to create pronounceable and unpronounceable
passwords. The full functional range is explained in the manual at
http://pear.php.net/manual/.


%prep
%setup -q -c

cp %{SOURCE1} LICENSE

cd %{pear_name}-%{version}
mv ../package.xml %{name}.xml


%build
cd %{pear_name}-%{version}
# Empty build section, most likely nothing required.


%install
cd %{pear_name}-%{version}
rm -rf %{buildroot}
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
%{pear_xmldir}/%{name}.xml
%dir %{pear_phpdir}/Text
%{pear_phpdir}/Text/Password.php
%{pear_testdir}/%{pear_name}


%changelog
* Wed Jan 16 2013 Remi Collet <remi@fedoraproject.org> - 1.1.1-1
- Initial package
