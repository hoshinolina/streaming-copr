Name:           proaudio-setup
Version:        0.1.3
Release:        %autorelease
Summary:        Automatic proaudio system tuning

License:        MIT
URL:            https://github.com/hoshinolina/proaudio-setup
Source0:        %{url}/archive/%{version_no_tilde}/proaudio-setup-%{version_no_tilde}.tar.gz

BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  systemd

Requires:       realtime-setup

%description
Automatic system tuning for low-latency proaudio.

Installing this package will automatically configure
the kernel and IRQs to reduce IRQ latency and support
smaller audio buffer sizes without drop-outs.

%prep
%autosetup -p1 -n %{name}-%{version}


%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel

for i in support/*; do
    sed 's,%%PREFIX%%,%{_prefix},g' "$i" > "${i%%.in}"
done

echo "enable %{name}.service" > support/50-%{name}.preset


%install
%pyproject_install
%pyproject_save_files -l proaudio_setup

install -Dm 644 -t %{buildroot}%{_unitdir} support/*.service
install -Dm 644 -t %{buildroot}%{_udevrulesdir} support/*.rules
install -Dm 644 -t %{buildroot}%{_presetdir} support/*.preset
install -Dm 755 -t %{buildroot}%{_systemd_util_dir}/system-sleep support/*.sleep


%post
%systemd_post %{name}.service
%{_bindir}/%{name} trigger postin
:


%preun
%systemd_preun %{name}.service
if [ $1 -eq 0 ] ; then
    %{_bindir}/%{name} trigger preun
fi
:

%postun
%systemd_postun_with_restart %{name}.service


%files -f %{pyproject_files}
%doc README.md
%{_bindir}/%{name}
%{_unitdir}/%{name}.service
%{_systemd_util_dir}/system-sleep/%{name}.sleep
%{_udevrulesdir}/80-%{name}.rules
%{_presetdir}/50-%{name}.preset


%changelog
%autochangelog
