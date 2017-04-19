%define aversion 1.3.4
%define arelease X-BUILD-NUMBER_centos6
%define actversion %(echo %{aversion}|sed -e "s/-.*$//g")
%define subvers %(echo %{aversion}|awk "/-/"|sed -e "s/^.*-//"|awk '{print "0." $1 "."}')
%define actrelease %(echo %{subvers}%{arelease}|sed -e "s/-/_/g")

#Workaround for 64 bit CPUs
%define _lib lib

###################################################################
#
#  The Preamble
#  information that is displayed when users request info
#
###################################################################
Summary: OpenR2 is a library that implements the MFC/R2 telephony signaling protocol over E1 lines
Name: libopenr2
Version: 1.3.3
Release: 1%{dist}
License: LGPL
Group: Utilities/System
Source: https://storage.googleapis.com/google-code-archive-downloads/v2/code.google.com/openr2/openr2-%{version}.tar.gz
Patch0: unavailable_dnis.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-root
URL: http://www.libopenr2.org
Packager: Nethesis <info@nethesis.it>
Requires: dahdi-linux
BuildRequires: dahdi-linux-devel
#
# Other tags not used
#
#Distribution:
#Icon:
#Provides:
#Conflicts:
#Serial:
#Requires:
#AutoReqProv:
#ExcludeArch:

%description
OpenR2 is a library that implements the MFC/R2 telephony signaling protocol over E1 lines

%package devel
Summary: libopenr2 libraries and header files for libopenr2 development
Group: Development/Libraries
Requires: %{name} = %{actversion}-%{release}

%description devel
The static libraries and header files needed for building additional plugins/modules

%package doc
Summary: Documentation files for OpenR2
Group: Development/Libraries
Requires: %{name} = %{actversion}

%description doc
The Documentation files for OpenR2

###################################################################
#
#  The Prep Section
#  If stuff needs to be done before building, this is the section
#  Use shell scripts to do stuff like uncompress and cd into source dir
#  %setup macro - cleans old build trees, uncompress and extracts original source
#
###################################################################
%prep
%setup -n openr2-%{version}
%patch0 -p0

###################################################################
#
#  The Build Section
#  Use shell scripts and do stuff that makes the build happen, i.e. make
#
###################################################################
%build
./configure --prefix=%{_prefix} --sysconfdir=%{_sysconfdir}
make

###################################################################
#
#  The Install Section
#  Use shell scripts and perform the install, like 'make install',
#  but can also be shell commands, i.e. cp, mv, install, etc..
#
###################################################################
%install
make DESTDIR=$RPM_BUILD_ROOT install
# HACK to ensure documentation ends up in the right place
#pushd .
#cd $RPM_BUILD_ROOT
#cd usr
#mkdir share
#mv man share/.
#popd

###################################################################
#
#  Install and Uninstall
#  This section can have scripts that are run either before/after
#  an install process, or before/after an uninstall process
#  %pre - executes prior to the installation of a package
#  %post - executes after the package is installed
#  %preun - executes prior to the uninstallation of a package
#  %postun - executes after the uninstallation of a package
#
###################################################################
%post
ldconfig

###################################################################
#
#  Verify
#
###################################################################
%verifyscript

###################################################################
#
#  Clean
#
###################################################################
%clean
cd $RPM_BUILD_DIR
%{__rm} -rf %{name}-%{version}
%{__rm} -rf /var/log/%{name}-sources-%{version}-%{release}.make.err
%{__rm} -rf $RPM_BUILD_ROOT

###################################################################
#
#  File List
#
###################################################################
%files
#
#  Module List
#
%defattr(-, root, root)
%{_bindir}/r2test
%{_bindir}/r2dtmf_detect
%{_sysconfdir}/r2proto.conf
%{_sysconfdir}/r2test.conf
%{_libdir}/libopenr2.so
%{_libdir}/libopenr2.so.*

%files devel
#
#  Header Files
#
%defattr(-, root, root)
%{_includedir}/openr2.h
%{_includedir}/openr2/*
%{_libdir}/libopenr2.a
%{_libdir}/libopenr2.la

%files doc
%defattr(-, root, root)
#
#  Manual Pages
#
%{_mandir}/man5/r2test.conf.5.gz
%{_mandir}/man8/r2test.8.gz
