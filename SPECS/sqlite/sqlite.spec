%define sourcever 3270200
Summary:        A portable, high level programming interface to various calling conventions
Name:           sqlite
Version:        3.27.2
Release:        5%{?dist}
License:        Public Domain
URL:            http://www.sqlite.org
Group:          System Environment/GeneralLibraries
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        http://sqlite.org/2018/%{name}-autoconf-%{sourcever}.tar.gz
%define sha1    sqlite=5f5750e3f39b7b60394a2fb6ddb2371f848670e6
Patch0:         CVE-2019-9936.patch
Patch1:         CVE-2019-9937.patch
Patch2:         CVE-2019-8457.patch
Patch3:         CVE-2019-16168.patch
Obsoletes:      sqlite-autoconf
Requires:       sqlite-libs = %{version}-%{release}
Provides:       sqlite3
%description
This package contains most of the static files that comprise the
www.sqlite.org website including all of the SQL Syntax and the
C/C++ interface specs and other miscellaneous documentation.

%package devel
Summary:        sqlite3 link library & header files
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
%description    devel
The sqlite devel package include the needed library link and
header files for development.

%package libs
Summary:        sqlite3 library
Group:          Libraries
Provides:       pkgconfig(sqlite3)
Obsoletes:      libsqlite
Obsoletes:      sqlite-autoconf
%description libs
The sqlite3 library.

%prep
%setup -q -n %{name}-autoconf-%{sourcever}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
%configure \
    CFLAGS="%{optflags}"                \
    CXXFLAGS="%{optflags}               \
    -DSQLITE_ENABLE_FTS3=1              \
    -DSQLITE_ENABLE_COLUMN_METADATA=1   \
    -DSQLITE_ENABLE_UNLOCK_NOTIFY=1     \
    -DSQLITE_SECURE_DELETE=1"           \
    --disable-static
make

%install
[ %{buildroot} != "/"] && rm -rf %{buildroot}/*
make DESTDIR=%{buildroot} install
install -D -m644 sqlite3.1 %{buildroot}/%{_mandir}/man1/sqlite3.1
find %{buildroot}/%{_libdir} -name '*.la' -delete
rm -rf %{buildroot}/%{_infodir}
%{_fixperms} %{buildroot}/*

%check
make %{?_smp_mflags} check

%post libs
/sbin/ldconfig

%postun libs
/sbin/ldconfig

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_bindir}/*
%{_mandir}/man1/*

%files devel
%defattr(-,root,root)
%{_libdir}/libsqlite3.so
%{_libdir}/libsqlite3.so.0
%{_libdir}/pkgconfig/*
%{_includedir}/*

%files libs
%defattr(-,root,root)
%{_libdir}/libsqlite3.so.0.8.6

%changelog
*   Fri Oct 18 2019 Michelle Wang <michellew@vmware.com> 3.27.2-5
-   Fix patch CVE-2019-16168.patch
*   Mon Sep 16 2019 Michelle Wang <michellew@vmware.com> 3.27.2-4
-   Add patch CVE-2019-16168.patch
*   Wed Jun 5 2019 Michelle Wang <michellew@vmware.com> 3.27.2-3
-   Add patch CVE-2019-8457.
*   Thu Apr 25 2019 Michelle Wang <michellew@vmware.com> 3.27.2-2
-   Add patch CVE-2019-9937.
*   Mon Apr 15 2019 Michelle Wang <michellew@vmware.com> 3.27.2-1
-   Upgrade to 3.27.2 and add patch CVE-2019-9936.
*   Sun Feb 3 2019 Michelle Wang <michellew@vmware.com> 3.26.0-1
-   Upgrade to 3.26.0 for a critical Vulnerability named 'Magallan'.
*   Fri Sep 21 2018 Srinidhi Rao <srinidhir@vmware.com> 3.25.1-1
-   Upgrade to version 3.25.1
*   Tue Feb 20 2018 Xiaolin Li <xiaolinl@vmware.com> 3.22.0-1
-   Upgrade to version 3.22.0
*   Fri Nov 10 2017 Xiaolin Li <xiaolinl@vmware.com> 3.21.0-1
-   Upgrade to version 3.21.0
*   Fri Jul 14 2017 Dheeraj Shetty <dheerajs@vmware.com> 3.19.3-1
-   Upgrading to version 3.19.0 and adding patch for CVE-2017-10989
*   Thu Jun 29 2017 Divya Thaluru <dthaluru@vmware.com> 3.18.0-2
-   Added obseletes for deprecated sqlite-autoconf package
*   Fri Apr 7 2017 Alexey Makhalov <amakhalov@vmware.com> 3.18.0-1
-   Version update
-   Package rename: sqlite-autoconf -> sqlite
*   Wed Nov 16 2016 Alexey Makhalov <amakhalov@vmware.com> 3.11.0-4
-   Added -devel and -libs subpackages
*   Tue Oct 04 2016 ChangLee <changlee@vmware.com> 3.11.0-3
-   Modified %check
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.11.0-2
-   GA - Bump release of all rpms
*   Tue Feb 23 2016 Xiaolin Li <xiaolinl@vmware.com> 3.11.0-1
-   Updated to version 3.11.0
*   Wed Feb 03 2016 Anish Swaminathan <anishs@vmware.com> - 3.8.3.1-2
-   Fix versioning
*   Tue Oct 7 2014 Divya Thaluru <dthaluru@vmware.com> 3080301-1
-   Initial build. First version
