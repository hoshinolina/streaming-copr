%define libfunnel_commit 779586dab6ad396ce4a363204c8b9a18f473ca5d
%define pipewire_static_commit 5b36797b30574cab48097010e177faf32e8fe245
%define spout2_commit ad55c6a6032a109db2493cf2749a6c1901cfc4b1

%define installdir /opt/spout2pw

# LDFLAGS not compatible with mingw, besides this isn't really a "system" package.
%undefine _auto_set_build_flags

Name:           spout2pw-proton
Version:        0.2.3
Release:        %autorelease
Summary:        Spout2 to PipeWire bridge (build for Proton/Steam)

License:        LGPL-2.1-only AND MIT AND BSD-2-Clause
URL:            https://github.com/hoshinolina/spout2pw
Source0:        %{url}/archive/%{version_no_tilde}/spout2pw-%{version_no_tilde}.tar.gz
Source1:        https://github.com/hoshinolina/libfunnel/archive/%{libfunnel_commit}/libfunnel-%{libfunnel_commit}.tar.gz
Source2:        https://github.com/hoshinolina/pipewire-static/archive/%{pipewire_static_commit}/pipewire-static-%{pipewire_static_commit}.tar.gz
Source3:        https://github.com/leadedge/Spout2/archive/%{spout2_commit}/Spout2-%{spout2_commit}.tar.gz

BuildArch:      x86_64

BuildRequires:  gcc-c++
BuildRequires:  meson
BuildRequires:  ninja-build
BuildRequires:  dbus-devel
BuildRequires:  wine-devel
BuildRequires:  mingw64-gcc-c++
BuildRequires:  mesa-libgbm-devel
BuildRequires:  libdrm-devel
BuildRequires:  vulkan-loader-devel

%description
Wine/Proton add-on to bridge Windows Spout2 video
streams to PipeWire video streams.

This version is for use with third-party Proton/Wine
versions (non-Fedora), e.g. with Steam or umu-launcher.

%prep
%autosetup -C
tar -xf %{SOURCE1} -C subprojects/libfunnel --strip-components=1
tar -xf %{SOURCE2} -C subprojects/pipewire-static --strip-components=1
tar -xf %{SOURCE3} -C subprojects/spoutdxtoc/Spout2 --strip-components=1

%build
unset CFLAGS CXXFLAGS LDFLAGS
./build.sh

%install
mkdir -p %{buildroot}%{installdir}
cp -vr build/pkg/* %{buildroot}%{installdir}

%files
%license COPYING.txt
%doc README.md
%{installdir}

%changelog
%autochangelog
