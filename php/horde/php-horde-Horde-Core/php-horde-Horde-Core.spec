%{!?pear_metadir: %global pear_metadir %{pear_phpdir}}
%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name    Horde_Core
%global pear_channel pear.horde.org

Name:           php-horde-Horde-Core
Version:        2.1.3
Release:        1%{?dist}
Summary:        Horde Core Framework libraries

Group:          Development/Libraries
License:        LGPL-2.1
URL:            http://pear.horde.org
Source0:        http://%{pear_channel}/get/%{pear_name}-%{version}.tgz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  gettext
BuildRequires:  php-pear(PEAR) >= 1.7.0
BuildRequires:  php-channel(%{pear_channel})
BuildRequires:  php-pear(%{pear_channel}/Horde_Role) >= 1.0.0
# To run unit tests
BuildRequires:  php-pear(%{pear_channel}/Horde_Test) >= 2.1.0
BuildRequires:  php-pear(%{pear_channel}/Horde_Url) >= 2.0.0
BuildRequires:  php-pear(%{pear_channel}/Horde_Injector) >= 2.0.0
BuildRequires:  php-pear(%{pear_channel}/Horde_Group) >= 2.0.0

Requires(post): %{__pear}
Requires(postun): %{__pear}
Requires:       php(language) >= 5.3.0
Requires:       php-date
Requires:       php-dom
Requires:       php-gettext
Requires:       php-hash
Requires:       php-json
Requires:       php-pcre
Requires:       php-pdo_mysql
Requires:       php-reflection
Requires:       php-session
Requires:       php-simplexml
Requires:       php-sockets
Requires:       php-spl
Requires:       php-pear(PEAR) >= 1.7.0
Requires:       php-channel(%{pear_channel})
BuildRequires:  php-pear(%{pear_channel}/Horde_Role) >= 1.0.0
Requires:       php-pear(%{pear_channel}/Horde_Alarm) >= 2.0.0
Conflicts:      php-pear(%{pear_channel}/Horde_Alarm) >= 3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Auth) >= 2.0.0
Conflicts:      php-pear(%{pear_channel}/Horde_Auth) >= 3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Autoloader) >= 2.0.0
Conflicts:      php-pear(%{pear_channel}/Horde_Autoloader) >= 3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Browser) >= 2.0.0
Conflicts:      php-pear(%{pear_channel}/Horde_Browser) >= 3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Cache) >= 2.0.0
Conflicts:      php-pear(%{pear_channel}/Horde_Cache) >= 3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Cli) >= 2.0.0
Conflicts:      php-pear(%{pear_channel}/Horde_Cli) >= 3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Compress) >= 2.0.0
Conflicts:      php-pear(%{pear_channel}/Horde_Compress) >= 3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Controller) >= 2.0.0
Conflicts:      php-pear(%{pear_channel}/Horde_Controller) >= 3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Data) >= 2.0.0
Conflicts:      php-pear(%{pear_channel}/Horde_Data) >= 3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Date) >= 2.0.0
Conflicts:      php-pear(%{pear_channel}/Horde_Date) >= 3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Exception) >= 2.0.0
Conflicts:      php-pear(%{pear_channel}/Horde_Exception) >= 3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Group) >= 2.0.0
Conflicts:      php-pear(%{pear_channel}/Horde_Group) >= 3.0.0
Requires:       php-pear(%{pear_channel}/Horde_History) >= 2.0.0
Conflicts:      php-pear(%{pear_channel}/Horde_History) >= 3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Injector) >= 2.0.0
Conflicts:      php-pear(%{pear_channel}/Horde_Injector) >= 3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Lock) >= 2.0.0
Conflicts:      php-pear(%{pear_channel}/Horde_Lock) >= 3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Log) >= 2.0.0
Conflicts:      php-pear(%{pear_channel}/Horde_Log) >= 3.0.0
Requires:       php-pear(%{pear_channel}/Horde_LoginTasks) >= 2.0.0
Conflicts:      php-pear(%{pear_channel}/Horde_LoginTasks) >= 3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Mime) >= 2.0.0
Conflicts:      php-pear(%{pear_channel}/Horde_Mime) >= 3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Mime_Viewer) >= 2.0.0
Conflicts:      php-pear(%{pear_channel}/Horde_Mime_Viewer) >= 3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Notification) >= 2.0.0
Conflicts:      php-pear(%{pear_channel}/Horde_Notification) >= 3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Perms) >= 2.0.0
Conflicts:      php-pear(%{pear_channel}/Horde_Perms) >= 3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Prefs) >= 2.0.0
Conflicts:      php-pear(%{pear_channel}/Horde_Prefs) >= 3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Secret) >= 2.0.0
Conflicts:      php-pear(%{pear_channel}/Horde_Secret) >= 3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Serialize) >= 2.0.0
Conflicts:      php-pear(%{pear_channel}/Horde_Serialize) >= 3.0.0
Requires:       php-pear(%{pear_channel}/Horde_SessionHandler) >= 2.0.0
Conflicts:      php-pear(%{pear_channel}/Horde_SessionHandler) >= 3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Share) >= 2.0.0
Conflicts:      php-pear(%{pear_channel}/Horde_Share) >= 3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Support) >= 2.0.0
Conflicts:      php-pear(%{pear_channel}/Horde_Support) >= 3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Template) >= 2.0.0
Conflicts:      php-pear(%{pear_channel}/Horde_Template) >= 3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Token) >= 2.0.0
Conflicts:      php-pear(%{pear_channel}/Horde_Token) >= 3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Text_Filter) >= 2.0.0
Conflicts:      php-pear(%{pear_channel}/Horde_Text_Filter) >= 3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Text_Filter_Csstidy) >= 2.0.0
Conflicts:      php-pear(%{pear_channel}/Horde_Text_Filter_Csstidy) >= 3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Translation) >= 2.0.0
Conflicts:      php-pear(%{pear_channel}/Horde_Translation) >= 3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Url) >= 2.0.0
Conflicts:      php-pear(%{pear_channel}/Horde_Url) >= 3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Util) >= 2.0.0
Conflicts:      php-pear(%{pear_channel}/Horde_Util) >= 3.0.0
Requires:       php-pear(%{pear_channel}/Horde_View) >= 2.0.0
Conflicts:      php-pear(%{pear_channel}/Horde_View) >= 3.0.0
# Optional
Requires:       php-pecl(LZF)
Requires:       php-pear(Net_DNS2)
Requires:       php-pear(%{pear_channel}/Horde_Crypt) >= 2.0.0
Conflicts:      php-pear(%{pear_channel}/Horde_Crypt) >= 3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Form) >= 2.0.0
Conflicts:      php-pear(%{pear_channel}/Horde_Form) >= 3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Http) >= 2.0.0
Conflicts:      php-pear(%{pear_channel}/Horde_Http) >= 3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Icalendar) >= 2.0.0
Conflicts:      php-pear(%{pear_channel}/Horde_Icalendar) >= 3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Image) >= 2.0.0
Conflicts:      php-pear(%{pear_channel}/Horde_Image) >= 3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Imap_Client) >= 2.0.0
Conflicts:      php-pear(%{pear_channel}/Horde_Imap_Client) >= 3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Ldap) >= 2.0.0
Conflicts:      php-pear(%{pear_channel}/Horde_Ldap) >= 3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Mail) >= 2.0.0
Conflicts:      php-pear(%{pear_channel}/Horde_Mail) >= 3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Nls) >= 2.0.0
Conflicts:      php-pear(%{pear_channel}/Horde_Nls) >= 3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Routes) >= 2.0.0
Conflicts:      php-pear(%{pear_channel}/Horde_Routes) >= 3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Tree) >= 2.0.0
Conflicts:      php-pear(%{pear_channel}/Horde_Tree) >= 3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Vfs) >= 2.0.0
Conflicts:      php-pear(%{pear_channel}/Horde_Vfs) >= 3.0.0
# Optionnal: Horde_ActiveSync, Horde_Editor, Horde_ElasticSearch, Horde_Kolab_Server
#            Horde_Kolab_Session, Horde_Kolab_Storage
#            Horde_Oauth, Horde_Service_Twitter, Horde_SpellChecker
#            Text_CAPTCHA, Text_Figlet, Text_LanguageDetect

