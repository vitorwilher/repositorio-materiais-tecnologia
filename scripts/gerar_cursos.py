#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gerador / scaffolder de páginas de curso do Repositório de Materiais (SENAC RJ).

O QUE FAZ
---------
Lê o REGISTRO de cursos abaixo e cria, para cada curso, a página
`cursos/<slug>/index.qmd` a partir do gabarito-padrão (PC · PTD · Referências ·
Materiais Complementares).

REGRA DE OURO: nunca sobrescreve.
---------------------------------
Se a página do curso já existe, o script a PRESERVA (mostra "mantido"). Assim você
pode rodar o gerador quantas vezes quiser sem perder conteúdo já preenchido pelos
instrutores. Para recriar uma página do zero, apague o arquivo e rode de novo.

COMO USAR
---------
    cd repositorio_materiais
    python scripts/gerar_cursos.py            # cria o que faltar
    python scripts/gerar_cursos.py --listar   # só lista o registro, não escreve

COMO ADICIONAR UM CURSO NOVO (ex.: nova tecnologia)
---------------------------------------------------
1. Acrescente um item em CURSOS (copie um existente como modelo).
2. Rode `python scripts/gerar_cursos.py`.
3. Edite o `cursos/<slug>/index.qmd` gerado e preencha os blocos.
4. Inclua o curso no diagrama da trilha (trilhas/trilha-*.qmd) e no
   fluxograma.qmd, e registre a mudança no changelog.qmd.

