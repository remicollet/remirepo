%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name PHPUnit_SkeletonGenerator
%global channel   pear.phpunit.de

Name:           php-phpunit-PHPUnit-SkeletonGenerator
Version:        1.2.1
Release:        1%{?dist}
Summary:        Tool that can generate skeleton test classes

Group:          Development/Libraries
License:        BSD
URL:            http://pear.phpunit.de/
Source0:        http://pear.phpunit.de/get/%{pear_name}-%{version}.tgz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php(language) >= 5.3.3
BuildRequires:  php-pear(PEAR) >= 1.9.4
BuildRequires:  php-channel(%{channel})

Requires(post): %{__pear}
Requires(postun): %{__pear}
Requires:       php(language) >= 5.3.3
Requires:       php-date
Requires:       php-pcre
Requires:       php-reflection
Requires:       php-spl
Requires:       php-tokenizer
Requires:       php-pear(PEAR) >= 1.9.4
Requires:       php-channel(%{channel})
Requires:       php-pear(%{channel}/Text_Template) >= 1.1.1
Requires:       php-pear(components.ez.no/ConsoleTools) >= 1.6

Provides:       php-pear(%{channel}/%{pear_name}) = %{version}

%description
Tool that can generate skeleton test classes from production code classes
and vice versa.


%prep
%setup -q -c
cd %{pear_name}-%{version}
# Package.xml is V2
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
        %{channel}/%{pear_name} >/dev/null || :
fi


%files
%defattr(-,root,root,-)
%doc %{pear_docdir}/%{pear_name}
%{pear_xmldir}/%{name}.xml
%{_bindir}/phpunit-skelgen
%{pear_phpdir}/SebastianBergmann/PHPUnit/SkeletonGenerator


%changelog
* Sat Jun 01 2013 Remi Collet <remi@fedoraproject.org> - 1.2.1-1
- Update to 1.2.1
- add explicit requires

* Thu Oct 11 2012 Remi Collet <remi@fedoraproject.org> - 1.2.0-1
- Version 1.2.0 (stable) - API 1.2.0 (stable)
- raise dependency: php >= 5.3.3

* Sat Mar 03 2012 Remi Collet <remi@fedoraproject.org> - 1.1.0-1
- Version 1.1.0 (stable) - API 1.1.0 (stable)

* Sat Jan 21 2012 Remi Collet <remi@fedoraproject.org> - 1.0.0-1
- initial package

