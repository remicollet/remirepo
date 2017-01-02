# spec file for php-pear-console-color2
#
# Copyright (c) 2014-2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%{!?__pear:       %global __pear       %{_bindir}/pear}
%{!?pear_metadir: %global pear_metadir %{pear_phpdir}}
%global pear_name Console_Color2

Name:           php-pear-console-color2
Version:        0.1.2
Release:        2%{?dist}
Summary:        Easily use ANSI console colors in your application

Group:          Development/Libraries
License:        MIT
URL:            http://pear.php.net/package/%{pear_name}
Source0:        http://pear.php.net/get/%{pear_name}-%{version}.tgz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php-pear(PEAR)

Requires(post): %{__pear}
Requires(postun): %{__pear}
Requires:       php-pear(PEAR)
Requires:       php-pcre
Provides:       php-pear(%{pear_name}) = %{version}


%description
You can use Console_Color::convert to transform colorcodes like %%r into
ANSI control codes.
  <?php
  include "Console/Color2.php";
  $console = new Console_Color2();
  print $console->convert("%%rHello World!%%n");
  ?>
would print "Hello World" in red, for example.


%prep
%setup -q -c -T
tar xif %{SOURCE0}

cd %{pear_name}-%{version}
sed -e '/composer.json/s/"data"/"doc"/' \
    ../package.xml >%{name}.xml


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
        pear.php.net/%{pear_name} >/dev/null || :
fi


%files
%defattr(-,root,root,-)
%doc %{pear_docdir}/%{pear_name}
%{pear_xmldir}/%{name}.xml
# Console is own by required php-pear
%{pear_phpdir}/Console/Color2.php



%changelog
* Sun Apr 13 2014 Remi Collet <remi@fedoraproject.org> - 0.1.2-2
- fix from review #1066255
- /usr/share/pear/Console is own by pear
- fix description

* Tue Feb 18 2014 Remi Collet <remi@fedoraproject.org> - 0.1.2-1
- initial package, version 0.1.2 (alpha)