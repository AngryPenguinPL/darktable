# Keep libraries private
%if %{_use_internal_dependency_generator}
%define __noautoprov '(.*)\\.so(.*)'
%define __noautoreq 'libdarktable\\.so(.*)'
%endif

Summary:	Utility to organize and develop raw images
Name:		darktable
Version:	2.4.3
Release:	1
Group:		Graphics
License:	GPLv3+
Url:		http://www.darktable.org
Source0:	https://github.com/darktable-org/darktable/releases/download/release-%{version}/%{name}-%{version}.tar.xz
Source100:	%{name}.rpmlintrc
BuildRequires:	cmake
BuildRequires:	desktop-file-utils
BuildRequires:	gettext
BuildRequires:	gnome-doc-utils
BuildRequires:	intltool
BuildRequires:	gettext-devel
BuildRequires:	gomp-devel
BuildRequires:	jpeg-devel
BuildRequires:	pkgconfig(cairo)
BuildRequires:	pkgconfig(colord)
BuildRequires:	pkgconfig(dbus-glib-1)
BuildRequires:	pkgconfig(exiv2)
BuildRequires:	pkgconfig(flickcurl)
BuildRequires:	pkgconfig(gconf-2.0)
BuildRequires:	pkgconfig(gnome-keyring-1)
BuildRequires:	pkgconfig(GraphicsMagick)
BuildRequires:	pkgconfig(gtk+-2.0)
BuildRequires:	pkgconfig(json-glib-1.0)
BuildRequires:	pkgconfig(lcms2)
BuildRequires:	pkgconfig(lensfun)
BuildRequires:	pkgconfig(libcurl)
BuildRequires:	pkgconfig(libglade-2.0)
BuildRequires:	pkgconfig(libgphoto2)
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(librsvg-2.0)
BuildRequires:	pkgconfig(libtiff-4)
BuildRequires:	pkgconfig(OpenEXR)
BuildRequires:	pkgconfig(sqlite3)
BuildRequires:	pkgconfig(zlib)

%description
Darktable is an open source photography workflow application and RAW developer.
A virtual lighttable and darkroom for photographers. It manages your digital
negatives in a database, lets you view them through a zoomable lighttable
and enables you to develop raw images and enhance them.

%files -f %{name}.lang
%doc doc/README doc/AUTHORS doc/LICENSE doc/TRANSLATORS
%{_bindir}/%{name}*
%{_libdir}/%{name}
%{_datadir}/appdata/darktable.appdata.xml
%{_datadir}/applications/%{name}.desktop
%{_datadir}/%{name}
%{_iconsdir}/hicolor/*/apps/%{name}*
%{_mandir}/man1/%{name}*

#----------------------------------------------------------------------------

%prep
%setup -q

%build
export CC=gcc
export CXX=g++
%cmake \
	-DCMAKE_LIBRARY_PATH:PATH=%{_libdir} \
	-DDONT_INSTALL_GCONF_SCHEMAS:BOOLEAN=ON \
	-DCMAKE_BUILD_TYPE:STRING=Release \
	-DBINARY_PACKAGE_BUILD=1 \
	-DPROJECT_VERSION:STRING="%{name}-%{EVRD}" \
	-DINSTALL_IOP_EXPERIMENTAL:BOOLEAN=ON

%make

%install
export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1

%makeinstall_std -C build

%find_lang %{name}

desktop-file-validate %{buildroot}/%{_datadir}/applications/%{name}.desktop
rm -rf %{buildroot}%{_datadir}/doc/%{name}

