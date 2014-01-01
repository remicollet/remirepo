# spec file for php-phpunit-git
#
# Copyright (c) 2013-2014 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/3.0/
#
# Please, preserve the changelog entries
#
%{!?pear_metadir: %global pear_metadir %{pear_phpdir}}
%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name    Git
%global pear_channel pear.phpunit.de

Name:           php-phpunit-git
Version:        1.2.0
Release:        4%{?dist}
Summary:        Simple wrapper for Git

Group:          Development/Libraries
License:        BSD
URL:            https://github.com/sebastianbergmann/git
Source0:        http://%{pear_channel}/get/%{pear_name}-%{version}.tgz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php(language) >= 5.3.3
BuildRequires:  php-pear(PEAR) >= 1.9.4
BuildRequires:  php-channel(%{pear_channel})

Requires(post): %{__pear}
Requires(postun): %{__pear}
Requires:       git
Requires:       php(language) >= 5.3.3
Requires:       php-spl
Requires:       php-pear(PEAR) >= 1.9.4
Requires:       php-channel(%{pear_channel})

Provides:       php-pear(%{pear_channel}/%{pear_name}) = %{version}
# Package have be renamed
Obsoletes:      php-phpunit-Git < 1.2.0-3
Provides:       php-phpunit-Git = %{name}-%{version}


%description
Simple PHP wrapper for Git.


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
        %{pear_channel}/%{pear_name} >/dev/null || :
fi


%files
%defattr(-,root,root,-)
%doc %{pear_docdir}/%{pear_name}
%{pear_xmldir}/%{name}.xml
%dir %{pear_phpdir}/SebastianBergmann
%{pear_phpdir}/SebastianBergmann/%{pear_name}


%changelog
* Sun Oct 20 2013 Remi Collet <remi@fedoraproject.org> - 1.2.0-4
- properly obsoletes old name

* Sun Oct 20 2013 Remi Collet <remi@fedoraproject.org> - 1.2.0-3
- rename to lowercase

* Tue Oct  1 2013 Remi Collet <remi@fedoraproject.org> - 1.2.0-2
- own /usr/share/pear/SebastianBergmann/Git

* Wed Aug 28 2013 Remi Collet <remi@fedoraproject.org> - 1.2.0-1
- initial package
