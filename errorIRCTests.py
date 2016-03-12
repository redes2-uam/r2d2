# -*- coding: utf-8 -*-
import logging, re, ircTests
from ircTests import IRCTest, TipoTest        
from codes import codes

class AdvancedTest(IRCTest):
    
    tipoTest = TipoTest.ERRORES
    
    def getScore(self):                
        return self.errorTestsScore/float(len(ircTests.errorTestsList)) 
        
"""
    Intento de abandonar un canal inexistente
    
    DEPENDENCIAS: LIST 
"""
class TestAbandonarCanalInexistente(AdvancedTest):
    
    def execute(self):                       
         
        # Conexión        
        self.ircServer.connect(self.testNick)
        
        # Generación de un canal temporal aleatorio...pero no hacemos JOIN
        tempCanal = self.ircServer.generateRandomString()        
        
        # Ahora enviamos el comando            
        self.ircServer.send(self.testNick, "PART #%s :Adios, mundo cruel!" % tempCanal)        
        self.ircServer.expect(self.testNick, r":\S+ %s %s #%s :\S+" % \
                              (codes['ERR_NOSUCHCHANNEL'], self.testNick, tempCanal))
                
        #Todo ha ido bien
        return self.getScore()        
    
    def getDescription(self):
        return type(self).__name__ + " - Intenta abandonar un canal inexistente" 
        
    def getInfo(self):
        return """Esta prueba comprueba que el servidor devuelve un código ERR_NOSUCHCHANNEL
cuando se intenta abandonar un canal inexistente"""
            
"""
    Tests que comprueba un comando JOIN malformado (sin argumentos)
    
    DEPENDENCIAS: LIST 
"""
class TestJoinSinArgumentos(AdvancedTest):
    
    def execute(self):                       
         
        # Conexión al servidor        
        self.ircServer.connect(self.testNick)
        
        # Envio de comando sin argumentos
        self.ircServer.send(self.testNick, "JOIN")
        self.ircServer.expect(self.testNick, r":\S+ %s %s JOIN :\S+" % \
                              (codes['ERR_NEEDMOREPARAMS'], self.testNick))
        
        return self.getScore()
    
    def getDescription(self):
        return type(self).__name__ + " - Comprueba el envio de una JOIN malformado" 
        
    def getInfo(self):
        return """Realiza el envio de un comando JOIN malformado (sin argumentos), y 
comprueba que el servidor reacciona correctamente"""            
            
class TestComandoWhoisSinNick(AdvancedTest):
    
    def execute(self):                
        
        self.ircServer.connect(self.testNick)
        
        # Envio del comando malformado (sin nick)                    
        self.ircServer.send(self.testNick, "WHOIS")
        self.ircServer.expect(self.testNick, r":\S+ %s %s :\S+" % \
                              (codes['ERR_NONICKNAMEGIVEN'], self.testNick))                
        
        return self.getScore()
                
    def getDescription(self):
        return type(self).__name__ + " - Envio de un comando WHOIS malformado" 
        
    def getInfo(self):
        return """Envio de un comando WHOIS malformado, sin especificar el usuario. La respuesta 
del servidor debería incluir el código de error ERR_NONICKNAMEGIVEN."""        
        

"""
    Solicita el topic de un canal al que se no ha establecido topic anteriormente. El 
    servidor debería devolver el código 331 "No topic is set"        
    DEPENDENCIAS: Conexión y registro
"""
class TestNoTopic(AdvancedTest):
    
    def execute(self):                

        # Conexión al servidor        
        self.ircServer.connect(self.testNick)
        
        # Creamos un canal de nombre aleatorio
        nuevoCanal = self.ircServer.generateRandomString()
        self.ircServer.joinChannel(self.testNick, nuevoCanal)
        
        # Solicitamos el topic del canal, que debería devolver un código RPL_NOTOPIC        
        self.ircServer.send(self.testNick, "TOPIC #%s" % nuevoCanal)                
        self.ircServer.expect(self.testNick, r":\S+ %s %s #%s :\S+" % \
                              (codes['RPL_NOTOPIC'], self.testNick, nuevoCanal))                        
        
        # Toda ha ido bien
        return self.getScore()                    
    
    def getDescription(self):
        return type(self).__name__ + " - Solicita el cambio del topic de un canal sin topic establecido" 
        
    def getInfo(self):
        return """Solicita el topic de un canal al que se no ha establecido topic anteriormente. El 
servidor debería devolver el código 331 (No topic is set)"""   
        

