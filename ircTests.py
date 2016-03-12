# -*- coding: utf-8 -*-
import abc
from ircServer import IRCServer
 
"""
    Clase abstracta que define un test genérico
"""
class IRCTest(object):
    __metaclass__ = abc.ABCMeta    
    
    def __init__(self, sDroid):
        self.sd = sDroid
        self.ircServer = IRCServer(self.sd)
        self.testNick = "yoda"                
        self.testNick2 = "luke"        
        
        # Puntuaciones máximas de cada tipo de prueba
        self.basicTestsScore = 3
        self.advancedTestsScore = 2
        self.errorTestsScore = 1
        
    @abc.abstractmethod
    def execute(self):
        """ Ejecuta el test """
        return
    
    @abc.abstractmethod
    def getDescription(self):
        """ Devuelve la puntuación si el test se ejecuta correctamente """
        return
    
    @abc.abstractmethod
    def getInfo(self):
        """ Muestra información sobre el test """
        return
    
    @abc.abstractmethod
    def getScore(self):
        """ Devuelve la puntuación si el test se ejecuta correctamente """
        return

class TipoTest:
    EMPAQUETADO = 'EM'
    BASICO = 'B'
    AVANZADO = 'A'
    ERRORES = 'E'
    
import basicIRCTests, advancedIRCTests, errorIRCTests

basicTestsList = [basicIRCTests.TestConexionRegistro,
                  basicIRCTests.TestComandoJoin,
                  basicIRCTests.TestComandoList,
                  basicIRCTests.TestComandoWhois,
                  basicIRCTests.TestComandoNames,
                  basicIRCTests.TestMensajePrivado,
                  basicIRCTests.TestMensajeACanal,
                  basicIRCTests.TestCambioNick,
                  basicIRCTests.TestPingPong,
                  basicIRCTests.TestAbandonarCanal,
                  basicIRCTests.TestCambioTopic,
                  basicIRCTests.TestComandoKick,
                  basicIRCTests.TestEmpaquetado]

advancedTestsList = [advancedIRCTests.TestComandoAway,
                     advancedIRCTests.TestModoProteccionTopic,
                     advancedIRCTests.TestModoCanalSecreto,
                     advancedIRCTests.TestModoCanalProtegidoClave,
                     advancedIRCTests.TestComandoQuit,
                     advancedIRCTests.TestComandoMOTD]
                     #advancedIRCTests.TestComandoDCCSend,                     

errorTestsList = [errorIRCTests.TestAbandonarCanalInexistente,
                     errorIRCTests.TestJoinSinArgumentos,
                     errorIRCTests.TestNoTopic,
                     errorIRCTests.TestMensajePrivadoANadie,                     
                     errorIRCTests.TestComandoDesconocido,
                     errorIRCTests.TestComandoWhoisSinNick,
                     errorIRCTests.TestPruebaEstres]