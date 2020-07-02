# prisitri
Agendamento de Recursos Genérico


### Endpoints

Endpoints são endereços para acessar recursos na internet. Os seguintes endpoints são disponibilizados através desta API:

| HTTP Method | URI                                                                        | Ação
| ---         | ---                                                                        | ---
| POST        | [host]/token/                                                              | Obter o token JWT
| GET         | [host]/orders/                                                             | Solicitações do usuário autenticado
| GET         | [host]/resources/[resourceId]/availabilities/[scheduleTypeId]/?date=[date] | Obter o token JWT
| GET         | [host]/users/[username]/                                                   | Obter o token JWT
| GET         | [host]/extendedusers/[extendedUserId]/                                     | Obter o token JWT
| GET         | [host]/companies/[companyId]/                                              | Obter o token JWT
| GET         | [host]/resourcetypes/[resourceTypeId]/                                     | Obter o token JWT
| GET         | [host]/resources/[resourceId]/                                             | Obter o token JWT
| GET         | [host]/extendedusers/[extendedUserId]/orders/                              | Obter o token JWT


## Regras de negócios
* Slots de tempo de uso dos solicitantes
* Slots de tempo de disponibilidade do recurso no dia (mais de um por dia)

## Histórias do usuário
* Solicitante
* Gerente do recurso