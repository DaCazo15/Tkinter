import subprocess, re, tempfile, os

class WiFiManager:
    @staticmethod
    def get_available_networks():
        """Obtiene la lista de redes WiFi disponibles."""
        try:
            result = subprocess.run(
                ['netsh', 'wlan', 'show', 'networks'],
                capture_output=True,
                text=True,
                encoding='latin-1'
            )
            if result.returncode != 0:
                raise Exception("No se pudo obtener la lista de redes WiFi.")
            
            networks = re.findall(r'SSID\s*\d+\s*:\s*(.+)', result.stdout)
            return networks if networks else []
            
        except Exception as e:
            raise Exception(f"Error al obtener redes WiFi: {str(e)}")

    @staticmethod
    def connect_to_network(ssid, password):
        """Conecta a una red WiFi con el SSID y contraseña proporcionados."""
        try:
            # Crear perfil XML
            profile = WiFiManager._generate_profile_xml(ssid, password)
            profile_path = os.path.join(tempfile.gettempdir(), f"{ssid}.xml")
            
            # Guardar perfil temporal
            with open(profile_path, "w") as f:
                f.write(profile)
            
            # Agregar perfil
            add_result = subprocess.run(
                ['netsh', 'wlan', 'add', 'profile', f'filename={profile_path}'],
                capture_output=True,
                text=True,
                shell=True
            )
            if add_result.returncode != 0:
                raise Exception(f"Error al agregar perfil: {add_result.stderr.strip()}")
            
            # Conectar
            connect_result = subprocess.run(
                ['netsh', 'wlan', 'connect', f'name={ssid}'],
                capture_output=True,
                text=True,
                shell=True
            )
            if connect_result.returncode != 0:
                raise Exception(f"Error al conectar: {connect_result.stderr.strip()}")
            
            return True
        except Exception as e:
            raise e
        finally:
            try:
                if os.path.exists(profile_path):
                    os.remove(profile_path)
            except:
                pass

    @staticmethod
    def _generate_profile_xml(ssid, password):
        """Genera el XML del perfil WiFi."""
        ssid_escaped = ssid.replace('"', '\\"')
        return f"""<?xml version="1.0"?>
<WLANProfile xmlns="http://www.microsoft.com/networking/WLAN/profile/v1">
    <name>{ssid_escaped}</name>
    <SSIDConfig>
        <SSID>
            <name>{ssid_escaped}</name>
        </SSID>
    </SSIDConfig>
    <connectionType>ESS</connectionType>
    <connectionMode>auto</connectionMode>
    <MSM>
        <security>
            <authEncryption>
                <authentication>WPA2PSK</authentication>
                <encryption>AES</encryption>
                <useOneX>false</useOneX>
            </authEncryption>
            <sharedKey>
                <keyType>passPhrase</keyType>
                <protected>false</protected>
                <keyMaterial>{password}</keyMaterial>
            </sharedKey>
        </security>
    </MSM>
</WLANProfile>"""