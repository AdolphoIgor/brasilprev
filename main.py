"""
    Para facilitar a execução/avaliação deste programa, procurei simplificar a estrutura de projeto reduzindo-o a um script, 
    todas as dependencias do projeto são padrão para a instação do Python.
    
    Este projeto usa Python 3.8+
    
    Ao escrever código, na busca por resolver o problema, mantenho a preocupação de equilibrar a redução de passos e a 
    legibilidade do código, a final, não adianta ter um código super performático, super reduzido, se as pessoas que
    por ventura venham a dar manutenção nele não sejam capaz de compreendê-lo; o que faltamente irá conduzir à sua
    substituição. Portanto, peço que tenham em mente que há muito espaço para redução e otimizações aqui. Ok?
    
    Procurei tambem apresentar variadas técnicas aqui que vão desde o emprego da metaprogramação e vai até o minsdset
    de desenvolvimento Pythônico, com técnicas de manipulação de dados mais adeqadas para a redução na solução do problema.
    
    Peço apenas sua compreensão pois excedi na quantidade de comentários neste código. O objetivo é guiá-los na 
    compreensão do programa.

    Quaisquer dúvidas, podem me alcançar pelo email: adolpho.igor@gmail.com
    
"""
from random import seed
from random import random, randint, shuffle
from statistics import mean
import collections

seed(1)

# Dicionario contendo acumuladores para a saída
dct_saida = {
    "timeout": 0,
    "lst_turnos": [],
    "lst_vencedores": []
}

lst_jogadores = None
for simulacao in range(300):
    # lista de jogadores
    lst_jogadores = [
        {"id": 0, "tipo": "impulsivo", "estrategia": "propriedade is not None", "saldo": 300, "posicao": 0},
        {"id": 1, "tipo": "exigente", "estrategia": "valor_aluguel > 50", "saldo": 300, "posicao": 0},
        {"id": 2, "tipo": "caulteloso", "estrategia": "(saldo - custo_venda) >= 80", "saldo": 300, "posicao": 0},
        {"id": 3, "tipo": "aleatorio", "estrategia": "random() >= 0.5", "saldo": 300, "posicao": 0},
    ]

    # lista de propriedades
    lst_propriedades = []
    for i in range(0, 20):
        custo = randint(50, 300)
        lst_propriedades.append({"id": i, "custo_venda": custo, "valor_aluguel": round(custo * 0.22, 2),
                                 "proprietario": -1})

    # essa é a ordem dos jogadores
    lst_ordem_jogador = [dct.get("id") for dct in lst_jogadores]
    shuffle(lst_ordem_jogador)

    TURNOS = 1000
    for rodada in range(TURNOS):
        for vez in lst_ordem_jogador:
            jogador = lst_jogadores[vez]

            # fim de partida
            if len(lst_ordem_jogador) == 1:
                dct_saida["lst_turnos"].append(rodada)
                dct_saida["lst_vencedores"].append(jogador.get("id"))
                break

            # esse é o dado do jogo
            valor_dado = randint(1, 6)

            # se deu a volta no tabuleiro
            if jogador["posicao"] + valor_dado > len(lst_propriedades):
                jogador['saldo'] += 100
                jogador["posicao"] = jogador["posicao"] + valor_dado - 1 - len(lst_propriedades)
            else:
                jogador["posicao"] += valor_dado - 1

            propriedade = lst_propriedades[jogador["posicao"]]
            proprietario = propriedade.get("proprietario")
            valor_aluguel = propriedade.get("valor_aluguel")
            jogador_id = jogador.get("id")

            if proprietario == -1:
                # pode comprar
                saldo = jogador.get("saldo")
                custo_venda = propriedade.get("custo_venda")
                """
                    Ponto importante: como a regra fala que o jogador PODE escolher comprar ou não, assumo que
                    isso implica que ele pode escolher não comprar se não tiver dinheiro suficiente (para cometer 
                    suicído).
                """
                if saldo >= custo_venda:
                    if eval(jogador.get("estrategia")):
                        jogador["saldo"] = round(saldo - propriedade.get("custo_venda"), 2)
                        propriedade['proprietario'] = jogador_id

            elif proprietario != jogador.get("id"):
                # tem que pagar aluguel
                if jogador['saldo'] - valor_aluguel <= 0:
                    lst_ordem_jogador.remove(jogador_id)

                    for prop in lst_propriedades:
                        if prop.get("proprietario") == jogador_id:
                            prop["proprietario"] = -1

                    continue

                proprietario = lst_jogadores[proprietario]
                proprietario['saldo'] = round(proprietario['saldo'] + valor_aluguel, 2)
                jogador['saldo'] = round(jogador['saldo'] - valor_aluguel, 2)

    # timeout
    if len(lst_ordem_jogador) > 1:
        dct_saida["timeout"] += 1
        dct_saida["lst_turnos"].append(TURNOS)

        jogadores = [dct for dct in lst_jogadores if dct.get("id") in lst_ordem_jogador]
        jogadores.sort(key=(lambda x: x.get("saldo")), reverse=True)

        vencedor = jogadores.pop(0)
        lst_empate = list(filter(lambda x: x.get("saldo") == vencedor.get("saldo"), jogadores))
        if len(lst_empate) == 0:
            dct_saida["lst_vencedores"].append(vencedor.get("id"))
            continue

        dct_saida["lst_vencedores"].append(lst_ordem_jogador[0])

# computando o resultado
lst_resultado = []
sum_vencedores = len(dct_saida.get('lst_vencedores'))
lst_somatorio = [{k: v} for k, v in collections.Counter(dct_saida.get('lst_vencedores')).items()]
jogador = None
for dct in lst_somatorio:
    for k, v in dct.items():
        for reg in lst_jogadores:
            if reg.get('id') == k:
                jogador = reg
                break

        lst_resultado.append({"id": k, "tipo": jogador.get("tipo"), "qtd": v, "perc": round(v / sum_vencedores, 2)})

lst_resultado.sort(key=(lambda x: x.get("qtd")), reverse=True)

print(f"Partidas terminadas por timeout: {dct_saida.get('timeout')}.")
print(f"Media de turnos por partida: {round(mean(dct_saida.get('lst_turnos')), 2)}.")
print(f"Percentagem de vitorias por comportamento:")
for item in lst_resultado:
    print(f"Tipo: {item.get('tipo')}, Porcentagem: {item.get('perc')}")

print(f"Comportamento mais vencedor: {lst_resultado[0].get('tipo')}.\n")
