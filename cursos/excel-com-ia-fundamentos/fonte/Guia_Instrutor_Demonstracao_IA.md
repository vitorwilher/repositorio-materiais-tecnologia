# Guia do Instrutor — Excel com IA (Fundamentos)
## Demonstração: construir a planilha da Mariana com apoio de uma IA externa (Claude)

**Para quem:** instrutores que vão ministrar o curso *Excel com IA — Fundamentos* (Instrumental, 8h, remoto).
**O que é este material:** um roteiro pronto para você mostrar, ao vivo, como uma IA generativa externa (Claude, ChatGPT ou Gemini) apoia o aluno a montar a planilha de vendas da persona **Mariana Silva**. Acompanha o arquivo **`Exemplo_Planilha_Inteligente_Mariana.xlsx`**.

---

## 1. A ideia central (diga isto para a turma)

> A IA **não fica dentro do Excel**. O fluxo é: **o aluno descreve o problema em português**, a IA responde com a fórmula/explicação/sugestão, e o **aluno copia para a célula e confere**.

É a competência "Engenharia de Comandos" da ementa: o aluno aprende a *pensar com a tecnologia*, não a decorar fórmula. A IA é o colega que explica e sugere; quem decide e confere é o aluno.

**Por que Claude como exemplo:** funciona em qualquer navegador, dá explicações didáticas em português e aceita que o aluno descreva a planilha em linguagem natural. Os mesmos prompts valem para ChatGPT e Gemini (citados no PTD) — apresente o que estiver mais à mão.

---

## 2. O arquivo de exemplo (3 abas)

| Aba | Para que serve na demonstração |
|-----|--------------------------------|
| **Antes** | Mostra a dor da Mariana: dados bagunçados, datas em formatos diferentes, valores como texto, sem totais, sem gráfico. Abra primeiro — gera o "antes". |
| **Depois (Planilha Inteligente)** | O resultado final: tabela formatada, coluna Total, data/hora automáticas, RESUMO (total, ticket médio, maior e menor venda), filtro e gráfico de colunas. É o modelo que o PTD pede que você entregue na Aula 1. |
| **Como pedir ao Claude** | Tabela com os prompts prontos, por aula. Pode projetar direto. |

> **Dica:** na Aula 1 o PTD manda **fornecer um modelo pronto** e avisar que o aluno construirá um parecido na última aula. Use a aba **Depois** como esse modelo.

---

## 3. Roteiro por aula (com os prompts do Claude)

As 4 aulas têm 2h cada. Os conhecimentos estão na organização curricular do Plano de Curso; abaixo, onde a IA entra.

### Aula 1 — Interface, guias e formatação
- Tour pelo Excel e pelo Teams; debate sobre experiências com Excel.
- Entregue o modelo (aba **Depois**) e mostre onde a turma quer chegar.
- Enquete: quem já usou IA generativa? Apresente o Claude rapidamente (abrir, fazer login, caixa de conversa).
- **Sem fórmula ainda** — só ambientação na ferramenta e na IA.

### Aula 2 — Fórmulas, função SOMA, HOJE e AGORA
Construa a planilha de vendas (Data, Produto, Quantidade, Valor Unitário, Total) e peça à IA:

- **Coluna Total:**
  > *No Excel, tenho a Quantidade na coluna C e o Valor Unitário na coluna D, a partir da linha 5. Qual fórmula coloco na coluna Total (E5) para multiplicar os dois? Explique como se eu nunca tivesse usado fórmula.*

- **Data e hora automáticas:**
  > *Quero que a planilha mostre sozinha a data de hoje e a hora atual, que se atualizam quando eu abro o arquivo. Quais funções do Excel uso e qual a diferença entre elas?*

### Aula 3 — Estatística (MÉDIA, MÁXIMO, MÍNIMO), classificar e filtrar
Abra a planilha da aula anterior. Gancho do PTD: *"Se seu gestor pedir agora a média das vendas, o maior e o menor valor — você responderia rápido?"*

- **Fórmulas estatísticas:**
  > *Tenho os valores de Total das vendas na coluna F (F5 até F16). Me dê as fórmulas em português do Excel para: soma de tudo, média, maior valor e menor valor. Explique a diferença entre MÉDIA, MÁXIMO e MÍNIMO.*

- **Validação da organização** (prompt sugerido no próprio PTD):
  > *Vou te descrever as colunas da minha planilha de vendas: Data, Produto, Quantidade, Valor Unitário, Forma de Pagamento e Total. Essa estrutura está boa para analisar os dados? O que você melhoraria?*

- **Classificar e filtrar:**
  > *Como eu classifico essa tabela do maior para o menor Total e como aplico um filtro para ver só as vendas pagas no Pix? Me dê o passo a passo no Excel.*

### Aula 4 — Gráficos, configuração de página e avaliação
- **Escolher o gráfico** (prompt sugerido no PTD):
  > *Quero um gráfico que compare o Total de vendas por produto. Qual tipo de gráfico é o mais indicado e como eu insiro ele no Excel a partir das colunas Produto e Total?*

- **Preparar para impressão/apresentação:**
  > *Como deixo essa planilha mais profissional para imprimir e apresentar: orientação da página, cabeçalho, rodapé com número de página e área de impressão? Passo a passo no Excel.*

- **Atividade avaliativa:** o aluno reconstrói a planilha da Mariana aplicando formatação, funções, organização e gráfico (instrumento de avaliação do PTD).

---

## 4. Boas práticas ao usar a IA (combine com a turma)

1. **A IA pode errar.** Toda fórmula sugerida deve ser testada na planilha. Se der `#NOME?` ou `#VALOR!`, peça à IA para corrigir descrevendo o erro.
2. **Separador de argumentos:** no Excel em português costuma ser **`;`** (ponto e vírgula), ex.: `=SOMA(F5:F16)`. Se a IA devolver com vírgula, troque.
3. **Privacidade / LGPD:** não cole dados reais e sensíveis de clientes (CPF, nomes, telefones) na IA. Use dados de exemplo, como os deste arquivo.
4. **Contas:** o curso usa conta Gmail e Microsoft; reforce que o aluno crie/entre antes da aula.
5. **Histórico e logoff:** ao fim de cada aula, manter a conversa no histórico e fazer logoff das contas no computador (orientação do PTD).

---

## 5. Como reproduzir a planilha do zero (caso queira gerar de novo)

O arquivo foi gerado pelo script `gerar_planilha_exemplo.py` (Python + openpyxl) nesta mesma pasta:

```bash
python gerar_planilha_exemplo.py
```

Útil se você quiser trocar os produtos/valores e gerar uma variação para outra turma.

---

*Material de apoio à habilitação — Cápsula de Inovação, Coordenação de Tecnologias, SENAC RJ.*
