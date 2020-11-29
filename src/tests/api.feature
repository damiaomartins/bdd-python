Feature: Folha de pagamento de funcionários por hora

  Background:
    Given o ambiente de testes esteja configurado


  Scenario: Funcionário horista precisa receber 50% de hora extra quando ultrapassar 40 horas na semana
    Given Um funcionário horista que recebe 30 reais por hora, submeteu uma planilha de horas totalizando 52 horas na última semana
    When For executada a folha de pagamento
    Then A folha de pagamento dará um total de 1740 reais, sendo 1200 de horas normais e 540 de horas extras

#  Scenario: Cadastrar novo funcionário
#    Given um funcionário com os seguindes dados:
#      | nome     | Fulano     |
#      | salario  | 1023       |
#      | admissao | 2020-11-29 |
#    When eu cadastrar ele através do endpoint "/employee/add"
#    Then o funcionário será cadastrado com sucesso

#  Scenario: Atualizar cadastro do funcionário
#    Given um funcionário cadastrado com os seguindes dados:
#      | id       | {id}       |
#      | nome     | Fulano     |
#      | salario  | 1023       |
#      | admissao | 2020-11-29 |
#    When eu cadastrar ele através do endpoint "/employee/add"
#    Then o funcionário será cadastrado com sucesso