class TestMensajePrivadoANadie(AdvancedTest):
    
    def execute(self):
        
        # Conexión de dos usuarios al servidor
        self.ircServer.connect(self.testNick)
        nuevoNick = self.ircServer.generateRandomString()
        
        # Enviamos el mensaje a un usuario no existente
        self.ircServer.send(self.testNick, "PRIVMSG %s :Luke, ¡yo soy tu padre!" % nuevoNick)
        self.ircServer.expect(self.testNick, r":\S+ 401 %s %s :.*" % (self.testNick, nuevoNick))        
    
        # Todo ha ido bien
        return self.getScore()
    
    def getDescription(self):
        return type(self).__name__ + " - Intenta el envio de un mensaje a un usuario inexistente" 
        
    def getInfo(self):
        return """Comprueba que el envio de un mensaje privado a un usuario inexistente falla 
" y devuelve el código de error apropiado"""         
                    
    
class TestPruebaEstres(AdvancedTest):
    
    def execute(self):                
                    
        # Conectamos dos usuarios
        self.ircServer.connect(self.testNick)
        self.ircServer.connect(self.testNick2)
        
        # Creamos un canal aleatorio
        nuevoCanal = self.ircServer.generateRandomString()        
    
        # Enviamos el mensaje a un usuario no existente
        self.ircServer.joinChannel(self.testNick, nuevoCanal)
        self.ircServer.joinChannel(self.testNick2, nuevoCanal)
        
        # Enviamos multitud de mensajes privados
        for i in range(0,100):
            nuevoMensaje = self.ircServer.generateRandomString()
            self.ircServer.sendMessageToUser(self.testNick, self.testNick2, nuevoMensaje)
            
        # Ahora en el canal
        for i in range(0,100):
            nuevoMensaje = self.ircServer.generateRandomString()
            
            self.ircServer.sendMessageToChannel(self.testNick, [self.testNick2], nuevoCanal, nuevoMensaje)                            
                                    
        # Todo ha ido bien
        return self.getScore()                                
    
    def getDescription(self):
        return type(self).__name__ + " - Realiza una prueba de estrés al servidor" 
        
    def getInfo(self):
        return """Realiza una prueba de estrés al servidor, enviando muy rápidamente multitud de
mensajes privados a un usuario, y a un canal general"""         
        

"""
    Este test genera un comando y argumentos inexistentes de forma aleatoria, los 
    envía al servidor y  espera la respuesta, que debería ser un comando 421 (ERR_UNKNOWNCOMMAND)
    DEPENDENCIAS: Conexión
"""
class TestComandoDesconocido(AdvancedTest):
    
    def execute(self):                
            
        # Conexión con el servidor
        self.ircServer.connect(self.testNick)
        
        # Generamos un comando inexistente y sus argumentos de forma aleatoria        
        command = self.ircServer.generateRandomString().upper()
        args = self.ircServer.generateRandomString()
        self.ircServer.send(self.testNick, "%s %s" % (command, args))
        self.ircServer.expect(self.testNick, r":\S+ 421 %s %s :.*" % (self.testNick, command))
        
        #Todo ha ido bien
        return self.getScore()        
    
    def getDescription(self):
        return type(self).__name__ + " - Envia un comando desconocido (no definido) al servidor" 
        
    def getInfo(self):
        return """Este test genera un comando y argumentos inexistentes de forma aleatoria, los 
    envía al servidor y  espera la respuesta, que debería ser un comando 421 (ERR_UNKNOWNCOMMAND)"""        
        
