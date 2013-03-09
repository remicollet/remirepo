%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name %(echo %{name} | sed -e 's/^php-dropbox-php-//' -e 's/-/_/g')
%global channelname pear.dropbox-php.com

Name:           php-dropbox-php-Dropbox
Version:        1.0.0
Release:        4%{?dist}
Summary:        Library for integrating dropbox with PHP

Group:          Development/Libraries
License:        MIT
URL:            http://www.dropbox-php.com/
Source0:        http://%{channelname}/get/%{pear_name}-%{version}.tgz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php-pear(PEAR)
BuildRequires:  php-channel(%{channelname})

Requires:       php-pear(PEAR)
Requires:       php-channel(%{channelname})
Requires(post): %{__pear}
Requires(postun): %{__pear}

Requires:       php-spl php-curl php-date php-hash
Requires:       php-json php-pcre

Requires:       php-pear(HTTP_OAuth)
Requires:       php-pecl(oauth)

Provides:       php-pear(%{channelname}/%{pear_name}) = %{version}

%description
This PHP library allows you to easily integrate dropbox with PHP.
The library makes use of OAuth.

Optional Dependencies:
Zend framework: Zend_{Oauth,Json,Uri} for OAuth/Zend back-end
Wordpress: WP_Http for OAuth/Wordpress back-end


%prep
%setup -q -c

mv package.xml %{pear_name}-%{version}/%{name}.xml


%build
# nothing

%install
cd %{pear_name}-%{version}
rm -rf %{buildroot} docdir
%{__pear} install --nodeps --packagingroot %{buildroot} %{name}.xml

# Clean up unnecessary files
rm -rf %{buildroot}%{pear_metadir}/.??*

# Install XML package description
mkdir -p %{buildroot}%{pear_xmldir}
install -pm 644 %{name}.xml %{buildroot}%{pear_xmldir}


%post
%{__pear} install --nodeps --soft --force --register-only \
    %{pear_xmldir}/%{name}.xml >/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    %{__pear} uninstall --nodeps --ignore-errors --register-only \
        %{channelname}/%{pear_name} >/dev/null || :
fi


%files
%defattr(-,root,root,-)
%doc %{pear_docdir}/%{pear_name}
%{pear_xmldir}/%{name}.xml
%{pear_phpdir}/%{pear_name}


%changelog
* Sat Mar 09 2013 Remi Collet <rpms@famillecollet.com> - 1.0.0-4
- backport for remi repo

* Thu Mar 07 2013 Gregor Tätzner <brummbq@fedoraproject.org> - 1.0.0-4
- require php-pecl(oauth) instead of php-oauth
- add note about optional dep to wordpress and zend

* Wed Mar 06 2013 Gregor Tätzner <brummbq@fedoraproject.org> - 1.0.0-3
- require HTTP_OAuth
- get source from pear host http://pear.dropbox-php.com

* Wed Feb 27 2013 Gregor Tätzner <brummbq@fedoraproject.org> - 1.0.0-2
- rename to php-dropbox-php-Dropbox

* Tue Feb 19 2013 Gregor Tätzner <brummbq@fedoraproject.org> - 1.0.0-1
- Initial package
