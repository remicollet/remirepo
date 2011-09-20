%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name   PHP_CompatInfo
%global channel     bartlett.laurent-laville.org

%if 0%{?fedora} >= 12 || 0%{?rhel} >= 6
%global withhtmldoc 1
%else
%global withhtmldoc 0
%endif

# TODO : link /usr/share/pear/data/PHP_CompatInfo/misc/jquery-1.5.min.js
#        to system jquery when available, then fix License (BSD only)


Name:           php-bartlett-PHP-CompatInfo
Version:        2.1.0
Release:        2%{?dist}
Summary:        Find out version and the extensions required for a piece of code to run

Group:          Development/Libraries
# PHP-CompatInfo is BSD, bundled jquery is MIT (or GPL)
License:        BSD and MIT
URL:            http://php5.laurent-laville.org/compatinfo/
Source0:        http://bartlett.laurent-laville.org/get/%{pear_name}-%{version}%{?prever}.tgz

# for old asciidoc version https://bugzilla.redhat.com/556171
Patch0:         PHP_CompatInfo-docs.patch
# Remove unused .js script
Patch1:         PHP_CompatInfo-deljs.patch
# Install generated doc using pear command
Patch2:         PHP_CompatInfo-addhtml.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php-pear(PEAR) >= 1.9.0
BuildRequires:  php-channel(%{channel})
# to run test suite
BuildRequires:  php-pear(pear.phpunit.de/PHPUnit) >= 3.5.0
BuildRequires:  php-pear(%{channel}/PHP_Reflect) >= 0.7.0
%if %{withhtmldoc}
# to build HTML documentation
BuildRequires:  php-pear(pear.phing.info/phing)
BuildRequires:  asciidoc >= 8.4.0
%endif

Requires(post): %{__pear}
Requires(postun): %{__pear}
Requires:       php-xml >= 5.2.0
Requires:       php-pear(PEAR) >= 1.9.0
Requires:       php-pear(%{channel}/PHP_Reflect) >= 0.7.0
Requires:       php-pear(Console_CommandLine) >= 1.1.3
Requires:       php-pear(components.ez.no/ConsoleTools) >= 1.6.1
Requires:       php-pear(pear.phpunit.de/PHPUnit) >= 3.5.0
# Optional and not yet availalble php-pear(Net_Growl) >= 2.2.2
# php-pear(components.ez.no/Base) required by ConsoleTools
# php-pear(pear.phpunit.de/PHP_Timer) required by PHPUnit

Provides:       php-pear(%{channel}/%{pear_name}) = %{version}%{?prever}


%description
PHP_CompatInfo will parse a file/folder/array to find out the minimum
version and extensions required for it to run. CLI version has many reports
(extension, interface, class, function, constant) to display and ability to
show content of dictionary references.

%if %{withhtmldoc}
HTML Documentation:  %{pear_docdir}/%{pear_name}/docs/index.html
%endif


%prep
%setup -q -c

# Package is V2
cd %{pear_name}-%{version}%{?prever}
mv -f ../package.xml %{name}.xml

%patch0 -p1 -b .fix
%patch1 -p1 -b .deljs
%if %{withhtmldoc}
%patch2 -p1 -b .addhtml
%endif


%build
cd %{pear_name}-%{version}%{?prever}

%if %{withhtmldoc}
# Generate the HTML documentation
phing -f docs/build-phing.xml \
      -Dhomedir=$PWD \
      -Dasciidoc.home=%{_datadir}/asciidoc \
      make-full-docs

# asciidoc fails silently
cpt=$(find docs -name \*.html | wc -l)
echo "File generated:$cpt, expected:5"
[ $cpt -eq 5 ] || exit 1
%endif

# restore unpatched docs (for install and checksum)
mv docs/index.txt.fix docs/index.txt


%install
rm -rf %{buildroot}
cd %{pear_name}-%{version}%{?prever}
%{__pear} install --nodeps --packagingroot %{buildroot} %{name}.xml

# Clean up unnecessary files
rm -rf %{buildroot}%{pear_phpdir}/.??*

# Install XML package description
mkdir -p %{buildroot}%{pear_xmldir}
install -pm 644 %{name}.xml %{buildroot}%{pear_xmldir}

# Fix wrong-script-end-of-line-encoding
sed -i -e 's/\r//' %{buildroot}%{_bindir}/phpci
sed -i -e 's/\r//' %{buildroot}%{pear_docdir}/%{pear_name}/README.markdown


%check
cd %{pear_name}-%{version}%{?prever}

# OK (444, Assertions: 8380, Skipped: 7) when all extensions installed
# OK, but incomplete or skipped tests!
# Tests: 329, Assertions: 5446, Skipped: 133.
# Reference tests need some fixes for EL-4, so ignore result for now
%{_bindir}/phpunit \
    -d date.timezone=UTC \
    -d memory_limit=-1 \
    --bootstrap %{buildroot}%{pear_phpdir}/Bartlett/PHP/CompatInfo/Autoload.php \
%if 0%{?rhel} < 6 && 0%{?fedora} < 8
    tests || exit 0
%else
    tests
%endif


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
%dir %{pear_cfgdir}/%{pear_name}
%config(noreplace) %{pear_cfgdir}/%{pear_name}/*dist
%{pear_xmldir}/%{name}.xml
%{pear_phpdir}/Bartlett/PHP/Compat*
%{pear_testdir}/%{pear_name}
%{pear_datadir}/%{pear_name}
%{_bindir}/phpci


%changelog
* Tue Sep 20 2011 Remi Collet <Fedora@FamilleCollet.com> - 2.1.0-2
- comments from review #693204
- remove ascii*js (not used)
- add MIT to license for bundled jquery

* Thu Aug 25 2011 Remi Collet <Fedora@FamilleCollet.com> - 2.1.0-1
- Version 2.1.0 (stable) - API 2.1.0 (stable)
- fix documentation for asciidoc 8.4

* Sat Jun 02 2011 Remi Collet <Fedora@FamilleCollet.com> - 2.0.0-1
- Version 2.0.0 (stable) - API 2.0.0 (stable)
- add HTML documentation

* Tue Apr 26 2011 Remi Collet <Fedora@FamilleCollet.com> - 2.0.0-0.3.RC4
- Version 2.0.0RC4 (beta) - API 2.0.0 (beta)

* Fri Mar 25 2011 Remi Collet <Fedora@FamilleCollet.com> - 2.0.0-0.2.RC3
- Version 2.0.0RC3

* Wed Feb 25 2011 Remi Collet <Fedora@FamilleCollet.com> - 2.0.0-0.1.RC2
- Version 2.0.0RC2
- Initial Release

