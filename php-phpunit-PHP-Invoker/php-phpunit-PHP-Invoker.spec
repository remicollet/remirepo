%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}

%global channel   pear.phpunit.de
%global pear_name PHP_Invoker

Name:           php-phpunit-PHP-Invoker
Version:        1.0.0
Release:        3%{?dist}
Summary:        Utility class for invoking callables with a timeout

Group:          Development/Libraries
License:        BSD
URL:            https://github.com/sebastianbergmann/php-invoker
Source0:        http://pear.phpunit.de/get/%{pear_name}-%{version}.tgz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  php-pear(PEAR) >= 1.9.4
BuildRequires:  php-channel(%{channel})

Requires(post): %{__pear}
Requires(postun): %{__pear}
Requires:       php-pear(PEAR) >= 1.9.4
Requires:       php-channel(%{channel})
# merge php-cntl + php >= 5.2.7, php-cli provides php-pcntl
Requires:       php-cli >= 5.2.7

Provides:       php-pear(%{channel}/%{pear_name}) = %{version}

%description
Utility class for invoking callables with a timeout.


%prep
%setup -q -c
cd %{pear_name}-%{version}
# package.xml is V2
mv ../package.xml %{name}.xml


%build
cd %{pear_name}-%{version}
# Empty build section, most likely nothing required.


%install
cd %{pear_name}-%{version}
rm -rf %{buildroot}
%{__pear} install --nodeps --packagingroot %{buildroot} %{name}.xml

# Clean up unnecessary files
rm -rf %{buildroot}%{pear_phpdir}/.??*

# Install XML package description
install -Dpm 644 %{name}.xml %{buildroot}%{pear_xmldir}/%{name}.xml


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
%{pear_phpdir}/PHP


%changelog
* Tue Nov 01 2011 Remi Collet <remi@fedoraproject.org> - 1.0.0-3
- fix provides

* Tue Nov 01 2011 Remi Collet <remi@fedoraproject.org> - 1.0.0-2
- new tarball, with documentation

* Tue Nov 01 2011 Remi Collet <remi@fedoraproject.org> - 1.0.0-1
- initial generated RPM by pear make-rpm-spec + cleanups

