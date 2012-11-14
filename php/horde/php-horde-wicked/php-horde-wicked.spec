%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name    wicked
%global pear_channel pear.horde.org

Name:           php-horde-wicked
Version:        1.0.2
Release:        1%{?dist}
Summary:        Wiki application

Group:          Development/Libraries
License:        GPLv2
URL:            http://www.horde.org/apps/wicked
Source0:        http://%{pear_channel}/get/%{pear_name}-%{version}.tgz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php-pear(PEAR) >= 1.7.0
BuildRequires:  php-channel(%{pear_channel})
BuildRequires:  php-pear(%{pear_channel}/Horde_Role) >= 1.0.0

Requires(post): %{__pear}
Requires(postun): %{__pear}
Requires:       php-pear(PEAR) >= 1.7.0
Requires:       php(language) >= 5.3.0
Requires:       php-date
Requires:       php-gettext
Requires:       php-pcre
Requires:       php-spl
Requires:       php-pear(%{pear_channel}/horde) >= 4.0.0
Requires:       php-pear(%{pear_channel}/horde) < 5.0.0alpha1
Requires:       php-pear(%{pear_channel}/Horde_Auth) >= 1.0.0
Requires:       php-pear(%{pear_channel}/Horde_Auth) < 2.0.0alpha1
Requires:       php-pear(%{pear_channel}/Horde_Autoloader) >= 1.0.0
Requires:       php-pear(%{pear_channel}/Horde_Autoloader) < 2.0.0alpha1
Requires:       php-pear(%{pear_channel}/Horde_Core) >= 1.0.0
Requires:       php-pear(%{pear_channel}/Horde_Core) < 2.0.0alpha1
Requires:       php-pear(%{pear_channel}/Horde_Db) >= 1.0.0
Requires:       php-pear(%{pear_channel}/Horde_Db) < 2.0.0alpha1
Requires:       php-pear(%{pear_channel}/Horde_Exception) >= 1.0.0
Requires:       php-pear(%{pear_channel}/Horde_Exception) < 2.0.0alpha1
Requires:       php-pear(%{pear_channel}/Horde_Form) >= 1.0.0
Requires:       php-pear(%{pear_channel}/Horde_Form) < 2.0.0alpha1
Requires:       php-pear(%{pear_channel}/Horde_Http) >= 1.0.0
Requires:       php-pear(%{pear_channel}/Horde_Http) < 2.0.0alpha1
Requires:       php-pear(%{pear_channel}/Horde_Lock) >= 1.0.0
Requires:       php-pear(%{pear_channel}/Horde_Lock) < 2.0.0alpha1
Requires:       php-pear(%{pear_channel}/Horde_Mail) >= 1.0.0
Requires:       php-pear(%{pear_channel}/Horde_Mail) < 2.0.0alpha1
Requires:       php-pear(%{pear_channel}/Horde_Mime) >= 1.0.0
Requires:       php-pear(%{pear_channel}/Horde_Mime) < 2.0.0alpha1
Requires:       php-pear(%{pear_channel}/Horde_Mime_Viewer) >= 1.0.0
Requires:       php-pear(%{pear_channel}/Horde_Mime_Viewer) < 2.0.0alpha1
Requires:       php-pear(%{pear_channel}/Horde_Notification) >= 1.0.0
Requires:       php-pear(%{pear_channel}/Horde_Notification) < 2.0.0alpha1
Requires:       php-pear(%{pear_channel}/Horde_Perms) >= 1.0.0
Requires:       php-pear(%{pear_channel}/Horde_Perms) < 2.0.0alpha1
Requires:       php-pear(%{pear_channel}/Horde_Prefs) >= 1.0.0
Requires:       php-pear(%{pear_channel}/Horde_Prefs) < 2.0.0alpha1
Requires:       php-pear(%{pear_channel}/Horde_Rpc) >= 1.0.0
Requires:       php-pear(%{pear_channel}/Horde_Rpc) < 2.0.0alpha1
Requires:       php-pear(%{pear_channel}/Horde_Text_Diff) >= 1.0.0
Requires:       php-pear(%{pear_channel}/Horde_Text_Diff) < 2.0.0alpha1
Requires:       php-pear(%{pear_channel}/Horde_Url) >= 1.0.0
Requires:       php-pear(%{pear_channel}/Horde_Url) < 2.0.0alpha1
Requires:       php-pear(%{pear_channel}/Horde_Util) >= 1.0.0
Requires:       php-pear(%{pear_channel}/Horde_Util) < 2.0.0alpha1
Requires:       php-pear(%{pear_channel}/Horde_Vfs) >= 1.0.0
Requires:       php-pear(%{pear_channel}/Horde_Vfs) < 2.0.0alpha1
Requires:       php-pear(Text_Wiki) >= 1.2.0
Requires:       php-pear(Text_Wiki) < 2.0.0alpha1
Provides:       php-pear(%{pear_channel}/wicked) = %{version}
Requires:       php-channel(%{pear_channel})

%description
Wicked is a wiki application for Horde.

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


%{pear_testdir}/wicked
%{_bindir}/wicked
%{_bindir}/wicked-convert-to-utf8
%{_bindir}/wicked-mail-filter

%changelog