Provides:       php-pear(%{pear_channel}/%{pear_name}) = %{version}


%description
These classes provide the core functionality of the Horde Application
Framework.


%prep
%setup -q -c
cd %{pear_name}-%{version}

# Don't install .po and .pot files
# Remove checksum for .mo, as we regenerate them
sed -e '/%{pear_name}.po/d' \
    -e '/LICENSE/s/role="horde"/role="doc"/' \
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
cd %{pear_name}-%{version}/test/$(echo %{pear_name} | sed -e s:_:/:g)
phpunit\
    -d include_path=%{buildroot}%{pear_phpdir}:.:%{pear_phpdir} \
    -d date.timezone=UTC \
    .


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
%{pear_phpdir}/Horde/Config
%{pear_phpdir}/Horde/Core
%{pear_phpdir}/Horde/Exception/*.php
%{pear_phpdir}/Horde/Registry
%{pear_phpdir}/Horde/Script
%{pear_phpdir}/Horde/Session
%{pear_phpdir}/Horde/Themes
%{pear_phpdir}/Horde/*.php
%{pear_phpdir}/Horde.php
%{pear_testdir}/%{pear_name}
# own locales (non standard) directories, .mo own by find_lang
%dir %{pear_datadir}/%{pear_name}
%dir %{pear_datadir}/%{pear_name}/locale
%{pear_datadir}/%{pear_name}/migration
# Web files
%dir %{pear_hordedir}/js
%{pear_hordedir}/js/date
%{pear_hordedir}/js/jquery.mobile
%{pear_hordedir}/js/map
%{pear_hordedir}/js/scriptaculous
%{pear_hordedir}/js/*js


%changelog
* Fri Dec 28 2012 Remi Collet <RPMS@FamilleCollet.com> - 2.1.3-1
- Update to 2.1.3 for remi repo

* Fri Dec 21 2012 Remi Collet <RPMS@FamilleCollet.com> - 2.1.2-1
- Update to 2.1.2 for remi repo

* Thu Dec 13 2012 Remi Collet <RPMS@FamilleCollet.com> - 2.1.1-1
- Update to 2.1.1 for remi repo

* Sat Dec  8 2012 Remi Collet <RPMS@FamilleCollet.com> - 2.1.0-1
- Update to 2.1.0 for remi repo

* Tue Nov 27 2012 Remi Collet <RPMS@FamilleCollet.com> - 2.0.4-1
- Update to 2.0.4 for remi repo

* Thu Nov 22 2012 Remi Collet <RPMS@FamilleCollet.com> - 2.0.3-1
- Update to 2.0.3 for remi repo

* Wed Nov  7 2012 Remi Collet <RPMS@FamilleCollet.com> - 2.0.2-1
- Update to 2.0.2 for remi repo

* Sun Nov  4 2012 Remi Collet <RPMS@FamilleCollet.com> - 2.0.1-1
- Initial package
