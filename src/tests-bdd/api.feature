Feature: Folha de pagamento de funcionários por hora

  Background:
    Given o ambiente de testes esteja configurado


  Scenario: Funcionário horista precisa receber 50% de hora extra quando ultrapassar 168 horas no mes
    Given O funcionário 123 que recebe 30 reais por hora, submeteu um total de 200 horas no último mes
    When For executada o sistema de pagamento
    Then O pagamento do funcionário dará um total de 6480 reais, sendo 5040 de horas normais e 1440 de horas extras


  Scenario Template: Funcionário horista precisa receber 50% de hora extra quando ultrapassar 40 horas na semana
    Given O funcionário <id> que recebe <valor_hora> reais por hora, submeteu um total de <horas_trabalhadas> horas no último mes
    When For executada o sistema de pagamento
    Then O pagamento do funcionário dará um total de <salario_bruto> reais, sendo <salario_horas_normais> de horas normais e <salario_horas_extras> de horas extras

    Examples:
      | id  | valor_hora | horas_trabalhadas | salario_bruto | salario_horas_normais | salario_horas_extras |
      | 123 | 30         | 52                | 1560          | 1560                  | 0                    |
      | 123 | 25.6       | 100               | 2560          | 2560                  | 0                    |
      | 123 | 30.55      | 170               | 5224.05       | 5132.40               | 91.65                |


  Scenario Template: Falha ao tentar gerar pagamento com dados inválidos
    Given O funcionário <id> que recebe <valor_hora> reais por hora, submeteu um total de <horas_trabalhadas> horas no último mes
    When For executada o sistema de pagamento
    Then A solicitação falhará com uma mensagem de erro

    Examples:
      | id        | valor_hora | horas_trabalhadas |
      | 123       | 0          | 100               |
      | 123       | -1         | 100               |
      | 123       | {vazio}    | 100               |
      | 123       | 10         | 0                 |
      | 123       | 10         | -1                |
      | 123       | 10         | {vazio}           |
      | 123       | {vazio}    | {vazio}           |
      | 123       | {not_set}  | 10                |
      | 123       | 10         | {not_set}         |
      | {vazio}   | 10         | 10                |
      | {not_set} | 10         | 10                |