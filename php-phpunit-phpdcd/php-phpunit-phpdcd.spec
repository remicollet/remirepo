%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name phpdcd
%global channel pear.phpunit.de

Name:           php-phpunit-phpdcd
Version:        0.9.2
Release:        1%{?dist}
Summary:        Dead Code Detector (DCD) for PHP code

Group:          Development/Libraries
License:        BSD
URL:            http://github.com/sebastianbergmann/phpdcd
Source0:        http://pear.phpunit.de/get/%{pear_name}-%{version}.tgz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  php-pear >= 1:1.8.1
BuildRequires:  php-channel(%{channel})
Requires:       php-common >= 5.2.0
Requires:       php-channel(%{channel})
Requires(post): %{__pear}
Requires(postun): %{__pear}
Requires:       php-pear(pear.phpunit.de/File_Iterator) >= 1.1.0
Requires:       php-pear(pear.phpunit.de/PHP_TokenStream) >= 0.9.1
Requires:       php-pear(components.ez.no/ConsoleTools) >= 1.6 

Provides:       php-pear(%{channel}/%{pear_name}) = %{version}


%description
phpdcd is a Dead Code Detector (DCD) for PHP code. It scans a PHP project
for all declared functions and methods and reports those as being "dead 
code" that are not called at least once.

%prep
%setup -q -c
[ -f package2.xml ] || mv package.xml package2.xml
%{__mv} package2.xml %{pear_name}-%{version}/%{name}.xml


%build
cd %{pear_name}-%{version}
# Empty build section, most likely nothing required.


%install
cd %{pear_name}-%{version}
%{__rm} -rf $RPM_BUILD_ROOT docdir
%{__pear} install --nodeps --packagingroot $RPM_BUILD_ROOT %{name}.xml

# Clean up unnecessary files
%{__rm} -rf $RPM_BUILD_ROOT%{pear_phpdir}/.??*

# Install XML package description
%{__mkdir} -p $RPM_BUILD_ROOT%{pear_xmldir}
%{__install} -pm 644 %{name}.xml $RPM_BUILD_ROOT%{pear_xmldir}


%clean
%{__rm} -rf $RPM_BUILD_ROOT


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
%{pear_xmldir}/%{name}.xml
%{pear_phpdir}/PHPDCD
%{_bindir}/phpdcd


%changelog
* Tue Feb 23 2010 Remi Collet <RPMS@FamilleCollet.com> 0.9.2-1
- rebuild for remi repository

* Thu Feb 4 2010 Christof Damian <christof@damian.net> 0.9.2-1
- initial packaging

