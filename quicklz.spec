#
# Conditional build:
%bcond_without	static_libs	# don't build static libraries

Summary:	Fast compression library
Name:		quicklz
Version:	1.5.0
Release:	1
License:	GPL v1, GPL v2, GPL v3
Group:		Libraries
Source0:	http://www.quicklz.com/%{name}.c
# Source0-md5:	76c8722e413ee99aff2ded50ced8b666
Source1:	http://www.quicklz.com/%{name}.h
# Source1-md5:	35e9b485b15c447f8306654ed0d584de
URL:		http://www.quicklz.com/
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		abi    0

%description
QuickLZ is the world's fastest compression library, reaching 308
Mbyte/s per core.

%package devel
Summary:	Header files for %{name} library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for %{name} library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki %{name}.

%package static
Summary:	Static %{name} library
Summary(pl.UTF-8):	Statyczna biblioteka %{name}
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static %{name} library.

%description static -l pl.UTF-8
Statyczna biblioteka %{name}.

%prep
%setup -qcT
cp -p %{S:0} %{S:1} .

%build
%{__cc} %{rpmcflags} -fPIC -c quicklz.c  -o quicklz.o

# Build the shared library
%{__cc} %{rpmcflags} -fPIC %{rpmldflags} -shared -Wl,-soname -Wl,lib%{name}.so.%{abi} -o lib%{name}.so.%{abi} quicklz.o

# Build the static library
%if %{with static_libs}
ar rcs lib%{name}.a quicklz.o
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir},%{_includedir}}

install -p lib%{name}.so.%{abi} $RPM_BUILD_ROOT%{_libdir}/lib%{name}.so.%{abi}.0.0
ln -s lib%{name}.so.%{abi} $RPM_BUILD_ROOT%{_libdir}/lib%{name}.so
/sbin/ldconfig -n $RPM_BUILD_ROOT%{_libdir}
cp -p %{name}.h $RPM_BUILD_ROOT%{_includedir}

%if %{with static_libs}
cp -p lib%{name}.a $RPM_BUILD_ROOT%{_libdir}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libquicklz.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libquicklz.so.0

%files devel
%defattr(644,root,root,755)
%{_includedir}/quicklz.h
%{_libdir}/libquicklz.so

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libquicklz.a
%endif
