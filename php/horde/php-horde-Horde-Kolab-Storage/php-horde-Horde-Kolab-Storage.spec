%{!?pear_metadir: %global pear_metadir %{pear_phpdir}}
%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name    Horde_Kolab_Storage
%global pear_channel pear.horde.org

Name:           php-horde-Horde-Kolab-Storage
Version:        2.0.5
Release:        1%{?dist}
Summary:        A package for handling Kolab data stored on an IMAP server

Group:          Development/Libraries
License:        LGPLv2
URL:            http://%{pear_channel}
Source0:        http://%{pear_channel}/get/%{pear_name}-%{version}.tgz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  gettext
BuildRequires:  php(language) >= 5.3.0
BuildRequires:  php-pear(PEAR) >= 1.7.0
BuildRequires:  php-channel(%{pear_channel})
# To run unit tests
BuildRequires:  php-pear(%{pear_channel}/Horde_Test) >= 2.1.0
BuildRequires:  php-pear(%{pear_channel}/Horde_Cache) >= 2.0.0
BuildRequires:  php-pear(%{pear_channel}/Horde_History) >= 2.0.0
BuildRequires:  php-pear(%{pear_channel}/Horde_Imap_Client) >= 2.0.0
BuildRequires:  php-pear(%{pear_channel}/Horde_Kolab_Format) >= 2.0.0

Requires(post): %{__pear}
Requires(postun): %{__pear}
Requires:       php(language) >= 5.3.0
Requires:       php-date
Requires:       php-imap
Requires:       php-json
Requires:       php-pcre
Requires:       php-spl
Requires:       php-pear(PEAR) >= 1.7.0
Requires:       php-pear(%{pear_channel}/Horde_Cache) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Cache) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Exception) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Exception) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Kolab_Format) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Kolab_Format) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Mime) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Mime) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Translation) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Translation) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Support) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Support) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Util) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Util) <  3.0.0
Requires:       php-channel(%{pear_channel})
# Optional
Requires:       php-pear(%{pear_channel}/Horde_Imap_Client) >= 2.14.0
Requires:       php-pear(%{pear_channel}/Horde_Imap_Client) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_History) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_History) <  3.0.0
Requires:       php-pear(HTTP_Request)
Requires:       php-pear(Net_IMAP) >= 1.1.0

Provides:       php-pear(%{pear_channel}/%{pear_name}) = %{version}


%description
Storing user data in an IMAP account belonging to the user is one of the
Kolab server core concepts. This package provides all the necessary means
to deal with this type of data storage effectively.

%prep
%setup -q -c
cd %{pear_name}-%{version}

# Don't install .po and .pot files
# Remove checksum for .mo, as we regenerate them
sed -e '/%{pear_name}.po/d' \
    -e '/Horde_Other.po/d' \
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

# Locales
for loc in locale/{??,??_??}
do
    lang=$(basename $loc)
    test -d %{buildroot}%{pear_datadir}/%{pear_name}/$loc && \
         echo "%%lang(${lang%_*}) %{pear_datadir}/%{pear_name}/$loc"
done | tee ../%{pear_name}.lang


%check
src=$(pwd)/%{pear_name}-%{version}

# Retrieve version of Horde_Kolab_Format
#format=$(sed -n "/VERSION = /{s/.* '//;s/'.*$//;p}"  %{pear_phpdir}//Horde/Kolab/Format.php)

# fix for unit consistency in sources tree
# waiting for upstream explanation on this issue
sed -e '/VERSION =/s/%{version}/@version@/' \
    -i $src/lib/Horde/Kolab/Storage.php

cd %{pear_name}-%{version}/test/$(echo %{pear_name} | sed -e s:_:/:g)

# Disable some tests which rely on Horde_Kolab_Format and Horde_Kolab_Storage
# as switching from @version@ to 2.0.3 alter test result (line wrap)
rm ComponentTest/Data/Object/Message/ModifiedTest.php
rm ComponentTest/Data/Object/Message/NewTest.php

phpunit \
    -d include_path=$src/lib:.:%{pear_phpdir} \
    -d date.timezone=UTC \
    .


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
%{pear_phpdir}/Horde/Kolab/Storage
%{pear_phpdir}/Horde/Kolab/Storage.php
%dir %{pear_datadir}/%{pear_name}
%dir %{pear_datadir}/%{pear_name}/locale
%{pear_testdir}/%{pear_name}


%changelog
* Tue Aug 27 2013 Remi Collet <remi@fedoraproject.org> - 2.0.5-1
- Update to 2.0.5
- raise dependency on Horde_Imap_Client >= 2.14.0

* Fri Mar 29 2013 Remi Collet <RPMS@FamilleCollet.com> - 2.0.4-2
- add requires on Net_IMAP

* Thu Mar 28 2013 Remi Collet <RPMS@FamilleCollet.com> - 2.0.4-1
- initial package
