import numpy as np
import skfuzzy as fuzz
import matplotlib
from skfuzzy import control as ctrl

temperatura_ambiente = ctrl.Antecedent(np.arange(-10, 51, 1), 'temperatura_ambiente')
temperatura_variacao = ctrl.Antecedent(np.arange(-5, 6, 1), 'temperatura_variacao')
temperatura_externa = ctrl.Antecedent(np.arange(-20, 51, 1), 'temperatura_externa')
acao_controlador = ctrl.Consequent(np.arange(-100, 101, 1), 'acao_controlador')

TA_MF = 'muito_frio'
TA_F = 'frio'
TA_C = 'confortavel'
TA_Q = 'quente'
TA_MQ = 'muito_quente'

temperatura_ambiente[TA_MF] = fuzz.trimf(temperatura_ambiente.universe, [-10, -10, 10])
temperatura_ambiente[TA_F] = fuzz.trimf(temperatura_ambiente.universe, [5, 10, 15])
temperatura_ambiente[TA_C] = fuzz.trimf(temperatura_ambiente.universe, [10, 17.5, 25])
temperatura_ambiente[TA_Q] = fuzz.trimf(temperatura_ambiente.universe, [20, 25, 30])
temperatura_ambiente[TA_MQ] = fuzz.trimf(temperatura_ambiente.universe, [25, 37.5, 50])

TV_D = 'decrescente'
TV_E = 'estavel'
TV_C = 'crescente'

temperatura_variacao[TV_D] = fuzz.trimf(temperatura_variacao.universe, [-5, -5, -1])
temperatura_variacao[TV_E] = fuzz.trimf(temperatura_variacao.universe, [-2, 0, 2])
temperatura_variacao[TV_C] = fuzz.trimf(temperatura_variacao.universe, [1, 3, 5])

TE_MF = 'muito_frio'
TE_FE = 'frio'
TE_AM = 'amena'
TE_QE = 'quente'
TE_MQE = 'muito_quente'

temperatura_externa[TE_MF] = fuzz.trimf(temperatura_externa.universe, [-20, -20, 0])
temperatura_externa[TE_FE] = fuzz.trimf(temperatura_externa.universe, [-5, 2.5, 10])
temperatura_externa[TE_AM] = fuzz.trimf(temperatura_externa.universe, [7, 13.5, 20])
temperatura_externa[TE_QE] = fuzz.trimf(temperatura_externa.universe, [15, 22.5, 30])
temperatura_externa[TE_MQE] = fuzz.trimf(temperatura_externa.universe, [25, 37.5, 50])

# Custom membership functions can be built interactively with a familiar,

AC_RF = 'resfriar_fortemente'
AC_RM = 'resfriar_moderadamente'
AC_M = 'manter'
AC_AM = 'aquecer_moderadamente'
AC_AF = 'aquecer_fortemente'

acao_controlador[AC_RF] = fuzz.trimf(acao_controlador.universe, [-100, -100, -50])
acao_controlador[AC_RM] = fuzz.trimf(acao_controlador.universe, [-60, -40, -20])
acao_controlador[AC_M] = fuzz.trimf(acao_controlador.universe, [-30, 0, 30])
acao_controlador[AC_AM] = fuzz.trimf(acao_controlador.universe, [20, 40, 60])
acao_controlador[AC_AF] = fuzz.trimf(acao_controlador.universe, [50, 75, 100])

# Rules
rule1 = ctrl.Rule(temperatura_ambiente[TA_MF] & temperatura_variacao[TV_E] & temperatura_externa[TE_MF], acao_controlador[AC_AF])
rule2 = ctrl.Rule(temperatura_ambiente[TA_F] & temperatura_variacao[TV_C] & temperatura_externa[TE_FE], acao_controlador[AC_AM])
rule3 = ctrl.Rule(temperatura_ambiente[TA_C] & temperatura_variacao[TV_E] & temperatura_externa[TE_AM], acao_controlador[AC_M])
rule4 = ctrl.Rule(temperatura_ambiente[TA_Q] & temperatura_variacao[TV_D] & temperatura_externa[TE_QE], acao_controlador[AC_RM])
rule5 = ctrl.Rule(temperatura_ambiente[TA_MQ] & temperatura_variacao[TV_E] & temperatura_externa[TE_MQE], acao_controlador[AC_RF])

tipping_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5])
tipping = ctrl.ControlSystemSimulation(tipping_ctrl)

# Plotar as funções de pertinência
temperatura_ambiente.view()
temperatura_variacao.view()
temperatura_externa.view()
acao_controlador.view()

# execução
tipping.input['temperatura_ambiente'] = 15
tipping.input['temperatura_variacao'] = 1
tipping.input['temperatura_externa'] = 10

tipping.compute()

resultado = tipping.output['acao_controlador']
print(f"Ação do controlador: {abs(round(resultado,2))}%")

acao_controlador.view(sim=tipping)

input(" ")
