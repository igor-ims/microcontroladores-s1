from machine import Pin
import utime
import _thread

# Ultrassom: Trigger no GP16, Echo no GP17
trigger = Pin(16, Pin.OUT)
echo = Pin(17, Pin.IN)

botao = Pin(19, Pin.IN, Pin.PULL_UP)
bomba_entrada = Pin(14, Pin.OUT)
bomba_saida = Pin(12, Pin.OUT)

bomba_entrada_ativa = False
bomba_saida_ativa = False

bomba_entrada.low()
bomba_saida.low()

# Função para medir distância com o HC-SR04
def ultrassom():
    
    global bomba_entrada_ativa
    global bomba_saida_ativa
    
    trigger.low()
    utime.sleep_us(2)
    trigger.high()
    utime.sleep_us(10)
    trigger.low()
    
    distance=0

    # Espera o início do pulso de eco
    while echo.value() == 0:
        pass
    signaloff = utime.ticks_us()

    # Espera o fim do pulso de eco
    while echo.value() == 1:
        pass
    signalon = utime.ticks_us()

    timepassed = signalon - signaloff
    distance = (timepassed * 0.0343) / 2
    print("Distância até o objeto: {:.2f} cm".format(distance))
        
    if distance>10 and bomba_saida_ativa==False:
        bomba_entrada_ativa=True
        bomba_entrada.low()
    else:
        bomba_entrada.high()
        bomba_entrada_ativa=False

#Função que roda em outra thread para o botão e LED
def botao_bomba_saida():
    
    global bomba_entrada_ativa
    global bomba_saida_ativa
    
    while True:
        if not botao.value() and bomba_entrada_ativa==False:  # Botão pressionado (ativo em nível baixo)
            bomba_saida_ativa=True
            bomba_saida.low()
        else:
            bomba_saida.high()
            bomba_saida_ativa=False
        utime.sleep(0.05)  # Pequeno delay para evitar rebote

# Iniciar a thread paralela para o botão
_thread.start_new_thread(botao_bomba_saida, ())

# Loop principal com sensor ultrassônico
while True:
    ultrassom()
    utime.sleep(1)