# app.py

import os # Importar la librería para leer variables de entorno
from flask import Flask, render_template
# import configparser # Ya no es necesario si quitamos la lectura de config.ini
from ssh_utils import connect_ssh, execute_command 

app = Flask(__name__)

# --- Lectura de Credenciales DESDE EL ENTORNO ---
try:
    # Si la variable de entorno no existe, fallará aquí
    HOSTNAME = os.environ['MIKROTIK_HOST']
    USERNAME = os.environ['MIKROTIK_USER']
    PASSWORD = os.environ['MIKROTIK_PASS']
    CONFIG_LOADED = True
except KeyError as e:
    print(f"ERROR: Falta la variable de entorno: {e}")
    CONFIG_LOADED = False
# -----------------------------------------------

@app.route('/')
def index():
    template_vars = {
        'title': 'Mikrotik Status',
        'status': 'error',
        'message': 'Error desconocido.',
        'command': ':put [interface print as-value]',
        'interfaces_output': None
    }
    
    if not CONFIG_LOADED:
        template_vars['title'] = "❌ Error de Configuración"
        template_vars['message'] = "Faltan variables de entorno (MIKROTIK_HOST, MIKROTIK_USER, MIKROTIK_PASS)."
        # Si las credenciales no se cargan, devolvemos un error 500
        return render_template('index.html', **template_vars), 500 

    client = None
    
    try:
        # 1. CONEXIÓN (Usando las variables del entorno)
        client = connect_ssh(HOSTNAME, USERNAME, PASSWORD)
        
        if client is None:
            template_vars['title'] = "❌ Fallo de Conexión SSH"
            template_vars['message'] = "Verifica las credenciales o la accesibilidad del host."
            return render_template('index.html', **template_vars), 500

        # 2. EJECUCIÓN del comando
        interfaces_output = execute_command(client, template_vars['command'])
        
        # 3. Preparar los datos para la plantilla
        template_vars['status'] = 'success'
        template_vars['title'] = "✅ Estado de Interfaces de Mikrotik"
        template_vars['message'] = f"Conexión exitosa a {HOSTNAME}."
        template_vars['interfaces_output'] = interfaces_output.strip() 

    except Exception as e:
        template_vars['title'] = "❌ Error Inesperado"
        template_vars['message'] = f"Ocurrió un error al ejecutar comandos: {e}"
        
    finally:
        if client:
            client.close()
            
    return render_template('index.html', **template_vars)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)