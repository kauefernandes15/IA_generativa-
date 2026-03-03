from classifier import classificar_mensagem

TEMPERATURES = [0.0, 0.5, 1.0]

mensagem_teste = "Quero cancelar minha assinatura"

for temp in TEMPERATURES:
    print(f"\n===== TESTANDO TEMPERATURA {temp} =====")

    for i in range(10):
        resposta = classificar_mensagem(mensagem_teste, temperature=temp)
        print(f"Execução {i+1}: {resposta}")