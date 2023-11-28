Integrantes:
  José Castro, 202073550-6
  Florencia Ramírez, 202073522-0

☆.。.:*・°☆.。.:*・°☆.。.:*・°☆.。.:*・°☆.。.:*・°☆

Instrucciones de compilación:
  Esta tarea fue hecha con mininet 2.3.0, compilada en ubuntu 20.04.
  
  Se debe instalar mininet
    $ git clone https://github.com/mininet/mininet
    $ mininet/util/install.sh -a
  Lo cual debería instalar todo lo necesario para la correcta compilación de la tarea.

  Se debe mover el archivo topologia1.py a la carpeta mininet y se debe mover el archivo controlador1.py a la carpeta 
  mininet/pox/pox/forwarding
  Se deben abrir 2 terminales distintas, donde se ejecutarán los códigos de la topología y el controlador
    $ python3 pox/pox.py --verbose openflow.spanning_tree --no-flood --hold-down openflow.discovery forwarding.controlador1.py
    $ sudo mn --custom topologia1.py --topo MyTopo --mac --controller remote --switch ovsk
  
  Luego para eliminar una conexión se ejecuta en la terminal de la topología:
    $ link s3 s4 down
  
☆.。.:*・°☆.。.:*・°☆.。.:*・°☆.。.:*・°☆.。.:*・°☆

Comentarios extra:
  - Se hizo solo la primera parte de la tarea, la red 1 con anillo interconectado con conexiones bidireccionales.
  - Se hizo el enlace extra entre el switch 1 y 3 como la figura, no 2 y 4 como dice el enunciado, en sí debería funcionar de
    manera similar si se hubiera hecho con esos.
  - El archivo controlador1.py es una copia del archivo l2_learning.py proporcionado en la instalación de POX.