Sem dependências externas (só biblioteca padrão do Python).
"""

import os
import sys
import datetime

# ---------------------------------------------------------------------------
# METADADOS DAS TRILHAS  (id -> rótulo curto + arquivo da página)
# ---------------------------------------------------------------------------
TRILHAS = {
    "t1": ("Trilha 1 — IA Aplicada",                       "trilha-1-ia-aplicada"),
    "t2": ("Trilha 2 — Dados",                             "trilha-2-dados"),
    "t3": ("Trilha 3 — Infraestrutura, Cloud e Redes",     "trilha-3-infraestrutura"),
    "t4": ("Trilha 4 — Cibersegurança",                    "trilha-4-ciberseguranca"),
    "t5": ("Trilha 5 — Programação e Desenvolvimento",     "trilha-5-programacao"),
    "t6": ("Trilha 6 — Produtividade e Citizen Development","trilha-6-produtividade"),
}

# Rótulo legível para cada status
STATUS_LABEL = {
    "ativo":   "ativo no catálogo",
    "novo":    "novo — proposta a validar (GT Tech)",
    "futuro":  "futuro — horizonte de expansão",
    "retorno": "em atualização — retorno previsto",
}

# ---------------------------------------------------------------------------
# REGISTRO DE CURSOS  (fonte única da verdade para o scaffolder)
#   slug    : pasta do curso (cursos/<slug>/index.qmd)
#   titulo  : título exibido
#   ch       : carga horária (texto livre)
#   status  : ativo | novo | retorno | futuro
#   trilhas : lista de ids de trilha (um curso pode estar em mais de uma)
#   origem  : origem/observação curta
#   codigo  : código NC ou SGA (opcional, "")
# ---------------------------------------------------------------------------
CURSOS = [
    # ---- Trilha 1 — IA Aplicada -------------------------------------------
    dict(slug="ia-na-pratica", titulo="Inteligência Artificial na Prática",
         ch="8h", status="ativo", trilhas=["t1"], origem="Canal próprio (ONDA1)", codigo="SGA 14149"),
    dict(slug="ia-sem-misterio", titulo="IA Sem Mistério: Turbinando Sua Produtividade",
         ch="16h", status="ativo", trilhas=["t1", "t2"], origem="Catálogo público", codigo=""),
    dict(slug="ia-muito-alem-do-prompt", titulo="Inteligência Artificial — Muito Além do Prompt",
         ch="24h", status="ativo", trilhas=["t1", "t2"], origem="Catálogo público", codigo="SGA 13192*"),
    dict(slug="apresentacoes-dinamicas-ia", titulo="Apresentações Dinâmicas com IA Generativa",
         ch="32h", status="ativo", trilhas=["t1"], origem="Catálogo público", codigo=""),
    dict(slug="ai-901-azure", titulo="AI-901 — Inteligência Artificial com Azure",
         ch="~48h", status="futuro", trilhas=["t1"], origem="Em reformulação (sucede o AI-900)", codigo=""),
    dict(slug="ia-aplicada-avancada", titulo="IA Aplicada Avançada — Multiagent, RAG e LLM Ops",
         ch="80h", status="novo", trilhas=["t1"], origem="Proposta 2027", codigo="NC-04"),

    # ---- Trilha 2 — Dados --------------------------------------------------
    dict(slug="informatica-fundamental-ia", titulo="Informática Fundamental com IA",
         ch="60h", status="ativo", trilhas=["t2", "t6"], origem="Aluno-base das trilhas de Dados", codigo=""),
    dict(slug="excel-com-ia", titulo="Excel com IA",
         ch="28h", status="ativo", trilhas=["t2", "t6"], origem="Catálogo público", codigo=""),
    dict(slug="excel-com-ia-fundamentos", titulo="Excel com IA — Fundamentos",
         ch="8h", status="ativo", trilhas=["t6"], origem="Isca (ONDA2)", codigo="SGA 14758"),
    dict(slug="excel-avancado-ia", titulo="Excel Avançado com IA — Automação e Dados",
         ch="36h", status="ativo", trilhas=["t2", "t6"], origem="Catálogo público", codigo=""),
    dict(slug="excel-dashboard", titulo="Excel Dashboard — Planilhas Gerenciais",
         ch="24h", status="ativo", trilhas=["t2", "t6"], origem="Ramo lateral opcional", codigo=""),
    dict(slug="power-bi", titulo="Power BI",
         ch="60h", status="ativo", trilhas=["t2"], origem="Catálogo público", codigo=""),
    dict(slug="banco-de-dados", titulo="Banco de Dados",
         ch="120h", status="ativo", trilhas=["t2"], origem="Catálogo (relação com SQL para Dados a definir)", codigo=""),
    dict(slug="sql-para-dados", titulo="SQL para Dados",
         ch="60h", status="novo", trilhas=["t2"], origem="Proposta 2027", codigo="NC-02"),
    dict(slug="fundamentos-engenharia-dados", titulo="Fundamentos de Engenharia de Dados",
         ch="120h", status="novo", trilhas=["t2"], origem="Proposta 2027 (candidata: parceria Semantix)", codigo="NC-03"),
    dict(slug="ia-generativa-negocios", titulo="IA Generativa Aplicada a Negócios",
         ch="24h", status="novo", trilhas=["t2", "t5"], origem="Proposta — isca comum", codigo="NC-01"),

    # ---- Trilha 3 — Infraestrutura, Cloud e Redes -------------------------
    dict(slug="linux-profissionais-ti", titulo="Linux para Profissionais de TI",
         ch="40h", status="novo", trilhas=["t3"], origem="Proposta 2027 — pré-requisito DevOps", codigo="NC-07"),
    dict(slug="cloud-fundamentos-azure", titulo="Cloud Fundamentos com Azure",
         ch="40h", status="novo", trilhas=["t3"], origem="Proposta 2027 — gap Azure", codigo="NC-08"),
    dict(slug="google-cloud-foundations", titulo="Google Cloud Foundations",
         ch="76h", status="ativo", trilhas=["t3"], origem="Catálogo público", codigo=""),
    dict(slug="aws-restart", titulo="AWS RE/START",
         ch="400h", status="ativo", trilhas=["t3"], origem="Canal próprio — parceria AWS (sazonal)", codigo=""),
    dict(slug="cisco-ccna", titulo="Formação Cisco CCNA V7.0",
         ch="210h", status="ativo", trilhas=["t3"], origem="Catálogo público — parceria Cisco", codigo=""),
    dict(slug="containers-kubernetes", titulo="Containers e Kubernetes Essentials",
         ch="60h", status="novo", trilhas=["t3"], origem="Proposta 2027 — lacuna prioritária", codigo="NC-09"),

    # ---- Trilha 4 — Cibersegurança ----------------------------------------
    dict(slug="lgpd-governanca-dados", titulo="LGPD e Governança de Dados",
         ch="24h", status="novo", trilhas=["t4"], origem="Proposta 2027 — isca de governança", codigo="NC-05"),
    dict(slug="pentest-fundamentos", titulo="Pentest Fundamentos",
         ch="60h", status="novo", trilhas=["t4"], origem="Proposta 2027 — isca ofensiva", codigo="NC-06"),
    dict(slug="ciberseguranca-cisco", titulo="Cibersegurança Cisco",
         ch="100h", status="ativo", trilhas=["t4"], origem="Parceria Cisco — núcleo técnico", codigo=""),

    # ---- Trilha 5 — Programação e Desenvolvimento -------------------------
    dict(slug="programador-front-end-ia", titulo="Programador Front-End com IA",
         ch="80h", status="ativo", trilhas=["t5"], origem="Catálogo público — isca", codigo=""),
    dict(slug="full-stack-java", titulo="Programador Full Stack — Formação com Java",
         ch="360h", status="ativo", trilhas=["t5"], origem="Catálogo público — rota Web/Full Stack", codigo=""),
    dict(slug="mobile-react-native", titulo="Programação Mobile — React Native",
         ch="60h", status="ativo", trilhas=["t5"], origem="Catálogo público", codigo=""),
    dict(slug="back-end-java", titulo="Desenvolvedor Back-End Java",
         ch="84h", status="ativo", trilhas=["t5"], origem="Catálogo público — rota Back-End", codigo=""),
    dict(slug="programacao-node", titulo="Programação NODE",
         ch="100h", status="futuro", trilhas=["t5"], origem="Cronograma 2026 (ainda não publicado)", codigo=""),
    dict(slug="php-laravel", titulo="Programação em PHP com Laravel",
         ch="168h", status="ativo", trilhas=["t5"], origem="Catálogo público — mercado RJ", codigo=""),
    dict(slug="python-django", titulo="Programação em Python com Django",
         ch="168h", status="ativo", trilhas=["t5"], origem="Catálogo público — rota Python/IA", codigo=""),
    dict(slug="python-avancado-ia", titulo="Programação Avançada em Python com IA",
         ch="100h", status="ativo", trilhas=["t5"], origem="Catálogo público — ponte para Dados", codigo=""),

    # ---- Trilha 6 — Produtividade e Citizen Development -------------------
    dict(slug="informatica-melhor-idade", titulo="Informática Básica para Melhor Idade",
         ch="60h", status="ativo", trilhas=["t6"], origem="Ramo de inclusão digital", codigo=""),
    dict(slug="power-platform", titulo="Microsoft Power Platform",
         ch="48h", status="retorno", trilhas=["t6"], origem="Em atualização (Copilot Studio) — retorno previsto", codigo="SGA 13192"),
]


def gabarito(c):
    """Gera o conteúdo .qmd de um curso (página-stub a partir do registro)."""
    nome_trilhas = ", ".join(TRILHAS[t][0] for t in c["trilhas"])
    links_trilhas = " · ".join(
        f"[{TRILHAS[t][0]}](../../trilhas/{TRILHAS[t][1]}.qmd)" for t in c["trilhas"]
    )
    status_txt = STATUS_LABEL.get(c["status"], c["status"])
    codigo = f" · Código: {c['codigo']}" if c.get("codigo") else ""
    subtitulo = f"{c['ch']} · {nome_trilhas}"

    return f"""---
