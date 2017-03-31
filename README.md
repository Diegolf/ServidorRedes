# ServidorRedes
Instituto Federal Sudeste de Minas Gerais - Campus Barbacena. Tecnologia em Sistemas para a Internet - 3º Período
Trabalho prático da disciplina de redes de computadores.
Servidor HTTP desenvolvido em python, utilizando socket, expreção regular e thread.

Exemplo de uso:
<pre>
from servidorHTTP import ServidorHTTP
servidor = ServidorHTTP("127.0.0.1",8000)
servidor.iniciarServidor()
</pre>

Linha de comando:
<pre>
$ python servidorHTTP.py 127.0.0.1 8000
</pre>
