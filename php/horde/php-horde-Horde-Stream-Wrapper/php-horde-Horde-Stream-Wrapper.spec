%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name Horde_Stream_Wrapper
%global pear_channel pear.horde.org

Name:           php-horde-Horde-Stream-Wrapper
Version:        1.0.1
Release:        3%{?dist}
Summary:        Horde Stream wrappers

Group:          Development/Libraries
License:        LGPLv2+
URL:            http://pear.horde.org
Source0:        http://pear.horde.org/get/%{pear_name}-%{version}.tgz

BuildArch:      noarch

Provides:       php-pear(%{pear_channel}/%{pear_name}) = %{version}

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires:  php-pear >= 1.7.0
BuildRequires:  php-channel(%{pear_channel})

Requires(post): %{__pear}
Requires(postun): %{__pear}
Requires:       php-channel(%{pear_channel})
Requires:       php-common >= 5.2.0
Requires:       php-pear >= 1.7.0

%description
This package provides various stream wrappers.

%prep
%setup -q -c
[ -f package2.xml ] || mv package.xml package2.xml
mv package2.xml %{pear_name}-%{version}/%{name}.xml

cd %{pear_name}-%{version}

%build
cd %{pear_name}-%{version}
# Empty build section, most likely nothing required.

%install
cd %{pear_name}-%{version}
%{__pear} install --nodeps --packagingroot $RPM_BUILD_ROOT %{name}.xml

# Clean up unnecessary files
rm -rf $RPM_BUILD_ROOT%{pear_phpdir}/.??*

# Install XML package description
mkdir -p $RPM_BUILD_ROOT%{pear_xmldir}
install -pm 644 %{name}.xml $RPM_BUILD_ROOT%{pear_xmldir}

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
%{pear_xmldir}/%{name}.xml
%{pear_phpdir}/Horde
%doc %{pear_docdir}/%{pear_name}

%changelog
* Wed Aug 01 2012 Remi Collet <RPMS@FamilleCollet.com> - 1.0.1-3
- backport for remi repo

* Thu Jul 12 2012 Nick Bebout <nb@fedoraproject.org> - 1.0.1-3
- Fix packaging issues

* Tue Jul 10 2012 Nick Bebout <nb@fedoraproject.org> - 1.0.1-2
- Fix packaging issues

* Thu Jun 21 2012 Nick Bebout <nb@fedoraproject.org> - 1.0.1-1
- Upgrade to 1.0.1

* Sat Jan 28 2012 Nick Bebout <nb@fedoraproject.org> - 1.0.0-1
- Initial package
