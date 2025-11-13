import paramiko

def execute_command(client, command):
    """Ejecuta un comando en el cliente SSH y devuelve la salida estándar."""
    stdin, stdout, stderr = client.exec_command(command)
    
    output = stdout.read().decode()
    errors = stderr.read().decode()
    
    if errors:
        # Imprime el error si existe
        print(f"⚠️ Error al ejecutar el comando '{command}': \n{errors}")
        
    return output

def connect_ssh(hostname, username, password):
    """
    Establece y devuelve un cliente SSH conectado.
    Maneja excepciones de conexión y autenticación.
    """
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy()) 

    try:
        ssh_client.connect(
            hostname=hostname, 
            username=username, 
            password=password
        )
        print(f"✅ Conexión establecida con {hostname}")
        return ssh_client
        
    except paramiko.AuthenticationException:
        print("❌ Fallo de autenticación. Verifica usuario/contraseña.")
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
    
    return None # Retorna None si la conexión falla

# Nota: La función execute_command no necesita el cliente en este archivo.
# Se le pasará cuando se use en el archivo principal.