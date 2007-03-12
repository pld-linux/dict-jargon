%define		dictname jargon
Summary:	The On-Line Hacker Jargon File dictionary for dictd
Summary(pl):	S³ownik Hacker Jargon dla dictd
Name:		dict-%{dictname}
Version:	4.4.7
Release:	3
License:	GPL
Group:		Applications/Dictionaries
# Source0:	http://www.tuxedo.org/~esr/jargon/jarg433.gz
Source0:	http://atos.wmid.amu.edu.pl/~undefine/jarg433.gz
# Source0-md5:	dcfee414bc8576e9d6eab9b2980226a0
URL:		http://www.dict.org/
BuildRequires:	dictfmt
BuildRequires:	dictzip
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	%{_sysconfdir}/dictd
Requires:	dictd
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package contains The On-Line Hacker Jargon File, version %{version},
formatted for use by the dictionary server in the dictd package.

%description -l pl
Ten pakiet zawiera s³ownik The On-Line Hacker Jargon File w wersji
%{version}, sformatowany do u¿ytku z serwerem s³ownika dictd.

%prep
%setup -q -c -T
%{__gzip} -dc %{SOURCE0} > jarg433

%build
dictfmt -j -u http://www.jargon.org/ -s "Jargon File (4.3.3, 20 Sep 2002)" %{dictname} < jarg433
dictzip %{dictname}.dict

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_datadir}/dictd,%{_sysconfdir}/dictd}

dictprefix=%{_datadir}/dictd/%{dictname}
echo "# The On-Line Hacker Jargon File dictionary
database %{dictname} {
	data  \"$dictprefix.dict.dz\"
	index \"$dictprefix.index\"
}" > $RPM_BUILD_ROOT%{_sysconfdir}/dictd/%{dictname}.dictconf
mv %{dictname}.* $RPM_BUILD_ROOT%{_datadir}/dictd

%clean
rm -rf $RPM_BUILD_ROOT

%post
%service -q dictd restart

%postun
if [ "$1" = 0 ]; then
	%service -q dictd restart
fi

%files
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/dictd/%{dictname}.dictconf
%{_datadir}/dictd/%{dictname}.*
