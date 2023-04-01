import discord
import subprocess
from discord.ext import tasks, commands
import datetime
import os

# Configuración del bot de Discord
bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())
TOKEN = '' #Token del bot de Discord
channel_id = '' #ID del canal de voz

# Función para hacer backup de la base de datos y enviarla al canal
@tasks.loop(hours=24) # Hacer backup cada 24 horas
async def backup_database():
    filename = f'backup_{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.sql'
    subprocess.run(['mysqldump.exe', '-h', 'host_base_de_datos', '-u', 'usuario_base_de_datos', '-pcontraseña_base_de_datos', 'nombre_base_de_datos', '--skip-column-statistics', '--single-transaction', '--routines', '--triggers', '--events', f'--result-file={filename}'])
    print(f'Backup de la base de datos guardado correctamente en el archivo {filename}')
    # Verificar que el archivo de backup existe y es mayor a 0 bytes antes de enviarlo al canal de voz
    if os.path.exists(filename) and os.path.getsize(filename) > 0:
        channel = bot.get_channel(channel_id)
        if channel is not None:
            await channel.send(file=discord.File(filename))
            print(f'Backup enviado al canal {channel.name}')
            os.remove(filename) # Eliminar el archivo después de enviarlo al canal
            print(f'Archivo {filename} eliminado')
        else:
            print(f'No se encontró el canal con el ID {channel_id}')
    else:
        print('El archivo de backup no existe o está vacío, no se enviará al canal de voz')

@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user}')
    backup_database.start() # Iniciar la tarea de backup cada 24 horas

# Iniciar el bot
bot.run(TOKEN)
    