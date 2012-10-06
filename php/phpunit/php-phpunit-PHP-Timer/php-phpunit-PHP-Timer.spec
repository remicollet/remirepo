%{!?pear_metadir: %global pear_metadir %{pear_phpdir}}
%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name PHP_Timer
%global channel pear.phpunit.de

Name:           php-phpunit-PHP-Timer
Version:        1.0.4
Release:        1%{?dist}
Summary:        PHP Utility class for timing

Group:          Development/Libraries
License:        BSD
URL:            http://github.com/sebastianbergmann/php-timer/
Source0:        http://pear.phpunit.de/get/%{pear_name}-%{version}.tgz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  php-pear >= 1:1.9.2
BuildRequires:  php-channel(%{channel})
Requires:       php-channel(%{channel})
Requires:       php-common >= 5.2.7
Requires(post): %{__pear}
Requires(postun): %{__pear}

Provides:       php-pear(%{channel}/%{pear_name}) = %{version}


%description
PHP Utility class for timing

%prep
%setup -q -c
cd %{pear_name}-%{version}
mv ../package.xml %{name}.xml


%build
cd %{pear_name}-%{version}
# Empty build section, most likely nothing required.


%install
cd %{pear_name}-%{version}
%{__rm} -rf $RPM_BUILD_ROOT docdir
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
    %{channel}/%{pear_name} >/dev/null || :
fi


%files
%defattr(-,root,root,-)
%doc %{pear_docdir}/%{pear_name}
%{pear_xmldir}/%{name}.xml
%{pear_phpdir}/PHP

%changelog
* Sat Oct  6 2012 Remi Collet <rpms@famillecollet.com> 1.0.4-1
- update to 1.0.4

* Mon Sep 24 2012 Remi Collet <rpms@famillecollet.com> 1.0.3-1
- update to 1.0.3

* Sun Oct 23 2011 Remi Collet <rpms@famillecollet.com> 1.0.2-1
- update to 1.0.2

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Sep 26 2010 Christof Damian <christof@damian.net> - 1.0.0-2
- fix timezone warnings

* Thu Jul 15 2010 Christof Damian <christof@damian.net> - 1.0.0-1
- initial package

