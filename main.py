import time 
import random  
import logging  #  módulo para el registro de mensajes
import threading  # módulo para manejar hilos
import keyboard  # módulo para detectar eventos de teclado

# Tamaño del buffer 
BUFFER_SIZE = 25  
buffer = [None] * BUFFER_SIZE  # Inicializa el buffer 
in_index = 0  # Índice del productor
out_index = 0  # Índice del consumidor
buffer_count = 0  # Número de elementos actuales en el buffer

# Condiciones para controlar el acceso al buffer
buffer_lock = threading.Lock()  # Crea un bloqueo para asegurar el acceso exclusivo al buffer
not_empty = threading.Condition(buffer_lock)  # Condición que permite que los hilos esperen si el buffer está vacío
not_full = threading.Condition(buffer_lock)  # Condición que permite que los hilos esperen si el buffer está lleno

continuar = True  # Variable que controla la ejecución de los hilos

# Configuración del logging para mostrar el estado de cada hilo
logging.basicConfig(level=logging.DEBUG, format='%(threadName)s: %(message)s')

# función para ver el estado actual del buffer
def verBuffer():
    print("Buffer:") 
    for item in buffer:  
        print(f'| {item if item is not None else " "} ', end="")
    print("|") 

def producer():
    """Función que simula el comportamiento del productor."""
    global in_index, buffer_count 
    while continuar: 
        with not_full:  # Bloquea el acceso
            # Verifica si el buffer está lleno
            if buffer_count == BUFFER_SIZE:
                logging.info('Productor dormido: el buffer está lleno.') 
            else:
                num_items = random.randint(1, 5)  # Genera un número aleatorio de elementos a producir
                # Calcula el número máximo de elementos que se pueden insertar sin superar el tamaño del buffer
                num_items = min(num_items, BUFFER_SIZE - buffer_count)

                for i in range(num_items):
                    # Selecciona aleatoriamente un elemento de una lista de caracteres
                    item = random.choice(['#', '@', '&', 'A', 'B', 'C'])
                    buffer[in_index] = item 
                    logging.info(f'Inserto: {item} en posición {in_index + 1}')  
                    # Actualización de índices y contadores
                    in_index = (in_index + 1) % BUFFER_SIZE  
                    buffer_count += 1 
                verBuffer() 
                not_empty.notify()  # Notifica al consumidor que hay elementos disponibles

        # Tiempo aleatorio antes de intentar producir de nuevo
        time.sleep(random.uniform(1, 8)) 

def consumer():
    """Función que simula el comportamiento del consumidor."""
    global out_index, buffer_count 
    while continuar:  
        with not_empty:  # Bloquea el acceso a otros hilos
            # Verifica si el buffer está vacío
            if buffer_count == 0:
                logging.info('Consumidor dormido: el buffer está vacío.') 
            else:
                num_items = random.randint(1, 5)  # Genera un número aleatorio de elementos a consumir
                # Verifica que hay suficientes elementos para consumir
                num_items = min(num_items, buffer_count)

                for i in range(num_items):
                    item = buffer[out_index] 
                    buffer[out_index] = None  # Elimina el elemento del buffer
                    logging.info(f'Consume: {item} de posición {out_index + 1}')  # Registra la eliminación del elemento
                    
                    # Actualización de índices y contadores
                    out_index = (out_index + 1) % BUFFER_SIZE 
                    buffer_count -= 1
                verBuffer()  # Muestra el estado actual del buffer
                not_full.notify()  # Notifica al productor que hay espacio disponible

        # Tiempo aleatorio antes de intentar consumir de nuevo
        time.sleep(random.uniform(1, 8))

# Muestra el estado inicial del buffer
verBuffer()
# Creación e inicio de los hilos del productor y consumidor
thread_producer = threading.Thread(target=producer, name='Productor')  # Crea un hilo para el productor
thread_consumer = threading.Thread(target=consumer, name='Consumidor')  # Crea un hilo para el consumidor

thread_producer.start()  # Inicia el hilo del productor
thread_consumer.start()  # Inicia el hilo del consumidor

keyboard.wait('esc')  # Espera hasta que se presione la tecla Escape

continuar = False  # Cambio de la bandera para detener al productor y consumidor
print("Deteniendo el programa...")  
