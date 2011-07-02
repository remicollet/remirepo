%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global channel   bartlett.laurent-laville.org
%global pear_name PHP_Reflect

%if 0%{?fedora} >= 12 || 0%{?rhel} >= 6
%global withhtmldoc 1
%else
%global withhtmldoc 0
%endif


Name:           php-bartlett-PHP-Reflect
Version:        1.0.0
Release:        1%{?dist}
Summary:        Adds the ability to reverse-engineer PHP

Group:          Development/Libraries
License:        BSD
URL:            http://bartlett.laurent-laville.org/
Source0:        http://%{channel}/get/%{pear_name}-%{version}%{?prever}.tgz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php-pear(PEAR) >= 1.9.0
BuildRequires:  php-channel(%{channel})
# to run test suite
BuildRequires:  php-pear(pear.phpunit.de/PHPUnit) >= 3.5.0
%if %{withhtmldoc}
# to build HTML documentation
BuildRequires:  php-pear(pear.phing.info/phing)
BuildRequires:  asciidoc >= 8.4.0
%endif

Requires:       php-pear(PEAR) >= 1.9.0
Requires(post): %{__pear}
Requires(postun): %{__pear}
Requires:       php-channel(%{channel})

Provides:       php-pear(%{channel}/%{pear_name}) = %{version}%{?prever}


%description
PHP_Reflect adds the ability to reverse-engineer classes, interfaces,
functions, constants and more, by connecting php callbacks to other tokens.

%if %{withhtmldoc}
Documentation :  %{pear_docdir}/%{pear_name}/docs/userguide.html
%endif


%prep
%setup -q -c

# Package is V2
cd %{pear_name}-%{version}%{?prever}
mv -f ../package.xml %{name}.xml


%build
cd %{pear_name}-%{version}%{?prever}

%if %{withhtmldoc}
# Generate the HTML documentation
phing -f docs/build-phing.xml \
      -Dhomedir=$PWD \
      -Dasciidoc.home=%{_datadir}/asciidoc \
      make-userguide
%endif


%install
cd %{pear_name}-%{version}%{?prever}
rm -rf $RPM_BUILD_ROOT
%{__pear} install --nodeps --packagingroot $RPM_BUILD_ROOT %{name}.xml

# Clean up unnecessary files
rm -rf $RPM_BUILD_ROOT%{pear_phpdir}/.??*

# Install XML package description
mkdir -p $RPM_BUILD_ROOT%{pear_xmldir}
install -pm 644 %{name}.xml $RPM_BUILD_ROOT%{pear_xmldir}

%if %{withhtmldoc}
# Install the HTML Documentation
install -m 644 docs/userguide.html $RPM_BUILD_ROOT%{pear_docdir}/%{pear_name}/docs
%endif


%check
cd %{pear_name}-%{version}%{?prever}

# Version 1.0.0 : OK (25 tests, 42 assertions)
%{_bindir}/phpunit \
  -d date.timezone=UTC \
  --bootstrap $RPM_BUILD_ROOT%{pear_phpdir}/Bartlett/PHP/Reflect/Autoload.php \
  tests


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
%{pear_phpdir}/Bartlett
%{pear_testdir}/PHP_Reflect


%changelog
* Sat Jun 02 2011 Remi Collet <Fedora@FamilleCollet.com> - 1.0.0-1
- Version 1.0.0 (stable) - API 1.0.0 (stable)
- add HTML documentation

* Tue Apr 26 2011 Remi Collet <Fedora@FamilleCollet.com> - 1.0.0-0.1.RC1
- Version 1.0.0RC1 (beta) - API 1.0.0 (beta)

* Sat Apr 17 2011 Remi Collet <Fedora@FamilleCollet.com> - 0.7.0-1
- Version 0.7.0 (beta) - API 0.7.0 (beta)

* Mon Apr 11 2011 Remi Collet <Fedora@FamilleCollet.com> - 0.6.0-1
- Version 0.6.0 (beta) - API 0.6.0 (beta)

* Wed Apr 06 2011 Remi Collet <Fedora@FamilleCollet.com> - 0.5.1-1
- Version 0.5.1 (beta) - API 0.5.0 (beta)

* Fri Mar 25 2011 Remi Collet <Fedora@FamilleCollet.com> - 0.5.0-1
- Version 0.5.0 (beta) - API 0.5.0 (beta)

* Wed Feb 25 2011 Remi Collet <Fedora@FamilleCollet.com> - 0.4.0-1
- Version 0.4.0 (beta)
- Initial RPM package

