%{!?pear_metadir: %global pear_metadir %{pear_phpdir}}
%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name    Horde_Form
%global pear_channel pear.horde.org

# Note : test not ready (old .phpt)

Name:           php-horde-Horde-Form
Version:        2.0.6
Release:        2%{?dist}
Summary:        Horde Form API

Group:          Development/Libraries
License:        LGPLv2
URL:            http://pear.horde.org
Source0:        http://%{pear_channel}/get/%{pear_name}-%{version}.tgz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  gettext
BuildRequires:  php(language) >= 5.3.0
BuildRequires:  php-pear(PEAR) >= 1.7.0
BuildRequires:  php-channel(%{pear_channel})

Requires(post): %{__pear}
Requires(postun): %{__pear}
Requires:       php(language) >= 5.3.0
Requires:       php-date
Requires:       php-json
Requires:       php-pcre
Requires:       php-pear(PEAR) >= 1.7.0
Requires:       php-channel(%{pear_channel})
Requires:       php-pear(%{pear_channel}/Horde_Core) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Core) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Date) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Date) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Exception) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Exception) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Mail) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Mail) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Mime) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Mime) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Nls) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Nls) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Token) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Token) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Translation) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Translation) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Util) >= 2.3.0
Requires:       php-pear(%{pear_channel}/Horde_Util) <  3.0.0

Provides:       php-pear(%{pear_channel}/%{pear_name}) = %{version}


%description
The Horde_Form package provides form rendering, validation, and other
functionality for the Horde Application Framework.


%prep
%setup -q -c

cd %{pear_name}-%{version}

# Don't install .po and .pot files
# Remove checksum for .mo, as we regenerate them
sed -e '/%{pear_name}.po/d' \
    -e '/%{pear_name}.mo/s/md5sum=.*name=/name=/' \
    ../package.xml >%{name}.xml


%build
cd %{pear_name}-%{version}

# Regenerate the locales
for po in $(find locale -name \*.po)
do
   msgfmt $po -o $(dirname $po)/$(basename $po .po).mo
done


%install
rm -rf %{buildroot}
cd %{pear_name}-%{version}
%{__pear} install --nodeps --packagingroot %{buildroot} %{name}.xml

# Clean up unnecessary files
rm -rf %{buildroot}%{pear_metadir}/.??*

# Install XML package description
mkdir -p %{buildroot}%{pear_xmldir}
install -pm 644 %{name}.xml %{buildroot}%{pear_xmldir}

for loc in locale/{??,??_??}
do
    lang=$(basename $loc)
    test -d %{buildroot}%{pear_datadir}/%{pear_name}/$loc \
         && echo "%%lang(${lang%_*}) %{pear_datadir}/%{pear_name}/$loc"
done | tee ../%{pear_name}.lang


%clean
rm -rf %{buildroot}


%post
%{__pear} install --nodeps --soft --force --register-only \
    %{pear_xmldir}/%{name}.xml >/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    %{__pear} uninstall --nodeps --ignore-errors --register-only \
        %{pear_channel}/%{pear_name} >/dev/null || :
fi


%files -f %{pear_name}.lang
%defattr(-,root,root,-)
%doc %{pear_docdir}/%{pear_name}
%{pear_xmldir}/%{name}.xml
%{pear_phpdir}/Horde/Form
%{pear_phpdir}/Horde/Form.php
%{pear_testdir}/%{pear_name}
%dir %{pear_datadir}/%{pear_name}
%dir %{pear_datadir}/%{pear_name}/locale


%changelog
* Fri Jan 10 2014 Remi Collet <remi@fedoraproject.org> - 2.0.6-2
- cleanups

* Fri Oct 25 2013 Remi Collet <remi@fedoraproject.org> - 2.0.6-1
- Update to 2.0.6

* Fri Jun 28 2013 Remi Collet <remi@fedoraproject.org> - 2.0.5-1
- Update to 2.0.5
- requires php-json, Horde_Util 2.3.0

* Fri May 31 2013 Remi Collet <remi@fedoraproject.org> - 2.0.4-1
- Update to 2.0.4
- switch from Conflicts >= max to Requires < max

* Tue Jan 29 2013 Remi Collet <remi@fedoraproject.org> - 2.0.3-1
- Update to 2.0.3

* Wed Jan  9 2013 Remi Collet <remi@fedoraproject.org> - 2.0.2-1
- Update to 2.0.2
- use local script instead of find_lang

* Thu Nov 22 2012 Remi Collet <remi@fedoraproject.org> - 2.0.1-1
- Update to 2.0.1

* Sun Nov  4 2012 Remi Collet <remi@fedoraproject.org> - 2.0.0-1
- Update to 2.0.0

* Thu Jun 21 2012 Nick Bebout <nb@fedoraproject.org> - 1.1.0-1
- Upgrade to 1.1.0

* Sat Jan 28 2012 Nick Bebout <nb@fedoraproject.org> - 1.0.6-1
- Initial package