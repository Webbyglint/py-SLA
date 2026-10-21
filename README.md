# Monitor de SLA de Chamados

Ferramenta em Python que transforma um export de chamados de TI em um relatório
de cumprimento de SLA, sem trabalho manual em planilha.

> Todos os dados deste repositório são **fictícios**, gerados por `gerar_dados.py`.

## Problema
Em times de suporte de TI, acompanhar o SLA costuma ser um processo manual:
exportar chamados, montar planilha, aplicar fórmulas e conferir um a um quais
estouraram o prazo. É repetitivo, demorado e sujeito a erro, e a liderança só
descobre o problema quando já é tarde.

## Solução
Um script que:
1. lê o CSV exportado da ferramenta de chamados;
2. calcula o tempo de resolução de cada chamado e compara com o prazo da prioridade
   (Crítica 4h, Alta 8h, Média 24h, Baixa 72h);
3. agrega o cumprimento por **prioridade**, **categoria** e **semana**;
4. gera um relatório em Markdown já pronto para compartilhar.

## Resultado
Com 300 chamados simulados, o relatório sai em menos de 1 segundo e já aponta a
categoria mais crítica e a evolução semanal, trabalho que manualmente levaria
bem mais tempo a cada ciclo.

## Como usar
```bash
python gerar_dados.py              # cria chamados.csv (dados fictícios)
python sla_report.py chamados.csv  # gera relatorio_sla.md
```

## Testes
```bash
pip install pytest
pytest
```

## Decisões técnicas
- **Somente biblioteca padrão:** sem dependências, roda em qualquer máquina.
- **Regras de SLA em um dicionário:** mudar um prazo é editar uma linha.
- **Funções puras (`resumir`, `agrupar`):** fáceis de testar e reutilizar.
- **Seed fixa no gerador:** os dados são reproduzíveis.

## Próximos passos
- Ler direto da API/banco em vez de CSV
- Considerar horário comercial no cálculo do SLA
- Enviar o relatório por e-mail automaticamente
- Gráficos com matplotlib
