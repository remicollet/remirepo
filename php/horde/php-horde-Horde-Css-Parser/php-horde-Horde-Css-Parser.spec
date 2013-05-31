%{!?pear_metadir: %global pear_metadir %{pear_phpdir}}
%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name Horde_Css_Parser

Name:           php-horde-Horde-Css-Parser
Version:        1.0.0
Release:        1%{?dist}
Summary:        Horde CSS Parser

Group:          Development/Libraries
License:        LGPL-2.1
URL:            http://pear.horde.org/package/Horde_Css_Parser
Source0:        http://pear.horde.org/get/%{pear_name}-%{version}.tgz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php-pear(PEAR)

Requires(post): %{__pear}
Requires(postun): %{__pear}
Requires:       php-pear(PEAR)
Provides:       php-pear(pear.horde.org/Horde_Css_Parser) = %{version}
BuildRequires:  php-channel(pear.horde.org)
Requires:       php-channel(pear.horde.org)

%description
This package provides access to the Sabberworm CSS Parser from within the
Horde framework.

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
%{pear_phpdir}/Horde/Css/Parser.php
%{pear_phpdir}/Sabberworm/CSS/CSSList/AtRuleBlockList.php
%{pear_phpdir}/Sabberworm/CSS/CSSList/CSSBlockList.php
%{pear_phpdir}/Sabberworm/CSS/CSSList/CSSList.php
%{pear_phpdir}/Sabberworm/CSS/CSSList/Document.php
%{pear_phpdir}/Sabberworm/CSS/CSSList/KeyFrame.php
%{pear_phpdir}/Sabberworm/CSS/CSSList/MediaQuery.php
%{pear_phpdir}/Sabberworm/CSS/Parsing/UnexpectedTokenException.php
%{pear_phpdir}/Sabberworm/CSS/Property/AtRule.php
%{pear_phpdir}/Sabberworm/CSS/Property/Charset.php
%{pear_phpdir}/Sabberworm/CSS/Property/CSSNamespace.php
%{pear_phpdir}/Sabberworm/CSS/Property/Import.php
%{pear_phpdir}/Sabberworm/CSS/Property/Selector.php
%{pear_phpdir}/Sabberworm/CSS/Rule/Rule.php
%{pear_phpdir}/Sabberworm/CSS/RuleSet/AtRuleSet.php
%{pear_phpdir}/Sabberworm/CSS/RuleSet/DeclarationBlock.php
%{pear_phpdir}/Sabberworm/CSS/RuleSet/RuleSet.php
%{pear_phpdir}/Sabberworm/CSS/Value/Color.php
%{pear_phpdir}/Sabberworm/CSS/Value/CSSFunction.php
%{pear_phpdir}/Sabberworm/CSS/Value/PrimitiveValue.php
%{pear_phpdir}/Sabberworm/CSS/Value/RuleValueList.php
%{pear_phpdir}/Sabberworm/CSS/Value/Size.php
%{pear_phpdir}/Sabberworm/CSS/Value/String.php
%{pear_phpdir}/Sabberworm/CSS/Value/URL.php
%{pear_phpdir}/Sabberworm/CSS/Value/Value.php
%{pear_phpdir}/Sabberworm/CSS/Value/ValueList.php
%{pear_phpdir}/Sabberworm/CSS/Parser.php
%{pear_phpdir}/Sabberworm/CSS/Settings.php




%changelog
