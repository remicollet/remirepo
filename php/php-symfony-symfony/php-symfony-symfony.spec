%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name symfony

Name:           php-symfony-symfony
Version:        1.4.20
Release:        1%{?dist}
Summary:        Open-Source PHP Web Framework

Group:          Development/Libraries
License:        MIT
URL:            http://www.symfony-project.org/
Source0:        http://pear.symfony-project.com//get/symfony-%{version}.tgz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source1:        symfony.README.fedora

BuildArch:      noarch
BuildRequires:  php-channel(pear.symfony-project.com)
BuildRequires:  php-pear(PEAR)

Requires:       php-common >= 5.2.4
Requires:       php-dom
Requires:       php-simplexml
Requires:       php-pear(PEAR)
Requires:       php-channel(pear.symfony-project.com)
Requires:       php-doctrine-Doctrine >= 1.2.4
Requires:       php-pear-phing >= 1.0.0
#Requires:       php-pear-propel_generator >= 1.4.0
#Requires:       php-pear-propel_runtime >= 1.4.0
Requires:       php-pear(pear.swiftmailer.org/Swift) >= 4.0.5
Requires(post): %{__pear}
Requires(postun): %{__pear}

Provides:       php-pear(pear.symfony-project.com/%{pear_name}) = %{version}


%description

Symfony is a complete framework designed to optimize the development of web
applications by way of several key features. For starters, it separates a web
application's business rules, server logic, and presentation views.
It contains numerous tools and classes aimed at shortening the development time
of a complex web application. Additionally, it automates common tasks so that
the developer can focus entirely on the specifics of an application.
The end result of these advantages means there is no need to reinvent the wheel
every time a new web application is built!

%prep
%setup -q -c

cp %{SOURCE1} README.fedora

cd %{pear_name}-%{version}

# Remove bundled libraries
sed -e '/vendor\/swiftmailer/d'   \
    -e '/lib\/vendor\/doctrine/d' \
    -e '/lib\/vendor\/phing/d'    \
    -e '/lib\/vendor\/propel/d'   \
    -e '/LICENSE.swiftmailer/d'   \
    -e '/LICENSE.phing/d'         \
    -e '/LICENSE.Propel/d'        \
    ../package.xml >%{name}.xml


%build
cd %{pear_name}-%{version}
# Empty build section, most likely nothing required.


%install
cd %{pear_name}-%{version}
%{__pear} install --nodeps --packagingroot %{buildroot} %{name}.xml

sed -i -e "s|dirname.*/lib/vendor/doctrine|'%{pear_phpdir}|" \
    %{buildroot}%{pear_phpdir}/%{pear_name}/plugins/sfDoctrinePlugin/config/sfDoctrinePluginConfiguration.class.php

sed -i -e "s|sfConfig::get.*sf_symfony_lib_dir.*/vendor/swiftmailer|'%{pear_phpdir}/Swift|" \
    %{buildroot}%{pear_phpdir}/%{pear_name}/mailer/sfMailer.class.php \
    %{buildroot}%{pear_phpdir}/%{pear_name}/task/sfCommandApplicationTask.class.php

# Clean up unnecessary files
rm -rf %{buildroot}%{pear_metadir}/.??*

find %{buildroot}%{pear_phpdir} -name .sf -print0 | xargs -0 rm -fr


# change dos files to unix
for file in `find -name LICENSE.ICU`; do
 sed "s|\r||g" $file > $file.new && \
 touch -r $file $file.new && \
 mv $file.new $file
done

for file in \
  %{pear_phpdir}/%{pear_name}/plugins/sfPropelPlugin/test/functional/fixtures/symfony \
  %{pear_phpdir}/%{pear_name}/plugins/sfDoctrinePlugin/test/functional/fixtures/symfony \
  %{pear_phpdir}/%{pear_name}/task/generator/skeleton/project/symfony \
  %{pear_datadir}/%{pear_name}/bin/create_sandbox.sh \
  ; do
   chmod a+x %{buildroot}/$file
done


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
        %{pear_name} >/dev/null || :
fi


%files
%defattr(-,root,root,-)
%doc README.fedora
%doc %{pear_docdir}/%{pear_name}
%{pear_xmldir}/%{name}.xml
%{pear_datadir}/%{pear_name}
%{pear_phpdir}/%{pear_name}
%{_bindir}/symfony


%changelog
* Mon Nov 26 2012 Remi Collet <RPMS@FamilleCollet.com> - 1.4.20-1
- upstream 1.4.20 (security fix), rebuild for remi repository
- remove bundled lib from package.xml
- move doc to /usr/share/doc/pear
- rename symfony.xml to php-symfony-symfony.xml

* Sat Jun 09 2012 Remi Collet <RPMS@FamilleCollet.com> - 1.4.18-1
- upstream 1.4.18 (security fix), rebuild for remi repository

* Mon Jun  4 2012 Christof Damian <christof@damian.net> - 1.4.18-1
- upstream 1.4.18 (security fix)

* Thu Mar  8 2012 Christof Damian <christof@damian.net> - 1.4.17-2
- fix doctrine path

* Thu Mar  8 2012 Christof Damian <christof@damian.net> - 1.4.17-1
- upstream 1.4.17

* Mon Feb 07 2011 Remi Collet <RPMS@FamilleCollet.com> - 1.4.8-2
- rebuild for remi repository

* Fri Jan 14 2011 Christof Damian <christof@damian.net> - 1.4.8-2
- fix timezone warning
- change quoting in sed
- update tar file and url

* Tue Nov 23 2010 Christof Damian <christof@damian.net> - 1.4.8-1
- upstream 1.4.8

* Fri May 14 2010 Christof Damian <christof@damian.net> - 1.4.4-1
- upstream 1.4.4

* Thu Feb 25 2010 Christof Damian <christof@damian.net> - 1.4.3-1
- upstream 1.4.3

* Sat Feb 20 2010 Christof Damian <christof@damian.net> - 1.4.2-1
- upstream 1.4.2
- add requires for dom and simplexml
- use sed instead of patches to fix paths

* Tue Dec 8 2009 Christof Damian <christof@damian.net> - 1.4.1-1
- upstream 1.4.1

* Tue Dec 1 2009 Christof Damian <christof@damian.net> 1.4.0-1
- upstream 1.4.0

* Mon Sep 28 2009 Christof Damian <christof@damian.net> 1.2.9-1
- upstream 1.2.9

* Thu Sep 24 2009 Christof Damian <christof@damian.net> 1.2.8-4
- fix provide

* Wed Sep 2 2009 Christof Damian <christof@damian.net> 1.2.8-3
- added README.fedora detailing the changes

* Fri Aug 21 2009 Christof Damian <christof@damian.net> 1.2.8-2
- removed bundled libs
- added patch for doctrine 1.1

* Tue Aug 11 2009 Christof Damian <christof@damian.net> 1.2.8-1
- initial rpm
