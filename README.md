# Labirinto e Algoritmos de Busca

Este projeto implementa e compara quatro algoritmos de busca (BFS, DFS, A*, e Greedy) para encontrar caminhos em um labirinto gerado aleatoriamente. Ele mede o desempenho dos algoritmos em termos de tempo de execução, consumo de memória, completude e optimalidade. Além disso, gera gráficos para visualização dos resultados.

## Instalação

Para rodar este projeto, você precisa ter o Python 3.x instalado. Você também deve instalar as bibliotecas necessárias. Você pode fazer isso usando o `pip`:

```bash
pip install numpy matplotlib psutil
```

### Execute 
Execute o script Python com o comando abaixo. Isso gerará o labirinto, executará os algoritmos de busca e exibirá os gráficos comparativos:
```bash
python3 main.py
```

## Saída Esperada

- **Labirinto**: O labirinto gerado será impresso no console.
- **Arquivos de Texto**: Arquivos contendo os passos intermediários de cada algoritmo serão criados no diretório atual, com nomes como `BFS_passos.txt`, `DFS_passos.txt`,`A*_passos.txt` e `Greedy_passos.txt`
- **Gráficos**: Gráficos comparando o tempo de execução, consumo de memória, completude e optimalidade dos algoritmos serão exibidos em uma janela de plotagem.



## Autores

- **Thomás T. Pereira**
- **Ygor S. Viera** - [Perfil GitHub](https://github.com/eplaie)

