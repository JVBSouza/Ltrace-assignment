<br />
<p align="center">
  <h2 align="center">LTrace Programmin Assignment</h2>
  <p align="center">
    Teste prático de programação
  </p>
</p>

<!-- ABOUT THE PROJECT -->
## Sobre o teste
O teste era composto por duas etapas. Primeiro um plugin em python e segundo um programa de histograma de texto em c++</br>
O teste de python consistia em desenvolver um plugin para o software [3D SLICER](https://www.slicer.org/) que realizasse uma segmentação binária do volume selecionado no programa</br>
Já o teste em C++ era desenvolver uma aplicação simples que recebe um arquivo texto e imprime de forma decrescente a letra e quantidade de vezes que aparecia no arquivo

### Built With

* Python
* C++


<!-- GETTING STARTED -->
## Rodando os testes
### Plugin
1. Nas configurações do programa 3D Slicer adicione a pasta com o arquivo do plugin .py
2. Selecione o módulo, adicione algum dos volumes de amostras e aplique um valor de limiar
3. Para mais testagem, aperte o botão "Reload and test" para rodas os testes padrões

<br/>

### Histograma de texto
1. Entre na pasta text_histogram e compile o projeto cmake
2. Rode o comando ./text_histogram ./COPYING ./README

<!-- LICENSE -->
## License

Distributed under the GNU License. See `LICENSE` for more information.

<!-- CONTACT -->
## Contact

Authors: José Vinícius Boing de Souza
