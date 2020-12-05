# control_personal_mac
TP Especial para Redes de Computadoras: Control de personal con las MACs de celulares que se ven en WiFi. FI-UNMDP, 2020. 

Alumnos: Mariquena Gros y Pablo Porzio.

Solo para Linux

Fuentes:
  - https://www.thepythoncode.com/article/building-network-scanner-using-scapy
  - https://stackoverflow.com/questions/8600161/executing-periodic-actions-in-python
  - https://pynative.com/python-json-load-and-loads-to-parse-json/
  - https://code-maven.com/interactive-shell-with-cmd-in-python

Instrucciones:
  - Cargar empleados.json con el siguiente formato:
  
      {
      
        "mac 1": "nombre empleado 1",
          ...
        "mac N": "nombre empleado N"
          
      }
  - Cargar config.json con el siguiente formato:
      
      {
      
              "lan": "IP/mask CIDR",
	      "periodoControl": X,
	      "plazoMax": Y
     
      }
      - X = periodo de control de WiFi, en segundos.
      - Y = plazo maximo para considerar que un empleado sigue online, en segundos.
  - Ejecutar como sudo.
