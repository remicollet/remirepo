%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name PHPUnit_SkeletonGenerator
%global channel   pear.phpunit.de

Name:           php-phpunit-PHPUnit-SkeletonGenerator
Version:        1.0.0
Release:        1%{?dist}
Summary:        Tool that can generate skeleton test classes

Group:          Development/Libraries
License:        BSD
URL:            http://pear.phpunit.de/
Source0:        http://pear.phpunit.de/get/%{pear_name}-%{version}.tgz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php-channel(%{channel})
BuildRequires:  php-pear(PEAR) >= 1.9.4

Requires(post): %{__pear}
Requires(postun): %{__pear}
Requires:       php-pear(PEAR) >= 1.9.4
Requires:       php-common >= 5.2.7
Requires:       php-pear(components.ez.no/ConsoleTools) >= 1.6
Requires:       php-pear(%{channel}/Text_Template) >= 1.1.1
Requires:       php-channel(%{channel})

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
rm -rf %{buildroot}%{pear_phpdir}/.??*

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
%{pear_phpdir}/PHPUnit/SkeletonGenerator
%{pear_phpdir}/PHPUnit/SkeletonGenerator.php


%changelog
* Sat Jan 21 2012 Remi Collet <remi@fedoraproject.org> - 1.0.0-1
- initial package

