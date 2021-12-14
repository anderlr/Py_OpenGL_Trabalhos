## O cenário e o algoritmo de Dijkstra

Uma nave espacial precisa sair o mais rápido possível de uma galáxia, porém as leis da galáxia obrigam a nave a pagar pedágio a cada planeta na qual ela se aproximar, sendo obrigatório viajar de planeta em planeta. A nave decidiu portanto realizar o menor caminho.


### Cenário:
![alt text](https://i.imgur.com/JwyH8DT.png)

### Algoritmo de Dijkstra:

O Algoritmo de Dijkstra (E.W. Dijkstra) é um dos algoritmos que calcula o caminho de custo mínimo entre vértices de um grafo. Escolhido um vértice como raiz da busca, este algoritmo calcula o custo mínimo deste vértice para todos os demais vértices do grafo. Ele é bastante simples e com um bom nível de performance. Ele não garante, contudo, a exatidão da solução caso haja a presença de arcos com valores negativos.

Este algoritmo parte de uma estimativa inicial para o custo mínimo e vai sucessivamente ajustando esta estimativa. Ele considera que um vértice estará fechado quando já tiver sido obtido um caminho de custo mínimo do vértice tomado como raiz da busca até ele. Caso contrário ele dito estar aberto.


![alt text](https://i.imgur.com/I3YyuX4.png)
![alt text](https://i.imgur.com/fllqvQH.png)

### Checklist:

- [x] Modelar a nave espacial
- [x] Modelar os planetas
- [ ] Adicionar cor ou textura para a nave
- [x] Adicionar cor ou textura para a os planetas
- [x] Posicionar a nave no cenário
- [x] Posicionar os planetas
- [x] Posicionar a câmera no cenário
- [x] Movimentar a nave seguindo menor caminho (Dijkstra)


https://pt.vecteezy.com/arte-vetorial/2772916-space-ufo-icon-collection
https://www.freepik.com/free-vector/colorful-cartoon-planets-icon-kit_8270973.htm#page=1&query=planet%20icon&position=0&from_view=keyword
http://www.inf.ufsc.br/grafos/temas/custo-minimo/dijkstra.html
https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyopengl - pip install PyOpenGL‑3.1.5‑cp39‑cp39‑win_amd64.whl
