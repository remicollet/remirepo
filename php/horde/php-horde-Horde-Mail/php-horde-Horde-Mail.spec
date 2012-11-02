%{!?pear_metadir: %global pear_metadir %{pear_phpdir}}
%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name    Horde_Mail
%global pear_channel pear.horde.org

# Can run test because of circular dependency with Horde_Mime
%global with_tests   %{?_with_tests:1}%{!?_with_tests:0}

Name:           php-horde-Horde-Mail
Version:        2.0.0
Release:        1%{?dist}
Summary:        Horde Mail Library

Group:          Development/Libraries
License:        BSD
URL:            http://pear.horde.org
Source0:        http://%{pear_channel}/get/%{pear_name}-%{version}.tgz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch:      noarch
BuildRequires:  php-pear
BuildRequires:  php-channel(%{pear_channel})
%if %{with_tests}
# To run unit tests
BuildRequires:  php-pear(%{pear_channel}/Horde_Test) >= 2.0.0
%endif

Requires(post): %{__pear}
Requires(postun): %{__pear}
Requires:       php(language) >= 5.3.0
Requires:       php-channel(%{pear_channel})
Requires:       php-pear(%{pear_channel}/Horde_Exception) >= 2.0.0
Conflicts:      php-pear(%{pear_channel}/Horde_Exception) >= 3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Mime) >= 2.0.0
Conflicts:      php-pear(%{pear_channel}/Horde_Mime) >= 3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Stream_Filter) >= 2.0.0
Conflicts:      php-pear(%{pear_channel}/Horde_Stream_Filter) >= 3.0.0
# Optionnal
Requires:       php-pear(Net_SMTP) >= 1.6.0
Requires:       php-pear(Net_DNS2)

Provides:       php-pear(%{pear_channel}/%{pear_name}) = %{version}


%description
The Horde_Mail library is a fork of the PEAR Mail library that provides
additional functionality, including (but not limited to):
* Allows a stream to be passed in.
* Allows raw headertext to be used in the outgoing messages (required for
things like message redirection pursuant to RFC 5322 [3.6.6]).
* Native PHP 5 code.
* PHPUnit test suite.
* Provides more comprehensive sendmail error messages.
* Uses Exceptions instead of PEAR_Errors.


%prep
%setup -q -c -T
tar xif %{SOURCE0}

cd %{pear_name}-%{version}
cp ../package.xml %{name}.xml


%build
cd %{pear_name}-%{version}
# Empty build section, most likely nothing required.


%install
cd %{pear_name}-%{version}
%{__pear} install --nodeps --packagingroot %{buildroot} %{name}.xml

# Clean up unnecessary files
rm -rf %{buildroot}%{pear_metadir}/.??*

# Install XML package description
mkdir -p %{buildroot}%{pear_xmldir}
install -pm 644 %{name}.xml %{buildroot}%{pear_xmldir}


%check
%if %{with_tests}
cd %{pear_name}-%{version}/test/$(echo %{pear_name} | sed -e s:_:/:g)
phpunit AllTests.php
%else
: Test disabled, missing '--with tests' option.
%endif


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
%{pear_phpdir}/Horde/Mail
%{pear_testdir}/%{pear_name}


%changelog
* Fri Nov  2 2012 Remi Collet <RPMS@FamilleCollet.com> - 2.0.0-1
- Update to 2.0.0 for remi repo

* Thu Jun 21 2012 Nick Bebout <nb@fedoraproject.org> - 1.2.0-1
- Upgrade to 1.2.0

* Sat Jan 28 2012 Nick Bebout <nb@fedoraproject.org> - 1.0.3-1
- Initial package
