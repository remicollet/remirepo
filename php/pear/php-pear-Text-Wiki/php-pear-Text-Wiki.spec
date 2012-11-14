%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name Text_Wiki

Name:           php-pear-Text-Wiki
Version:        1.2.1
Release:        1%{?dist}
Summary:        Transforms Wiki and BBCode markup into XHTML, LaTeX or plain text

Group:          Development/Libraries
License:        LGPLv2+
URL:            http://pear.php.net/package/Text_Wiki
Source0:        http://pear.php.net/get/%{pear_name}-%{version}.tgz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php-pear(PEAR)

Requires(post): %{__pear}
Requires(postun): %{__pear}
Requires:       php-pcre
Requires:       php-pear(PEAR)

Provides:       php-pear(%{pear_name}) = %{version}


%description
Transforms Wiki and BBCode markup into XHTML, LaTeX or plain text markup. 
This is the base engine for all of the Text_Wiki sub-classes

The text transformation is done in 2 steps.
The chosen parser uses markup rules to tokenize the tags and content.
Renderers output the tokens and text into the requested format.
The tokenized form replaces the tags by a protected byte value associated
to an index in an options table. This form shares up to 50 rules by all
parsers and renderers.

The package is intented for versatile transformers as well as converters.
Text_Wiki is delivered with its own parser, which is used by Yawiki or
Horde's Wicked and three basic renderers: XHTML , LaTeX and plain text.
Strong sanitizing of XHTML is default.

Parsers and Renderers exist for BBCode, Cowiki, Dokuwiki, Mediawiki
and Tikiwiki.

It is highly configurable and can be easily extended.


%prep
%setup -q -c
cd %{pear_name}-%{version}
mv ../package.xml %{name}.xml
 

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
%{pear_phpdir}/Text


%changelog
* Wed Nov 14 2012 Remi Collet <remi@fedoraproject.org> - 1.2.1-1
- Initial package