title: "{c['titulo']}"
subtitle: "{subtitulo}"
---

::: {{.callout-note appearance="simple"}}
**Status:** <span class="status-pill status-{c['status']}">{c['status']}</span> &nbsp; {status_txt}{codigo}
&nbsp;·&nbsp; **Carga horária:** {c['ch']} &nbsp;·&nbsp; **Origem:** {c['origem']}

**Material:** *a preencher* &nbsp;·&nbsp; **Última atualização:** *a preencher*
:::

## Onde este curso entra nas trilhas

Faz parte de: {links_trilhas}.

> *Preencha aqui o pré-requisito (curso anterior) e o próximo passo (call-to-action de upsell),
> conforme o diagrama da trilha. Ex.: "Vem de **X** · Próximo passo: **Y**".*

::: {{.panel-tabset}}

## PC — Plano de Curso

> *A preencher.* Resumo do Plano de Curso oficial. Linkar o `.docx` canônico.
> Sugestão de subtópicos: Identificação · Requisitos de acesso · Justificativa ·
> Objetivo · Organização curricular (conhecimentos, habilidades, atitudes) ·
> Orientações metodológicas · Avaliação · Instalações e recursos · Perfil docente · Certificação.

## PTD — Plano de Trabalho Docente

> *A preencher.* Situação de aprendizagem, indicador(es) da UC, planejamento das aulas
> (com sugestões de corte) e procedimentos/instrumentos de avaliação. Linkar o `.docx` canônico.

## Referências Bibliográficas

> *A preencher.* Bibliografia básica (oficial, do PC) e complementar (apoio).

## Materiais Complementares

> *A preencher.* Guias do instrutor, datasets/planilhas-exemplo, modelos, vídeos, prompts,
> tutoriais e demais apoios. Linkar arquivos da pasta de origem do curso, quando houver.

:::

## Histórico de atualizações (deste curso)

| Data | O que mudou | Autor |
|------|-------------|-------|
| *a preencher* | Criação da página (scaffold). | Cápsula de Inovação |

: Histórico do material deste curso. {{tbl-colwidths="[18,62,20]"}}
"""


def main():
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    cursos_dir = os.path.join(base, "cursos")

    if "--listar" in sys.argv:
        print(f"{len(CURSOS)} cursos no registro:\n")
        for c in CURSOS:
            tr = ",".join(c["trilhas"])
            print(f"  [{c['status']:7}] {c['slug']:32} {c['ch']:6} ({tr})  {c['titulo']}")
        return

    criados, mantidos = [], []
    for c in CURSOS:
        pasta = os.path.join(cursos_dir, c["slug"])
        os.makedirs(pasta, exist_ok=True)
        arq = os.path.join(pasta, "index.qmd")
        if os.path.exists(arq):
            mantidos.append(c["slug"])
            continue
        with open(arq, "w", encoding="utf-8") as f:
            f.write(gabarito(c))
        criados.append(c["slug"])

    print(f"Gerador de cursos — {datetime.date.today().isoformat()}")
    print(f"  criados:  {len(criados)}")
    for s in criados:
        print(f"    + cursos/{s}/index.qmd")
    print(f"  mantidos (já existiam, preservados): {len(mantidos)}")
    for s in mantidos:
        print(f"    = cursos/{s}/index.qmd")


if __name__ == "__main__":
    main()
