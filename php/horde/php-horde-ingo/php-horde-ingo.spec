%{!?pear_metadir: %global pear_metadir %{pear_phpdir}}
%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name ingo

Name:           php-horde-ingo
Version:        3.0.2
Release:        1%{?dist}
Summary:        An email filter rules manager

Group:          Development/Libraries
License:        BSD-2-Clause
URL:            http://pear.horde.org/package/ingo
Source0:        http://pear.horde.org/get/%{pear_name}-%{version}.tgz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php-pear(PEAR)

Requires(post): %{__pear}
Requires(postun): %{__pear}
Requires:       php-pear(PEAR)
Requires:       php-pear(pear.horde.org/horde) >= 5.0.0
Requires:       php-pear(pear.horde.org/horde) < 6.0.0alpha1
Requires:       php-pear(pear.horde.org/Horde_Auth) >= 2.0.0
Requires:       php-pear(pear.horde.org/Horde_Auth) < 3.0.0alpha1
Requires:       php-pear(pear.horde.org/Horde_Autoloader) >= 2.0.0
Requires:       php-pear(pear.horde.org/Horde_Autoloader) < 3.0.0alpha1
Requires:       php-pear(pear.horde.org/Horde_Core) >= 2.0.0
Requires:       php-pear(pear.horde.org/Horde_Core) < 3.0.0alpha1
Requires:       php-pear(pear.horde.org/Horde_Exception) >= 2.0.0
Requires:       php-pear(pear.horde.org/Horde_Exception) < 3.0.0alpha1
Requires:       php-pear(pear.horde.org/Horde_Group) >= 2.0.0
Requires:       php-pear(pear.horde.org/Horde_Group) < 3.0.0alpha1
Requires:       php-pear(pear.horde.org/Horde_Form) >= 2.0.0
Requires:       php-pear(pear.horde.org/Horde_Form) < 3.0.0alpha1
Requires:       php-pear(pear.horde.org/Horde_Imap_Client) >= 2.0.0
Requires:       php-pear(pear.horde.org/Horde_Imap_Client) < 3.0.0alpha1
Requires:       php-pear(pear.horde.org/Horde_Mime) >= 2.0.0
Requires:       php-pear(pear.horde.org/Horde_Mime) < 3.0.0alpha1
Requires:       php-pear(pear.horde.org/Horde_Perms) >= 2.0.0
Requires:       php-pear(pear.horde.org/Horde_Perms) < 3.0.0alpha1
Requires:       php-pear(pear.horde.org/Horde_Share) >= 2.0.0
Requires:       php-pear(pear.horde.org/Horde_Share) < 3.0.0alpha1
Requires:       php-pear(pear.horde.org/Horde_Util) >= 2.0.0
Requires:       php-pear(pear.horde.org/Horde_Util) < 3.0.0alpha1
Requires:       php-pear(PEAR) >= 1.7.0
Provides:       php-pear(pear.horde.org/ingo) = %{version}
BuildRequires:  php-channel(pear.horde.org)
Requires:       php-channel(pear.horde.org)

%description
Ingo is an email-filter management application. It is fully
internationalized, integrated with Horde and the IMP Webmail client, and
supports both server-side (Sieve, Procmail, Maildrop) and client-side
(IMAP) message filtering.

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
rm -rf $RPM_BUILD_ROOT
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
        pear.horde.org/%{pear_name} >/dev/null || :
fi


%files
%defattr(-,root,root,-)
%doc %{pear_docdir}/%{pear_name}


%{pear_xmldir}/%{name}.xml
# Expand this as needed to avoid owning dirs owned by our dependencies
# and to avoid unowned dirs

%{pear_datadir}/ingo

%{_bindir}/ingo-convert-prefs-to-sql
%{_bindir}/ingo-convert-sql-shares-to-sqlng
%{_bindir}/ingo-postfix-policyd

%changelog
