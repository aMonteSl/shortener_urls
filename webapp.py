#!/usr/bin/python3
import socket


class webApp:

    def __init__(self, hostname, port):
        "INICIAR NUESTRA APP WEB"

        # AF_INET = IPv4, SOCK_STREAM = TCP
        mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Habilitar reutilización de direcciones
        mySocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        mySocket.bind((hostname, port))

        # Cola máxima de 5 conexiones TCP
        mySocket.listen(5)

        while True:
            print("Esperando alguna conexión...")
            connectionSocket, addr = mySocket.accept()
            print("Conexión recibida de: " + str(addr))
            recibido = connectionSocket.recv(2048)
            print(f"El crudo en bytes:{recibido}\n\n")
            print(f"Lo recibido en string:{recibido.decode('utf-8')}\n\n")

            # Manejar/parsear recursos
            parsed_request = self.parse(recibido.decode("utf-8"))

            # Proceso la peticion y creo la respuesta
            return_code, html_respuesta = self.procces(parsed_request)

            # Enviar respuesta
            if return_code is not None:
                response = "HTTP/1.1 " + return_code + "\r\n\r\n" \
                    + html_respuesta + "\r\n"
                connectionSocket.send(response.encode("utf-8"))
                connectionSocket.close()

    def parse(self, request):
        "PARSEO LA PERICION EXTRAYENDO LA INFO"

        print("PARSE: NO HAY NADA QUE PARSEAR AHORA MISMO")
        return None

    def procces(self, parsed_request):
        "PROCESA LOS DATOS DE LA PETICION"
        "DEVUELVE EL CODIGO HTTP DE LA RESPUESTA Y UNA PAGINA HTML"

        print("PROCCES: No HAY NADA QUE PROCESAR")
        return "200 OK", "<html><body>Hola mundo</body></html>"


if __name__ == "__main__":
    try:
        my_webapp = webApp("", 1234)
    except KeyboardInterrupt:
        print("Finalizando el servidor...")
