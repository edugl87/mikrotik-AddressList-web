# app.py

import configparser
from flask import Flask, render_template # <- Importamos render_template
from ssh_utils import connect_ssh, execute_command 

app = Flask(__name__)

# --- Lectura de Credenciales ---
config = configparser.ConfigParser()
try:
    config.read('config.ini')
    HOSTNAME = config['mikrotik_router']['hostname']
    USERNAME = config['mikrotik_router']['username']
    PASSWORD = config['mikrotik_router']['password']
    CONFIG_LOADED = True
except Exception as e:
    print(f"ERROR: No se pudo cargar la configuración de config.ini: {e}")
    CONFIG_LOADED = False
# ------------------------------

@app.route('/')
def index():
    # Variables a pasar a la plantilla HTML
    template_vars = {
        'title': 'Mikrotik Status',
        'status': 'error',
        'message': 'Error desconocido.',
        'command': ':put [interface print as-value]',
        'interfaces_output': None
    }
    
    if not CONFIG_LOADED:
        template_vars['title'] = "❌ Error de Configuración"
        template_vars['message'] = "No se pudieron cargar las credenciales de 'config.ini'."
        return render_template('index.html', **template_vars), 500

    client = None
    
    try:
        # 1. CONEXIÓN
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
        
        # El HTML espera la salida ya formateada, reemplazamos '\n' por saltos de línea HTML
        template_vars['interfaces_output'] = interfaces_output.strip() 

    except Exception as e:
        template_vars['title'] = "❌ Error Inesperado"
        template_vars['message'] = f"Ocurrió un error al ejecutar comandos: {e}"
        
    finally:
        # 4. CIERRE de la conexión
        if client:
            client.close()
            
    # <- Renderizamos el archivo index.html
    return render_template('index.html', **template_vars)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')